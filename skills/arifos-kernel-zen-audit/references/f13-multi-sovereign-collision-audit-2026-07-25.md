# F13 Multi-Sovereign Collision Audit — 2026-07-25

**Target:** arifOS kernel source at `/root/arifOS/`
**Spec:** EXTERNAL_FALSIFICATION_SPEC.md §PATH 3 (Tests 3.1–3.4)
**Author:** Hermes Agent (DeepSeek V4 Flash)

---

## Source-by-Source Findings

### 1. Sovereign Detection (`session.py:1364`, `session.py:280`)

**Auto-identity path** (no explicit signature, session.py:1357-1364):
```python
_actor_lower = actor_id.lower().strip()
_is_sovereign = _actor_lower in ("arif", "888", "ariffazil")
```
Plain string comparison. Three hardcoded strings. Case-insensitive.

**Persistent sovereign identity map** (runtime/session.py:280-282):
```python
_SOVEREIGN_IDENTITY_MAP: dict[str, str] = {
    "ariffazil": "ariffazil",
}
```
Only ONE entry. `"arif"` and `"888"` are NOT in this map.

**Challenge mode map** (session.py:1659-1663):
```python
_SOVEREIGN_MAP: dict[str, str] = {
    "arif": "arif",
    "ariffazil": "ariffazil",
    "888": "888",
}
```

**Drift:** Three separate sovereign identity sources with inconsistent contents. The auto-sign path accepts 3 names, the persistent store accepts 1, the challenge mode accepts 3.

**Implication for PATH 3:** To provision sovereign B with `actor_id="SOVEREIGN_B"`, you must add it to ALL three maps. Currently only `"ariffazil"` is canonical. No autonomic registration path exists.

---

### 2. Conflict Resolver Wiring (`conflict_resolver.py`)

**Resolver exists** — `/root/arifOS/arifosmcp/core/conflict_resolver.py` defines:
- `VerdictRank`: VOID(7) > HOLD(6) > UNKNOWN(5) > SABAR(4) > PARTIAL(3) > SEAL(2) > PROCEED(1)
- `OrganRank`: HUMAN(8) > ARIFOS(7) > A_FORGE(6) > AAA(5) > WELL(4) > WEALTH(3) > GEOX(2) > CLERK(1)
- `resolve_conflict()`: O(1) lookup + compare, 5 rules
- `resolve_multi_organ()`: iterative pairwise

**RESOLVER IS NOT WIRED.** Search for `resolve_conflict` or `ConflictEnvelope` calls in:
- `tools.py` (the _arif_judge_deliberate function at line ~16191)
- `judge.py` (the async MCP wrapper)
- `tools/session.py`

**Result:** No call to `resolve_conflict()` exists in the normal judge path. Each `arif_judge` call stores verdict independently. The resolver is dead code for this purpose.

**If it WERE wired:** Two F13 sovereigns both map to `organ="human"` (rank 8). Rule 3 (same organ, more restrictive wins) would make VOID beat SEAL. But this is by accident of the rank ordering, not by multi-sovereign design.

---

### 3. Session Ownership Enforcement (`runtime/session.py:163`, `runtime/tools.py:16191+`)

**`_ACTOR_SESSION_MAP: dict[str, str]`** exists at runtime/session.py:163. Maps `session_id → actor_id`.

**But `_arif_judge_deliberate`** (tools.py:~16191) does NOT check:
```python
# THIS CHECK DOES NOT EXIST:
if _ACTOR_SESSION_MAP.get(session_id, "").lower() != (actor_id or "").lower():
    return {"verdict": "HOLD", "reason": "session ownership mismatch"}
```

**The `_wrap_handler`** (tools.py:~23291) only fills in missing `actor_id`:
```python
if kwargs.get("session_id") and not kwargs.get("actor_id"):
    _sess = _SESSIONS.get(kwargs["session_id"])
    if _sess and _sess.get("actor_id"):
        kwargs["actor_id"] = _sess["actor_id"]
```
This is convenience, not enforcement. If caller provides both `session_id` and `actor_id`, no cross-check is performed.

**SCT token as indirect binding:** `verify_and_inject_token` (tools.py:23077) validates SCT and extracts the `actor` claim. If sovereign B presents sovereign A's valid SCT token, the verification passes, and `kwargs["actor_id"]` is set from the token claims (tools.py:23215). So the SCT provides weak binding — as strong as the token's non-repudiation.

---

### 4. VAULT999 Collision Detection (`tools.py:5810`, `tools/vault.py:401+`)

**`_VAULT_LEDGER: list[dict[str, Any]]`** at tools.py:5810 — pure Python list, pure append.

**`outcomes.jsonl`** — append-only line-delimited JSON. No dedup, no merge, no reconciliation.

**`_JUDGE_STATE_REGISTRY: dict[str, dict[str, Any]]`** at tools.py:5818 — Python dict, last-writer-wins. Two sovereigns writing to the same key produce non-deterministic results (dict write is not atomic across MCP threads/processes).

**No collision check exists.** Two entries for the same action_id can coexist:
```jsonl
{"action": "forge_execute_XYZ", "verdict": "SEAL", "session": "A_session", "ts": "T1"}
{"action": "forge_execute_XYZ", "verdict": "VOID", "session": "B_session", "ts": "T2"}
```

Both persist. No downstream reconciler. No collision alarm.

---

## PATH 3 Test Verdicts

| # | Test | PASS/FAIL | Why |
|---|------|-----------|-----|
| 3.1 | Concurrent VOID+VOID | PASS (by accident) | Both VOIDs; no conflict since same verdict |
| 3.2 | SEAL vs VOID | FAIL | Arrival-order dependent. No cross-sovereign resolution wired. |
| 3.3 | Repeat 3.2 × 20 | FAIL (expected variance) | Random arrival order = non-deterministic dict state |
| 3.4 | Ownership boundary | FAIL | Sovereign B can adjudicate A's session via session_id param |

**Composite: 8/50**

---

## Recommended Fixes

### Fix 1: Wire conflict resolver into judge path
In `_arif_judge_deliberate` (tools.py), before storing verdict, check if a different sovereign already has a verdict for the same action_id. If yes, construct `ConflictEnvelope(organ_a="human", organ_b="human", verdict_a=existing, verdict_b=new)` and call `resolve_conflict()`.

### Fix 2: Add session-ownership gate
In `_arif_judge_deliberate` (or `_arif_kernel_intercept`), add:
```python
if session_id and _ACTOR_SESSION_MAP.get(session_id, "").lower() != (actor_id or "").lower():
    return HOLD("session belongs to different sovereign")
```

### Fix 3: Unify sovereign identity
Consolidate the three identity sources into one canonical registry. Use a single `SOVEREIGN_IDENTITY_REGISTRY` keyed by `actor_id` with Ed25519 public keys.

### Fix 4: Add VAULT999 collision detection
When appending to `outcomes.jsonl`, check if a prior entry for the same `action_id` exists with a different verdict. If so, flag as `F13_COLLISION` and escalate to 888_HOLD.

### Fix 5: Implement all-sovereign consent for irreversible
For IRREVERSIBLE actions (`ack_irreversible=True`), require ALL recognized sovereigns to SEAL before execution proceeds. Any single VOID blocks.
