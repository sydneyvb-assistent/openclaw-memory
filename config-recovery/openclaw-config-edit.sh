#!/bin/bash
# openclaw-config-edit.sh - SAFE config editor with automatic backup + validation
# Use this instead of editing openclaw.json directly
# Usage: openclaw-config-edit.sh [python-script-file]
# If python-script-file provided, it will be executed to modify the config
# Otherwise, opens editor with validation on save

set -euo pipefail

CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${SCRIPT_DIR}/openclaw-config-backup.sh"
VALIDATE_SCRIPT="${SCRIPT_DIR}/openclaw-config-validate.sh"
RESTORE_SCRIPT="${SCRIPT_DIR}/openclaw-config-restore.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() { echo -e "${GREEN}[SAFE-EDIT]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Step 1: Create backup
log "Creating backup..."
if ! bash "$BACKUP_SCRIPT"; then
    error "Backup failed, aborting"
    exit 1
fi

# Step 2: If Python script provided, run it
if [ -n "${1:-}" ] && [ -f "$1" ]; then
    log "Applying changes from: $1"
    
    # Create temp file for modified config
    TEMP_CONFIG=$(mktemp)
    cp "$CONFIG_FILE" "$TEMP_CONFIG"
    
    # Run the Python script with temp config
    if python3 "$1" "$TEMP_CONFIG"; then
        log "Python script completed"
    else
        error "Python script failed"
        rm -f "$TEMP_CONFIG"
        exit 1
    fi
    
    # Validate the result
    log "Validating changes..."
    if bash "$VALIDATE_SCRIPT" "$TEMP_CONFIG"; then
        log "Validation passed, applying to live config"
        cp "$TEMP_CONFIG" "$CONFIG_FILE"
        rm -f "$TEMP_CONFIG"
    else
        error "Validation failed! Changes not applied."
        warn "Temp file kept at: $TEMP_CONFIG"
        warn "To restore from backup: bash $RESTORE_SCRIPT"
        exit 1
    fi
else
    # Interactive mode - open editor
    log "Opening editor (manual edit mode)"
    warn "Make your changes, save and quit. Config will be validated."
    
    TEMP_CONFIG=$(mktemp)
    cp "$CONFIG_FILE" "$TEMP_CONFIG"
    
    ${EDITOR:-vi} "$TEMP_CONFIG"
    
    log "Validating changes..."
    if bash "$VALIDATE_SCRIPT" "$TEMP_CONFIG"; then
        log "Validation passed, applying to live config"
        cp "$TEMP_CONFIG" "$CONFIG_FILE"
        rm -f "$TEMP_CONFIG"
    else
        error "Validation failed! Changes not applied."
        warn "Review errors above. Your edited file is at: $TEMP_CONFIG"
        warn "To restore from backup: bash $RESTORE_SCRIPT"
        read -p "Apply anyway? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            warn "Forcing apply despite validation errors"
            cp "$TEMP_CONFIG" "$CONFIG_FILE"
            rm -f "$TEMP_CONFIG"
        else
            rm -f "$TEMP_CONFIG"
            exit 1
        fi
    fi
fi

log "Config updated successfully"

# Step 3: Offer restart
if openclaw gateway status 2>/dev/null | grep -q "running"; then
    read -p "Restart OpenClaw gateway to apply changes? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        openclaw gateway restart
    fi
fi