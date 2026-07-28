# F13 Challenge-Based Authorization — Architecture & Phase Path

> Key insight from 2026-07-25 session: Ed25519 alone eliminates shared-secret auth but not copy-paste. The gap is the human experience layer, not the cryptography.

## What F13 Proved

Before this session, F13 was a sentinel string compare (env var match). After this session:

| Before | After |
|---|---|
| String compare against `ARIFOS_SOVEREIGN_KEY` env | Real Ed25519 signature verification |
| Anyone with the env var value could bypass | Only holder of `arif_private.pem` can authorize |
| No replay protection | Challenge-based nonce, consumed after one use |
| DID registry under `/root/` (permission-denied risk) | `/opt/arifos/.secrets/did/` with systemd drop-in guards |
| `authority_token` was the only param | `actor_signature` + `nonce` + `key_id` exposed on MCP schema |

## The Four-Layer Reality of Any Constitutional Element

This session established a framework for evaluating whether a constitutional element is "real":

| Layer | Status | Meaning |
|---|---|---|
| Code | ✅ Real | The logic exists, imports succeed, function is callable |
| HOLD power | ✅ Real | ESCALATE stops the chain; downstream tools see the block |
| Canonical binding | ✅ Real | cc_id + judge_state_hash emitted; binds verdict to receipt |
| F13 Ed25519 crypto | ✅ Real | Challenge-based one-time nonce; Ed25519 verify; replay-safe |
| Zero-bypass actuator | ❌ Not yet proven | Direct VAULT append path exists (recovery bypass) |

**Rule:** A system is as real as its weakest enforcement layer. If the actuator can bypass the chain, the chain is advisory, not constitutional.

## Identity Authentication ≠ One-Time Action Authorization

This is the session's core architectural distinction:

| Property | Identity Auth (one-time) | Action Auth (per-action) |
|---|---|---|
| Proves | "This key signed this challenge" | "Arif approved THIS specific action NOW" |
| Nonce | Random, user-generated | Kernel-issued, bound to action |
| Replay-safe | No (same nonce+signature replayed) | Yes (nonce consumed after use) |
| Binds to | actor_id | candidate_hash + session_id + action_class |
| Used for | arif_init, session establish | arif_judge, forge_seal, action authorization |

The free-nonce path (still available with `ARIFOS_FREE_NONCE_ALLOWED=true`) is identity auth only. The challenge-based path (default) is action auth.

## Phase 1-4 Path to Zero Copy-Paste

| Phase | Architecture | Human Experience |
|---|---|---|
| **1** (done) | Challenge-based Ed25519; one-time nonce; DID under `/opt/arifos/` | Copy nonce → sign → paste signature (crypto-clerk) |
| **2** (next) | Judge embeds challenge in ESCALATE response; AAA approval card | Read action summary → tap Approve → done |
| **3** | WebAuthn/passkey; biometric/PIN; origin+RP ID binding | Face ID / fingerprint → approve |
| **4** | Risk-adaptive tiering; scoped delegation | Only R4-R5 prompts; R0-R3 autonomous |

### Phase 2 Key Design: Judge-Driven Challenge

Instead of the agent calling `issue_actor_challenge()` separately, the judge embeds the challenge in its ESCALATE response:

```
arif_judge(action_class=ACTION_AUTHORIZATION, reversibility=R4)
  → ESCALATE + authorization_request { nonce, session_id, candidate_hash, human_summary }
  → AAA renders approval card
  → Arif taps Approve (passkey/signer signs the challenge)
  → arif_judge again with actor_signature + nonce
  → ALLOW + cc_id
```

This eliminates the need for a separate `arif_challenge` tool.

## AUDIT_RECORD vs ACTION_AUTHORIZATION — Seal Purpose Separation

Audi0t records (R2, no F13) and action authorization (R4/R5, F13 required) are DIFFERENT seal purposes. This was the P0 fix from this session:

| Classification | reversibility_level | seal_purpose | authority_effect | F13 required |
|---|---|---|---|---|
| AUDIT_RECORD | R2 | RECORD | NONE | No |
| EVIDENCE_ATTESTATION | R2 | RECORD | NONE | No |
| VAULT_RECEIPT | R2 | RECORD | NONE | No |
| ACTION_AUTHORIZATION | R4 | AUTHORIZE | EXECUTION_GRANT | Yes |
| CONSTITUTIONAL_AMENDMENT | R5 | AUTHORIZE | SOVEREIGN_CHANGE | Yes |

The deterministic AUDIT_RECORD → R2 normalization prevents agents from accidentally triggering F13 on audit records.

## Direct VAULT Append — The Remaining Bypass

Receipts #4703 and #4704 (this session) were written directly to `/root/.local/share/arifos/vault999/outcomes.jsonl`. This is a recording bypass. It does not grant execution authority, but it means the canonical chain `judge → cc_id → seal → vault` can be circumvented.

**Fix:** Route all VAULT writes through `arif_seal`. The current gap is that `arif_seal` is still classified as L5/irreversible by `classify_tool()` regardless of `seal_purpose=RECORD`. Until that's fixed, the bypass exists.
