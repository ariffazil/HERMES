# F13 Multi-Sovereign Audit — Worked Example

**Date:** 2026-07-25
**Target:** `/root/arifOS` — arifOS Constitutional Kernel
**Feature:** F13 SOVEREIGN floor — multi-surface tracing + negative-space gap detection

---

## 5-Surface Trace

### Surface 1 — Declaration

**FLOOR_TABLE.json:**
```json
{
  "id": "F13",
  "name": "SOVEREIGN",
  "rule": "Human veto FINAL. Harness switch belongs to sovereign.",
  "type": "HARD",
  "threshold": 1.00
}
```

**000_KERNEL_CANON.md §2:**
```
Arif (F13 SOVEREIGN — human, final veto)
         │
    arifOS (Ω — constitutional kernel)
    ├── F1-F13 floor enforcement
    ├── 888 JUDGE (verdict engine)
    └── 999 VAULT (immutable ledger)
```

**FLOOR_INVARIANTS.md:**
```
F13 SOVEREIGN — Hard invariant: Arif.veto == FINAL
No algorithm, no floor, no majority can override Arif's veto.
```

**Verdict:** Assumes a singular, named sovereign. No mention of multi-sovereign.

---

### Surface 2 — Code Enforcement

**`core/laws.py` `_check_f13_sovereign()` (lines 916-956):**

Four sovereignty signals checked (equal weight):
1. `actor_id` in `("arif", "sovereign", "human")`
2. `session_id` contains "sovereign"
3. `parameters.actor_id` in `("arif", "sovereign", "human")`
4. `parameters.f13_severity_acknowledged == True`

AI self-approval blocked: if `actor_id` is AI/agent/model name AND no explicit sovereign signal → `failed = True`.

**`core/judgment.py` `judge_apex()` (line 362):**
```python
f13_sovereign = 1.0 if kernel.human_approval_status == "approved" else 0.7
```
Contributes 20% weight to Genius score.

**`core/governance_kernel.py` `resolve_conflicting_verdicts()` (lines 272-339):**
Conservative Wins: VOID > HOLD > SABAR > PARTIAL > SEAL.
BUT: this resolves **agent verdicts within a session**, not competing F13 sovereign commands.

**Verdict:** Code enforces the default F13 check for a single sovereign. No concept of multiple sovereigns in enforcement logic.

---

### Surface 3 — DB / Infrastructure

**PostgreSQL trigger (`2026-06-03-f13-sovereign-patch.sql`):**
```sql
IF NEW.patched_by IS DISTINCT FROM 'Muhammad Arif bin Fazil' THEN
    RAISE EXCEPTION 'F13 VIOLATION: ...'
```
**Hardcodes a single human name.** No mechanism for multiple named sovereigns.

**`arifosmcp/core/shared/cascade.py` (line 139):**
```python
if sovereign_count > 1:
    raise ValueError(
        "Multiple sovereign tiers defined. L13 SOVEREIGN requires exactly ONE sovereignty floor."
    )
```

**Verdict:** Infrastructure unequivocally enforces a single sovereign. Multiple sovereign tiers are actively rejected.

---

### Surface 4 — Runtime Identity

**`arifosmcp/runtime/session.py` `_normalize_actor_id()` (line 677):**
```python
_SOVEREIGN_MAP = {
    "arif": "arif",
    "ariffazil": "arif",
    "arif_fazil": "arif",
    "arif-fazil": "arif",
    "arif fazil": "arif",
    "muhammad arif": "arif",
    "muhammad_arif": "arif",
    "888": "arif",
    "f13": "arif",
    "sovereign": "arif",
}
```
**All variants normalize to `"arif"`.** There is no second canonical sovereign identity.

**`arifosmcp/tools/session.py` (line 1655-1676):**
The "multi-sovereign" comment on line 1658 refers to the **crypto challenge map** — multiple recognized actor_ids that can request a challenge. Each entity is still normalized to `"arif"` via `_normalize_actor_id()`. It is NOT a multi-F13 mechanism.

**`contracts/identity.py`:** All `sovereign_id` fields default to `"ARIF_FAZIL"`.

**Verdict:** Runtime identity maps all paths to one canonical sovereign. No second sovereign identity exists anywhere.

---

### Surface 5 — Test Surface

**`tests/test_f13_adversarial.py` — 5 tests:**

| Test | Attack Vector | Passes? |
|------|--------------|---------|
| T1 | Agent self-grants sovereign | ✅ Blocks |
| T2 | Forge without judge | ✅ Blocks |
| T3 | Cross-agent F13 propagation | ✅ Blocks |
| T4 | Action class smuggling | ✅ Blocks |
| T5 | F13 veto override attempt | ✅ Blocks |

**Missing tests (no scenario exists for):**
- Two sovereign actors issuing contradictory commands
- Sovereign A VOIDs what Sovereign B approved
- Session-boundary competing sovereign commands
- Sovereign resignation / transfer protocol
- Sovereign quorum or committee

**Verdict:** Covers single-sovereign usurpation well. Zero coverage of multi-sovereign scenarios.

---

## Negative-Space Search Results

| Search Pattern | Hits | Finding |
|----------------|------|---------|
| `first-seal-wins` | **0** | No deterministic ordering rule for competing seals |
| `multi.*sovereign` | 7 | All unrelated to F13 (crypto challenge map, model cascade) |
| `compet.*void` | **0** | No concept of competing VOIDs |
| `second.*F13\|two.*sovereign` | **0** | No second sovereign concept |
| `ordering.*void\|void.*ordering` | **0** | No ordering rule for sovereign VOIDs |
| `quorum\|committee\|majority.*sovereign` | **0** | No sovereign council/group concept |
| `sovereign.*conflict\|conflict.*sovereign` | **0** | No conflict resolution between sovereigns |

---

## Gap Assessment

| Dimension | Status | Severity |
|-----------|--------|----------|
| Single sovereign enforcement | Fully defined across all 5 surfaces | 🟢 |
| AI usurpation blocking | 5 adversarial tests pass | 🟢 |
| **Multiple sovereigns** | **No concept exists anywhere** | 🔴 |
| **Competing VOID ordering** | **No rule defined** | 🔴 |
| **Sovereign conflict detection** | **No mechanism** | 🔴 |
| **Sovereign transfer/succession** | **No protocol** | 🔴 |

## Key Takeaway

F13 is designed for **exactly one sovereign**. The "two-person bug" — two F13 VOIDs conflicting with no arbitration — is a real architectural gap. The Conservative Wins protocol (VOID > HOLD > SABAR > PARTIAL > SEAL) only governs agent-level verdicts, not sovereign-level authority conflicts. If a second sovereign-level actor existed, the system would process commands in arrival order with no defined rule for escalation, tie-breaking, or conflict detection.
