# Hermes Live Fallback Chain — 2026-07-29

**Source:** `/root/.hermes/config.yaml`
**Probed:** 2026-07-29 session after Arif approved Flash primary swap + auto-beta bridge + sovereignty paradox analysis.

## Decision History (this session)

1. **Arif rejected OpenRouter as primary** — Sovereignty Paradox: constraining auto-beta to 1-2 model families nullifies its benefit while keeping its latency tax. OpenRouter stays at the edge as intelligent failover, not primary.
2. **Depth over speed** — auto-beta inserted at Position 2 (not Position 3) to eliminate the capability cliff between DeepSeek and Llama 8B. The 60s timeout gives auto-beta room to route through its classifier and find a comparable model.
3. **Flash replaces Pro as primary** — Pro returns `content: null` on 3/5 conversational tasks (ghost response = F1 violation). Flash passes 4/5, costs 1/3, and handles tool calling reliably. Pro reserved as tokenrouter fallback for deep reasoning.

## Current Hermes Fallback Chain (9 tiers)

```
Position 1 (PRIMARY):       deepseek/deepseek-v4-flash (direct)              — conversational primary
                              ↓ fail?
Position 1.5 (REASONING):   tokenrouter/deepseek-v4-pro (20s)                — deep reasoning reserve
                              ↓ fail?
Position 2 (BRIDGE):        openrouter/auto-beta (60s)                       — capability-equivalent failover
                              ↓ fail?
Position 3 (SPEED):         groq/llama-3.1-8b-instant (20s)                  — last resort speed lane
                              ↓ fail?
Position 4:                 sea-lion/Qwen-SEA-LION-v4-32B-IT (20s)
                              ↓ fail?
Position 5:                 gemini/gemini-2.5-flash (20s)
                              ↓ fail?
Position 6:                 tokenrouter/MiniMax-M3 (20s)
                              ↓ fail?
Position 7:                 tokenrouter/z-ai/glm-5.2 (20s)
                              ↓ fail?
Position 8 (SURVIVAL):      openrouter/free (60s)                             — 50 RM0 models, 20 req/min
                              ↓ fail?
Position 9 (LAST RESORT):   ollama/qwen2.5-coder:3b (20s)                     — local survival
```

## Config (YAML)

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek

fallback_providers:
  - model: deepseek/deepseek-v4-pro
    provider: tokenrouter
    timeout: 20
  - model: openrouter/auto-beta
    provider: openrouter
    timeout: 60
  - model: llama-3.1-8b-instant
    provider: groq
    timeout: 20
  - model: aisingapore/Qwen-SEA-LION-v4-32B-IT
    provider: sea-lion
    timeout: 20
  - model: gemini-2.5-flash
    provider: gemini
    timeout: 20
  - model: MiniMax-M3
    provider: tokenrouter
    timeout: 20
  - model: z-ai/glm-5.2
    provider: tokenrouter
    timeout: 20
  - model: openrouter/free
    provider: openrouter
    timeout: 60
  - model: qwen2.5-coder:3b
    provider: ollama
    timeout: 20
```

## Design Notes

- **Position 1.5 (tokenrouter/Pro):** Not a full-fledged fallback tier in the original sense. tokenrouter re-routes the same DeepSeek V4 Pro model through a different connection path — it's a "try again" hop, not a model change. If Flash fails AND tokenrouter/Pro also fails, only then does the system fall out to a different model family (auto-beta).
- **Position 2 (auto-beta, 60s timeout):** auto-beta needs more time than direct providers because of its classifier meta-round-trip (~200-500ms) and the fallback enumeration across 70+ providers. The 60s budget accommodates the worst case where the first 2-3 auto-beta choices also fail and it has to exhaust the community-ranked list.
- **Position 8 (openrouter/free, RM0):** Partially redundant with auto-beta (Position 2), which also routes through OpenRouter. Free tier remains as a fallback for when credit is depleted or auto-beta API is discontinued. Redundancy here is intentional — two different code paths for the same outcome.
- **No Qwen3-VL-30B-A3B in fallback chain:** Vision-native model sits in the auxiliary.vision provider config, not in the conversation fallback chain. Images are handled by the vision pipeline before the main text model is called.
- **Price control on auto-beta:** Default CQT=9 (cost-leaning). `max_price` and `cost_quality_tradeoff` cannot be set via Hermes `fallback_providers[]` — Hermes ignores `extra_body`/`plugins` on fallback entries. Price caps must be enforced via OpenRouter Management API guardrails.

## Previous Chain (before 2026-07-29)

Before this session, the chain was:
```
Position 1:   tokenrouter/deepseek-v4-pro (20s)
Position 2:   groq/llama-3.1-8b-instant (20s)          ← CAPABILITY CLIFF
Position 3:   sea-lion/Qwen-SEA-LION-v4-32B-IT (20s)
Position 4:   gemini/gemini-2.5-flash (20s)
Position 5:   tokenrouter/MiniMax-M3 (20s)
Position 6:   tokenrouter/z-ai/glm-5.2 (20s)
Position 7:   openrouter/free (60s)
Position 8:   ollama/qwen2.5-coder:3b (20s)
```

**Key changes:**
- Primary changed from deepseek-v4-pro → deepseek-v4-flash
- `deepseek-v4-pro` moved to tokenrouter Position 1.5 (reasoning reserve)
- `openrouter/auto-beta` inserted at Position 2 (capability bridge)
- 9 tiers instead of 8

## Vision Routing — Path B (Full Bypass)

**Changed from Path A (IMAGE TRANSCRIPT → Flash) to Path B (route entire turn to vision model) in this session.**

Images are handled by deterministic payload inspection, not by the fallback chain:

```
User sends TEXT
  → payload inspector: no image parts found
  → Flash primary (0ms overhead)
  → normal text conversation

User sends IMAGE
  → payload inspector: image_url detected in messages
  → gateway._prepare_inbound_message_text() routes to PATH B
  → defer images as pending_native + set model override
  → gateway._run_conversation_with_agent() consumes override
  → swap agent.model to 'qwen/qwen3-vl-30b-a3b-instruct' / 'openrouter'
  → build_native_content_parts() creates image_url content parts
  → qwen3-vl processes image natively — ONE API call, not two
  → responds directly — no [IMAGE TRANSCRIPT] pipeline
  → restore agent.model to deepseek-v4-flash / deepseek
  → next turn back on Flash
```

### Path A vs Path B Comparison

| Dimension | Path A (before) | Path B (current) |
|-----------|----------------|------------------|
| **Flow** | qwen3-vl describes → Flash responds | qwen3-vl directly responds |
| **API calls per image turn** | 2 (vision + primary) | 1 (vision model is primary for this turn) |
| **Latency** | ~4s + ~2s = ~6s+ | ~4s total (one qwen3-vl call) |
| **F2 TRUTH risk** | HIGH — transcript loss → hallucination | NONE — image seen directly |
| **Broken telephone** | YES — qwen3 describes, Flash fills gaps | NO — single model sees everything |
| **Tool calling on images** | Flash calls tools after description | qwen3-vl handles tools natively (770ms) |
| **Epistemic boundary** | Model makes claims from secondary data | Model sees primary data directly |

### Source Patches (1 file: gateway/run.py)

Full patch code: `references/path-b-vision-bypass-source-patch-2026-07-29.md`.

Three changes to `gateway/run.py`:

1. **`_prepare_inbound_message_text`** — Changed image routing: instead of transcribe→Flash via `_enrich_message_with_vision()`, defer images as `pending_native` + set `_pending_vision_model_overrides[session] = {model: qwen-vl, provider: openrouter}`.

2. **`_consume_pending_vision_model_override()`** — New consumer method (same pattern as `_consume_pending_native_image_paths`).

3. **`_run_conversation_with_agent`** — Before `agent.run_conversation()`: consume override → swap `agent.model`/`agent.provider` to qwen-vl. After: restore to Flash.

### Config Dependencies

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  supports_vision: false          # MUST be false — triggers bypass

auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen3-vl-30b-a3b-instruct
    timeout: 120

image_input_mode: text            # top-level, overwrites sub-section auto
```

### `image_input_mode` Config Trap

The Hermes config has **two entries** for `image_input_mode`:

```yaml
# Line 14 (under a sub-section): image_input_mode: auto
# Line 740 (top-level): image_input_mode: text
```

YAML resolves duplicate keys by preferring the LAST one parsed. The top-level `text` at line 740 **overwrites** the sub-section `auto` at line 14. The practical effect: all images go through the text pipeline (vision_analyze → description prepended), which is correct for Path B since the model switch happens at `_prepare_messages_for_non_vision_model`, not at the image_input_mode level.

If you change one, verify which one takes effect with `grep image_input_mode /root/.hermes/config.yaml`.

### Vision Model History

| Date | Model | Provider | Outcome |
|------|-------|----------|---------|
| 2026-07-24 | kimi-k3 | opencode-go | 403 Forbidden on image payloads (opencode-go proxy limitation) |
| 2026-07-29 (fix 1) | kimi-k3 | openrouter | Works, but content=null bug on some calls — unreliable for vision |
| 2026-07-29 (fix 2) | **qwen/qwen3-vl-30b-a3b-instruct** | openrouter | ✅ Native vision, free, no null content, 770ms tool calls |

**Live config:**
```yaml
auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen3-vl-30b-a3b-instruct
    timeout: 120
    api_key: ''
    base_url: ''
```

### The Sovereignty Paradox — Why OpenRouter Is NOT Primary

OpenRouter as PRIMARY was rejected by Arif (2026-07-29) for three reasons:

1. **Classifier Tax:** auto-beta adds 200-500ms TTFT via its community-spend classifier. This is real latency burned before first token.
2. **Sovereignty Paradox:** To make auto-router safe for sovereign topics (PETRONAS, 1MDB), you constrain `allowed_models` to 1-2 families — but that defeats the router's purpose. You're paying the latency + proxy fee for zero routing intelligence.
3. **Black-Box Kernel (F1 violation):** auto-beta's community-spend ranking has NO knowledge of which models censor MY governance topics. A censored model (MiniMax) can be selected for sovereign-adjacent work.

**Rule:** OpenRouter belongs at Position 2 (intelligent failover), never at primary. Primary stays direct DeepSeek V4 Flash — zero proxy, zero classifier, 100% epistemic control.
