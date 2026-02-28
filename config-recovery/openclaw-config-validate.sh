#!/bin/bash
# openclaw-config-validate.sh - Validate OpenClaw config before applying
# Returns 0 if valid, 1 if invalid

CONFIG_FILE="${1:-${HOME}/.openclaw/openclaw.json}"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Config file not found: $CONFIG_FILE" >&2
    exit 1
fi

# Check JSON validity
if ! python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "ERROR: Invalid JSON in $CONFIG_FILE" >&2
    exit 1
fi

# Check required top-level keys
REQUIRED_KEYS=("models" "agents" "channels" "gateway")
for key in "${REQUIRED_KEYS[@]}"; do
    if ! python3 -c "import json; d=json.load(open('$CONFIG_FILE')); exit(0 if '$key' in d else 1)" 2>/dev/null; then
        echo "WARNING: Missing required key: $key" >&2
    fi
done

# Validate model references exist in allowlist
python3 << PYEOF
import json
import sys

try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
    
    # Collect all allowed model IDs
    allowed_models = set()
    for provider, pdata in config.get('models', {}).get('providers', {}).items():
        for model in pdata.get('models', []):
            allowed_models.add(f"{provider}/{model['id']}")
    
    # Check default model references
    defaults = config.get('agents', {}).get('defaults', {}).get('model', {})
    primary = defaults.get('primary')
    fallbacks = defaults.get('fallbacks', [])
    
    errors = []
    if primary and primary not in allowed_models:
        errors.append(f"Primary model '{primary}' not in allowlist")
    
    for fb in fallbacks:
        if fb not in allowed_models:
            errors.append(f"Fallback model '{fb}' not in allowlist")
    
    if errors:
        print("WARNING: Model validation issues:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    
    sys.exit(0)
except Exception as e:
    print(f"ERROR during validation: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo "Config validation passed: $CONFIG_FILE"
    exit 0
else
    echo "Config validation FAILED" >&2
    exit 1
fi