---
name: retro
description: >
  On-demand review of recent agent sessions in this repo. Summarizes Claude
  Code transcripts (errors, denials, wasted tokens, review outcomes) and agent
  memory, then files improvement tickets to Linear. Never edits rules or agents.
disable-model-invocation: true
---

# Retro

Find what went wrong or cost too much in recent agent runs, and file Linear tickets so a human can fix the rules.

## 1. Rules

- Never edit files. Only run `scripts/digest.py` and delete finished plans (§4).
- Never quote raw transcript text in tickets; summarize.
- Every ticket needs concrete evidence (session/agent, step, error, token numbers, or file path).
- Max 5 new tickets per run. Skip one-off noise.
- Follow `.agents/rules/linear.md` (project, label, format, dedupe).

## 2. Gather

1. Run `scripts/digest.py` (this skill's folder). Pass the user's arg: a number → `--since-days N`; a session id → `--session ID`; none → since last retro.
2. Read `.agents/.plans/*.review.md` changed in the same window (checklist, cycles, `PLAN_ISSUE`, `## Result`).
3. Read `.agents/agent-memory/*/MEMORY.md` and each note file they link.

Don't open raw transcripts; the digest is enough.

## 3. Analyze

- **Memory promotion:** memory notes that should be a rule in an agent/skill/rule file, recur across agents, or contradict an existing rule.
- **Token waste:** most expensive agents/steps, large tool outputs, re-read files, repeated identical calls, low cache-read %, delegation that cost more than it saved.
- **Failures:** causes of STAGNANT/REGRESSING/BLOCKED, tool errors, permission denials, hook blocks.
- **Review quality:** reviewer false positives, vague or untestable criteria.
- **Instruction gaps:** conflicts or missing guidance between agent, skill, and rule files.

Ignore user rejections of tool calls unless they show a repeated agent mistake.

## 4. File

For each finding, dedupe per `.agents/rules/linear.md`, then create a ticket or comment on the existing one. Don't ask for confirmation.

Memory-promotion tickets end with:
`Cleanup: delete <memory note path> and its MEMORY.md line after this rule is fixed.`

Then run `scripts/digest.py --mark`.

Then clean up finished plans: for each `.agents/.plans/<slug>.review.md` containing `## Result: DONE`, delete it and `.agents/.plans/<slug>.md` (`rm`, never `rm -r`). Leave every other plan.

If Linear tools are unavailable: skip filing, don't mark, don't clean up, and list the findings (title, problem, evidence, affected file, suggested change) in the reply.

## 5. Reply

List ticket URLs (created or commented), or "No issues", and the plans deleted. Add one line with the run's total tokens from the digest.
