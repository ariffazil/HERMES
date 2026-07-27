# J-Space / Jacobian Shadow Probe

**Forged:** 2026-07-26  
**Source:** arifOS kernel forge session — INIT shadow measurement wiring  
**Code:** `arifosmcp/tools/shadow_probe.py`  
**Concept:** Measure the stability of system trajectory against small perturbations in INIT conditioning — the J-space Jacobian.

## The Idea

J-space is not a literal mathematical Jacobian (∂output/∂input matrix). It is a **conceptual sensitivity map**: if a small change in INIT parameters (actor_id, intent, authority) produces a large change in the output trajectory, that region of the possibility space is fragile. If small changes produce the same stable trajectory, the region is robust.

APEX G (governance alignment) can then be reinterpreted: G is not a score from a model. G is the **integral of all constraints that collapsed infinite possibility into one chosen trajectory**. A trajectory that emerges consistently across small perturbations has high G. A trajectory that flips dramatically on minor conditioning changes has low G.

## The Probe (as of 2026-07-26)

`probe_shadow(model_input, reference_domain)` returns measured values for four scalars:

| Scalar | What it Measures | Method |
|---|---|---|
| **G** | Governance alignment — contradiction scan result | GEOX `geox_contradiction_scan` proxy or word-level fallback |
| **C_dark** | Latent chaos / hantu patterns — entropy-based | Character-level adaptive entropy (proxy for logit distribution shape) |
| **W3** | Witness weight — evidence source diversity count | URL/citation/evidence ID counter |
| **h** | Humility — confidence calibration assessment | Pattern classifier: overconfident markers vs uncertainty markers |

Each returns a real measured value between 0.0 and 1.0, or honest `"UNMEASURED"` when the probe cannot run.

## Wiring to INIT

In `arifosmcp/tools/session.py` `_project_light()`, the SCT minting step:

1. Checks if `intent` is provided
2. If yes, calls `probe_shadow(intent, "agentic_boundary")`
3. If probe returns real measurements (G != "UNMEASURED"), uses them as `apex_scalars`
4. On probe failure or blank intent, falls through to `unmeasured_apex()` (all UNMEASURED)

This means every `arif_init` call with an intent now carries **real shadow telemetry**, not placeholder values.

## The 5-Layer Agency Hierarchy

```
Layer 1 — Identity    (who am I?)       → actor_id, lane
Layer 2 — State       (what do I know?) → memory context, evidence history
Layer 3 — Boundary    (what are my constraints?) → authority, F1-F13 floors
Layer 4 — Intent      (what is my purpose?) → declared goal, domain
Layer 5 — Confidence  (how certain am I?) → apex scalars G, C_dark, W3, h
         ↓
Trajectory — chosen action from the possibility space collapsed by layers 1-5
```

J-space probes layer 5 at the moment of INIT, providing the first real measurement of whether the system's declared confidence matches its latent state.

## Deployment Drift as J-Space Violation

A specific pattern: when `deployment_invariant.drift = true` (source_commit ≠ built_commit), the J-space is fundamentally fragile. The agent operates on code that does not match its source. Even if all 5 layers look consistent, the **execution substrate** is not aligned with the **declared identity**. The health endpoint now reports DEPLOYMENT=down when drift is detected.

## Affected Files

| File | Change |
|---|---|
| `arifosmcp/tools/shadow_probe.py` | NEW — probe_shadow() implementation |
| `arifosmcp/tools/session.py` | Wired shadow probe into _project_light() SCT minting |
| `arifosmcp/runtime/rest_routes/observatory_routes.py` | Added DEPLOYMENT state to seven_state_health() |
| `arifosmcp/runtime/sct.py` | unmeasured_apex() remains as fallback |
