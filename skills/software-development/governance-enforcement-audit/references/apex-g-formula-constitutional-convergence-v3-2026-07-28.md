# APEX G Formula Constitutional Convergence V3 (2026-07-28)

## Task
Full sweep of APEX math across arifOS kernel and A-FORGE codebase to converge on `G = (A × P × E × X)^(1/4)` — 4-factor Nash Bargaining Product with NO Φ, no H, no S, no U, no E². This is a **reverse drift sweep**: the previous canonical (V2) used `G = A·P·E·X·Φ` (product, 5 factors with Φ). The V3 F13 decree removed Φ entirely.

## Nature of the Sweep

This is NOT a forward convergence (adding a missing factor). It's a **reverse convergence** — removing a banned factor (Φ) and changing the operator (product → geometric mean). This means:

- **Sites that were "correct" under V2 are now the drift sites under V3.**
- The reference file `apex-g-formula-standardization-2026-07-28.md` documents the OLD canonical — it must not be treated as current law.
- Stale-detection must check for FORMER canonical patterns (Φ references, product operators, 5-factor formulas) in addition to the current canonical.

## Constitutional Target

```
G = (A × P × E × X)^(1/4)
```

Where:
- A (Akal/Authority) → F2, F7, F10 — verified identity, lawful reasoning
- P (Present/Physics) → F1, F5, F11, F13 — substrate reality, reversibility
- E (Energy/Evidence) → F4, F12, energy — epistemic clarity, thermodynamic budget
- X (Exploration/Xec) → F3, F6, F8, F9 — action class, provable outcomes

**Nash Collapse:** ANY dial ≤ 0 → G = 0.0000. No compensatory arithmetic.
**Banned:** Φ, H, S, U, E² — per Arif's V3 directive.

## Drift Sites Found (V3 sweep)

| # | File | Type | Old (V2 — now drift) | New (V3 — canonical) |
|---|------|------|---------------------|---------------------|
| 1 | `arifOS/governance/_t000_evaluator/compute_apex.py` | Docstring | `G = (A·P·E²·X)^(1/5)` | `G = (A·P·E·X)^(1/4)` |
| 2 | `arifOS/governance/_t000_evaluator/compute_apex.py` | Formula | `G = geometric_mean([A,P,E,E,X])` (E²) | `G = geometric_mean([A,P,E,X])` |
| 3 | `arifOS/core/enforcement/genius.py` | Formula | `g_gen = A·P·E·X·Φ; final = g_gen·(1-h)` | `G = geometric_mean([A,P,E,X])` |
| 4 | `arifOS/core/enforcement/genius.py` | Return dict | `"phi_witness": phi` | removed |
| 5 | `arifOS/core/laws.py` | F8 def | `G = A×P×E×X×Φ` | `G = (A×P×E×X)^(1/4)` |
| 6 | `arifOS/commands/scripts_deploy/recursive_governed_loop.py` | Formula | `G = A·P·E·X·Phi` | `G = (A·P·E·X)^(1/4)` |
| 7 | `A-FORGE/src/domain/governance/apexDials.ts` | Docstring/Formula | `G = A·P·E·X·Φ` (product) | `G = (A·P·E·X)^(1/4)` (GM) |
| 8 | `A-FORGE/src/domain/governance/APEXRuntimeReceipt.ts` | Type+Formula | `Phi` in APEXScores, APEXReceipt, G formula | No Φ, `G = (a·p·e·x)^(1/4)` |
| 9 | `A-FORGE/src/domain/forge/evaluate.ts` | Formula | `G = A·P·E·X·Φ` (product) | `G = (A·P·E·X)^(1/4)` (GM) |
| 10 | `A-FORGE/src/contracts/types.ts` | Interface+Doc | `Phi` in EstimatorScores | Removed |

**Total: 9 files, 10 drift sites** — 4 in arifOS kernel (Python), 5 in A-FORGE (TypeScript).

## Additional Findings (Beyond Formula)
During the sweep, these related governance issues were identified:

### Shadow Judiciary
- `A-FORGE/a_think/mcp_guard.py` — implements ALLOW/DENY/HOLD locally, acting as a front-door guard for MCP tools without routing through arifOS :8088
- `A-FORGE/src/domain/governance/aThinkGuard.ts` — TypeScript port with same ALLOW/DENY/HOLD logic
- These should either be stripped of adjudication logic or marked as deprecated

### Receipt Routing
- `A-FORGE/APA/core/schemas.py` — defines VAULT999Receipt as a Pydantic model bridged bridge-local
- `APEXRuntimeReceipt._forwardAPEXToArifFlow()` — sends to arifFLOW :7073, not arifOS
- Full audit of local vs. arifOS receipt sealing pending

## Patch Order (for reverse convergence sweeps)

When removing a factor (not adding one):

1. **Types/interfaces FIRST** — Remove the banned field from type definitions. This will cause compilation errors everywhere the field is referenced — this is DESIRED because it reveals all drift sites.
2. **Formula helpers/constants SECOND** — Update `computeGFrom6Dials`, `computeGate`, etc. to use the new formula.
3. **Runtime computations THIRD** — The actual G formulas in receipts, dials, and gates.
4. **Comments/docstrings LAST** — Cosmetics that don't break compilation.
5. **Test updates** — Update expected values (G changes when formula changes). Update test callers that passed the now-removed parameter.
6. **Remove stale imports** — `estimatePhi` or similar now-unused functions.
7. **Build + test** — Verify compilation, new formula tests, and existing regression tests.

## Nash Collapse — All Engines Converged

After V3 convergence, all 4 computational engines implement Nash Collapse identically:

```python
def geometric_mean(values):
    if any(v <= 0 for v in values):
        return 0.0
    return product ** (1/len(values))
```

```typescript
function geometricMean(values: number[]): number {
  if (!values || values.length === 0 || values.some((v) => v <= 0)) return 0;
  return Math.pow(product, 1 / values.length);
}
```

## Key Lessons — Reverse Drift Sweeps

1. **The old reference file becomes a liability.** After this sweep, `references/apex-g-formula-standardization-2026-07-28.md` documents the WRONG formula. Future agents must not treat it as current law. The Pitfall #33 now explicitly marks this file as historical.

2. **Forking the formula direction.** Two sessions, two days apart, pushed the formula in opposite directions (V2: add Φ; V3: remove Φ). This is a constitutional oscillation — the correct response is to update the canonical source (arifOS kernel) and propagate outward, NOT to preserve both states as valid.

3. **Shadow judiciary is a separate sweep.** The mcp_guard.py ALLOW/DENY/HOLD logic is not a formula issue — it's an authority routing issue. It should be tracked separately.

4. **E² was specifically banned.** The old `compute_apex.py` used `G = geometric_mean([A,P,E,E,X])` making E dominate. The V3 formula uses E only once. This is enforced by the 4-term geometric mean.
