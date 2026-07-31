# OPENAI_BASE_URL Poisoning — Discovery 2026-07-30

## Context

During SADO group integration, images sent to the group produced a 413
cascade failure through every fallback provider. Initial diagnosis
pointed to provider mismatch, but the actual root cause was subtler.

## Symptoms

Gateway log entries:
```
ERROR tools.vision_tools: Error analyzing image: Error code: 404 -
models/deepseek-v4-flash is not found for API version v1main
...
Auxiliary: marking openrouter unhealthy for 600s (payment / credit error)
...
413: Request too large for model llama-3.1-8b-instant (TPM limit)
```

The vision tool was calling deepseek-v4-flash on the wrong API endpoint
— Aliyun Token Plan instead of the configured auxiliary vision provider.

## Root Cause

The env var `OPENAI_BASE_URL` was set to Aliyun Token Plan:
```
OPENAI_BASE_URL=https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
```

The Hermes `auxiliary_client.py` (and the underlying OpenAI SDK client)
automatically reads `OPENAI_BASE_URL` from the environment and uses it
to override the base URL for ALL OpenAI-compatible API calls. This
includes:
- Primary chat model calls
- Auxiliary vision enrichment calls
- Tool execution calls

When `OPENAI_BASE_URL` points to a different API (Aliyun), every
auxiliary call goes to the wrong endpoint. The vision tool tried
`deepseek-v4-flash` on Aliyun → 404 (model doesn't exist there).

## Fix

```bash
# In the gateway startup script /usr/local/bin/hermes-gateway-secure.sh
# Add BEFORE the exec line:
unset OPENAI_BASE_URL
```

This prevents the env var from reaching the Hermes process while keeping
it available for other scripts (godel_enforcement.py, tovana_compiler.py)
that source kunci-mas.env directly.

## Source of the Var

```
/root/.secrets/kunci-mas.env:   export OPENAI_BASE_URL=...
/root/.secrets/vault.flat.env:  OPENAI_BASE_URL=...
/root/.secrets/kunci-mas.flat.env: OPENAI_BASE_URL=...
```

Also in the systemd EnvironmentFile:
```
/etc/systemd/system/hermes-asi-gateway.service: EnvironmentFile=/root/.secrets/vault.flat.env
```

## Why This Is Hard to Diagnose

1. The error message says "models/deepseek-v4-flash is not found" —
   sounds like a model name issue, not a routing issue
2. The gateway already warns: `OPENAI_BASE_URL is set... Auxiliary
   clients may route to the wrong endpoint` — but this is easily missed
   among other log noise
3. Only the auxiliary vision call breaks — primary chat works fine
   because it uses the configured provider URL, not the env var
4. The symptom (413 cascade) is identical to provider mismatch or
   OpenRouter payment errors, leading to misdiagnosis

## Detection

```bash
# Quick check
echo "OPENAI_BASE_URL=${OPENAI_BASE_URL:-not set}"
grep 'OPENAI_BASE_URL' /root/.secrets/kunci-mas.env

# In gateway logs
journalctl -u hermes-asi-gateway --since "1 hour ago" | grep -i "OPENAI_BASE_URL\|auxiliary clients may route"
```

## Prevention

Any new env var that starts with `OPENAI_` or ends with `_BASE_URL` in
kunci-mas.env should be checked: does the Hermes OpenAI SDK client
automatically pick it up? If yes, it must be unset in the gateway
startup script.

Future-proofing: when adding a new provider to kunci-mas.env, check
whether any of its env vars match patterns that the OpenAI SDK
auto-detects (`OPENAI_*`, `*_BASE_URL`, `*_API_KEY` with "openai" in the
name).
