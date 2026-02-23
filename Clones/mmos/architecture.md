# MMOS — Mind OS Architecture

> **Version:** 0.1.0 (Skeleton)
> **Status:** Scaffolding

## Overview

MMOS (Mind OS) is a multi-agent cognitive operating system that orchestrates **clone minds** — AI replicas of domain specialists — across functional squads. Each clone carries a full cognitive DNA (mental models, linguistic patterns, decision matrices) and operates within a squad-level chain of command.

## Core Principles

1. **Clone Fidelity** — Each mind replicates the specialist's actual reasoning, not a generic persona
2. **Squad Autonomy** — Squads are self-contained units with their own agents, tasks, workflows, and quality gates
3. **Quality Gates** — Mandatory audits before any deliverable exits the system. No output is final until it passes its squad's checklist pipeline
4. **Composability** — Agents from different squads can be composed into cross-functional workflows
5. **Traceability** — Every decision, output, and audit is logged for full operational transparency

## System Architecture

```
mmos/
├── squads/                          # Functional teams
│   ├── {squad}/
│   │   ├── agents/                  # Agent identity & commands (.md)
│   │   ├── tasks/                   # Task definitions (.md)
│   │   ├── workflows/               # Execution sequences (.yaml)
│   │   ├── templates/               # Output models & algorithms (.yaml)
│   │   ├── checklists/              # Quality Gate audits (.md)
│   │   └── data/                    # Knowledge bases & extracted frameworks
│   └── ...
├── outputs/
│   └── minds/                       # Clone cognitive profiles
│       ├── _template/               # DNA template for new minds
│       │   └── analysis/            # Cognitive spec files (.yaml)
│       └── {mind-name}/             # Individual clone instances
│           └── analysis/
├── infrastructure/                  # System-level prompts, logs, configs
├── docs/                            # Architecture & operational docs
├── architecture.md                  # This file
└── mmos-state.json                  # System state control
```

## Quality Gates

Quality Gates are **mandatory audit checkpoints** that every deliverable must pass before being considered final. They operate at the squad level:

| Gate | Description | Enforcement |
|------|-------------|-------------|
| **Pre-Flight** | Input validation — does the task have all required context? | Before task execution |
| **In-Process** | Mid-execution checks — is the agent following the correct workflow? | During execution |
| **Pre-Delivery** | Output audit — does the deliverable meet the squad's quality standards? | Before output is released |
| **Post-Mortem** | Retrospective — what can be improved for next iteration? | After delivery |

Each squad defines its own checklists in `squads/{squad}/checklists/`. A deliverable that fails a Quality Gate is **returned to the originating agent** with audit notes.

## Agent Command System

Agents respond to two types of custom commands:

| Prefix | Type | Example | Purpose |
|--------|------|---------|---------|
| `*` | **Action commands** | `*write-headline` | Execute a specific task |
| `+` | **Modifier commands** | `+tone-aggressive` | Modify agent behavior/parameters |

Commands are defined per-agent in their identity files (`squads/{squad}/agents/{agent}.md`).

## Cross-Squad Communication

Squads communicate through a **shared protocol**:

1. **Output Handoff** — Squad A produces an output artifact that Squad B consumes as input
2. **Workflow Composition** — A master workflow chains steps across multiple squads
3. **State Bus** — `mmos-state.json` tracks active agents, running workflows, and pending handoffs
4. **Mind Reference** — Any squad can read from `outputs/minds/` to adopt a clone's cognitive profile

### Communication Flow Example

```
[storytelling/agents/narrator] → *write-hook
    ↓ (output: hook-draft.md)
[copy/agents/copywriter] → *refine-copy +tone-direct
    ↓ (output: refined-hook.md)
[copy/checklists/plf/launch-checklist.md] → Quality Gate
    ↓ (pass/fail)
[media-buy/agents/media-planner] → *create-ad-set
```

## Mind DNA Specification

Each clone mind contains two layers:

### Layer 1 — Analysis (`outputs/minds/{name}/analysis/`)

The cognitive blueprint — **how the specialist thinks**.

| File | Purpose |
|------|---------|
| `cognitive-spec.yaml` | How the specialist thinks — reasoning chains, problem-solving patterns |
| `mental-models.yaml` | Frameworks and models the specialist relies on |
| `linguistic-patterns.yaml` | Voice, tone, vocabulary, rhetorical devices |
| `psychometric-profile.yaml` | Behavioral traits, risk tolerance, communication style |
| `decision-matrix.yaml` | How decisions are weighted — criteria, priorities, trade-offs |

### Layer 2 — Artifacts (`outputs/minds/{name}/artifacts/`)

The expression layer — **how the specialist communicates in practice**.

| File | Purpose |
|------|---------|
| `anecdotes.yaml` | Bank of real stories, metaphors, case studies, catchphrases, and cautionary tales |
| `voice_guide.md` | Actionable writing rules, verbal tics, sentence architecture, DO/DON'T calibration |

The **analysis** layer feeds the agent's reasoning; the **artifacts** layer feeds its output generation. Together they form the complete cognitive DNA of a clone.

## Squads

| Squad | Domain | Primary Output |
|-------|--------|----------------|
| **copy** | Copywriting & persuasion | Sales pages, emails, headlines, hooks |
| **design** | Visual & UX design | Layouts, wireframes, brand systems |
| **media-buy** | Paid traffic & media planning | Ad sets, audiences, budgets, campaigns |
| **storytelling** | Narrative & content | Stories, scripts, content strategies |
| **hr** | Talent & team operations | Assessments, culture docs, processes |
| **data** | Analytics & intelligence | Reports, dashboards, insights |
