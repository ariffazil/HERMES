# Provider Key Health — Direct Probe Protocol

**Source session:** 2026-08-04 FED + Hermes-ASI Multimodal Audit
**Lesson:** "Probe the substrate, not the proxy."

## The Pattern

When symptoms look like config/routing issues, check API keys FIRST — not config.

Test provider endpoints directly (curl to api.provider.com) instead of only through the proxy (LiteLLM :4000). This catches key expiry, auth failures, and provider-side issues that the proxy layer masks as routing errors.

## Diagnostic Sequence

1. Test provider API directly:
```bash
curl -s -H "Authorization: Bearer $KEY" \
  https://api.provider.com/v1/chat/completions \
  -d '{"model":"X","messages":[{"role":"user","content":"test"}],"max_tokens":10}'
```
2. If 401/403 → key expired or invalid. Rotate key. Do NOT touch config.
3. If 200 → key works. Then check proxy layer (LiteLLM, routing, capability flags).
4. Check quota/balance: some providers have quota endpoints (e.g., MiniMax: `mmx quota`).

## Common Misdiagnosis (Key Expiry Masquerading as Config)

| Symptom | Actual Cause |
|---|---|
| `NotFoundError: no endpoints support image input` | 401 from provider surfaced as routing failure |
| `image returned but no img_tokens` | Partial data from expired key |
| `rotation hits non-multimodal entries` | Routing hit a dead endpoint (key expired) |
| `response_format not supported` | Key expiry, not model capability |

## Key Locations (KUNCI-MAS Single-Source-of-Truth)

| File | Role |
|---|---|
| `/root/.secrets/kunci-mas.env` | Canonical SOT |
| `/root/.hermes/.env` | Hermes main |
| `/root/.hermes/profiles/<name>/.env` | Per-profile |
| litellm-config.yaml | Uses `os.environ/KEY_NAME` (auto-picks from env) |

## Provider-Specific Notes

### MiniMax
- Key prefix: `sk-cp-` = Token Plan subscription key
- No standard balance API endpoint
- Check quota: `mmx quota` CLI (installed at `/root/.npm-global/bin/mmx`)
- Models available: MiniMax-M3, M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2
- Auth header: `Authorization: Bearer <key>` (NOT api-key header)
- 8 models in Token Plan, 5h rolling + weekly quota windows

### MiMo (Xiaomi)
- Endpoint: `https://token-plan-sgp.xiaomimimo.com/v1` (Token Plan) or `https://api.xiaomimimo.com/v1` (PAYG)
- Key env: `MIMO_API_KEY`
- Models: `mimo-v2.5` (multimodal), `mimo-v2.5-pro` (text-only, deep-thinking)

### DeepSeek
- Endpoint: `https://api.deepseek.com/v1`
- Key env: `DEEPSEEK_API_KEY`
- Track A provider (probed via api_probe)

## Session Receipt (2026-08-04)

MiniMax key expired between 22:22 (mirror selfie test worked via auxiliary vision) and 22:36 (401 detected). Root cause of "intermittent multimodal failures" was key expiry, not LiteLLM capability flags. Fix: rotate key, update 5 locations (KUNCI-MAS + 4 Hermes profiles), restart litellm-federation.
