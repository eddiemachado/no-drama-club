---
description: Push the current branch and open a GitHub pull request using the repo PR template
argument-hint: "[optional context]"
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git branch:*), Bash(git switch:*), Bash(git push:*), Bash(gh repo view:*), Bash(gh pr view:*), Bash(gh pr create:*)
---

Context: $ARGUMENTS

## 1. Check

- `git status --porcelain`: uncommitted changes → run `/git-commit` first, then continue.
- Base = `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.
- `gh pr view --json url -q .url`: a PR already exists → reply with its URL and stop.

## 2. Branch

On the base branch → `git switch -c <name>` per `.agents/rules/git.md`.

## 3. Gather

- `git log --oneline <base>..HEAD`. No commits → stop.
- `git diff --stat <base>...HEAD`.
- If a plan matches this work: `.agents/.plans/<slug>.md` and the `## Result` in `.agents/.plans/<slug>.review.md`.

## 4. Push

`git push -u origin HEAD`. Never force-push.

## 5. Create

Fill `.github/pull_request_template.md`:
- Every section filled; write "None" where nothing applies. Drop the HTML comments.
- Terse. Facts from commits, diff, and plan only.
- End the body with: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

Title: `<type>: <summary>` per `.agents/rules/git.md` (it becomes the squash commit on `main`).

`gh pr create --base <base> --title "<title>" --body-file - <<'EOF' … EOF`

## 6. Reply

PR URL.
