# F1 AMANAH Reversibility Gap Audit — 2026-07-10

**Scope:** `/root/arifOS` | **F1 Score:** 0.50 (at threshold) | **Target:** ≥0.80

---

## Architecture Overview

**Constitutional F1 scoring** (`core/laws.py:457-514`):
- Threshold: `THRESHOLDS["F1_AMANAH"] = 0.50`
- Scoring: reversible patterns → 1.0 | destructive/irreversible → 0.3 | default → 0.7
- PASS if score ≥ 0.50

**Enforcement layers:**
1. `enforce_irreversibility_guard()` (`constitutional_map.py:2988-3009`) — requires `ack_irreversible=True` for tools flagged `irreversible=True` in CANONICAL_TOOLS
2. `SovereignGate` (`enforcement_engines.py:428-450`) — hardcoded list of 4 tools; sovereign bypass for `actor_id=="arif"`
3. `law_audit._check_f1_amanah()` (`core/shared/law_audit.py:514-541`) — rollback/backup path detection
4. `RollbackEngine` (`core/recovery/rollback_engine.py`) — in-memory checkpoint store (max 5)

---

## Critical Findings (8 Gaps)

### GAP 1 — `ack_irreversible` PARAMETER STILL EXISTS after removal comment
**File:** `arifosmcp/core/constitutional_core.py:111-115`
```
# REMOVED 2026-07-07: ack_irreversible was a self-attestation bypass
```
Comment claims removal, but `ack_irreversible` still present in:
- `arif_seal` (`tools/vault.py:24`)
- `arif_forge` (`constitutional_map.py:2527`)
- `arif_memory` (`tools/memory.py:670`)
- `browser.py` (`tools/browser.py:218`)

**Impact:** Self-attestation risk — same actor sets action AND ack flag.

### GAP 2 — SovereignGate hardcoded vs CANONICAL_TOOLS dynamic
**Files:**
- `arifosmcp/core/enforcement_engines.py:431-436` (hardcoded):
  ```python
  IRREVERSIBLE_TOOLS = ["arif_seal", "arif_seal_write", "arif_forge", "arif_forge_execute"]
  ```
- `arifosmcp/constitutional_map.py:2983-2985` (dynamic):
  ```python
  _IRREVERSIBLE_TOOLS = {name for name, spec in CANONICAL_TOOLS.items() if spec.get("irreversible", False)}
  ```

**Impact:** Adding `irreversible=True` to a new CANONICAL_TOOLS entry bypasses SovereignGate.

### GAP 3 — `law_audit.py:521` syntax bug — backup detection always True
**File:** `core/shared/law_audit.py:520-523`
```python
has_backup = any(
    kw in action_lower or kw in ctx_str
    for kw in ("backup", "rollback", "snapshot", "reversible", "dry-run")
)
```
**Bug:** `kw in action_lower or kw in ctx_str` evaluates as `bool or str` — always `True` (non-empty string is truthy). `any(...)` always returns `True`. Destructive-without-backup check never fires.

**Fix:** `any(kw in action_lower or kw in ctx_str for kw in ...)` — move the `or kw in ctx_str` inside the loop.

### GAP 4 — RollbackEngine: in-memory only, never called, no verification
**File:** `core/recovery/rollback_engine.py`
- `_checkpoints`: in-memory dict (line 33) — **lost on restart**
- `_max_history = 5`: only 5 snapshots
- `create_checkpoint()` (line 37): **never called from any verdict path**
- `rollback()` (line 71): restores but **never verifies correctness**

**Impact:** Rollback unavailable when needed; state permanently lost on restart.

### GAP 5 — `rollback_plan` in evidence_required but never validated
**Files:** `constitutional_map.py` + `descriptions/arif_forge.md`

`arif_forge` has `evidence_required: ... rollback_plan ...` but:
- No code validates `rollback_plan` field is populated
- `enforce_irreversibility_guard()` only checks `ack_irreversible` boolean
- No test verifies rollback_plan presence or functionality

**Impact:** `rollback_plan` requirement is documentation only.

### GAP 6 — `arif_seal` / VAULT999: zero reversibility, no defined contingency
**Files:** `constitutional.llms.txt:264`, `constitutional_map.py:299`

`arif_seal` has `reversibility_score: 0.0`. `enforce_irreversibility_guard()` lets it through with `ack_irreversible=True` alone. VAULT999 appends to immutable ledger — no rollback possible.

**Impact:** Permanently irreversible class of actions with no contingency doctrine.

### GAP 7 — F1 score 0.3 < 0.50 but doesn't block
**File:** `core/laws.py:500-505`

Destructive actions get score 0.3 (below 0.50 threshold). But `enforce_irreversibility_guard()` is a separate gate — with `ack_irreversible=True`, action proceeds regardless of F1 score.

**Impact:** F1 score of 0.30 is meaningless for destructive+acked actions.

### GAP 8 — No backup infrastructure
No backup system exists for:
- Governance kernel state
- Session state
- Constitutional floor scores
- Tool contracts / CANONICAL_TOOLS

---

## Canonical Tool Reversibility (from `constitutional.llms.txt`)

| Tool | reversibility_score |
|------|--------------------|
| arif_judge | 0.0 |
| arif_judge_deliberate | 0.0 |
| arif_seal | 0.0 |
| arif_forge | 0.2 |
| arif_act | 0.2 |
| arif_memory (forget mode) | IRREVERSIBLE (F13) |
| arif_memory (general) | 0.7 |
| forge_execute | 0.0–0.5 |
| GEOX/WEALTH/WELL | 1.0 (compute only) |

---

## Priority Fixes

1. **GAP 3** — `law_audit.py:521` syntax fix (trivial, high impact)
2. **GAP 2** — Sync SovereignGate with dynamic lookup (trivial, high impact)
3. **GAP 4** — Persist RollbackEngine checkpoints to VAULT999/Postgres + auto-trigger (large, critical)
4. **GAP 1** — Remove `ack_irreversible` or architect proper third-party verification (medium)
5. **GAP 5** — Add `rollback_plan` evidence validation (medium)
6. **GAP 7** — Integrate F1 score into gate — score 0.3 with `ack_irreversible=True` should minimum HOLD

---

## Audit Command Set

```bash
# Find all ack_irreversible params after removal comment
grep -rn "ack_irreversible" /root/arifOS/arifosmcp/ --include="*.py"

# Check SovereignGate hardcoded vs dynamic match
python3 -c "
from arifosmcp.constitutional_map import CANONICAL_TOOLS, _IRREVERSIBLE_TOOLS
dyn = _IRREVERSIBLE_TOOLS
print('Dynamic:', sorted(dyn))
# vs hardcoded in enforcement_engines.py

# Test the any() bug
action_lower = 'delete everything'
ctx_str = 'context'
keywords = ('backup', 'rollback')
result = any(kw in action_lower or kw in ctx_str for kw in keywords)
print('any() result (should be False):', result)  # Returns True — BUG

# Check RollbackEngine usage
grep -rn "create_checkpoint\|rollback_engine\|RollbackEngine" /root/arifOS/core/ --include="*.py"
```
