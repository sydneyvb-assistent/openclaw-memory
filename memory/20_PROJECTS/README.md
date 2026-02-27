# Projects Directory

Bounded, scoped project memory. Each subdirectory is a project namespace.

## Structure

```
20_PROJECTS/
└── <project-name>/
    ├── decision-log.md    # Project-specific decisions
    ├── open-questions.md  # Unresolved questions
    └── task-backlog.md    # Active and pending tasks
```

## Creating a New Project

1. Create subdirectory: `mkdir 20_PROJECTS/<project-name>`
2. Copy template files from `.template/`
3. Add project-specific constraints/decisions as needed

## Archiving

When a project completes, move to `memory/archive/projects/<project-name>-YYYY-MM-DD/`
