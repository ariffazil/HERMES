# Light-Init Sovereign Authority Bug (2026-07-24)

## Symptom

arifOS kernel returns `OBSERVE_ONLY` authority even after Ed25519 sovereign signature verification succeeds. The session token (SCT) carries `auth: OBSERVE_ONLY` and `seal_allowed: false`. The kernel issues a challenge nonce despite the signature already being verified.

```
arif_init(mode="light", actor_id="ARIF", nonce="...", actor_signature="...")
→ authority_scope: "OBSERVE_ONLY"
→ seal_allowed: false
→ challenge_required: true
→ challenge_nonce: "lgHkBdfMNbkV-..."
```

## Root Cause

In `tools/session.py`, the `_project_light()` function at line 449-453 hardcodes `signature_verified=False` and `is_sovereign_principal=False` when calling `identity_band_authority()`. But the deeper root cause is in the light-init flow at lines 1370-1398:

The auto-identity path successfully verifies the Ed25519 signature and sets:
```python
sess["signature_verified"] = True
sess["authority"] = "FULL"
sess["agent_class"] = "SOVEREIGN_PRINCIPAL"
```

But does NOT set the corresponding light-init variables:
```python
_light_actor_verified = True   # MISSING
_light_band = "FULL"            # MISSING
_light_agent_class = "SOVEREIGN_PRINCIPAL"  # MISSING
_light_authority_level = "SOVEREIGN"        # MISSING
```

These variables are initialized to unverified defaults at line 1274-1277:
```python
_light_actor_verified = False
_light_band = "OBSERVE_ONLY"
_light_agent_class = "UNVERIFIED"
_light_authority_level = "ANONYMOUS"
```

Then the Ed25519-exempt check at lines 1402-1458 runs — if the actor isn't in `_ED25519_EXEMPT_SYSTEM_ACTORS` (which "ariffazil" wasn't), it falls through to the challenge path at lines 1459-1480, which issues a new challenge nonce and leaves `_light_band` at "OBSERVE_ONLY".

Finally, `_project_light()` is called at line 1485 with `actor_verified=_light_actor_verified` (still False) and `authority_override=_light_band` (still "OBSERVE_ONLY").

## Fix

Add 4 lines to `tools/session.py` after the auto-identity block at line 1393:

```python
sess["signature_verified"] = True
sess["actor_band"] = "FULL"
sess["agent_class"] = "SOVEREIGN_PRINCIPAL"
sess["authority"] = "FULL"
_light_actor_verified = True          # ← ADD
_light_band = "FULL"                   # ← ADD
_light_agent_class = "SOVEREIGN_PRINCIPAL"  # ← ADD
_light_authority_level = "SOVEREIGN"        # ← ADD
```

This ensures the light-init variables are updated when the auto-identity path succeeds, so the subsequent `_project_light()` call and Ed25519-exempt check both see the correct authority level.

## Verification

After patching and restarting arifOS:

```bash
systemctl restart arifos
sleep 3
curl -s http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin)['service_health'])"
# Expected: green
```

Then re-init with signature — should return `authority_scope: "FULL"` or `"SOVEREIGN"` instead of `"OBSERVE_ONLY"`.

## Files Modified

- `/root/arifOS/arifosmcp/tools/session.py` — lines 1394-1397 (4 lines added after auto-identity block)
- Deployed code at `/opt/arifos/app/arifosmcp/tools/session.py` (same change)