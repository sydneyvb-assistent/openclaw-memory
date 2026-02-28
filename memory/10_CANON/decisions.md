# Canon: Decisions

Architectural and behavioral decisions that shape the agent.

## Format
- Decision: [description] [YYYY-MM-DD] [scope]

## Memory System Decisions

- Decision: Memory Architect 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) is the canonical memory system [2026-02-27] [system:memory]
- Decision: GitHub repo is the durable source of truth; auto-commit and push enabled [2026-02-27] [system:memory]
- Decision: QMD (Quick Markdown Search) is the retrieval backend for hybrid search [2026-02-28] [system:memory]
- Decision: Nightly compaction runs at 3:00 AM via LaunchAgent ai.openclaw.memory-maintenance [2026-02-28] [system:memory]
- Decision: Pre-compaction flush writes typed items to memory/30_SESSIONS/YYYY-MM-DD.md before compaction triggers [2026-02-27] [system:memory]
- Decision: WORKING tier (inbox/scratch) is emptied nightly; durable items promoted to CANON [2026-02-27] [system:memory]

## Model Routing Decisions

- Decision: Model selection policy — classify tasks as LOW/MEDIUM/HIGH complexity, route to cheapest sufficient model [2026-02-27] [system:models]
- Decision: Primary default model is moonshot/kimi-k2.5 [2026-02-28] [system:models]
- Decision: Escalate to OpenAI/Anthropic only for high-stakes tasks or Groq failures [2026-02-27] [system:models]

## Config Safety Decisions

- Decision: Config recovery system with backup/validate/restore scripts in ~/bin/ [2026-02-28] [system:safety]
- Decision: openclaw-config-edit.sh is the ONLY allowed method for config modifications [2026-02-28] [system:safety]
- Decision: Daily config backup cron at 3:00 AM [2026-02-28] [system:safety]