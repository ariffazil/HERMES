# APEX G Formula Standardization — Worked Session (2026-07-28)

> ⛔ **HISTORICAL — SUPERSEDED BY V3 (2026-07-28).**
> This document describes the V2 canonical formula `G = A·P·E·X·Φ` (product, 5 factors, Φ dial).
> **Do NOT apply this formula.** The current canonical is `G = (A×P×E×X)^(1/4)` (geometric mean, 4 factors, NO Φ).
> See `references/apex-g-formula-constitutional-convergence-v3-2026-07-28.md` for the current canonical.
> Both documents are kept for historical audit trail purposes only.

## Task
Standardize ALL drifted G formula variants across A-FORGE to canonical `G = A · P · E · X · Φ` (product, 4dp precision). Fix 6 files, run empirical tests, verify Nash collapse and equivalence. Do NOT break compilation.

## Canonical Source (V2 — superseded)
`/root/arifOS/arifosmcp/runtime/apex_primitives.py:146`:
```python
# G = A · P · E · X · Φ
G = round(A * P * E * X * PHI, 4)
# C_dark = A · (1-P) · (1-X)
C_dark = round(A * (1 - P) * (1 - X), 3)
```

## Drift Inventory

| # | File | Line | Type | Drift | Fix |
|---|------|------|------|-------|-----|
| 1 | `APEXRuntimeReceipt.ts` | 12 | Comment | `G = A·P·E·X` (missing Φ) | `G = A·P·E·X·Φ` |
| 2 | `APEXRuntimeReceipt.ts` | 49 | Type union | `APEXDimension = "A"\|"P"\|"E"\|"X"` (missing "Φ") | Add `"Φ"` |
| 3 | `APEXRuntimeReceipt.ts` | 52-55 | Interface | `APEXScores` missing Phi field | Add optional `Phi?: number` |
| 4 | `APEXRuntimeReceipt.ts` | 70 | Interface | `APEXReceipt` missing Phi field | Add `Phi: number` |
| 5 | `APEXRuntimeReceipt.ts` | 119 | Runtime | `round(a·p·e·x·1000)` — 4-term, 3dp | `round(a·p·e·x·phi·10000)` — 5-term, 4dp |
| 6 | `APEXRuntimeReceipt.ts` | 167 | Function | `estimateAPEXX()` no phi param | Add optional `phiSignals=1.0` |
| 7 | `apexDials.ts` | 8 | Comment | `G = (A·P·E·X)^(1/4)` — GM | `G = A·P·E·X·Φ` — product |
| 8 | `apexDials.ts` | 225-227 | Runtime | `geometricMean([A,P,E,X])` — GM | `A·P·E·X·phi` — product |
| 9 | `apexDials.ts` | 289 | String | `"G=(A·P·E·X)^(1/4)"` | `"G = A·P·E·X·Φ"` |
| 10 | `apexDials.ts` | 360-362 | Runtime | `geometricMean([A,P,E,X])` — GM | `dials.A·dials.P·dials.E·dials.X` — product |
| 11 | `apexDials.ts` | 411 | Display | `"G = (A·P·E·X)^(1/4)"` | `"G = A·P·E·X·Φ"` |
| 12 | `AgentEngine.ts` | 879 | Comment | `G = A × P × X × E²` | `G = A · P · E · X · Φ` |
| 13 | `AgentEngine.ts` | 902 | Display | ordering `A,P,X,E` | correct ordering `A,P,E,X` + add `Φ=1.0` |
| 14 | `taskJacobian.ts` | 14 | JSDoc | `G = (A·P·X·E²)·(1-h)` | `G = A·P·E·X·Φ` |
| 15 | `taskJacobian.ts` | 303 | Runtime | `A·P·X·E²·(1-h)` — E², missing Φ | `A·P·E·X·(1-humilityCap)` where `Φ=1-h` |
| 16 | `cognition/index.ts` | 23 | JSDoc | `G = (A·P·X·E²)·(1-h)` | `G = A·P·E·X·Φ` |
| 17 | `reality-loop/types.ts` | 334 | Comment | `G = Q·V·Ψ·Φ` (wrong formula) | `G = A·P·E·X·Φ` |

**Total: 17 drift sites across 6 files.**

## Files Modified (V2 sweep)

| File | Patches | Purpose |
|------|---------|---------|
| `src/domain/governance/APEXRuntimeReceipt.ts` | 6 | Added Φ to types, interface, G formula, estimate function |
| `src/domain/governance/apexDials.ts` | 5 | Changed geometric mean to product, added Φ, updated display |
| `src/domain/engine/AgentEngine.ts` | 2 | Fixed comment + display string |
| `src/domain/cognition/taskJacobian.ts` | 2 | Fixed formula + JSDoc |
| `src/domain/cognition/index.ts` | 1 | Fixed JSDoc |
| `src/domain/reality-loop/types.ts` | 1 | Fixed comment |
| `test/apex_g_standardization.test.ts` | — | New 8-assertion test suite |
