# Memory Architect System

**Persistent operational rules for OpenClaw memory management.**

This document is the canonical reference for the memory system. I must follow these rules every session.

---

## 1. Repository Structure (4-Tier)

```
memory/
├── 10_CANON/           # Small, stable, curated (NEVER lose these)
│   ├── constraints.md  # Hard rails and invariants
│   ├── decisions.md    # Architectural decisions
│   ├── preferences.md  # Stable preferences
│   └── README.md       # Canon rules
├── 20_PROJECTS/        # Bounded, scoped project memory
│   ├── <project>/
│   │   ├── decision-log.md
│   │   ├── open-questions.md
│   │   └── task-backlog.md
│   └── .template/      # Copy for new projects
├── 30_SESSIONS/        # Append-only daily flush notes
│   └── YYYY-MM-DD.md   # One file per day
└── 40_WORKING/         # Temporary inbox/scratch (EMPTIED nightly)
    ├── inbox.md
    └── scratch.md
```

**Rule:** If CANON grows >200 lines, split by domain. Keep file count minimal.

---

## 2. Typed Memory Format (MANDATORY)

Every stored memory MUST use these exact types:

```markdown
- [Type]: [description] [YYYY-MM-DD] [scope]

Types: Constraint:, Decision:, Preference:, Task:, OpenQuestion:
Scope: [global], [project:<name>], [system:<component>]

Examples:
- Constraint: NEVER store secrets in memory [2026-02-28] [global]
- Decision: Use QMD for retrieval [2026-02-28] [system:memory]
- Task: Complete setup [2026-02-28] [project:memory-architect]
- OpenQuestion: How to handle large files? [2026-02-28] [system:memory]
```

**Rules:**
- 1-2 bullets per item (max)
- Include date and scope on every entry
- No prose, no speculation, no repetition

---

## 3. Read Before Write (NON-NEGOTIABLE)

Before ANY plan, config change, or decision:

1. Search memory using `memory_search`:
   ```
   query: "constraint config"
   maxResults: 10
   ```

2. If constraint/decision exists → FOLLOW IT
3. If conflict exists → CANON wins, record "Conflict:" in today's session

---

## 4. Write Before Compaction/Reset (MANDATORY)

MUST write typed items to today's session file BEFORE:
- Any decision is made
- Any constraint/rail is introduced
- Any stable preference appears
- Tasks are assigned
- An open question blocks progress
- Triggering compaction / reset / milestone

**Location:** `memory/30_SESSIONS/YYYY-MM-DD.md`

---

## 5. Pre-Compaction Flush

OpenClaw auto-flushes when context nears compaction:
- Trigger: `softThresholdTokens: 4000`
- Action: Extract typed items, write to session file
- Response: `NO_REPLY`

**I do NOT see this flush.** It's automatic.

---

## 6. Nightly Compaction (3:00 AM)

LaunchAgent `ai.openclaw.memory-maintenance` runs:

1. **Config backup** → `~/.openclaw/backups/`
2. **Python compaction** (`scripts/nightly_compact.py`):
   - Parse session files (last 7 days)
   - Promote items to CANON (deduplicated)
   - Archive WORKING files
3. **QMD reindex**: `qmd update && qmd embed`
4. **Git commit + push**: `nightly: compact memory YYYY-MM-DD`

---

## 7. QMD Retrieval (Primary Search)

**Installation:** `npm link /tmp/qmd` (built from source)

**Commands:**
```bash
qmd query "semantic search"     # Hybrid (semantic + lexical)
qmd search "lexical keywords"   # BM25 only
qmd vsearch "vector query"      # Vector only
qmd get memory/10_CANON/constraints.md  # Fetch file
```

**After ANY memory change:**
```bash
qmd update    # Reindex
qmd embed     # Regenerate embeddings
```

**Collection:** `memory` → `~/.openclaw/workspace/memory/**/*.md`

---

## 8. Config Safety (NEVER FORGET)

**Before ANY config edit:**
```bash
openclaw-config-backup.sh              # Create backup
openclaw-config-edit.sh <script.py>    # Safe edit with validation
openclaw-config-restore.sh             # If needed
```

**Never:**
- Edit `openclaw.json` directly
- Run `sed` or manual edits on config
- Skip validation

---

## 9. Quick Reference Commands

```bash
# Test retrieval
qmd query "constraint memory"

# Manual compaction
cd ~/.openclaw/workspace && python3 scripts/nightly_compact.py

# Check cron status
launchctl list | grep openclaw

# View logs
tail -f ~/.openclaw/logs/memory-maintenance.log
```

---

## 10. Operational SLOs

| SLO | Target | Measurement |
|-----|--------|-------------|
| Durability | 100% | Critical facts in CANON survive sessions |
| Retrievability | >95% | Relevant memory surfaced before action |
| Compaction Safety | 0 loss | Never lose constraints/decisions |

---

## 11. If Something Breaks

| Problem | Fix |
|---------|-----|
| `memory_search` returns nothing | `qmd update && qmd embed` |
| QMD not found | Check PATH: `which qmd` |
| Compaction not running | `launchctl list \| grep openclaw` |
| Config corrupted | `openclaw-config-restore.sh` |
| Git conflicts | `cd ~/.openclaw/workspace && git pull --rebase` |

---

## 12. Commit This to Memory

**Every session I MUST:**
1. ✅ Read SOUL.md, USER.md, MEMORY.md (this file)
2. ✅ Search memory before acting
3. ✅ Write typed items before compaction
4. ✅ Use qmd for retrieval
5. ✅ Commit changes to GitHub

**Never:**
- ❌ Store secrets in memory files
- ❌ Edit config without backup
- ❌ Forget to run `qmd embed` after changes

---

*Last updated: 2026-02-28*
*Canonical source: https://github.com/sydneyvb-assistent/openclaw-memory/*