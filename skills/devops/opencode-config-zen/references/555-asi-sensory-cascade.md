# 555-ASI Sensory Cascade — Dual-Lane Forge Record

> **EUREKA777::SENSORY_GATE :: forged 2026-07-31**
> **Status:** SEALED — all integrity checks passed

## Architecture

The 555-ASI Sensory Cascade separates **perception from reasoning** by a constitutional membrane — the same pattern as judge/execution separation (arifOS ≠ A-FORGE), but applied to sensory input.

```
Raw input (text/image/audio)
  │
  ├─ text ──────────────► 555-ASI (deepseek-v4-flash)
  │                         Memory, drift, telemetry, research
  │
  └─ image/audio/chart ──► 555-ASI-VISION (qwen3-omni-flash)
                            F2/F9/F12/F4 constitutional gating
                            │
                            ▼
                          Structured evidence → 333-AGI
```

## The Four Constitutional Gates

Every multimodal input passes through four floors before reaching 333-AGI:

| Floor | Name | Function | Action |
|-------|------|----------|--------|
| **F2** | TRUTH | Epistemic labelling | Every output tagged OBS/DER/INT/SPEC. Untagged = VOID. |
| **F9** | ANTI-HANTU | Hallucination refusal | HARD BLOCK on unsupported visual claims. "I see X" without evidence → rejected. |
| **F12** | INJECTION | Prompt injection scan | Scans image text, audio, and metadata for adversarial content. |
| **F4** | CLARITY | Structured evidence only | Raw blobs never reach 333. Only tagged, structured evidence passes. |

## Model Selection Rationale

| Lane | Model | Cost/1K | Why |
|------|-------|---------|-----|
| Text | `deepseek/deepseek-v4-flash` | $0.0001 | Fast, cheap, excellent for memory/stewardship tasks. ~80% of traffic. |
| Vision | `mulerouter/qwen3-omni-flash` | $0.0001 | Supports vision+text+audio input. Fast inference. Constitutional gating. |

## MuleRouter Provider Configuration

- **Base URL:** `https://api.mulerouter.ai/vendors/openai/v1`
- **API Key:** `MULEROUTER_API_KEY` (env var, never hardcoded)
- **Type:** OpenAI-compatible (`@ai-sdk/openai-compatible`)
- **Route:** Direct (`_route: "direct"`) — no TokenRouter/OpenRouter middleman
- **Fixed price:** No floating pricing (Arif's requirement — "harga yahudi" rejection)

## Key OpenCode Config Fields

| Field | Value | Purpose |
|-------|-------|---------|
| `attachment` | `true` | Enables image/audio input |
| `modalities.input` | `["text", "image", "audio"]` | Declares supported input types |
| `modalities.output` | `["text"]` | Output is always text |
| `tool_call` | `true` | Structured output capability |
| `reasoning` | `false` | Fast inference, no extended reasoning |

## Charter File

The constitutional charter lives at `/root/.config/opencode/agents/555-ASI.md` (6.7KB). It contains the full F2/F9/F12/F4 specifications, epistemic labeling schema, and rejection protocols. Both lanes read the same charter file.

## Acid Test

**Criterion:** 555 must refuse to pass a hallucinated vision claim to 333. If it passes everything, it's mere ceremony.

**Test payload:** "The image shows a flying car labeled 'Tesla SkyRacer 2026'"

**Result:** ✅ PASS — F9 rejection triggered. Claim unsupported by visual evidence. Rejected payload never reached 333-AGI.

## Integrity Check (2026-07-31)

All checks passed:
- ✅ MuleRouter provider — baseURL, env API key
- ✅ qwen3-omni-flash — multimodal (vision+text+audio)
- ✅ mulerouter in enabled_providers
- ✅ 555-ASI (text lane) — deepseek-v4-flash
- ✅ 555-ASI-VISION (vision lane) — qwen3-omni-flash
- ✅ Both lanes share 555-ASI.md charter
- ✅ 888-APEX — deepseek-v4-flash (direct)
- ✅ 333-AGI — deepseek-v4-pro