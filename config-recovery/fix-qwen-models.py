import json
import sys

config_file = sys.argv[1] if len(sys.argv) > 1 else "~/.openclaw/openclaw.json"

with open(config_file, 'r') as f:
    config = json.load(f)

# Add missing Qwen models to groq if not present
groq_models = config['models']['providers']['groq']['models']
existing_ids = {m['id'] for m in groq_models}

qwen_models = [
    {
        "id": "qwen3-32b",
        "name": "Qwen3 32B",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    },
    {
        "id": "qwen-2.5-coder-32b",
        "name": "Qwen2.5 Coder 32B",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    },
    {
        "id": "qwen-2.5-32b",
        "name": "Qwen2.5 32B",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    }
]

for model in qwen_models:
    if model['id'] not in existing_ids:
        groq_models.append(model)
        print(f"Added {model['id']} to groq models")
    else:
        print(f"{model['id']} already exists")

# Also update default model to groq/qwen3-32b if needed
if config['agents']['defaults']['model']['primary'] == 'groq/qwen/qwen3-32b':
    config['agents']['defaults']['model']['primary'] = 'groq/qwen3-32b'
    print("Fixed primary model reference")

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("Config updated successfully")