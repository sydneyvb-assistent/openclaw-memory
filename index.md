# OpenClaw Memory Archive

This repository contains the persistent memory and configuration for the OpenClaw agent system.

## Structure

- **[memory/](memory/)** - Agent memory archive
  - `10_CANON/` - Core constraints, decisions, preferences
  - `20_PROJECTS/` - Project-scoped memory
  - `30_SESSIONS/` - Daily session logs
  - `40_WORKING/` - Scratch/inbox (emptied nightly)
  
- **[config-recovery/](config-recovery/)** - Safe config editing tools
  
- **Rendered Site** - [View on GitHub Pages](https://sydneyvb-assistent.github.io/openclaw-memory/)

## Quick Links

- [Memory Archive (Rendered)](https://sydneyvb-assistent.github.io/openclaw-memory/memory.html)
- [Today's Session](memory/30_SESSIONS/2026-02-27.md)
- [Constraints](memory/10_CANON/constraints.md)
- [Decisions](memory/10_CANON/decisions.md)

## System Configuration

- **Primary Model:** moonshot/kimi-k2.5
- **Backup Models:** See routing-config.json
- **Gateway:** Auto-start via LaunchAgent
- **Config Backups:** Daily at 3:00 AM

## Recovery

If config is corrupted:
```bash
bash ~/bin/openclaw-config-restore.sh
```

---

*Last updated: 2026-02-28*