# PRMT — Pre-Routing Modality Translation

## What It Is

PRMT (Pre-Routing Modality Translation) is the architectural pattern Hermes uses for multimodal inputs. Instead of routing to a different model based on input modality (Pattern A) or extracting signals to make a policy decision (Pattern B), PRMT translates the modality into text *before* the primary reasoning model ever sees it.

```
[Image] → Qwen2.5-VL-72B → text transcript → DeepSeek V4 Flash (same primary)
                                                                   ↓
                                                            Claude / Gemini /
                                                            GPT / anyone
```

## Why the Standard Taxonomies Don't Describe It

The multimodal routing literature (2025-2026) defines two dominant patterns:

### Pattern A: Model Swap

Detect modality → swap the *primary model* to one that handles it.

| Action | Example |
|---|---|
| Image present | Swap to VLM (Qwen-VL, Claude Sonnet 4, GPT-5-vision) |
| Pure text reasoning | Swap to frontier LLM |
| Chit-chat text | Swap to cheap small LLM |

**Systems:** NVIDIA LLM Router v2, RouteLLM (ICLR 2025), MMR-Bench, OpenRouter auto-beta

**Failure mode:** If the swapped-to VLM is down, *every text-only fallback crashes* because image bytes are in context (413 "request too large"). This was Hermes' Path B — reverted 2026-07-30.

### Pattern B: Signal-Decision Fabric

Extract *signals* from the request (not content) → compose with boolean logic → decide action.

| Signal | Source | Used For |
|---|---|---|
| Embedding similarity (text) | Text encoder | Domain classification |
| Embedding similarity (image) | CLIP/SigLIP | Image relevance |
| PII/jailbreak detectors | Specialized models | Block/redact |
| Text intent | Small LLM (Qwen 1.7B) | Task classification |

Decision example: `IF (image_present AND PII_detected) → route_to_restricted_handler`

**Systems:** vLLM Semantic Router (VSR), NVIDIA v2 intent-based routing

**Failure mode:** Requires reference parity between training and deployed encoders. VSR discovered their deployed Rust/Candle path was 82% anti-correlated with PyTorch reference (wrong pooling, normalization, resize).

### PRMT: Where Hermes Sits

PRMT doesn't fit either pattern:

| Dimension | Pattern A | Pattern B | PRMT (Hermes) |
|---|---|---|---|
| What happens to image | Primary model sees pixels | Signals extracted; image may be discarded | Image → text transcript → primary model sees text only |
| Vision provider dies | Cascade crash to text-only models | Signal failure; policy degrades | Graceful: "sorry, can't see" |
| Image bytes in context | Yes — 413 risk on fallback | Depends on policy | Never — zero 413 risk |
| Fallback models need vision | Yes — every fallback must accept pixels | No — signal-based routing | No — transcript is plain text |
| Audit trail | Model output only | Signal records | Transcript inspectable before reasoning |
| Primary model flexibility | Fixed to provider pool | Any model | ANY text model — full provider-agnostic |
| Recovery from vision errors | Swap to another VLM | Re-route with different signals | Impossible — what Qwen misses is lost forever |

## The Cost-Quality Tradeoff Specific to PRMT

PRMT's economics are different from both Pattern A and B:

| Cost factor | Pattern A | Pattern B | PRMT |
|---|---|---|---|
| Vision call | Always (model accepts image) | Always (signal extraction) | Always (transcript generation) |
| Reasoning call | Only if no image | Varies | Always (same primary) |
| Total per image turn | 1 API call (VLM) | 1-2 API calls (signals + model) | **2 API calls** (vision + reasoning) |
| Total per text turn | 1 API call | 1-2 API calls | 1 API call |

PRMT costs **exactly one extra vision call** per image turn. Vision calls cost ~$0.000014 (Qwen-VL) vs reasoning calls at ~$0.14/M (DeepSeek Flash). The overhead is negligible (<0.01% per turn).

## The Blind Spot

Both AIs (this session, 2026-07-30) that analyzed PRMT independently agreed:
- It's not EUREKA — it's Unix philosophy applied to agent multimodality
- It's not covered in existing literature because labs assume the reasoning model must handle all modalities
- The tradeoff (unrecoverable translation errors) is real but acceptable for Hermes' use case

Neither identified this: **PRMT has no recovery mechanism.** In Pattern A, if the cheap VLM misses something, you escalate to the frontier VLM. In Pattern B, you re-route with different signals. In PRMT, what Qwen misses is lost forever — because the primary model never sees the original pixels. The current Hermes implementation partially handles this by including the file path in the transcript block so the agent *can* call vision_analyze again for a second look — but that's reactive, not proactive.

## When PRMT Is the Right Choice

PRMT is optimal when:
1. **Primary model is text-only** (e.g., DeepSeek V4 Flash cannot accept image_url)
2. **Vision quality requirements are low-to-medium** (scene description, OCR, not precision measurement)
3. **Fallback chain is large and heterogeneous** (many models, some may not support vision)
4. **413 payload risk is unacceptable** (image bytes in context = ticking bomb on large images)

PRMT is suboptimal when:
1. **Primary model is VLM-capable** (Claude, GPT-5, Qwen-VL as primary → switch to native)
2. **Precision visual tasks** (seismic dip angle measurement, well log table extraction)
3. **Only one model in chain** (no fallback diversity to protect)

## Source Material

Related: `references/mas-framework.md` for the broader arifOS architectural context (Multimodal Agentic Swarm convergence).

This analysis was produced from session 2026-07-30 after:
- Debugging the OpenRouter Qwen-VL vision pipeline
- Receiving deep research briefs on multimodal routing literature (VSR, RouteLLM, MMR-Bench, NVIDIA LLM Router v2)
- Mapping Hermes' actual `gateway/run.py` code against the taxonomy
- Arif's config analysis confirming `image_input_mode: text` + `supports_vision: false` = PRMT

Related research:
- vLLM Semantic Router: https://github.com/vllm-project/semantic-router
- RouteLLM (ICLR 2025): https://arxiv.org/abs/2406.18665
- MMR-Bench: https://arxiv.org/abs/2601.17814
- NVIDIA LLM Router v2: https://github.com/NVIDIA-AI-Blueprints/llm-router
