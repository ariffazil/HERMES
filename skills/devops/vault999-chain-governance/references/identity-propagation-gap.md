# Identity Propagation Gap — Forensic Trace + Deployed Fix

> **Diagnosed:** 2026-07-13 (Claude external review + Hermes forensic confirmation)
> **Fixed:** 2026-07-13 (5 files deployed to /opt/arifos/app/)
> **Severity:** CRITICAL — 83% of receipts_v2.jsonl had anonymous identity (F2 violation)
> **Status:** FIXED, deployed, verified. Historical receipts NOT rewritten (F1 immutability).

## Problem Statement

Claude's feedback: "Fix identity propagation kernel→organ. Receipts logging anonymous while session_id + actor_id were passed. This is not one bug among many — every VAULT999 receipt minted since is evidentially void under your own F2."

## Forensic Trace

### Step 1: Chain Stats (pre-fix)

```
receipts_v2.jsonl (10,393 entries):
  actor=openclaw-anon:  8,654  (83%)
  actor=anonymous:        367
  session=unknown:      9,566  (92%)

outcomes.jsonl (2,406 entries):
  actor=MISSING:          479
  actor=unknown:           31
  session=MISSING:        485

seal_chain.jsonl (167 entries):
  actor_source=self_report:    55  (33%)
  kernel_verdict=UNKNOWN:      43  (26%)
  actor_source=jwt_verified:   16  (10%)
```

### Step 2: Root Cause Chain

```
OpenClaw gateway → (no envelope) → wrap_legacy_call()
  → federation_envelope.py L639: effective_actor = actor_id or "openclaw-anon"
  → ingress_middleware.py L1336: create_and_seal_receipt(actor_id=envelope.actor_id...)
  → vault_receipt.py: writes to receipts_v2.jsonl with placeholder identity
```

The 2026-07-09 fix (`_actor_for_response`) only covered the RESPONSE path, not the receipt writing path. Identity was resolved correctly in responses but still used the raw placeholder in receipts.

### Step 3: Kernel Write Path Gap

`_arif_vault_seal()` in `tools.py` verified identity (Ed25519 at L16764, kernel eval at L16865) but the verification result was thrown away — never flowed into the chain_entry at L17155. `actor_source` and `kernel_verdict` fields were missing.

## The Deployed Fix (2026-07-13)

### New function: `resolve_receipt_identity()` in `vault_receipt.py`

```python
_RELAY_PLACEHOLDERS = frozenset({
    "anonymous", "openclaw-anon", "unknown", "null", "", "None",
})

def resolve_receipt_identity(
    session_id: str | None,
    actor_id: str | None,
    session_context: dict | None = None,
) -> tuple[str, str]:
    """Resolve real identity for a VAULT999 receipt.
    
    Called by ALL receipt writers before minting. If the candidate actor_id
    is a relay placeholder, attempts to resolve from session context.
    Falls back to "anonymous" only when no real identity can be found.
    """
    resolved_session = session_id or "unknown"
    resolved_actor = actor_id or "anonymous"

    if not _is_placeholder(actor_id):
        resolved_actor = str(actor_id)
    elif session_context:
        resolved_actor = (
            session_context.get("actor_id")
            or session_context.get("canonical_actor_id")
            or session_context.get("declared_name")
            or resolved_actor
        )
        if _is_placeholder(resolved_actor):
            resolved_actor = "anonymous"

    if _is_placeholder(session_id) and session_context:
        real_sid = (
            session_context.get("session_id")
            or session_context.get("canonical_session_id")
        )
        if real_sid and not _is_placeholder(real_sid):
            resolved_session = real_sid

    return resolved_session, resolved_actor
```

### Files modified

| File | Change |
|------|--------|
| `vault_receipt.py` | Added `resolve_receipt_identity()` shared resolver |
| `ingress_middleware.py` L1336 | Calls resolver with session context before `create_and_seal_receipt` |
| `forge.py` L558 | Calls resolver before `create_and_seal_receipt` |
| `judge.py` L1172 | Replaced inline placeholder check with resolver |
| `tools.py` L17183 | `_arif_vault_seal` chain_entry now includes `actor_source` + `kernel_verdict` |

### Deployment

```bash
# Source is at /root/arifOS/, runtime at /opt/arifos/app/
cp /root/arifOS/arifosmcp/core/vault_receipt.py /opt/arifos/app/arifosmcp/core/vault_receipt.py
cp /root/arifOS/arifosmcp/runtime/ingress_middleware.py /opt/arifos/app/arifosmcp/runtime/ingress_middleware.py
cp /root/arifOS/arifosmcp/tools/forge.py /opt/arifos/app/arifosmcp/tools/forge.py
cp /root/arifOS/arifosmcp/tools/judge.py /opt/arifos/app/arifosmcp/tools/judge.py
cp /root/arifOS/arifosmcp/runtime/tools.py /opt/arifos/app/arifosmcp/runtime/tools.py
sudo systemctl restart arifos
```

## Remaining Gaps

1. **MCP transport layer** — connections arriving without sovereign token create sessions with `openclaw-anon` from birth. Resolver can't find identity that was never injected. Needs OpenClaw-side fix.
2. **Historical receipts** — 10K+ receipts with anonymous identity. NOT rewritten (F1 immutability). Sovereign decision needed on annotation vs. leave-as-is.
3. **AAA writer** — `seal_chain.js` still defaults `actor_source` to `self_report` when caller doesn't provide it. Kernel now provides it, but non-kernel callers still hit the default.

## Lesson: Deployment Path Gotcha

Initial fix was applied to `/root/arifOS/` (source repo) but the running process uses `/opt/arifos/app/`. The fix had NO EFFECT until files were copied to the runtime location. Always verify the runtime path before declaring a fix deployed.
