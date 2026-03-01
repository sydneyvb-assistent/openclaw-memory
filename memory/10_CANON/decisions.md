# Canon: Decisions

Architectural and behavioral decisions that shape the agent.

## Format
- Decision: [description] [YYYY-MM-DD] [scope]

## CRITICAL: Development Orchestrator Decisions (STRICT)

- Decision: Role is ORCHESTRATOR not CODER — I write PRDs and delegate to Codex [2026-02-28] [system:development]
- Decision: I do NOT write code — exception only for trivial <=10 line fixes [2026-02-28] [system:development]
- Decision: If Codex unavailable, I must ASK before coding myself — NEVER assume [2026-02-28] [system:development]
- Decision: This rule is ABSOLUTE — no exceptions for "quick" or "small" changes [2026-02-28] [system:development]

## Memory System Decisions

- Decision: Memory Architect 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) is the canonical memory system [2026-02-27] [system:memory]
- Decision: GitHub repo is the durable source of truth; auto-commit and push enabled [2026-02-27] [system:memory]
- Decision: QMD (Quick Markdown Search) is the retrieval backend for hybrid search [2026-02-28] [system:memory]
- Decision: Nightly compaction runs at 3:00 AM via LaunchAgent ai.openclaw.memory-maintenance [2026-02-28] [system:memory]
- Decision: Pre-compaction flush writes typed items to memory/30_SESSIONS/YYYY-MM-DD.md before compaction triggers [2026-02-27] [system:memory]
- Decision: WORKING tier (inbox/scratch) is emptied nightly; durable items promoted to CANON [2026-02-27] [system:memory]

## Model Routing Decisions

- Decision: DEFAULT model is Moonshot kimi-k2.5 for almost everything (strong default) [2026-02-28] [system:models]
- Decision: STRICT TRIVIAL GATE defines when downshift to cheaper models is allowed [2026-02-28] [system:models]
- Decision: TRIVIAL tier: OpenAI gpt-5-nano (primary), Groq llama-3.1-8b-instant, Anthropic claude-haiku-4-5 [2026-02-28] [system:models]
- Decision: NON-TRIVIAL tier: Moonshot kimi-k2.5 (primary), Anthropic claude-sonnet-4-6, OpenAI gpt-5.2, Groq llama-3.3-70b-versatile [2026-02-28] [system:models]
- Decision: HEAVY tier: Moonshot kimi-k2-thinking (primary), Anthropic claude-opus-4-6, OpenAI gpt-5.2 [2026-02-28] [system:models]
- Decision: Escalate immediately to NON-TRIVIAL if: steps/planning, code/config/commands, >5 sentences, tools needed, uncertainty [2026-02-28] [system:models]
- Decision: Escalate to HEAVY if: NON-TRIVIAL output inconsistent, task clearly complex/high-stakes [2026-02-28] [system:models]
- Decision: Cost discipline ONLY on STRICTLY TRIVIAL requests; competence > cost for real tasks [2026-02-28] [system:models]
- Decision: Policy is: strong default + trivial downshift + fast escalation [2026-02-28] [system:models]

## Config Safety Decisions

- Decision: Config recovery system with backup/validate/restore scripts in ~/bin/ [2026-02-28] [system:safety]
- Decision: openclaw-config-edit.sh is the ONLY allowed method for config modifications [2026-02-28] [system:safety]
- Decision: Daily config backup cron at 3:00 AM [2026-02-28] [system:safety]- Decision: Memory Architect system initialized with 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) [2026-02-27] [system:memory]
- Decision: GitHub repo set as durable source of truth; OpenClaw pre-compaction flush enabled [2026-02-27] [system:memory]
- Decision: Model selection policy — classify tasks as LOW/MEDIUM/HIGH complexity, route to cheapest sufficient model, escalate only when needed [2026-02-27] [system:models]
- Decision: Memory Architect system initialized with 4-tier structure (CANON/PROJECTS/SESSIONS/WORKING) [2026-02-27] [system:memory]
