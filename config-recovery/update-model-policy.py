import json
import sys

config_file = '/Users/sydneyassistent/.openclaw/openclaw.json'

with open(config_file, 'r') as f:
    config = json.load(f)

# Update model configuration with new policy
# TRIVIAL tier: gpt-5-nano (primary), llama-3.1-8b-instant, claude-haiku-4-5
# NON-TRIVIAL (default): kimi-k2.5 (primary), claude-sonnet-4-6, gpt-5.2, llama-3.3-70b-versatile
# HEAVY: kimi-k2-thinking (primary), claude-opus-4-6, gpt-5.2

# Update default model
config['agents']['defaults']['model']['primary'] = 'moonshot/kimi-k2.5'

# Update fallbacks in priority order
config['agents']['defaults']['model']['fallbacks'] = [
    # Same tier (NON-TRIVIAL)
    'anthropic/claude-sonnet-4-6',
    'openai/gpt-5.2',
    'groq/llama-3.3-70b-versatile',
    # TRIVIAL tier (only for trivial tasks)
    'openai/gpt-5-nano',
    'groq/llama-3.1-8b-instant',
    'anthropic/claude-haiku-4-5',
    # HEAVY tier
    'moonshot/kimi-k2-thinking',
    'anthropic/claude-opus-4-6'
]

# Ensure all models exist in providers
# Check groq models
groq_models = config['models']['providers']['groq']['models']
groq_ids = [m['id'] for m in groq_models]

if 'llama-3.1-8b-instant' not in groq_ids:
    groq_models.append({
        "id": "llama-3.1-8b-instant",
        "name": "Llama 3.1 8B Instant",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    })

if 'llama-3.3-70b-versatile' not in groq_ids:
    groq_models.append({
        "id": "llama-3.3-70b-versatile",
        "name": "Llama 3.3 70B Versatile",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    })

# Check openai models
openai_models = config['models']['providers']['openai']['models']
openai_ids = [m['id'] for m in openai_models]

if 'gpt-5-nano' not in openai_ids:
    openai_models.append({
        "id": "gpt-5-nano",
        "name": "GPT-5 Nano",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    })

if 'gpt-5-mini' not in openai_ids:
    openai_models.append({
        "id": "gpt-5-mini",
        "name": "GPT-5 Mini",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 128000,
        "maxTokens": 8192
    })

if 'gpt-5.2' not in openai_ids:
    openai_models.append({
        "id": "gpt-5.2",
        "name": "GPT-5.2",
        "reasoning": True,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 200000,
        "maxTokens": 16384
    })

# Check anthropic models
anthropic_models = config['models']['providers']['anthropic']['models']
anthropic_ids = [m['id'] for m in anthropic_models]

if 'claude-haiku-4-5' not in anthropic_ids:
    anthropic_models.append({
        "id": "claude-haiku-4-5",
        "name": "Claude Haiku 4.5",
        "reasoning": False,
        "input": ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 200000,
        "maxTokens": 8192
    })

if 'claude-sonnet-4-6' not in anthropic_ids:
    anthropic_models.append({
        "id": "claude-sonnet-4-6",
        "name": "Claude Sonnet 4.6",
        "reasoning": False,
        "input": ["text", "image"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": 200000,
        "maxTokens": 16384
    })

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("Model configuration updated successfully")
print(f"Primary: {config['agents']['defaults']['model']['primary']}")
print(f"Fallbacks: {len(config['agents']['defaults']['model']['fallbacks'])} models")

# Update aliases
aliases = config['agents']['defaults'].get('models', {})
aliases['moonshot/kimi-k2.5'] = {"alias": "Kimi"}
aliases['openai/gpt-5-nano'] = {"alias": "GPT-Nano"}
aliases['openai/gpt-5-mini'] = {"alias": "GPT-Mini"}
aliases['openai/gpt-5.2'] = {"alias": "GPT-5.2"}
aliases['groq/llama-3.1-8b-instant'] = {"alias": "Groq-8B"}
aliases['groq/llama-3.3-70b-versatile'] = {"alias": "Groq-70B"}
aliases['anthropic/claude-haiku-4-5'] = {"alias": "Claude-Haiku"}
aliases['anthropic/claude-sonnet-4-6'] = {"alias": "Claude-Sonnet"}
aliases['anthropic/claude-opus-4-6'] = {"alias": "Claude-Opus"}
aliases['moonshot/kimi-k2-thinking'] = {"alias": "Kimi-Thinking"}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("Aliases updated")