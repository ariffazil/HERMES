---
name: vault999-reader
description: >
  Bridge to arifOS VAULT999 append-only ledger. READS seal entries,
  verifies chain integrity, lists recent vault operations — AND knows
  the legitimate WRITE path (local append-only chain via AAA
  a2a-server/seal_chain.js) when the arifOS MCP seal gate refuses
  SOVEREIGN authority. USE WHEN: "check vault", "vault999 status",
  "read seals", "ledger integrity", "arifOS vault", "seal the artifact",
  "arif_seal refused", "888_HOLD on seal", "append to vault",
  "audit receipt for SEAL".
---

# Vault999 Reader (now Reader + Audit-Receipt Writer)

**Two paths, one chain. Read freely. Write only via the proven audit-receipt pattern.**

## Decision Tree — which path do I need?

```
Q: Do I just want to READ or VERIFY the ledger?
   → See "Read Path" below. (Direct filesystem read — no MCP gate.)

Q: Arif said "seal X" / "arif_seal" / "write to VAULT999"?
   → See "Write Path" below. CRITICAL: do not invent a custom writer.
   → There is exactly ONE legitimate writer: /root/AAA/a2a-server/seal_chain.js

Q: arif_seal returned "888_HOLD: ATOMIC requires arif_ack_id"?
   → This is the ENVELOPE VALIDATION GATE (2026-07-11 discovery).
   → Different from the "authority LOW" gate. Fires even with FULL+verified sessions.
   → The session token is not propagating to the seal middleware.
   → See "Gate B: arif_ack_id envelope" below.
```

## Read Path

1. Chain location: **`/root/.local/share/arifos/vault999/seal_chain.jsonl`** (append-only ledger — **this is the active path; older docs that say `/root/VAULT999/seal_chain.jsonl` are OUTDATED**. Verified 2026-07-09 against the live chain: 132 entries, recent seals at seq 85+ show the writer has migrated. The `/root/VAULT999/` parent directory may not exist on all hosts — check the `.local/share/arifos/` path first.)
2. Chain head: **`/root/.local/share/arifos/vault999/seal_chain_head.json`** (current seq + hash)
3. Dormant historical ledger: `/srv/arifos/VAULT999/SEALED_EVENTS.jsonl` (last activity 2026-04-21; do NOT trust for "today's seals")
4. Writer (canonical): `/root/AAA/a2a-server/seal_chain.js`
5. Mirror (Python): `/root/arifOS/arifosmcp/runtime/seal_chain.py`
6. Use `getHead()`, `getChainLength()`, `getRecent(n)`, `verifyChain()` from the writer.
6. **Verify quirk**: `verifyChain()` is sync (NOT async — it returns a plain object,
   not a Promise). Calling `.then()` on it throws TypeError. Also: walking the full
   ledger often reports `prev_hash mismatch` on the seq 18-60 legacy range —
   this is a KNOWN ACCEPTED GAP (sovereign ruling 2026-06-05), not new damage.
   Check `broken_at_seq` — if it's between 18 and 60 inclusive, OR if `prev_hash`
   equals 'genesis', the writer is supposed to skip it (it does).

## Write Path — The Audit-Receipt Pattern

> **Proven 2026-07-09, seq=8 (Quantum Substrate Architecture).**
> Same pattern as seq=7 (hermes-cognitive, kernel zen audit, same day).

When `mcp__arif_fazil__arif_seal` returns `888_HOLD` because authority
is `LOW` instead of `SOVEREIGN`, do NOT invent a workaround. There is
a legitimate next path: the local append-only chain writer. It is the
same writer the kernel uses when its own SOVEREIGN gate refuses.

### Step 1 — Confirm gate refused honestly

```javascript
const result = await mcp__arif_fazil__arif_seal({...}, mode: 'dry_run');
// expected: 888_HOLD, capability 'kernel.seal', authority LOW
// If you see this, MCP path is closed for this session.
```

### Step 2 — Build payload with HONEST downgrade fields

The writer enforces FOUR structural invariants (G1 fix, forged 2026-07-05):

| Invariant | Requires for SEAL | If violated |
|---|---|---|
| INV-1_KERNEL_VERIFIED | `kernel_verdict ≠ UNKNOWN/FAIL` | downgrade → HOLD |
| INV-2_ACTOR_VERIFIED | `actor_source ≠ self_report` | downgrade → HOLD |
| INV-3_WITNESS_PRESENT | ≥1 non-null witness channel | downgrade → HOLD |
| INV-4_SESSION_LINEAGE | real `session_id` + `context_id` | downgrade → HOLD |

For an audit-receipt via local chain, you WILL trip INV-1 and INV-2.
That is correct. Set `kernel_verdict: 'UNKNOWN'` and
`actor_source: 'self_report'` honestly — the verdict WILL be downgraded
to HOLD, and the entry will carry the violation reasons under
`invariants_violated[]`. **This is the receipt**: an honest HOLD is
better than a fabricated SEAL.

### Step 3 — Witness triangle (INV-3)

Provide at least one non-null witness channel:

```javascript
witness: {
  human: 'verbal-ack:ARIF:<signal>:<date>',     // captured sovereign signal
  ai:    'hermes-cognitive:<action>:<date>',     // this dispatch
  external: null,                                 // populated by remote mirror
}
```

### Step 4 — Write (two methods)

**Method A: JavaScript writer (canonical, with invariant checking)**
```javascript
const { writeSeal } = require('/root/AAA/a2a-server/seal_chain.js');
const result = await writeSeal(payload, {
  event_type: 'session.seal',
  principal: 'agent:<actor>',
  active_floors: ['F1','F2','F3','F4','F7','F9','F11','F13'],
  trigger_reason: 'human_request',
  violated_floors: null,
  input_hash: sha256(artifact_content),
});
// result.verdict will be 'HOLD' (downgraded). result.invariants_violated lists why.
// Chain advances seq by 1. prev_hash on the new entry = old head. Hash chain intact.
```

### Step 5 — Verify the new link, not the whole chain

```javascript
const head = sc.getHead();           // {seq, hash, merkle_root, ...}
const recent = sc.getRecent(2);      // [seq=N-1, seq=N]
// Confirm: recent[1].prev_hash === recent[0].this_hash === old head hash
// That single-link check is what matters. Full verifyChain() will likely
// still report "broken" because of legacy seq 18-60 — that is pre-existing.
```

### Step 6 — Receipt

Output to Arif:
- seq + this_hash + merkle_root + prev_hash (proves chain link)
- final_verdict (will be HOLD — say so, don't dress it up)
- invariants_violated (the receipt for WHY it was downgraded)
- irreversibility_class: `LOW_RISK_RECEIPT` (matches hermes-cognitive seq=7)
- the exact sovereign signal that triggered the write (e.g. 'arif_seal')

## What It Checks

- VAULT999 directory and file existence
- vault999.jsonl entry count and JSON validity
- arifOS MCP `arif_vault_seal` and `arif_judge_deliberate` tool availability
- Chain integrity (new entry's prev_hash matches previous head)
- G1 invariants are visible on every entry (`invariants_violated[]`)
- Remote mirror is best-effort (HTTP 422 is OK, local chain is authoritative)

## Anti-patterns

- ❌ Custom writer at /tmp or anywhere else. Use the canonical writer.
- ❌ Fake a SOVEREIGN signature to bypass the MCP gate. The gate refused for a reason.
- ❌ Set `actor_source: jwt_verified` without a real JWT. F2 TRUTH violation.
- ❌ Pretend the verdict is SEAL when the writer downgraded it. Honest HOLD = receipt.
- ❌ Trust `verifyChain()` as a fresh-state signal — legacy gaps exist.
- ❌ Passing session_token to arif_seal thinking it will fix the arif_ack_id gate — it won't. The middleware intercepts before the tool runs.

## Gate B: arif_ack_id envelope (2026-07-11 discovery)

When `arif_seal` returns:
```json
{"status":"HOLD","verdict":"HOLD","result":{"reason":"ATOMIC requires arif_ack_id (L13 sovereign approval)","gate":"envelope_validation"}}
```

This is a **middleware-level gate**, not the tool's own authority check. It fires:
- Even when `arif_init` returned `authority: FULL` + `actor_verified: true`
- Even when passing `session_token` explicitly
- The nine_signal shows `delta: RETAK` (CRACKED — config mismatch)

**Root cause:** The `_envelope` parameter on `arif_seal` requires an `arif_ack_id` field — a sovereign acknowledgment ID that the standard `arif_init` flow does not produce. The session token is not being propagated from the MCP gateway to the seal middleware.

**Current workaround:** Use the filesystem Read Path for reads, or the local chain writer (Write Path) for audit-receipt writes. The MCP seal path is blocked until the envelope validation is fixed.

**Fix needed:** Either:
1. `arif_init` should emit an `arif_ack_id` when sovereign identity is verified, OR
2. The seal middleware should derive ack authority from the verified session token, OR
3. Add `arif_ack_id` as a first-class parameter on `arif_seal` that the gateway populates.

## References

- `references/audit-receipt-pattern.md` — full seq=8 receipt transcript with all invariants, payload, hashes
- `scripts/seal_audit_receipt.js` — ready-to-adapt writer template
