---
name: arifos-constitutional-floor-modification
description: "Modify arifOS constitutional floors (F1-F13) across AGENTS.md, public mapping, and kernel code. Covers the full lifecycle: docs, kernel enforcement, tests, SOT manifest."
triggers:
  - "upgrade F8"
  - "modify constitutional floor"
  - "change F1-F13"
  - "update floor definition"
  - "floor enforcement"
version: "1.0"
author: Hermes
date: 2026-07-12
---

# arifOS Constitutional Floor Modification

Constitutional floors (F1-F13) are defined in THREE places. All must be updated together.

## The Three Locations

| Location | File | What it governs |
|----------|------|-----------------|
| **Operational table** | `/root/AGENTS.md` line ~82 | Agent behavior rules |
| **Public mapping** | `/root/AGENTS.md` line ~105 | Public ↔ operational label bridge |
| **Kernel enforcement** | `/root/arifOS/core/enforcement/` | Programmatic floor checks |

## Modification Procedure

### Step 1: Update AGENTS.md Operational Table

Find the floor row in the `F1-F13 Floors` table:

```
| **F8** | GENIUS | Simplest correct path. `G ≥ 0.80` per Unified Mapping. |
```

Update the description. Keep the `| **F8** | GENIUS |` prefix intact.

### Step 2: Update AGENTS.md Public Abstraction Mapping

Find the floor row in the Double Registry table:

```
| **F8** | GENIUS | PARADOX | Simplest correct path (live) / hold contradictions without collapse (public) |
```

Update the Bridge column to reflect the change.

### Step 3: Update Kernel Enforcement

The kernel enforces floors in two files:

**`/root/arifOS/core/enforcement/genius.py`** — The `calculate_genius()` function:
- Returns a dict with `genius_score`, `verdict`, `passed`
- Verdict logic: `SEAL` if G ≥ 0.80, `PARTIAL` if G ≥ 0.60, `VOID` if G < 0.60
- To add new fields: add them to the return dict (around line 642)
- Keep existing fields unchanged for backward compatibility

**`/root/arifOS/core/judgment.py`** — The `CognitionResult` class:
- Dataclass with fields for each floor score
- To add new fields: add to the class definition AND wire through in the cognition method

### Step 4: Run Tests and Lint

```bash
cd /root/arifOS
python -m pytest tests/golden/organs/mind/test_mind_golden.py tests/test_minda.py tests/test_cognitive_tier_gate.py -q --tb=short
ruff check core/enforcement/genius.py core/judgment.py
```

### Step 5: Verify Kernel Behavior

```python
cd /root/arifOS
python -c "
from core.enforcement.genius import calculate_genius, coerce_floor_scores
floors = coerce_floor_scores({})
result = calculate_genius(floors)
print('verdict:', result['verdict'])
print('new_field:', result.get('new_field', 'MISSING'))
"
```

## Pitfalls

### PITFALL: Full test suite times out
The full test suite (`python -m pytest tests/`) takes >120s. Use targeted test files:
```bash
python -m pytest tests/golden/organs/mind/ tests/test_minda.py tests/test_cognitive_tier_gate.py -q
```

### PITFALL: Pre-existing LSP errors
`genius.py` and `judgment.py` have pre-existing NumPy typing errors. These are NOT caused by your changes. Only new errors matter.

### PITFALL: Backward compatibility
New fields in the return dict are additive. Existing callers that don't read new fields must not break. Never change the `verdict` logic (SEAL/PARTIAL/VOID thresholds) without sovereign approval.

### PITFALL: SOT Manifest
If the floor change is constitutional (changes what agents MUST do), update the SOT Manifest in AGENTS.md at the bottom of the file.

## Example: F8 17x Upgrade (2026-07-12)

Added Dalio's 17x principle to F8 GENIUS:

1. AGENTS.md operational: added "Below threshold → keep probing (information EV > action EV)"
2. AGENTS.md public mapping: added "17× threshold rule"
3. genius.py: added `probe_signal`, `confidence_gap`, `recommended_action`, `information_ev_multiplier`
4. judgment.py: added `probe_signal` and `recommended_action` to CognitionResult
5. Tests: 80/80 pass. Ruff: clean.
