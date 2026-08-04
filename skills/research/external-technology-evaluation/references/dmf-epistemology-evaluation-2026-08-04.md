# DMF + Epistemology Tripartition — Evaluation (2026-08-04)

## Source Chain

Arif pasted a Gemini Deep Research output: 13-page PDF "Paradigms of Epistemology and Measurement" (Google Docs renderer, Skia/PDF). Traced to its actual source: **DMF paper** (arXiv:2606.03463, Stabile & Zimuel, Jun 2026). The PDF was a companion piece — epistemological justification for DMF's deterministic memory approach.

**GitHub**: https://github.com/matstech/dmf — `pip install dmf-memory`

## What DMF Is

CPU-first deterministic memory framework for conversational agents. Replaces LLM-based summarisation with:
- spaCy morpho-syntactic analysis + VADER sentiment → deterministic NLP signals
- Interaction-count decay (Δn, NOT wall-clock) — same formula as our Phase 1
- Score-dependent inertia μ(Ω) = 1 - η·Ω — same as our Phase 1
- Zero LLM calls in memory loop — same as our Phase 1
- 5×–242× fewer tokens than Mem0 while achieving comparable accuracy

## What Was Already In arifOS (Not EUREKA)

| Feature | arifOS Status |
|---------|--------------|
| Interaction-count decay Δn | ✅ memory_decay.py |
| Ebbinghaus exponential decay | ✅ Ω_eff(Δn) = Ω · e^(-λ·Δn) |
| Score-dependent inertia | ✅ μ(Ω) = 1 - η·Ω |
| Zero LLM in memory loop | ✅ Phase 1 design |
| Source-canonical raw records | ✅ Honcho + RAW |
| 4-tier hierarchy | ✅ STM/MTM/LTM/Archive |
| Tri-witness (W³) | ✅ forge_witness — maps to Bell sampling |

## What Was EUREKA (7 atoms)

### E1 — Epistemic Tripartition Doctrine
Three layers of truth-testing, each mapped to constitutional floors:
- Semantic (F2): qualitative, NLP proxies
- Deterministic (F7/F8): quantitative, mathematical decay
- Witnessed (F11/F13): quantum-style, multiple observers → classical shadows

Saved: `/root/ariffazil/docs/doctrines/epistemic-tripartition.md`

### E2 — Bell Sampling = W³ Tri-Witness
Quantum Bell sampling protocol is mathematically equivalent to W³:
- Three independent measurements on same artifact
- Geometric mean ∛(H·A·E) — non-compensatory (zero in any channel = zero)
- Three is minimum to defeat SPAM noise
- SPAM = State Preparation AND Measurement = epistemic label corruption

Saved: `/root/ariffazil/docs/doctrines/bell-sampling-as-tri-witness.md`

### E3 — Three-Channel Survival Score with Logistic Projection
DMF decomposes Ω into three pre-sigmoid channels:
- Content: info density + sentiment + entity count − divergence
- Operational: preference, constraint, correction, replacement signals
- Provenance: caller-supplied metadata

Then: Ω = σ(z) — logistic sigmoid centered at midpoint. Bounded [0,1], maximally sensitive near midpoint where average turns cluster.

**Our gap**: We use linear V(m) = Σwᵢfᵢ(m). No sigmoid projection. No provenance channel in Ω scoring.

### E4 — Recall-Time NLP (not write-time)
DMF central invariant: "source-canonical memory" — raw records are authoritative; structured cards are projections; semantic interpretation runs at query time.

**Our gap**: We score at write time, retrieve at query. DMF argues this couples storage to model evolution.

### E5 — Topic Supersession
Newer facts about same topic suppress older ones during retrieval. User says "I used to prefer X, now Y" → X gets `replacement` signal → suppressed in retrieval.

**Our gap**: Preference updates don't propagate. Both old and new survive.

### E6 — NLP Feature Extraction Pipeline
spaCy POS tagging → information density (semantic tokens / total tokens)
VADER → sentiment magnitude (|compound|)
spaCy NER → named entity count (saturation-normalized)
Moving centroid → semantic divergence (cosine distance)

**Our gap**: We use simpler signals for V(m). Not POS-based.

### E7 — Quantum Scalability Escape as Architecture Principle
Brute-force state verification = O(4ⁿ), impossible. Bell sampling = O(1) per witness × 3 = O(1). This is WHY arifOS uses 3 witnesses not 16+.

## Doctrine Atoms Produced

1. `/root/ariffazil/docs/doctrines/epistemic-tripartition.md` — 3-layer truth testing
2. `/root/ariffazil/docs/doctrines/bell-sampling-as-tri-witness.md` — W³ formal proof

## Proposed Next Actions (not yet executed)

- **Phase A** (done): Doctrine atoms authored
- **Phase B** (deferred): Add 3 missing memory signals (sentiment, entity count, supersession) to cognitive/memory_decay
- **Phase C** (deferred): Benchmark DMF vs our engine on LoCoMo dataset

## Lesson: Document Purpose First

Arif asked "What is this for?" after a 1500-word deep analysis. The lesson: when sharing an external research document, **state its PURPOSE in the first sentence** before analysis. "This is the epistemological justification for DMF, the memory framework we based Phase 1 on" — that's the opening line, not a deep-dive into quantum tomography.

---

## Deep Analysis Round 2 (2026-08-04 evening)

### SOURCE PDF MATH ERROR [OBS]

The source PDF contains a substantive error in the QST (Quantum State Tomography) section. It claims:

> ⟨X⟩ = P_X(-1) + P_X(+1)

**This is wrong.** For eigenvalues ±1, the correct formula is:

> ⟨X⟩ = (+1)·P(+1) + (-1)·P(-1) = P(+1) - P(-1)

**Verified numerically:**
- P(+1)=0.9, P(-1)=0.1 → paper gives 1.0, correct is 0.8
- P(+1)=0.5, P(-1)=0.5 → paper gives 1.0, correct is 0.0
- P(+1)=0.2, P(-1)=0.8 → paper gives 1.0, correct is -0.6

The paper's formula always produces 1.0 (since probabilities sum to 1), which is the identity operator trace, not the observable expectation value. This error would propagate into the density matrix reconstruction if naively implemented. F2 TRUTH: treat the tomography section of this paper with caution.

### System-Novel EUREKA Candidates (3 additional)

**E8 — Witness-Set Calibration (GST-Zen)** [DER, conf 0.80]
- Joint estimation of (a) arifOS floor threshold, (b) AI-witness accuracy, (c) human-witness accuracy, (d) external-witness accuracy — WITHOUT requiring pre-labeled ground truth
- Paper's GST analogy: self-consistent benchmarking that learns gates + SPAM errors jointly
- Current system: FloorCalibrator calibrates thresholds but ASSUMES labeled cases = ground truth. Tri-witness W3 assumes witnesses are independent clean sensors.
- Zen kernel: "Kalibrat instrumen, bukan hanya bacaan."
- Falsification: held-out test set contradicts EM-estimated witness biases
- Closest existing: rsi_audit.py confusion_matrix tracks CORRECT_HOLD/FALSE_HOLD post-hoc

**E9 — Tamper-Evident Shadow Set (Classical-Shadows-Zen)** [DER, conf 0.75]
- Small randomized "shadow queries" that preserve property families for later inference
- Paper reference: Huang-Kueng-Preskill 2020 (Nature Physics 16, 1050-1057)
- Current system: external_witness_probe.py runs 18 fixed checks (not randomized, not property-preserving)
- Zen kernel: "Ukur kecil, ramal banyak."
- Falsification: shadow cannot recover a specific property the full probe would have detected

**E10 — Twin-Run Differential Witness (Bell-Sampling-Zen)** [INT, conf 0.70]
- Two independent measurement paths → compare relational invariants, not absolute values
- Current system: identity-invariance test harness already does cross-substrate comparison; arif_memory score_prediction mode compares prediction vs observation
- Novel at scale: for each major verdict, produce a "twin" verdict under paraphrased prompt and compare
- Zen kernel: "Dua ukuran, satu kebenaran relatif."

### External Source Cross-Verification

- **Bell sampling (arXiv:2306.00083v5)**: "circuit shadows" from Bell samples are classically intractable to produce but allow efficient extraction of circuit properties. Universal quantum computation model.
- **Classical shadows (Nature Physics 16, 1050-1057, HKP 2020)**: O(log M) copies suffice to predict M properties, independent of system size.
- **Gate Set Tomography (q-2021-10-05-557)**: self-consistent benchmarking that reconstructs gates + state-prep + measurement jointly. Robust to SPAM errors.
- **SPAM (QST manual, Qiskit)**: assumes ideal preparation/measurement — an assumption "almost never respected in actual hardware."
- **APEX vocabulary constraint (apex-vocabulary.v1.md)**: explicitly rejects borrowing quantum prestige for ordinary governance. Quantum vocabulary reserved for legitimate quantum-runtime domains only.
