---
name: dirty-tree
description: Editing files that already carry the user's uncommitted changes cannot be committed alone
metadata:
  type: project
---

If a target file is untracked or has user uncommitted edits (HEAD is an older version), a per-hunk commit is impossible. Leave it uncommitted and point the reviewer at the working tree.

**Why:** the user told us never to stage unrelated changes.
**How to apply:** check `git status` for target files before dispatching; tell implementers not to commit those.
