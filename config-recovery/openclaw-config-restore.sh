#!/bin/bash
# openclaw-config-restore.sh - Restore config from backup
# Usage: openclaw-config-restore.sh [backup-file]
# If no backup-file specified, restores latest backup

CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
BACKUP_DIR="${HOME}/.openclaw/backups"
LATEST_LINK="${BACKUP_DIR}/openclaw.json.latest"

# Find backup to restore
if [ -n "$1" ]; then
    BACKUP_FILE="$1"
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "ERROR: Backup file not found: $BACKUP_FILE" >&2
        exit 1
    fi
else
    if [ -L "$LATEST_LINK" ] && [ -f "$LATEST_LINK" ]; then
        BACKUP_FILE=$(readlink "$LATEST_LINK")
    else
        # Find most recent backup
        BACKUP_FILE=$(ls -t "$BACKUP_DIR"/openclaw.json.* 2>/dev/null | head -1)
    fi
fi

if [ -z "$BACKUP_FILE" ] || [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: No backup file found to restore" >&2
    echo "Available backups:" >&2
    ls -la "$BACKUP_DIR"/openclaw.json.* 2>/dev/null >&2 || echo "  (none)" >&2
    exit 1
fi

echo "Restoring from: $BACKUP_FILE"
echo "Target: $CONFIG_FILE"

# Validate backup before restoring
if ! python3 -c "import json; json.load(open('$BACKUP_FILE'))" 2>/dev/null; then
    echo "ERROR: Backup file contains invalid JSON!" >&2
    exit 1
fi

# Create emergency backup of current config if it exists
if [ -f "$CONFIG_FILE" ]; then
    EMERGENCY_BACKUP="${BACKUP_DIR}/openclaw.json.emergency_$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$EMERGENCY_BACKUP"
    echo "Emergency backup of current config: $EMERGENCY_BACKUP"
fi

# Restore
cp "$BACKUP_FILE" "$CONFIG_FILE"
echo "Config restored successfully"

# Restart gateway if running
if openclaw gateway status | grep -q "running"; then
    echo "Restarting OpenClaw gateway..."
    openclaw gateway restart
fi