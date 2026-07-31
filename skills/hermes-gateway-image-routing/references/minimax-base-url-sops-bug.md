# MINIMAX_BASE_URL Sops-Encrypted Bug (2026-07-30)

## Root Cause

`MINIMAX_BASE_URL` in `kunci-mas.env` was migrated from `arifOS/.env` via sops encryption
and stored as ciphertext:

```
export MINIMAX_BASE_URL=ENC[AES256_GCM,data:qeRnWa+E0BVNQgiVWXzYocHl/aeYYA==,...]
```

This propagated through the entire Hermes provider routing chain and crashed `urlparse`.

## Symptoms

Any code path that resolved the `minimax` provider for vision/auxiliary tasks crashed with:
```
ValueError: Invalid IPv6 URL
```
in `urlparse` at `utils.py:486`.

The error appeared in:
- `vision_analyze_tool` (all calls failed)
- `resolve_vision_provider_client('minimax', ...)`  
- `resolve_provider_client` → `base_url_host_matches` → `base_url_hostname`

## Why it was hard to spot

1. **Error message was misleading**: `"Invalid IPv6 URL"` — looked like a bad IPv6 config,
   not an encrypted env var
2. **Provider routing code was opaque**: The crash happened deep in `_wrap_if_needed` →
   `_needs_codex_wrap`, far from the env var read site
3. **Duplicated root-cause chasing**: The team chased:
   - Path B model swap (wrong — it was already reverted)
   - `model.supports_vision: true` (wrong — already false)
   - OpenRouter 413 cascade (wrong — that was a downstream symptom)
   - A2A delegation to OpenClaw (wrong — architectural solution to wrong problem)
4. **sops encrypted value looked like a real value**: `ENC[AES256_GCM,data:...]` is
   valid sops syntax — easy to miss as "just another encrypted key"

## Debug trace

```
resolve_vision_provider_client("minimax", "minimax-m3", async_mode=True)
  ↓
_get_cached_client("minimax", "minimax-m3", ...)
  ↓
resolve_provider_client("minimax", "minimax-m3", ...)
  ↓
resolve_api_key_provider_credentials("minimax")
  → creds["base_url"] = "ENC[AES256_GCM,data:...]"  ← from MINIMAX_BASE_URL env var
  ↓
raw_base_url = creds["base_url"] or pconfig.inference_base_url
  = "ENC[AES256_GCM,data:...]"  ← encrypted value wins (non-empty string!)
  ↓
base_url = _to_openai_base_url(raw_base_url)
  → no /anthropic suffix → no transformation → still ciphertext
  ↓
explicit_base_url overrides base_url ✓ (client created with correct URL)
  ↓
_wrap_if_needed(client, final_model, raw_base_url, api_key)  ← line 5007
  → raw_base_url = "ENC[AES256_GCM,data:...]"  ← NOT the overridden base_url!
  ↓
_needs_codex_wrap(client_obj, raw_base_url, model)
  → base_url_hostname(raw_base_url)
  → urlparse("//ENC[AES256_GCM,data:...]")
  → ValueError: Invalid IPv6 URL  🚨
```

Note: The bug was at `resolve_provider_client` line 5007 — `_wrap_if_needed` receives
`raw_base_url` (the original, unmodified value from creds) even though `base_url` was
correctly overridden by `explicit_base_url` at line 4942. This is a framework code
quirk — the `raw_base_url` variable is used for wrapping decisions while `base_url` is
used for client construction.

## Fix

Two changes fixed it:

1. **Replace encrypted value in vault**: Both `kunci-mas.env` and `kunci-mas.flat.env`
   had the encrypted value replaced with the actual URL:
   ```bash
   MINIMAX_BASE_URL="https://api.minimax.io"
   ```

2. **Set auxiliary.vision.base_url as explicit override**: Bypasses the env var path:
   ```bash
   hermes config set auxiliary.vision.base_url "https://api.minimax.io/v1"
   ```

## Verification

After the fix:
```python
vision_analyze_tool(image_url=path, user_prompt=prompt)
# → Success: True
# → Analysis: "SCENE: A food court viewed from above..."
```

## Prevention

- URL-type env vars (`*_BASE_URL`, `*_HOST`, `*_ENDPOINT`) must NEVER contain
  sops-encrypted ciphertext
- Add vault-verify check: scan for `ENC[AES256_GCM,` in URL-typed values
- When debugging `urlparse` errors, check all env vars that feed into the
  provider resolution chain first
