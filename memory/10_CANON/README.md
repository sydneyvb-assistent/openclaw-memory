# Canon: README

This directory contains the **canonical memory** — small, stable, curated facts that survive compaction.

## Files

| File | Purpose |
|------|---------|
| constraints.md | Hard rails and invariants |
| preferences.md | Stable preferences |
| decisions.md | Architectural decisions |

## Rules

1. Stay small. If a file exceeds 200 lines, split by domain.
2. Append-only. Never edit historical entries.
3. Typed entries only: Constraint:, Decision:, Preference:
4. Include date (YYYY-MM-DD) and scope tag on every entry.

## Scope Tags

- [global] — Applies to all sessions
- [project:<name>] — Applies to specific project
- [system:<component>] — Applies to system component
