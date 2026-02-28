#!/bin/bash
# openclaw-config-backup.sh - Automatic config backup before edits
# Place in ~/bin/ or ~/.openclaw/scripts/

CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
BACKUP_DIR="${HOME}/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/openclaw.json.${TIMESTAMP}"
LATEST_LINK="${BACKUP_DIR}/openclaw.json.latest"

# Ensure backup dir exists
mkdir -p "$BACKUP_DIR"

# Keep only last 50 backups
rotate_backups() {
    ls -t "$BACKUP_DIR"/openclaw.json.* 2>/dev/null | tail -n +51 | xargs -r rm -f
}

# Create backup
create_backup() {
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        ln -sf "$BACKUP_FILE" "$LATEST_LINK"
        echo "Backup created: $BACKUP_FILE"
        rotate_backups
    else
        echo "ERROR: Config file not found at $CONFIG_FILE" >&2
        exit 1
    fi
}

create_backup