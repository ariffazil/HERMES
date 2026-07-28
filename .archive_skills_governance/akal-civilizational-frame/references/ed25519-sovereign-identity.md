# Ed25519 Sovereign Identity — F13 Challenge-Based Authorization (2026-07-25)

> Current state: Challenge-based Ed25519 is the DEFAULT for F13. Free-nonce fallback exists (env-gated). Sentinel string is legacy. See also `governed-agent-anatomy/references/seal-chain-workflow.md`.

## Key Locations (Production)

| File | Contains | Access |
|---|---|---|
| `/opt/arifos/identity/arif_public.pem` | Public key (PEM Ed25519) | `ariffazil:ariffazil` 644 |
| `/opt/arifos/identity/agent_identities.json` | Agent identity registry | `ariffazil:ariffazil` 644 |
| `/opt/arifos/.secrets/did/registry.json` | DID registry | `ariffazil:ariffazil` 644 |
| `/root/.secrets/aaa-identity/keys/arif_private.pem` | **Private key** (PEM Ed25519) | `root:root` 600 — NEVER exposed to service |

All runtime identity paths configurable via systemd drop-in (`10-f13-auth.conf`).

### Outdated paths (no longer used)
- `/root/compose/sekrits/arifos_sovereign.pub` — removed
- `/root/AAA/IDENTITY/keys/arif_public.pem` — still exists but not used at runtime; `/opt/arifos/identity/` is canonical

## Three Verification Paths in `_verify_sovereign_token()`

| Priority | Path | Default | Replay-safe | Gate |
|---|---|---|---|---|
| 1 | **Challenge-based** via `crypto_auth.verify_actor_signature()` | ✅ ON | ✅ Nonce consumed after one use | Always tried first |
| 2 | Free-nonce via `resolve_actor_public_key()` + Ed25519 verify | ❌ OFF | ❌ Replayable | `ARIFOS_FREE_NONCE_ALLOWED=true` |
| 3 | Sentinel string compare | ❌ Legacy | ❌ No | `ARIFOS_SOVEREIGN_KEY` env match |

Challenge-based path calls `verify_actor_signature()` → `verify_init_identity()` → `resolve_actor_public_key()` + `_consume_actor_challenge()`. If nonce was never pre-issued by `issue_actor_challenge()`, returns `challenge_not_issued` → verify fails.

## How the E2E Flow Works

```
1. Kernel issues challenge via issue_actor_challenge("arif")
2. User signs "arif:{nonce}" with private key
3. User calls arif_judge with actor="arif", actor_signature=b64, nonce=...
4. Kernel calls verify_actor_signature("arif", nonce, signature_b64)
5. Kernel resolves public key from agent_identities.json
6. Kernel verifies Ed25519 signature
7. Kernel consumes nonce (one-time, no replay)
8. Returns ALLOW + cc_id + judge_state_hash
```

### MCP Call Pattern

```python
arif_judge(
    actor="arif",                  # CANONICAL — NOT actor_id
    actor_signature="base64...",
    nonce="hex...",
    action_class="ACTION_AUTHORIZATION",
    reversibility_level="R4",
    session_id="SEAL-...",
    session_token="sct_v1...",
)
```

**PITFALL:** Use `actor="arif"` not `actor_id="arif"`. The wrapper translates `actor_id` → `actor` via `kwargs.pop("actor_id", None)`, but this can fail silently when ingress middleware strips the param. `actor` is the canonical schema name.

## Response When F13 Passes

```json
{
  "decision": "ALLOW",
  "seal_type": "SEAL_AUTHORIZATION",
  "constitutional_chain_id": "cc_9dd05a01b1f717e99e...",
  "judge_state_hash": "sha256:2117c2f23fae89b031db...",
  "requires_human_signature": true,
  "authorized_execution": true
}
```

## Phase 1-4 Forward Path

| Phase | What | Status |
|---|---|---|
| 1 | Challenge-based Ed25519, one-time nonce, real crypto, DID under /opt/arifos | ✅ Deployed (2026-07-25) |
| 2 | Judge embeds challenge in ESCALATE response; AAA approval card; one-tap signing; no visible crypto | 🔜 |
| 3 | WebAuthn/passkey; biometric/PIN/security key; origin+RP ID binding; transaction-bound challenge | 🔜 |
| 4 | Risk-adaptive: R0-R3 autonomous, R4 passkey, R5 hardware key; scoped delegation for repetitive work | 🔜 |

## Key Design Rule — Judge-Driven Challenge

`arif_init` starts a session. F13 proves Arif approves ONE consequential action. These are DIFFERENT.

Judge should generate the challenge ONLY when R4/R5 is detected, returning:
```json
{
  "decision": "ESCALATE",
  "reason": "F13_REQUIRED",
  "authorization_request": {
    "nonce": "...",
    "actor": "arif",
    "session_id": "SEAL-...",
    "candidate_hash": "sha256:...",
    "human_summary": "Deploy commit abc123 to production; restart one service"
  }
}
```

Not on every `arif_init`. Phase 2 makes this the default.

## Systemd Drop-in

File: `/etc/systemd/system/arifos.service.d/10-f13-auth.conf`

```ini
[Service]
SupplementaryGroups=arifos-auth
Environment=ARIFOS_RUNTIME_BASE=/opt/arifos
Environment=ARIFOS_ARIF_PUBLIC_KEY_PATH=/opt/arifos/identity/arif_public.pem
Environment=ARIFOS_AGENT_IDENTITY_REGISTRY=/opt/arifos/identity/agent_identities.json
Environment=ARIFOS_DID_REGISTRY_PATH=/opt/arifos/.secrets/did/registry.json
Environment=ARIFOS_DEV_DID_REGISTRY_FALLBACK=0
ExecStartPre=/usr/bin/test -r /opt/arifos/identity/arif_public.pem
ExecStartPre=/usr/bin/test -r /opt/arifos/identity/agent_identities.json
ExecStartPre=/usr/bin/test -r /opt/arifos/.secrets/did/registry.json
```

## Verification

```bash
# Check identity resolution works from service user
sudo -u ariffazil python3 -c "
from arifosmcp.runtime.crypto_auth import resolve_actor_public_key
key = resolve_actor_public_key('ARIF')
assert key is not None
print('PASS: ARIF Ed25519 public key resolved')
"

# Check no deployment drift
curl -s http://localhost:8088/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('release', d.get('software_release', {}))
print(f'Source: {r.get(\"source_commit\",\"?\")[:7]}')
print(f'Built:  {r.get(\"built_commit\",\"?\")[:7]}')
print(f'Deployed: {r.get(\"deployed_commit\",\"?\")[:7]}')
print(f'Drift: {r.get(\"drift\",\"?\")}')
"
```

## Historical Context

This file supersedes the 2026-07-11 version which described:
- Old key paths (`/root/compose/sekrits/`, `/root/AAA/IDENTITY/keys/`)
- Sentinel-based `_verify_sovereign_token()` (string compare, not crypto)
- Missing tool wiring (`arif_init` didn't call `verify_init_identity()`)

All three gaps are now closed. The 2026-07-11 reference can be found in older `akal-cognitive-invariants` profile copies.
