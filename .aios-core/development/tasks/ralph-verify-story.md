---
tools:
  - bash
  - read
  - glob
  - grep
---

# ralph-verify-story

Verify a story implementation with fresh context. This task is spawned by the Ralph Loop workflow as an isolated QA subagent after a story has been implemented. The verifier has no knowledge of implementation decisions — it judges purely on acceptance criteria, code quality, and test coverage.

## Execution Modes

### 1. YOLO Mode - Autonomous (0 prompts)
- Full autonomous verification
- **Best for:** Ralph Loop automated execution

### 2. Interactive Mode - Balanced (2-3 prompts) **[DEFAULT]**
- Report findings before verdict
- **Best for:** Manual execution

**Parameter:** `mode` (optional, default: `yolo` when called from ralph-loop)

---

## Task Definition

```yaml
task: ralphVerifyStory()
responsible: QA Agent
responsible_type: Agent
atomic_layer: Verification
model_routing: opus

inputs:
  - campo: storyId
    tipo: string
    obrigatorio: true
  - campo: storyPath
    tipo: string
    obrigatorio: true
  - campo: commitHash
    tipo: string
    obrigatorio: true
  - campo: projectPath
    tipo: string
    obrigatorio: true

outputs:
  - campo: verdict
    tipo: string
    enum: [APPROVE, REJECT]
    destino: Return value
  - campo: issuesFound
    tipo: number
    destino: Return value
  - campo: qualityScore
    tipo: number
    destino: Return value
```

---

## Pre-Conditions

```yaml
pre-conditions:
  - [ ] Story file exists and has been updated by implementor
    blocker: true
  - [ ] Commit hash is valid and exists in git log
    blocker: true
  - [ ] Project builds successfully
    blocker: true
```

---

## Verification Steps

### Step 1: Read Story and Understand Requirements

1. Read the story file completely
2. Extract all acceptance criteria (ACs)
3. Note any special requirements or constraints
4. Read project's `.claude/CLAUDE.md` for standards

### Step 2: Review the Diff

1. Run `git diff {commitHash}~1..{commitHash}` to see all changes
2. Verify changes are scoped to this story (no unrelated changes)
3. Check for accidental inclusions (env files, logs, etc.)

### Step 3: Acceptance Criteria Validation

For each AC:
1. Verify it's implemented (not just checked off)
2. Trace from AC to the code that implements it
3. Verify edge cases are handled
4. Mark as PASS or FAIL with reason

### Step 4: Code Quality Review

1. **Architecture:** Does the code follow existing patterns?
2. **Security:** Any OWASP vulnerabilities introduced?
3. **Performance:** Any obvious performance issues?
4. **Maintainability:** Is the code readable and maintainable?
5. **No over-engineering:** Are changes minimal and focused?

### Step 5: Test Verification

1. Run the project's test suite
2. Verify new tests exist for new functionality
3. Check test quality (not just existence)
4. Ensure no tests were broken

### Step 6: Build Verification

1. Run `npm run build` (or equivalent)
2. Run `npm run lint`
3. Run `npm run typecheck` (if available)
4. All must pass with 0 new errors

### Step 7: Produce Verdict

**Deterministic rules (apply in order):**

1. If any AC is not implemented → REJECT
2. If tests fail → REJECT
3. If build/lint fails → REJECT
4. If security vulnerability found → REJECT
5. If all above pass → APPROVE

**Quality Score:**
```
score = 100
  - 20 per failed AC
  - 15 per security issue
  - 10 per missing test
  - 5 per code quality issue
  - 5 per style violation
Bounded between 0 and 100
```

---

## Output Format

```yaml
verdict: APPROVE | REJECT
storyId: "{storyId}"
commitHash: "{commitHash}"
qualityScore: 0-100
issuesFound: number
reviewedAt: ISO-8601

acceptance_criteria:
  - ac: "AC description"
    status: PASS | FAIL
    evidence: "How it was verified"

issues:
  - severity: critical | high | medium | low
    description: "Issue description"
    file: "path/to/file"
    line: number
    suggestion: "How to fix"

checks:
  tests: PASS | FAIL
  lint: PASS | FAIL
  build: PASS | FAIL
  typecheck: PASS | FAIL | N/A
```

---

## Post-Conditions

```yaml
post-conditions:
  - [ ] All ACs evaluated with PASS/FAIL
    blocker: true
  - [ ] Verdict produced (APPROVE or REJECT)
    blocker: true
  - [ ] Quality score calculated
    blocker: true
  - [ ] Issues documented with actionable suggestions
    blocker: false
```

---

## Error Handling

**Strategy:** conservative (when in doubt, REJECT)

1. **Cannot read story:** REJECT with reason
2. **Cannot run tests:** REJECT with reason
3. **Ambiguous AC:** REJECT and flag for human clarification
4. **Build timeout:** REJECT with suggestion to investigate

---

## Performance

```yaml
duration_expected: 5-15 min
cost_estimated: $0.05-0.25
token_usage: ~8,000-30,000 tokens
model: opus
```

---

## Metadata

```yaml
version: 1.0.0
created: "2026-02-22"
author: "AIOS Optimization"
tags:
  - ralph-loop
  - verification
  - fresh-context
  - qa
```
