#!/bin/bash
# guardrail-bash.sh — PreToolUse hook for Bash commands
# Blocks dangerous operations, warns on risky ones
# Exit codes: 0 = allow, 2 = block

# Input comes from stdin as JSON: { "tool_name": "Bash", "tool_input": { "command": "..." } }
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# BLOCK: git push --force (any variant)
if echo "$COMMAND" | grep -qE 'git\s+push\s+.*(-f|--force|--force-with-lease)'; then
  echo "BLOCKED: git push --force detected. This can destroy remote history." >&2
  echo "If you really need this, ask the user for explicit confirmation first." >&2
  exit 2
fi

# BLOCK: git reset --hard without user intent
if echo "$COMMAND" | grep -qE 'git\s+reset\s+--hard'; then
  echo "BLOCKED: git reset --hard discards all uncommitted changes." >&2
  echo "Ask the user for explicit confirmation before running this." >&2
  exit 2
fi

# BLOCK: rm -rf on project root directories
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+.*(grupo-lawteck|climatronico-blog|relatorios_lawteck|RepairHub|Criador de PDFs|Landing page|Scripts Live|aios-squads|\.aios-core)\b'; then
  echo "BLOCKED: Attempting to rm -rf a project directory." >&2
  exit 2
fi

# BLOCK: dropping all tables or database
if echo "$COMMAND" | grep -qiE '(DROP\s+DATABASE|DROP\s+SCHEMA.*CASCADE)'; then
  echo "BLOCKED: DROP DATABASE/SCHEMA CASCADE detected." >&2
  exit 2
fi

# All checks passed
exit 0
