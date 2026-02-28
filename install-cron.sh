#!/bin/bash
# Install nightly memory maintenance cron job
# Run this once to set up

CRON_LINE='0 3 * * * bash /Users/sydneyassistent/bin/nightly-memory-maintenance.sh >> /Users/sydneyassistent/.openclaw/logs/cron.log 2>&1'

# Add to crontab if not already present
(crontab -l 2>/dev/null | grep -v "nightly-memory-maintenance"; echo "$CRON_LINE") | crontab -

echo "Cron job installed. Current crontab:"
crontab -l | grep "memory-maintenance"