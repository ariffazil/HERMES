# G-Fold Flow Doctrine — Federation Vital Sign

**Sealed:** 2026-07-25  
**Author:** Hermes / Arif (F13)  
**Source:** Constitutional analysis session — G-fold as the federation's internal compass  
**Relationship:** Extends `apex-verification-pipeline` (which defines G's computation) with G's federation-wide circulation

---

## 1. G is NOT a sensor — it is a coherence gate

G = A · P · E · X · Φ is a **multiplicative Nash product**. This structure determines its behaviour:

- **Any primitive = 0 → G = 0 (VOID)** — instantaneous collapse, not gradual decay
- **All primitives ≥ 0.80 → G stays stably ≥ 0.80** — steady-state vital sign, not a fluctuating metric
- **G does NOT spike on anomaly** — the real early-warning signal is C_dark (shadow term), which rises gradually before G collapses
- **C_dark triggers HOLD faster than G drops** — a federation with high G but C_dark ≥ 0.30 HOLDs immediately

| Regime | G value | Dominant feel | Federation state |
|--------|---------|---------------|------------------|
| **SEAL** | ≥ 0.80 | All five primitives robust | Full trust, proceed |
| **SABAR** | [0.50, 0.80) | One or two primitives degraded | Conditional go, patience |
| **HOLD** | any (C_dark ≥ 0.30) | Shadow bound exceeded | Immediate stop |
| **VOID** | 0.0 | Any primitive zero — collapsed | Complete block |

---

## 2. Single computational source — constitutional rule

```
G is computed ONLY in:
  arif_think(mode='apex')
    → arifosmcp.runtime.apex_canonical.compute_apex()
    → module: arifosmcp.runtime.apex_canonical

CANONICAL_G_SOURCE = "arif_think.mode=apex"   (A-FORGE/src/domain/governance/gAuthority.ts)
```

Enforced at three levels:

1. **A-FORGE** — every local estimate stamps `g_authority: "local_estimate"`, `derived_local: true`. `gAuthority.ts` exists solely to prevent local G from being mistaken for canonical.
2. **AAA/cockpit** — UI displays tagged `wire_estimate_not_canonical`.
3. **ScalarCollector** — `collect_G()` refuses non-apex-tagged sources; returns UNMEASURED (F9 anti-hantu) when no apex derivation present.

**No organ may self-certify its own G.** Not GEOX, not WELL, not A-FORGE, not AAA.

---

## 3. Circulatory path — contributors → kernel → consumers

```
                    CONTRIBUTORS (INPUTS)
  GEOX ──→ P (physics: well/seis/geo evidence)
  WELL ──→ H_witness → Φ (human vitality signal)
  arifOS ──→ A (floor compliance, lease validity)
  A-FORGE ──→ X (execution success, ΔS stability)
  AAA ──→ Ext_witness → Φ (civilizational mesh)
  VAULT999 ──→ E (Merkle chain integrity, clarity)

                        │
                        ▼
              KERNEL (single source)
              arif_think(mode='apex')
              G = A·P·E·X·Φ
              G_seal = G_raw · (1-h) · |ΔS|^β · W³
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
     nine_signal.Ω  ScalarCollector  Health endpoint
     (omega plane)  → arif_judge    :8088/health
                    meta.scalar_     nine_signal
                    snapshot
                        │
                        ▼
                Verdict: SEAL/
                SABAR/HOLD/VOID
```

**2026-07-26 update:** Organs now also CONSUME G by fetching kernel `/health`. GEOX proxies it in its own `/health`. WELL uses it to gate C4/C5 decisions. A-FORGE uses it in the 4-layer forge gate via `computeGateWithKernelG()`. G is no longer judge-private.

---

## 4. Nine-signal translation — G → felt experience

G enters the nine-signal as **Ω (omega) = intelligence discipline plane**:

| Ω state | G range | Malay | English |
|---------|---------|-------|---------|
| WISE | ≥ 0.80 | BIJAKSANA | WISE |
| SMART | [0.50, 0.80) | BIJAK | SMART |
| FOOLISH | < 0.50 | BANGANG | FOOLISH |

**Overall nine-signal = MIN(Δ_state, Ψ_state, Ω_state)** — the worst plane dominates. G alone is never sufficient: read all three planes (Δ = machine health, Ψ = governance/C_dark, Ω = intelligence/G).

---

## 5. Live Probe Verification — Current vs Doctrine

Probed 2026-07-27 from federation source code and runtime health endpoints:

### Per-Organ G-Source Table

| Organ | Health Endpoint G | Status | Source Tag | Verdict |
|-------|-------------------|--------|------------|---------|
| **GEOX** (:8081) | Live-fetched from kernel | RESOLVED | Kernel proxy + UNMEASURED fallback | ✅ **F2 FIXED 2026-07-26** — Was hardcoded 0.5 NOMINAL (F2 violation). Now auto-fetches `apex_scalars` from kernel `/health` response; on failure returns `{value: None, status: "UNMEASURED"}`. Piggybacks on existing kernel health probe — zero extra round-trips. |
| **WELL** (:18083) | Live-fetched | CONSUMED | G-fold wired 2026-07-26 | ✅ Gap closed — `_get_live_G()` in `well_assess_homeostasis` fetches kernel G and gates C4/C5 downgrades. See `g-fold-organ-consumption-pattern.md`. |
| **A-FORGE** (:7071) | Hybrid — kernel G preferred, local fallback | HYBRID RESOLVED | `arif_think.mode=apex` when reachable, `local_estimate` on fallback | ✅ **WIRED 2026-07-26** — `GovernanceBridge.fetchCanonicalG()` queries kernel `/health`; `evaluate.ts:computeGateWithKernelG()` uses kernel G as Layer 2 of 4-layer forge gate, falls back to local A·P·E·X·Φ if kernel unreachable. Authority stamp changes accordingly. tsc build passes. |
| **AAA** (:3001) | Not in /health | — | Contract says arif_think() | ⚠️ No live consumption. |
| **WEALTH** (:18082) | Not in /health | — | — | ⚠️ No G visibility. |
| **AAA** (:3001) | Not in /health | — | Contract says arif_think() | ⚠️ No live consumption. |
| **WEALTH** (:18082) | Not in /health | — | — | ⚠️ No G visibility. |

**Key finding (2026-07-26 delta):** Three organs now consume live G from the kernel — GEOX, WELL, A-FORGE. G is no longer judge-private. AAA and WEALTH remain unwired.

### Pre-Action Gate Doctrine

Every organ, before committing to an irreversible action, MUST read live G from the kernel:

| Gate | Organ | Action | Should |
|------|-------|--------|--------|
| Vitality check | WELL | Before approving C4/C5 task | ✅ DONE — `_get_live_G()` fetches kernel G; G < 0.50 → PROCEED downgraded to DEFER. See `g-fold-organ-consumption-pattern.md`. |
| Health display | GEOX | `/health` endpoint | ✅ DONE — live-fetched from kernel, UNMEASURED on failure |
| Layer 3 forge gate | A-FORGE | GovernanceBridge | ✅ DONE — `fetchCanonicalG()` in GovernanceBridge, `computeGateWithKernelG()` in evaluate.ts |
| Score synthesis | WEALTH | Before wisdom synthesis | If C_dark ≥ 0.30 → flag `epistemic_source: UNRELIABLE` |
| Agent spawn | Hermes | Before delegating to subagent | Read G from vitals; if HOLD → queue, don't forge |

### Implementation Invariant

> **Every organ's `/health` endpoint MUST surface its G-source as either `"arif_think(mode='apex')"` (canonical, fetched live) or `"UNMEASURED"` (honest — no fetch available). Hardcoded float stubs (e.g. GEOX's G:0.5 NOMINAL) are F2 violations.**

Canonical MCP path for any organ to read live G:

```
organ → arif_think(mode='apex') → kernel → apex_canonical.compute_apex()
                                           → {G, C_dark, primitives, verdict}
organ reads apex_scalars.G from response
organ also reads arifos://vitals for real-time snapshot
```

A-FORGE's GovernanceBridge (`/root/A-FORGE/src/domain/governance/GovernanceBridge.ts`) now has HTTP transport to the kernel (used for T0-T3 risk classification AND `fetchCanonicalG()`). It fetches G before every forge lease via `computeGateWithKernelG()`.

## 6. The compass property

Crystallised doctrine from Arif (2026-07-25), with live-gap overlay:

> **G is the federation's magnetic north. Every organ should align to it before acting, not just the judge before sealing.**

| Surface | Before (probed 2026-07-25) | After (2026-07-26) |
|---------|---------------------------|---------------------|
| A-FORGE pre-execution | Checks forge_evaluate, does NOT read G | ✅ `computeGateWithKernelG()` probes kernel G before lease start |
| WELL vitality gate | Has own G_WELL (local), no kernel G read | ✅ `_get_live_G()` fetches kernel G, gates C4/C5 |
| GEOX | Contributes P, hardcodes 0.5 | ✅ Live-fetched from kernel, UNMEASURED on failure |
| Health endpoints | GEOX hardcodes 0.5, WELL returns UNMEASURED | ✅ GEOX now live-fetches; WELL exposes `live_G` in homeostasis output |
| G's feel | Judge's private scalar | ✅ Three organs consume live G pre-action |

G is advisory, not blocking: "G-fold is advisory evidence. Only arif_judge may SEAL." Organs use G as **context for risk assessment**, not as a hard gate. The hard gate remains at 888_JUDGE.

---

## 6. Diagram reference

```
G = A · P · E · X · Φ

A = (valid_leases / total_leases) · (floor_compliance / 13)
P = w_well · P_well + w_seis · P_seis + w_geo · P_geo
E = (clarity / (1 + uncertainty)) · reversibility
X = (successful_steps / total_steps) · exp(-|ΔS_t|)
Φ = ∛(H · AI · Ext)   — Nash tri-witness

C_dark = A · (1-P) · (1-X)   — hallucination bound
dS/dt ≤ 0                    — conservation law

G_seal = G · (1-h) · |ΔS|^β · W³   — gate layer
```

---

## 7. Nine-signal → G mapping implementation

```python
# arifosmcp/runtime/tools.py :3458 — _nine_signal_from_apex (deprecated but canonical logic)
# Ω plane:
if G >= 0.80:    omega = ("BIJAKSANA", "WISE")
elif G >= 0.50:  omega = ("BIJAK", "SMART")
else:            omega = ("BANGANG", "FOOLISH")

# Overall = MIN(Δ, Ψ, Ω)
overall_map = {3: ("SELAMAT", "SAFE"), 2: ("RETAK", "DEGRADED"), 1: ("ROSAK", "FAILED")}
```

---

## 8. Constitutional references

- **Canonical compute:** `arifosmcp/runtime/apex_canonical.py` (595 lines, 7 axioms, 5 measurement laws)
- **Source authority label:** `A-FORGE/src/domain/governance/gAuthority.ts` (40 lines, single source constant)
- **Scalar feed to judge:** `arifosmcp/core/scalar_collector.py` (701 lines, F9 anti-hantu contract)
- **Implied by:** F8 GENIUS (G ≥ 0.80), F3 WITNESS (Φ), F7 HUMILITY (h gate), F9 ANTIHANTU (C_dark)
- **Federated by:** nine-signal telemetry at `:8088/health` → omega plane → federation-wide visibility
