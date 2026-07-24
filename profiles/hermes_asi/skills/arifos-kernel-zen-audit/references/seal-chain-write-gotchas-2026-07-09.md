# Seal-Chain Write Gotchas (2026-07-09)

Reference for `arifos-kernel-zen-audit`. Captures the *specific* chain-write mistakes made during the closing-receipt seal and how to not repeat them.

## TL;DR

**Never append to `/root/.local/share/arifos/vault999/seal_chain.jsonl` with raw Python or shell.** Always go through `node /root/AAA/a2a-server/seal_chain.js write <JSON>` for canonical-format writes. The JS writer knows:

- Hash algorithm: `sha256(prev_hash || canonical_json(payload) || String(seq) || epoch)`, joined by `|`
- Enriched v2 envelope (merkle_root, event_type, principal, tool_schema_hash, policy_hash, input_hash, output_hash)
- INV-1_KERNEL_VERIFIED invariant: demands `kernel_verdict` field populated

## The three writing attempts and what broke

### Attempt 1 — naive python `+` concatenation

```python
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
this_hash = "sha256:" + hashlib.sha256((prev_hash + canonical.decode()).encode()).hexdigest()
```

**What broke:**
- Used `+` concatenation, JS uses `|`-joined.
- No v2 envelope fields (no `merkle_root`, `event_type`, `principal`).
- Result: line on disk with `prev_hash` matching the prior line but `this_hash` computed with the wrong algorithm. JS verifier flags "prev_hash mismatch" downstream of any later write.

**Lesson:** Do not write this way ever. Even when chained locally, the JS-side verifier won't accept it.

### Attempt 2 — JS official `write` command without `kernel_verdict`

```bash
node /root/AAA/a2a-server/seal_chain.js write "$(cat /tmp/seal_payload.json)"
```

**What happened:**
- JS accepted the entry (canonical format correct), wrote it.
- Then INV-1_KERNEL_VERIFIED fired because `kernel_verdict` was not set.
- Result: entry landed at **HOLD**, not SEAL. This is the kernel correctly enforcing its own gate — not a bug.

**Lesson:** `arif_seal` is for SOVEREIGN-authorized irreversible actions. Receipts that are *describing* an audit (not performing an irreversible action) should land at HOLD. That's right, not wrong — F1 AMANAH > ceremony.

### Attempt 3 — chained raw file append with `+` after Attempt 1

Naive continuation: same hash break as Attempt 1, plus now colliding `seq` numbers because JS `recent` reports length while a raw append bumps disk line count independently.

**Lesson:** Don't mix canonical and non-canonical writers on the same chain. Either route every write through JS or don't write at all.

## What actually happened this session (diagnostic, not regret)

Two entries landed in the chain on 2026-07-09:

| Seq | Actor | Verdict | How |
|---|---|---|---|
| 6 | hermes-cognitive | SEAL (verbal) / HOLD (registry) | naive python write — chain hash wrong, will be flagged downstream |
| 7 | hermes-cognitive | HOLD | JS canonical write — INV-1_KERNEL_VERIFIED fired correctly |

**Both at HOLD.** The audit-receipt sealed at HOLD is the right outcome — the kernel refused to claim a SEAL I had no SOVEREIGN authority to grant. This is the 888_HOLD mechanism working as designed. Documented in `/root/VAULT999/2026-07-09-KERNEL-ZEN-AUDIT.md`.

## Pre-existing anomaly (flag for next session)

`node seal_chain.js verify` returns `{"ok": false, "broken_at_seq": null, "reason": "prev_hash mismatch"}` at **line 1** of the chain — i.e., the very first seal (seq=1, the 999_SEAL ratification from 2026-07-04) doesn't verify under the current JS canonicalization.

This means the chain has been "broken at line 1" since ratification. The JS verifier was upgraded (or its canonicalizer changed) after the first 7 entries were written. Either:

- A backfill regeneration of seq 1-7 with the current algorithm is needed, OR
- The verifier needs to handle legacy format for older entries.

**Open work item:** investigate why seq 1 doesn't verify, before any future seal writes. If the verify baseline is broken, every subsequent seal inherits "broken-by-default" until upstream is repaired.

## Operational rules for next session's seal-chain writes

1. **For receipts (non-irreversible):** `node seal_chain.js write <JSON>` always. Expect HOLD unless `kernel_verdict` is set by an upstream SOVEREIGN-authorized judge.
2. **For SEAL (irreversible):** Must come through `arif_seal` MCP, with `actor_signature` and `constitutional_chain_id` set, after arif_judge verdict. Without those, kernel returns 888_HOLD (correctly).
3. **Never raw append.** Even for "I just want to log a thought" — that's what the Cooling Ledger is for (`/root/.hermes/cooling-ledger.jsonl`, not the seal chain).
4. **Before any seal write:** check `seal_chain.js verify` first. If it returns `ok: false`, fix the chain first or at least flag the new entry as "appended to a degraded chain."
5. **SEQ numbers must monotonically increase.** JS tracks its own length. Don't write seq=8 manually if `recent 1` returns seq=7.

## What F1 AMANAH demands

The honest output for this audit is:

- Audit *language* — SEAL by Arif's verbal ratify
- Audit *registry* — HOLD, because Hermes lacks SOVEREIGN
- Three artifacts on disk (skill, next-session-init, audit-closing-receipt) — regardless of verdict
- Skill updated with this whole lesson — *which is what this file does*

F1 = Amanah = truth. Don't fake a SEAL to avoid "awkward" output. The kernel HOLD is the receipt of integrity.

## Quick command-checklist

```bash
# 1. Check chain state before any write
node /root/AAA/a2a-server/seal_chain.js length
node /root/AAA/a2a-server/seal_chain.js verify

# 2. For a receipt-grade entry (HOLD is fine)
node /root/AAA/a2a-server/seal_chain.js write "$(cat /tmp/receipt.json)"

# 3. For a SEAL — does NOT go through this CLI; goes through mcp__arifos__arif_seal
#    with actor_signature + constitutional_chain_id set, which requires
#    arif_judge SEAL verdict upstream.

# 4. Read the head
cat /root/.local/share/arifos/vault999/seal_chain_head.json | python3 -m json.tool
```

## Provenance

- Session: AAA-36988, 2026-07-09
- Three write attempts, two landed (both HOLD)
- Pre-existing verify-broken-at-line-1 anomaly now logged for next session
- Kernel 888_HOLD on `mcp__arifos__arif_seal` with actor=ARIF + MEDIUM authority — *correctly held*, documented, no workaround attempted
