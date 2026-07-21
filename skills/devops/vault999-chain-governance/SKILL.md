---
name: vault999-chain-governance
description: "Manage VAULT999 append-only seal chain integrity — verification, writer hardening, incident response, IMAGE_SEAL separation, identity propagation, and recovery. Covers chain verification (hash chain walk, duplicate detection, fork detection), writer hardening (pg_advisory_xact_lock, FOR UPDATE, unique constraints), identity propagation (dual write path gap, actor_source/kernel_verdict plumbing), incident documentation (freeze → snapshot → manifest → classify), and recovery (epoch fork, quarantine, repair). Use when: Arif says 'check seal chain', 'vault integrity', 'VAULT999 chain break', 'writer hardening', 'IMAGE_SEAL', 'seq mismatch', 'prev_hash', 'chain audit', 'recovery fork', 'vault999 writer', 'identity propagation', 'actor_source', 'self_report receipts', 'anonymous receipts', 'receipts logging anonymous', or any task touching /root/.local/share/arifos/vault999/."
tags:
  - vault999
  - seal-chain
  - writer
  - postgres
  - integrity
  - incident
triggers:
  - "check seal chain"
  - "vault integrity"
  - "VAULT999 chain break"
  - "writer hardening"
  - "IMAGE_SEAL"
  - "seq mismatch"
  - "prev_hash mismatch"
  - "chain audit"
  - "recovery fork"
  - "vault999 writer"
  - "identity propagation"
  - "actor_source"
  - "self_report receipts"
  - "anonymous receipts"
  - "receipts logging anonymous"
  - "kernel_verdict"
  - "seal chain health"
  - "duplicate sequence"
  - "advisory lock"
  - "FOR UPDATE"
  - "epoch recovery"
  - "chain freeze"
  - "incident manifest"
---

# VAULT999 Chain Governance

> **Layer:** VAULT999 — Constitutional Ledger
> **Writer:** `/root/arifOS/deploy/vault999-writer/main.py` (FastAPI + asyncpg)
> **Chain file:** `/root/.local/share/arifos/vault999/seal_chain.jsonl`
> **Chain head:** `/root/.local/share/arifos/vault999/seal_chain_head.json`
> **Chain verifier:** `/root/arifOS/arifosmcp/runtime/vault_chain.py`
> **Seal chain JS tool:** `/root/AAA/a2a-server/seal_chain.js`

## Chain Structure

The seal chain is stored in two layers:

### Layer 1: PostgreSQL `vault_seals` table (canonical)
- Written by `vault999-writer` service (FastAPI, port 5001)
- Each row: `id`, `event_type`, `session_id`, `actor_id`, `seal_hash`, `chain_hash`, `prev_seal_id`, `action`, `payload`, `verdict`, `epoch`, `witness`, `signature`, `signed_by`, `sealed_at`
- Hash chain: `compute_chain_hash(prev_seal_hash, seal_hash)` links entries
- Writer auth: `X-Writer-Token` header + optional Ed25519 signature verification

### Layer 2: `seal_chain.jsonl` (flat-file mirror)
- Each line is a JSON object with `seq`, `prev_hash`, `this_hash`, `merkle_root`, `epoch`, `actor`, `verdict`, `payload`
- Written by `seal_chain.js` tool (Node.js)
- Hash chain: `sha256(prev_hash + current_content)` links entries
- `seal_chain_head.json` caches the latest seq

## Chain Verification

### Hash Chain Walk
```python
import json

chain = [json.loads(l) for l in open('/root/.local/share/arifos/vault999/seal_chain.jsonl')]
canonical = []
last_verified = 0

for i, entry in enumerate(chain):
    seq = entry.get('seq')
    if seq is None:
        continue  # IMAGE_SEAL or other non-seq entry
    prev = entry.get('prev_seal_hash', entry.get('prev_hash', ''))
    curr = entry.get('seal_hash', entry.get('this_hash', ''))
    
    if canonical:
        expected_prev = canonical[-1]['curr']
        if prev != expected_prev:
            print(f'BREAK at seq {seq}: prev_hash {str(prev)[:20]} ≠ expected {str(expected_prev)[:20]}')
            break
    canonical.append({'seq': seq, 'prev': prev, 'curr': curr})
    last_verified = seq

print(f'Last verified: seq {last_verified}')
```

### Duplicate Detection
```python
from collections import Counter
seqs = [e.get('seq') for e in chain if e.get('seq') is not None]
dupes = {s: c for s, c in Counter(seqs).items() if c > 1}
if dupes:
    print(f'Duplicate sequences: {dupes}')
    # First occurrence is canonical; sort by epoch for each dupe, keep earliest
```

### Key Rule: First Occurrence Per Seq Is Canonical
The chain may have cosmetic duplicates from early multi-writer days. The first entry per sequence number forms the canonical path. Sort by `ts`/`epoch` ascending for each duplicate seq, keep the first.

## Writer Hardening

### Problem: Concurrent Writer Races
Two concurrent `SELECT ... ORDER BY epoch DESC LIMIT 1` calls can read the same "last" record, both compute prev_hash from it, and both INSERT — creating duplicate sequences and broken prev_hash chains.

### Fix (Applied 2026-07-13)
In `/root/arifOS/deploy/vault999-writer/main.py`, both `write_seal()` and `write_audit_receipt()` must:

```python
# Acquire advisory lock to prevent concurrent writer races
await conn.execute("SELECT pg_advisory_xact_lock(999)")

# Read current head with FOR UPDATE to block concurrent readers
prev_row = await conn.fetchrow(
    """SELECT id, seal_hash, chain_hash FROM vault_seals
       ORDER BY epoch DESC LIMIT 1
       FOR UPDATE"""
)
```

**Controls required:**
- `pg_advisory_xact_lock(999)` — PostgreSQL advisory lock (transaction-scoped, auto-releases on commit/rollback)
- `FOR UPDATE` — row-level lock on the current head row, blocks concurrent writers
- `UNIQUE(epoch_id, sequence)` constraint on the database table
- `UNIQUE(receipt_id)` constraint — prevents duplicate seal receipts
- Startup chain verification — verify hash chain integrity on service start
- Stale prev_hash rejection — reject INSERT if `provided_prev_hash != actual_canonical_head`

## IMAGE_SEAL Separation

**Problem:** GEOX well-render IMAGE_SEAL entries use a different schema (`entry_type: IMAGE_SEAL`, no `seq` field) but were written to the same `seal_chain.jsonl` file, causing format transitions that confuse hash chain walkers.

**Fix:** IMAGE_SEAL entries MUST go to a separate file `image_seal_chain.jsonl`:
```python
# In GEOX renderer, change:
with open('/root/.local/share/arifos/vault999/seal_chain.jsonl', 'a') as f:
    json.dump(image_seal_entry, f)
# To:
with open('/root/.local/share/arifos/vault999/image_seal_chain.jsonl', 'a') as f:
    json.dump(image_seal_entry, f)
```

## Incident Response Protocol

When a chain break is detected:

### Step 1: FREEZE
Prevent all further authoritative sealing:
```bash
# Snapshot current chain
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p /root/VAULT999/incident-$(date +%Y-%m-%d)
cp /root/.local/share/arifos/vault999/seal_chain.jsonl /root/VAULT999/incident-$(date +%Y-%m-%d)/seal_chain_before.jsonl
cp /root/.local/share/arifos/vault999/seal_chain_head.json /root/VAULT999/incident-$(date +%Y-%m-%d)/seal_chain_head_before.json

# Mark vault status: DEGRADED
echo "Authoritative sealing: DISABLED"
echo "Chain status: DEGRADED"
```

### Step 2: CLASSIFY (Determine failure class)

There are three materially different failure classes:

| Failure | Detection | Repair |
|---------|-----------|--------|
| **Duplicate sequence numbers** | `Counter(seqs)` shows `seq > 1` | Canonical branch selection (first occurrence wins) + writer fix |
| **Wrong prev_hash** | Hash chain walk breaks at a specific seq | Fork from last verified record; create recovery epoch |
| **Format transition** (IMAGE_SEAL mixed in) | Entries without `seq` field in the chain file | Separate to `image_seal_chain.jsonl`; no repair needed for main chain |

Build an incident table without changing source records:

| Field | Source |
|-------|--------|
| `physical_id` | Line number in seal_chain.jsonl |
| `sequence` | `entry.get('seq')` or null |
| `timestamp` | `entry.get('ts', entry.get('epoch', ''))` |
| `prev_hash_claimed` | `entry.get('prev_seal_hash', entry.get('prev_hash', ''))` |
| `record_hash_stored` | `entry.get('seal_hash', entry.get('this_hash', ''))` |
| `writer_instance` | `entry.get('actor', '?')` |
| `failure_reason` | `duplicate_seq | prev_hash_mismatch | format_transition | none` |

Then establish: `last_good_record = highest sequence where recomputed_hash == stored_hash AND prev_hash == previous canonical record hash AND sequence increments exactly once`

### Step 3: DECIDE (Three options)

#### Option A: Cosmetic duplicates, chain intact
If first-occurrence path is clean (no prev_hash breaks, seq increments monotonic):
- **No fork needed.** Chain is trustworthy as-is.
- Document: "First-occurrence path is clean. Duplicates are cosmetic."
- Proceed directly to Step 4 (harden writer).

#### Option B: Broken chain, needs fork
If hash chain walk fails (prev_hash doesn't match):
- Keep damaged records as forensic evidence
- Create recovery checkpoint at `last_good_seq + 1`
- New entry declares `event_type: VAULT_CHAIN_RECOVERY`
- Include: `last_verified_seq`, `last_verified_hash`, `broken_branch_digest` (Merkle root of all damaged records), `incident_report_hash`, `recovery_policy_hash`, `new_epoch`
- Authorized by SOVEREIGN (ARIF F13)
- Witnessed by independent verifier

#### Option C: Format transition (IMAGE_SEAL in main chain)
- Move IMAGE_SEAL entries to separate file
- No repair needed for main chain
- Add startup check that warns if IMAGE_SEAL entries appear in main chain

### Step 4: DOCUMENT (Always)

Create incident manifest:
```json
{
  "incident_id": "VAULT-INC-YYYY-MM-DD-001",
  "detected_at": "...",
  "severity": "CRITICAL|HIGH|MEDIUM",
  "status": "FROZEN|RESOLVED|CORRECTION_ACCEPTED",
  "summary": "...",
  "last_verified_seq": N,
  "failure_class": "duplicate_sequence|prev_hash_mismatch|format_transition",
  "root_cause_hypothesis": "...",
  "snapshot_path": "...",
  "quarantined_records": {"seq_range": "N-M", "status": "QUARANTINED"},
  "recovery_plan": {"type": "...", "requires": ["SOVEREIGN authorization"]},
  "writer_controls_required": ["..."]
}
```

### Step 5: HARDEN
Apply writer hardening (see Writer Hardening section above).
Add database constraints:
```sql
ALTER TABLE vault_seals ADD CONSTRAINT unique_epoch_seq UNIQUE (epoch_id, sequence);
ALTER TABLE vault_seals ADD CONSTRAINT unique_receipt_id UNIQUE (receipt_id);
```

## Identity Propagation: The Dual Write Path Problem

> **Diagnosed 2026-07-13 by Claude (external review), confirmed by Hermes forensic trace.**

There are TWO write paths to the seal chain. Neither fully propagates identity verification.

### Path 1: Kernel Direct Write (Python)

**Location:** `arifOS/runtime/tools.py` → `_arif_vault_seal()`, lines ~17155-17171

The kernel writes a minimal chain entry directly to `seal_chain.jsonl`:
```python
chain_entry = {
    "id": entry_id,
    "previous_id": prev,
    "timestamp": _now(),
    "content_hash": content_hash,
    "actor_id": actor_id,       # passed but NOT verified at write time
    "session_id": session_id,   # passed but NOT verified at write time
    "type": "constitutional_seal",
}
```

**The gap:** The kernel DOES verify identity earlier in the flow (Ed25519 at line ~16764-16808, kernel evaluation at line ~16865), but the verification result (`signature_verified`, `authority_level`, kernel verdict) is **thrown away** — it never flows into `chain_entry`. The chain entry has no `actor_source` or `kernel_verdict` field.

### Path 2: AAA Enriched Write (Node.js)

**Location:** `AAA/a2a-server/seal_chain.js` → `writeSeal()`, lines ~600-720

The AAA writer produces enriched entries with `actor_source`, `kernel_verdict`, `witness`, `merkle_root`, etc. It has INV-1 through INV-4 invariants that check:
- INV-1: `kernel_verdict ≠ UNKNOWN/FAIL` for SEAL
- INV-2: `actor_source ≠ self_report` for SEAL
- INV-3: `witness_channels ≥ 1` for SEAL
- INV-4: session/context umbilical required

**The gap:** When the caller doesn't provide `actor_source`, it defaults to `self_report` (line 485). INV-2 only downgrades SEAL→HOLD — it marks the receipt as broken but doesn't FIX the identity. The invariant is reactive (punishes bad input) not proactive (verifies identity before writing).

### Current Chain State (2026-07-13)

```
167 total receipts:
  55  actor_source: self_report        (33% — unverified identity claims)
  43  kernel_verdict: UNKNOWN          (26% — kernel never adjudicated)
  28  actor_source: sovereign_ack
  20  actor_source: f13_sovereign_ack
  18  actor_source: sovereign_directive
  16  actor_source: jwt_verified       (10% — actually verified)
```

**F2 implication:** ~33% of receipts have unverified identity claims. Under F2 (TRUTH), these receipts are evidentially void — they assert an actor without proof.

### Fix Architecture (DEPLOYED 2026-07-13)

The fix was implemented and deployed on 2026-07-13. Key changes:

1. **`resolve_receipt_identity()`** — new shared resolver in `vault_receipt.py`. All receipt writers (ingress_middleware, forge, judge) call it before minting. Resolves real identity from session context when candidate is a placeholder (openclaw-anon, anonymous, unknown).

2. **Kernel path fix:** `_arif_vault_seal()` in `tools.py` now propagates `actor_source` (ed25519_verified | sovereign_directive | jwt_verified | kernel_evaluated) and `kernel_verdict` (PASS | FAIL) into the chain_entry dict.

3. **AAA path fix:** Not yet changed — the AAA writer still defaults to `self_report` when caller doesn't provide `actor_source`. But the kernel now provides it, so kernel-originated seals carry real `actor_source`.

4. **Backfill policy:** Historical `self_report` receipts are NOT rewritten (F1 immutability). Sovereign decision needed on whether to annotate or leave as-is.

## Pitfalls

### PITFALL: Kernel verification results are thrown away at write time

The kernel verifies identity (Ed25519, HMAC, forge session, kernel evaluation) BEFORE writing to the chain, but the verification result doesn't propagate into the chain entry. This means `actor_source` defaults to `self_report` even when the kernel DID verify. When tracing identity propagation bugs, check BOTH the verification path (lines ~16764-16865) AND the write path (lines ~17155-17171) — they are disconnected.

**Rule:** A chain entry's `actor_source` reflects what the WRITER knows, not what the KERNEL verified. If the writer doesn't receive the verification result, it defaults to `self_report`.

### PITFALL (DISCOVERED 2026-07-13 EUREKA deployment): `seal_chain.jsonl` is not the canonical chain — `receipts_v2.jsonl` is

The verifier `node /root/AAA/a2a-server/seal_chain.js verify` reads
`seal_chain.jsonl` (~282KB, ~160 entries). However the authoritative
ledger is `receipts_v2.jsonl` (~9.3MB). Two writers in two file formats
existed historically; the seed `seal_chain.jsonl` is a stub frozen in
early 2026 and contains 3-4 fork duplicates per seq in the 50-63 range.

**Symptom:** `node seal_chain.js verify` returns
`{ok: false, broken_at_seq: 61, reason: 'prev_hash mismatch'}` on
EVERY invocation after the chain reaches seq > 60. The chain head
file `seal_chain_head.json` references the canonical seq 9907 in
`receipts_v2.jsonl`, not the duplicate fork in `seal_chain.jsonl`.

**Distinguish before declaring crisis:**
```bash
# Which file is the canonical writer producing?
ls -la /root/.local/share/arifos/vault999/seal_chain.jsonl /root/.local/share/arifos/vault999/receipts_v2.jsonl
wc -l /root/.local/share/arifos/vault999/seal_chain.jsonl /root/.local/share/arifos/vault999/receipts_v2.jsonl

# Which file does the head point to?
cat /root/.local/share/arifos/vault999/seal_chain_head.json
tail -1 /root/.local/share/arifos/vault999/receipts_v2.jsonl | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('seq', 'no-seq'))"
```

**Rule:** do NOT mark a deployment as "chain integrity failure" solely
because `seal_chain.js verify` reports a fork in `seal_chain.jsonl`.
That file has been superseded by `receipts_v2.jsonl`; the verifier has
not yet been pointed at the new file. This is a writer/tooling bug, not
a chain break.

**Fix path (when F13 ratifies):**
1. Update `seal_chain.js` to read `receipts_v2.jsonl` (or whichever file
   the `seal_chain_head.json` references).
2. OR mark `seal_chain.jsonl` as legacy and stub the verifier to return
   `{ok: true, note: 'legacy stub; canonical in receipts_v2.jsonl'}`.
3. Freeze the duplicate-fork file (rename to
   `seal_chain.legacy-2026.jsonl`) so future verifiers ignore it.

**Reference Incident 2026-07-13:** EUREKA session ran
`build_convergence_receipt` (success, 8 tools, 13 floors, no schema
drift, runtime TRUE) but `node seal_chain.js verify` returned
`ok: false` with a `prev_hash mismatch` at the legacy duplicate-fork
boundary. Production-runtime convergence was achieved; chain verify
was a tooling artifact. Documented here so a future session does not
re-spent 30 minutes investigating what is just a writer routing issue.

### PITFALL: Over-escalation — not every duplicate is a break
Cosmetic duplicates from early multi-writer days are NOT chain breaks. Always run the first-occurrence-path walk before declaring a crisis. The chain is intact if every seq appears in the canonical path with the correct prev_hash. The correction from this session (2026-07-13): "I over-escalated. The chain was intact."

**Rule:** First-occurrence path seq 1→N must have zero breaks. The first entry per sequence number forms the canonical path — sort by timestamp ascending for duplicates.

### PITFALL: IMAGE_SEAL entries look like breaks but aren't
IMAGE_SEAL entries have a different structure (`entry_type`, `token`, `well_id`, `image_sha256`) without `seq` or `prev_hash` fields. A hash chain walk that iterates ALL entries sequentially will fail when it hits an IMAGE_SEAL — but the failure is in the walker, not the chain. Filter entries by `entry_type != 'IMAGE_SEAL'` before walking the hash chain.

### PITFALL: seal_chain.jsonl may have mixed JSON formats
Entries may be serialized with different settings (sorted keys vs not, with/without trailing newline). Use `json.loads(line.strip())` per line, not `json.load(file)`.

### PITFALL: Remote mirror fails silently
`seal_chain.js` attempts a remote mirror after each write. If the mirror rejects (HTTP 422), stderr shows the error but the LOCAL chain is intact. Always verify with `node seal_chain.js head` — the cosmetic error is not a failure.

### PITFALL: Deployment path mismatch — source ≠ runtime
arifOS source lives at `/root/arifOS/` but the running process uses `/opt/arifos/app/`. Editing source files alone does NOT deploy the fix. You must `cp` the modified files to `/opt/arifos/app/` THEN restart `systemctl restart arifos`. This bit the 2026-07-13 identity propagation fix — initial edits to `/root/arifOS/` had no effect until deployed to `/opt/arifos/app/`.

**Checklist:**
1. Edit files in `/root/arifOS/arifosmcp/...`
2. `cp /root/arifOS/arifosmcp/core/vault_receipt.py /opt/arifos/app/arifosmcp/core/vault_receipt.py` (repeat for each modified file)
3. `sudo systemctl restart arifos`
4. Verify with `curl -sf http://localhost:8088/health`
5. Check that new receipts use resolved identity

### PITFALL: The chain head file may lag behind
`seal_chain_head.json` caches the latest seq. If the writer adds entries but doesn't update the head, `tail -1 seal_chain.jsonl` shows a different seq than `head.json`. Always trust the chain file, not the head cache.

## Extending the Seal Chain: New Event Types

seal_chain.js supports extensible event types via `classifyEventType()` and
domain-specific validation functions. To add a new first-class VAULT999 type:

1. **Register** the `event_type` in `classifyEventType()` — match before generic fallback
2. **Write** a validation function with domain invariants (INV-{prefix}{N}_{NAME} convention)
3. **Wire** into `writeSeal()` — runs after `enforceSealInvariants`, violations merged
4. **Export** from `module.exports`

### Known Event Types

| event_type | Source | Since |
|------------|--------|-------|
| `a2a.dispatch` | A2A task dispatch | v2 |
| `cooling.receipt` | COOLING_RECEIPT (seal_v3) metabolic cycle | 2026-07-13 |
| `forge.shell` | A-FORGE shell execution | v2 |
| `constitutional.verdict` | arif_judge verdict | v2 |
| `tool.register` | Tool/agent registration | v2 |
| `seal.issued` | E1 SEAL issuance (JITU) | v2 |
| `seal.verified` | E1 SEAL verification/consumption | v2 |
| `session.seal` | Session closure seal | v2 |
| `a2a.general` | Generic/unclassified | v2 |

### COOLING_RECEIPT Invariants (seal_v3)

| Invariant | Check | Meaning |
|-----------|-------|---------|
| INV-C1 | `action_class === 'OBSERVE'` | COOLING-MUST-NOT-SELF-DEPLOY |
| INV-C2 | `caller` not contain "forge" | Cooling routes through governance, never execution |
| INV-C3 | `supersedes.type === 'COLD_LINK'` | Original seal immutable; COOLING is forward reference |
| INV-C4 | `judge_required=true` unless AUTO/OBSERVE_ONLY | Governance path must be explicit |

Full pattern documentation: `references/cooling-type-extension-pattern.md`

## PITFALL: eventType variable duplication when wiring new types
When wiring a new validation function into `writeSeal()`, the `eventType`
variable is declared in the validation block and must be reused (not redeclared)
in the enriched envelope fields section. Delete the second `const eventType = ...`
line in the envelope fields section. Syntax check with `node --check seal_chain.js`.

## File References

- Kernel write path: `/root/arifOS/arifosmcp/runtime/tools.py` (`_arif_vault_seal`, lines ~16595-17202, chain write at ~17155-17171)
- Kernel identity verification: `/root/arifOS/arifosmcp/runtime/governance_identity.py` (Ed25519, HMAC, forge session, sovereign signal)
- Kernel authority binding: `/root/arifOS/arifosmcp/runtime/authority.py` (AuthorityState, legacy mirror)
- AAA enriched writer: `/root/AAA/a2a-server/seal_chain.js` (INV-1 through INV-4, actor_source default, invariant enforcement)
- Writer (Postgres): `/root/arifOS/deploy/vault999-writer/main.py`
- Chain verifier: `/root/arifOS/arifosmcp/runtime/vault_chain.py`
- Chain file: `/root/.local/share/arifos/vault999/seal_chain.jsonl`
- Chain head: `/root/.local/share/arifos/vault999/seal_chain_head.json`
- JS seal tool: `/root/AAA/a2a-server/seal_chain.js`
- COOLING_RECEIPT spec: `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`
- Cooling type extension pattern: `references/cooling-type-extension-pattern.md`
- Identity propagation gap forensic trace: `references/identity-propagation-gap.md`
- PRL forge patterns (Qdrant + embedding + dual-gate): `references/prl-forge-patterns.md`
- Incident archive: `/root/VAULT999/` (per-date incident directories)
- VAULT999 recovery package: `/root/A-FORGE/forge_work/2026-07-12/VAULT999_RECOVERY_2026_07/`

## Reference Incident: VAULT-INC-2026-07-12-001

This session's chain scare is the canonical reference:
- **Detection:** 3 parallel writer branches, all seq 1-63 duplicated
- **Bias:** Initial hash walk over-escalated — flagged format transitions as breaks
- **Correction:** First-occurrence path was clean. Seq 55-62 modern era — every hash verified, every link clean.
- **Fix applied:** Writer hardening (advisory lock + FOR UPDATE)
- **Lesson:** Always walk first-occurrence path before declaring crisis

Incident archive at `/root/VAULT999/incident-2026-07-12/`:
- `incident_manifest.json`
- `seal_chain_before.jsonl`
- `seal_chain_head_before.json`
- `CORRECTION_ACCEPTED.md`
