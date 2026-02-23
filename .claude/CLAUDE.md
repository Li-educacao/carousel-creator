# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Operational Rules

### NEVER
- Implement without showing options first (always 1, 2, 3 format)
- Delete/remove content without asking first
- Delete anything created in the last 7 days without explicit approval
- Change something that was already working
- Pretend work is done when it isn't
- Process batch without validating one first
- Add features that weren't requested
- Use mock data when real data exists in database
- Explain/justify when receiving criticism (just fix)
- Trust AI/subagent output without verification
- Create from scratch when similar exists in squads/

### ALWAYS
- Present options as "1. X, 2. Y, 3. Z" format
- Use AskUserQuestion tool for clarifications
- Check squads/ and existing components before creating new
- Read COMPLETE schema before proposing database changes
- Investigate root cause when error persists
- Commit before moving to next task
- Create handoff in `docs/sessions/YYYY-MM/` at end of session
- **Use Model Routing when spawning subagents** (see Model Routing section below)
- **Use Squad Routing for domain tasks** — scan PRD/story for domain keywords → route to correct squad (see Squad Routing section below)

## Workspace Overview

This is a **multi-project workspace** managed by the **Synkra AIOS framework** (v3.11.3+git, brownfield mode). It contains 7 independent projects under a shared AIOS orchestration layer. The root is NOT a git repo; individual projects have their own git repos.

AIOS core installed from GitHub main (2026-02-11) with features ahead of npm release: Synapse (WIS), Constitution, Quality Gates, Schemas V3. Clone at `Clones/aios-core/` for future updates (`git pull`).

## Synkra AIOS Framework

AIOS is a meta-framework that orchestrates AI agent personas for development workflows. Configuration lives in `.aios-core/` (framework) and `core-config.yaml` (project settings).

### Constitution (v1.0.0)

The AIOS Constitution defines 6 articles with automatic enforcement gates. All agents, tasks, and workflows MUST comply.

| Article | Principle | Level | Gate | Action |
|---------|-----------|-------|------|--------|
| **I** | CLI First | **NON-NEGOTIABLE** | dev-develop-story | WARN if UI created before CLI |
| **II** | Agent Authority | **NON-NEGOTIABLE** | Agent definitions | Only @devops pushes, only @qa gives verdicts, etc. |
| **III** | Story-Driven Dev | **MUST** | dev-develop-story | BLOCK if no valid story |
| **IV** | No Invention | **MUST** | spec-write-spec | BLOCK if spec contains invented features |
| **V** | Quality First | **MUST** | pre-push-quality-gate | BLOCK if lint/test/build/typecheck fails |
| **VI** | Absolute Imports | **SHOULD** | ESLint | INFO only |
| **VII** | Squad First | **MUST** | Workflow steps | WARN if domain squad exists but not used |

**Severity levels:** BLOCK (stops execution), WARN (allows with alert), INFO (report only).

**Self-Critique Checkpoints:**
- **Step 5.5** (after code, before tests): 3+ predicted bugs, 3+ edge cases, error handling, security
- **Step 6.5** (after tests, before done): project patterns, no hardcoded values, tests added, docs updated, no console.log

**Full document:** `.aios-core/constitution.md`

### Synapse — Workflow Intelligence System (WIS)

Intelligent workflow suggestion and learning engine. Provides `*next` suggestions, workflow matching, wave analysis (parallelizable tasks), and pattern learning. Details at `.aios-core/workflow-intelligence/`.

### Quality Gates & Schemas

**Quality system** at `.aios-core/quality/` — 3-layer metrics collection:
- Layer 1: Core dev checks (lint, typecheck, test, build)
- Layer 2: PR automation (CodeRabbit findings, QA agent metrics)
- Layer 3: Final verification

**Schemas V3** at `.aios-core/schemas/` — validation schemas for:
- `agent-v3-schema.json` — Agent capabilities matrix (spec pipeline, execution, recovery, QA, memory, worktree)
- `task-v3-schema.json` — Task metadata (deterministic, composable, pipeline phase, verification, self-critique)
- `squad-schema.json` / `squad-design-schema.json` — Squad structure validation

### Agent System

- **Activation:** `@agent-name` syntax — `@dev`, `@qa`, `@architect`, `@pm`, `@po`, `@sm`, `@analyst`, `@devops`, `@ux-design-expert`, `@data-engineer`, `@squad-creator`, `@aios-master`
- **Commands:** `*` prefix — `*help`, `*create-story`, `*task {name}`, `*workflow {name}`, `*exit`
- **Agent definitions:** `.aios-core/development/agents/` (12 agents in YAML/Markdown)
- **Task templates:** `.aios-core/development/tasks/` (188 task workflows)
- **Workflows:** `.aios-core/development/workflows/` (brownfield-discovery, brownfield-fullstack, greenfield-fullstack, qa-loop, ralph-loop, story-development-cycle, etc.)

### Agent Context Rules

When an agent is active:
- Follow that agent's specific persona and expertise
- Use the agent's designated workflow patterns
- Maintain the agent's perspective throughout the interaction
- Respect agent boundaries — use the appropriate agent for each task
- If MCP management is needed, delegate to `@devops`

### Story-Driven Development

All development follows stories in `docs/stories/`:
1. **Work from stories** — All development starts with a story
2. **Update progress** — Mark checkboxes as tasks complete: `[ ]` → `[x]`
3. **Track changes** — Maintain the File List section in the story
4. **Follow criteria** — Implement exactly what the acceptance criteria specify

Framework docs load from `docs/framework/` (coding-standards.md, tech-stack.md, source-tree.md).

### Brownfield Workflow

This workspace uses brownfield mode (existing projects). Two approaches:
- **PRD-First** (large features): `@pm` → `*create-doc brownfield-prd` → `@analyst` → `*document-project`
- **Quick Enhancement**: `@pm` → `*brownfield-create-epic` or `*brownfield-create-story`

### Workflow Execution

#### Task Execution Pattern
1. Read the complete task/workflow definition
2. Understand all elicitation points
3. Execute steps sequentially
4. Handle errors gracefully
5. Provide clear feedback

#### Interactive Workflows
- Workflows with `elicit: true` require user input
- Present options clearly
- Validate user responses
- Provide helpful defaults

### Key Config Paths

| Path | Purpose |
|------|---------|
| `.aios-core/core-config.yaml` | Framework configuration |
| `.aios-core/constitution.md` | Constitution — principles and gates |
| `.aios-core/development/agents/` | Agent persona definitions |
| `.aios-core/development/tasks/` | Executable task workflows |
| `.aios-core/development/workflows/` | Multi-step workflows |
| `docs/stories/` | Development stories |
| `docs/prd/` | Product requirement docs (sharded) |
| `docs/framework/` | Coding standards, tech stack, source tree |
| `.ai/` | Decision logs (ADR format) |

### AIOS Master Commands

| Command | Purpose |
|---------|---------|
| `*help` | Show available commands |
| `*create-story` | Create new story |
| `*task {name}` | Execute specific task |
| `*workflow {name}` | Run workflow |
| `*create-doc brownfield-prd` | Create brownfield PRD |
| `*brownfield-create-epic` | Quick epic creation |
| `*brownfield-create-story` | Single story creation |
| `*document-project` | Document existing project (via `@analyst`) |
| `*execute-checklist {name}` | Run a validation checklist |

### Testing Requirements

- Run all tests before marking tasks complete
- Ensure linting passes: `npm run lint`
- Verify type checking: `npm run typecheck` (when available)
- Run tests incrementally during development
- Document test scenarios in story files

## Projects

Each project has its own `.claude/CLAUDE.md` with full details. Summary:

| # | Project | Tech | Path |
|---|---------|------|------|
| 1 | **Grupo Lawteck** | React + Vite, Supabase | `grupo-lawteck/` |
| 2 | **Climatronico Blog** | Astro 5, MDX | `climatronico-blog/` |
| 3 | **Relatorios Lawteck** | Python, Selenium | `relatorios_lawteck/` |
| 4 | **Criador de PDFs** | Python | `Criador de PDFs/` |
| 5 | **Landing Page Lawteck** | Static | `Landing page Lawteck peças/` |
| 6 | **Scripts Live** | Shell | `Scripts Live/` |
| 7 | **RepairHub** | React + Vite, Supabase | `RepairHub/` |

## AIOS Squads

Squads are specialized AI agent teams (MMOS mind clones). Repository at `aios-squads/`, symlink `squads/` → `aios-squads/packages/`. **Always check `squads/` before creating from scratch.**

| Squad | Version | Lead | Agents | Purpose |
|-------|---------|------|--------|---------|
| **design-system** | 1.0.0 | @design-chief | 9 (Brad Frost, Draplin, Chris Do, etc.) | Design systems, tokens, branding, WCAG |
| **media-buy-squad** | 1.0.0 | @ad-midas | 5 (Sobral, Kasim, Molly, Tessmann, Finch) | Facebook/Google Ads, traffic, funnels |
| **security-squad** | 1.0.0 | @security-chief | 4 (Schneier, Troy Hunt, Manico, Williams) | Security audits, OWASP, threat modeling |
| **mmos-squad** | 3.0.1 | @mind-mapper | 10 | Cognitive cloning, DNA Mental, 36 minds |
| **etl-squad** | 2.0.0 | @data-collector | 1 | Web scraping, content collection |
| **creator-squad** | 1.0.0 | @expansion-creator | 1 | Expansion pack scaffolding |

**Activation:** Squad dependencies resolve to squad-local paths: `squads/{squad}/tasks|scripts|templates|data/{name}`.
Details: `squads/{squad}/README.md` | Management: `@squad-creator`

## MCP Infrastructure

MCP management is **exclusively** handled by `@devops`. Other agents are consumers only. Native Claude Code tools always preferred over MCP for local operations. Full rules in `.claude/rules/mcp-usage.md`.

## Git & GitHub Integration

### Commit Conventions
- Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, etc.
- Reference story ID: `feat: implement IDE detection [Story 2.1]`
- Atomic, focused commits

### GitHub CLI
- Ensure authenticated: `gh auth status`
- PR creation: `gh pr create`
- Check org access: `gh api user/memberships`

## Environment

- `.env.example` at root documents all available service keys (LLM providers, Supabase, GitHub, ClickUp, N8N, Sentry, Railway, Vercel)
- Individual projects may have their own `.env` and `.env.local` files
- Node.js 18+ required for JS/TS projects
- Python 3.8+ required for Python projects

## Debugging

```bash
export AIOS_DEBUG=true              # Enable debug mode
tail -f .aios/logs/agent.log       # View agent logs
npm run trace -- workflow-name     # Trace workflow execution
```

## Model Routing (ALWAYS ACTIVE)

When spawning subagents via the Task tool, **always** select the model based on these rules. This saves tokens and wait time by using lighter models for simple tasks.

### Quick Reference — Agent → Model

| Model | Agents |
|-------|--------|
| **opus** | @architect, @qa, @analyst |
| **sonnet** | @dev, @pm, @sm, @po, @ux-design-expert, @data-engineer, @devops, @expansion-creator, @aios-master |
| **haiku** | @data-collector, validation tasks, checklists, indexing |

### Task Overrides (regex — checked BEFORE agent default)

| Pattern | Model |
|---------|-------|
| `^validate-.*` | haiku |
| `^execute-checklist.*` | haiku |
| `^index-docs.*` | haiku |
| `^update-source-tree.*` | haiku |
| `^update-manifest.*` | haiku |
| `^create-doc.*` | sonnet |
| `^architect-review.*` | opus |
| `^create-agent.*` | opus |
| `^analyze-framework.*` | opus |
| `^propose-modification.*` | opus |

### Priority Cascade (highest wins)

1. **Manual override** — user says "use opus/sonnet/haiku"
2. **Task override** — regex match from table above
3. **Agent default** — from agent table above
4. **Global default** — sonnet

### How to Apply

When calling the Task tool, include `model: "haiku"`, `model: "sonnet"`, or `model: "opus"` based on the rules above. Example:

```
Task tool call:
  description: "Validate agents"
  subagent_type: "general-purpose"
  model: "haiku"              ← from task override (validate-*)
  prompt: ...
```

### Full Config

- Rules: `.aios-core/config/model-routing-rules.yaml`
- Engine: `.aios-core/core/routing/model-router.js`
- Log: `.aios/routing-log.jsonl`
- Commands: `*model-routing show/test/enable/disable`, `*cost-report`

## Squad Routing (ALWAYS ACTIVE)

When a task involves a specific domain, the corresponding **squad MUST be used** instead of generic AIOS agents. Squads contain MMOS mind clones with 88-98% fidelity — always superior to generic agents for their domain.

### Quick Reference — Domain → Squad

| Domain | Squad | Lead | Replaces |
|--------|-------|------|----------|
| Design (tokens, components, branding, WCAG) | `design-system` | @design-chief | @ux-design-expert |
| Marketing (Facebook/Google Ads, traffic, funnels) | `media-buy-squad` | @ad-midas | — |
| Security (audits, OWASP, threats) | `security-squad` | @security-chief | — |
| Cognitive Cloning (minds, DNA Mental) | `mmos-squad` | @mind-mapper | — |
| Data Collection (scraping, ETL) | `etl-squad` | @data-collector | — |
| Expansion Creation (new squads/packs) | `creator-squad` | @expansion-creator | — |

### How to Apply

1. **Scan** PRD/story/task description for domain keywords
2. **Match** → activate squad lead agent with `target_context: "hybrid"`
3. **Squad lead delegates** to specialist agents within the squad
4. **Management stays on core** — @pm, @po, @sm remain core AIOS agents

### Priority Cascade

1. **Manual override** — user says "use squad X"
2. **Domain match** — keywords in task/story/PRD (see patterns in rules file)
3. **Agent affinity** — squad agent referenced directly (e.g. @brad-frost → design-system)
4. **Workflow hint** — workflow step references squad context
5. **None** — use core AIOS agents

### Parallel Execution

Independent domains CAN run in parallel (max 3):
- Design + Security (parallel OK)
- Design + Marketing (parallel OK)
- Security + Marketing (parallel OK)
- Same domain = always sequential

### Full Config

- Rules: `.aios-core/config/squad-routing-rules.yaml`
- Squads: `squads/` (symlink → `aios-squads/packages/`)

---
*Synkra AIOS Claude Code Configuration v3.4 — Updated 2026-02-22 (Added: Squad Routing, enhanced squads registry)*
