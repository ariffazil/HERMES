---
name: arifos-runtime-module-authoring
description: Create new arifOS runtime modules (audit, fatigue, scoring, etc.) following project conventions — Pydantic v2, VAULT999 persistence, ruff clean, line budgets.
---

# arifOS Runtime Module Authoring

Canonical reference for creating new `arifosmcp/runtime/*.py` modules.

## Trigger
Use when the user asks to create a new arifOS runtime Python module — audit, fatigue, scoring, validation, or any governed utility.

**If the task requires Qdrant vector indexing, dual-gate architecture, blast-radius classification, or EMD pipeline integration, use `arifos-organ-forging` instead — this skill is for simple ~250-line runtime utilities only.**

## Pre-flight
1. Read the canonical template: `arifosmcp/runtime/rsi_audit.py` — docstring structure, imports, Pydantic v2 patterns, logger, module-level instances.
2. Check `arifosmcp/models/verdicts.py` for verdict enums (SealType, VerdictState).
3. Check `arifosmcp/runtime/tools.py` `_hold()` function for integration hook patterns.

## Conventions

### Docstring header
```python
"""arifosmcp/runtime/<name>.py — <brief>

(1) ComponentName: what it does, file path.
(2) SecondComponent: what it does.
...

Floors engaged: F... · DITEMPA BUKAN DIBERI 🔥🌎🧠🪙
"""
```

### Imports (ruff I001 clean)
```python
from __future__ import annotations

import json
import logging
...
from typing import Any, Literal

from pydantic import BaseModel, Field
```

- Use `from __future__ import annotations` so `X | None` works (no `Optional[X]`).
- Split all imports onto separate lines — ruff enforces I001/E401.

### Persistence
- JSON state files: `/root/VAULT999/<name>.json` — single dict, use `json.dumps(state)` (no `indent=2` to save lines).
- JSONL append-only logs: `/root/VAULT999/<name>.jsonl` — one JSON object per line.
- Always `mkdir(parents=True, exist_ok=True)` before writing.

### Pydantic v2 Models
- Use `BaseModel` with `Field(default_factory=...)` for auto-generated IDs/timestamps.
- Use `Literal[...]` for constrained string enums.
- `model_validate_json(line)` for JSONL parsing, `model_dump_json()` for serialization.
- `model_copy(update={...})` for immutable updates.

### Time
- Always use `datetime.now(UTC)` — never naive datetimes.
- Date keys: `datetime.now(UTC).strftime("%Y-%m-%d")`.

### Module-level integration instances
```python
t3_counter = T3DailyCounter()
receipt_randomizer = ReceiptRandomizer()
review_scorer = ReviewConsistencyScorer()

def check_t3_fatigue_gate() -> dict[str, Any]:
    """Integration hook for tools.py."""
    return t3_counter.check_and_increment()

def reset_fatigue_state() -> None:
    """Reset state (testing only). Never call in production."""
    for p in (T3_DAILY_PATH, DEEP_READ_LOG_PATH):
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
```

### Line budget
Hard constraint: **<250 lines**. Compress aggressively — use shorter docstrings, inline keyword arguments, remove `.items()` variable names where clear from context.

## Pitfalls

### Stale persisted state
When a configurable value (like `self.cap`) is stored in the JSON state file and also settable on the instance, the persisted copy goes stale when the instance attribute changes. **Always use `self.<attr>` in comparisons, never `state["<attr>"]`.** Example fix:
```python
# WRONG — stale cap from old state file
if state["count"] >= state["cap"]:

# CORRECT — live instance attribute
if state["count"] >= self.cap:
```

### Statistical minimums
Two-proportion z-test requires ≥5 samples per group. Add a reasonable higher minimum (e.g., ≥10 daytime) to avoid false positives from small samples. Return `{"flagged": False, "reason": "insufficient_data"}` when below threshold. Full stats helper: `references/proportion-z-test.md`.

### Corrupt JSONL lines
Always wrap JSONL parsing in try/except and use `logger.debug(...)` for skipped lines — don't fail silently but don't crash on a single corrupt line.
