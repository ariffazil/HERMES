---
name: provider-routing-zen
description: >-
  Govern LLM provider selection, routing, and cost-quality optimisation across
  the AAA federation. Maps constitutional roles to providers, sets per-role
  cost-quality dials (CQT), enforces ZDR/sovereignty constraints, and designs
  resilient fallback chains. Covers OpenRouter, TokenRouter, FLAME, LiteLLM
  (FED FLAME FRAME), and direct provider integrations.
---

# Provider Routing Zen — AAA Federation

> **Doctrine:** Every model call has a constitutional role. Choose the provider for the role, not for habit.
> **Canonical SOT:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json`
> **Deep reference:** `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` (OpenRouter-specific)

## When to Use This Skill

- Defining or updating a fallback chain for any agent (Hermes, OpenClaw, OpenCode, Forge)
- Deciding which provider should serve a constitutional role (OBSERVE, THINK, JUDGE, FORGE, SEAL)
- Optimising cost vs quality across the federation
- Mapping multi-seat Token Plan providers — see `references/qwen-token-plan-multi-seat.md`

## Workflow Correction (2026-08-03)

**Audit first. Do NOT jump to creating new provider blocks before completing a full inventory.**

When Arif asks about provider mapping, the sequence is:

1. Enumerate ALL keys in vault (kunci-mas) + shell env
2. Probe each key live via `/models` + `/chat/completions`
3. Cross-reference config providers → key_env → actual key access
4. Identify gaps: unmapped seats, shared keys, stale model lists
5. **Report findings as a gap table BEFORE touching any config**
6. Fix only what's needed — not all gaps need new providers

**Correction (proven):** I created a new provider before Arif saw the full audit.
He said: "wei hang kangan cipta baru. audit first apa ada and then fix whatever
needed to be fix."

See `references/qwen-token-plan-multi-seat.md` for the full 4-seat zen architecture,
audit procedure, and pre/post-gap analysis.stry
- Auditing whether current routing leaks sovereign data or violates F2/F9/F13
- Designing FLAME tool-lane routing
- Diagnosing 401/InvalidApiKey cascades where an entire provider chain dies at once

## Qwen Token Plan TEAM Edition — THE FED primary (2026-08-02)

> **Status:** ✅ LIVE — primary provider for Hermes (`qwen-token-plan` / **`qwen3.8-max` GA**), RM0 marginal on flat monthly seats.
> **PRIMARY MODEL CHANGE (2026-08-03):** Hermes `model.default` is now **`qwen3.8-max`** (GA, released 2026-08-02, GA-priced 2026-08-05), NOT `deepseek-v4-pro`. The `qwen3.8-max-preview` model ID is RETIRED — all config refs migrated to `qwen3.8-max` (only `.bak` files retain the old ID). `qwen3.8-max` supports **native base64 vision** (verified live) — PRMT vision-transcript pipeline is now optional. Constitutional roles 666_JUDGE / 999_SEAL remain DeepSeek-v4-pro ONLY (FFF gate). See `references/qwen38-max-primary-2026-08-03.md`.
> **2026-08-03 UPDATE:** Hermes primary model is now **qwen3.8-max** (GA 2026-08-02) served via `key_env: QWEN_HERMES_API_KEY` (Standard seat) in live config. Live-verified 2026-08-03: native base64 vision ✅ (correct description), structured tool calls ✅ (clean args, no content:null), 1M ctx, always-on reasoning with working `reasoning_effort` param (low/high/xhigh; low ≈40% fewer reasoning tokens, ≈25% faster). ⚠️ Pro seat `QWEN_OPENCODE_API_KEY` returned `insufficient_quota` for qwen3.8-max AND qwen3.8-max-preview on 2026-08-03. ⚠️ Live fallback chain is now only 2 entries: opencode-go/deepseek-v4-pro → minimax/MiniMax-M3 (down from 11-tier). Open weights for qwen3.8-max promised ~week of 2026-08-02 (first ever Max-class open-weight; license TBD).
> **Base URL:** `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
> **Transport:** `openai_chat` (compatible-mode = OpenAI-compatible chat completions)
> **Seat registry SOT:** `/root/AAA/federation/seats.yaml` — env var → seat → key prefix, tier, monthly credits, vault/rotation status. READ THIS FILE before touching any Qwen key.

**Seat wiring (verified live 2026-08-03 — 4 active keys, 4 Team seats + 1 Individual, 2 Team seats unmapped in config):**

→ Full 4-seat map, unmapped-seat detection with vault-vs-config cross-reference, provider-sharing-same-key pitfall, and per-seat rate-limit behaviour: `references/qwen-token-plan-multi-seat.md` (PROVEN 2026-08-03).

| Env var | Seat | Key prefix | Monthly | Serves |
|---|---|---|---|---|
| `QWEN_OPENCODE_API_KEY` | Team Pro | `sk-sp-H.DIEXP` | 100K | **Hermes PRIMARY** + OpenCode + Codex |
| `QWEN_API_KEY` (legacy) | Team Pro | `sk-sp-H.DIEXP` | 100K | **SAME key** as OPENCODE — alias only |
| `QWEN_HERMES_API_KEY` | Team Standard | `sk-sp-D.IPRH` | 25K | Hermes fallback + LiteLLM forge/planner/ops/small |
| `QWEN_BAILIAN_KEY` (legacy) | Team Standard | `sk-sp-D.IPRH` | 25K | **SAME key** as HERMES — alias only |
| `QWEN_INDIVIDUAL_API_KEY` | Individual Pro | `sk-sp-H.DIIYD` | 5h+7d windows | **Multimodal ONLY** (TTS, image, video). NOT primary chat. |
| `QWEN_OPENCLAW_API_KEY` | Team Standard (Seat 2) | `sk-sp-D.IEHM` | 25K | ❌ DEAD — key purged 2026-08-02. Seat vacated. Needs rotation. |

**⚠️ CRITICAL: Only 2 actual keys exist under these 6 env var names.** `QWEN_API_KEY` = `QWEN_OPENCODE_API_KEY` (same key, Pro 100K). `QWEN_BAILIAN_KEY` = `QWEN_HERMES_API_KEY` (same key, Standard 25K). `QWEN_OPENCLAW_API_KEY` is dead (key purged). **Do NOT treat these as independent keys when designing fallback chains.**

**⚠️ Individual Pro ToS risk:** Individual Pro §1 prohibits "automated scripts, application backends, non-interactive batch processing." Using it as Hermes primary is a compliance violation. Use ONLY for multimodal generation (TTS, image gen, video) — never for chat primary or fallback.

**⚠️ Individual Pro quota model:** 5-hour and 7-day rolling windows (12K/5h, 40K/7d), NOT monthly like Team seats. Exhaustion is silent until 429 hits. The error message is `"code": "insufficient_quota"` (not `"Throttling.RateQuota"` — this is quota exhaustion, not transient rate limiting).

**Provider wiring (live 2026-08-02):**
- `qwen-token-plan` → `key_env: QWEN_OPENCODE_API_KEY` (Pro 100K) — Hermes primary
- `qwen-token-plan-standard` → `key_env: QWEN_HERMES_API_KEY` (Standard 25K) — fallback lane
- `qwen-token-plan-individual` → `key_env: QWEN_INDIVIDUAL_API_KEY` (Individual Pro) — multimodal only
- `qwen-responses` → `key_env: QWEN_INDIVIDUAL_API_KEY` (Individual Pro) — FED Harness

**Fallback chain (live 2026-08-03):** PRIMARY `qwen3.8-max` @ qwen-token-plan → **deepseek-v4-pro @ opencode-go** (reasoning reserve) → **MiniMax-M3 @ minimax** (independent provider, compression lane). Note: the live Hermes chain collapsed to this short 2-entry list; the older 11-tier chain below is historical reference. **666/999 judge+seal = DeepSeek-only, never Qwen.** `reasoning_effort: ''` on Qwen = xhigh always-on (intentional). See `references/qwen38-max-primary-2026-08-03.md`.

**Everything keys off the provider name `qwen-token-plan`:** once the provider's key is alive, `auxiliary.vision`, `auxiliary.compression`, `moa.*` presets, `tts.provider`, and `search.name` all heal at once — no per-field wiring needed.

> **Reference:** `references/qwen-token-plan-seat-wiring.md` under the `tokenrouter-guide` skill (devops/) — full diagnosis recipe, curl probes, and the 2026-08-01 fix transcript.

## Two-Lane Architecture: OpenRouter (Mind) vs FLAME (Muscles)

### OpenRouter Structural Benefits (Arif, 2026-07-29)

OpenRouter is a centralised LLM gateway routing signals to 400+ models across 70+ providers via a single API key and one standard interface. For arifOS, where the kernel (:8088) is central and AAA MCP is the connection wire, OpenRouter sits at the edge — proxying external calls instead of requiring reintegration for each new model.

| Benefit | Mechanism | Floor |
|---------|-----------|-------|
| **Code Entropy Reduction (ΔS < 0)** | One OpenAI-compatible endpoint. Switch models by changing the model string in the payload | F4 CLARITY |
| **Resilience (F1 Safety)** | Silent failover on upstream outages/rate limits. Chain stays alive without manual 888_HOLD | F1 AMANAH |
| **Tri-Witness Validation** | Summon entirely different model families (DeepSeek, Mistral, Gemini) via one API to cross-validate signals without structural debt | F3 TRI-WITNESS |
| **Targeted Execution** | Route latency-sensitive tasks to Groq LPU (320 tok/s), heavy docs to Gemini 1M context, all governed from one control plane | F8 GENIUS |

The structural value is decoupling internal kernel logic from external provider chaos. You dictate routing rules; the gateway executes them.

| Lane | Layer | What | Provider | Cost |
|------|-------|------|----------|------|
| **Mind (Agent)** | OpenRouter | Agent intelligence, reasoning, judgment, conversation | auto-beta → DeepSeek V4 Flash/Pro | $30 credit, ~$0.50-1.00/session |
| **Muscles (Tools)** | FLAME | Model routing for 35 tool tasks, summarisation, extraction, classification | Groq→SEA-LION→Gemini→Cerebras→openrouter/free | RM0 — all free tiers |

**Never cross the streams:** Tool output must never enter the governed cascade. Agent output must never route through FLAME. Separate lanes, separate concerns.

## MuleRouter — Multimodal Gateway (Integrated 2026-07-30, Corrected 2026-07-30)

> **Status:** ✅ LIVE — key staged in kunci-mas.env, provider registered in Hermes config & AGENT_MODEL_MAP (17th provider, ACTIVE).
> **Base URL:** `https://api.mulerouter.ai/vendors/openai/v1/chat/completions`
> **Key env:** `MULEROUTER_API_KEY`
>
> **Bottom line:** MuleRouter is a multi-modality API aggregator — 31 models across Qwen, DeepSeek, GPT, Grok, GLM, Kimi, MiniMax, Wan, Kling — with **fixed pricing, satu key, satu bill**. All LLM chat goes through OpenAI-compatible `/v1/chat/completions`. Media generation (TTS, music, video, image) uses async task endpoints.
>
> **2026-07-30 correction:** Earlier version of this skill incorrectly stated MuleRouter had "no DeepSeek models." This was a doc-search error — the `/v1/models` endpoint (via `vendors/openai/v1/models`) reveals 31 models including **deepseek-v4-flash** and **deepseek-v4-pro**. Always probe `/v1/models` directly before claiming model gaps — commercial aggregators update faster than their docs.
>
> **Key constraints (not gaps):**
> - **Vision base64 — CORRECTED:** MuleRouter was initially believed to reject data: URIs. Tested 2026-07-30: MuleRouter qwen-vl-max successfully processes base64 images. Now live as Hermes auxiliary.vision.provider.
> - **No STT/ASR endpoint documented.** Speech recognition is still via OpenAI Whisper or local faster-whisper.
> - **Media generation is async-task based.** All non-chat endpoints (TTS, image gen, video, music) use the pattern: POST → `task_id` → poll GET until `status: "completed"`. See `references/mulerouter-integration-2026-07-30.md` for full endpoint paths and formats.
> - **Base URL is `/vendors/openai/v1` NOT bare `/v1`.** The bare `/v1` returns 404. The correct OpenAI-compatible base is `https://api.mulerouter.ai/vendors/openai/v1`. This applies to ALL endpoints — chat, models list, and chat-compatible vision. Media endpoints use vendor-specific paths (`/vendors/minimax/...`, `/vendors/openai/...`).
>
> **Use cases:**
> - **LLM chat** — deepseek-v4-flash, qwen3.7-max, gpt-5.5 (fixed price vs OpenRouter's floating "harga yahudi")
> - **Vision (URL-only)** — qwen-vl-max, qwen3-vl-plus, qwen3-omni-flash
> - **Media generation (TBD integration)** — Wan video, Kling video, MiniMax TTS/Music, GPT Image 2
>
> **Test results (live, 2026-07-30):**
>
> | Endpoint | Model | Response | Latency |
> |---|---|---|---|
> | Text | qwen3-vl-plus | "VERIFIED" | < 2s |
> | LLM list | /v1/models | 31 models incl. deepseek-v4-flash/pro | < 1s |
> | **TTS (HD)** | MiniMax Speech 2.8 HD | ✅ 8.4s MP3, 128kbps | ~3s gen |
> | **Image Gen** | GPT Image 2 | ✅ 1024x1024 PNG | ~5s gen |
>
> **Full model list (31):**
> deepseek-v4-flash, deepseek-v4-pro, glm-5.1, gpt-5.4/5.4-mini/5.4-nano, gpt-5.5, gpt-5.6-luna/5.6-sol/5.6-terra, grok-4, grok-4-20-non-reasoning, grok-code-fast-1, kimi-k2.6, qwen-flash, qwen-plus, qwen-vl-max, qwen3-max, qwen3-max-2026-01-23, qwen3-omni-flash, qwen3-vl-flash, qwen3-vl-plus, qwen3.5-flash, qwen3.5-omni-flash, qwen3.5-omni-plus, qwen3.5-plus, qwen3.6-flash, qwen3.6-max-preview, qwen3.6-plus, qwen3.7-max, qwen3.7-plus.
>
> **Arif's preference:** "OpenRouter harga yahudi" — floating pricing is a constitutional pain point. Fixed pricing preferred. MuleRouter + OpenCode Go + TokenRouter now cover the three fixed-price lanes.
>
> See `references/mulerouter-integration-2026-07-30.md` for full integration transcript.

### Wolf Cabinet Model — Three-Layer Constitutional Architecture (EUREKA 2026-07-30)

> **The one breath:** Provider bukan kedai runcit model. Provider adalah lapisan perlembagaan. Δ merasa, Ω menghakimi, Ψ bertahan. Tiga layer, satu swarm.
>
> **Contradiction resolved:** The federation needs both a unified multimodal surface (one key, fixed price, vision/TTS/music/video) AND constitutional multi-provider redundancy for judgment. Previously this looked like a trade-off — pick one provider and accept the gap. Wolf Cabinet compresses into: **provider selection IS constitutional layer assignment.**
>
> **Canonical implementation:** `/root/AAA/scripts/federation_model_router.py`
> **Full reference:** `references/wolf-cabinet-model-2026-07-30.md`

```
                    Δ (PERCEPTION) → MuleRouter
                    Ω (JUDGMENT)   → OpenRouter
                    Ψ (SURVIVAL)   → Ollama
```

| Layer | Provider | Why | Risk if down | Floor |
|-------|----------|-----|-------------|-------|
| **Δ Perception** | MuleRouter | Satu key, fixed price, vision/TTS/music/video, DeepSeek Flash/Pro ✅ | Reversible — retry | F1 SAFE |
| **Ω Judgment** | OpenRouter | Multi-provider DeepSeek V4 Pro redundancy — no single point of failure | **Irreversible** | F1 HARD |
| **Ψ Survival** | Ollama | Local qwen3:8b — zero cost, sovereign, always available | Zero (local) | F13 SOVEREIGN |

**Routing rules (in order of priority):**
1. **Vision** (any agent) → MuleRouter (qwen-vl-max / qwen3-vl-plus / qwen3-omni-flash)
2. **Fast chat** (Hermes daily) → MuleRouter deepseek-v4-flash (fixed price) or OpenCode Go ($10/mo flat)
3. **Constitutional reasoning** (judge/seal, 888-APEX) → OpenRouter deepseek-v4-pro ONLY (multi-provider redundancy)
4. **Deep code/reasoning** (OpenCode, 333-AGI) → OpenRouter deepseek-v4-pro (proven reliability, broad model access)
5. **Research/omni** (555-ASI) → MuleRouter qwen3-max (fixed pricing)
6. **ALL CLOUD FAIL** → Ollama local recovery (qwen3:8b)

**Why the layers map to F-floors:**
- MuleRouter handles perception — can be retried, reversible, F1-safe
- OpenRouter handles judgment — multi-provider failover protects constitutional integrity (F1 AMANAH irreversible)
- Ollama handles survival — zero dependency on external providers (F13 SOVEREIGN floor)

### Provider Comparison Matrix

| Dimension | MuleRouter | OpenRouter | Direct (DeepSeek/TokenRouter) |
|-----------|-----------|------------|-------------------------------|
| **Billing model** | Satu key, satu bill, fixed pricing ✅ | Floating/"harga yahudi" ❌ | Fixed per-provider |
| **Vision enrich** | Qwen3-Max/VL-Plus via chat ✅ | Qwen3-VL, etc ✅ | — |
| **TTS** | MiniMax Speech 2.8 HD ✅ | ❌ | MiniMax direct ✅ |
| **Music gen** | MiniMax Music 2.5 ✅ | ❌ | MiniMax direct ✅ |
| **Video gen** | Wan 2.6, Kling V3, MJ Video ✅ | ❌ (limited) | ❌ |
| **Image gen** | GPT Image 2, MJ, Nano Banana ✅ | ✅ | Mage MCP ✅ |
| **LLM models** | Qwen3.7 Max, GPT-5.5, Grok 4 | 300+ models | DeepSeek, etc |
| **DeepSeek** | **✅ NOW AVAILABLE —** deepseek-v4-flash and deepseek-v4-pro added to MuleRouter's model list (2026-07-30). Note: MuleRouter has a narrower set than OpenRouter but coverage is expanding. | ✅ | ✅ Primary |
| **STT (ASR)** | **❌ Not documented** | ❌ | Local Whisper ✅ |
| **Pricing stability** | Fixed — doesn't change with demand ✅ | Floating by demand ❌ | Fixed per provider |
| **Credit model** | Pay-as-you-go, satu key | Topup $5 minimum | Varies |

### When to Choose Which

| Scenario | Pick |
|----------|------|
| DeepSeek reasoning primary | Direct DeepSeek or TokenRouter |
| Vision enrichment for text-only model | OpenRouter (proven, $0.000014/call with Qwen VL Plus) |
| Video generation (Wan/Kling/MJ) | **MuleRouter** — only option covering all three |
| Music generation | MiniMax direct or MuleRouter |
| TTS | MiniMax direct (already wired) or MuleRouter |
| Unified billing (satu roof, satu bill) | MuleRouter — but missing STT and base64 vision |
| Maximum model variety for fallback | OpenRouter (343 models) |

### The Unified-Billing Trap (Probed 2026-07-30, Corrected 2026-07-30)

Satu key, satu bill sounds ideal, but in practice Arif's stack still needs **two** things MuleRouter doesn't provide (not three — DeepSeek is now available via MuleRouter):

1. **STT** — MuleRouter's docs don't show any speech-to-text endpoint. Arif currently uses OpenAI Whisper or local faster-whisper.
2. **Base64 vision** — MuleRouter rejects data: URIs — only publicly accessible image URLs work. This makes it **unusable as `auxiliary.vision.provider`** for Hermes PRMT pipeline (which encodes Telegram images as base64).

**Resolved: DeepSeek models are now available via MuleRouter.** As of 2026-07-30, `/vendors/openai/v1/models` returns deepseek-v4-flash and deepseek-v4-pro. Hermes now uses MuleRouter as its default provider with deepseek-v4-flash as the primary model. This was previously the binding constraint against MuleRouter as text primary — it is no longer a constraint.

**Hybrid approach (live, confirmed):**
| Lane | Provider | Why |
|------|----------|-----|
| Constitutional text (333, 888, Hermes) | **OpenRouter / OpenCode Go** | DeepSeek V4 Flash/Pro — proven tool calling |
| Fast text + omni (555-ASI) | **MuleRouter** | qwen3-max at 1015ms, fixed pricing |
| Vision for URL-based images | **MuleRouter** | qwen-vl-max at 1883ms, qwen3-omni-flash at 1030ms |
| Vision for Telegram (base64) | **OpenRouter** (auxiliary.vision) | Only path that handles data: URIs |
| Local recovery | **Ollama** | qwen2.5:3b / qwen3:8b (TBD) |

| TokenRouter | Balance-based, fixed per-model | ✅ |
| OpenRouter | **Floating** — harga ikut demand | ⚠️ Harga yahudi — acceptable only for constitutional (multi-provider redundancy) |
| MiniMax Token Plan | Quota-based (5.1B tokens/mo) | ✅ Fixed |

**Rule:** When a choice exists between fixed and floating pricing for the same capability, prefer fixed. Floating pricing is acceptable only when:
- No fixed-price alternative exists for that capability AND the capability is strategically essential (e.g., multi-provider DeepSeek redundancy for constitutional judgment), OR
- The absolute cost is negligible (< $0.001/call) AND the capability layer is reversible (perception, not judgment)

**Constitutional mapping of pricing models:**
| Layer | Preferred pricing | Why |
|-------|-----------------|-----|
| Δ Perception (MuleRouter) | Fixed | Predictable budget for high-volume multimodal ops |
| Ω Judgment (OpenRouter) | Floating acceptable | Multi-provider redundancy is the primary value — pricing is secondary |
| Ψ Survival (Ollama) | Zero (local) | Always free, always available |

### The Unified-Billing Frame (Corrected 2026-07-30)

"Satu key, satu bill" for multimodal work is now achievable via MuleRouter — it covers LLM chat (incl. DeepSeek V4 Flash/Pro), vision, TTS, music, video, and image gen under one roof. The remaining gaps are:

1. **STT (ASR)** — MuleRouter has no documented speech-to-text endpoint. Still needs OpenAI Whisper or local faster-whisper.
2. **Constitutional redundancy** — OpenRouter's multi-provider DeepSeek topology is still required for 888-APEX / 999-SEAL judgment.

**Correction — base64 vision:** MuleRouter was previously believed to reject `data:` URIs. This was a doc-search error — **tested 2026-07-30: MuleRouter qwen-vl-max successfully processed base64 images via Hermes auxiliary vision path.** Hermes now uses MuleRouter as `auxiliary.vision.provider` with `qwen-vl-max`. The "URL-only" constraint from earlier doc search was a false negative. Always probe the API, not the docs.

**Wolf Cabinet resolves this:** Not "one provider to rule them all" but "each constitutional layer picks the right provider."

### When to Choose Which

| Scenario | Pick |
|----------|------|
| Multimodal ops (vision, TTS, music, video) | **MuleRouter** — satu key, fixed price |
| Constitutional judgment (888-APEX, 999-SEAL) | **OpenRouter ONLY** — multi-provider DeepSeek V4 Pro |
| Hermes daily chat | **MuleRouter** deepseek-v4-flash (fixed) or **OpenCode Go** ($10/mo flat) |
| DeepSeek reasoning primary (333-AGI, OpenCode) | **OpenRouter** — proven tool calling, model variety |
| Vision enrichment for Telegram (base64) | **OpenRouter** or MiniMax direct — MuleRouter rejects data: URIs |
| Video generation (Wan/Kling) | **MuleRouter** — only option covering all three |
| Music generation | MiniMax direct or MuleRouter |
| TTS | MiniMax direct (already wired) or MuleRouter |
| Maximum model variety for fallback | OpenRouter (343 models) |
| Local recovery, zero cost | **Ollama** — qwen3:8b |

## Vision Model Strategy — PRMT (Current) / Path B (Historical)

> **PRMT Epistemic Dependency — F2 vulnerability:** DeepSeek's reasoning ceiling = Qwen-VL's descriptive floor. Language is not the medium — language IS the reality. Full analysis: `references/prmt-epistemic-dependency.md`

**⚠️ Path B (model swap) was REVERTED 2026-07-30 due to cascade failure.** The current Hermes vision strategy is **PRMT** (Pre-Routing Modality Translation): image → text transcript via Qwen-VL → same text-only primary model. See `hermes-gateway-image-routing` skill for full details, including `references/prmt-architecture.md`.

### Path B (Historical — Reverted 2026-07-30)

Kept for reference only. This approach was attempted 2026-07-29: payload inspector detects image → **switch model entirely** to vision specialist — no transcript, no second API hop. Reverted because when the override provider failed (auth/network), image bytes were still in context, and all text-only fallback models crashed with 413 "request too large."

### Path B Implementation (Gateway-based, 2026-07-29)

Three source patches to `gateway/run.py`, all auto-reverting per-session-clear:

1. **`_prepare_inbound_message_text` — image routing block**  
   When `_img_mode == "text"` (text-only model like Flash + images present), instead of calling `_enrich_message_with_vision()`:  
   → Defer images as `pending_native` (same mechanism as native vision models)  
   → Set `_pending_vision_model_overrides[session_key] = {"model": "qwen/qwen3-vl-30b-a3b-instruct", "provider": "openrouter"}`

2. **`_consume_pending_vision_model_override()` — new consumer**  
   Same pattern as `_consume_pending_native_image_paths()`. Consumes and clears the override dict for the session, ensuring one-turn-only effect.

3. **`_run_conversation_with_agent` — model swap + restore**  
   Before `agent.run_conversation()`: if override exists and native images are pending → save `agent.model`/`agent.provider`, swap to qwen-vl/OpenRouter.  
   After `agent.run_conversation()`: restore original model/provider.  
   Guarded by `_restore_model is not None` — no-op on non-bypass turns.

**Why gateway, not run_agent.py:** The existing `pending_native_image_paths` pattern already handles deferred native image attachment. Hooking Path B into the same mechanism is less invasive than patching the core agent loop — the gateway already decides routing, so the model swap sits naturally at the routing decision point.

Full patch: `references/path-b-vision-bypass-source-patch-2026-07-29.md`.

### Path A vs Path B — Experimental Finding

Before this session, Path A was the default: qwen3-vl describes image → [IMAGE TRANSCRIPT] → Flash reads and responds. Arif's observation: "Flash always hallucinate on images" was confirmed as a **text-only model limitation**, not a Flash bug. Flash receives a lossy text description and confidently fills the gaps with fabricated detail (F2 TRUTH violation).

Path B eliminates the problem at the architectural level: the vision model never describes for the text model — it IS the solver for that turn. No human-in-the-loop description, no broken telephone.

### Best vision-native candidates (free via OpenRouter, probed 2026-07-29)

| Model | Latency (reasoning) | Tool calls | Context | Cost | Censorship |
|-------|:---:|:---:|:---:|:---:|:---:|
| **qwen/qwen3-vl-30b-a3b-instruct** | **3.9s** | **770ms** ✅ | 262K | Free | None (CN Alibaba) |
| qwen/qwen3-vl-32b-instruct | 17.3s | TBD | 131K | Free | None (CN Alibaba) |
| mistralai/mistral-small-3.2-24b-instruct | 5.3s | TBD | 256K | Free | Mistral AI (EU) |
| meta-llama/llama-4-scout | 21.8s | TBD | 1310K | Free | Meta (US) |

**Qwen3-VL-30B-A3B** is the standout: MoE architecture (3B active per token = very fast), native vision, epistemic tagging, correct tool calling. See `references/model-benchmark-methodology.md` for full benchmark.

**Vision model config wiring (Hermes):**
```yaml
# In /root/HERMES/config.yaml providers section:
openrouter:
    api: https://openrouter.ai/api/v1
    key_env: OPENROUTER_API_KEY
    models:
      - id: qwen/qwen3-vl-30b-a3b-instruct
        name: Qwen3-VL-30B-A3B — Vision-native primary (free, fast)
      - id: deepseek/deepseek-v4-pro
        name: DeepSeek V4 Pro — Sovereign reasoning fallback
```

## Constitutional Role → Provider Mapping

| Role | Primary Provider | OpenRouter OK? | CQT | ZDR? |
|------|----------------|----------------|-----|------|
| `000_INIT` | DeepSeek V4 Pro (direct) | **FORBIDDEN** | — | Required |
| `111_OBSERVE` | OpenRouter/free or FLAME | **PRIMARY** | 10 | Not needed |
| `333_THINK` | DeepSeek V4 Pro (direct) | **FALLBACK** (cqt=3) | 3 | Required |
| `444_ROUTE` | OpenRouter/auto-beta | **PRIMARY** (classify only) | 9 | Required |
| `555_MEMORY` | Direct long-context | **FALLBACK** (1M models) | 5 | Required |
| `666_JUDGE` | DeepSeek V4 Pro (direct) | **FORBIDDEN** | — | Required |
| `777_FORGE` | DeepSeek or OR auto-beta | **FALLBACK** (cqt=5) | 5 | Required |
| `999_SEAL` | DeepSeek V4 Pro (direct) | **FORBIDDEN** | — | Required |

**Hard rule:** 666_JUDGE and 999_SEAL NEVER go through OpenRouter — `identity_verified: false`, no `fff_gate`.

## Per-Agent Routing Table (Live 2026-07-30 — Wolf Cabinet Model)

Every agent has a constitutional role AND a provider surface. Route by constitutional layer, not just by model name. The 3-layer Wolf Cabinet architecture splits traffic:

```
                     ┌──────────────────────────────┐
                     │     FEDERATION MODEL ROUTER   │
                     │  /root/AAA/scripts/federation_model_router.py
                     └──────────┬───────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
  │  Δ MULEROUTER  │   │  Ω OPENROUTER  │   │  Ψ OLLAMA      │
  │  (perception)  │   │  (judgment)    │   │  (survival)    │
  │  fixed price   │   │  multi-provider│   │  local, free   │
  │  satu key      │   │  floating price│   │  sovereign     │
  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
          │                    │                    │
  ┌───────┼────────┐   ┌───────┼────────┐   ┌───────┼────────┐
  │       │        │   │       │        │   │       │        │
  ▼       ▼        ▼   ▼       ▼        ▼   ▼       ▼        ▼
vision  text    TTS/  ds-v4   ds-v4   other  qwen3   qwen2.5  ...
-vl-max ds-flash music -pro    -flash  models :8b     :3b
qwen3   (Hermes  (TBD) (888/   (333/   via OR  (future)(current)
-vl-plus daily)         999     OpenCode         target)
qwen3                     JUDGE  daily)
-omni                     SEAL)
-flash
-flash
```

| Agent | Text Primary | Via | Vision | Via | Const. |
|---|---|---|---|---|---|
| **333-AGI / OpenCode** (you) | deepseek-v4-pro | **OpenRouter** | qwen-vl-max | **MuleRouter** | OpenRouter (multi-provider) |
| **Hermes** (chat) | deepseek-v4-flash | **OpenCode Go** ($10/mo flat) | qwen3-omni-flash | **MuleRouter** | N/A (no judge) |
| **555-ASI** (research) | qwen3-max (1015ms) | **MuleRouter** | qwen3-vl-plus | **MuleRouter** | N/A (no judge) |
| **888-APEX** (verdict) | deepseek-v4-pro | **OpenRouter ONLY** | N/A (text-only) | — | OpenRouter ONLY |
| **GEOX Δ** (seismic) | deepseek-v4-pro | **OpenRouter** | qwen-vl-max | **MuleRouter** | N/A (evidence, not judge) |
| **Recovery** | qwen2.5:3b | Ollama | — | — | — |

**Routing rules (in order of priority):**

1. **Vision** (any agent) → MuleRouter qwen3-omni-flash (fast, 1030ms) or qwen-vl-max (quality, 1883ms)
2. **Constitutional reasoning** (judge/seal) → OpenRouter deepseek-v4-pro ONLY (multi-provider redundancy)
3. **Fast chat** (Hermes daily) → OpenCode Go deepseek-v4-flash ($10/mo flat, fixed pricing)
4. **Deep code/reasoning** (OpenCode) → OpenRouter deepseek-v4-pro (proven reliability)
5. **Research/omni** (555-ASI) → MuleRouter qwen3-max (1015ms, fixed pricing)
6. **ALL CLOUD FAIL** → Ollama local recovery

**Key constraints that shaped this table:**

- MuleRouter vision is URL-only (no base64) — cannot be `auxiliary.vision.provider` for Telegram images
- OpenRouter has multi-provider redundancy for deepseek-v4-pro — constitutional agents (888, 333) must stay on OR for judgment
- OpenCode Go is $10/mo flat — best for Hermes daily driver where cost predictability matters
- 555-ASI (research) is the best MuleRouter candidate — benefits from fixed pricing and fast qwen3-max
- **When evaluating a new aggregator's model catalog: always probe `/v1/models` directly instead of relying on docs pages.** Commercial aggregators (MuleRouter, OpenRouter, TokenRouter) update faster than their documentation. On 2026-07-30, searching MuleRouter docs returned no DeepSeek results, but `/v1/models` revealed deepseek-v4-flash and deepseek-v4-pro. Doc search is not evidence; API response is evidence.

## Cost-Quality Dial (CQT) — Per Role

OpenRouter's `cost_quality_tradeoff` is a 0-10 dial. Override the global default:

- **CQT 0-2:** Pure quality — highest-stakes reasoning (sovereign topics)
- **CQT 3-4:** Quality-leaning — constitutional deliberation, THINK
- **CQT 5-6:** Balanced — FORGE, default agent work
- **CQT 7-9:** Cost-leaning — batch ops, routing classification
- **CQT 10:** Cheapest survivor only — FLAME tool tasks, observe

**Default:** `openrouter/auto-beta` defaults to **CQT=9** (cost-leaning). The deprecated `openrouter/auto` (powered by NotDiamond) defaulted to 7. The difference matters when routing classification work — auto-beta's 9 lean means it picks cheaper community-majority models, which can shift quality on sovereign-adjacent topics.

**Critical distinction:** `openrouter/auto-beta` routes via **community spend-share** (trailing 7-day spend by task class), NOT by NotDiamond model evaluation. The deprecated `openrouter/auto` used NotDiamond's task classifier + evaluator. Auto-beta's community-signal approach is cheaper for OR to run but has NO knowledge of model censorship profiles — if a censored model (MiniMax) has majority community spend for a task class, auto-beta will pick it. **This is why sovereign topics must hard-route direct to DeepSeek.**

**`allowed_models` wildcard format:** OpenRouter's per-request `allowed_models` accepts wildcard arrays:

- `["anthropic/*", "deepseek/*"]` — allow all Anthropic and DeepSeek models
- `["-minimax/*"]` — prefix with `-` to **exclude** all MiniMax models (critical for MY governance — SHADOW-MM-001)
- `["*"]` — allow everything
- Combine with `data_collection: "deny"` for ZDR enforcement
- **Best practice:** On any request that touches sovereign topics, include `"allowed_models": ["deepseek/deepseek-v4-pro"]` to hard-route past the router entirely.

**Zero-completion insurance:** OpenRouter does NOT charge for failed requests. If the selected provider 429s or times out, the auto-failover kicks to the next provider serving the same model at zero cost for the failed attempt.

**Sovereign override:** ANY task touching MY governance, PETRONAS, 1MDB, Najib, Jho Low, myKad — set CQT=0 AND route to DeepSeek V4 Pro DIRECT. Bypass OpenRouter entirely. The auto-router's community-spend ranking does not know which models censor these topics.

## Pricing That Matters (Hermes Agent)

Current session burn: ~$0.50–1.00 per session. OpenRouter credit remaining (2026-07-24): $30.00 (org arifOS, topped up 2026-07-24).

| Model | Cost/M Input | Cost/M Output | Notes |
|-------|-------------|--------------|-------|
| **qwen/qwen3-vl-30b-a3b-instruct** | **$0.00 (FREE)** | **$0.00** | **Vision-native, 3.9s reasoning, 770ms tool calls, 262K ctx, uncensored CN** |
| deepseek-v4-flash | $0.14 | $0.28 | Cheapest paid, fast, text-only (no vision) |
| deepseek-v4-pro | $0.44 | $0.87 | Apex reasoning, severe reasoning overhead (see pitfalls) |
| moonshotai/kimi-k3 | $3.00 | $15.00 | Vision, content=null risk always-on thinking (see pitfalls) |
| openrouter/auto-beta | $0 extra | $0 extra | Same price as selected model |
| openrouter/free | $0 | $0 | 50 RM0 models, 20 req/min |

**Qwen3-VL-30B-A3B-Instruct** — probed 2026-07-29 via OpenRouter free tier. MoE (30B total, 3B active). Native vision eliminates transcript-pipeline hallucination. Tool calling at 770ms. Simple reasoning at 528ms avg. Complex reasoning at 3.9s. Zero MY censorship. **Best candidate for Hermes primary when user sends images frequently.** See `references/model-benchmark-methodology.md` for full comparison.
| Prompt caching (Anthropic) | ~$0.014 effective | ~$0.028 effective | ~90% off on cached ~8K kernel |

System prompt caching rule of thumb: Hermes loads ~8K tokens of system prompts. On Anthropic models via OR with `cache_control: {type: "ephemeral"}`, cache reads cost ~10% of normal input — ~92% saving on every cached call.

**⚠️ Credit balance note (2026-07-24, updated):** This workspace (f5be0c4e) now has **$30 credits** (topped up 2026-07-24). `is_free_tier: false`. The earlier finding of 0 credits was from a management sub-key before the topup — the $30 was applied to the ORG workspace where the management key lives, same workspace as the API key. `searxng/.env` is a symlink → `vault.env` — updating vault.env auto-updates searxng. Always verify with `curl /api/v1/credits` using the active key.

### Auto-Beta Routing Pipeline (Detailed)

The auto-beta router processes each prompt through a 5-step pipeline:

1. **Task classification** — classifier meta-model assigns one of ~30 fine-grained task types (coding, reasoning, translation, research, support, etc.)
2. **Model ranking** — ranks all models by trailing 7-day community spend-share for that specific task class (NOT by NotDiamond as the deprecated `auto` did)
3. **Dial application** — applies `cost_quality_tradeoff` to shift toward cheaper (higher CQT) or pricier (lower CQT) models within the ranked list
4. **Fallback routing** — routes with automatic failover to the next provider serving the same model, respecting `allowed_models` (wildcard array, e.g. `anthropic/*`, `deepseek/*`) and modality constraints (text-only vs vision)
5. **Graceful degradation** — if routing metadata is unavailable (e.g. new task type with no community data), falls back to a standard model instead of failing

The response `model` field reveals which model actually served. Trust this for auditing, never assumptions.

**Wildcard `allowed_models` format:** `anthropic/*`, `deepseek/*`, `-minimax/*` (prefix with `-` to exclude). Combine with `data_collection: "deny"` for ZDR enforcement.**

### Auto-Beta SPOF — Path A Mitigation (forged 2026-07-24)

`openrouter/auto-beta` is **4 agents'** fallback chain in AGENT_MODEL_MAP.json. If OR discontinues it, the chain collapses differently per agent. The fix (Path A + B + C from chaos engineering audit):

**Path A — Distribute explicit OR fallbacks in SOT chains:**

Before (auto-beta was sole OR entry):
```python
fallbacks = ["glm/glm-5.2", "openrouter/auto-beta"]
# If auto-beta dies → drops directly to GLM-5.2 (forge), or worse
```

After (stacked explicit fallbacks):
```python
fallbacks = [
  "glm/glm-5.2", 
  "openrouter/auto-beta",
  "openrouter/auto",                           # explicit OR router (older but stable)
  "openrouter/deepseek/deepseek-v4-flash",     # direct OR model — no router dependency
  "openrouter/free"
]
```

**Key insight:** `openrouter/auto` (the deprecated NotDiamond router) and `openrouter/deepseek/deepseek-v4-flash` (direct model via OR) are SEPARATE entries that don't depend on auto-beta being available. Even if auto-beta is discontinued, these three OR entries provide fallback through different code paths.

The fix was applied to 4 agents: forge, opencode, hermes, openclaw. Verify with:
```bash
python3 -c "
import json
with open('/root/.config/federation-models.json') as f:
    sot = json.load(f)
for a in sot['agents']:
    fb = [f['model_key'] for f in a.get('fallback_chain',[])]
    or_count = sum(1 for k in fb if k.startswith('openrouter/'))
    if or_count > 2:
        print(f'✅ {a[\"agent_id\"]}: {or_count} OR entries')
"
```

**Path B — SOT completeness check:**
```bash
bash /root/AAA/registries/federation-model-sync.sh --completeness
# Flags agents with zero fallbacks (expected: claude-code, copilot, grok — single-model agents)
```

**Path C — Model ID validation in `--verify`:**
```bash
python3 /root/AAA/src/resolvers/opencode_render.py --verify
# Now checks that every model_key in SOT fallback chains exists in MODEL_KEY_TRANSLATION
# Catches typos like "openrouter/auto-betax" before they go live
```

### Implementation Path: Session Stickiness (PATCHED 2026-07-24)

Session stickiness requires a source-code change in Hermes runtime — it CANNOT be achieved through config alone:

- **Source location:** `/usr/local/lib/hermes-agent/agent/agent_init.py` (lines 952-956, function `_run_loop` or equivalent LLM-request dispatch point)
- **Change added:** Every outgoing OpenRouter LLM call now carries header `x-session-id: aaa-hermes-{agent.session_id}`
- **Trigger condition:** Only injected when `base_url` matches `openrouter.ai` AND `agent.session_id` is non-empty
- **Effect:** Pins model+provider for 5min inactivity. Skips classifier round-trip on follow-ups → ~30% latency reduction, hits provider prompt cache.
- **Current status:** ✅ PATCHED — live in `/usr/local/lib/hermes-agent/agent/agent_init.py`
- **Verification:** After restart, check that outbound requests carry the header via Heracles logs or OR dashboard request inspector
- **Revert:** `git checkout -- agent/agent_init.py` in the Hermes agent source root

## Fallback Chain Architecture

### Capability Cliff Anti-Pattern (F2 TRUTH hazard)

A **capability cliff** occurs when a small, cheap model sits immediately below a heavy reasoning model in the fallback chain — e.g., DeepSeek V4 Pro → Groq Llama 8B. If the primary fails, **every complex prompt falls into a model that cannot handle it**, producing hallucination or garbage output instead of intelligent degradation. This is an F2 TRUTH violation (fidelity < 0.99 on failover).

**The fix:** Insert `openrouter/auto-beta` between the heavy primary and the cheap speed lane. Auto-beta classifies prompt complexity and routes to a comparable model — converting *blind survival* to *intelligent failover*.

| Pattern | Chain | F2 impact |
|---------|-------|-----------|
| **Cliff (BAD)** | DeepSeek V4 Pro → Groq Llama 8B | Systemic hallucination on failover — truth breaks at step 2 |
| **Bridged (GOOD)** | DeepSeek V4 Pro → auto-beta → Groq Llama 8B | auto-beta finds comparable model, Groq is last resort only |

**Fallback position strategy:** Under W_scar, reliability and output fidelity beat millisecond savings. Position auto-beta as close to the primary as possible (Position 2). Do NOT bury it after the speed lane (Position 3+) — the complex prompt may never reach it.

### Active Hermes Fallback Chain (2026-07-30)

The live 11-tier Hermes chain in `/root/.hermes/config.yaml` — actual config, not reference pattern.

**Important:** The chain below is the `fallback_providers` array. The PRIMARY model lives outside this list at `model.default: deepseek-v4-flash` (direct DeepSeek via OpenCode Go). This chain activates when the primary fails.

```
PRIMARY:                    deepseek-v4-flash (OpenCode Go)   — conversational agent, $10/mo flat
                              ↓ fail?
Position 1 (REASONING):    tokenrouter/deepseek-v4-pro          (20s) — deep reasoning reserve
                              ↓ fail?
Position 2 (FAST TEXT):    mulerouter/qwen3-max                 (30s) ← NEW — fast text fallback
Position 3 (VISION):       mulerouter/qwen-vl-max               (30s) ← NEW — vision quality fallback
Position 4 (BRIDGE):       openrouter/auto-beta                 (60s) — capability-equivalent failover
Position 5 (SPEED):        groq/llama-3.1-8b-instant            (20s) — last resort only
Position 6:                sea-lion/Qwen-SEA-LION-v4-32B-IT     (20s)
Position 7:                gemini/gemini-2.5-flash              (20s) — Google free tier
Position 8:                tokenrouter/MiniMax-M3               (20s)
Position 9:                tokenrouter/z-ai/glm-5.2             (20s)
Position 10 (SURVIVAL):    openrouter/free                      (60s) — 50 RM0 models
Position 11 (LOCAL):       ollama/qwen2.5-coder:3b              (20s) — survival (needs upgrade to qwen3:8b)
```

**Changes from the previous 9-tier chain:**
- MuleRouter inserted at Positions 2 (qwen3-max) and 3 (qwen-vl-max) — fast text + vision before the smart router
- Every other entry bumped by 2 positions
- OpenRouter auto-beta now sits at Position 4 (was 2) — still the bridge but after MuleRouter opportunistic tier

**Note:** `qwen2.5-coder:3b` at Position 11 may fail — only `qwen2.5:3b` is pulled locally. Upgrade target: `qwen3:8b` or `deepseek-r1:7b` for meaningful local recovery.

### The Sovereignty Paradox (Arif, 2026-07-29)

OpenRouter as PRIMARY introduces a paradox: to make a smart-router safe for sovereign topics, you must constrain it via `allowed_models` to 1-2 approved model families (e.g., `["deepseek/*", "qwen/*"]`). But constraining the router this aggressively **defeats its purpose** — you're paying the latency tax (~200-500ms classification meta-round-trip) and proxy fee while getting no routing intelligence. You could make those calls directly with less latency and same cost.

**The arithmetic:**
```
Smart Router (constrained to 2 families):
  1. Classifier tax: +200-500ms TTFT
  2. allowed_models = ["deepseek/*", "qwen/*"]
  3. Model selected by community spend-share → constrained choice
  4. same outcome as direct call, slower

Direct call:
  1. No classifier tax
  2. model = deepseek/deepseek-v4-flash
  3. Zero proxy hop
  4. same outcome, faster
```

**Rule:** OpenRouter belongs at the **intelligent failover layer**, not at primary. Keep primary direct (DeepSeek V4 Flash). OpenRouter sits at Position 2 — it catches primary failure and routes to comparable models (Claude Sonnet, GPT-4o, etc.) that you don't have direct API keys for. This way:
- Your primary calls have zero routing overhead
- Your failover has maximum model variety
- Sovereign concerns never touch the proxy

### Standard Tier Pattern (Updated 2026-07-30 with MuleRouter)

```
Tier 1 (PRIMARY):              DeepSeek V4 Flash (OpenCode Go)               — conversational agent, tool calling, $10/mo flat
Tier 1.5 (REASONING RESERVE):  tokenrouter/DeepSeek V4 Pro                   — deep reasoning, reserved for complex multi-step
Tier 2 (MULEROUTER FAST):      mulerouter/qwen3-max                          — fast text fallback (1015ms, fixed pricing)
Tier 3 (MULEROUTER VISION):    mulerouter/qwen-vl-max                        — vision quality fallback (1883ms, URL-only)
Tier 4 (INTELLIGENT FAILOVER): openrouter/auto-beta                          — capability-equivalent failover to comparable model
Tier 5+ (COST/SPEED):          groq/llama-3.1-8b-instant, SEA-LION, Gemini  — hardcoded speed lanes
Tier N-1 (FREE SURVIVAL):      openrouter/free                               — 50 RM0 models, 20 req/min
Tier N (LOCAL):                ollama/qwen2.5-coder:3b (upgrade needed)      — last resort
HOLD:                          888_HOLD (F13 — never auto-resolve)
```

**Why MuleRouter sits before auto-beta:** OpenRouter's smart router is a classifier round-trip (+200-500ms TTFT). MuleRouter's qwen models respond instantly with no classifier overhead. If the primary fails, checking MuleRouter (2 calls: qwen3-max + qwen-vl-max) costs at most 60s total but succeeds for the common case (text). Auto-beta then catches anything MuleRouter can't handle.

### Flash vs Pro — Conversational Agent Decision (Arif, 2026-07-29)

DeepSeek V4 Flash is the **constitutional primary for conversational agents**. Not Pro. This decision was forged through live empirical testing, not theoretical model ranking.

| Dimension | Flash | Pro |
|---|---|---|
| **Conversation reliability** | ✅ 4/5 agent tasks pass | ❌ 2/5 — `content: null` on 3/5 tasks |
| **Tool calling** | ✅ Pass | ❌ Silent failure — returns `content: null` |
| **BM conversational** | ✅ Pass | ❌ Ghost response on BM natural tasks |
| **Cost/M tokens** | $0.14/$0.28 | $0.44/$0.87 |
| **Latency** | Fast | Slow — burns 69-100% tokens on internal reasoning |
| **Deep reasoning** | Limited | ✅ Best-in-class — but only usable when explicitly requested |

**Constitutional logic:** Pro returning `content: null` is a **direct threat to F1 AMANAH (Safety)** — it produces ghost responses that break the multi-agent chain (broken wire). A model that silently fails on tool calls cannot serve as a primary reasoning metabolizer in a system where F2 TRUTH and ΔS < 0 are hard constraints.

**Reserve logic:** Pro stays in the chain as a **reasoning reserve** (tokenrouter, Position 1.5). It is explicitly NOT the default — it must be either:
- Invoked by name for targeted deep reasoning (structured tasks, policy analysis, complex geology)
- Dropped onto when Flash fails on a genuinely complex prompt (tokenrouter retry)

**Pricing note:** Pro's $0.44/$0.87 is 3× Flash's $0.14/$0.28, making it an expensive default when Flash handles 80%+ of daily traffic adequately.

**Live Hermes fallback chain (2026-07-29):** See `references/hermes-live-fallback-chain-2026-07-29.md`.

For FLAME (tool lane): `Groq→SEA-LION→Gemini→Cerebras→OpenRouter/free→OpenCode→Ollama`

**`openrouter/free` details:** ~50 RM0 models, 20 requests/min limit. Routes to free-tier providers. Use only for FLAME tool tasks, never for constitutional work. Cheapest survival mode when credit is depleted.

## ZDR / Data Residency

| Data Class | ZDR Required | Mechanism |
|-----------|-------------|-----------|
| MY governance / PETRONAS / 1MDB | YES | Per-request `zdr: true` + route direct to DeepSeek, never OpenRouter |
| PII (myKad, phone, email) | YES | DLP guardrail + `zdr: true` |
| AAA constitutional content | YES | Workspace-level ZDR enforced |
| Public web fetches | NO | Standard routing OK |
| Free-tier tool tasks | NO | Standard routing OK |

**Closed allowlist for ZDR-safe models:** `z-ai/*, mistralai/*, x-ai/*, meta-llama/*, deepseek/*, qwen/*, xiaomi/*`

## Reasoning Control

Available on models routed through OpenRouter that support it:

```json
{"reasoning": {"effort": "high" | "medium" | "low" | "minimal"}}
```

Supported by: DeepSeek V4 Pro, Claude Sonnet 4.x, Kimi K2/K3, Inkling, Gemini 3.x Muse Spark.

**Critical caveat (Feb 2026 community audit):** Some models silently drop reasoning tokens when combined with structured output (`response_format`) or tool calling. Tested:
- **Kimi K2.5/K3:** Safest for universal reasoning with tools — maintains visibility
- **Claude Sonnet 4.x:** Opt-in reasoning, reliable when enabled
- **DeepSeek V4 Pro:** Reliable with tools, reasoning tokens preserved
- **GPT-5.x:** Reasoning transparency varies per sub-model
- **Rule:** Audit your specific model+structured+tool combo before relying on `reasoning_details` in the epistemic pipeline

## Structured Outputs

OpenRouter normalises JSON Schema enforcement across providers:

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "strict": true,
      "name": "my_schema",
      "schema": { ... }
    }
  }
}
```

Works across: OpenAI (GPT-5.x), Anthropic (Claude 4.x), DeepSeek (V4 Pro), and models proxied through OR's normalisation layer. Test each provider's strict schema compliance before relying on it for constitutional output.

## Session Stickiness + Prompt Caching

- Pass `x-session-id: aaa-hermes-<session_start>-<uuid>` on every OpenRouter request → pins model + provider for 5min inactivity. Expected: ~30% latency reduction.
- Add `cache_control: {"type": "ephemeral"}` to the last system message on Anthropic models → ~90% off input cost on repeat kernel loads. Hermes loads ~8K tokens of system prompts — that's ~92% saving on every cached call.
- Override provider routing per-request via `provider` object (`order`, `ignore`, `only`, `max_price`, `zdr`).

## Tools of the Trade

| Source of Truth | Path |
|----------------|------|
| AAA model registry | `/root/AAA/registries/models/AGENT_MODEL_MAP.json` |
| OpenRouter Zen doc | `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` |
| OpenRouter Agent Guide | `/root/AAA/docs/OPENROUTER_AGENT_GUIDE.md` |
| OpenRouter Hermes Ops | `/root/AAA/docs/OPENROUTER_HERMES_OPS.md` |
| Claude Code proxy routing (2026-08-01) | This skill's `references/claude-code-deepseek-proxy-routing.md` |
| OpenCode SOT pipeline (2026-07-24) | This skill's `references/opencode-sot-pipeline-2026-07-24.md` |
| Doc architecture pattern | This skill's `references/openrouter-doc-architecture.md` |
| Hermes live fallback chain (2026-07-29) | This skill's `references/hermes-live-fallback-chain-2026-07-29.md` |
| Model benchmark methodology | This skill's `references/model-benchmark-methodology.md` |\n| Benchmark test script (runnable) | This skill's `scripts/benchmark-agentic-model-test.py` |\n| Vision diagnostic script (runnable) | This skill's `scripts/vision-auxiliary-diagnostic.py` |\n| Multimodal routing architecture | This skill's `references/multimodal-router-architecture.md` |
| Wolf Cabinet Model (EUREKA 2026-07-30) | This skill's `references/wolf-cabinet-model-2026-07-30.md` |
| MuleRouter evaluation | This skill's `references/mulerouter-evaluation.md` |\n| MuleRouter integration transcript (2026-07-30) | This skill's `references/mulerouter-integration-2026-07-30.md` |\n| Qwen3-VL-30B evaluation | This skill's `references/qwen3-vl-30b-agentic-eval-2026-07-29.md` |
| Path B vision bypass source patch | This skill's `references/path-b-vision-bypass-source-patch-2026-07-29.md` |
| Session stickiness patch | This skill's `references/session-stickiness-source-patch.md` |
| Hermes config state snapshot | This skill's `references/hermes-openrouter-config-state-2026-07-24.md` |
| FLAME engine | `/root/A-FORGE/flame/` |
| LiteLLM federation gateway / FED FLAME FRAME (2026-08-02) | This skill's `references/litellm-federation-gateway-2026-08-02.md` |
| Qwen fallback chain live test (2026-08-02) | This skill's `references/qwen-fallback-live-test-2026-08-02.md` |
| **Unified routing audit — 3-layer accretion (2026-08-03)** | This skill's `references/unified-routing-audit-2026-08-03.md` |
| OpenCode config | `/root/HERMES/opencode.json` |
| Secrets | `/root/.secrets/vault.env` (OPENROUTER_API_KEY, OPENROUTER_MANAGEMENT_KEY) |
| Hermes config | `/root/HERMES/config.yaml` |

## Hermes Config Wiring

To add OpenRouter as a live Hermes provider (not just documented):

### Provider Definition

Add to `providers:` in `~/.hermes/config.yaml`:

```yaml
  openrouter:
    api: https://openrouter.ai/api/v1
    key_env: OPENROUTER_API_KEY
    models:
    - id: openrouter/auto-beta
      name: OpenRouter Auto-Beta (cost/quality task routing)
    - id: deepseek/deepseek-v4-flash
      name: DeepSeek V4 Flash (via OR)
    - id: deepseek/deepseek-v4-pro
      name: DeepSeek V4 Pro (via OR)
    - id: moonshotai/kimi-k3
      name: Kimi K3 (via OR)
    - id: google/gemini-3.5-flash
      name: Gemini 3.5 Flash (via OR)
    - id: meta/muse-spark-1.1
      name: Muse Spark 1.1 (via OR)
    - id: openai/gpt-5.6-sol
      name: GPT 5.6 Sol (via OR)
    name: OpenRouter (auto-failover, 343 models)
    transport: openai_chat
```

Use `hermes config set` — never hand-edit config.yaml:

```bash
hermes config set providers.openrouter.api https://openrouter.ai/api/v1
hermes config set providers.openrouter.key_env OPENROUTER_API_KEY
hermes config set providers.openrouter.transport openai_chat
hermes config set 'providers.openrouter.models[0].id' openrouter/auto-beta
hermes config set providers.openrouter.name "OpenRouter"
```

### Fallback Chain Insertion

Insert as Position 2 in `fallback_providers`:

```yaml
- model: openrouter/auto-beta
  provider: openrouter
  timeout: 60
```

**Important:** `hermes config set` does NOT handle arrays of objects reliably. Use Python YAML via `terminal()` or `execute_code()`:

```python
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
# Insert at position 2 (index 1)
cfg['fallback_providers'].insert(1, {
    'model': 'openrouter/auto-beta',
    'provider': 'openrouter',
    'timeout': 60
})
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
```

Run `hermes config check` after any config edit to verify integrity.

### CQT Per-Request Override (Hermes Agent)

When calling OpenRouter through auto-beta, pass the tradeoff via plugins:

```python
plugins=[{"id": "auto-router", "cost_quality_tradeoff": 5}]
```

### Ordering Reference

| Tier | Provider | Role | CQT |
|------|----------|------|-----|
| 1 | DeepSeek V4 Flash (direct) | Text-primary — conversational agent, tool calling | — |
| 2 | Qwen2.5-VL-72B (OpenRouter aux) | Vision side-car — PRMT transcript only (never primary) | — |
| 3 | openrouter/auto-beta | Smart failover — auto-failover, 70+ providers | 5 |
| 4 | openrouter/free | Survival — 50 RM0 models, 20 req/min | 10 |
| 5 | ollama/qwen2.5-coder:3b | Last resort — local | — |

## OpenClaw Cron Model Configuration

OpenClaw isolated-session cron jobs (`session: isolated`) use a **hardcoded fallback chain** when `model: -` (not set). This fallback lives in the cron job's `payload.fallbacks` and can contain stale/incorrect model names.

**Problem pattern:** When `model: -`, OpenClaw's isolated session tries an internal chain like `minimax/MiniMax-M3 → deepseek/deepseek-chat → ollama/qwen2.5:7b`. The model `deepseek/deepseek-chat` does NOT exist — correct DeepSeek IDs are `deepseek-v4-pro` and `deepseek-v4-flash`. The `ollama/qwen2.5:7b` model fails if Ollama provider is not configured. All three can fail → `FallbackSummaryError`.

**Fix — Pin model and clear broken fallbacks:**
```bash
openclaw cron edit <job-id> --model deepseek-v4-flash --clear-fallbacks
```

**Best practice:** Always set `--model` explicitly on OpenClaw cron jobs. Never rely on the default fallback chain — `deepseek/deepseek-chat` was correct in 2025 but no longer valid. After fixing, verify with:
```bash
openclaw cron show <job-id> | grep -E 'model:|fallbacks|last.*status'
```

## Vision Auxiliary: opencode-go Returns 403 for Images (probed 2026-07-29)

**`opencode-go` as `auxiliary.vision.provider` is BROKEN for all image input.** The OpenCode Go API at `opencode.ai/zen/go/v1/chat/completions` returns **HTTP 403 Forbidden** on any request containing `image_url` data (base64 or URL). This means:

- User sends an image → Hermes calls `opencode-go/kimi-k3` for vision analysis → **403** → vision returns error → main model (text-only) gets empty/null analysis → **hallucinates**
- This is NOT a model limitation — `kimi-k3` itself has vision capability. The issue is the proxy.
- OpenCode Go works fine for text-only requests. Only multimodal (image) payloads are blocked.

**Fix (applied 2026-07-29):** Change vision auxiliary from `opencode-go` to `openrouter`:

```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model moonshotai/kimi-k3
hermes config set auxiliary.vision.timeout 120
```

**Verification:**
```python
# Test vision via opencode-go (SHOULD FAIL: 403)
curl -X POST 'https://opencode.ai/zen/go/v1/chat/completions' \
  -H "Authorization: Bearer $OPENCODE_GO_API_KEY" \
  -d '{"model":"kimi-k3","messages":[{"role":"user","content":[{"type":"text","text":"color?"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}],"max_tokens":50}'
# → {"error":{"message":"Internal server error"}} or 403

# Test vision via openrouter (SHOULD WORK)
curl -X POST 'https://openrouter.ai/api/v1/chat/completions' \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{"model":"moonshotai/kimi-k3","messages":[{"role":"user","content":[{"type":"text","text":"color?"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}],"max_tokens":200}'
# → ✅ correct analysis, cost ~$0.0016/call
```

**Note on kimi-k3 vision output:** Kimi K3 via OpenRouter may return `content: null` with all text inside `reasoning` when `max_tokens` is too low. For vision tasks, set `max_tokens >= 200` and let `extract_content_or_reasoning(response)` in `vision_tools.py` handle extraction from reasoning field.

### Vision Auxiliary: kimi-k3 → qwen3-vl Swap (2026-07-29)

**Problem:** Kimi K3's always-on thinking mode (`content: null`) was unreliable even for vision tasks. Some calls returned empty vision analysis → text-only primary (Flash) hallucinated on image content.

**Fix (applied 2026-07-29):** Swapped vision auxiliary from `moonshotai/kimi-k3` to `qwen/qwen3-vl-30b-a3b-instruct`:

```bash
# Must use python3 yaml — hermes config set doesn't handle nested keys
python3 -c "
import yaml
cfg = yaml.safe_load(open('/root/.hermes/config.yaml'))
cfg['auxiliary']['vision']['model'] = 'qwen/qwen3-vl-30b-a3b-instruct'
yaml.dump(cfg, open('/root/.hermes/config.yaml','w'), default_flow_style=False, sort_keys=False)
"
```

**Why qwen3-vl:**
- Native vision, free via OpenRouter ($0)
- MoE 30B/3B active — fast inference (~770ms tool calls)
- No censorship issues for MY governance topics (Alibaba CN origin)
- No content=null bug — always returns clean vision descriptions
- 262K context window

**Note:** Kimi K3 remains usable for vision if explicitly invoked with proper `max_tokens >= 500`. It is no longer the default auxiliary vision model. The opencode-go 403 fix (switching provider to OpenRouter) is still valid as the transport layer — only the model changed.

### Vision Auxiliary: TokenRouter/OpenRouter Credit Exhaustion → MiniMax Direct (2026-07-30)

**Problem:** ASI bot (hermes_asi profile) received an image via Telegram and the fallback cascade completely failed:
1. DeepSeek direct (primary) — payload too large (image embedded as raw base64 in text context)
2. TokenRouter (deepseek-v4-pro) — **$-0.04 credit deficit** → 403
3. OpenRouter (auto-beta) — **$0 credits, only enough for 3,661 of 65,535 tokens** → 402
4. Groq (llama-3.1-8b-instant) — **6,000 TPM limit, requested 228,500 tokens** → 413
5. Compression (3 attempts from 54→48→45 messages) — still over 200K tokens → dead end

**Root cause:** The vision auxiliary pointed to `tokenrouter/MiniMax-M3` but TokenRouter had a negative balance. Worse, `image_input_mode: text` caused the image to be dumped as raw base64 directly into the main model's text context (no vision preprocessing), inflating the payload to 228K tokens.

**Fix (applied 2026-07-30):** Two config changes in the ASI profile (`/root/HERMES/profiles/hermes_asi/config.yaml`):

| Setting | Before | After |
|---|---|---|
| `image_input_mode` | `text` | `auto` |
| `auxiliary.vision.provider` | `tokenrouter` | `minimax` |
| `auxiliary.vision.model` | `MiniMax-M3` | `minimax-m3` |
| `auxiliary.vision.api_key` | `{env:TOKENROUTER_API_KEY}` | `{env:MINIMAX_API_KEY}` |

**Why MiniMax direct:**
- **Separate credit pool** — MiniMax Token Plan (~5.1B monthly tokens) is independent of OpenRouter/TokenRouter balances. No per-token billing — quota-based subscription.
- **MiniMax-M3 is natively multimodal** — accepts `image_url` content in standard OpenAI-compatible chat completions. 3s inference on 1280×720 JPEG, returned 200 with accurate description.
- **No credit-based throttling** — quota-based, not per-token billing.

**Critical: `image_input_mode: auto` is required.** When set to `text`, Hermes does NOT route the image through the vision auxiliary at all — it embeds raw base64 into the text context, which:
- Blows up token count (153KB JPEG → ~228K tokens of base64)
- Makes 413 errors worse
- Defeats the purpose of having a vision auxiliary

**Two distinct failure modes (do not conflate):**
1. **Vision auxiliary failure** — the model that describes the image (MiniMax, Qwen3-VL) fails → no image description → primary model hallucinates
2. **Compression auxiliary failure** — when context is large (50+ messages), compression tries to summarize using TokenRouter/OpenRouter → those fail on credits → context stays huge → 413 on Groq

The compression auxiliary (`auxiliary.compression`) still follows the main model chain. If TokenRouter and OpenRouter are both out of credits, compression will ALSO fail — this is a separate problem from vision routing.

**Gateway restart constraint:** After editing a profile's `config.yaml`, the gateway BLOCKS `systemctl restart` from within its own process (SIGTERM propagates to child processes). Workaround:
```bash
# From inside the gateway process:
nohup bash -c 'sleep 2 && systemctl restart hermes-asi-gateway' > /tmp/restart.log 2>&1 &
```

**Test verification (curl direct to MiniMax):**
```python
import requests, base64
b64 = base64.b64encode(open("/path/to/image.jpg","rb").read()).decode()
r = requests.post(
    "https://api.minimax.io/v1/chat/completions",
    headers={"Authorization": f"Bearer {MINIMAX_API_KEY}",
             "Content-Type": "application/json"},
    json={"model": "minimax-m3", "messages": [{"role":"user","content":[
        {"type":"text","text":"Describe this image"},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
    ]}], "max_tokens": 1000},
    timeout=30
)
```

**If OpenRouter/TokenRouter credits are restored later:** Revert `auxiliary.vision` back to OpenRouter if preferred (qwen3-vl is free via OpenRouter when credits exist). But MiniMax direct is the recommended default while the ASI chain has no credit balance — it is currently the ONLY path that works independently of credit top-ups.

## Pitfalls (expanded) — see also `references/` files in this skill

- **`hermes config set` can DESTROY the config file.** This tool does NOT merge YAML — it overwrites the entire top-level key. Setting `telegram.allowed_chats` via `hermes config set` flattened a 1334-line, 34KB `config.yaml` to 3 lines (PROVEN 2026-07-30, twice in one session). The setting was written, but everything else — model, providers, auxiliary, federation, skills, cron — was silently dropped. **Never use `hermes config set` on top-level sections that other config depends on.** Use Python yaml manipulation via `terminal()` for any non-trivial config edit. Also, `hermes config set model.provider <name>` truncates the `model:` block to just `provider:` and `default:` — all other model settings silently dropped.

```bash
python3 << 'PYEOF'
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
# Make your edit
cfg['telegram']['allowed_chats'].append('-1003815535761')
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
PYEOF
```

**Restoration procedure when config is flattened:**
1. Check `ls /root/.hermes/config.yaml*.bak` — Hermes auto-creates `.bak` files **only when the YAML is invalid**, not as routine backups. The naming pattern is `.corrupt.<timestamp>.bak` (not `.bak` alone). If the file is valid YAML but semantically wrong, no `.bak` is created.
2. Restore the most recent: `cp /root/.hermes/config.yaml.corrupt.<latest_ts>.bak /root/.hermes/config.yaml`
3. **Patch Python YAML only** for the fix — never use `hermes config set` again in the same session.
4. Only safe use of `hermes config set`: isolated single-value fields that no other config section depends on (`display.language`, `model.supports_vision: false`, `stt.enabled`). Never for arrays, lists, or top-level blocks.
5. **Always validate after any edit:** `python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/config.yaml')); print('OK')"`

**Config.yaml YAML corruption repair (PROVEN 2026-07-30):** Over time, config.yaml can accumulate orphan lines, duplicate provider entries, or malformed search blocks. To repair:
1. **Find orphan lines:** `tail -15 /root/.hermes/config.yaml` — look for list items without parent keys, dangling name/value pairs at wrong indentation.
2. **Detect duplicate provider entries:** `grep -n "^  <provider-name>:" /root/.hermes/config.yaml` — if two entries exist at same level, the second silently overwrites the first in YAML.
3. **Remove orphans:** `sed -i '<start>,<end>d'` with explicit line numbers from `grep -n`. Verify line count with `wc -l` before and after.
4. **Fix the `search:` block:** A common artifact — after removing orphans, `search:` may exist without `search_backend:`. Append: `echo '  search_backend: brave' >> /root/.hermes/config.yaml`.
5. **Validate:** `python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/config.yaml')); print('OK')"`
6. **Check no duplicate provider entries remain** by running a YAML key scan.

**Telegram group "not allowed" troubleshooting (PROVEN 2026-07-30):** When Hermes responds "This group is not allowed" in a Telegram group, the group's chat ID is missing from `allowed_chats` or `free_response_chats`. Procedure:
1. **Find the chat ID:** Check `/root/HERMES/logs/gateway.log` for inbound messages from that group — the `chat=<id>` field in the log line is the chat ID. The `channel_directory.json` also maps group names to IDs.
2. **Check `allowed_chats`:** `grep -A20 "^telegram:" /root/.hermes/config.yaml | grep allowed_chats -A15`
3. **Check `free_response_chats`:** The value is a YAML single-quoted string containing a serialized Python list with escaped single quotes (`''`). Each entry looks like `''-1003815535761''`.
4. **Add to `allowed_chats`:** Insert a new list item `- '-1003815535761'` in the YAML array.
5. **Add to `free_response_chats`:** The format is a YAML single-quoted string. Insert with proper escaping — replace `5444180135'']'` with `5444180135'',''-1003815535761'']'` (note: double single quotes for YAML escaping).
6. **Validate YAML:** `python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/config.yaml')); print('OK')"`
7. **Restart:** `hermes gateway restart`
8. **Confirm:** Check logs for zero "not allowed" warnings for that chat ID after restart.

- **Config.yaml edit guard blocks direct write_file/patch.** The Hermes agent refuses `write_file()` and `patch()` on `/root/.hermes/config.yaml`. Must route through `terminal()` with Python yaml manipulation. This is intentional — prevents agent-side corruption. Always use the terminal-based Python yaml pattern above.

- **`image_input_mode` duplicate declaration causes silent override (PROVEN 2026-07-30b).** Having `image_input_mode` in BOTH the `model:` block AND at the root level of config.yaml causes the root-level value to be silently ignored (Python YAML dict merge behavior). The `model:` block value wins. If `model:` block has `image_input_mode: auto` and root has `image_input_mode: text`, the effective mode is `auto` — images are NOT enriched via vision auxiliary and raw bytes hit the main model → 413. **Fix:** `grep -n \"image_input_mode\" /root/.hermes/config.yaml` — ensure exactly ONE occurrence at the root level (indentation 0). Remove any inside the `model:` block.** `hermes gateway start/restart` runs a user service that picks up env from the current shell. `systemctl restart hermes-asi-gateway.service` runs the systemd unit which sources `/root/AAA/agents/hermes-asi/runtime/.env` via `/usr/local/bin/hermes-gateway-secure.sh`. These have DIFFERENT env vars, DIFFERENT bot tokens, and DIFFERENT failure modes. The systemd unit unsets `OPENAI_BASE_URL` to prevent routing poisoning. **Rule:** Always use `systemctl restart hermes-asi-gateway.service` for ASI bot changes. `hermes gateway start` is only for testing. Running both simultaneously creates competing gateway instances that fight over Telegram polling.** When `model.provider` is changed (e.g. from `opencode-go` to `mulerouter`), `auxiliary.vision.provider` MUST be aligned to the same provider family. If they diverge — primary on MuleRouter, auxiliary on OpenRouter — the auxiliary enrichment can fail on a different failure domain (balance, rate limit, network). When it fails, raw image bytes are forwarded to the text-only primary model → 413 Payload Too Large → cascade through all text-only fallbacks. **Fix:** Always change auxiliary.vision.provider to match model.provider when switching primary. The enrichment and the primary must share the same failure domain.

A previous session reported MuleRouter rejects `data:` URIs, but this was NOT re-tested in the session where the 413 cascade occurred. The 413 there was caused by a **provider mismatch** (auxiliary.vision still on OpenRouter while primary was MuleRouter), not by MuleRouter rejecting base64. **Test MuleRouter with a base64 image directly before assuming it fails** — if it works, it eliminates the last gap in the satu-roof vision story.

- **Doc search is NOT evidence — probe the API.** When evaluating a new provider, always call `/v1/models` to get the actual model list. On 2026-07-30, searching MuleRouter's docs returned ZERO hits for "DeepSeek" — leading to a false negative claim. The API returned 31 models including deepseek-v4-flash and deepseek-v4-pro. Commercial aggregators update faster than their docs. API response is evidence; doc search is not.

- **DeepSeek V4 Flash is text-only — no native vision (probed 2026-07-29).** When users send images in Telegram, Hermes vision pipeline creates an [IMAGE TRANSCRIPT] via an auxiliary model. Flash reads this transcript and confidently fills in gaps — causing hallucination on image-dependent tasks. Arif reports: "Flash always hallucinate when I share any image input." This is NOT a Flash bug; it's a text-only model limitation. Fix: use a vision-native primary model (Qwen3-VL-30B-A3B) so images are seen directly.

- **Three-tapisan model (forged 2026-07-24):** OpenRouter CAN serve as Hermes's intelligence layer, but 3 hard filters apply:
  1. **Identity-sensitive ops NEVER route through OR** — 000_INIT, 666_JUDGE, 999_SEAL, MY governance (Najib, 1MDB, PETRONAS, myKad), and MiniMax (SHADOW-MM-001) must go direct to DeepSeek. Auto-router has `identity_verified: false`.
  2. **Session can't switch provider mid-stream** — model/provider fixed at session start. Must restart gateway + new session to change routing. Hermes runtime constraint.
  3. **Cost awareness** — auto-beta defaults CQT=9 (cheap), but can pick expensive models (Claude, R1) on certain tasks. Monitor credit balance ($30.00 as of 2026-07-24, org arifOS).

- **Auto-router for JUDGE/SEAL.** Never. OpenRouter has `identity_verified: false` — it cannot authenticate a constitutional verdict. F1 AMANAH + F13 SOVEREIGN.
- **Auto-router for 000_INIT.** Never. Identity binding needs sovereign direct — OpenRouter abstracts the provider, so the init binding is to a proxy, not the actual model.
- **Auto-router for MY governance.** The router selects by community spend share, which can pick a censored model (MiniMax M3 has **SHADOW-MM-001** — silent MY governance censorship on Najib, 1MDB, PETRONAS, myKad). Always route sovereign topics direct to DeepSeek. **Never route MiniMax models through auto-beta** — they must be explicitly excluded in `allowed_models` if auto-beta is used at all on these topics.
- **Reasoning drops with tools.** Some models (GPT-5.x, certain Claude variants) silently suppress reasoning tokens when `response_format` or tool_calling is active. Kimi K2.5 is the safest for reasoning visibility with tool use. Audit your specific combo.
- **Kimi K3 always-on thinking breaks agentic workflows (probed 2026-07-29).** Kimi K3's forced thinking mode dumps ALL output into `reasoning_content` and leaves `content` as `null`. Tool calls still work (correct `tool_calls` in response), but the final response after tool execution is invisible — Hermes sees `content: null` and can't deliver a message to the user. **This is a dealbreaker for conversational agents.** K2.5 does not have this issue. Workaround: set `include_reasoning: true` and fall back to `reasoning_content` as content, but this requires runtime patching. For now, Kimi K3 is only suitable for vision tasks (where content is an image, not text) — never as a primary conversational model.
- **DeepSeek V4 Pro reasoning overhead (probed 2026-07-29).** Even with `reasoning: {effort: "low"}`, Pro burns 69-100% of completion tokens on internal reasoning, leaving `content: null` on 3/5 general agent tasks (BM natural, tool use, reasoning). This makes it unreliable as a primary conversational model — it will silently fail on tool calls and BM conversations. Use Pro only for targeted deep reasoning with `max_tokens >= 1000` and `reasoning: {effort: "high"}`. For general agent tasks, DeepSeek V4 Flash is more reliable (4/5 passed vs Pro's 2/5). Full 5-dimension benchmark and methodology: `references/model-benchmark-methodology.md`.
- **Assume cascade matches SOT.** The AGENT_MODEL_MAP is the canonical cascade. This skill documents the *proposed* optimised chain. Verify with `curl -s http://localhost:8088/health | jq .cascade` before assuming.
- **No session_id.** OpenRouter's auto-beta loses session stickiness without it — every call goes through the classifier again, losing 30% latency.
- **No cache breakpoint.** Long system prompts (Hermes ~8K, constitutional kernel ~15K) are ~90% wasted on repeat without `cache_control`.
- **FLAME and agent lanes cross.** Tool output must never enter the governed cascade. Agent output must never route through FLAME. Separate lanes, separate concerns.
- **OpenRouter MCP OAuth.** The MCP server at `mcp.openrouter.ai/mcp` needs one-time OAuth approval with the management key. Not approved = no live model discovery.
- **openrouter/auto is deprecated.** It was powered by NotDiamond and has been replaced by `openrouter/auto-beta`. Never reference `openrouter/auto` in new config.
- **vault.env keys wrapped in double quotes.** `export KEY="sk-or-v1-..."` means `cut -d= -f2` captures the quotes. Always strip: `tr -d '"'`. Without stripping, `curl` sends `Bearer "sk-or-v1-..."` (with literal quotes) → 401 Missing Authentication header. This affects all vault.env keys extracted via shell, not just OpenRouter.
- **Ghost tool causes OpenRouter Auto Exacto to fail with "No endpoints found that support tool use".** When an agent declares a tool in its available tool list (system prompt tool registration, opencode_toolbench.yaml, etc.) but there is NO MCP endpoint backing it at runtime, OpenRouter's Auto Exacto (tool-call routing layer) attempts to find a provider supporting tools for the model — but the ghost tool itself is unresolvable because no server handles it. This produces a misleading error that looks like a provider availability issue when it's actually a tool registration defect. **Fix:** Remove the ghost tool from tool registration (`plugin_tools: []` in `opencode_toolbench.yaml`) or implement the MCP server. Check: `grep -r 'aaa_measure' /root/AAA/registries/ /root/AAA/agents/opencode/`. Real example: `aaa_measure` was declared as a plugin tool but had no MCP endpoint at `:3001/mcp` — removing it from `opencode_toolbench.yaml` resolved the OpenRouter routing error immediately.

- **extra_body on fallback entries.** Hermes fallback_providers[] only reads model/provider/timeout. Any plugins, extra_body, or provider routing overrides are silently ignored. Enforce OR policy via Management API guardrails instead.
- **`hermes config set model.provider` TRUNCATES the model block.** Running `hermes config set model.provider <name>` replaces the ENTIRE `model:` YAML block with just `provider` and `default`. All other model settings (`supports_vision`, `request_timeout`, `context_length`, `max_tokens`, `timeout`) are silently dropped. The command does NOT merge — it overwrites. Workaround: use `sed -i 's|provider: old|provider: new|'` on `/root/.hermes/config.yaml` instead, restoring the truncated fields from the auto-created `.bak` file.

- **Config.yaml edit guard.** The Hermes agent BLOCKS direct write_file/patch on `/root/.hermes/config.yaml` with `Refusing to write to Hermes config file`. To modify it, must use `terminal()` with python3 yaml manipulation or direct `hermes config set` CLI. Always route config changes through `hermes config set` or a terminal-based python3 script, never through write_file/patch tools.
- **MCP OAuth requires `auth: oauth` in server config.** Registering an MCP server with just `url` and `transport` is not enough if the server requires OAuth. The entry must explicitly include `auth: oauth` in the mcp_servers config, or `--auth oauth` on `hermes mcp add`. Without it, `hermes mcp login <name>` won't trigger the OAuth flow. Add via config: `mcp_servers.<name>.auth: oauth`.
- **MCP OAuth in headless/remote environments.** `hermes mcp login <name>` opens a browser via system TTY. On a VPS with no display, the SDK prints the authorization URL and falls back to stdin — paste the full redirect URL (or `?code=...&state=...`) and press Enter. The redirect MUST point to the local callback server port shown in the URL. From the user's remote browser, opening `http://127.0.0.1:<port>/callback` won't reach the VPS — instead paste the redirect URL into the waiting stdin. Use `process(action='submit')` to send the redirect URL string (including the full `http://127.0.0.1:<port>/callback?code=...&state=...` URL) to the background login process.
- **searxng/.env is a symlink, not a separate file.** `/root/searxng/.env -> /root/.secrets/vault.env`. Chmod on a symlink only affects the symlink (always 777 by POSIX), not the target (600 root:root — correct). Updating vault.env auto-updates searxng/.env — no separate patch. mtime on the symlink reflects symlink creation, not vault.env modification. Do NOT flag 777 on searxng/.env as a security regression.
- **OpenRouter management key rotation.** Once a key is exposed in conversation, rotate at openrouter.ai/keys. Management API at `openrouter.ai/api/v1/keys` (NOT `/admin/keys`). Full 3-loop audit procedure:
  1. **Loop 1 — Scan all surfaces:** `grep -r 'OPENROUTER_API_KEY\|sk-or-'` across vault.env, searxng/.env, all .bak files, Docker env vars, agent configs. Check running Docker containers with `docker exec <name> env | grep OPENROUTER`.
  2. **Loop 2 — Update vault + containers:** Use Python to write full 73-char keys to vault.env (sed corrupts quoting). vault.env stores truncated placeholders (`sk-or-...8db4`) — the `...` is literal. Always verify the new key has credits with `curl /api/v1/auth/key` — Management API sub-keys are free-tier by default.
  3. **Loop 3 — Test all surfaces:** auth test + model call test for each. Verify MCP endpoints that inject the key. Only then disable old key with `DELETE /api/v1/keys/:hash`.
  - **Management API key list:** `GET /api/v1/keys` returns array of `{hash, name, label, disabled, limit, usage, is_free_tier, workspace_id}`.
  - **Create key:** `POST /api/v1/keys {"name":"<name>"}`. Response truncates the key value — full key only shown once in UI.
  - **Verify key:** `GET /api/v1/auth/key` returns label, management status, free tier, usage, rate limits.
  - **Credits check:** `GET /api/v1/credits` returns `{total_credits, total_usage}`. Always verify before deploying a rotated key.
  - **vault.env has literal `...` in placeholder values.** When replacing, use Python regex or write the full value. The length check must match: real OpenRouter keys are 97 chars (`sk-or-v1-` prefix + 90 hex chars). Earlier reports of 73 chars were counting redacted display values; verify with `${#KEY}` in shell.
- **Sub-key has $0 credits by default.** Management API sub-keys do NOT automatically inherit the main API key's prepaid credit balance. Always verify a new sub-key with `curl /api/v1/auth/key` before deploying. If it returns `is_free_tier: true, usage: 0, total_credits: 0` but 402 on model calls, the key exists on a workspace with no spend authority. Top up at openrouter.ai/settings/credits or use `openrouter/free` for RM0 survival.
- **Personal vs Org workspace credits are isolated.** OpenRouter has two account tiers: Personal (regular API keys, shared credit pool) and Organization (sub-keys under management keys, per-workspace billing). Credits topupped on a Personal account do NOT apply to an Org workspace's sub-keys — they're separate `workspace_id`s. Always verify with `curl /api/v1/credits` on the active workspace before deploying.
- **Old management key persists after creating a new one.** `POST /api/v1/keys` to create a management key does NOT deactivate the old one. The old key remains live with full authority until manually disabled at openrouter.ai/keys. There is NO API endpoint to revoke management keys — only the web UI. Sub-keys can be deleted programmatically: `DELETE /api/v1/keys/:hash` → `{"deleted":true}`.
- **`/admin/keys` returns a 404 HTML page, not JSON.** The correct Management API endpoint is `GET /api/v1/keys` (sub-keys, requires management key Bearer auth), NOT `/admin/keys` which renders an OpenRouter web page.\n- **Key rotation scope-creep trap.** When rotating keys: verify the new key works (auth test + model call), update vault.env, confirm deployment picks it up, then **stop**. Do NOT chase downstream optimizations, audit third-party integrations, or start provisioning guardrails in the same cycle. Each downstream fix belongs in its own task loop. Arif will signal with "bodoh x payah la rotate buat semak kacau bilau. Apa yang ada guna ja" when you've over-scoped. The correct pattern: 3 loops only (scan/update/verify), declare done, surface remaining items as separate follow-ups.\n- **YAML list patching doubles entries.** When using `hermes config set` or python yaml to modify `fallback_providers`, the operation can create duplicates if the same model lands at multiple indices or old entries aren't removed first. Always verify with `hermes fallback list` after a change and run a dedup step if needed.

- **Provisioned-but-empty seats read as literal `PASTE_*` placeholders (PROVEN 2026-08-01).** When a QwenCloud Team seat is created in the console but the key is never pasted into the vault, kunci-mas.env holds a literal `PASTE_HERMES_...` / `PASTE_PRO_SEA...` / `PASTE_INDIVID...` value. Every config reference to that env var then returns `InvalidApiKey` (401) — and if all fallbacks ride that same provider, the whole chain dies at once. **Detection:** `grep -E '^(export )?QWEN' /root/.secrets/kunci-mas.env | sed -E 's/=(.{14}).*/=\1.../'` — any `PASTE_*` value is an empty seat. **Real keys often already exist under legacy names** (`QWEN_API_KEY` = Pro, `QWEN_BAILIAN_KEY` = Standard) — copy them into the seat-named vars rather than waiting for rotation. Probe first: `curl -s -m 15 https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/models -H "Authorization: Bearer $KEY"` — `{"data":[...]}` = alive, `InvalidApiKey` = dead/placeholder. Full recipe: `references/qwen-token-plan-seat-wiring.md` under the `tokenrouter-guide` skill.

- **Fallback-chain theatre — a chain whose entries all ride one provider/key diversifies nothing (PROVEN 2026-08-01).** A `fallback_providers` list with 5 entries all on `provider: qwen-token-plan` is not a fallback chain — one dead key 401s every entry identically. Real resilience requires ≥2 independent providers with independent keys (e.g. qwen-token-plan → mulerouter → ollama). Audit rule: count distinct providers (and distinct key_env vars) in the chain; if it's 1, it's theatre.

- **`hermes config set` stores JSON list values as literal quoted STRINGS (PROVEN 2026-08-01).** `hermes config set fallback_providers '[{...json...}]'` writes `fallback_providers: '[{...}]'` — a quoted string, not a YAML list — and the runtime fails iterating it. `set_config_value` only coerces scalars (bool/int/float); `_set_nested` refuses to grow lists. **Fix:** for list-valued keys, edit config.yaml directly with a python yaml round-trip then validate with `yaml.safe_load`. Scalars (`model.provider`, `model.default`) work fine via the CLI. (The `patch`/`write_file` tools refuse Hermes config.yaml by design — terminal+python is the sanctioned path.)

- **Broken-fallback retry death spiral → fragmented Telegram responses (PROVEN 2026-08-02).** When `fallback_providers` is a quoted string (not a list), the runtime has NO valid fallback. Every retry hits the same primary, which keeps failing. The agent's internal model-switching status messages (`qwen3.6-flash · 52%`, `deepseek-v4-pro · 7%`) leak into the chat because the agent loop can't complete normally. **Symptom:** User sees multiple rate-limit messages, model names with percentages, and fragmented responses. **Diagnostic:** `python3 -c "import yaml; cfg=yaml.safe_load(open('/root/.hermes/config.yaml')); print(type(cfg.get('fallback_providers')).__name__)"` — if it prints `str` instead of `list`, the fallback chain is dead. **Fix script:** `scripts/diagnose-fallback-chain.py` — runs full provider diversity, key independence, and string-bug detection across both default and ASI profiles.

- **Individual Pro "Allocated quota exceeded" is NOT rate limiting — it's quota exhaustion (PROVEN 2026-08-02).** The Individual Pro seat (`QWEN_INDIVIDUAL_API_KEY`, `sk-sp-H.DIIYD`) has 5h+7d rolling windows, NOT monthly credits. When the window exhausts, the API returns `HTTP 429: Allocated quota exceeded, please increase your quota limit` — the same HTTP status as rate limiting but a completely different root cause. **Distinction:** Team seats return `429` for rate limiting (temporary); Individual Pro returns `429` for quota exhaustion (until window resets). **Detection:** Check the error body — `"code": "insufficient_quota"` = Individual Pro window exhausted; `"code": "Throttling.RateQuota"` = Team seat rate limited. **Fix:** Never use Individual Pro as the primary for an agent backend — it violates ToS §1 ("no automated scripts, application backends") AND has unpredictable rolling-window exhaustion. Use Team seats for agents, Individual Pro for multimodal only (TTS, image gen, vision).

- **OpenClaw background polling silently drains Qwen quota (PROVEN 2026-08-02).** OpenClaw cron jobs that use `bailian-token-plan` or `qwen-token-plan` as their model provider poll in the background, consuming quota from the shared Team seat without any visible user-facing activity. If OpenClaw shares a key with Hermes or LiteLLM, the first sign of trouble is Hermes returning 429 with no obvious cause. **Detection:** Check OpenClaw cron model assignments: `grep -r 'qwen\\|token-plan\\|bailian' /root/HERMES/profiles/hermes_asi/cron/`. **Fix:** Pin OpenClaw cron to an independent provider (MiniMax, Groq, Ollama) or its own dedicated seat. Never let OpenClaw share a key with the primary chat agent.

- **OpenClaw config uses `${QWEN_API_KEY}` by default — same key as Hermes primary (PROVEN 2026-08-02).** OpenClaw's `bailian` provider in `/root/.openclaw/workspace/hermes-config/config.yaml` references `${QWEN_API_KEY}` which resolves to KEY A (Team Pro) — the same key Hermes uses as primary. Every OpenClaw agent process (vision, image_gen, delegation, chat) silently eats from the shared pool. **Fix:** Change all `${QWEN_API_KEY}` references in OpenClaw config to `${QWEN_OPENCLAW_API_KEY}` (KEY D, workspace, 153 models, separate dashscope-intl endpoint). Python yaml round-trip across the file. Restart OpenClaw gateway after change.

- **Hermes cron jobs pinned to dead provider silently fail with 401 while burning quota (PROVEN 2026-08-02).** Cron jobs created with `--provider deepseek --model deepseek-v4-pro` keep that pin forever. When the DeepSeek API key expires or is revoked, every scheduled run fails with `HTTP 401: Invalid API-key` — but the job keeps retrying, burning quota on the dead endpoint. **Detection:** `hermes cron list` — look for `error: RuntimeError: HTTP 401` in the Last run column. **Fix recipe:** (1) Identify all 401 jobs: `hermes cron list | grep 'HTTP 401' -B5`. (2) Pause them all: `hermes cron pause <id>`. (3) Rewire each to `qwen-token-plan`: `hermes cron update <id> --model deepseek-v4-pro --provider qwen-token-plan`. (4) Resume: `hermes cron resume <id>`. (5) Verify next run succeeds. **Prevention:** When creating cron jobs, prefer `--provider qwen-token-plan` (the federation primary with its own fallback chain) over single-provider keys. Single-provider keys die silently; federation primaries have fallback chains.

- **Compression provider MUST be independent from primary (PROVEN 2026-08-02).** When `auxiliary.compression.provider` is set to the same provider as the primary (e.g., both `qwen-token-plan`), a rate limit on the primary ALSO kills compression. The cascade: (1) primary rate-limits, (2) Hermes tries to compress context before falling back, (3) compression uses the same rate-limited provider → fails, (4) context stays at full size, (5) fallback drops to smaller models (groq 128K, ollama 32K), (6) context exceeds their limits → `BadRequestError` / `context length exceeded`. **Symptom:** `Context compression failed after 3 attempts` followed by `BadRequestError` on groq/ollama. **Fix:** Set `auxiliary.compression.provider` to an independent provider with a large context window (e.g., `minimax` with `minimax-m3` at 1M ctx). The compression provider must have: (a) a different key from the primary, (b) a different API endpoint from the primary, (c) ≥1M context window to handle large conversations. **Config:** `cfg['auxiliary']['compression'] = {'provider': 'minimax', 'model': 'minimax-m3', 'timeout': 120}`. **Verification:** After setting, test that compression works when the primary is down: `curl -s -m 15 https://api.minimax.io/v1/chat/completions -H "Authorization: Bearer $MINIMAX_API_KEY" -d '{"model":"minimax-m3","messages":[{"role":"user","content":"Summarize: ..."}],"max_tokens":200}'`.

- **Context cliff in fallback chain — smaller models can't handle large context (PROVEN 2026-08-02).** When fallback models have progressively smaller context limits, a conversation that works on the primary (1M ctx) will fail on smaller fallback models (groq 128K, ollama 32K). This is a separate failure mode from rate limiting — the API call succeeds but returns `BadRequestError` because the payload exceeds the model's max context. **Rule:** Compression must succeed BEFORE the chain reaches the first small-context model. If compression is also failing (see above), the context cliff is guaranteed. **Mitigation:** (1) Independent compression provider, (2) `model.context_length` set to match the SMALLEST cloud fallback model (e.g., 256K to match groq's 128K with some headroom), (3) `compression.threshold` lowered (0.25 instead of 0.30) to trigger earlier. **Context limits of common models:** deepseek-v4-pro 1M, qwen3.6-flash 1M, minimax-m3 1M, llama-3.1-8b-instant 128K, qwen2.5:3b 32K. **Do NOT** put a 32K model after a 1M model without compression in between.

- **Live-probe every fallback entry — never assume (PROVEN 2026-08-02).** What the config says and what the API returns are often different. In this session: MuleRouter had negative balance (-0.75), OpenRouter had $0 credits, Gemini was removed by the user, Ollama had `qwen2.5:3b` not `qwen2.5-coder:3b`. 2 of 6 entries were dead. **Procedure:** For each entry in the fallback chain, run a 1-token chat completion with a 15s timeout. `curl -s -m 15 -X POST <base_url>/chat/completions -H "Authorization: Bearer $KEY" -d '{"model":"<model>","messages":[{"role":"user","content":"Say OK"}],"max_tokens":5}'`. Check for `choices` in response = alive; `error` = dead. **Do this EVERY time you audit a fallback chain.** The skill's `scripts/diagnose-fallback-chain.py` now includes live probes. Run it: `python3 /root/.hermes/skills/devops/provider-routing-zen/scripts/diagnose-fallback-chain.py --live`.

- **Three-layer routing accretion — FLAME → LiteLLM → FED, bukan reka bentuk (PROVEN 2026-08-03).** Tiga lapisan routing wujud secara akresi, bukan dirancang: (1) FLAME (:18901) — dibina dulu untuk free-tier Groq aggregation, (2) LiteLLM (:4000) — dibina kemudian sebagai proxy tempatan, (3) FED Router (:7074) — dibina paling baru dengan balance tracking + latency telemetry. Setiap lapisan ada fallback chain sendiri — tiga tempat nak debug bila gagal, tiga config nak maintain. **Dead finding:** `flame-api.service` dalam auto-restart loop (exit code 1) — FLAME engine hidup tapi API mati. Ini bermakna semua LiteLLM fallback path ke FLAME (`flame-free`, `gemini-*`) adalah jalan mati tanpa visible error. **Unified target:** Satu routing plane — FED sebagai intelligence layer, semua provider (Qwen TP, MiniMax, DeepSeek, Groq) direct tanpa proxy perantaraan. Buang LiteLLM dan FLAME (simpan 368MB RAM, 3 config jadi 1). **Migration doctrine:** Canary — wire Groq direct → 24h test → stop dead services → bersihkan config → 48h observation → seal. Full audit: `references/unified-routing-audit-2026-08-03.md`.

- **Missing `capabilities` field causes tool-call JSON text dump (PROVEN 2026-08-01).** When a Hermes provider doesn't declare `capabilities: [function_calling]`, Hermes does NOT send the `tools` parameter in the API request. The model has no structured tool-call interface, so it tries to "use tools" by outputting raw JSON like `{"name": "web_extract", "arguments": {...}}` as plain text in the reply. **Symptom:** User sees JSON tool-call syntax dumped in chat, model responds with apologies or "How can I assist?" after the JSON. **Fix:** Add capabilities to the provider block:
```yaml
  opencode-go:
    ...
    capabilities:
      - chat
      - function_calling
      - reasoning
```
**How to add safely:** Use `sed` to insert after `transport:` line — do NOT use `hermes config set` (it wipes the entire provider block).
```bash
cd ~/.hermes && sed -i '/^  opencode-go:/,/^  [a-z]/ {
  /transport: openai_chat/a\    capabilities:\n      - chat\n      - function_calling\n      - reasoning
}' config.yaml
python3 -c "import yaml; yaml.safe_load(open('config.yaml')); print('YAML valid')"
```
**Verification:** After restart, the model should use structured tool calls (invisible to user) instead of dumping JSON text. Compare with a provider that already has capabilities declared (e.g., `tokenrouter` has `capabilities: [chat, function_calling, reasoning]`).

- **`hermes config set providers.<name>.<field>` wipes the entire provider block (PROVEN 2026-08-01).** Running `hermes config set providers.opencode-go.capabilities '["chat"]'` replaced the ENTIRE opencode-go block (name, api, key_env, transport, primary, models list — all gone) with just `capabilities: '["chat"]'`. This is the same destruction pattern as `hermes config set model.provider` wiping the model block. **Recovery:** If config is git-tracked, `cd ~/.hermes && git checkout <commit> -- config.yaml`. Then use `sed` or Python yaml for the edit. **Rule:** `hermes config set` is ONLY safe for isolated leaf values that no other config depends on.

- **Python yaml round-trip SILENTLY STRIPS ALL COMMENTS from config.yaml (PROVEN 2026-08-03).** `yaml.safe_load` + `yaml.dump` preserves every value but drops every `#` comment line — config.yaml went from 1,406 lines / 21 comments to 1,386 lines / 0 comments with a semantically-identical diff. Comments in this config are human notes (seat labels, warnings, provenance) — losing them is real damage even though nothing "breaks." **Detection:** after any round-trip, compare `grep -c '^\s*#'` before vs after. **Mitigations, in order:** (1) prefer targeted `sed` for value swaps; (2) if you must round-trip, take a `.bak` first and restore it if the edit turns out to be a no-op; (3) for comment-preserving bulk edits use `ruamel.yaml` round-trip mode if available. (Session 2026-08-03: restored from backup after discovering the migration had already been applied — see next pitfall.)

- **Verify-before-mutate: another agent may have already applied the migration (PROVEN 2026-08-03).** Flagged 5 stale `qwen3.8-max-preview` refs at 20:35; by 20:56 a parallel agent (333-AGI, per AGENT_MODEL_MAP ingest notes) had already migrated all of them. The migration script then correctly reported `CHANGED 0` — but the yaml round-trip still rewrote the file (stripping comments, see above). **Rule:** before ANY config migration, re-grep for the target string immediately before writing. If zero matches remain, the work is done — do NOT write, do NOT round-trip; verify and report only. Multi-agent federation means config is a shared mutable surface; a no-op write is still a mutation (comments, mtime, ordering). Also cross-check registry `last_ingested` / `probed_by` fields for signs another agent already acted.

- **Registry entries can be FORWARD-DATED — probe > registry > docs (PROVEN 2026-08-03).** AGENT_MODEL_MAP.json carried a `qwen3.8-max` GA record dated 2026-08-05 (two days in the future) with `probed_by` citing an announcement email, while live probes on 2026-08-03 showed BOTH `qwen3.8-max` and the "retired" `qwen3.8-max-preview` serving fine. Registry dates are claims, not observations. For retirement/rollover decisions (preview→GA model-ID swaps), confirm with a live 1-token probe per ID before declaring anything dead: `scripts/tokenplan-model-probe.py`.

- **qwen3.8-max native base64 vision (PROVEN 2026-08-03).** Generated a solid-red PNG in pure stdlib, sent as `data:image/png;base64,...` image_url to `qwen3.8-max` on the Token Plan endpoint → HTTP 200, correct answer "Red" in 6.3s. Extends the MuleRouter base64 correction: the PRIMARY model now sees base64 images natively, so the PRMT transcript path is optional whenever qwen3.8-max is primary (no broken-telephone vision hallucination). Reusable probe for text liveness + base64 vision + latency on any Token Plan model ID: `scripts/tokenplan-model-probe.py`.
