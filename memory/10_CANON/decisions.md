# Canon: Decisions

Architectural and behavioral decisions that shape the agent.

## Format
- Decision: [description] [YYYY-MM-DD] [scope]

## Global Decisions

*No decisions recorded yet. Nightly compaction will populate this.*
- Decision: Memory Architect system initialized with 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) [2026-02-27] [system:memory]
- Decision: GitHub repo set as durable source of truth; OpenClaw pre-compaction flush enabled [2026-02-27] [system:memory]
- Decision: Model selection policy — classify tasks as LOW/MEDIUM/HIGH complexity, route to cheapest sufficient model, escalate only when needed [2026-02-27] [system:models]
