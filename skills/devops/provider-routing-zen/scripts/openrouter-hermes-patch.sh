#!/bin/bash
# OpenRouter -> Hermes integration patch
# Execute: bash /tmp/openrouter-hermes-patch.sh
# Reversible: cp /root/.hermes/config.yaml /root/.hermes/config.yaml.bak.pre-openrouter
#
# Adds OpenRouter auto-beta as Tier 2 fallback (after DeepSeek direct)
# Adds OpenRouter free as survival tier (before local/ollama)
# Adds OpenRouter MCP server for live model discovery
#
# NOTE: OpenRouter-specific per-request params (ZDR, CQT, model allowlist)
# must be handled via OpenRouter Management API guardrails, NOT here.
# Script: /root/AAA/scripts/provision-openrouter-guardrail.py

set -e
CONFIG=/root/.hermes/config.yaml
cp "$CONFIG" "$CONFIG.bak.pre-openrouter"

python3 -c "
import yaml

with open('$CONFIG') as f:
    cfg = yaml.safe_load(f)

cfg['fallback_providers'] = [
    {'model': 'deepseek/deepseek-v4-pro', 'provider': 'tokenrouter', 'timeout': 20},
    {'model': 'openrouter/auto-beta', 'provider': 'openrouter', 'timeout': 30},
    {'model': 'llama-3.1-8b-instant', 'provider': 'groq', 'timeout': 20},
    {'model': 'aisingapore/Qwen-SEA-LION-v4-32B-IT', 'provider': 'sea-lion', 'timeout': 20},
    {'model': 'gemini-2.5-flash', 'provider': 'gemini', 'timeout': 20},
    {'model': 'gemma-4-31b', 'provider': 'cerebras', 'timeout': 20},
    {'model': 'MiniMax-M3', 'provider': 'tokenrouter', 'timeout': 20},
    {'model': 'z-ai/glm-5.2', 'provider': 'tokenrouter', 'timeout': 20},
    {'model': 'openrouter/free', 'provider': 'openrouter', 'timeout': 60},
    {'model': 'qwen2.5-coder:3b', 'provider': 'ollama', 'timeout': 20},
]

cfg.setdefault('mcp_servers', {})
cfg['mcp_servers']['openrouter'] = {
    'description': 'OpenRouter MCP - model discovery, credit monitoring, benchmarks, test messaging',
    'url': 'https://mcp.openrouter.ai/mcp',
    'transport': 'streamable-http',
    'auth': 'oauth',
    'timeout': 30,
}

with open('$CONFIG', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print('PATCH APPLIED')
"

python3 -c "import yaml; yaml.safe_load(open('$CONFIG')); print('YAML VALID')"

echo ""
echo "=== New fallback chain ==="
python3 -c "
import yaml
cfg = yaml.safe_load(open('/root/.hermes/config.yaml'))
for i, fb in enumerate(cfg.get('fallback_providers', [])):
    print(f'  Tier {i+1}: {fb[\"model\"]}')
print()
print(f'MCP servers: {len(cfg.get(\"mcp_servers\", {}))}')
"
echo ""
echo "Revert: cp $CONFIG.bak.pre-openrouter $CONFIG"
echo "MCP OAuth: connect once to trigger browser flow, approve with management key"
