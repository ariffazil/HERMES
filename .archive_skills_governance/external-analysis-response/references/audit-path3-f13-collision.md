# Path 3 Audit — F13 MULTI-SOVEREIGN COLLISION

**Spec:** EXTERNAL_FALSIFICATION_SPEC.md Path 3  
**Date:** 2026-07-25  
**Files audited:** session.py (3154L), judge.py (2179L), tools.py (24560L), vault.py, runtime/session.py, conflict_resolver.py

## Verdict Summary

| Test | Description | Verdict | Why |
|------|-------------|---------|-----|
| 3.1 | Concurrent VOID+VOID | ✅ PASS (by accident) | Both same verdict; no conflict |
| **3.2** | **SEAL vs VOID** | **❌ FAIL** | Arrival-order dependent, last-writer-wins |
| **3.3** | **Repeat 20x** | **❌ FAIL** | Variance expected — no atomic resolution |
| **3.4** | **Ownership boundary** | **❌ FAIL** | No session-ownership enforcement in judge |

**Overall: UNDEFINED** — 3/4 tests fail. Conflict resolver exists but is unwired.

## Five Structural Failures

### 1. Sovereign detection is mixed (string + crypto)
Three separate identity sources drift against each other:
- **Localhost auto-sign** (session.py:1364): accepts `actor_id.lower() in ("arif", "888", "ariffazil")` — string match
- **Challenge mode** (session.py:1296-1341): proper Ed25519 verification when nonce+signature provided
- **Sovereign identity map** (runtime/session.py:280-282): `{"ariffazil": "ariffazil"}` — only accepts exact "ariffazil"
**File:** session.py:1364, runtime/session.py:280-282.

### 2. Conflict resolver EXISTS but is NOT wired into judge
`conflict_resolver.py` defines correct deterministic ranking:
- VOID (rank 7) always wins over SEAL (rank 2)
- Same organ → more restrictive verdict wins

BUT it's NEVER called from `_arif_judge_deliberate`. Designed for cross-organ conflicts (GEOX vs WEALTH), not multi-sovereign.
**File:** conflict_resolver.py, tools.py:16191-16370 (judge path).

### 3. No session-ownership enforcement
`_ACTOR_SESSION_MAP` (runtime/session.py:163) maps session_id→actor_id but NO check in judge path enforces it. Sovereign B can judge using A's session_id by simply passing it.
**File:** tools.py:23286-23400 (`_wrap_handler` only fills missing actor_id, never blocks mismatch).

### 4. VAULT999 has no collision detection
`outcomes.jsonl` is pure append-only. Competing verdicts for the same action coexist:
```json
{"action": "forge_execute_XYZ", "verdict": "SEAL", "session": "A", "ts": "T1"}
{"action": "forge_execute_XYZ", "verdict": "VOID", "session": "B", "ts": "T2"}
```
No reconciliation, no conflict flag, no escalation.
**File:** vault.py (append-only log), tools.py `_JUDGE_STATE_REGISTRY` (last-writer-wins).

### 5. Single sovereign slot, not a federation
The identity map only has one entry. Two Ed25519 keypairs with separate actor_ids would need infrastructure that was never tested.
**File:** runtime/session.py:280-282.

## Fix Priority

1. **P0** — Wire conflict_resolver into judge path: before storing a verdict, check if another sovereign has already judged the same action_id. If yes, call resolve_conflict().
2. **P0** — Add session-ownership gate in `_arif_judge_deliberate` or `_arif_kernel_intercept`.
3. **P1** — Unify sovereign identity: reconcile three separate identity sources into one.
4. **P1** — Add VAULT999 collision detection: when appending, check for prior entries with same action_id but different verdict → flag as F13_COLLISION.
5. **P2** — Implement two-phase verdict for irreversible actions: all recognized sovereigns must SEAL before execution proceeds.
