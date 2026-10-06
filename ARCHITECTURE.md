# ARCHITECTURE.md

## LLMs

- `.agents/` is the source of truth. Always create and edit agents, skills, hooks, and commands there.
- `.claude/` only holds symlinks to `.agents/` folders, plus `settings.json`. When adding a new top-level folder to `.agents/`, add a matching symlink in `.claude/` (e.g. `ln -s ../.agents/<folder> .claude/<folder>`).