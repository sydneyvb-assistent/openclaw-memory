#!/bin/bash
# nightly-memory-maintenance.sh
# Daily maintenance for OpenClaw memory system
# Runs at 3:00 AM via LaunchAgent

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
LOG_FILE="${HOME}/.openclaw/logs/memory-maintenance.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Memory Maintenance Started ==="

# 1. Backup config
if [ -f "${HOME}/bin/openclaw-config-backup.sh" ]; then
    log "Running config backup..."
    bash "${HOME}/bin/openclaw-config-backup.sh" >> "$LOG_FILE" 2>&1 || true
fi

# 2. Run Python compaction (the actual promotion logic)
log "Running Python compaction..."
if [ -f "${WORKSPACE}/scripts/nightly_compact.py" ]; then
    cd "$WORKSPACE"
    python3 scripts/nightly_compact.py >> "$LOG_FILE" 2>&1 || log "Compaction script had errors"
else
    log "ERROR: nightly_compact.py not found"
fi

# 3. Update QMD index
log "Updating QMD index..."
qmd update >> "$LOG_FILE" 2>&1 || true
qmd embed >> "$LOG_FILE" 2>&1 || true

log "=== Memory Maintenance Complete ==="
echo "" >> "$LOG_FILE"