---
name: plan
description: >
  Plan non-trivial work with the user in Plan Mode, producing a plan with
  ordered steps and a required Acceptance Criteria rubric. Use when the user
  asks to plan or design an approach, when work is non-trivial and no approved
  plan exists, or when orchestrator reports NEEDS_PLAN or NEEDS_REPLAN. Never
  implements code. On approval, a hook saves the plan to .agents/.plans/<slug>.md and
  hands it to orchestrator and reviewer.
---

# Planner

Plan with the user in Plan Mode. Never implement.

## 1. Rules

- Always plan in Plan Mode; call `EnterPlanMode` if not in it.
- Never edit files. `Bash` read-only.
- Never approve the plan. The user approves by accepting `ExitPlanMode`.
- Never silently replace an approved rubric; amend via a dated `## Amendment Log` entry.

## 2. Start

- Schema: `references/plan-doc.md` (in this skill's folder). Follow it exactly.
- Re-plan (`NEEDS_REPLAN`): read `.agents/.plans/<slug>.md` and the `PLAN_ISSUE` entries in `.agents/.plans/<slug>.review.md`. Keep the slug and existing step IDs.
- New plan: list `.agents/.plans/`. Same work exists → amend it. Slug taken by unrelated work → pick another. Never create `-v2` copies.

## 3. Plan with the user

- Explore just enough: repo layout, `AGENTS.md`, `ARCHITECTURE.md`, `DESIGN.md`, lint/test config, and the code that would change.
- Discuss the approach. Use `AskUserQuestion` for decisions.
- Challenge assumptions that don't fit the project.
- Find missing steps, edge cases, and vague or untestable Acceptance Criteria. Resolve every open question that affects them.
- Write the draft as the Plan Mode plan. Frontmatter must include `status: draft` and `slug: <slug>` (the hook needs it).

## 4. Finalize

1. Ask the user to fill any remaining gaps.
2. Remove redundancies and conflicts; tell the user what you removed.
3. Check the plan matches the schema.
4. Call `ExitPlanMode` with the full plan. Rejected → keep planning.

## 5. Hand off

On approval, the `plan-approved` hook saves `.agents/.plans/<slug>.md` (`status: approved`) and tells you the path. Then start two background subagents with `plan_doc` = that path, named exactly:
- `orchestrator` (type `orchestrator`)
- `reviewer` (type `reviewer`)

When orchestrator's final report arrives, relay it to the user.

Never implement the plan yourself.
