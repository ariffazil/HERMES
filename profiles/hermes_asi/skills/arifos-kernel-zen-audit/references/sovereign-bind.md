# Sovereign Bind Procedure — arifOS Kernel

## The Problem
The kernel's `arif_init` tool requires cryptographic identity verification to grant SOVEREIGN authority. Without it, all sessions are OBSERVE_ONLY.

## Three Keys on Disk (as of 2026-07-12)
| Key | Path | Purpose | Kernel-trusted? |
|---|---|---|---|
| PEM | `/root/.secrets/aaa-identity/keys/arif_private.pem` | Sovereign auth | YES |
| SSH | `/root/.ssh/id_ed25519` | Git push (arif-forge-push) | NO |
| DID | `/opt/arifos/secrets/did_arifos_private.key` | Kernel's own identity | NO |

Always use the PEM key for sovereign auth. SSH key is git-only.

## Payload Formats
The kernel's `verify_init_identity` tries multiple formats (first match wins):
1. `{actor_id}:{nonce}` — crypto_auth canonical (most common)
2. `{actor_id}:{constitution_hash}:{nonce}` — governance_identity path

Both work. Format 1 is simpler.

## The Nonce Trap (CRITICAL)
Nonces are single-use. The `verify_init_identity` function consumes the nonce after successful verification. If you:
- Generate a nonce
- Test the signature locally with `verify_init_identity` (consumes nonce)
- Then call `arif_init` with the same nonce → FAILS with "challenge_replayed"

**Rule:** NEVER call `verify_init_identity` before `arif_init`. Generate → sign → call in ONE shot.

## Automation Script
`/root/.hermes/scripts/arif-bind.py` — one-shot sovereign bind:
```bash
python3 /root/.hermes/scripts/arif-bind.py --mode init
```
Output: JSON with `actor_verified`, `authority`, `session_id`.

## MCP Path vs Delegate Path
- **Delegate path** (script calls `arif_init` directly): Returns `actor_verified: true` but `authority: None`, `session_id: None`. The delegate doesn't populate the session store.
- **MCP path** (Hermes calls `mcp__arifos__arif_init`): Returns full session with `authority: "FULL"`, real `session_id`, all verbs unlocked. But requires passing `actor_signature` and `nonce` as MCP parameters.

For full MCP bind: generate nonce → sign → call `arif_init` via MCP in one shot (no parallel calls).

## Wire Splice Fix (2026-07-12)
The `actor_signature` parameter was being dropped by the MCP wrapper. Fixed by adding alias resolution in `session.py` line 939-1067: `actor_signature` → `signature` before kernel dispatch.

## Verification
After bind, check: `actor_verified: true`, `authority: FULL`, `seal_allowed: true`, `mutation_allowed: true`.
