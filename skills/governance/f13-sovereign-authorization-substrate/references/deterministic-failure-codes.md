# F13 Deterministic Failure Codes

These are the canonical failure reason codes for F13 challenge-based authorization.
Every failure path MUST return one of these — not generic strings.

> **Deployment status:** 13 core codes exist in `crypto_auth.py` as both
> `F13_FAILURE_CODES` (human-readable messages) and `FAILURE_CODES` (code→code mapping).
> Classification (CL6-8) and A-FORGE (F1-F6) codes are Phase 2 aspirational — not yet
> deployed. Wired into `verify_authorization_challenge()` and `verify_judge_signature()`
> but NOT yet into the judge `ESCALATE` response path.

## Core Auth Failures ✅ (deployed)

| Code | Meaning | When | In `FAILURE_CODES`? |
|---|---|---|---|
| `F13_REQUIRED` | Action classified R4/R5 and no valid authorization supplied | Judge first pass | ✅ |
| `SIGNATURE_MISSING` | No Ed25519 signature provided with authorization_response | Judge verify pass | ✅ |
| `SIGNATURE_INVALID` | Signature present but Ed25519 verification failed | Judge verify pass | ✅ |
| `KEY_NOT_REGISTERED` | Actor's public key not found in any registry | Judge verify pass | ✅ |

## Challenge Lifecycle ✅ (deployed)

| Code | Meaning | When | In `FAILURE_CODES`? |
|---|---|---|---|
| `CHALLENGE_UNKNOWN` | challenge_id not in issued store (wrong ID, or already consumed+purged) | Judge verify pass | ✅ |
| `CHALLENGE_EXPIRED` | Challenge TTL exceeded (default 120s) | Judge verify pass | ✅ |
| `NONCE_REPLAY` | Nonce already consumed — atomic consume detected duplicate | Judge verify pass | ✅ |
| `AUTHORIZATION_ALREADY_CONSUMED` | authorization_id already used in prior execution | A-FORGE gate | ✅ |

## Binding Mismatches ✅ (deployed)

| Code | Meaning | When | In `FAILURE_CODES`? |
|---|---|---|---|
| `ACTOR_MISMATCH` | Signed actor != actor in the current session/challenge | Judge verify pass | ✅ |
| `SESSION_MISMATCH` | session_id in signed payload != current session | Judge verify pass | ✅ |
| `CANDIDATE_HASH_MISMATCH` | candidate hash changed between challenge issuance and verification | Judge verify pass | ✅ |
| `PLAN_HASH_MISMATCH` | plan hash changed between challenge issuance and verification | Judge verify pass | ✅ |
| `AUDIENCE_MISMATCH` | Signed audience != expected audience (e.g. wrong organ) | Judge verify pass | ✅ |

## Classification Failures ❌ (Phase 2 — not yet deployed)

| Code | Meaning | When | In `FAILURE_CODES`? |
|---|---|---|---|
| `CLASSIFICATION_HOLD` | Reversibility class cannot be determined — treat as R4 (fail closed) | Judge reversibility gate | ❌ |
| `BLAST_RADIUS_UNKNOWN` | Blast radius could not be determined — fail closed | Judge reversibility gate | ❌ |
| `CAPABILITY_NOT_RECOGNIZED` | Requested capability is not a known tool/action | Judge capability gate | ❌ |

## A-FORGE Execution Failures ❌ (Phase 2 — not yet deployed)

| Code | Meaning | When | In `FAILURE_CODES`? |
|---|---|---|---|
| `MISSING_AUTHORIZATION_ID` | forge called without authorization_id | Forge preflight | ❌ |
| `MISSING_CONSTITUTIONAL_CHAIN_ID` | forge called without cc_id | Forge preflight | ❌ |
| `MISSING_JUDGE_STATE_HASH` | forge called without jsh | Forge preflight | ❌ |
| `AUTHORIZATION_EXPIRED` | authorization_id TTL exceeded | Forge preflight | ❌ |
| `CANDIDATE_DRIFT` | candidate hash at forge time != candidate hash from authorization | Forge preflight | ❌ |
| `SEAL_RECORD_AS_EXECUTION` | seal_type=RECORD passed where AUTHORIZATION required | Forge preflight | ❌ |

## Response Shape

All failure responses follow this shape:

```json
{
  "decision": "ESCALATE",
  "reason": "<CODE>",
  "authorized_execution": false,
  "requires_human_signature": true,
  "authorization_consumed": false,
  "failure_detail": "<human-readable explanation of what went wrong and how to retry>"
}
```

For execution-bound failures (A-FORGE gate):

```json
{
  "verdict": "HOLD",
  "reason": "<CODE>",
  "authorized_execution": false,
  "forged": false,
  "failure_detail": "<human-readable>"
}
```
