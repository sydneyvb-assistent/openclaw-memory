# Canon: Constraints

Hard rails and invariants for the agent. These are non-negotiable.

## Format
- Constraint: [description] [YYYY-MM-DD] [scope]

## Global Constraints

- Constraint: NEVER store secrets/tokens/credentials in memory files [2026-02-27] [global]
- Constraint: ALWAYS search memory before making decisions or changing config [2026-02-27] [global]
- Constraint: ALWAYS write typed items before compaction/reset/milestone [2026-02-27] [global]
- Constraint: LOW tasks → Groq/Moonshot small models; MEDIUM → OpenAI mid/Claude Sonnet; HIGH → Claude Opus/OpenAI flagship [2026-02-27] [system:models]
- Constraint: NEVER default to strongest model without justification; escalate progressively one tier at a time [2026-02-27] [system:models]
- Constraint: Fallback policy: retry same model → alternative provider same tier → escalate one tier; silent unless impacts correctness [2026-02-27] [system:models]
- Constraint: NEVER store secrets/tokens/credentials in memory files [2026-02-27] [global]
- Constraint: ALWAYS search memory before making decisions or changing config [2026-02-27] [global]
- Constraint: ALWAYS write typed items before compaction/reset/milestone [2026-02-27] [global]
- Constraint: LOW tasks → Groq/Moonshot small models; MEDIUM → OpenAI mid/Claude Sonnet; HIGH → Claude Opus/OpenAI flagship [2026-02-27] [system:models]
- Constraint: NEVER default to strongest model without justification; escalate progressively one tier at a time [2026-02-27] [system:models]
- Constraint: Fallback policy: retry same model → alternative provider same tier → escalate one tier; silent unless impacts correctness [2026-02-27] [system:models]
- Constraint: LOW models — Primary: openai/gpt-5-nano; Fallback: groq/llama-3.1-8b-instant, anthropic/claude-haiku-4-5 [2026-02-27] [system:models]
- Constraint: MEDIUM models — Primary: openai/gpt-5-mini; Fallback: anthropic/claude-sonnet-4-6, groq/llama-3.3-70b-versatile, moonshot/kimi-k2.5 [2026-02-27] [system:models]
- Constraint: HIGH models — Primary: anthropic/claude-opus-4-6; Fallback: openai/gpt-5.2, moonshot/kimi-k2-thinking [2026-02-27] [system:models]
