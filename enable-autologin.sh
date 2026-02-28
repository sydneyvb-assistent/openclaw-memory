#!/bin/bash
# One-time auto-login setup script
# Run this once, then delete it

set -e

# Enable auto-login for sydneyassistent
sudo defaults write /Library/Preferences/com.apple.loginwindow autoLoginUser sydneyassistent
sudo defaults write /Library/Preferences/com.apple.loginwindow autoLoginUserUID $(id -u sydneyassistent)

echo "Auto-login enabled for sydneyassistent"
echo "Reboot to test: sudo shutdown -r now"

# Self-destruct
rm -- "$0"