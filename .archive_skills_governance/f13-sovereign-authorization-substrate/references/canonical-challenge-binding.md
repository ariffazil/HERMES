# Canonical Challenge Binding Schema

The signed payload MUST be a deterministic canonical JSON serialization of this
structure, hashed with SHA-256, then signed with Ed25519.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `challenge_id` | `string` | Server-issued unique challenge ID (`chal_<uuid>`) |
| `nonce` | `string` | Base64 32-byte cryptographically random nonce |
| `actor` | `string` | Sovereign actor ID (canonical: `"arif"`) |
| `session_id` | `string` | Current session ID |
| `candidate_hash` | `string` | `sha256:` prefixed hash of the action candidate |
| `action_class` | `string` | One of: `ACTION_AUTHORIZATION`, `AUDIT_RECORD`, `SEAL_RECORD` |
| `reversibility` | `string` | One of: `R0` through `R5` |
| `blast_radius` | `string` | One of: `NONE`, `LOW`, `MEDIUM`, `HIGH`, `SOVEREIGN` |
| `seal_purpose` | `string` | One of: `AUTHORIZE`, `RECORD`, `RECOVER` |
| `authority_effect` | `string` | One of: `EXECUTION_GRANT`, `WITNESS_RECORD`, `RECOVERY` |
| `audience` | `string` | Target server/organ (e.g. `"arifOS"`, `"A-FORGE"`) |
| `issued_at` | `string` | ISO-8601 UTC timestamp |
| `expires_at` | `string` | ISO-8601 UTC timestamp |

## Optional Fields

| Field | Type | Description |
|---|---|---|
| `plan_id` | `string` | Plan ID when execution is part of a plan |
| `target_environment` | `string` | One of: `staging`, `production`, `sovereign` |
| `target_actuator` | `string` | Specific tool/actuator being authorized |
| `human_summary` | `string` | Plain-language description for the human to read before signing |

## Canonical Serialization Rules

1. Sort all keys alphabetically (deterministic JSON)
2. No whitespace between keys/values (compact)
3. ASCII-safe encoding (`ensure_ascii=True`)
4. Ed25519 sign the **raw canonical JSON bytes** directly — Ed25519 does internal SHA-512 hashing. Do NOT pre-hash with SHA-256 before signing, or the signature won't verify.
5. The `jsh` (judge state hash) returned in the ALLOW result is `SHA-256(canonical_bytes)` — this is for ledger binding, NOT for signing.

## Signing Payload

```python
import json, base64

payload = {
    "actor": "arif",
    "session_id": "sess_xyz",
    "candidate_hash": "sha256:deadbeef...",
    "action_class": "ACTION_AUTHORIZATION",
    "reversibility": "R4",
    "blast_radius": "MEDIUM",
    "seal_purpose": "AUTHORIZE",
    "authority_effect": "EXECUTION_GRANT",
    "audience": "arifOS",
    "nonce": "base64_nonce_here",
    "issued_at": "2026-07-25T12:00:00Z",
    "expires_at": "2026-07-25T12:02:00Z"
}
# Canonical: sorted keys, no whitespace, ASCII-safe
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
# Sign the raw bytes — Ed25519 handles hashing internally
signature_b64 = base64.b64encode(private_key.sign(canonical.encode())).decode()
```

## Verifying Flow

```python
# Reconstruct the canonical payload from stored challenge
from arifosmcp.runtime.crypto_auth import serialize_challenge_for_signing
canonical = serialize_challenge_for_signing(stored_challenge_dict)
try:
    public_key.verify(sig_bytes, canonical)
    # OK — signature matches canonical payload
except InvalidSignature:
    # FAIL — payload was tampered with
```

⚠️ **Important:** `serialize_challenge_for_signing()` (spec-compliant) omits None-valued
optional fields and keys not present in the dict. `canonical_serialize_challenge()` (legacy)
always includes all keys with empty-string defaults. Use the same function on both
signing and verification sides — never mix the two.

## Authorization Response (after successful verification)

```json
{
  "verdict": "ALLOW",
  "cc_id": "cc_<sha256[:16]>",
  "jsh": "<sha256_hex>",
  "authorization_id": "auth_<uuid16>",
  "authorization_consumed": true,
  "challenge_id": "chal_<uuid12>",
  "actor_id": "arif",
  "blast_radius": "MEDIUM",
  "reversibility": "R0",
  "nonce": "<base64_nonce>"
}
```
