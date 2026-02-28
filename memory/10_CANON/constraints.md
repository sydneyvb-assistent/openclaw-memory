# Canon: Constraints

Hard rails and invariants for the agent. These are non-negotiable.

## Format
- Constraint: [description] [YYYY-MM-DD] [scope]

## Memory System Constraints

- Constraint: NEVER store secrets/tokens/credentials in memory files [2026-02-27] [global]
- Constraint: ALWAYS search memory before making decisions or changing config [2026-02-27] [global]
- Constraint: ALWAYS write typed items before compaction/reset/milestone [2026-02-27] [global]
- Constraint: Memory Architect 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) is the persistent source of truth [2026-02-27] [system:memory]
- Constraint: GitHub repo is the durable source of truth; all durable memory must be committed [2026-02-27] [system:memory]
- Constraint: Use ONLY typed memory format (Constraint:/Decision:/Preference:/Task:/OpenQuestion:) [2026-02-27] [global]
- Constraint: Pre-compaction flush MUST write to memory/30_SESSIONS/YYYY-MM-DD.md [2026-02-27] [system:memory]
- Constraint: Nightly compaction promotes items from SESSIONS to CANON; WORKING is emptied [2026-02-27] [system:memory]

## Model Routing Constraints (NEW POLICY)

- Constraint: DEFAULT model is ALWAYS Moonshot kimi-k2.5 (NON-TRIVIAL tier) [2026-02-28] [system:models]
- Constraint: DOWNSHIFT to TRIVIAL tier ONLY when STRICT TRIVIAL GATE passes [2026-02-28] [system:models]
- Constraint: STRICT TRIVIAL GATE: no tools, no multi-step, no irreversible action, <=5 sentences, no config/security/finance/debugging [2026-02-28] [system:models]
- Constraint: When in doubt: NOT TRIVIAL — use NON-TRIVIAL default [2026-02-28] [system:models]
- Constraint: TRIVIAL tier: OpenAI gpt-5-nano (primary), Groq llama-3.1-8b-instant, Anthropic claude-haiku-4-5 [2026-02-28] [system:models]
- Constraint: NON-TRIVIAL tier: Moonshot kimi-k2.5 (primary), Anthropic claude-sonnet-4-6, OpenAI gpt-5.2, Groq llama-3.3-70b-versatile [2026-02-28] [system:models]
- Constraint: HEAVY tier: Moonshot kimi-k2-thinking (primary), Anthropic claude-opus-4-6, OpenAI gpt-5.2 — ONLY for complex/high-stakes tasks [2026-02-28] [system:models]
- Constraint: Escalate to NON-TRIVIAL immediately if: steps/planning needed, code/config/commands, >5 sentences, tools needed, uncertainty [2026-02-28] [system:models]
- Constraint: Escalate to HEAVY if: NON-TRIVIAL output inconsistent, task clearly complex/high-stakes [2026-02-28] [system:models]
- Constraint: Fallback policy: retry same model once → next fallback → escalate tier; silent unless affects correctness [2026-02-28] [system:models]
- Constraint: Cost discipline ONLY on STRICTLY TRIVIAL requests; for real tasks: competence > cost [2026-02-28] [system:models]
- Constraint: NEVER use multiple model calls unless failure forces fallback [2026-02-28] [system:models]

## QMD Retrieval Constraints

- Constraint: QMD is the primary retrieval backend for memory search [2026-02-28] [system:memory]
- Constraint: ALWAYS run 'qmd update' and 'qmd embed' after memory changes [2026-02-28] [system:memory]
- Constraint: Use 'qmd query' for semantic search, 'qmd search' for lexical search [2026-02-28] [system:memory]

## Config Safety Constraints

- Constraint: ALWAYS backup config before editing using openclaw-config-backup.sh [2026-02-28] [system:safety]
- Constraint: ALWAYS validate config with openclaw-config-validate.sh before applying [2026-02-28] [system:safety]
- Constraint: Use openclaw-config-edit.sh for ALL config modifications [2026-02-28] [system:safety]
- Constraint: NEVER modify openclaw.json directly without backup + validation [2026-02-28] [system:safety]