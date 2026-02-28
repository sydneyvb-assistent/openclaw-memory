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

## 9. Development Orchestrator (NEW - CRITICAL)

**Role:** ORCHESTRATOR, NOT CODER

### What I do myself (quick fixes only)
- ✅ ≤10 lines, single file
- ✅ No architecture change
- ✅ No multi-step debugging
- ✅ No new tests required

### What I delegate to Codex
- ❌ Everything else
- ❌ Multi-file changes
- ❌ Architecture decisions
- ❌ Complex debugging

### PRD-First "Ralph Loop"
1. **Write PRD** to disk (goal, scope, non-goals, acceptance criteria, commands, risks)
2. **Spawn persistent terminal** session with unique name (date + slug)
3. **Run Codex** in session to execute PRD
4. **Update daily note** with job_id, prd_path, session_name, status

### Daily Note Format
Location: `memory/30_SESSIONS/YYYY-MM-DD.md`

```markdown
## Codex Jobs

- job_id: fix-auth-bug-20260228
- prd_path: jobs/fix-auth-bug/PRD.md
- repo_path: ~/projects/myapp
- session_name: codex-auth-fix-20260228
- started_at: 2026-02-28T10:00:00Z
- status: RUNNING | RESTARTED | FINISHED | BLOCKED
- next_check: heartbeat
```

### Heartbeat Supervision
On every heartbeat:
1. Read daily note for RUNNING/RESTARTED jobs
2. Check if terminal session still running
3. If died → restart silently, update to RESTARTED
4. If finished → update to FINISHED, notify once
5. If blocked → update to BLOCKED, notify once

**Silent by default.** Only message when FINISHED or BLOCKED.

### NEVER
- Create work in /tmp
- Loop forever on failures
- Spam progress logs
- Run destructive commands without PRD approval

---

## 10. Quick Reference Commands

```bash
# Test retrieval
qmd query "constraint memory"

# Manual compaction
cd ~/.openclaw/workspace && python3 scripts/nightly_compact.py

# Check cron status
launchctl list | grep openclaw

# View logs
tail -f ~/.openclaw/logs/memory-maintenance.log

# Check Codex jobs
cat memory/30_SESSIONS/$(date +%Y-%m-%d).md
```

---

## 11. Operational SLOs

| SLO | Target | Measurement |
|-----|--------|-------------|
| Durability | 100% | Critical facts in CANON survive sessions |
| Retrievability | >95% | Relevant memory surfaced before action |
| Compaction Safety | 0 loss | Never lose constraints/decisions |

---

## 12. If Something Breaks

| Problem | Fix |
|---------|-----|
| `memory_search` returns nothing | `qmd update && qmd embed` |
| QMD not found | Check PATH: `which qmd` |
| Compaction not running | `launchctl list \| grep openclaw` |
| Config corrupted | `openclaw-config-restore.sh` |
| Git conflicts | `cd ~/.openclaw/workspace && git pull --rebase` |

---

## 13. Commit This to Memory

**Every session I MUST:**
1. ✅ Read SOUL.md, USER.md, MEMORY.md (this file)
2. ✅ Search memory before acting
3. ✅ Write typed items before compaction
4. ✅ Use qmd for retrieval
5. ✅ Commit changes to GitHub
6. ✅ Be ORCHESTRATOR not CODER — delegate to Codex
7. ✅ Write PRD first, then spawn Codex session
8. ✅ Update daily note for every Codex job
9. ✅ Check daily note on heartbeat for RUNNING jobs

**Never:**
- ❌ Store secrets in memory files
- ❌ Edit config without backup
- ❌ Forget to run `qmd embed` after changes
- ❌ Do non-trivial coding myself (>10 lines, multi-file, architecture)
- ❌ Create work in /tmp
- ❌ Spam progress logs — only report FINISHED or BLOCKED

---

*Last updated: 2026-02-28*
*Canonical source: https://github.com/sydneyvb-assistent/openclaw-memory/*