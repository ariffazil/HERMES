---
name: agentic-rl-readiness-audit
description: 'Falsifiable readiness audit for agentic RL / world-model projects. D1-D4 proof gates: weight mutation, learning (optimization + generalization), world-model prediction, governance receipt. Path A (CPU proof) before Path B (GPU scale).'
category: governance
authority: F13 SOVEREIGN
forged: 2026-07-26
---

# Agentic RL Readiness Audit — D1–D4 Proof Gates

**DITEMPA BUKAN DIBERI** — Forged, Not Given.  
**Prinsip:** Computing a loss ≠ Training a model. Loss exists ≠ Learning exists.

---

## Three-Layer Separation

Before any audit, separate the claim into three layers:

| Layer | Question | Status |
|---|---|---|
| **Theory** | Is the architecture conceptually sound? | ✅ / ❌ |
| **Data Capture** | Does trajectory collection infrastructure exist? | ✅ / ❌ |
| **Learning System** | Is there a demonstrated closed-loop learning cycle? | ✅ / ❌ |

**Learning System** requires: `nn.Module → loss.backward() → optimizer.step() → checkpoint delta → evaluation delta`. Without all five, zero learning is occurring regardless of theoretical sophistication.

---

## D1 — Weight Mutation Proof

**Goal:** Prove the optimizer actually changes model parameters.

```
checkpoint_A = model.state_dict()
train(model, steps=100)
checkpoint_B = model.state_dict()
assert checkpoint_A != checkpoint_B  # by value, not reference
```

**Minimum:** 100 steps on CPU. Any model size. Any optimizer.

**Failure mode:** `checkpoint_A == checkpoint_B` → loss function is decorative, not functional.

**Evidence:**
- `model_hash_before` (SHA256 of state_dict)
- `model_hash_after` (SHA256 of state_dict)
- Training logs showing non-zero gradient norms

---

## D2 — Learning Proof (Two Sub-Gates)

### D2a — Optimization Proof
```
training_loss_before > training_loss_after
```
Proves the model fits the training data.

### D2b — Generalization Proof
```
heldout_loss_before > heldout_loss_after
heldout_reward_before < heldout_reward_after
```
Proves the model learned a pattern, not memorized trajectories. Held-out set can be tiny.

**Lock the metric before training:**
- Classification: exact match, cross-entropy
- Regression: MSE, cosine distance
- RL: reward, advantage

**Evidence:**
- `train_loss_before` / `train_loss_after`
- `eval_loss_before` / `eval_loss_after`
- Seed, hyperparameters, dataset split

---

## D3 — World Model Proof

**Goal:** Measure prediction quality directly.

```
gap_before = error(predict_observation, actual_observation)  # at step 0
gap_after  = error(predict_observation, actual_observation)  # at step N
assert gap_before > gap_after
```

**Lock metric before training:** MSE, cross-entropy, cosine distance, or exact match. Same metric throughout.

**Failure mode:** `gap_before ≈ gap_after` → world model is not learning. Revise architecture before scaling.

**Evidence:**
- `Gap@Step0`
- `Gap@Step100`
- Prediction samples (input → predicted → actual)

---

## D4 — Governance Proof (F11 Compliance)

Every training run must produce a signed receipt:

```json
{
  "run_id": "<uuid>",
  "timestamp": "<ISO8601>",
  "model_hash_before": "<sha256>",
  "model_hash_after": "<sha256>",
  "dataset_hash": "<sha256>",
  "seed": 42,
  "hyperparameters": { "lr": 0.001, "batch_size": 32, "steps": 100 },
  "steps": 100,
  "train_loss_before": 0.0,
  "train_loss_after": 0.0,
  "eval_loss_before": 0.0,
  "eval_loss_after": 0.0,
  "verdict": "LEARNING_DEMONSTRATED | OPTIMIZATION_ONLY | FAILED"
}
```

**Principle:** Any result must be reproducible. Without MODEL_HASH, DATASET_HASH, SEED, HYPERPARAMS — F11 auditability is unresolved.

---

## The AAA–FFF Dataset Chain as Reward Substrate

The existing HuggingFace dataset chain (`ariffazil/AAA` through `ariffazil/FFF`) IS the reward model and evaluation substrate for D1–D4. The FFF 6-gate protocol generates a scalar reward ∈ [0, 1]:

| Gate | Type | Signal |
|------|------|--------|
| G1_PARSE | Binary | 1 if parseable |
| G2_TRUTH | Continuous | Truthfulness ≥ 0.75 |
| G3_EVIDENCE | Binary | Evidence cited |
| G4_AUDIT | Binary | Audit trail maintained |
| G5_LEASE | Binary | Lease authority respected |
| G6_SOVEREIGNTY | Binary | F13 respected (0 = 888_HOLD) |

**Critical gap (2026-07-26):** Datasets are verdict-shaped (final evaluations per model), not trajectory-shaped (step-by-step prompt→response→gate_scores). For D1–D4, build a thin wrapper that scores BBB prompt→response pairs through the FFF evaluator and produces trajectory entries.

See `references/aaa-fff-reward-chain.md` for full dataset structure and per-gate wiring.

---

## Path A vs Path B

### Path A — CPU Proof (RECOMMENDED FIRST)

Tests the entire causal chain on minimal hardware: `Trajectory → Encoding → Model → Hybrid Loss → Backward → Optimizer → Checkpoint Mutation → Evaluation → Receipt`. If any link breaks, discover before spending on GPU.

**Runs on:** VPS CPU. Policy heads, linear probes, small transformers.

### Path B — GPU Scale (SECOND)

Only after D1–D4 pass on CPU. Danger: GPU ✅ + Cloud ✅ + Data ✅ but still no verified learning loop ❌.

---

## Verdict Grammar

| Verdict | Meaning |
|---|---|
| **SEAL** | Path A is the right next experiment. Proceed with D1–D4 on CPU. |
| **HOLD** | Theory or data capture layer is unresolved. Do not attempt learning until layers 1–2 pass. |
| **SABAR** | Architecture exists but critical uncertainty remains. Requires more analysis before Path A. |
| **VOID** | Foundational flaw in theory, loss formulation, or trajectory infrastructure. |

---

## Constitutional Reading

```
EVIDENCE:
  - Architecture exists:         ✅ / ❌ / PARTIAL
  - Loss formulation exists:     ✅ / ❌ / PARTIAL
  - Trajectory capture exists:   ✅ / ❌ / PARTIAL
  - Learning proof (D1-D4):      ✅ / ❌ / PARTIAL

INTERPRET:
  True Phase 2 gate is not GPU availability.
  True gate is: demonstrated closed-loop learning on a minimal model.

VERDICT:
  SEAL / HOLD / SABAR / VOID
  (for Path A as the next experiment — not for the architecture itself)
```

## Reference Files

- `references/aaa-fff-reward-chain.md` — HuggingFace dataset chain structure (ariffazil/AAA through ariffazil/FFF), trajectory format gap, FFF 6-gate protocol as reward function, D1–D4 wiring per gate. Origin: 2026-07-26 analysis connecting federation datasets to world-model training.

**DITEMPA BUKAN DIBERI** — Before scaling, prove that even a tiny model can learn from the forge.
