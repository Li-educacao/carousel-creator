---

## Task Definition (AIOS Task Format V1.0)

```yaml
task: configureModelRouting()
responsavel: Orion (Commander)
responsavel_type: Agente
atomic_layer: Config

**Entrada:**
- campo: action
  tipo: string
  origem: User Input
  obrigatório: true
  validação: "show | test | enable | disable"

- campo: task_name
  tipo: string
  origem: User Input
  obrigatório: false
  validação: Task name to test routing for (required when action=test)

- campo: model_override
  tipo: string
  origem: User Input
  obrigatório: false
  validação: "opus | sonnet | haiku (simulates --model= override)"

- campo: agent_id
  tipo: string
  origem: User Input
  obrigatório: false
  validação: Agent to simulate (e.g. dev, architect)

**Saída:**
- routing_display: Formatted routing information
```

---

## Steps

### Step 1: Load Configuration

1. Read `core-config.yaml` → `modelRouting` section
2. Read `model-routing-rules.yaml` from path in `modelRouting.rulesFile`
3. If file not found, report error and stop

### Step 2: Execute Action

#### Action: `show`

Display current configuration:

```
🧭 Model Routing Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: {enabled/disabled}
Global Default: {globalDefault}
Rules File: {rulesFile}
Log File: {logFile}

📋 Agent Defaults:
┌─────────────────────┬─────────┬─────────────────────────────────┐
│ Agent               │ Model   │ Reason                          │
├─────────────────────┼─────────┼─────────────────────────────────┤
│ @architect          │ opus    │ Architectural decisions...       │
│ @dev                │ sonnet  │ Implementation tasks...          │
│ @data-collector     │ haiku   │ Mechanical ETL collection        │
│ ...                 │ ...     │ ...                             │
└─────────────────────┴─────────┴─────────────────────────────────┘

📋 Task Overrides:
┌─────────────────────┬─────────┬─────────────────────────────────┐
│ Pattern             │ Model   │ Reason                          │
├─────────────────────┼─────────┼─────────────────────────────────┤
│ ^validate-.*        │ haiku   │ Validation is mechanical         │
│ ^architect-review.* │ opus    │ Architecture review...           │
│ ...                 │ ...     │ ...                             │
└─────────────────────┴─────────┴─────────────────────────────────┘

📋 Priority Cascade:
  1. Manual override (--model=X)
  2. Task override (regex match)
  3. Agent default
  4. Complexity score
  5. Performance hints (token estimate)
  6. Task model_hint (metadata)
  7. Global default → {globalDefault}
```

#### Action: `test`

Simulate routing for a task:

1. Build context from provided parameters:
   - `taskName` = provided task_name
   - `agentId` = provided agent_id (or null)
   - `manualOverride` = provided model_override (or null)
2. Run through 7-level priority cascade
3. Display result:

```
🧭 Routing Test
━━━━━━━━━━━━━━━

Input:
  Task: {task_name}
  Agent: {agent_id or "none"}
  Override: {model_override or "none"}

Result:
  🧠 Model: {model} (Priority {priority})
  📝 Reason: {reason}
  💰 Estimated Cost: {estimatedCost}
  💚 Savings vs Opus: {savings}
```

#### Action: `enable`

1. Set `modelRouting.enabled: true` in `core-config.yaml`
2. Confirm: `✅ Model routing ENABLED`

#### Action: `disable`

1. Set `modelRouting.enabled: false` in `core-config.yaml`
2. Confirm: `⛔ Model routing DISABLED — all subagents will use Claude Code default model`

---

## Examples

```
*model-routing show
*model-routing test validate-agents
*model-routing test dev-develop-story --agent=dev
*model-routing test architect-review --model=haiku
*model-routing enable
*model-routing disable
```
