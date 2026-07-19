# arifOS Seal Debugging Reference — 2026-07-10

## Session context

BASIN-PROSPECT-001: Attempted to seal evidence from GEOX direct queries (Sabah Basin structural closures) via `arif_seal`. Pipeline worked end-to-end but vault kept returning HOLD. Debugged across ~3 hours of iterative tracing.

---

## The Four-Layer arifOS Verification Stack

When `arif_seal(mode="seal", ack_irreversible=True, ...)` is called:

```
Layer 1: Ed25519 sovereign signature (optional — lines 16128-16207)
         Requires: actor_signature + nonce (both non-None, nonce fresh)
         Result: signature_verified=True, authority="SOVEREIGN"
         If skipped (nonce=None): falls through with signature_verified=False

Layer 2: Kernel evaluate_intent + L01/L11 floor check (lines 16210-16261)
         Requires: session_registry passed to _KERNEL.evaluate_intent()
         Bug fixed: session_registry was NOT being passed → L11 always failed
         Result: k_verdict["passed"] = True/False

Layer 3: Judge contract resolution (lines 16263-16303)
         Requires: constitutional_chain_id OR judge_state_hash (one must be non-None)
         If both None: returns HOLD with reason "judge contract required"
         SABAR verdict from arif_judge does NOT produce a contract

Layer 4: Vault write (lines 16305+)
         Issues entry to _VAULT_LEDGER + dual-write to VAULT999
         Requires: all above layers passed
```

---

## Diagnostic Checklist

### Is SCT token resolving to FULL authority?

```python
from arifosmcp.runtime.sct import verify_sct
claims = verify_sct(sct_token)
print(claims.get("auth"))  # expect: "FULL"
```

If OBSERVE_ONLY: SCT verification is failing silently. Check that the token is present in the session under `session_token` key.

### Is session in the registry when kernel evaluates?

```python
from arifosmcp.runtime import tools as rt
registry = set(rt._SESSIONS.keys())
try:
    from arifosmcp.runtime.session import get_all_session_ids
    registry.update(get_all_session_ids())
except: pass
print(sid in registry)  # expect: True
```

If False: the session wasn't stored in `_SESSIONS` — likely a process boundary issue (different Python interpreter).

### Is `_resolve_judge_contract` returning None or a hold?

```python
from arifosmcp.runtime.tools import _resolve_judge_contract
jc, hold = _resolve_judge_contract(
    constitutional_chain_id=None,
    judge_state_hash=None,
    tool_name="arif_vault_seal"
)
print(f"contract={jc}, hold={hold is not None}")  # hold should be True (both None)
```

If hold=False: one of the IDs was non-None and found in registry.

### What does kernel.evaluate_intent actually return?

```python
from arifosmcp.runtime import tools as rt
_KERNEL = rt._KERNEL
registry = set(rt._SESSIONS.keys())
result = _KERNEL.evaluate_intent(
    tool_name="arif_vault_seal",
    params={
        "mode": "seal",
        "ack_irreversible": True,
        "actor_signature": None,
        "nonce": None,
        "signature_verified": False,
        "session_registry": registry,
    },
    session_id=sid,
    actor_id="ariffazil",
)
print(result)  # expect: {"passed": True, "violated_laws": [], "threat_score": 0.0}
```

### Is `seal_allowed` True in the auth envelope?

```python
from arifosmcp.runtime.tools import _build_action_result_envelope
# Returns the full envelope — check authority.seal_allowed field
```

`seal_allowed = (_runtime_auth in ("FULL","SOVEREIGN") and verdict == "SEAL")`. Verdict comes from `_compute_canonical_verdict(out)`. If verdict = RETAK (not SEAL), seal_allowed = False even with FULL auth.

---

## Key File Locations

| File | Line | What it does |
|------|------|-------------|
| `arifOS/arifosmcp/runtime/tools.py` | 16128 | Ed25519 signature verification block |
| `arifOS/arifosmcp/runtime/tools.py` | 16218 | Kernel eval WITHOUT session_registry (BUG) |
| `arifOS/arifosmcp/runtime/tools.py` | 16263 | Judge contract gate — first HOLD source |
| `arifOS/arifosmcp/runtime/tools.py` | 16286 | judge_contract is None → second HOLD source |
| `arifOS/arifosmcp/runtime/tools.py` | 7081 | `_resolve_judge_contract` function |
| `arifOS/arifosmcp/runtime/tools.py` | 3757 | `seal_allowed` formula |
| `arifOS/arifosmcp/runtime/sct.py` | — | `verify_sct` — resolves SCT to authority |
| `arifOS/arifosmcp/tools/vault.py` | 21 | `arif_seal` function — top-level API |
| `arifOS/arifosmcp/core/law_evaluator.py` | 475 | L11 check: session in registry |

---

## The Bypass That Works

The sovereign bypass (F13 + FULL SCT) skips Layer 3 (judge contract). It requires:
1. SCT resolves to `auth: "FULL"` ✅ (works — verified)
2. `floors={"F13": "SOVEREIGN_ACK"}` passed to `arif_seal` ✅
3. **BUT**: `floors` must be plumbed through to `_arif_vault_seal` — it was NOT in the function signature. The patch adds it.

Without the bypass: `arif_judge` must return SEAL verdict (not SABAR) AND produce `constitutional_chain_id` + `judge_state_hash`. External model degradation blocks this.

---

## What External Model Failure Causes

- `arif_think` → calls TokenRouter (`deepseek-reasoner`) → HTTP 503 + MiMo → HTTP 429
- No thinking output → `arif_judge` verdict = SABAR
- SABAR verdict → no judge contract issued → `arif_seal` → HOLD

This is correct constitutional behavior, not a bug. The fix is either:
- Wait for model quota refill (~30min for MiMo)
- Use the sovereign bypass (pending the `floors` parameter fix)
- Accept `seal_card` mode (read-only, no permanent write) as the artifact

---

## Ed25519 vs EC P-256 Key Confusion

| Key | Path | Use |
|-----|------|-----|
| Ed25519 | `/root/.ssh/operator_did_did_ed25519` | arifOS nonce signing, session verification |
| EC P-256 | `/root/.secrets/aaa-identity/keys/arif_private.pem` | AAA JWT only — NOT for arifOS |

Ed25519 sig for nonce challenge: sign payload `ariffazil:{nonce}` (no curly braces, just colon-separated).
