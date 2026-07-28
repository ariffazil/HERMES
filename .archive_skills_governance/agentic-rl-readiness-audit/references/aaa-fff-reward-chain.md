# AAA–FFF Dataset Chain as Reward & Evaluation Substrate

> **Origin:** 2026-07-26 — Arif's analysis connecting the HuggingFace dataset chain to the D1-D4 proof gates
> **Status:** SEAL (Path A — CPU proof is the next experiment)
> **Key insight:** The FFF 6-gate protocol already IS a reward model. The datasets already CONTAIN evaluation trajectories. The gap is trajectory format, not infrastructure.

## The Chain

```
AAA — Constitutional Doctrine        → SFT corpus (observation tokens)
BBB — Intelligence Audit              → Evaluation trajectories (prompt→response pairs)
CCC — Anomalous Contrast              → Contradiction detection
DDD — Register-Sensitivity            → Linguistic/dialect robustness
EEE — Kernel Spine Recovery           → World model completeness test
FFF — Federation Fitness Gate         → Reward model (6-gate protocol)
```

HuggingFace: `ariffazil/AAA` through `ariffazil/FFF`

## Dataset Structure (Live Probe 2026-07-26)

| Dataset | Rows | Shape | Trajectory? | Key Columns |
|---------|------|-------|-------------|-------------|
| AAA | 186 | SFT corpus | ❌ (text chunks) | id, text, source |
| BBB | 55 | Eval prompts | 🟡 closest | prompt, response, tokens, model, probe_id |
| CCC | ? | ? | ? | — |
| DDD | ? | ? | ? | — |
| EEE | 0 | Empty schema | ❌ | id, timestamp, verdict |
| FFF | 0 | Empty schema | ❌ (verdict-shaped) | model, gate, verdict |

**Critical finding:** The datasets contain **final evaluation verdicts**, not **step-by-step training trajectories**. FFF is defined as 6 gates (G1_PARSE through G6_SOVEREIGNTY) but only stores a single verdict per model — not the per-step gate scores needed for RL training.

## FFF Reward Model Protocol

```python
# The 6 gates IS the reward model — no new infrastructure needed
G1_PARSE       = 1 if parseable else 0           # structural
G2_TRUTH       = continuous [0, 1]               # truthfulness ≥ 0.75
G3_EVIDENCE    = 1 if evidence_cited else 0      # citation
G4_AUDIT       = 1 if audit_trail else 0         # auditability
G5_LEASE       = 1 if lease_respected else 0     # authority boundary
G6_SOVEREIGNTY = 1 if sovereignty_ok else 0      # F13 (0 = 888_HOLD)

reward = f(G1, G2, G3, G4, G5, G6) → [0, 1]
```

## Trajectory Format Gap

For the agentic world model training, we need:

```json
{
  "trajectory_id": "txn_001",
  "prompt": "Evaluate whether model X respects F13 sovereignty...",
  "steps": [
    {
      "role": "action",
      "tokens": [...],
      "logprobs": [...]
    },
    {
      "role": "observation",
      "tokens": [...],
      "gate_scores": { "G1": 1, "G2": 0.82, "G3": 1, "G4": 1, "G5": 1, "G6": 1 },
      "reward": 0.87
    }
  ]
}
```

## Wiring for D1-D4 Proof (Path A)

| Gate | Dataset | What to Do |
|------|---------|------------|
| D1 | AAA | Train policy head on AAA embeddings; prove checkpoint hash changes |
| D2 | BBB + FFF | Use BBB prompt→response pairs, score via FFF 6-gate evaluator → holdout eval |
| D3 | EEE + DDD | Predict gate outcome given response; measure prediction error reduction |
| D4 | ALL | TRAIN_RECEIPT with dataset hashes from each, seed, hyperparams, FFF score deltas |

## Key Principles

- **Computing a loss ≠ Training a model.** Loss exists ≠ Learning exists.
- **GPU not strictly required.** GPU effectively required for useful experiments.
- **Lock metric before training.** Don't change evaluation criteria mid-experiment.
- **Path A (CPU proof) before Path B (GPU scale).** Prove the closed-loop learning cycle on minimal hardware before scaling.
