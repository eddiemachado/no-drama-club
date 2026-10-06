#!/usr/bin/env bash
# PostToolUse hook for ExitPlanMode: on plan approval, saves it to .agents/.plans/<slug>.md
# with `status: approved` and tells Claude to start the orchestrator and reviewer.
set -euo pipefail

PAYLOAD="$(cat)" python3 - <<'PYEOF'
import glob
import json
import os
import re
import sys

START = ("Start two named subagents in the background, both with plan_doc={path}: "
         "`orchestrator` (name: orchestrator) to implement the plan, and `reviewer` "
         "(name: reviewer) to read the plan and wait for review requests from orchestrator. "
         "Do not implement the plan yourself. When orchestrator's final report arrives, "
         "relay it to the user.")

def respond(context):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }))
    sys.exit(0)

try:
    payload = json.loads(os.environ.get("PAYLOAD", ""))
except Exception:
    sys.exit(0)

tool_input = payload.get("tool_input", {}) or {}
plan = tool_input.get("plan") or ""

# Fall back to the newest file in Claude's plans folder.
if not plan:
    path = tool_input.get("planFilePath") or ""
    if not path:
        files = glob.glob(os.path.expanduser("~/.claude/plans/*.md"))
        path = max(files, key=os.path.getmtime) if files else ""
    if path and os.path.isfile(path):
        with open(path) as f:
            plan = f.read()

if not plan:
    respond("plan-approved hook: could not read the approved plan. Save it to "
            ".agents/.plans/<slug>.md with `status: approved` yourself. Then: " + START.format(path=".agents/.plans/<slug>.md"))

slug = re.search(r"^slug:\s*([a-z0-9-]+)\s*$", plan, re.MULTILINE)
if not slug:
    respond("plan-approved hook: the plan has no `slug:` in its frontmatter, so it "
            "wasn't saved. Follow the plan skill: save it to .agents/.plans/<slug>.md in the "
            "schema with `status: approved`. Then: " + START.format(path=".agents/.plans/<slug>.md"))
slug = slug.group(1)

if re.search(r"^status:", plan, re.MULTILINE):
    plan = re.sub(r"^status:.*$", "status: approved", plan, count=1, flags=re.MULTILINE)
else:
    respond("plan-approved hook: the plan has no `status:` frontmatter, so it wasn't "
            "saved. Follow the plan skill's schema, save it to .agents/.plans/" + slug +
            ".md with `status: approved`. Then: " + START.format(path=".agents/.plans/" + slug + ".md"))

root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
os.makedirs(os.path.join(root, ".agents", ".plans"), exist_ok=True)
rel = os.path.join(".agents", ".plans", slug + ".md")
with open(os.path.join(root, rel), "w") as f:
    f.write(plan)

respond("The user approved the plan. It is saved to " + rel + " with `status: approved`. "
        + START.format(path=rel))
PYEOF
