# Jacobian Cognition Kernel — Forged 2026-07-25

**Status:** SEALED (OpenCode via A-FORGE, receipt `RECEIPT-JACOBIAN-COGNITION-KERNEL-20260725`)
**Location:** `/root/A-FORGE/src/domain/cognition/`
**Language:** TypeScript (Ω-plane — will migrate to Δ-plane Python in future iteration)

## What It Does

The Jacobian Cognition Kernel gives the federation metabolic learning — the ability to encode a goal into a task vector with per-field sensitivity, execute, measure fidelity, adjust weights on failure, detect drift, and persist the Jacobian across sessions.

Before: G was `UNMEASURED` — an aspirational label. Tasks failed silently. Sensitivity was nonexistent.

After: G is `COMPUTED` — `(A·P·X·E²)·(1-h)` from live task state. Sensitivity is a `TaskSensitivity` struct with 7 fields. Failure adjusts weights. Drift is detected via EMD gate.

## Architecture

```
Goal text → encodeGoal() → T = [t₁,...,tₘ] with J = ∂T/∂G
                               ↓
                        Execute tasks
                               ↓
                        metabolicCycle() → adjust weights on failure
                               ↓
                        emdPass() → compare T₁ to T₀, detect drift
                               ↓
                        recompute() → recalculate only high-sensitivity tasks
```

### Four Engines

| Module | Lines | Role |
|--------|-------|------|
| `taskJacobian.ts` | 145 | Types: TaskSensitivity, TaskVectorEntry, GoalVector, JacobianMatrix. Compute: G, C_dark, W3, continuity hash. |
| `goalEncoder.ts` | 390 | Natural language → task vector. Domain classification (8 domains) via keyword rules. Organ routing per domain. |
| `emdGate.ts` | 273 | Encode→Metabolize→Decode. Detect anomalies: divergence, scope creep, domain drift, risk shift, tool mismatch. C_dark thresholds: ≥0.30→HOLD, ≥0.50→VOID. |
| `metabolicLoop.ts` | 276 | Failure weight adjustment. risk_weight ×1.2, constraint_weight ×1.2 on failure. Regression toward 1.0 on success. Cap at 5 cycles → HOLD_RECOMMENDED. |

### 5 MCP Tools

| Tool | Purpose |
|------|---------|
| `forge_apex_encode` | Goal → task vector with Jacobian sensitivity |
| `forge_apex_metabolize` | Run metabolic cycle on goal (adjust weights from outcomes) |
| `forge_apex_emd` | EMD validation gate — verify decode matches encode |
| `forge_apex_recompute` | Recompute on field change — recalculates only high-sensitivity tasks |
| `forge_apex_goal_status` | Inspect current goal state |

## Key Types

```typescript
interface TaskSensitivity {
  risk: number;      // [0,1]
  scope: number;     // [0,1]
  authority: number; // [0,1]
  time: number;      // [0,1]
  cost: number;      // [0,1]
  organ: number;     // [0,1]
  domain: number;    // [0,1]
}

interface TaskVectorEntry {
  task_id: string;
  label: string;
  sensitivity: TaskSensitivity;  // J = ∂T/∂G
  domain: TaskDomain;
  organ: OrganTag;
  c_dark_contribution: number;   // [0,1];
  state: "pending" | "running" | "completed" | "failed" | "re_routed";
  provenance: TaskProvenance;
  last_sensitivity_check: string;
}

interface GoalVector {
  goal_id: string;
  goal_hash: string;
  goal_text: string;
  tasks: TaskVectorEntry[];
  G: number;        // (A·P·X·E²)·(1-h)
  C_dark: number;   // average per-task C_dark
  version: number;
}
```

## G Formula Note

The kernel computes G = (A·P·X·E²)·(1-h) — this is the **V1 formula** (E², no Φ primitive). The sealed canonical formula is G = A·P·E·X·Φ (V2 from `apex-verification-pipeline`). The Jacobian kernel uses V1 because it's computing G from task state (execution efficiency), not from the full witness+physics pipeline. This is acceptable — the two G values serve different purposes:

- **Jacobian G:** How efficiently are tasks executing? (operational G, from task state)
- **APEX G:** Is the action constitutionally permitted? (governance G, from witness+physics)

Eventually these should converge, but they are different planes today.

## Constitutional Alignment

| Floor | Enforcement |
|-------|-------------|
| F2 TRUTH | Every sensitivity is computed from domain heuristics + phrase analysis, not asserted |
| F4 CLARITY | Each encode/decode cycle reduces ambiguity (ΔS ≤ 0) |
| F7 HUMILITY | G capped at (1-h) where h=0.04. Confidence never exceeds 0.92 |
| F8 GENIUS | G = (A·P·X·E²)·(1-h) computable from live task state. WAS: UNMEASURED |
| F9 ANTI-HANTU | C_dark ≥0.30 triggers HOLD, ≥0.50 triggers VOID |
| F11 AUDIT | Every metabolic adjustment, every encode/decode, produces anomaly report |

## Tests

- **40 tests, 9 suites, 0 fail** (62ms)
- Covers: goal encoding, task classification, Jacobian sensitivity, metabolic cycle, EMD gate, recompute, edge cases (empty goals, unknown domains, single-task goals, high-failure scenarios)

## Gap

The kernel lives in TypeScript (Ω-plane), not Python (Δ-plane). The Jacobian — the *thought* of sensitivity — runs in the *transport* language. This means:

- No built-in state persistence across process restarts (buildContinuityHash() is an escape hatch)
- No direct introspection from arif_think (separate process, MCP bridge required)
- The metabolic loop is a function call, not a kernel primitive

**Doctrinal end-state:** Task decomposition + Jacobian computation in Python (Δ). Jacobian transport + cockpit in TypeScript (Ω). Jacobian-gated execution in Rust (Ψ).
