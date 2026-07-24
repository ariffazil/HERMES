# arifOS Genius Enforcement Architecture (F8 GENIUS)

Reference for understanding how G scores are computed and enforced in the kernel.

## `core/enforcement/genius.py`

The `calculate_genius()` function computes the Unified Genius Equation:
```
G = A · P · E · X · Φ × (1 - h)
```

Where dials (A/P/X/E) are derived via PCA eigendecomposition (≥5 observations) or geometric mean cluster projection (fallback).

### Return Dict Fields (as of 2026-07-12)

```python
{
    "genius_score": float,          # Final G score (0.0-1.0)
    "dials": dict,                  # A/P/X/E/PHI dial values
    "hysteresis": float,            # Hysteresis factor
    "passed": bool,                 # G >= 0.80
    "verdict": str,                 # "SEAL" / "PARTIAL" / "VOID"
    "derivation": str,              # "pca_eigendecomposition" / "cluster_projection"
    "derivation_meta": dict,        # PCA metadata
    "provenance": str,              # "constitutional_measurement"
    "phi_witness": float,           # Witness dial
    # Dalio 17x fields (added 2026-07-12):
    "probe_signal": bool,           # True when G < 0.80
    "confidence_gap": float,        # max(0.0, 0.80 - G)
    "recommended_action": str,      # "ACT" / "PROBE" / "REJECT"
    "information_ev_multiplier": float,  # min(17.0, 17.0 * gap) or 0.0
}
```

### Verdict Logic

```python
G >= 0.80  →  SEAL   (act — confidence above threshold)
0.60 <= G < 0.80  →  PARTIAL (don't act — probe more)
G < 0.60  →  VOID   (reject — too uncertain)
```

### 17x Probe-vs-Act Signals

| G Score | probe_signal | recommended_action | information_ev_multiplier |
|---|---|---|---|
| 0.85 | False | ACT | 0.0 |
| 0.72 | True | PROBE | 1.36 |
| 0.60 | True | PROBE | 3.40 |
| 0.40 | True | REJECT | 6.80 |
| 0.10 | True | REJECT | 11.90 |

**Formula:** `information_ev_multiplier = min(17.0, 17.0 * (0.80 - G))` when G < 0.80, else 0.0.

## `core/judgment.py` → `CognitionResult`

The judgment layer consumes genius scores and produces constitutional verdicts.

```python
@dataclass
class CognitionResult:
    verdict: str              # SEAL, VOID, SABAR, PARTIAL
    truth_score: float
    genius_score: float
    grounded: bool
    floor_scores: dict[str, float]
    module_results: dict[str, Any]
    probe_signal: bool = False         # From genius (17x)
    recommended_action: str = "ACT"    # From genius (17x)
    # ... other fields
```

## How to Check

```bash
# Run genius-related tests (targeted — full suite times out)
cd /root/arifOS
grep -rl "genius\|calculate_genius\|CognitionResult" tests/ | head -5
python -m pytest tests/golden/organs/mind/test_mind_golden.py tests/test_minda.py -q

# Verify genius output programmatically
python -c "
from core.enforcement.genius import calculate_genius, coerce_floor_scores
floors = coerce_floor_scores({})
result = calculate_genius(floors)
print(result['verdict'], result['probe_signal'], result['recommended_action'])
"

# Lint check
ruff check core/enforcement/genius.py core/judgment.py
```

## Enforcement Points Summary

| Layer | File | What It Does |
|---|---|---|
| Scoring | `core/enforcement/genius.py` | Computes G, derives dials, returns probe signals |
| Judgment | `core/judgment.py` | Consumes G, produces CognitionResult with verdict |
| MCP Intercept | `arifosmcp/tools/arif_kernel_intercept.py` | Gates actions (ALLOW/DENY/ESCALATE/SABAR) |
| Decision Thresholds | `arifosmcp/runtime/tools.py` | Advisory confidence bands |

**Key insight:** The genius layer (scoring) and the intercept layer (gating) are separate enforcement points. A change to F8 threshold logic goes in `genius.py`. A change to action gating goes in `arif_kernel_intercept.py`. Don't confuse them.
