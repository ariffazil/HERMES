# Cross-Organ Wiring Pattern — arifOS Kernel Integration

Pattern for connecting external engines into arifOS kernel's `arif_judge` flow.

## Architecture

```
External Engine (A-FORGE / WELL / custom)
    ↓ writes state to /tmp/<engine>_state.json
arifOS Kernel Enforcement Gate (new file)
    ↓ reads state, evaluates, returns flags
arifOS judge.py
    ↓ imports gate, calls after somatic gate
arif_judge verdict
```

## Step-by-Step

### 1. Create gate module in enforcement directory

```python
# /root/arifOS/arifosmcp/core/enforcement/<your>_gate.py

from __future__ import annotations
import json, os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_STATE_PATH = "/tmp/<engine>_state.json"

@dataclass
class GateResult:
    """Result of gate evaluation."""
    verdict: str  # "PASS", "FLAGGED", "HOLD"
    details: dict

    def to_dict(self) -> dict:
        return {"verdict": self.verdict, **self.details}

def evaluate_gate(evidence: Optional[dict] = None) -> GateResult:
    """Evaluate the gate. Called from judge.py."""
    try:
        if not os.path.exists(_STATE_PATH):
            return GateResult(verdict="PASS", details={"reason": "no state"})
        state = json.loads(Path(_STATE_PATH).read_text())
        # ... evaluate based on state ...
        return GateResult(verdict="PASS", details={...})
    except Exception:
        return GateResult(verdict="PASS", details={"reason": "gate error"})
```

### 2. Wire into judge.py

Location: `/root/arifOS/arifosmcp/tools/judge.py`

**Add import** (near line 47, after somatic_loop import):
```python
from arifosmcp.core.enforcement.<your>_gate import (
    evaluate_<your>_gate,
)
```

**Add gate call** (after the somatic state gate, before self-modification lock):
```python
# ── YOUR GATE (description) ──────────────────────────────────
_result = evaluate_<your>_gate(evidence=_evidence)
_evidence["<your>_gate"] = _result.to_dict()
if _result.verdict == "FLAGGED":
    # Append flags but do NOT auto-block (F5 PEACE)
    for _f in _result.details.get("flags", []):
        _evidence.setdefault("<your>_flags", []).append(_f)
```

### 3. Gate placement in judge.py flow

```
arif_judge()
  → MARUAH critic gate
  → Somatic state gate (machine telemetry → CRITICAL = HOLD)
  → YOUR GATE ← insert here
  → Self-modification lock
  → Deliberation
  → Verdict
```

### 4. Cross-organ state sharing

External engines write state to `/tmp/<engine>_state.json` (or `/var/arifos/` for persistent state).
Kernel gates read from the same path.

**Convention:**
- `/tmp/` = ephemeral, cleared on reboot, OK for session-scoped state
- `/var/arifos/` = persistent, for state that survives reboots
- State files are JSON, written atomically (write to .tmp, rename)

### 5. Existing enforcement directory

```
/root/arifOS/arifosmcp/core/enforcement/
├── somatic_loop.py          # Machine telemetry → NOMINAL/STRESSED/CRITICAL
├── paradox_gate.py          # Active paradoxes → resolution risk flags
├── drift_detector.py        # Semantic drift detection
├── governance_alerts.py     # Governance alert routing
├── grandiosity_filter.py    # Overclaim detection
├── maruah_critic.py         # Dignity/ethics critique
├── ontology_budget.py       # Ontology boundary enforcement
├── risk_classifier.py       # Risk level classification
└── sfag.py                  # Self-referential feedback guard
```

## Pitfalls

- **Gates are FLAGS, not BLOCKS** (unless they detect CRITICAL/IRREVERSIBLE state). F5 PEACE: de-escalate, don't choke.
- **F9 ANTIHANTU**: Gates read STRUCTURAL state, not "feelings." Never claim the gate "senses" or "perceives."
- **Import placement matters**: Add imports near the existing enforcement imports (~line 43-47).
- **Gate placement matters**: After somatic gate, before self-modification lock.
- **State file format**: JSON. Include a `verdict` field. Include enough detail for `arif_judge` evidence.

## Provenance

Session: 2026-07-11. Wired paradox_gate.py into arifOS kernel.
Pattern: A-FORGE paradox engine writes state → arifOS kernel reads → flags in arif_judge evidence.
