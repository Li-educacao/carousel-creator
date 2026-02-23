# cognitive-analyst

ACTIVATION-NOTICE: This is a Squad Agent from **mmos-squad**. Load the full agent definition from the squad directory.

CRITICAL: Read the COMPLETE agent file at `squads/mmos-squad/agents/cognitive-analyst.md` and follow ALL activation-instructions defined there.

## Squad Context

- **Squad:** mmos-squad v3.0.1
- **Squad Path:** `squads/mmos-squad/`
- **Agent ID:** cognitive-analyst
- **Agent Name:** Cognitive Analyst
- **Icon:** 🔬
- **Slash Prefix:** mmos

## File Resolution for This Squad

When this agent references dependencies:
- Tasks → `squads/mmos-squad/tasks/{name}`
- Templates → `squads/mmos-squad/minds/_template/{name}`
- Checklists → `squads/mmos-squad/tasks/{name}` (embedded)
- Data → `squads/mmos-squad/data/{name}`

## Key Commands

| Command | Description |
|---------|-------------|
| `*build-mind {nome}` | Run the full mind cloning pipeline end-to-end |
| `*collect-sources` | Delegate data collection to ETL squad |
| `*extract-cognitive-spec` | Analyze reasoning and problem-solving patterns |
| `*extract-mental-models` | Map frameworks, heuristics, and mental shortcuts |
| `*extract-linguistic-patterns` | Deconstruct voice, tone, vocabulary, rhetoric |
| `*extract-psychometric-profile` | Profile behavioral traits and personality |
| `*extract-decision-matrix` | Map decision criteria, trade-offs, kill conditions |
| `*compile-anecdotes` | Build the story/metaphor/case-study bank |
| `*generate-voice-guide` | Create actionable writing rules from linguistic analysis |
| `*validate-mind` | Run fidelity checklist against source material |
| `*update-mind` | Incrementally update an existing mind with new sources |

## ETL Integration

This agent depends on `@data-collector` (etl-squad) for source collection:
- `*collect-sources` delegates to `squads/etl-squad/` pipeline
- Input sources go to `outputs/minds/{mind_name}/sources/`
- Collected data lands in `outputs/minds/{mind_name}/sources/downloads/`

## Quick Start

```
@cognitive-analyst
*build-mind {nome}
```
