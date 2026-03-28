#!/usr/bin/env bash
set -euo pipefail

payload="$(cat)"
command_text="$(
  printf '%s' "$payload" | python3 -c '
import json
import sys

data = json.load(sys.stdin)
print(data.get("tool_input", {}).get("command", ""))
'
)"

if printf '%s' "$command_text" | grep -Eiq '(^|[[:space:]])(rm[[:space:]]+-rf|git[[:space:]]+reset[[:space:]]+--hard|mkfs|dd[[:space:]]+if=|shutdown|reboot|halt)([[:space:]]|$)'; then
  cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked by project baseline hook: destructive shell pattern."}}
EOF
  exit 0
fi
