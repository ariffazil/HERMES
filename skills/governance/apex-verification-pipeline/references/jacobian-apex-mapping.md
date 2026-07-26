# Jacobian → APEX Primitive Mapping

The APEX equation G = A · P · E · X · Φ maps directly to the dual-sensitivity kernel (Jacobian + ToAC) implemented in the A2A server's goal decomposition pipeline.

## Primitive → Kernel Half Mapping

| Primitive | Name | Kernel Half | What computes it | Code location |
|-----------|------|-------------|------------------|---------------|
| **A** | Awareness | Cognitive (Jacobian) | `encodeGoalToTasks(G)` — maps goal to task vector. ∂tasks/∂intent | `goal_decomposition.js` |
| **P** | Presence | Cognitive (Jacobian) | `buildJacobian(G, T)` — ∂task/∂riskband, ∂task/∂org_scope. Sensitivity matrix. | `goal_decomposition.js` |
| **E** | Evidence | Perceptual (ToAC) | `decodeTasksToEnvelopes()` — ∂envelope/∂emd_confidence. Dispatch through EMD gate. | `task_routing.js` + `emd-validation-gate.js` |
| **X** | Execution | Cognitive (Jacobian) | Stored J matrices from past metabolic sessions. Cross-goal memory (not yet VAULT999-persistent). | `metabolizer_loop.js` |
| **Φ** | Witness | Perceptual (ToAC) | `emdValidationGate()` — W³ = ∛(h·ai·ext). Tri-witness validation. | `emd-validation-gate.js` |

## The F8 GENIUS Variant

The `POST /a2a/goal/decompose` route also implements the F8 variant:
```
G = A · P · X · E² · (1-h)
```
Where `h` = hallucination rate from EMD gate blocks. This variant embeds humility directly into the score rather than treating it as a separate gate.

## Live Computation

Every call to `POST /a2a/goal/decompose` returns:
- `jacobian.fields` — which goal fields have sensitivities
- `jacobian.matrix` — per-task sensitivity rows (∂taskᵢ/∂fieldⱼ)
- `envelopes[].ring` — cognitive ring assignment (generator/epistemic_floor)
- `summary.by_ring` — count breakdown per ring

The G-score itself is not yet computed in the route — all four terms (A from encoder, P from Jacobian, E from envelopes dispatched, h from EMD log) are available but need the dual-sensitivity bridge to compute G live.

## Anthropic Global Workspace Alignment (2026-07-25)

| Anthropic finding | Our implementation |
|------------------|-------------------|
| LLMs have an internal global workspace | J-space = explicit, governed, federated workspace |
| Workspace is implicit, per-forward-pass | J-space is structured, cross-session (via Jacobian persistence) |
| No governance over workspace content | F1-F13 membrane gates every workspace entry |
| No anomaly detection | EMD gate + tri-witness = ToAC physics |
| No metabolism | Δ encoder → Ω decoder → Ψ metabolizer |

## 7 Axioms in Jacobian Terms

1. **Multiplicativity** — zero in any Jacobian field collapses G
2. **Five-sufficient** — three Jacobian pairs + one ToAC witness
3. **Nash bargaining** — G = ∏ p_i because veto = multiplicative gate
4. **Shadow** — C_dark = A·(1-P)·(1-X) < 0.30 (sensitivity gaps)
5. **Conservation** — dS/dt ≤ 0 (metabolic Jacobian update)
6. **Tri-witness** — Φ = ∛(H·AI·Ext) ≥ 0.70 (EMD gate)
7. **F13 veto** — only sovereign overrides G (888-HOLD)
