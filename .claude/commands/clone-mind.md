# clone-mind

Orquestração do pipeline completo de clonagem cognitiva DNA Mental™ — 6 fases, 15 agentes, 30+ tasks.

**Triggers:** "clone mind", "clonar mente", "/clone-mind", "build mind", "*build-mind", "*map"

## Identity

**Orchestrator:** `@mind-mapper` (mmos-squad) — single entry point via `*map {name}`
**Squad:** `squads/mmos-squad/` (MMOS v3.0.1)
**Pipeline Task:** `squads/mmos-squad/tasks/map-mind.md` (auto-detect workflow)
**Legacy Pipeline:** `squads/mmos-squad/tasks/execute-mmos-pipeline.md` (manual 6-phase)
**Gold Standard:** `outputs/minds/lawhander-climatronico/`

## How to Execute

1. Read the COMPLETE agent definition at `squads/mmos-squad/agents/mind-mapper.md`
2. Adopt the Mind Mapper persona (🧠 Cognitive Archaeologist)
3. Execute `*map {name}` — auto-detects greenfield/brownfield, public/no-public
4. The pipeline orchestrates all 15 agents automatically by phase

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| `name` | Yes | Subject identifier (e.g., `gary_halbert`, `naval_ravikant`) |
| `--force-mode` | No | Override auto-detection: `public`, `no-public-interviews`, `no-public-materials` |
| `--materials-path` | No | Path to pre-collected materials |
| `--start-phase` | No | Resume from specific phase: `viability`, `research`, `analysis`, `synthesis`, `implementation`, `testing` |

## Pipeline — 6 Phases

```
PHASE 0 → Viability    : APEX + ICP scoring, GO/NO-GO decision
PHASE 1 → Research     : Source collection (ETL squad delegation)
PHASE 2 → Analysis     : 8-layer cognitive extraction (parallel agents)
PHASE 3 → Synthesis    : Identity-core + meta-axioms + synthesis artifacts
PHASE 4 → Implementation : System prompt compilation + operational manual
PHASE 5 → Testing      : Fidelity scoring + blind testing + quality gates
```

### PHASE 0 — Viability (🎲 Victoria)

**Agent:** `@victoria-viability-specialist`
**Task:** `squads/mmos-squad/tasks/viability-assessment.md`

- APEX scoring across 6 dimensions (Content Depth, Source Diversity, Uniqueness, Demand, Complexity, Accessibility)
- ICP (Ideal Clone Profile) matching
- GO/NO-GO decision with ROI estimation
- **Gate:** Score < 50 = NO-GO, 50-69 = conditional, 70+ = GO

### PHASE 1 — Research Collection (📚 Research Specialist + ETL Squad)

**Agent:** `@research-specialist`
**Task:** `squads/mmos-squad/tasks/research-collection.md`
**Delegation:** `@data-collector` (etl-squad) for actual collection

| Source | ETL Script | Output |
|--------|-----------|--------|
| YouTube (canal próprio) | `squads/etl-squad/bin/collect-youtube.js` | Transcripts .md por vídeo |
| YouTube (entrevistas) | youtube-specialist + busca ativa | Transcripts .md (outros canais) |
| Blogs | `squads/etl-squad/bin/collect-blog.js` | Posts .md |
| Podcasts | youtube-specialist + `speaker-filter.js` | Filtered transcripts |
| Books/PDFs | document-specialist | Chapters .md |
| Social | social-specialist + Apify MCP | Posts .json/.md |

**CRITICAL — YouTube deve cobrir DUAS categorias:**
1. **Canal próprio** — Todos os vídeos do canal oficial da mente (palestras, aulas, conteúdo original)
2. **Entrevistas/Participações** — Buscar ativamente `"{nome}" entrevista`, `"{nome}" podcast`, `"{nome}" interview` no YouTube para encontrar aparições em outros canais. Entrevistas revelam camadas cognitivas diferentes do conteúdo próprio (respostas espontâneas, pressão do entrevistador, contradições naturais)

**CRITICAL:** `speaker-filter.js` DEVE ser aplicado em entrevistas e podcasts para filtrar APENAS as falas do sujeito, removendo perguntas do entrevistador.

**Gate:** Minimum 5 sources across 2+ categories.

### PHASE 2 — Analysis (🔍 Daniel + 🏗️ Barbara + 🔬 Cognitive Analyst + 💎 Sarah)

**Parallel execution — agents work on different layers simultaneously:**

| Agent | Layers | Focus |
|-------|--------|-------|
| 🔍 Daniel (`@daniel-behavioral-analyst`) | L2-L3 | Behavioral patterns, writing style, routines |
| 🏗️ Barbara (`@barbara-cognitive-architect`) | L4-L5 | Mental models, recognition patterns, frameworks |
| 🔬 Cognitive Analyst (`@cognitive-analyst`) | L1, L6-L8 | Observable behaviors + deep identity layers |
| 💎 Sarah (`@identity-analyst`) | L6-L8 | Values hierarchy, obsessions, paradoxes |

**Human Checkpoints:** Layers 6, 7, and 8 (values, obsessions, contradictions) require human validation before proceeding.

**Analysis outputs (5 files):**

| # | Output | Depends On |
|---|--------|------------|
| 1 | `analysis/cognitive-spec.yaml` | — |
| 2 | `analysis/mental-models.yaml` | #1 |
| 3 | `analysis/linguistic-patterns.yaml` | #1 |
| 4 | `analysis/psychometric-profile.yaml` | #1, #3 |
| 5 | `analysis/decision-matrix.yaml` | #2, #4 |

**Layer artifacts (9 files, parallel):**

| Artifact | Layer | Human Checkpoint |
|----------|-------|-----------------|
| `behavioral_patterns.yaml` | L1 | No |
| `writing_style.yaml` | L2 | No |
| `routine_analysis.yaml` | L3 | No |
| `recognition_patterns.yaml` | L4 | No |
| `values_hierarchy.yaml` | L6 | **YES** |
| `core_obsessions.yaml` | L7 | **YES** |
| `contradictions.yaml` | L8 (GOLD LAYER) | **YES** |
| `anecdotes.yaml` | Stories/metaphors | No |
| `voice_guide.md` | Golden rules, DO/DON'T | No |

### PHASE 3 — Synthesis (🔬 Charlie + 🔧 Constantin)

**Agents:**
- 🔬 Charlie (`@charlie-synthesis-expert`) — Synthesis compilation
- 🔧 Constantin (`@constantin-implementation-architect`) — Identity DNA + meta-axioms

**Task:** `squads/mmos-squad/tasks/build-synthesis-artifacts.md`

1. **identity-core.yaml** (MASTER REF) — Must be first
2. Then in parallel:
   - `memory-system.yaml`
   - `frameworks_synthesized.md`
   - `communication_templates.md`
   - `tools.md`
   - `decision_patterns.md`
   - `psychometric_profile.json`

### PHASE 4 — Implementation (⚙️ System Prompt Architect)

**Agent:** `@system-prompt-architect`
**Task:** `squads/mmos-squad/tasks/system-prompt-creation.md`

| Output | Description |
|--------|-------------|
| `system_prompts/system-prompt-generalista.md` | Production system prompt (**HUMAN CHECKPOINT**) |
| `system_prompts/history.yaml` | Version tracking |
| `system_prompts/metadata.yaml` | Pipeline metadata, APEX scoring |
| `README.md` | Project overview |

### PHASE 5 — Testing & Quality (✅ Quinn + ⚔️ Debate)

**Agents:**
- ✅ Quinn (`@quinn-quality-specialist`) — Completeness + fidelity scoring + quality gates
- ⚔️ Debate (`@debate`) — Adversarial fidelity testing against source material

**Tasks:**
- `squads/mmos-squad/tasks/mind-validation.md` (20 checks, 4 categories)
- `squads/mmos-squad/tasks/test-fidelity.md` (blind testing)

**Scoring:** Minimum 70% (14/20), Target 94%+ (19/20).
**If fail:** Return to PHASE 2 with audit notes.

### Post-Pipeline — Activation (🪞 Mirror)

**Agent:** `@emulator` (Mirror)
**Task:** `squads/mmos-squad/tasks/activate-clone.md`

Load the generated system prompt and activate the clone for conversational testing.

## Legendary Agents (15 Total)

| Icon | Name | Agent ID | Phase | Role |
|------|------|----------|-------|------|
| 🧠 | Mind Mapper | `mind-mapper` | Orchestrator | Pipeline orchestration, auto-detection |
| 🎲 | Victoria | `victoria-viability-specialist` | 0 | APEX scoring, GO/NO-GO |
| 📚 | Research Specialist | `research-specialist` | 1 | Source discovery & collection |
| 📥 | DataSync | `data-importer` | 1 | Data import & validation |
| 🔍 | Daniel | `daniel-behavioral-analyst` | 2 | Behavioral patterns, L2-L3 |
| 🏗️ | Barbara | `barbara-cognitive-architect` | 2 | Mental models, L4-L5 |
| 🔬 | Cognitive Analyst | `cognitive-analyst` | 2 | 8-layer deep analysis |
| 💎 | Sarah | `identity-analyst` | 2 | Values, obsessions, paradoxes L6-L8 |
| 🔬 | Charlie | `charlie-synthesis-expert` | 3 | Synthesis compilation |
| 🔧 | Constantin | `constantin-implementation-architect` | 4 | Identity DNA, meta-axioms |
| ⚙️ | System Prompt Architect | `system-prompt-architect` | 4 | System prompt compilation |
| 🎯 | Mind PM | `mind-pm` | All | Pipeline project management |
| ✅ | Quinn | `quinn-quality-specialist` | 5 | Quality gates, fidelity scoring |
| ⚔️ | Debate | `debate` | 5 | Adversarial fidelity testing |
| 🪞 | Mirror | `emulator` | Post | Clone activation & testing |

## Squad Dependencies

| Squad | Role | Path |
|-------|------|------|
| **mmos-squad** | Full pipeline orchestration + all agents | `squads/mmos-squad/` |
| **etl-squad** | Source collection (Phase 1) | `squads/etl-squad/` |
| **mind-builder** | Legacy lite pipeline (single agent) | `squads/mind-builder/` |

## File Resolution

- Agents → `squads/mmos-squad/agents/{name}`
- Tasks → `squads/mmos-squad/tasks/{name}`
- Templates → `squads/mmos-squad/minds/_template/`
- Checklists → `squads/mmos-squad/tasks/` (embedded)
- Data → `squads/mmos-squad/data/`
- Lib → `squads/mmos-squad/lib/` (Python utilities)
- ETL Scripts → `squads/etl-squad/scripts/` and `squads/etl-squad/bin/`
- Output → `outputs/minds/{name}/` (symlinked to squad minds/)

## Output Structure

```
outputs/minds/{name}/
├── README.md
├── viability/
│   ├── viability-output.yaml
│   └── prd.md
├── sources/
│   ├── sources_master.yaml
│   └── downloads/
│       ├── blogs/
│       ├── youtube/
│       ├── podcasts/
│       ├── books/
│       └── social/
├── analysis/                          (5 files)
│   ├── cognitive-spec.yaml
│   ├── mental-models.yaml
│   ├── linguistic-patterns.yaml
│   ├── psychometric-profile.yaml
│   └── decision-matrix.yaml
├── artifacts/                         (16 files)
│   ├── behavioral_patterns.yaml       (L1)
│   ├── writing_style.yaml             (L2)
│   ├── routine_analysis.yaml          (L3)
│   ├── recognition_patterns.yaml      (L4)
│   ├── values_hierarchy.yaml          (L6 🔴)
│   ├── core_obsessions.yaml           (L7 🔴)
│   ├── contradictions.yaml            (L8 🔴 GOLD)
│   ├── anecdotes.yaml
│   ├── voice_guide.md
│   ├── identity-core.yaml             (MASTER REF)
│   ├── memory-system.yaml
│   ├── frameworks_synthesized.md
│   ├── communication_templates.md
│   ├── tools.md
│   ├── decision_patterns.md
│   └── psychometric_profile.json
├── system_prompts/                    (3 files)
│   ├── system-prompt-generalista.md
│   ├── history.yaml
│   └── metadata.yaml
└── validation/
    └── validation-report.yaml
```

## Quick Start

```
/clone-mind naval_ravikant
```

Or via direct agent activation:
```
@mind-mapper
*map naval_ravikant
```
