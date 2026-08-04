# LiteLLM Proxy Multimodal Audit — 2026-08-04

**Audit by:** Kimi K3 / FI-008
**Reviewed by:** Hermes (acknowledgement + skill patch)
**Verdict:** hermes-asi **text-only at LiteLLM proxy layer**. All 3 modalities rejected.
**Smoking gun:** `litellm.NotFoundError: OpenAIException - No endpoints found that support image input. Received Model Group=hermes-asi. Available Model Group Fallbacks=None`

## Evidence Matrix (T0 OBS · 2026-08-04T14:0X UTC)

| # | Endpoint / Model | Image | Audio | Video | image_tokens |
|---|---|---|---|---|---|
| 1 | `http://127.0.0.1:4000/v1` `alias=hermes-asi` | ❌ NotFoundError | ❌ | ❌ | — |
| 2 | `http://127.0.0.1:4000/v1` `alias=asi-555-vision` | ✅ 200 | (untested) | (untested) | 1024 ✓ |
| 3 | `https://token-plan-sgp.xiaomimimo.com/v1` `model=mimo-v2.5` | ✅ 200 | (untested) | (untested) | 1024 ✓ |
| 4 | `http://127.0.0.1:4000/v1` `alias=hermes-asi` text-only path | ✅ pong | — | — | (n/a) |

Verbatim error string:
```
litellm.NotFoundError: NotFoundError: OpenAIException -
No endpoints found that support image input. Received Model Group=hermes-asi
Available Model Group Fallbacks=None
```

## Routing Map — What hermes-asi Actually Is

`/root/A-FORGE/litellm-config.yaml` lines 1–13:

```yaml
- model_name: hermes-asi
  litellm_params:
    model: openai/mimo-v2.5-pro        # Xiaomi deep-thinking, NOT multimodal
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
    api_key: os.environ/MIMO_API_KEY
- model_name: hermes-asi              # fallback
  litellm_params:
    model: openai/MiniMax-M3          # multimodal-capable
    api_base: https://api.minimax.io/v1
```

**Why it fails:** LiteLLM 1.90's image-input router inspects each model's capability metadata **before forwarding**. Neither `mimo-v2.5-pro` nor `MiniMax-M3` is tagged as supporting image input in the config — the proxy hard-rejects the group before any request leaves the box. `MiniMax-M3` actually is multimodal; the config doesn't declare it.

The dedicated multimodal lane (lines ~120–137):

```yaml
- model_name: asi-555-vision
  litellm_params:
    model: openai/mimo-v2.5           # ← the multimodal one, NOT -pro
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
- model_name: asi-555-vision
  litellm_params:
    model: openai/qwen3.7-plus        # Aliyun vision
```

## Claim vs Reality

| Surface | Claim | Reality |
|---|---|---|
| `Hermes-ASI model.supports_vision: true` | vision-capable | declared, but routing layer ignores it (OBS) |
| `Hermes-ASI vision.provider: minimax / minimax-m3` | vision → MiniMax | only used for `auxiliary.vision` calls, NOT main `hermes-asi` alias (OBS) |
| `Hermes-ASI image_input_mode: text` | passes image as text desc | this is the actual Hermes policy — multimodal input is dropped at the Hermes layer regardless (OBS) |
| MiMo docs claim `mimo-v2.5` supports image/audio/video | ✅ | ✅ verified via direct API; `image_tokens=1024` (OBS) |
| FED :4000 is multimodal gateway | ❌ it's LiteLLM proxy, not a multimodal gateway | OBS |

## Why the Docs Look Confusing

MiMo URLs (`mimo.mi.com/docs/.../image-understanding` etc.) describe `mimo-v2.5` — the base multimodal model. But `hermes-asi` is bound to `mimo-v2.5-pro` (deep-thinking variant). Federation has both, but the alias points at the wrong one for multimodal.

Also: docs use endpoint `https://api.xiaomimimo.com/v1`; Hermes uses `https://token-plan-sgp.xiaomimimo.com/v1`. Same vendor, different billing gateway. Both reach `mimo-v2.5` multimodal — Test 3 confirms.

## What's Actually Wired (T0 OBS)

| Capability | hermes-asi status |
|---|---|
| Text chat | ✅ Works |
| Image understanding | ❌ blocked; use `asi-555-vision` instead |
| Audio (ASR) understanding | ❌ blocked; no dedicated alias |
| Video understanding | ❌ blocked; no dedicated alias |
| Image generation (TTS-vision, etc.) | ⚠️ `mimo-v2.5-tts-voicedesign` configured but separate tool |
| Speech-to-text (whisper-1) | ✅ Hermes STT pipeline independent of chat |
| Text-to-speech (mimo TTS) | ✅ `tts.provider: mimo` configured |

**Audio understanding ≠ STT.** Whisper transcribes; understanding (semantic Q&A over audio) needs a multimodal LLM. No alias for audio-understanding today.

**Video understanding** has no alias at all — not even a `*-vision` lane. Direct `mimo-v2.5` supports it per docs, but the proxy doesn't expose it under any alias.

## Root Cause (DER)

Two config gaps in `/root/A-FORGE/litellm-config.yaml`:

1. `hermes-asi` routes to text-only backends — `mimo-v2.5-pro` and `MiniMax-M3` without capability flags. Should either point at `mimo-v2.5` multimodal or declare `supports_image_input: true` on the fallback.
2. No `*-audio` or `*-video` alias — federation has the capability, just no lane name.

## Fix Options (T1 reversible · no 888_HOLD needed)

| # | Fix | Diff size | Risk |
|---|---|---|---|
| A | Add a `hermes-asi-vision` alias pointing at `mimo-v2.5` (multimodal) | +8 lines | low — additive |
| B | Patch `hermes-asi` to include `mimo-v2.5` as a third fallback | +4 lines | low — chat still works |
| C | Add `asi-555-audio` + `asi-555-video` aliases (full multimodal surface) | +16 lines | low |
| D | Set `image_input_mode: auto` in `hermes_asi/config.yaml` so Hermes passes images natively | 1 line | medium — Hermes vision path untested live |

**Kimi recommended combo:** A + C, leave `image_input_mode` alone (Hermes' text mode is a deliberate governance choice — see F11 auditability).

## ⚠️ Dead Code Finding (post-audit, 2026-08-04T22:22+08)

**After the fix was applied (commit 6a98bb24), Kimi verified traffic flow:**

- All 169 LiteLLM POSTs in 30min came from 100.64.0.2 — same network namespace as LiteLLM itself
- No external agent traffic through LiteLLM at all
- Hermes config has `mimo-platform.api: https://api.xiaomimimo.com/v1` — direct provider URL, bypasses LiteLLM
- Config comment was correct all along: "LiteLLM serves as fed-health probe target + FED route metadata source"

**Conclusion:** The LiteLLM alias patch (Fix A) was **dead code** — harmless but no production value. Agents route direct to provider APIs. The fix options (A/B/C/D) were solving a routing layer that doesn't exist in production traffic.

**Correct action:** Document capability matrix in Hermes provider config (where agents actually route), not in LiteLLM aliases. Commit 6a98bb24 can be reverted or left (harmless).

**Lesson:** Always verify actual traffic flow through a routing layer before patching it. Check `token_bank.db` route metadata, FED health probes, or network namespace isolation before assuming a config layer is in the hot path.

## Open: Archival Provider Drift

`mulerouter / openrouter / tokenrouter` (~$109 stranded) are orphaned from `litellm-config.yaml` but still in `token_bank.db`:

- `mulerouter`: $49.93
- `tokenrouter`: $59.94
- `openrouter`: $0.50 BLIND (no credit balance, usage only)

Three legitimate paths:
1. Withdraw cash from active providers, drop the orphans
2. Re-add to `litellm-config.yaml` (revive)
3. Tombstone in DB with audit receipt (F11)

Not urgent, but real money.

## Capabilities Confirmed in MiMo Docs (separate session)

| Capability | Activation |
|---|---|
| Image understanding | Auto (OpenAI multimodal content parts) |
| Audio understanding | `input_audio` content type |
| Video understanding | `video_url` + `fps` + `media_resolution` params |
| Web Search tool | Plugin activated in MiMo Console; $5/1K overseas |
| Deep Thinking (CoT) | `extra_body={"thinking": {"type": "enabled"}}` (default ON); `reasoning_content` mandatory in multi-turn |
| Function calling | OpenAI-compatible `tools` array |
| Structured Output (JSON mode) | `response_format={"type": "json_object"}` |
| Streaming | `stream: true`; concatenate JSON client-side |

All MiMo capabilities exist. The federation just doesn't expose them all through aliases.
