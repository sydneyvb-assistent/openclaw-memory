import json
import sys

config_file = sys.argv[1] if len(sys.argv) > 1 else "~/.openclaw/openclaw.json"

with open(config_file, 'r') as f:
    config = json.load(f)

# Set primary model to moonshot/kimi-k2.5
config['agents']['defaults']['model']['primary'] = 'moonshot/kimi-k2.5'
print("Set primary model to: moonshot/kimi-k2.5")

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("Config updated successfully")