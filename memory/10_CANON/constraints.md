# Canon: Constraints

Hard rails and invariants for the agent. These are non-negotiable.

## Format
- Constraint: [description] [YYYY-MM-DD] [scope]

## Global Constraints

- Constraint: NEVER store secrets/tokens/credentials in memory files [2026-02-27] [global]
- Constraint: ALWAYS search memory before making decisions or changing config [2026-02-27] [global]
- Constraint: ALWAYS write typed items before compaction/reset/milestone [2026-02-27] [global]
- Constraint: Memory Architect 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) is the persistent source of truth [2026-02-27] [system:memory]
- Constraint: GitHub repo is the durable source of truth; all durable memory must be committed [2026-02-27] [system:memory]
- Constraint: Use ONLY typed memory format (Constraint:/Decision:/Preference:/Task:/OpenQuestion:) [2026-02-27] [global]
- Constraint: Pre-compaction flush MUST write to memory/30_SESSIONS/YYYY-MM-DD.md [2026-02-27] [system:memory]
- Constraint: Nightly compaction promotes items from SESSIONS to CANON; WORKING is emptied [2026-02-27] [system:memory]

## Model Routing Constraints

- Constraint: LOW tasks → Groq/Moonshot small models; MEDIUM → OpenAI mid/Claude Sonnet; HIGH → Claude Opus/OpenAI flagship [2026-02-27] [system:models]
- Constraint: NEVER default to strongest model without justification; escalate progressively one tier at a time [2026-02-27] [system:models]
- Constraint: Fallback policy: retry same model → alternative provider same tier → escalate one tier; silent unless impacts correctness [2026-02-27] [system:models]
- Constraint: LOW models — Primary: openai/gpt-5-nano; Fallback: groq/llama-3.1-8b-instant, anthropic/claude-haiku-4-5 [2026-02-27] [system:models]
- Constraint: MEDIUM models — Primary: openai/gpt-5-mini; Fallback: anthropic/claude-sonnet-4-6, groq/llama-3.3-70b-versatile, moonshot/kimi-k2.5 [2026-02-27] [system:models]
- Constraint: HIGH models — Primary: anthropic/claude-opus-4-6; Fallback: openai/gpt-5.2, moonshot/kimi-k2-thinking [2026-02-27] [system:models]

## QMD Retrieval Constraints

- Constraint: QMD is the primary retrieval backend for memory search [2026-02-28] [system:memory]
- Constraint: ALWAYS run 'qmd update' and 'qmd embed' after memory changes [2026-02-28] [system:memory]
- Constraint: Use 'qmd query' for semantic search, 'qmd search' for lexical search [2026-02-28] [system:memory]

## Config Safety Constraints

- Constraint: ALWAYS backup config before editing using openclaw-config-backup.sh [2026-02-28] [system:safety]
- Constraint: ALWAYS validate config with openclaw-config-validate.sh before applying [2026-02-28] [system:safety]
- Constraint: Use openclaw-config-edit.sh for ALL config modifications [2026-02-28] [system:safety]
- Constraint: NEVER modify openclaw.json directly without backup + validation [2026-02-28] [system:safety]