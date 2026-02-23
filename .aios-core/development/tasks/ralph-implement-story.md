---
tools:
  - bash
  - read
  - write
  - edit
  - glob
  - grep
---

# ralph-implement-story

Implement a single story with fresh context. This task is spawned by the Ralph Loop workflow as an isolated subagent — it receives only the story file, progress context, and project CLAUDE.md. No accumulated context from previous stories.

## Execution Modes

### 1. YOLO Mode - Autonomous (0 prompts)
- Full autonomous implementation
- **Best for:** Ralph Loop automated execution

### 2. Interactive Mode - Balanced (3-5 prompts) **[DEFAULT]**
- Checkpoints for key decisions
- **Best for:** Manual execution

**Parameter:** `mode` (optional, default: `yolo` when called from ralph-loop)

---

## Task Definition

```yaml
task: ralphImplementStory()
responsible: Dev Agent
responsible_type: Agent
atomic_layer: Execution
model_routing: sonnet

inputs:
  - campo: storyId
    tipo: string
    obrigatorio: true
  - campo: storyPath
    tipo: string
    obrigatorio: true
  - campo: progressFile
    tipo: string
    obrigatorio: false
    default: "ralph/progress.md"
  - campo: projectPath
    tipo: string
    obrigatorio: true

outputs:
  - campo: commitHash
    tipo: string
    destino: Return value
  - campo: filesChanged
    tipo: array
    destino: Return value
  - campo: testsStatus
    tipo: string
    destino: Return value
```

---

## Pre-Conditions

```yaml
pre-conditions:
  - [ ] Story file exists and is readable
    blocker: true
  - [ ] Story status is not "Done"
    blocker: true
  - [ ] Project has a valid package.json or equivalent
    blocker: true
  - [ ] Git working tree is clean (no uncommitted changes)
    blocker: true
```

---

## Execution Steps

### Step 1: Read Story and Context

1. Read the story file completely
2. Read `ralph/progress.md` if it exists (to understand what was already done)
3. Read project's `.claude/CLAUDE.md` for tech stack and conventions
4. Identify all acceptance criteria (ACs)
5. Identify the File List section (files already touched)

### Step 2: Plan Implementation

1. Map each AC to concrete implementation tasks
2. Identify files that need to be created or modified
3. Determine test strategy (unit, integration, e2e)
4. Estimate complexity — if story seems too large, log warning

### Step 3: Implement

1. For each AC, implement the required changes
2. Follow project coding standards
3. Use existing patterns and components (check squads/ first)
4. Write clean, focused code — no over-engineering
5. Run linter incrementally to catch issues early

### Step 4: Write Tests

1. Write tests covering each AC
2. Run tests and ensure they pass
3. Fix any failures before proceeding

### Step 5: Self-Critique (Step 5.5 from Constitution)

Before finishing, evaluate:
- 3+ predicted bugs
- 3+ edge cases
- Error handling coverage
- Security implications
- No hardcoded values
- No console.log left
- No mock data when real data available

### Step 6: Commit

1. Stage only the files related to this story
2. Create atomic commit with conventional format: `feat: {story title} [Story {storyId}]`
3. Capture the commit hash

### Step 7: Update Story File

1. Mark completed ACs with `[x]`
2. Update the File List section with new/modified files
3. Add dev notes if relevant

---

## Post-Conditions

```yaml
post-conditions:
  - [ ] All acceptance criteria implemented
    blocker: true
  - [ ] Tests pass
    blocker: true
  - [ ] Linter passes (0 new errors)
    blocker: true
  - [ ] Commit created with proper message
    blocker: true
  - [ ] Story file updated with progress
    blocker: false
```

---

## Error Handling

**Strategy:** retry with investigation

1. **Lint failure:** Fix issues, re-run
2. **Test failure:** Investigate root cause, fix, re-run
3. **Build failure:** Check for missing dependencies, fix
4. **Large story:** Log warning, implement what's feasible, flag remainder

---

## Performance

```yaml
duration_expected: 10-30 min
cost_estimated: $0.05-0.20
token_usage: ~10,000-40,000 tokens
model: sonnet
```

---

## Metadata

```yaml
version: 1.0.0
created: "2026-02-22"
author: "AIOS Optimization"
tags:
  - ralph-loop
  - implementation
  - fresh-context
  - dev
```
