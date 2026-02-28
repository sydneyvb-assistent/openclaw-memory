import json
import sys

config_file = sys.argv[1] if len(sys.argv) > 1 else "~/.openclaw/openclaw.json"

with open(config_file, 'r') as f:
    config = json.load(f)

# Add gpt-5.1-codex to openai models if not present
openai_models = config['models']['providers']['openai']['models']
model_exists = any(m['id'] == 'gpt-5.1-codex' for m in openai_models)

if not model_exists:
    new_model = {
        "id": "gpt-5.1-codex",
        "name": "GPT-5.1 Codex",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    }
    openai_models.append(new_model)
    print(f"Added gpt-5.1-codex to openai models")
else:
    print(f"gpt-5.1-codex already exists in models")

# Fix the alias entry if it uses wrong provider format
aliases = config.get('agents', {}).get('defaults', {}).get('models', {})
if 'openai/gpt-5.1-codex' in aliases:
    # Keep the alias but ensure model ID format is correct
    print(f"Found alias for openai/gpt-5.1-codex")

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("Config updated successfully")