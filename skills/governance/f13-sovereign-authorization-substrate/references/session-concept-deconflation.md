# Session Concept Deconflation — Transport vs Authorization

> Forged 2026-07-25 from live E2E debugging. The single most critical architectural fix in the F13 challenge auth flow.

## The Bug

`verify_authorization_challenge()` was called with `session_id=""` (empty string) because the MCP transport session ID differed from the one passed as an argument. The empty string silently turned off session binding checks — any transport session could use any challenge.

## The Fix

| Before | After |
|---|---|
| One `session_id` field meaning "whatever the caller sends" | Two separate concepts with explicit names |
| `session_id=""` silently bypassed binding checks | Empty transport session is NOT a valid signal |
| Challenge bound to ephemeral MCP connection ID | Challenge bound to stable actor/sovereign session |

## The Two Concepts

| Concept | `transport_session_id` | `authorization_session_id` |
|---|---|---|
| Purpose | Ephemeral MCP connection/request identity | Stable sovereign/SCT session |
| Lifetime | Per-request | Hours (SCT TTL) |
| Changes | Changes between calls | Stable across transport changes |
| Example | MCP JSON-RPC `session_id` param | SCT-derived session, actor-bound |
| Source | Network layer (FastMCP) | Kernel authority resolver |
| Used in challenge? | No | Yes — canonical payload field |

## Canonical Payload Field

The challenge is serialized with `authorization_session_id` (not `session_id`):

```json
{
  "actor": "arif",
  "authorization_session_id": "SEAL-b0755a09...",
  "nonce": "...",
  "candidate_hash": "sha256:abc123",
  ...
}
```

## Production Rule

`issue_authorization_challenge()` accepts `authorization_session_id` (derived from SCT/actor identity).
`verify_authorization_challenge()` loads from Redis/in-memory by nonce — no caller-supplied fields except `actor`, `nonce`, `signature_b64`. The stored payload is the single source of truth for what was signed.

## Why This Matters

A changed MCP transport connection between challenge issuance and signed verification must NOT invalidate an otherwise valid authorization. The constitutional authorization is about WHO approved WHAT, not which TCP connection they used.

## Files Changed

- `arifosmcp/runtime/crypto_auth.py`: `session_id` → `authorization_session_id` in `issue_authorization_challenge()`, `canonical_serialize_challenge()`, `_build_authorization_request()`, `_load_challenge_by_nonce()`
- `arifosmcp/tools/arif_kernel_intercept.py`: caller updated to pass `authorization_session_id=actor` to `issue_authorization_challenge()`
