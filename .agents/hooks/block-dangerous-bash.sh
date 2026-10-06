#!/usr/bin/env bash
# PreToolUse hook for Bash: blocks `rm -rf` and force-pushes to main/master.
# Exits 2 (block) with a reason on stderr, 0 (allow) otherwise.
set -euo pipefail

PAYLOAD="$(cat)" python3 - <<'PYEOF'
import json
import os
import re
import sys

try:
    payload = json.loads(os.environ.get("PAYLOAD", ""))
except Exception:
    sys.exit(0)

command = payload.get("tool_input", {}).get("command", "") or ""
if not command:
    sys.exit(0)

RM_RF = re.compile(
    r"""
    (^|[;&|]\s*)rm\s+          # start of an rm invocation
    (?:-\S+\s+)*               # any number of flag tokens
    (?:                        # a flag token combining recursive + force
        -[A-Za-z]*r[A-Za-z]*f[A-Za-z]* |
        -[A-Za-z]*f[A-Za-z]*r[A-Za-z]* |
        --recursive |
        --force
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

def has_rm_rf(cmd: str) -> bool:
    has_recursive = bool(re.search(r"(^|[;&|]\s*)rm\s+.*(-[A-Za-z]*r|--recursive)", cmd, re.IGNORECASE))
    has_force = bool(re.search(r"(^|[;&|]\s*)rm\s+.*(-[A-Za-z]*f|--force)", cmd, re.IGNORECASE))
    is_rm = bool(re.search(r"(^|[;&|]\s*)rm(\s|$)", cmd))
    return is_rm and has_recursive and has_force

FORCE_PUSH_MAIN = re.compile(
    r"git\s+push\b.*(--force(-with-lease)?|(?<!\S)-f(?!\S))",
    re.IGNORECASE,
)

def is_force_push_to_main(cmd: str) -> bool:
    if not re.search(r"git\s+push", cmd, re.IGNORECASE):
        return False
    if not FORCE_PUSH_MAIN.search(cmd):
        return False
    return bool(re.search(r"\b(main|master)\b", cmd, re.IGNORECASE)) or not re.search(
        r"git\s+push\s+\S+\s+\S+", cmd
    )

if has_rm_rf(command):
    print("Blocked by block-dangerous-bash.sh: refusing to run an rm -rf style command", file=sys.stderr)
    sys.exit(2)

if is_force_push_to_main(command):
    print("Blocked by block-dangerous-bash.sh: refusing to force-push to main/master", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
PYEOF
