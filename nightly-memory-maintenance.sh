#!/bin/bash
# nightly-memory-maintenance.sh
# Daily maintenance for OpenClaw memory system
# Runs at 3:00 AM via cron

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
LOG_FILE="${HOME}/.openclaw/logs/memory-maintenance.log"
BACKUP_DIR="${HOME}/.openclaw/backups"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Memory Maintenance Started ==="

# 1. Backup config (if not already done by config-backup)
if [ -f "${HOME}/bin/openclaw-config-backup.sh" ]; then
    log "Running config backup..."
    bash "${HOME}/bin/openclaw-config-backup.sh" >> "$LOG_FILE" 2>&1 || true
fi

# 2. Empty WORKING tier (40_WORKING)
log "Cleaning WORKING tier..."
if [ -d "${MEMORY_DIR}/40_WORKING" ]; then
    # Move files older than 7 days to archive, delete the rest
    find "${MEMORY_DIR}/40_WORKING" -type f -mtime +7 -exec mv {} "${BACKUP_DIR}/" \; 2>/dev/null || true
    find "${MEMORY_DIR}/40_WORKING" -type f -delete 2>/dev/null || true
    log "WORKING tier cleaned"
else
    log "WORKING tier directory not found"
fi

# 3. Archive old session files (30_SESSIONS older than 30 days)
log "Archiving old session files..."
if [ -d "${MEMORY_DIR}/30_SESSIONS" ]; then
    ARCHIVE_DIR="${MEMORY_DIR}/.archive/sessions"
    mkdir -p "$ARCHIVE_DIR"
    find "${MEMORY_DIR}/30_SESSIONS" -name "*.md" -mtime +30 -exec gzip {} \; -exec mv {}.gz "$ARCHIVE_DIR/" \; 2>/dev/null || true
    log "Old sessions archived"
fi

# 4. Promote durable items from sessions to canon (placeholder - requires agent logic)
log "Session compaction reminder: Review memory/30_SESSIONS for items to promote to 10_CANON/"

# 5. Git commit any pending changes
log "Checking for git changes..."
cd "$WORKSPACE"
if [ -d .git ]; then
    # Add new memory files
    git add memory/ 2>/dev/null || true
    git add "*.qmd" 2>/dev/null || true
    
    # Check if there are changes to commit
    if ! git diff --cached --quiet; then
        git commit -m "chore: nightly memory maintenance $(date +%Y-%m-%d)

- Archive old session files
- Clean WORKING tier
- Backup config" >> "$LOG_FILE" 2>&1 || true
        
        # Push to GitHub
        if git push origin main >> "$LOG_FILE" 2>&1; then
            log "Changes pushed to GitHub"
        else
            log "WARNING: Push failed (may need manual intervention)"
        fi
    else
        log "No changes to commit"
    fi
else
    log "Not a git repository"
fi

log "=== Memory Maintenance Complete ==="
echo "" >> "$LOG_FILE"