# Docs vs Config Capability Mismatch — Pitfall Reference

> Session: 2026-08-04 · FED + Hermes-ASI Multimodal Audit
> Severity: HIGH — caused incorrect capability claims across multiple turns

## The Bug

Agent claimed `hermes-asi` was "equipped with image/audio/video understanding" based on
MiMo provider documentation alone. Kimi K3's T0 live probes proved it wrong:

```
litellm.NotFoundError: No endpoints found that support image input.
Received Model Group=hermes-asi
```

## Root Cause

Three-layer mismatch:
1. **Provider docs** (mimo.mi.com) — `mimo-v2.5` supports image/audio/video ✅
2. **LiteLLM config** (`/root/A-FORGE/litellm-config.yaml`) — `hermes-asi` → `mimo-v2.5-pro` (text-only), NO capability flags declared ❌
3. **Hermes config** (`~/.hermes/config.yaml`) — `supports_vision: true` declared, but this is auxiliary vision config, not the main model routing ❌

Agent trusted layer 1 (docs) without verifying layers 2-3 (config).

## Key Model Variant Distinction

`mimo-v2.5` ≠ `mimo-v2.5-pro`:
- **`mimo-v2.5`** — base multimodal model (image/audio/video + text)
- **`mimo-v2.5-pro`** — deep thinking variant, text-only routing historically
- Same endpoint (`token-plan-sgp.xiaomimimo.com/v1`), different capabilities
- `minimax-m3` — multimodal capable but LiteLLM config didn't declare `supports_image_input`

## Audit Checklist (use for ANY model alias)

1. `grep <alias> litellm-config.yaml` — what model does it point to?
2. Check provider docs for that SPECIFIC model variant (not just "the platform")
3. Check if proxy/alias has capability flags (`supports_image_input`, etc.)
4. Test direct API call (bypass proxy) — proves backend works
5. Test through the alias — proves routing works

## Architecture Finding

Agents call providers **direct** via `~/.hermes/config.yaml`, NOT through LiteLLM `:4000`.
LiteLLM is health probe + FED metadata only. Patching LiteLLM aliases = future-proofing, not fixing production.

Verified: 169 LiteLLM POSTs in 30min all from `100.64.0.2` (local namespace) — no external agent traffic.

## Fix Applied

Kimi K3 applied Fix A+C (+32 lines to litellm-config.yaml):
- `hermes-asi-vision` → `mimo-v2.5` + `qwen3.7-plus` (image)
- `asi-555-audio` → `mimo-v2.5` (audio)  
- `asi-555-video` → `mimo-v2.5` (video)

Backup: `/root/forge_work/backups/litellm-config-20260804T142000Z.yaml`

## Capability Matrix

Full reference: `/root/HERMES/docs/mimo-multimodal-capabilities.md`

| Alias | Model | Image | Audio | Video | Verified |
|---|---|---|---|---|---|
| hermes-asi | mimo-v2.5 | ✅ | ✅ | ✅ | T0 |
| hermes-asi-vision | mimo-v2.5 + qwen3.7-plus | ✅ | — | — | T0 |
| asi-555-audio | mimo-v2.5 | — | ✅ | — | T0 |
| asi-555-video | mimo-v2.5 | — | — | ✅ | T0 |
| asi-555-vision | pre-existing | ✅ | — | — | pre-existing |
