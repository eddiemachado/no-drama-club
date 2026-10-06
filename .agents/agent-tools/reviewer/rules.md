# Reviewer — Standing Rules (Global)

Checked on every review. Each becomes a `G` item in the checklist.

- [ ] G1 No secrets or credentials committed
- [ ] G2 No features or work outside the plan's scope
- [ ] G3 Plan scope wasn't silently reinterpreted or expanded
- [ ] G4 No destructive operations beyond what the plan approved
- [ ] G5 No dead code or commented-out blocks left behind
- [ ] G6 Existing tests and lint pass (if the repo has them)
- [ ] G7 No bugs: logic errors, crashes, or bad null/empty handling under realistic inputs
- [ ] G8 No security holes: injection, unvalidated external input, missing auth checks
- [ ] G9 New logic branches have matching tests
- [ ] G10 No logic that duplicates something already in the codebase

Don't flag: style issues lint would catch, naming preferences, or hypothetical future needs outside the plan.

## Repo conventions

Read these once at startup (use what exists). Each documented rule that applies to the plan becomes an `R` item, citing its source:

1. `<repo>/AGENTS.md`
2. `<repo>/ARCHITECTURE.md`
3. `<repo>/DESIGN.md`
4. Lint/format/test config (`.eslintrc*`, `.prettierrc*`, `pyproject.toml`, `package.json` scripts)

If none exist, use the `G` items only and note the gap in the checklist.
