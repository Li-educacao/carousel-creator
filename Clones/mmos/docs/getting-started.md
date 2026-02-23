# MMOS — Getting Started

## Quick Reference

### Creating a New Mind Clone

1. Copy the template:
   ```
   cp -r outputs/minds/_template outputs/minds/{mind-name}
   ```

2. Fill in each YAML file in `{mind-name}/analysis/` with the specialist's cognitive DNA

3. Register the mind in `mmos-state.json` under `minds.available`

### Activating a Squad Agent

1. Define the agent in `squads/{squad}/agents/{agent-name}.md`
2. Define its tasks in `squads/{squad}/tasks/`
3. Create workflows in `squads/{squad}/workflows/`
4. Add quality checklists in `squads/{squad}/checklists/`

### Running a Cross-Squad Workflow

1. Define the master workflow referencing steps from multiple squads
2. Each step produces an artifact and updates `mmos-state.json`
3. The next squad picks up the artifact and continues
4. Quality Gates are enforced at each handoff point
