# World Model Instrumentation for Governed Agents

> **References:** ECHO [arxiv:2605.24517], PaW [arxiv:2606.02388], Qwen-AgentWorld [arxiv:2606.24597], True Agents Model the World (Prime Intellect)
> **Forged:** 2026-07-21 — A-FORGE Phase 1 + 1.5 implementation
> **Constitutional:** F2 TRUTH, F4 CLARITY, F7 HUMILITY, F8 GENIUS, F11 AUDIT

## The Core Insight

Standard agentic RL uses **sparse outcome rewards** — an entire trajectory gets a single signal (success/failure). But every trajectory is information-rich: each step contains an **action** from the agent AND the **resulting observation** from the environment. Standard RL masks out observation tokens from the loss function — **throwing away free supervision**.

**World Model instrumentation captures this supervision** by recording action→observation pairs with metadata about surprise, entropy, and prediction gaps. This data feeds future RL training (ECHO/PaW hybrid objectives) where the agent learns to predict environment responses alongside selecting actions.

## Five Architecture Laws

| Law | Inti | Source |
|-----|------|--------|
| **L1** | OBSERVATION IS SIGNAL, NOT EXHAUST — tool output is evidence, never dead context | ECHO |
| **L2** | ZERO-COST DENSITY — metadata from in-flight data; reuse log-probs, don't recompute | ECHO |
| **L3** | SURPRISE TEACHES MORE THAN ROUTINE — high-entropy actions carry most information; filter low-info observations | PaW |
| **L4** | MODEL DYNAMICS, NOT DATA — code execution predicts (learnable); retrieval memorizes (overfitting risk) | True Agents |
| **L5** | SIMULATE BEFORE YOU DEPLOY — learned simulator is reversible; real infra is not | Qwen-AgentWorld |

## Implementation Pattern (4 Modules)

### 1. Metadata Layer (`worldModel.ts`)

Attach `wm_metadata` to every tool receipt. This is the **instrumentation surface** — zero additional compute, metadata derived from data already in-flight.

```
wm_metadata: {
  action_hash: sha256(tool+args),        // what was done
  observation_hash: sha256(output),       // what happened
  wm_priority: "P0"|"P1"|"P2",          // training priority tier
  wm_eligible: bool,                      // should this train WM?
  agent_confidence: 0-1,                 // how sure was the agent?
  surprise_score: 0-1,                   // how unexpected was output?
  observation_entropy: float,            // output complexity proxy
  prediction_gap: float|null             // expected vs actual delta
}
```

**Priority Tiers (L4):**
- **P0**: shell, docker, git — deterministic state transitions, learnable dynamics. Always eligible.
- **P1**: filesystem, database — state-dependent but learnable. Eligible if output > 10 chars & non-trivial.
- **P2**: fetch, search, browse — retrieval tools. **Excluded** from WM training (memorization risk > learning benefit).

### 2. Logger Layer (`worldModelLogger.ts`)

Append-only JSONL ledger with SHA-256 hash chaining (mini VAULT999 architecture):

- `trajectories.jsonl` — action→observation pairs with WM metadata
- `predictions.jsonl` — agent prediction vs actual observation (confidence gap)

Each record: `H(prev_hash ‖ canonical(record))`. Genesis hash: 64 zeros.

### 3. Prediction Layer (`observationPredictor.ts`)

The **richest signal** (L3): delta between what the agent expected and what actually happened.

```
BEFORE execution: predictObservation() → stores prediction in buffer
AFTER execution:  verifyPrediction() → computes gap, logs to ledger
```

**Gap scoring**: Jaccard distance on token sets. Gap > 0.3 = significant. Gap > 0.7 with confidence > 0.8 = CRITICAL (possible model blind spot, F7 HUMILITY trigger).

**Alert routing**: CRITICAL gaps emit `wm_gap_alert` events to the event-bus. These surface on dashboards for immediate review.

### 4. Analytics Layer (`wmAnalytics.ts`)

Real-time analytics over accumulated trajectory data:

- **Dashboard** (`generateDashboard`): per-tool metrics, hourly trends, priority distribution, gap trend (improving/stable/degrading), chain health, Phase 2 readiness
- **Quality Report** (`generateQualityReport`): signal quality scoring, overfit detection, best training tools ranking
- **Alert Pipeline** (`emitGapAlert`/`emitPendingAlerts`): event-bus emission for dashboard consumption
- **Readiness Assessment** (`getPhase2Readiness`): trajectory count gates (min 100), prediction count gates (min 30), infra blockers, effort estimate

## Wiring Into Existing Tool Surface

The instrumentation is **non-breaking** — it adds metadata to existing returns without changing any API contracts:

1. **forgeShell.ts**: After execution, call `buildWmMetadata()` → `logTrajectory()`. Add `wm_metadata` to return JSON. Pass to `sealer.seal()`.
2. **arifSeal.ts**: Add optional `wm_metadata` field to `SealRecord`. Include in `seal()` params.
3. **event-bus.ts**: Extend `SseEvent` union with `WmGapAlertEvent` type.

## Phase 2 Readiness (ECHO-Style RL Training)

Phase 2 requires these gates before proceeding:

| Gate | Minimum | Purpose |
|------|---------|---------|
| Trajectories | 100 | Enough data for meaningful WM loss signal |
| Predictions | 30 | Enough gap data to assess overfit risk |
| GRPO implementation | Code | DeepSeekMath GRPO + hybrid ECHO loss (λ ∈ [0.01, 0.05]) |
| Agent harness | Harbor-style | Wraps forge_* tools in Docker sandboxes for safe rollouts |
| Reward model | Binary verifier | All task tests pass → 1, else → 0 |
| Sovereign approval | 888_HOLD | Arif must approve RL training on live infra |

Estimated effort: 3-5 engineering days for Phase 2 MVP.

## Pitfalls

- **Overfitting**: Dense WM loss overfits faster than pure RL, especially in retrieval-heavy domains. Use separate normalization, tool selection filtering, and early stopping.
- **λ balance**: WM loss must be weighted carefully (λ ∈ [0.01, 0.05]). Too high → agent prioritizes prediction over action. Too low → no benefit.
- **Not all observations are useful**: Filter out empty outputs, trivial outputs ("OK", "[]"), malformed trajectories, and P2 tool outputs.
- **Domain interference**: WM training in one domain can help (forth-lang → deepdive) or hurt (forth-lang → general-agent). Behavioral analysis required.
- **Chain hygiene**: The trajectory log inherits VAULT999's hash chain principles. Never delete or rewrite entries.

## Code Location

All modules in `/root/A-FORGE/src/domain/governance/`:
- `worldModel.ts` — metadata types, priority classifier, entropy/surprise/gap calculators
- `worldModelLogger.ts` — append-only JSONL logger with hash chaining
- `observationPredictor.ts` — predict→verify→gap scoring cycle
- `wmAnalytics.ts` — dashboard, quality reports, alert pipeline, readiness assessment

Data at `/root/.local/share/arifos/world-model/`:
- `trajectories.jsonl` — hash-chained action→observation pairs
- `predictions.jsonl` — prediction vs actual gap records

EUREKA artifact at `/root/A-FORGE/forge_work/2026-07-21/AGENTIC-WORLD-MODEL-EUREKA.md` (SHA256: 484f5e36).
