#!/bin/bash
# pre-compact.sh — Salva estado critico ANTES da compactacao
# O SessionStart(compact) depois re-injeta esse snapshot
# v2.1 — Dynamic project discovery (no hardcoded project names)

DIR="${CLAUDE_PROJECT_DIR:-.}"
SNAPSHOT_DIR="$DIR/.claude/snapshots"
mkdir -p "$SNAPSHOT_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SNAPSHOT="$SNAPSHOT_DIR/pre-compact-latest.md"

{
  echo "# Pre-Compaction Snapshot v2"
  echo "Saved at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""

  # 1. Active projects (auto-discover all git repos in workspace)
  echo "## Active Projects"
  for proj_dir in "$DIR"/*/; do
    proj=$(basename "$proj_dir")
    if [ -d "$proj_dir/.git" ]; then
      LAST_COMMIT_AGE=$(cd "$proj_dir" && git log -1 --format="%cr" 2>/dev/null)
      BRANCH=$(cd "$proj_dir" && git branch --show-current 2>/dev/null)
      CHANGES=$(cd "$proj_dir" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      if [ "$CHANGES" -gt 0 ]; then
        echo "- **$proj** (branch: $BRANCH): $CHANGES uncommitted files | last commit: $LAST_COMMIT_AGE"
      fi
    fi
  done
  echo ""

  # 2. Active workflow state (from .aios/)
  echo "## Active Workflows"
  if ls "$DIR/.aios/"*-state.yaml 1>/dev/null 2>&1; then
    for state_file in "$DIR/.aios/"*-state.yaml; do
      WF_NAME=$(grep -m1 'workflow_name:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      WF_STATUS=$(grep -m1 'status:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      WF_PHASE=$(grep -m1 'current_phase:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      WF_STEP=$(grep -m1 'last_completed_step:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      WF_CONTEXT=$(grep -m1 'target_context:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      WF_SQUAD=$(grep -m1 'squad_name:' "$state_file" 2>/dev/null | sed 's/.*: *//')
      echo "- **$WF_NAME** | status: $WF_STATUS | phase: $WF_PHASE | last step: $WF_STEP"
      [ -n "$WF_SQUAD" ] && [ "$WF_SQUAD" != "null" ] && echo "  squad: $WF_SQUAD (context: $WF_CONTEXT)"
    done
  else
    echo "No active workflows"
  fi
  echo ""

  # 3. Active PRD (auto-discover from any project with docs/prd/)
  echo "## Active PRD (summary)"
  FOUND_PRD=false
  # Find most recently modified PRD across all projects
  LATEST_PRD=$(find "$DIR" -maxdepth 4 -path "*/docs/prd*.md" -o -path "*/docs/prd/*.md" 2>/dev/null | \
    xargs ls -t 2>/dev/null | head -1)
  if [ -n "$LATEST_PRD" ]; then
    # Extract project name from path
    PRD_PROJECT=$(echo "$LATEST_PRD" | sed "s|$DIR/||" | cut -d'/' -f1)
    echo "**Project:** $PRD_PROJECT"
    echo "**File:** $(basename "$LATEST_PRD")"
    head -30 "$LATEST_PRD" 2>/dev/null
    FOUND_PRD=true
  fi
  if [ "$FOUND_PRD" = false ]; then
    echo "No active PRD found"
  fi
  echo ""

  # 4. Squads in use (from agent log + workflow state)
  echo "## Squads Used (recent)"
  if [ -f "$DIR/ralph/agent-log.jsonl" ]; then
    tail -20 "$DIR/ralph/agent-log.jsonl" 2>/dev/null | \
      jq -r 'select(.desc != null) | .desc' 2>/dev/null | \
      grep -iE "design|media|security|mmos|etl|creator" | \
      sort -u | head -5 | while read -r line; do
        echo "- $line"
      done
  fi
  if ls "$DIR/.aios/"*-state.yaml 1>/dev/null 2>&1; then
    grep -h 'squad_name:' "$DIR/.aios/"*-state.yaml 2>/dev/null | \
      sed 's/.*: *//' | sort -u | while read -r sq; do
        [ -n "$sq" ] && [ "$sq" != "null" ] && echo "- Active squad: $sq"
      done
  fi
  echo "(If empty, no squad-specific work detected)"
  echo ""

  # 5. Ralph Loop status
  echo "## Ralph Loop"
  if [ -f "$DIR/ralph/loop-status.json" ]; then
    jq -r '"Status: " + .status + " | Story: " + (.currentStoryId // "none") + " | Done: " + ((.stories // [] | map(select(.status=="done")) | length) | tostring) + "/" + ((.totalStories // 0) | tostring)' "$DIR/ralph/loop-status.json" 2>/dev/null
  else
    echo "No active loop"
  fi
  echo ""

  # 6. Recent progress
  echo "## Recent Progress"
  if [ -f "$DIR/ralph/progress.md" ]; then
    tail -10 "$DIR/ralph/progress.md"
  else
    echo "No progress file"
  fi
  echo ""

  # 7. Last 5 subagents
  echo "## Last 5 Subagents"
  if [ -f "$DIR/ralph/agent-log.jsonl" ]; then
    tail -5 "$DIR/ralph/agent-log.jsonl" | \
      jq -r '"- " + (.ts // "?") + " | " + (.type // "?") + " | " + (.desc // "?") + " (" + ((.turns // 0) | tostring) + " turns, " + (((.duration_ms // 0) / 1000) | tostring) + "s)"' 2>/dev/null
  else
    echo "No agent log"
  fi
  echo ""

  # 8. Active stories (auto-discover from any project)
  echo "## Active Stories"
  # Search root docs/stories and all project docs/stories
  find "$DIR" -maxdepth 4 -path "*/docs/stories/*.md" 2>/dev/null | while read -r f; do
    if grep -q "Status:.*In Progress\|Status:.*Review\|Status:.*Draft" "$f" 2>/dev/null; then
      PROJ=$(echo "$f" | sed "s|$DIR/||" | cut -d'/' -f1)
      TITLE=$(head -1 "$f" | sed 's/^#* *//')
      echo "- [$PROJ] $(basename "$f"): $TITLE"
      grep -m3 "^\- \[" "$f" 2>/dev/null | sed 's/^/  /'
    fi
  done
  echo ""

  # 9. Architecture decisions (auto-discover from any project)
  echo "## Recent Architecture Decisions"
  find "$DIR" -maxdepth 3 -path "*/.ai/*.md" 2>/dev/null | \
    xargs ls -t 2>/dev/null | head -5 | while read -r f; do
      PROJ=$(echo "$f" | sed "s|$DIR/||" | cut -d'/' -f1)
      TITLE=$(head -1 "$f" | sed 's/^#* *//')
      echo "- [$PROJ] $(basename "$f"): $TITLE"
    done
  echo ""

} > "$SNAPSHOT"

# Tambem salva copia timestamped (manter ultimos 5)
cp "$SNAPSHOT" "$SNAPSHOT_DIR/pre-compact-$TIMESTAMP.md"
ls -t "$SNAPSHOT_DIR"/pre-compact-2*.md 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null

echo "Snapshot saved to $SNAPSHOT"
