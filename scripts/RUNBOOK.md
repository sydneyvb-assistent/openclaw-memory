# Memory Architect: Operational Runbook

## Quick Commands

### Test Retrieval

```bash
# 1. Reindex memory
openclaw memory index --force

# 2. Search for constraints
openclaw memory search --query "constraint memory"

# 3. Get specific file
openclaw memory search --query "CANON"
```

### Manual Compaction

```bash
# Run nightly compaction manually
python3 ~/.openclaw/workspace/scripts/nightly_compact.py

# Check cron status
openclaw cron list
openclaw cron runs --id 8e6be817-0481-4114-8d3e-2fa06f84545d
```

### Add Project

```bash
PROJECT_NAME="my-project"
mkdir -p ~/.openclaw/workspace/memory/20_PROJECTS/$PROJECT_NAME
cp ~/.openclaw/workspace/memory/20_PROJECTS/.template/*.md \
   ~/.openclaw/workspace/memory/20_PROJECTS/$PROJECT_NAME/
# Edit files to replace {{PROJECT_NAME}}
```

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| `memory_search` returns nothing | Index status | Run `openclaw memory index --force` |
| memoryFlush not firing | Config values | `openclaw config get agents.defaults.compaction.memoryFlush` |
| Compaction deletes items | Working vs Canon | Ensure items promoted before WORKING cleared |
| QMD not working | Binary path | Install: `bun install -g https://github.com/tobi/qmd` |
| Git conflicts | Remote state | Run `git pull --rebase` before compaction |
| Cron not running | Gateway status | `openclaw gateway status` must show running |

## File Locations

| Component | Path |
|-----------|------|
| Workspace | `~/.openclaw/workspace/` |
| Memory | `~/.openclaw/workspace/memory/` |
| Scripts | `~/.openclaw/workspace/scripts/` |
| Config | `~/.openclaw/openclaw.json` |
| Cron jobs | `~/.openclaw/cron/jobs.json` |
| Session store | `~/.openclaw/agents/main/sessions/sessions.json` |

## Configuration Reference

### Pre-Compaction Flush

```bash
openclaw config get agents.defaults.compaction.memoryFlush
```

Expected output:
```json
{
  "enabled": true,
  "softThresholdTokens": 4000,
  "systemPrompt": "Session nearing compaction...",
  "prompt": "Flush now: extract..."
}
```

### Memory Search

```bash
openclaw config get agents.defaults.memorySearch
```

Expected output includes:
- `enabled: true`
- `provider: "gemini"`
- `query.hybrid.enabled: true`
- `query.hybrid.mmr.enabled: true`
- `query.hybrid.temporalDecay.enabled: true`

## Restart Gateway

After config changes:

```bash
openclaw gateway restart
```

## Daily Workflow

1. **During day**: Agent writes typed items to `memory/30_SESSIONS/YYYY-MM-DD.md`
2. **Pre-compaction**: Auto-flush writes any pending items
3. **03:00 AM**: Nightly cron runs compaction script
4. **Compaction**: Promotes items to CANON/PROJECTS, clears WORKING, commits to git

## Typed Memory Format

```markdown
- [Type]: [description] [YYYY-MM-DD] [scope]

Types: Constraint:, Decision:, Preference:, Task:, OpenQuestion:
Scope: [global], [project:<name>], [system:<component>]

Example:
- Constraint: NEVER store secrets in memory [2026-02-27] [global]
- Decision: Use Gemini for embeddings [2026-02-27] [system:memory]
- Task: Complete QMD setup [2026-02-27] [project:memory-architect]
```
