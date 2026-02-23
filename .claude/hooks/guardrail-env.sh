#!/bin/bash
# guardrail-env.sh — PreToolUse hook for Edit/Write on sensitive files
# Warns when touching .env files or credentials
# Exit codes: 0 = allow, 2 = block

# Input comes from stdin as JSON
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=""

if [ "$TOOL_NAME" = "Edit" ]; then
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
elif [ "$TOOL_NAME" = "Write" ]; then
  FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

BASENAME=$(basename "$FILE_PATH")

# BLOCK: Direct modification of .env files (secrets)
if echo "$BASENAME" | grep -qE '^\.env(\.local|\.production|\.staging)?$'; then
  echo "BLOCKED: Modifying $BASENAME which may contain secrets." >&2
  echo "Use .env.example for documentation. Ask user before touching real .env files." >&2
  exit 2
fi

# BLOCK: Credential files
if echo "$BASENAME" | grep -qiE '(credentials|secrets|tokens)\.(json|yaml|yml|toml)$'; then
  echo "BLOCKED: Modifying credential file $BASENAME." >&2
  exit 2
fi

# All checks passed
exit 0
