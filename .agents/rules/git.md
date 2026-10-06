# Git rules

## Branches

- Never commit or push on `main` or `master`. Before any commit, check `git branch --show-current`; on `main`/`master`, create a branch first.
- Branch name: `<type>/<short-slug>` (e.g. `feat/retro-skill`). For plan work, use the plan slug.
- Never force-push.

## Types

| Type | Use for |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace, lint fixes |
| `refactor` | Restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or external dependencies |
| `ci` | CI/CD changes |
| `chore` | Maintenance, config, dependencies |
| `revert` | Reverting previous commits |

## Commits

- Format: `<type>: <summary>`. Imperative, lowercase, no period, under 72 chars.
- Optional body: why, max 2 sentences.
- Branch commits can be small (per step or fix); they get squashed.

## Pull requests

- Merge by squash only. The PR title becomes the commit on `main`.
- PR title: `<type>: <summary>`, same rules as commits. Use the type of the main change.
