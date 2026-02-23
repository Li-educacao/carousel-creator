---

## Task Definition (AIOS Task Format V1.0)

```yaml
task: modelCostReport()
responsavel: Orion (Commander)
responsavel_type: Agente
atomic_layer: Analytics

**Entrada:**
- campo: period
  tipo: string
  origem: User Input
  obrigatório: false
  validação: "today | week | month | all (default: all)"

- campo: group_by
  tipo: string
  origem: User Input
  obrigatório: false
  validação: "model | task | agent (default: model)"

**Saída:**
- cost_report: Formatted cost analysis report
```

---

## Steps

### Step 1: Load Data

1. Read `core-config.yaml` → `modelRouting.logFile` path
2. Read the JSONL file (each line is a JSON routing decision)
3. If file not found or empty: report "No routing data yet. Run workflows with model routing enabled to collect data."

### Step 2: Filter by Period

- `today` — entries from current date
- `week` — entries from last 7 days
- `month` — entries from last 30 days
- `all` — all entries (default)

### Step 3: Aggregate Metrics

For each group (model, task, or agent):
- Count of routing decisions
- Total estimated cost
- Total baseline cost (all-opus)
- Total savings
- Savings percentage

### Step 4: Display Report

```
💰 Model Routing Cost Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Period: {period} ({entry_count} routing decisions)

📊 By {group_by}:
┌──────────────┬───────┬──────────────┬──────────────┬──────────────┬─────────┐
│ {Group}      │ Count │ Est. Cost    │ Baseline     │ Savings      │ %       │
├──────────────┼───────┼──────────────┼──────────────┼──────────────┼─────────┤
│ haiku        │ 42    │ $0.0105      │ $0.4200      │ $0.4095      │ 97.5%   │
│ sonnet       │ 28    │ $0.1260      │ $0.2800      │ $0.1540      │ 55.0%   │
│ opus         │ 10    │ $0.2250      │ $0.2250      │ $0.0000      │ 0.0%    │
├──────────────┼───────┼──────────────┼──────────────┼──────────────┼─────────┤
│ TOTAL        │ 80    │ $0.3615      │ $0.9250      │ $0.5635      │ 60.9%   │
└──────────────┴───────┴──────────────┴──────────────┴──────────────┴─────────┘

💡 Summary: Saved $0.5635 (60.9%) vs running everything on Opus.
```

### Step 5: Script Execution

The report can also be generated programmatically:

```bash
node .aios-core/development/scripts/generate-cost-report.js [--period=all] [--group-by=model]
```

---

## Examples

```
*cost-report
*cost-report --period=today
*cost-report --period=week --group-by=agent
*cost-report --group-by=task
```
