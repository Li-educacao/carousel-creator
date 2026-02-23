/**
 * @module ModelRouter
 * @description Intelligent model routing engine for AIOS subagent spawning
 * @version 1.0.0
 *
 * Routes tasks to the optimal Claude model (opus/sonnet/haiku) based on
 * a 7-level priority cascade defined in model-routing-rules.yaml.
 *
 * Priority cascade:
 *   1. manual_override   — User passes --model=X
 *   2. task_override     — Regex match on task name
 *   3. agent_default     — Per-agent model assignment
 *   4. complexity_score  — Annotated complexity tier
 *   5. performance_hints — Token estimate heuristics
 *   6. task_model_hint   — Optional model_hint in task metadata
 *   7. global_default    — Fallback (sonnet)
 */

'use strict';

const fs = require('fs');
const path = require('path');

const VALID_MODELS = ['opus', 'sonnet', 'haiku'];

class ModelRouter {
  /**
   * @param {Object} options
   * @param {string} options.rulesPath - Path to model-routing-rules.yaml
   * @param {string} options.logPath   - Path to routing-log.jsonl
   * @param {string} options.globalDefault - Fallback model (default: sonnet)
   */
  constructor(options = {}) {
    this.rulesPath = options.rulesPath || null;
    this.logPath = options.logPath || null;
    this.globalDefault = options.globalDefault || 'sonnet';
    this.rules = null;
  }

  /**
   * Load and parse rules from YAML file.
   * Uses a simple YAML parser (key: value) since we avoid external deps.
   * In practice, the orchestrator reads the YAML and passes it as object.
   * @param {Object} rulesObject - Pre-parsed rules object
   */
  loadRules(rulesObject) {
    this.rules = rulesObject;
  }

  /**
   * Route a task to the optimal model.
   *
   * @param {Object} context
   * @param {string} [context.manualOverride]  - Explicit model from --model= flag
   * @param {string} [context.taskName]        - Task being executed
   * @param {string} [context.agentId]         - Active agent (without @)
   * @param {number} [context.complexityScore] - Annotated complexity (1-25)
   * @param {number} [context.estimatedTokens] - Estimated token usage
   * @param {string} [context.taskModelHint]   - model_hint from task metadata
   * @returns {Object} { model, reason, priority, estimatedCost, savings }
   */
  route(context = {}) {
    if (!this.rules) {
      return this._result(this.globalDefault, 'No rules loaded — using global default', 7);
    }

    // Priority 1: Manual override
    if (context.manualOverride && VALID_MODELS.includes(context.manualOverride)) {
      return this._result(context.manualOverride, `Manual override: --model=${context.manualOverride}`, 1);
    }

    // Priority 2: Task override (regex match)
    if (context.taskName && this.rules.task_overrides) {
      for (const override of this.rules.task_overrides) {
        const regex = new RegExp(override.pattern);
        if (regex.test(context.taskName)) {
          return this._result(override.model, `Task override: ${override.reason} (${override.pattern})`, 2);
        }
      }
    }

    // Priority 3: Agent default
    if (context.agentId && this.rules.agent_defaults) {
      const normalizedAgent = context.agentId.replace('@', '').toLowerCase();
      const agentConfig = this.rules.agent_defaults[normalizedAgent];
      if (agentConfig) {
        return this._result(agentConfig.model, `Agent default: @${normalizedAgent} → ${agentConfig.reason}`, 3);
      }
    }

    // Priority 4: Complexity score
    if (context.complexityScore != null && this.rules.complexity_tiers) {
      for (const [, tier] of Object.entries(this.rules.complexity_tiers)) {
        const [min, max] = tier.range;
        if (context.complexityScore >= min && context.complexityScore <= max) {
          return this._result(tier.model, `Complexity tier: score ${context.complexityScore} → ${tier.description}`, 4);
        }
      }
    }

    // Priority 5: Performance hints (token estimate)
    if (context.estimatedTokens != null && this.rules.performance_hints) {
      const thresholds = this.rules.performance_hints.token_thresholds;
      if (thresholds) {
        if (context.estimatedTokens <= thresholds.haiku_max) {
          return this._result('haiku', `Token estimate: ${context.estimatedTokens} ≤ ${thresholds.haiku_max}`, 5);
        } else if (context.estimatedTokens <= thresholds.sonnet_max) {
          return this._result('sonnet', `Token estimate: ${context.estimatedTokens} ≤ ${thresholds.sonnet_max}`, 5);
        } else {
          return this._result('opus', `Token estimate: ${context.estimatedTokens} > ${thresholds.sonnet_max}`, 5);
        }
      }
    }

    // Priority 6: Task model hint (metadata)
    if (context.taskModelHint && VALID_MODELS.includes(context.taskModelHint)) {
      return this._result(context.taskModelHint, `Task model_hint: ${context.taskModelHint}`, 6);
    }

    // Priority 7: Global default
    return this._result(this.globalDefault, `Global default: ${this.globalDefault}`, 7);
  }

  /**
   * Build result object with cost estimation.
   * @private
   */
  _result(model, reason, priority) {
    const costs = this._getCosts(model);
    const baselineCosts = this._getCosts('opus');

    // Estimate for a "typical" task (5K input, 2K output tokens)
    const typicalInput = 5000;
    const typicalOutput = 2000;

    const estimatedCost = (typicalInput / 1e6) * costs.input + (typicalOutput / 1e6) * costs.output;
    const baselineCost = (typicalInput / 1e6) * baselineCosts.input + (typicalOutput / 1e6) * baselineCosts.output;
    const savings = baselineCost - estimatedCost;
    const savingsPercent = baselineCost > 0 ? ((savings / baselineCost) * 100).toFixed(1) : '0.0';

    return {
      model,
      reason,
      priority,
      estimatedCost: `$${estimatedCost.toFixed(4)}`,
      baselineCost: `$${baselineCost.toFixed(4)}`,
      savings: `$${savings.toFixed(4)} (${savingsPercent}%)`,
    };
  }

  /**
   * Get cost rates for a model from loaded rules.
   * @private
   */
  _getCosts(model) {
    const defaults = {
      opus: { input: 15.0, output: 75.0 },
      sonnet: { input: 3.0, output: 15.0 },
      haiku: { input: 0.25, output: 1.25 },
    };

    if (this.rules && this.rules.models && this.rules.models[model]) {
      return {
        input: this.rules.models[model].cost_per_mtok_input,
        output: this.rules.models[model].cost_per_mtok_output,
      };
    }

    return defaults[model] || defaults.sonnet;
  }

  /**
   * Log a routing decision to JSONL file.
   * @param {Object} decision - Result from route()
   * @param {Object} context  - Original routing context
   */
  log(decision, context = {}) {
    if (!this.logPath) return;

    const entry = {
      timestamp: new Date().toISOString(),
      model: decision.model,
      reason: decision.reason,
      priority: decision.priority,
      estimatedCost: decision.estimatedCost,
      savings: decision.savings,
      context: {
        taskName: context.taskName || null,
        agentId: context.agentId || null,
        manualOverride: context.manualOverride || null,
      },
    };

    try {
      const logDir = path.dirname(this.logPath);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      fs.appendFileSync(this.logPath, JSON.stringify(entry) + '\n');
    } catch {
      // Silently fail — logging should never break routing
    }
  }

  /**
   * Format a routing decision for display.
   * @param {Object} decision - Result from route()
   * @returns {string} Formatted string
   */
  static formatDecision(decision) {
    const icon = { opus: '\u{1F9E0}', sonnet: '\u26A1', haiku: '\u{1F343}' }[decision.model] || '\u2753';
    return [
      `${icon} Model: ${decision.model} (P${decision.priority})`,
      `   Reason: ${decision.reason}`,
      `   Cost: ${decision.estimatedCost} | Baseline: ${decision.baselineCost} | Savings: ${decision.savings}`,
    ].join('\n');
  }
}

/**
 * Create a ModelRouter instance from config.
 * @param {Object} config - From core-config.yaml modelRouting section
 * @returns {ModelRouter}
 */
function createModelRouter(config = {}) {
  return new ModelRouter({
    rulesPath: config.rulesFile || null,
    logPath: config.logFile || null,
    globalDefault: config.globalDefault || 'sonnet',
  });
}

module.exports = {
  ModelRouter,
  createModelRouter,
  VALID_MODELS,
};
