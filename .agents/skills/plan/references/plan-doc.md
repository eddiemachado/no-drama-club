# Plan doc schema

This file is the contract. Orchestrator and reviewer consume the file, not the host's Plan Mode UI. Cursor, Claude, and Codex may each produce their own draft; normalize it into this shape before anyone implements.

## Location

Write to `<repo>/.agents/.plans/<slug>.md`.

- `<slug>` is kebab-case from the title (`oauth-refresh-tokens`).
- The sibling review log is `<repo>/.agents/.plans/<slug>.review.md` (orchestrator/reviewer create this, not planner).
- `.agents/.plans/` is scratch for the loop and is gitignored. `/retro` deletes plans whose review has `## Result: DONE`.

If the host already wrote a plan somewhere else (Claude `~/.claude/plans/`, Cursor plan UI, Codex), copy or rewrite it into `.agents/.plans/<slug>.md` so every host hands orchestrator the same path convention.

## Required sections

Use these headings, exactly:

```markdown
---
status: draft
slug: example-slug
---

# Title

## Context

What is true in the repo now, and why this work exists. Short.

## Approach

The strategy, not the task list. Tradeoffs that were already decided.

## Steps

### S1 — Short step title

What changes, in which area, and what "done" means for this step.

### S2 — …

## Acceptance Criteria

- [ ] Observable, testable outcome (not "implement X")
- [ ] …
- [ ] Out of scope is honored: …

## Open Questions

- None. | or unresolved items that would change the rubric

## Amendment Log

_Empty until a later amendment._
```

### Rules for the rubric

`## Acceptance Criteria` is load-bearing. Every item must be something a reviewer can PASS/FAIL against a diff without re-interpreting intent.

- Use checkboxes (`- [ ]`).
- Prefer outcomes and constraints over implementation chores.
- Include explicit out-of-scope if the user narrowed the work.
- One item per criterion. Do not bury multiple bars in one line.

### Rules for steps

- Stable ids (`S1`, `S2`, …) so orchestrator can name `step:` in handoffs.
- Each step should be independently reviewable.
- Do not put secret values in the plan.

### `status`

- `draft` — planner wrote it; do not orchestrate yet.
- `approved` — the user explicitly accepted this file. Only the user flips this. Planner never self-approves.

### Amendments

Never silently rewrite an approved plan. Append a dated entry under `## Amendment Log` (what changed, which criteria/steps, why — usually a `NEEDS_REPLAN` signal) and set `status: draft`. The user must approve again before orchestrator resumes. Keep prior step ids stable; add `S3` rather than renumbering unless the old steps are obsolete, in which case say so in the log.
