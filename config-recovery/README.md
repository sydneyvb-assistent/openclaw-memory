# Config Recovery System

Automatische backup, validatie en recovery voor OpenClaw config.

## Snelstart

```bash
# 1. Deploy scripts
cd ~/.openclaw/workspace/config-recovery
chmod +x *.sh
mkdir -p ~/bin
cp *.sh ~/bin/

# 2. Maak eerste backup
openclaw-config-backup.sh

# 3. Test restore (optioneel)
openclaw-config-restore.sh
```

## Scripts

| Script | Functie |
|--------|---------|
| `openclaw-config-backup.sh` | Maakt timestamped backup + symlink 'latest' |
| `openclaw-config-validate.sh` | Checkt JSON + model references |
| `openclaw-config-restore.sh` | Herstelt van backup (met emergency backup van huidige) |
| `openclaw-config-edit.sh` | **SAFE edit mode** — backup + validatie + edit in één |

## Gebruik

### Safe edit mode (aanbevolen)
```bash
openclaw-config-edit.sh
```
Opent editor, valideert bij save, maakt automatisch backup.

### Met Python script
```bash
openclaw-config-edit.sh fix-model-ids.py
```
Voert Python script uit op config, valideert resultaat.

### Handmatig herstellen
```bash
# Laatste backup
openclaw-config-restore.sh

# Specifieke backup
openclaw-config-restore.sh ~/.openclaw/backups/openclaw.json.20260228_091500
```

### Daily backup via cron
```bash
openclaw cron add --name "config-backup" \
  --schedule "0 3 * * *" \
  --command "~/bin/openclaw-config-backup.sh"
```

## Wat wordt gecontroleerd?

- ✅ JSON validiteit
- ✅ Required keys (models, agents, channels, gateway)
- ✅ Model references in allowlist
- ✅ Emergency backup voor restore

## Storage

- Backups: `~/.openclaw/backups/`
- Retentie: laatste 50 backups
- Latest symlink: `~/.openclaw/backups/openclaw.json.latest`