# OpenClaw LLM Provider Diagnosis — 2026-07-11

## Session context

Arif reported "LLM request failed" on OpenClaw's @ASI_arifos_bot Telegram gateway. Every inbound Telegram message was failing silently. Three additional issues found during doctor: MCP servers failing, brave search unavailable, version mismatch.

## Root cause chain

1. **Primary provider** `bailian-token-plan/deepseek-v4-pro` had `"api": "anthropic-messages"` in config
2. **Endpoint** `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` is OpenAI-compatible (NOT Anthropic)
3. Every request → HTTP 404 (Anthropic Messages path not found on OpenAI endpoint)
4. Fallback chain (`xiaomi-coding/mimo-v2.5-pro`, `bailian-token-plan/glm-5.2`, `minimax/MiniMax-M3`) did NOT trigger because 404 was treated as hard transport error
5. Secondary issue: Bailian TokenPlan quota was also exhausted (429), but this was masked by the format error

## Fix applied

```python
# Changed in /root/.openclaw/openclaw.json
d['models']['providers']['bailian-token-plan']['api'] = 'openai-completions'  # was 'anthropic-messages'
```

Then: `systemctl restart openclaw-gateway`

## Post-fix behavior

- Primary (`bailian-token-plan/deepseek-v4-pro`): correctly returned 429 (quota exhausted)
- Fallback 1 (`xiaomi-coding/mimo-v2.5-pro`): **worked** (HTTP 200, response received)
- Gateway operational with MiMo V2.5 Pro as effective model

## Key verification commands

```bash
# Check what provider/model the gateway is using
journalctl -u openclaw-gateway --since "5 min ago" | grep "embedded run agent"

# Test a specific provider endpoint directly
curl -s -w "\nHTTP:%{http_code}" -X POST "<baseUrl>/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <key>" \
  -d '{"model":"<model-id>","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'

# Check active config
cat /root/.openclaw/openclaw.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Primary:', d['agents']['defaults']['model']['primary'])
print('Fallbacks:', d['agents']['defaults']['model']['fallbacks'])
providers = d['models']['providers']
for name, p in providers.items():
    print(f'  {name}: api={p.get(\"api\")}, baseUrl={p.get(\"baseUrl\",\"?\")}')
"
```

## Bailian TokenPlan provider details

| Field | Value |
|---|---|
| Provider slug | `bailian-token-plan` |
| Base URL | `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| Correct API format | `openai-completions` |
| API key env var | `QWEN_API_KEY` (in vault.env) |
| Available models | qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.6-flash, deepseek-v4-pro, deepseek-v4-flash, deepseek-v3.2, kimi-k2.7-code, kimi-k2.6, kimi-k2.5, glm-5.2, glm-5.1, glm-5, MiniMax-M2.5 |

## Telegram bot sharing

Both Hermes and OpenClaw use the same @ASI_arifos_bot token (`8149595687:***`). This is confirmed OK — they handle different message types and don't conflict. Hermes handles cognitive/DM tasks, OpenClaw handles gateway/agent tasks.

## Additional fixes (same session)

### 1. MCP servers: `sh -lc` fails with bash syntax in env files

**Symptom:** MCP servers `postgres` and `brave-search` both failed with `McpError: MCP error -32000: Connection closed` on every gateway startup.

**Root cause:** MCP server commands used `"command": "sh"` with `["-lc", "set -a; . /root/.env; ..."]`. But `/root/.env` contains `export -f` (bash function exports) that POSIX `sh` (dash) cannot parse. Subprocess crashes immediately.

**Diagnostic:**
```bash
sh -lc 'set -a; . /root/.env; set +a; echo OK' 2>&1
# → "sh: 21: export: Illegal option -f"
bash -lc 'set -a; . /root/.env; set +a; echo OK'
# → OK
```

**Fix:** Change `"command": "sh"` → `"command": "bash"` for all MCP servers sourcing `/root/.env`.

### 2. MCP postgres: Docker hostname vs localhost

**Root cause:** `/root/.env` had `POSTGRES_URL=...@postgres:5432/vault999` — `postgres` is Docker container name (internal DNS). MCP servers run on host network.

**Fix:** `postgres:5432` → `127.0.0.1:5432` in `/root/.env`.

### 3. Postgres password mismatch

**Root cause:** `/root/.env` had `POSTGRES_PASSWORD=ArifPostgres2026!` while vault.env had `ArifPostgresVault2026!`. The POSTGRES_URL in `/root/.env` used literal `***` (Docker placeholder).

**Fix:** Updated POSTGRES_URL in `/root/.env` with actual password `ArifPostgres2026!`.

### 4. Version mismatch causing plugin skips

**Symptom:** 6 plugins skipped: `plugin requires plugin API >=2026.6.11, but this host is 2026.6.1`.

**Root cause:** Gateway service runs from `/usr/lib/node_modules/openclaw/` (2026.6.1). npm global at `/root/.npm-global/` had 2026.6.11. Plugins installed to npm global but gateway used system-level.

**Fix:**
```bash
npm install -g openclaw@2026.6.11 --prefix /usr
# Verify: node -e "console.log(require('/usr/lib/node_modules/openclaw/package.json').version)"
```

**Pitfall:** `npm install -g` without `--prefix /usr` goes to npm global, NOT system-level. Gateway uses system-level.

### 5. Brave: native plugin vs MCP server

Two brave integrations: native plugin (`@openclaw/brave-plugin`) and MCP server (`mcp-server-brave-search`). Both were broken for different reasons. Native plugin preferred; MCP server is backup.

## Final state

- 7 plugins loaded: acpx, art-governor, brave, browser, memory-core, ollama, telegram
- 0 MCP failures
- 0 LLM errors
- Fallback chain working: bailian-token-plan (429) → xiaomi-coding/mimo-v2.5-pro (200)
