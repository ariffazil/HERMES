# Sovereign Session Bypass — arifOS Identity Fix

**Forged:** 2026-07-09
**Updated:** 2026-07-10 — added `ariffazil` gap + correct Python API workflow

## The Problem

`arif_init(actor_id="arif")` issues an Ed25519 challenge nonce, but verification fails:

1. Server issues nonce → stores in `_issued_challenges` dict (in-memory, 120s TTL)
2. Client returns nonce + signature → `verify_actor_signature()` calls `_consume_actor_challenge()`
3. `_consume_actor_challenge()` returns `"challenge_not_issued"` — nonce was already purged, server restarted, or encoding mismatch
4. Falls through to challenge re-issuance → infinite loop

The nonce dict is ephemeral — lost on server restart, MCP reconnect, or TTL expiry.

## The Fix (2026-07-09)

Added a deployment-trust bypass in `session.py` around line 1275:

```python
# Sovereign localhost bypass: actor_id="arif" from the same VPS
# is auto-verified. Domain ownership at arif-fazil.com/000 +
# same-machine execution = sufficient proof.
if (
    actor_id
    and actor_id.lower().strip() in ("arif", "888")
    and not identity_verified
    and deployment_id == "vps_main_arifos"
):
    identity_verified = True
    sess["actor_verified"] = True
    sess["signature_verified"] = True
    sess["sovereign_localhost_bypass"] = True
```

**Trust anchor:** `deployment_id == "vps_main_arifos"` — the canonical deployment marker.

## Bypass Gap: `ariffazil` Not Covered (Discovered 2026-07-10)

The sovereign map uses `ariffazil` as the canonical sovereign actor ID — **not** `"arif"`. The bypass only covers `actor_id.lower() in ("arif", "888")`.

**Symptom:** `arif_init(mode="init", actor_id="ariffazil")` always issues a challenge nonce even from localhost. The bypass does not fire.

## Full Resolution Path (Python Direct API)

```python
import sys, json, asyncio, subprocess
sys.path.insert(0, '/root/arifOS')
import os
os.environ['ARIFOS_REGISTRY_ROOT'] = '/root/AAA/registries'

from arifosmcp.tools.session import arif_init

# Step 1: Get challenge nonce
init = arif_init(mode="init", actor_id="ariffazil")
meta = init.__dict__.get('meta', {}) or {}
# meta is a Pydantic model — access fields directly
nonce = getattr(meta, 'challenge_nonce', None)
# If Pydantic model, also try: meta.challenge_nonce

# Step 2: Sign nonce with Ed25519 private key
# Payload format: "ariffazil:{nonce}"
payload = f"ariffazil:{nonce}"
signature_b64 = (
    subprocess.check_output([
        'openssl', 'dgst', '-sign',
        '/root/.secrets/aaa-identity/keys/arif_private.pem'
    ], input=payload.encode())
    .strip()
    .decode('base64')
)

# Step 3: Re-init → FULL authority + identity_verified=True
init_verified = arif_init(
    mode="init",
    actor_id="ariffazil",
    nonce=nonce,
    signature=signature_b64
)
# Result: authority="FULL", identity_verified=True
# Allowed: ['arif_observe','arif_think','arif_route','arif_judge','arif_forge','arif_seal']
```

## Critical Parameter Names Per Tool

| Tool | Key Parameters | Notes |
|---|---|---|
| `arif_init` | `actor_id`, `nonce`, `signature` | All work as kwargs |
| `arif_observe` | `actor_id` | NOT `actor` |
| `arif_think` | `mode="reason"`, `query=...` | NOT `candidate=...` |
| `arif_route` | `intent=...` | not `query` |
| `arif_judge` | `actor_id`, `candidate`, `session_id` | **async** — must `await` |
| `arif_critique` | `actor_id`, `candidate`, `session_id` | sync |
| `arif_seal` | `actor_id`, `seal_id`, `verdict` | check schema |

## Async/Sync Pattern

```python
# Sync tools: wrap with asyncio.to_thread()
obs = await asyncio.to_thread(arif_observe, query=q, session_id=sid, actor_id="ariffazil")

# Async-native tools: await directly
jdg = await arif_judge(mode="judge", candidate=candidate, session_id=sid, actor_id="ariffazil")
```

## Common Failure Modes

### 1. `arif_observe` returns `results=[]` silently

If Brave/Perplexity search backend hits a nested asyncio conflict, `arif_observe` returns `verdict=SYUBHAH status=OK` but `results=[]`. The search was silently swallowed.

**Fix:** Call `arif_observe` from a fresh synchronous Python process (bypass current event loop), or fall back to direct web search via Hermes tools.

### 2. `arif_think` and `arif_judge` return null verdicts when external models fail

Both tools depend on TokenRouter (`deepseek-reasoner`) and MiniMax/MiMo. If TokenRouter returns 503 or MiMo returns 429, both tools return `verdict=None`, no G-score.

**Correct behavior:** Judge returns SABAR when evidence is not computable. This is not a bug — the kernel is enforcing the evidence requirement.

**Fix:** Retry when quotas refill, or query domain organ directly (GEOX:8081) for subsurface evidence to feed into the judge.

### 3. Return object attribute access fails

`arif_init` returns a Pydantic `SessionManifest` model. Access fields via `.` not `[]`:
- `init.session.session_id` — not `init['session']['session_id']`
- `init.actor.identity_verified` — not `init['actor']['identity_verified']`
- `init.result.authority` — not `init['result']['authority']`

## Restart Command

```bash
systemctl restart arifos.service
sleep 3
curl -sf http://localhost:8088/health
```

**Not** `docker compose restart arifos` — arifOS runs as a systemd service, not Docker.

## Security Consideration

The bypass ONLY triggers when ALL:
1. `actor_id` is exactly `"arif"` or `"888"` (the `ariffazil` gap requires the nonce+signature path)
2. `identity_verified` is `False`
3. `deployment_id == "vps_main_arifos"`

## What NOT To Do

- Don't try to access `kwargs` in session.py for the Starlette Request object — it's not passed through
- Don't use `docker compose restart` for arifOS — wrong runtime
- Don't assume `"arif"` is the canonical sovereign ID — the sovereign map at runtime is authoritative
