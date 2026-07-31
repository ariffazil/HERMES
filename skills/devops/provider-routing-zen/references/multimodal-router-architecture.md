# Multimodal Router Architecture — Reference

> **Source:** Deep research across vLLM Semantic Router, NVIDIA LLM Router v2, RouteLLM (ICLR 2025), MMR-Bench (arXiv 2026), LLMRouter (UIUC), and llm-semantic-router tri-encoder project.
> **Date:** 2026-07-30
> **Intent of this doc:** Architectural taxonomy and design patterns for multimodal routing systems. NOT about configuring a specific router — that belongs in the parent skill (`provider-routing-zen`) or specific router documentation.

## 1. What is a Multimodal Router?

A multimodal router sits **in front of** one or more LLMs/VLMs and decides, per-request, **which model or policy action** to take based on the **modalities present in the input** — text, image, audio, video, document — not just the prompt text.

There are two distinct patterns:

### Pattern A: Modality-Aware Model Selection

Pick the right model *given* the modalities present. E.g.:

- Has image → route to VLM
- Pure text, hard reasoning → route to frontier LLM
- Chit-chat text → route to cheap small LLM

### Pattern B: Signal-Decision Fabric (vLLM Semantic Router)

A **programmable policy layer** that extracts signals from the full request (text + image + audio), composes them with boolean logic, and makes a routing decision — not prompt classification, but **request-level policy**.

```
Clinical text + clinical image + PHI/PII signal → protected medical VLM with privacy plugins
Generic text + passport image → block/redact, route to identity-doc handler
Code prompt + code screenshot → security-specialized model + jailbreak checks
```

## 2. Core Architecture — The Six Layers

### Layer 1 — Input Ingestion & Modality Detection

Receive an OpenAI-compatible chat request. Detect which modalities are present:
- Text-only → simpler routing path
- Text + image → VLM routing
- Text + audio → ASR + routing
- Multi-turn with vision history → special handling (Router-Suggest decides character-by-character whether visual context matters)

### Layer 2 — Signal Extraction

Signals are **independent observations** extracted from the request. Each signal is typed and has provenance.

| Signal type | Source | Typical latency |
|---|---|---|
| Regex/keyword match | Text prompt | < 1 ms |
| Embedding similarity (text) | Text encoder | ~5 ms |
| Embedding similarity (image) | Image encoder (SigLIP, CLIP) | ~50 ms |
| Embedding similarity (audio) | Audio encoder (Whisper) | ~50 ms |
| LLM intent classification | Small LLM (e.g. Qwen 1.7B) | ~100-300 ms |
| Safety/PII/jailbreak detectors | Specialized models | Variable |

**Key design property:** Signals run **concurrently** — wall-clock latency is bounded by the slowest signal, not the sum.

### Layer 3 — Decision Composition

Signals are composed into decisions through **priority + boolean logic**:

```
IF (image_present AND PII_detected) → route_to_restricted_handler
IF (contains_code AND is_complex) → route_to_frontier_reasoning
ELSE IF (image_present) → route_to_vlm
ELSE IF (text_is_simple) → route_to_cheap_llm
```

This is the **Signal-Decision architecture** from VSR. Decisions must be **observable, auditable, programmable** — not a black box.

### Layer 4 — Routing Strategy

| Strategy | How it works | When to use |
|---|---|---|
| **Intent-based** | Small LLM classifies intent from full multimodal input, maps intent → model via config | Clear intent categories (visual analysis → VLM, code → coding LLM) |
| **Auto-routing (neural network)** | Embeddings (CLIP) encode text/image into shared space → trained NN predicts optimal model | Historical usage data available; data-driven routing |
| **Embedding-based** | Tri-encoder (text+image+audio towers) → shared embedding space → cosine similarity against anchor embeddings | Need strict reference parity; production signal correctness |
| **Rule/cost-based** | Pick cheapest model matching modality + constraints | Simple cost optimisation, no training needed |
| **Cascade** | Try cheap model first, escalate on low confidence | Can beat single frontier model on both cost AND quality |

RouteLLM (ICLR 2025) trained four types on human preference data:
- **Matrix Factorization** (MF) — best cost-quality tradeoff, ICLR 2025
- **BERT classifier** — 45% cost savings at comparable quality on MMLU
- **Similarity-weighted** ranking
- **Cascade** — try cheap, escalate on low confidence

### Layer 5 — Model/Policy Dispatch

The router either:
- Returns a **model recommendation** (NVIDIA v2, OpenRouter Auto Router) — your app calls the chosen model
- **Proxies the request** (NVIDIA v1, LiteLLM) — routes transparently
- Returns a **policy action** (VSR) — block, redact, route, or plugin-invoke

### Layer 6 — Audit & Eval Gate

Every routing decision logged (F11). Critical production concern: **silent quality regression** — routing to a cheap model that seems fine but subtly degrades quality. Mitigation: a pre-merge eval gate running 50-500 representative cases with groundedness checks. See `provider-routing-zen` parent skill — silent quality regression is the hidden tax.

## 3. Key Implementations Compared

| System | Router Model | Method | Inputs | Output | Training |
|---|---|---|---|---|---|
| **RouteLLM** (lm-sys) | MF / BERT / cascade | Preference-based | Text only | Chosen model | Human preference data |
| **NVIDIA LLM Router v2** | Qwen 1.7B / CLIP+NN | Intent-based OR auto-router | Text + Image | Model name | None / preference data |
| **VSR Semantic Router** | Multi-modal-embed tri-encoder | Signal-Decision policy fabric | Text + Image + Audio | Policy action (route/block/redact) | Cached MNRL loss |
| **OpenRouter Auto Router** | NotDiamond ML | Cost-quality tradeoff dial (0-10) | Text + Image | Model endpoint | Preference data |
| **Azure AI Foundry Router** | Trained LM | Balanced / Cost / Quality modes | Text + Image | Model endpoint | Prompt quality training |
| **MMR-Bench policies** | CLIP fusion + classifier | Modality-aware budget-aware routing | Text + Image | Model choice | Budget-aware training |

## 4. Signal Correctness — The Hardest Production Problem

### Vision Signal Anti-Correlation (vLLM VSR Case Study)

The `multi-modal-embed-small` path in VSR was **82% anti-correlated** on an 11-image probe — medical X-rays scored closer to semiconductor candidates than to medical anchors. Three separate bugs:

1. **Wrong pooling head** — BERT-style mean+Linear+tanh instead of SigLIP attentional probe pooling
2. **Missing image normalisation** — Go loader produced [0,1] range, SigLIP expects (x-0.5)/0.5
3. **Wrong resize algorithm** — bilinear vs PIL bicubic+antialias

After fixes: cosine > 0.999 on 20/20 images vs PyTorch reference.

**Lesson:** For multimodal routing, **reference parity is a control-plane invariant**. The deployed path must match the reference path. Pre-fix cosine on canonical fixture was 0.990145; even small drift (< 1%) can invert routing decisions entirely.

### The Diagnostic Chain (from VSR team)

1. Suspect encoder weakness → test reference path → **reference works fine**
2. Suspect preprocessing → isolate model-forward drift vs preprocessing drift
3. Fix each layer independently, validate with three-vector isolation:
   - Python vs Candle-PIL (model-forward only)
   - Candle-PIL vs Candle-Go (preprocessing only)
   - Python vs Candle-Go (full pipeline)

### Modality Fusion Problem

Pure text routing is easy. Once images enter, the router must decide **whether the image matters**. A medical text prompt + a car image should NOT route to a medical VLM — the image is out-of-domain noise. The router needs to detect **semantic coherence** between modalities, not just their presence.

## 5. Modality Detection via Tri-Encoder (VSR approach)

The `multi-modal-embed-large` model from llm-semantic-router project:

- **Architecture:** Tri-encoder with separate towers projected into one shared 768-dim space
- **Text encoder:** `mmbert-embed-32k-2d-matryoshka` (32K token limit)
- **Image encoder:** `google/siglip2-so400m-patch14-384`
- **Audio encoder:** `openai/whisper-medium`
- **Training objective:** Cached multiple negatives ranking loss (MNRL)
- **Validation:** eval_top1 = 0.8617, eval_loss = 0.3897
- **Usage:** Encode query + candidate anchors as `PairItem(modality=..., value=...)`, compute cosine similarity

```python
from hf_st_mm.data import PairItem
from hf_st_mm.model import MultiModalSentenceEmbedder

model = MultiModalSentenceEmbedder(text_encoder_name, image_encoder_name, audio_encoder_name, ...)
items = [
  PairItem(modality="text", value="route this request to billing"),
  PairItem(modality="image", value="/path/to/screenshot.png"),
  PairItem(modality="audio", value="/path/to/call.wav"),
]
embeddings = model.encode_items(items)  # [3, 768]
```

## 6. Economic Dimension

### Cost Lever

2026 price spread ~100x: DeepSeek V4 $0.44/M input → GPT-5.5-pro $30/M input / $180/M output. RouteLLM proved 85% cost savings on MT Bench at 95% of GPT-4 quality, needing the strong model on only 14% of queries.

| Traffic mix (cheap/frontier) | Savings vs all-frontier |
|---|---|
| 50/50 | 40-49% |
| 70/30 | 56-69% |
| 80/20 | 64-79% |

The curve shape matters: first slice of cheap-model traffic barely moves the bill (10/90 saves < 10% everywhere). Savings compound once cheap share crosses 50%. Router accuracy matters more than raw price gaps.

### Router Overhead

| Method | Latency | vs 800ms p50 inference |
|---|---|---|
| Rule-based | < 1 ms | 0.1% |
| Embedding-based | ~5 ms | 0.6% |
| ML classifier | 50-100 ms | 6-12.5% |

Even the most expensive router is single-digit percentage of total call. Exception: a router that ITSELF calls an LLM to classify difficulty — adds full inference round-trip.

### Zero-Shot Transfer

RouteLLM routers trained on one strong/weak model pair **transferred to unseen model pairs** at test time. This makes routing durable in a market where the model lineup changes monthly — you don't re-train the router every time a provider ships a new tier.

MMR-Bench showed that policies trained on a subset of models/tasks generalize zero-shot to new datasets and text-only benchmarks without retuning.

### MMR-Bench Key Finding

Routed multimodal systems can **exceed the strongest single model's accuracy at ~33% of its cost** by routing easy tasks to cheap models.

## 7. Decision Design Space (2026 survey)

Three axes for every routing system:

| Axis | Options | Cost | Quality impact |
|---|---|---|---|
| **When** | Pre-request / at-inference / post-response | Cheapest: pre-request | Most accurate: cascade |
| **What** | Query features / model metadata / past performance | — | — |
| **How** | Rules / classifiers / RL / cascades | Rules cheapest | Cascades most accurate |

Layered strategy in practice:
1. **Cheap rule pass** — obvious cases (known template → small model)
2. **Embedding/classifier pass** — ambiguous middle
3. **Cascade** — answer with small model, escalate if confidence check fails

The cascade pattern can genuinely beat a single frontier model on **both** cost and quality, because it spends frontier tokens only on requests that provably needed them.

## 8. Production Pitfalls Summary

- **Silent quality regression** — cheapest model that *can* handle ≠ cheapest model that *should*. Eval gate (50-500 representative cases) mandatory before pushing routing changes to production.
- **Vision signal anti-correlation** — cross-language serving stacks (Go → Rust FFI → Candle → PyTorch) can introduce embedding drift that inverts routing decisions. Reference comparison should be first diagnostic, not last.
- **Encoder size ≠ correctness** — VSR's `multi-modal-embed-small` scored 10/10 through PyTorch reference but was 82% inverted through Candle binding. The bug was implementation drift, not model weakness.
- **Modality coherence detection** — router must detect whether image evidence is semantically coherent with text, not just mechanically present.
- **Router calling LLM for classification** — adds full inference round-trip overhead. Reserve for genuinely hard routing decisions.
- **Cost-quality dial alignment** — `openrouter/auto-beta` defaults to CQT=9 (cost-leaning). On sovereign-adjacent topics, community spend-share ranking may select censored models. Route sensitive topics direct.

## 9. Sources

- vLLM Semantic Router blog: *From Text to Multimodal Routing: Hardening Vision Signals in VSR* (2026-05-28)
- NVIDIA LLM Router v2: github.com/NVIDIA-AI-Blueprints/llm-router
- RouteLLM: arXiv 2406.18665 (ICLR 2025)
- MMR-Bench: arXiv 2601.17814 (Jan 2026)
- Learned Routing Among Specialized Expert Models: arXiv 2511.06441 (Nov 2025)
- llm-semantic-router multi-modal-embed-large: huggingface.co/llm-semantic-router/multi-modal-embed-large
- LLM Model Routing 2026 guide: digitalapplied.com
- Router-Suggest: Dynamic Routing for Multimodal Auto: arXiv 2601.05851
