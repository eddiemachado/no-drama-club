---
description: Review uncommitted changes and commit them, or turn blocking issues into a mini plan
argument-hint: "[--reviewed <files…>] | [paths or topic]"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git branch:*), Bash(git switch:*)
---

Arguments: $ARGUMENTS

- **Workflow mode** (`--reviewed <files…>`): an agent in the plan workflow; the `reviewer` agent handles review. No review, no questions.
- **Manual mode** (default): optional paths or topic to scope the commit.

## 1. Scope

Run `git status --porcelain`. No changes → say so and stop.
- Workflow mode: scope = the listed files.
- Manual mode: scope = files matching the arg. No arg and changes span unrelated areas → pick the area the conversation points to; if unclear, list the groups and ask which to commit.

Workflow mode → skip to §4.

## 2. Review (manual mode)

1. `git diff HEAD --stat -- <scope>`, then `git diff HEAD -- <file>` per file.
2. Read untracked (`??`) files in full; they never appear in a diff.
3. Check against `.agents/agent-tools/reviewer/rules.md` (G-items) and the repo files it lists.
4. Tag each finding with severity, rule ID, and `file:line`:
   - `CRITICAL`: bug, security.
   - `MAJOR`: rule or convention violation, missing error handling.
   - `MINOR`: style, naming. Never blocks.

## 3. Blocking issues (any CRITICAL/MAJOR)

Don't commit. Write a mini plan per `.agents/skills/plan/references/plan-doc.md`:
- Context: review of manual edits.
- Steps: one per file group.
- Acceptance Criteria: one per blocking issue, phrased pass/fail; plus "out of scope: everything else".

Call `EnterPlanMode`, then `ExitPlanMode` with the plan. Stop. On approval, the `plan-approved` hook starts orchestrator + reviewer. Never start the orchestrator yourself.

## 4. Commit

1. `git branch --show-current`: on `main`/`master` → `git switch -c <type>/<short-slug>` per `.agents/rules/git.md`.
2. Stage scope files by name: `git add -- <files>`. Never `git add -A` or `git add .`. Skip files that look like secrets.
3. Message per `.agents/rules/git.md`.
4. `git commit -m "<message>"`, then confirm with `git status --porcelain`.

## 5. Reply

Commit hash and message, plus any `MINOR` notes. Manual mode only: offer `/git-create-pr`.
