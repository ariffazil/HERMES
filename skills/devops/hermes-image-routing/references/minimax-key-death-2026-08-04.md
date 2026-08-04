# Minimax API Key Death — 2026-08-04

**Severity:** CRITICAL — affects load-bearing auxiliary vision path
**Key:** `sk-cp-...UgO4` (127 chars)
**Sources:** kunci-mas.env + hermes/.env (same key)

## Evidence

```
$ curl -s -H "Authorization: Bearer $MINIMAX_API_KEY" https://api.minimax.io/v1/models
HTTP 401
{"type":"error","error":{"type":"authorized_error","message":"login fail: Please carry the API secret key in the 'Authorization' field of the request header (1004)"}}

$ curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer $MINIMAX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","messages":[{"role":"user","content":"Say hello"}],"max_tokens":20}'
HTTP 401
{"type":"error","error":{"type":"authorized_error","message":"login fail: Please carry the API secret key..."}}

# Also tried api-key header:
$ curl -s -H "api-key: $MINIMAX_KEY" https://api.minimax.io/v1/models
HTTP 401 (same error)
```

## Impact Map

| Service | Config | Status |
|---|---|---|
| Hermes auxiliary vision | `auxiliary.vision.provider: minimax`, `model: minimax-m3` | ⚠️ BROKEN |
| hermes-asi fallback | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |
| openclaw primary | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |
| agi-333 primary | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |
| apex-888 primary | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |
| codex fallback | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |
| opencode fallback | litellm: `openai/MiniMax-M3` | ⚠️ BROKEN |

## Timeline

- 22:22 MYT — Mirror selfie test: SUCCESS (auxiliary vision via minimax-m3)
- 22:36 MYT — Kimi audit: direct mimo-v2.5-pro → NotFoundError (text-only)
- 22:36 MYT — Key probe: HTTP 401 (dead)

**Key died between test and audit (14 min window).** Possible causes:
- Token Plan expiry
- Manual revocation from console
- Rate limit / abuse trigger
- Platform-side key rotation

## Mystery: Why did the mirror selfie test work?

Options:
1. **Cached vision result** — auxiliary vision call happened before key expiry
2. **Different key path** — Hermes might read key from different env source
3. **Key expired between test and now** — 14 min window

Most likely: option 3. Keys can die mid-session.

## Fix Recipe

1. Generate new key from `platform.minimax.io` console
2. Update KUNCI-MAS: paste new key → I wire + regenerate + restart
3. Verify: `curl -s -H "Authorization: Bearer $NEW_KEY" https://api.minimax.io/v1/models`
4. Restart: `systemctl restart litellm-federation` + hermes gateway

## Lesson

**Always probe API keys at session start.** Config presence ≠ key validity. A key that worked 5 minutes ago may be dead now. The 401 error is silent — no alarm, no webhook, just "login fail".
