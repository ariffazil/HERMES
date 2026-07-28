# APEX G Constitutional Convergence — NEW Canonical (2026-07-28)

## Constitutional Directive

The canonical formula **changed** by constitutional decree (F13-ratified). Previous canonical `G = A·P·E·X·Φ` is **superseded**.

### New Canonical

```
G = (A × P × E × X)^(1/4)
```

**Nash Collapse rule is ABSOLUTE:** if ANY dial ≤ 0, G = 0.0000. No compensatory arithmetic.

### Dial Definitions

| Dial | Name | Meaning | Zero if |
|------|------|---------|--------|
| **A** | Authority | Verified identity, cryptographic signature, valid session lease | Any component adjudicates without kernel authority |
| **P** | Physics/Present | Substrate reality, physical constraints, reversibility (F1/F7) | State/receipts split across organs |
| **E** | Energy/Evidence | Epistemic clarity, source citation, thermodynamic entropy (F2/F4) | Same computation runs in multiple places |
| **X** | Execution/Exploration | Action class within lease bounds, provable outcomes | Execution bypasses 888_JUDGE → 777_FORGE → 999_SEAL chain |

### HARAM Terms (explicitly forbidden)

- **Φ (Phi) dial** — removed. Dials are exactly A, P, E, X. No fifth factor.
- **E²** — E enters exactly once. Squaring E is HARAM.
- **H (Hysteresis)** — `(1-h)` factor is HARAM.
- **S, U, or any other dial** — not in the canonical set.
- **^(1/5)** — exponent is exactly ^(1/4) (geometric mean of 4 terms). ^(1/5) is HARAM.
- **Product without GM** — G = A·P·E·X (raw product) is HARAM. The canonical form is the geometric mean (A·P·E·X)^(1/4).

## Drift Sites Found

After convergence from `A·P·E·X·Φ` to `(A×P×E×X)^(1/4)`, ALL sites that still use the old formula or any other variant are now drift:

| File | Line | Old Formula | New Fix Required |
|------|------|------------|-----------------|
| `arifOS/core/enforcement/genius.py` | 15 | `G = A·P·E·X·Φ` (product) | `G = (A*P*E*X)**0.25` — remove Φ, add GM |
| `arifOS/governance/_t000_evaluator/compute_apex.py` | 3, 129-130 | `G = (A·P·E²·X)^(1/5)` | `G = (A·P·E·X)^(1/4)` |
| `A-FORGE/src/domain/governance/apexDials.ts` | 226-228 | `A*P*E*X*phi` (product) | `(A*P*E*X)**0.25` |
| `A-FORGE/src/domain/governance/apexDials.ts` | 338 | `GM([eF, eF, eF, e1, e2])` (E² pattern) | `GM([eFloors, energy1])` |
| `A-FORGE/src/domain/governance/apexDials.ts` | 362-364 | `A*P*E*X` (product) | `(A*P*E*X)**0.25` |
| `A-FORGE/src/domain/governance/apexDials.ts` | 518-520 | `GM([A,P,E])*X` (hybrid) | `GM([A,P,E,X])` |
| `arifOS/docs/APEX_FALSIFIABILITY_PROTOCOL.md` | 62 | `G = A*P*E*X` (product) | `G = (A×P×E×X)^(1/4)` |
| `arifOS/commands/scripts_deploy/recursive_governed_loop.py` | 151 | `A*P*E*X*Phi` (product+Φ) | `(A*P*E*X)**0.25` |
| `arifOS/docs/APEX_CANON.md` | 5 | `G = (A·P·E²·X)^(1/5)` | `G = (A×P×E×X)^(1/4)` |
| `root/CLAUDE.md` | 159 | `G = (A·P·E²·X)^⅕` | `G = (A×P×E×X)^(1/4)` |
| `arifOS/AGENTS.md` | 228 | `G = (A·P·X·E²)·(1-h)` | `G = (A×P×E×X)^(1/4)` |
| `paper_trading/governed_engine.py` | 361 | `(A×P×E×X)^(1/4)` ✅ | Already correct — reference implementation |

**Total: 10+ drifted sites across 7 files.** Plus 6 static doc files with stale formulas.

## Key Lessons

1. **A constitutional formula change creates a NEW drift set.** All sites that were "canonical" under the old formula become drift under the new one. The old reference file (`apex-g-formula-standardization-2026-07-28.md`) is now history, not law.
2. **Φ removal is not additive like adding a missing factor.** The old canonical had 5 factors (A·P·E·X·Φ). The new one has 4 factors (A·P·E·X). Every site that still has Φ or a 5th factor is drift.
3. **^(1/4) vs product is not just a notation difference.** Product (A·P·E·X) collapses to zero when any dial is zero, same as GM. But GM (A·P·E·X)^(1/4) returns the geometric mean, not the raw product. For (0.8, 0.8, 0.8, 0.8): product=0.4096, GM=0.8. These are different values. The constitutional choice is GM, which is the Nash Bargaining Product.
4. **Tests must be rewritten, not just code.** The existing `apex_g_standardization.test.ts` test validates against the old canonical (product, 5 factors). It must be rewritten to validate the new canonical (GM, 4 factors).
