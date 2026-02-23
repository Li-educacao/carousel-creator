#!/usr/bin/env node
'use strict';

/**
 * MEMORY INTEGRATION — Connects LocalMemoryBridge to Synapse
 * Automatically learns patterns and injects learned context into rules
 */

const LocalMemoryBridge = require('./local-memory-bridge.js');

class MemoryIntegration {
  constructor(dataDir = '.synapse') {
    this.bridge = new LocalMemoryBridge(dataDir);
  }

  /**
   * Record command execution in memory
   * Called after every command
   */
  recordExecution(command, agent, context = {}) {
    try {
      this.bridge.recordCommand(command, agent, context);
    } catch (err) {
      console.error('[memory-integration] Recording failed:', err.message);
    }
  }

  /**
   * Get suggestions for next command
   * Injected into Synapse context
   */
  getNextSuggestions(currentCommand, agent) {
    try {
      return this.bridge.suggestNext(currentCommand, agent);
    } catch (err) {
      console.error('[memory-integration] Suggestion failed:', err.message);
      return [];
    }
  }

  /**
   * Export memory context for Synapse injection
   * This becomes <synapse-memory> in the rules
   */
  exportForSynapse() {
    try {
      const context = this.bridge.exportContext();
      return {
        memory: {
          learned: true,
          totalCommands: context.totalCommands,
          totalExecutions: context.totalExecutions,
          mostUsed: context.mostUsed,
          agentFrequency: context.byAgent,
          lastUpdated: context.lastUpdated,
        },
      };
    } catch (err) {
      console.error('[memory-integration] Export failed:', err.message);
      return { memory: { learned: false } };
    }
  }

  /**
   * Generate memory hints for Synapse formatter
   * Adds "Learned from X patterns" to output
   */
  getMemoryHints() {
    try {
      const context = this.bridge.exportContext();
      if (context.totalCommands === 0) {
        return 'No patterns learned yet. Start using commands to build memory.';
      }

      const topCmd = context.mostUsed[0];
      return `📚 Learned ${context.totalCommands} patterns from ${context.totalExecutions} executions. ` +
             `Top command: ${topCmd.command} (${topCmd.count}x)`;
    } catch (err) {
      return 'Memory system inactive';
    }
  }

  /**
   * Cleanup old patterns
   * Called periodically (weekly)
   */
  cleanup() {
    try {
      this.bridge.cleanup();
      return 'Cleanup complete';
    } catch (err) {
      console.error('[memory-integration] Cleanup failed:', err.message);
      return 'Cleanup failed';
    }
  }
}

module.exports = MemoryIntegration;

// CLI Usage
if (require.main === module) {
  const integration = new MemoryIntegration();
  const cmd = process.argv[2];

  if (cmd === 'record') {
    const command = process.argv[3];
    const agent = process.argv[4] || '@dev';
    integration.recordExecution(command, agent);
    console.log(`Recorded: ${agent} ${command}`);
  } else if (cmd === 'suggest') {
    const command = process.argv[3] || '*help';
    const agent = process.argv[4] || '@dev';
    const suggestions = integration.getNextSuggestions(command, agent);
    console.log(JSON.stringify(suggestions, null, 2));
  } else if (cmd === 'export') {
    const context = integration.exportForSynapse();
    console.log(JSON.stringify(context, null, 2));
  } else if (cmd === 'hints') {
    console.log(integration.getMemoryHints());
  } else if (cmd === 'cleanup') {
    console.log(integration.cleanup());
  } else {
    console.log(`
Memory Integration CLI

Usage:
  node memory-integration.js record <cmd> [agent]  - Record command execution
  node memory-integration.js suggest <cmd> [agent] - Get next command suggestions
  node memory-integration.js export                - Export Synapse context
  node memory-integration.js hints                 - Show memory summary
  node memory-integration.js cleanup               - Clean old patterns
    `);
  }
}
