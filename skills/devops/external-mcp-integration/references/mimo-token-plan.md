# MiMo Token Plan — Provider Config Reference

> Xiaomi MiMo offers two API surfaces: Token Plan (subscription) and Platform API (pay-per-usage).

## Endpoints & Keys

| Provider | Base URL | Env Var | Key Prefix | Status (2026-07-19) |
|----------|----------|---------|------------|---------------------|
| **Token Plan SGP** | `https://token-plan-sgp.xiaomimimo.com/v1` | `MIMO_API_KEY` | `tp-` | ⚠️ Quota exhausted |
| **Platform API** | `https://api.xiaomimimo.com/v1` | `MIMO_PLATFORM_API_KEY` | `sk-` | ✅ Active |

Both offer the same model set: `mimo-v2.5-pro`, `mimo-v2.5`, `mimo-v2.5-pro-ultraspeed`, `mimo-v2.5-asr`, `mimo-v2.5-tts`, etc.

## Hermes Provider Config

### Token Plan (subscription)
```yaml
providers:
  xiaomi-mimo:
    name: MiMo Token Plan SGP
    api: https://token-plan-sgp.xiaomimimo.com/v1
    key_env: MIMO_API_KEY
    transport: openai_chat
    models:
      - id: mimo-v2.5-pro
        name: MiMo V2.5 Pro (Token Plan)
      - id: mimo-v2.5
        name: MiMo V2.5 multimodal (Token Plan)
```

### Platform API (pay-per-usage)
```yaml
providers:
  mimo-platform:
    name: MiMo Platform (pay-per-usage)
    api: https://api.xiaomimimo.com/v1
    key_env: MIMO_PLATFORM_API_KEY
    transport: openai_chat
    models:
      - id: mimo-v2.5-pro-ultraspeed
        name: MiMo V2.5 Pro UltraSpeed
      - id: mimo-v2.5-pro
        name: MiMo V2.5 Pro
      - id: mimo-v2.5
        name: MiMo V2.5 multimodal
```

**Fix miswired key_env:**
```bash
hermes config set providers.xiaomi-mimo.key_env MIMO_API_KEY
```

## OpenClaw Provider Config

Location: `/root/.openclaw/openclaw.json` → `models.providers`

### Token Plan
```json
"mimo-token-plan": {
  "baseUrl": "https://token-plan-sgp.xiaomimimo.com/v1",
  "apiKey": "${MIMO_API_KEY}",
  "api": "openai-completions",
  "models": [
    {"id": "mimo-v2.5-pro", "name": "MiMo V2.5 Pro (Token Plan)", "reasoning": true, "input": ["text"], "contextWindow": 1048576, "maxTokens": 131072},
    {"id": "mimo-v2.5", "name": "MiMo V2.5 multimodal (Token Plan)", "reasoning": true, "input": ["text", "image"], "contextWindow": 1048576, "maxTokens": 131072}
  ]
}
```

### Platform API
```json
"xiaomi-coding": {
  "baseUrl": "https://api.xiaomimimo.com/v1",
  "apiKey": "sk-suk...x9ou",
  "api": "openai-completions",
  "models": [
    {"id": "mimo-v2.5-pro", "name": "MiMo V2.5 Pro (DEFAULT, 1M ctx)", "reasoning": true, "input": ["text"], "contextWindow": 1048576, "maxTokens": 131072},
    {"id": "mimo-v2.5", "name": "MiMo V2.5 (multimodal)", "reasoning": true, "input": ["text", "image"], "contextWindow": 1048576, "maxTokens": 131072},
    {"id": "mimo-v2.5-pro-ultraspeed", "name": "MiMo V2.5 Pro UltraSpeed (fallback)", "reasoning": true, "input": ["text"], "contextWindow": 1048576, "maxTokens": 131072}
  ]
}
```

**Edit pattern** — add a provider via Python one-liner:
```bash
cat /root/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
d['models']['providers']['mimo-token-plan'] = { ... }
json.dump(d, open('/root/.openclaw/openclaw.json','w'), indent=2)
"
systemctl restart openclaw-gateway.service
```

## Key Verification

Always live-test before declaring wired:
```bash
source /root/.secrets/vault.env
curl -s --max-time 10 "$BASE_URL/models" \
  -H "Authorization: Bearer $API_KEY"
```

And a full chat test:
```bash
curl -s --max-time 15 "$BASE_URL/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"model":"mimo-v2.5-pro","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'
```

Common errors:
- `"quota exhausted"` — Token Plan subscription depleted. Switch to Platform API or wait for renewal.
- `"invalid_api_key"` — Key format or provider mismatch.
- HTTP 401 — Wrong key or base URL.

## Quota Exhaustion Recovery Pattern (2026-07-19)

When MiMo Token Plan hits quota on one machine, it's dead everywhere sharing that key:

1. **Check if other VPS has different key:**
   ```bash
   ssh root@<REMOTE_IP> 'grep "MIMO_API_KEY\|tp-sle" /root/.secrets/vault.env'
   ```
2. **If same key:** Quota is shared — both machines exhausted. No copy possible.
3. **If different key:** Wire the other VPS's key to this machine.
4. **Rotate provider instead:** When Token Plan is dead, switch to MiniMax (separate key, separate quota) or DeepSeek direct API (no quota limit). Pattern:
   ```python
   # OpenClaw model rotation
   model['primary'] = 'minimax/MiniMax-M2.7'
   model['fallbacks'] = ['deepseek/deepseek-v4-flash', 'deepseek/deepseek-v4-pro']
   ```
5. **Check what working VPS uses:** If WawaBot (A-FLOW) is alive, check its config:
   ```bash
   ssh root@<REMOTE_IP> 'python3 -c "import json;d=json.load(open(\"/root/.openclaw/openclaw.json\"));print(d[\"agents\"][\"defaults\"][\"model\"][\"primary\"])"'
   ```
   Mirror the working config.

**Root cause:** Two VPSes with same Token Plan key share quota. One exhausted = both exhausted. Solution: different provider with independent quota.
