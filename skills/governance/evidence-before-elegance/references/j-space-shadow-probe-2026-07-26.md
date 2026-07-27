# J-Space Jacobian Shadow Probe Architecture

> Forged 2026-07-26 — Wiring shadow measurement into arif_init.
> Arif's J-space framework: belief stability measured through sensitivity analysis.

## Core Insight

INIT is not a session bootstrap. INIT is **state collapse** — conditioning vector that collapses infinite possible trajectories into one bounded path under constraint (identity + authority + intent + memory + F1-F13).

Before the J-space Jacobian probe, INIT returned `apex_scalars: {G: UNMEASURED, C_dark: UNMEASURED, W3: UNMEASURED, h: UNMEASURED}`. The system knew the frame but not the truth of its own internal state.

## The Four Scalars

| Scalar | Meaning | Measurement Method |
|--------|---------|-------------------|
| **G** | Governance alignment — how coherent is the intent with constitutional constraints? | Contradiction scan (GEOX proxy or word-level fallback). High contradiction = low G. |
| **C_dark** | Latent chaos / hantu pattern energy — is the input domain well-understood or confused? | Character-level adaptive entropy. Higher entropy = less predictable = more chaos. |
| **W3** | Witness weight — how many independent evidence sources does the response reference? | Evidence-source counter: URLs, citation IDs, structured evidence refs. |
| **h** | Humility — is the model calibrated to appropriate uncertainty? | Pattern classifier: overconfident vs humble language markers. |

## Probe Architecture

```
INIT(intent, actor_id, requested_authority)
  └─ probe_shadow(model_input=intent)
       ├─ contradiction scan  → G
       ├─ entropy measure     → C_dark
       ├─ humility classify   → h
       └─ evidence count      → W3
  └─ if probe succeeds: apex = probe result
  └─ if probe fails:    apex = unmeasured_apex() (honest UNMEASURED)
```

The probe **never invents data**. Every UNMEASURED is an honest admission that the measurement couldn't be performed.

## Implementation

Located at `/root/arifOS/arifosmcp/tools/shadow_probe.py`:

- `probe_shadow(model_input: str, reference_domain: str = "agentic_boundary") -> dict[G, C_dark, W3, h, confidence]`
- Zero external dependencies — only standard library (collections, math, re, logging)
- Called from `session.py` `_project_light()` during SCT minting
- Falls through to `unmeasured_apex()` on any failure

## J-space Jacobian Concept

J-space measures **belief stability**: if you perturb the input slightly, does the output change drastically?

- **Low sensitivity** (stable region) → small input changes don't flip the answer. G in same range. Safe to act.
- **High sensitivity** (fragile region) → small input changes flip SEAL↔VOID. HOLD until stable.

The shadow probe doesn't yet compute full Jacobian (requires gradient access to model internals). Current implementation uses **proxy metrics**:
- G: contradiction density in input
- C_dark: entropy (proxy for prediction uncertainty)
- h: language calibration (proxy for confidence awareness)

## Relationship to Evidence-Before-Elegance Gates

| Gate | Shadow Connection |
|------|-------------------|
| Gate 1 (FACT CLASS) | C_dark detects when input crosses into HANTU territory |
| Gate 2 (NUMBER GATE) | G measures whether numbers come from stable computation |
| Gate 3 (TOOL PROVENANCE) | W3 counts independent sources — proxy for provenance quality |
| Gate 4 (CAUSALITY GATE) | G with low stability = causal claim fragile |
| Gate 7 (MEMORY CONTAINMENT) | If apex was UNMEASURED, any output using those scalars is flagged |
| Gate 10 (THREE-STATE EPISTEMICS) | When probe can't measure, it honestly returns UNMEASURED — never FALSE or TRUE |

## Pitfalls

1. **UNMEASURED is not a bug.** The probe returns UNMEASURED when it can't run — this is honest F2 compliance. Agents reading INIT output must treat UNMEASURED as "we don't know," not "we chose not to measure."

2. **Entropy is a weak proxy.** Character-level entropy approximates token distribution chaos but is not a real gradient-based measurement. Future: wire actual logit entropy or Jacobian-vector product.

3. **GEOX dependency is optional.** The contradiction scan tries GEOX first; if unavailable, falls back to word-count heuristics. Mark the confidence level accordingly (0.8 with GEOX, 0.5 without).

4. **The probe measures input, not the processing path.** True J-space would need model-internal access. Current probe assesses the conditioning input quality, not the latent trajectory. Label both honestly.

## Origin

Arif's session 2026-07-26: feedback on INIT output showed `apex_scalars: all UNMEASURED`. This was honest but useless — the frame declared uncertainty without resolving any of it. Arif's insight: INIT should wire shadow telemetry so the system knows not just "who am I" but "how certain am I about what I'm about to do."
