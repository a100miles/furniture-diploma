# Agent instructions

Applies to any coding agent (Codex, Claude Code, Cursor, etc.) and to humans.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<optional body: what and why>

Refs: DIP-<n>
```

- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`, `style`
- Scope is optional: `backend`, `frontend`, `docs`, `ci`, etc.
- Subject: imperative mood, lowercase, no trailing period, 72 characters or fewer
- Breaking changes: add `!` after the type/scope and a `BREAKING CHANGE:` footer
- Put the YouTrack ticket in a `Refs: DIP-<n>` footer, not in the subject
- Do not add agent names as co-authors or add session/tool trailers
- Do not use the em dash; use a plain "-"

Examples:

```
feat(backend): add auto-layout endpoint

Refs: DIP-15
```

```
docs: add technology comparison

Refs: DIP-7
```
