#!/usr/bin/env bash
# SessionStart hook: if /retro hasn't run here in 7+ days and sessions are pending,
# tells Claude to suggest it once. Silent otherwise.
set -euo pipefail

PAYLOAD="$(cat)" python3 - <<'PYEOF'
import glob
import json
import os
import time

DAYS = 7

try:
    payload = json.loads(os.environ.get("PAYLOAD", ""))
except Exception:
    payload = {}

root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
pdir = os.path.expanduser("~/.claude/projects/" + root.replace("/", "-"))
marker = os.path.join(pdir, ".retro-last")
last = os.path.getmtime(marker) if os.path.exists(marker) else 0
if time.time() - last < DAYS * 86400:
    raise SystemExit(0)

current = payload.get("session_id", "")
pending = [f for f in glob.glob(os.path.join(pdir, "*.jsonl"))
           if os.path.getmtime(f) > last and not os.path.basename(f).startswith(current or "\0")]
if not pending:
    raise SystemExit(0)

age = "has never run on this machine" if not last else "last ran %d days ago" % ((time.time() - last) // 86400)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "/retro %s (%d session(s) to review; transcripts expire after 30 days). "
                             "Suggest running /retro to the user once, briefly. Don't run it unless they agree."
                             % (age, len(pending)),
    }
}))
PYEOF
