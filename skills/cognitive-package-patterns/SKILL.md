---
name: cognitive-package-patterns
description: Patterns for building Phase-N cognitive-intelligence modules under `/root/HERMES/cognitive/`. Use when creating a new module directory (e.g. `cognitive/narrative_intel/`, `cognitive/emotion_engine/`), extending an existing one, or wiring cognitive modules into arifOS receipt flow. Covers the receipt-as-evidence-not-verdict contract, the Ebbinghaus-with-inertia form, embedding-backend defensive defaults, cue-vocabulary coverage tests, and the immutable-decision / reversible-decision boundary that separates cognitive computations from constitutional seals.
load_when: working in /root/HERMES/cognitive/ as source code; designing a new Phase-N cognitive module per arifOS research briefs; wiring cognitive computations to forge_receipt_draft or arif_memory
category: software-development
---

# Cognitive Package Patterns for Hermes Phase 1+

The cognitive package at `/root/HERMES/cognitive/` is the first in a planned series of cognitive-intelligence layers for Hermes Agent. The research brief (`/root/HERMES/scratch/research_brief_phase1_validation.md`) identifies four axes — Causal, Temporal, Metacognitive, Narrative+Emotion — of which Phase 1 shipped Memory Decay, Causal Claim Tagging, and Metacognitive Drift Monitor. Future sessions will build Phase 2 (Narrative) and Phase 3 (Emotion) using the same scaffolding.

## When to load

- Creating a new `cognitive/<axis>/` module directory.
- Extending an existing module with new operations or evidence classes.
- Wiring any cognitive computation into the receipt/arifOS flow.
- Translating a research-paper formula into a verified implementation.
- Debugging a cognitive module against the Phase 1 contract.

Do NOT load for pure arifOS kernel work or unrelated Python — those have their own skills.

## Architecture invariants

The Phase 1 package settled on five non-negotiable patterns. Any new module MUST comply.

### 1. Three-tier layout

```
cognitive/
  __init__.py            # package init, re-exports
  config.py              # canonical constants (Ω₀, λ, η, CAPS)
  receipt.py             # Receipt dataclass + emit_receipt()
  requirements.txt       # deps (keep minimal)
  README.md              # usage + research alignment
  <axis>/
    __init__.py          # re-export public API
    <engine>.py          # core implementation
    (tests live in tests/, not per-axis)
  tests/
    test_<axis>.py       # pytest module, runnable as documented below
```

Per-axis `tests/` directories were rejected — kept all tests under `cognitive/tests/` so `python -m pytest cognitive/tests/ -v` works without configuration.

### 2. Receipt-as-evidence, never verdict

Every compute/detect function calls `emit_receipt()` and returns a structured result whose `.receipt` field is the load-bearing artifact. Receipts carry evidence + timestamp + epistemic label + confidence, never a SEAL/HOLD/VOID verdict — irreversible commitments still require 888 JUDGE through arifOS.

**Confidence cap lives in the receipt layer**, not at every call site. The `Receipt.__post_init__` clamps to `CONFIDENCE_CAP = 0.90` so individual call sites cannot smuggle 0.99 confidence past the F7 HUMILITY ceiling.

The most recent receipt in a module is exposed via `get_last_receipt()` so callers can read it without threading it through every function. Structured result dataclasses (`DecayResult`, `CausalClaim`, `DriftSignal`) embed their own receipt so callers do not have to manage parallel state.

### 3. Constants live in `config.py`

`Ω₀ = 0.03`, `λ = 0.05` (tuned down from 0.10 to double the half-life), `η = 0.50`, `CONFIDENCE_CAP = 0.90` plus axis-specific caps (e.g. causal caps per evidence class) live in `cognitive/config.py`. Module files import them; they do not redefine. New modules add their caps to `config.py` rather than scattering them.

Sanity-check the weights at import time:

```python
assert abs(sum(weights.values()) - 1.0) < 1e-6, "weights must sum to 1.0"
```

This catches mis-imported or partial weight dicts before they ship.

### 4. The Ebbinghaus-with-inertia form

For temporal-decay style modules, the canonical form is:

```
Ω_eff(Δn) = Ω · exp(-λ · Δn · μ(Ω))
where μ(Ω) = 1 - η · V(m)
```

The inertia `μ` multiplies the **exponent**, not the strength — this preserves the curve shape and prevents runaway protection for high-value items. Bare `e^(-λ·Δn)` without reinforcement is too thin for benchmarks; Alexander (2026) compounds stability non-linearly per recall:

```
S_new = S_old · (1 + ln(1 + recall_count))
```

Quantization changes precision, **never deletes**. Tier thresholds use `effective_strength` thresholds that map to bit-widths (`STM=32`, `MTM=8`, `LTM=4`, `ARCHIVE=2`).

### 5. Embedding backends: deterministic defaults, heavy ones opt-in

For any module that embeds text (drift monitor, semantic scoring, similarity search):

- Provide a deterministic pure-Python fallback (TF-IDF, fingerprint, hash-bucket).
- Provide the heavier ML backend as a separate class (e.g. `SentenceTransformerEmbedder`).
- **Default to the deterministic backend** even if the heavy one is importable. The heavy backend is only used when the caller explicitly constructs it.
- Reasoning: implicit model downloads make CI slow and non-reproducible; they also break the F2 TRUTH floor's reproducibility requirement.

The Phase 1 drift monitor learned this the hard way — its default auto-loaded `all-MiniLM-L6-v2`, making tests slow and inadvertently network-dependent. Fixed by inverting the default.

**EXCEPTION (proven empirically 2026-08-04):** when the heavy backend is small (≤100MB), already installed, deterministic-loaded, and simulation tests show the deterministic backend produces systematically wrong verdicts (e.g. TF-IDF drift monitor flagged 9/10 ON_TOPIC turns as DRIFT_ALERT because TF-IDF baseline cosine distance for non-identical sentences is >0.5), invert the default. Wrap the heavy backend construction in `try/except` so a missing package still falls back gracefully. The "deterministic default" rule is a default, not a religion — recalibrate when the simulation report contradicts it.

Verify the inversion with simulation re-run, not just unit tests: unit tests on embedding backends test identical-text → 0.0 (works for both TF-IDF and sentence-transformers) but miss the real-world discrimination gap.

## Cue-vocabulary coverage

Regex or keyword-based taggers (causal, sentiment, intent) fail silently when their vocabulary misses a common form. Always include at least one test that exercises:

- The bare lemma (`"A caused B"` for a `caused`-aware vocabulary that primarily has `"caused by"`).
- The bilingual equivalents if advertised (`sebab`, `kerana`, `menyebabkan`).
- Cues at the start of text, middle, and end.
- The case-insensitive match (`"BECAUSE"` must hit `"because"`).

The Phase 1 test `test_receipt_emitted` for `tag_causal("A caused B")` was the failing-test-by-design that surfaced the missing "caused" lemma.

## Wiring to arifOS

| Phase 1 output | arifOS primitive | Notes |
|---|---|---|
| memory_decay receipt | `forge_receipt_draft` (Lane B) → `arif_memory(mode=forget)` gated by F1 + 888 | Irreversible prune requires F1 AMANAH lock |
| causal_tagger claim | `arif_judge(mode=validate action_class=CAUSAL_CLAIM)` | Reversible — Lane B receipt is enough |
| drift_monitor signal | `forge_cool_drift` → VAULT999 → 888 | Drift scales the confidence cap down: `0.90 · (1 - drift_score)` |

Never call `arif_seal` from cognitive code. Receipts are evidence-layer artifacts. Sealing is the kernel's job.

## Testing contract

All tests runnable with one command:

```bash
cd /root/HERMES && python -m pytest cognitive/tests/ -v
```

No config, no conftest, no fixtures files. Test files import the public API at module top. Per-module coverage target:

| Test class | What to cover |
|---|---|
| `TestValue`/`TestEvidence` | Boundary values, clamping, invalid inputs, weight sum |
| `TestDecay`/`TestClassification` | Zero gap, large gap, value asymmetry, edge tiers |
| `TestEmbed`/`TestBackend` | Identical inputs, unrelated inputs, zero vector |
| `TestEngine`/`TestPipeline` | End-to-end with receipt verification |
| `TestIntegration` | Multi-step lifecycle (decay → reinforce → quantize) |

`compileall` MUST pass before commit. Run:

```bash
python -m compileall -q cognitive
```

## Pitfalls (durable, learned from Phase 1)

1. **Determinism beats cleverness.** If a heuristic plus an ML model produce equivalent accuracy on synthetic data, ship the heuristic as the default.
2. **Embedders are a category, not a single choice.** Always provide at least two backends and pick the deterministic one as default.
3. **Receipt leakage breaks audits.** Every result dataclass MUST carry its receipt; do not return a tuple `(result, receipt)`.
4. **Confidence cap is single-source.** If you find yourself writing `min(conf, 0.90)` anywhere outside `Receipt.__post_init__`, stop and remove it — it duplicates the cap and creates drift. **EXCEPTION:** varying confidence *below* the cap based on marker density (e.g. `cap * (0.85 + 0.15 * strength)`) is legitimate *calibration*, not duplication — it makes per-class confidence discriminating instead of flat at the cap. The simulation report's "Avg confidence (correct) 0.546 vs (incorrect) 0.561 — POOR" finding is the symptom of flat-cap output that needs calibration.
5. **Interaction count, not wall-clock.** Tests that use `time.sleep(...)` become flaky and OS-dependent. Pin memory/drift logic to canonical counters or deterministic seeds.
6. **Multi-source agreements deserve distinct classifications.** Causal claims with trace references (`OBS_CAUSAL`) are fundamentally different from multi-source reasoning (`DER_CAUSAL`) and from no-evidence speculation (`SPEC_CAUSAL`). Hard caps per class.
7. **Pattern-check order is part of the contract.** When classifying evidence into multiple tiers, the order you check patterns matters and the order is load-bearing. The Phase 1 simulation found DER_CAUSAL recall at 0.40 because the OBS regex was checked first — multi-source sentences containing trace/log keywords (e.g. "Based on metrics from Prometheus and Grafana") got classified as OBS_CAUSAL instead of DER_CAUSAL. **Rule of thumb: check the more-specific tier first.** DER (multi-source agreement) is more specific than OBS (single-source trace); INT (single-source inference) is more specific than SPEC (no evidence). When in doubt, add a one-line test that exercises the boundary case ("based on X and Y" with trace keywords in the same sentence) before shipping a regex change.

## Phase 2 Gaps Identified from DMF Paper Analysis (2026-08-04)

External review of `matstech/dmf` (arXiv:2606.03463) revealed three concrete gaps in our current memory_decay implementation. These are **future work**, not retroactive rewrites:

### Gap A — Three-channel Survival Score (current: single-channel linear aggregate)

DMF decomposes Ω into three pre-sigmoid additive channels:

```
z = w_c · content + w_o · operational + w_p · provenance
Ω = σ(z - midpoint)
```

Where:
- **content** = info_density + sentiment_mag + entity_density − divergence (current: we have linear content signals but no operational or provenance)
- **operational** = preference, constraint, correction, current/past state, replacement patterns (current: **missing entirely**)
- **provenance** = caller-supplied metadata (correction flag, preference update, constraint mark) (current: **missing entirely**)

**Recommended next**: add `operational_channel()` and `provenance_channel()` functions to `memory_decay/engine.py`, then move from linear `V(m) = Σwᵢfᵢ(m)` to logistic `Ω = σ(z)`. The sigmoid gives bounded [0,1], maximal sensitivity near midpoint, graceful saturation at extremes.

### Gap B — Recall-time NLP (current: write-time scoring)

DMF's central invariant: raw text is authoritative; structured cards are projections; **semantic interpretation runs at query time, not write time**. This decouples storage stability from model evolution.

Our engine scores at write, retrieves at query. When the scoring model changes, all old scores become stale. Moving to query-time scoring means the **same raw record** can be re-scored by any future model without rewriting history.

**Design question for Phase 2**: keep write-time scoring (cheap, deterministic) but add a query-time re-scoring hook that updates the score lazily. Storage cost: a single timestamp per entry for "last scored at". Compute cost: linear in retrieval size, bounded by token budget.

### Gap C — Topic supersession (current: no propagation)

DMF's pruning rule: newer facts about same topic suppress older ones during retrieval. User says "I used to prefer X, now Y" → X gets `replacement` signal → suppressed in retrieval.

Our engine preserves both old and new preferences with no supersession. This causes contradictory context to surface ("user prefers Tavily" AND "user prefers SearXNG" appearing together).

**Recommended next**: add a `supersession_signal` extractor that detects explicit replacement patterns (`X dulu, sekarang Y`, `not X but Y`, `replace X with Y`), and a `TopicSupersessionIndex` that filters at retrieval time.

### Pattern: External Paper → Gap Audit

When a new external paper validates our architecture, run a **gap audit** not a **rebuild**. Map every claim:

| Status | Action |
|--------|--------|
| ✅ Already in arifOS | Note as validation, no work |
| ⚠️ Partially present | Mark gap, schedule extension |
| ❌ Missing | Mark gap, design before coding |

Full evaluation: `../external-technology-evaluation/references/dmf-epistemology-evaluation-2026-08-04.md`

## Compatibility shims for partial Phase-N rebuilds

When a Phase 2+ rewrite of a cognitive module is started but not finished (engine.py uses new class names, the consumer-side `__init__.py` and `tests/` still import old names), don't rewrite the consumers. Add a compatibility block at the bottom of the new engine.py that:

1. Re-declares the old dataclass names as frozen `@dataclass` shims with the same field shape.
2. Provides stateless helper functions (value_score, score_dependent_inertia, effective_decay, reinforce, tier_for_strength, quantize_strength) that translate old kwargs to new math.
3. Pulls canonical constants (Ω₀, λ, η, tier thresholds, factor weights) from `cognitive.config` — never duplicate constants in the shim, so tuning the canonical source still propagates.
4. Re-exports everything from `<module>/__init__.py` with explicit import lines so pytest discovery works.

This pattern keeps the Phase 2 engine as source-of-truth while unblocking the simulation harness and test suite. The shim block is bounded: when a major version drops Phase 1 consumers, delete it. The block is also a useful regression target — if any Phase 1 test still fails after the shim lands, the new engine has a math divergence, not a wiring issue.

Apply the same pattern when an MCP server exposes a new tool name and the consumer expects the old name: shim at the boundary, don't rewrite the consumer.

## Future Phase 2/3 patterns

The research brief's Narrative + Emotion axes will mirror this layout. `cognitive/narrative_intel/` and `cognitive/emotion_engine/` are expected to:

- Reuse `cognitive.receipt` and `cognitive.config` unchanged.
- Add their own caps to `config.py` (e.g. `EMPATHY_*_CAP`).
- Use the same deterministic-default backend principle for any new embedder.
- Provide bilingual cue tests if their cue vocabulary includes Bahasa Melayu.
- Emit recipes for both the empirical claim and the deontic guard (F6 EMPATHY ⇄ MARUAH dual-register).

When building a new axis, fork one of the Phase 1 modules — they are the templates.

## Files in this skill

- `references/phase1-architecture.md` — full Phase 1 design walkthrough (constants, receipt schema, decay formula derivation, dependency map)
- `references/2026-08-04-phase1-tuning-round1.md` — session record of the first tuning round that fixed REINFORCED memory retention, DER_CAUSAL recall, confidence calibration, and drift-monitor baseline. Contains full before/after numbers, exact code patterns applied, and the hidden "Phase 2 partial rebuild overwrite" trap encountered during tuning.
- `references/llm-generated-validation-trap.md` — How to detect and refuse LLM-projected validation reports (imports commented out, hardcoded PASS verdicts, placeholder text). The 2026-08-04 session surfaced this when Arif pasted a "Causal Intelligence Substrate" v0.1 blueprint whose "simulation results" were faked. Rule: require actual file output from actual module calls before accepting any validation claim.
- `templates/new_axis_engine.py` — minimal starter template for a new cognitive axis module (boilerplate with receipt emission, result dataclass, `get_last_receipt()`)
- `templates/test_axis_skeleton.py` — pytest skeleton adapted for a cognitive axis module (4 test classes: boundary, engine, pipeline, integration)

Full shipping source (the real Phase 1 modules to fork):

- `cognitive/memory_decay/engine.py` — Ebbinghaus-with-inertia, value scoring, tier hierarchy, quantization
- `cognitive/causal_tagger/tagger.py` — regex cue detection, evidence classification, cause/effect extraction
- `cognitive/drift_monitor/monitor.py` — TF-IDF drift monitor with sentence-transformers opt-in
</content>
</invoke>