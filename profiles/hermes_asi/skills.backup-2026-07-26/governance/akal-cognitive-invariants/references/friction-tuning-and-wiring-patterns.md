# AKAL — Friction Tuning Lessons & Wiring Patterns

> Practical lessons from building and tuning AKAL's friction scoring,
> wiring scattered kernel modules, and fixing the PRESENT broken import.

---

## Friction Scoring: Blast Radius Floor

**Problem:** Text-based friction scoring can produce LOW friction for irreversible actions
that happen to use simple language. A career-defining MSS decision phrased in plain
English scored 0.22 (LOW) without the floor.

**Fix:** Blast radius floor — the minimum friction score for each blast class:

```python
blast_floor = {"low": 0.0, "medium": 0.25, "high": 0.50, "irreversible": 0.80}
score = max(score, blast_floor.get(blast_radius, 0.0))
```

**Rule:** Irreversible actions can NEVER be low-friction. The blast radius floor ensures this.
Without it, the kernel treats "delete everything permanently" the same as "what time is it"
if the text doesn't contain enough regex pattern matches.

---

## Friction Scoring: Pattern Bank Tuning

**Problem:** Initial regex patterns were too narrow. Three failures found in stress test:

| Pattern | Failed Text | Fix |
|---|---|---|
| `\bpermanent\b` | "permanently" | `\bpermanently?\b` |
| (missing) | "seismic", "well log" | Add domain terms to `_CROSS_DOMAIN` |
| (missing) | "career", "livelihood" | Add human-impact terms to `_STAKES` |

**Rule:** Pattern banks must include the vocabulary the ACTUAL queries use, not just
abstract governance terms. Domain-specific terms (seismic, basin, petrophysics) belong
in `_CROSS_DOMAIN`. Human-impact terms (career, dignity, financial future) belong in
`_STAKES`.

**Weight tuning:** After stress test, blast_radius weight was increased from 0.20 to 0.30
(the single most important signal). Cross_domain increased from 0.10 to 0.15.

---

## Wiring Pattern: Connecting Scattered Modules to AKAL Hooks

When a kernel capability exists in scattered modules but isn't enforced as an invariant:

1. **Don't rewrite.** The computation already exists. Find it with grep.
2. **Create a thin hook** in `akal_wiring.py` that imports and calls the existing function.
3. **Wrap all imports in try/except** for graceful degradation:
   ```python
   try:
       from arifosmcp.core.physics.thermodynamics_hardened import get_thermodynamic_budget
   except ImportError:
       get_thermodynamic_budget = None
   ```
4. **Store results in AkalState** so the state travels through 000→999.
5. **Return results in hook output dict** so organs can inspect.
6. **Advisory first, mandatory later.** Don't block the pipeline on a newly-wired dial
   until it's proven.

**Key lesson:** The gap between "field exists in schema" and "invariant enforced in pipeline"
is where governance lives. AKAL was the first dial to cross that gap.

---

## PRESENT Fix: Missing `select_philosophy_state`

**Problem:** `sensing_protocol.py:49` imported `select_philosophy_state` from
`philosophy_registry.py` — function didn't exist. The try/except caught it silently,
so PRESENT never returned real reality state.

**Fix:** Added `select_philosophy_state()` to `philosophy_registry.py`. It computes a
`confidence_cap` based on:
- F7 HUMILITY base cap (0.90 — never 1.0)
- Gödel lock penalties (G1 incompleteness -0.15, G2 contradiction -0.10, etc.)
- Entropy penalty (high dS reduces cap)

**Signature:**
```python
def select_philosophy_state(
    confidence: float = 0.88,
    dS: float = 0.0,
    intervention: float = 0.5,
    session_id: str = "global",
    locks: list[str] | None = None,
) -> dict[str, Any]:
```

**Returns:** `{"confidence_cap": float, "locks_active": list, "entropy_dS": float, ...}`

**Rule:** When a function is imported but doesn't exist, the try/except prevents crashes
but also prevents the feature from working. Always verify that imported functions actually
exist in the target module.

---

## AkalState: Complete Field List

```python
@dataclass
class AkalState:
    # AKAL invariants (I1-I5)
    friction: FrictionResult | None      # I1 — 333_MIND
    shadow: ShadowTrace | None           # I2 — 555_HEART
    novelty: NoveltyResult | None        # I3 — 777_FORGE
    values: DualVerdict | None           # I4 — 888_JUDGE
    latency: LatencyRequirement | None   # I5 — 999_VAULT

    # APEX dials
    reality_class: str | None            # PRESENT: LIVE|CACHED|INFERRED|UNKNOWN
    thermo_exhausted: bool | None        # ENERGY-ENTROPY: budget status
    reversibility_level: str | None      # AMANAH: reversible|partial|irreversible

    # Metadata
    created_at: float
    cycle_stages: list[str]
```

The `completeness()` method now tracks 8 dimensions:
`I1_friction`, `I2_shadow`, `I3_novelty`, `I4_values`, `I5_latency`,
`PRESENT`, `ENERGY_ENTROPY`, `AMANAH`.

---

## Stress Test Results (17/17 PASS)

| Agent | Friction | Shadow | Novelty | Dual-Eval | Latency | Can Seal |
|---|---|---|---|---|---|---|
| A (baseline) | LOW ✅ | optional ✅ | optional ✅ | L5a only ✅ | no gates ✅ | YES ✅ |
| B (high-friction) | HIGH ✅ | mandatory ✅ | enforced ✅ | L5b required ✅ | branching ✅ | NO ✅ |
| C (irreversible) | CRITICAL ✅ | blocking ✅ | enforced ✅ | sovereign required ✅ | 300s cooling ✅ | NO ✅ |

---

*v1.0 — 2026-07-11. Tuning lessons from stress test + PRESENT fix.*
*DITEMPA BUKAN DIBERI*
