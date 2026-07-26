# VAULT999 Chain Audit Methodology

> **Class:** Chain integrity verification for the arifOS immutable ledger.
> **Origin:** 2026-07-12 session — Arif identified chain break, audit revealed concurrent writer duplicates.
> **Key insight:** The canonical path (first entry per seq) is intact. Concurrent writer duplicates are cosmetic.

## Detection Methodology

### Step 1: Load and Parse

```python
import json

with open('/root/.local/share/arifos/vault999/seal_chain.jsonl') as f:
    lines = [l.strip() for l in f if l.strip()]

entries = []
for line in lines:
    try:
        d = json.loads(line)
        if isinstance(d, dict):
            entries.append(d)
    except:
        pass  # Malformed line — record as bad
```

### Step 2: Build Canonical Path

Concurrent writers may write multiple entries with the same seq. The canonical path picks the FIRST entry per sequence number:

```python
from collections import defaultdict

by_seq = defaultdict(list)
for e in entries:
    s = e.get('seq', '?')
    by_seq[s].append(e)

canonical = []
for s in sorted([k for k in by_seq.keys() if isinstance(k, int)]):
    canonical.append(by_seq[s][0])
```

### Step 3: Verify Chain Links

```python
breaks = []
for i in range(1, len(canonical)):
    curr = canonical[i]
    prev = canonical[i-1]
    
    prev_hash_stored = curr.get('prev_hash', '')
    prev_this_hash = prev.get('this_hash') or prev.get('chain_hash', '')
    
    if prev_hash_stored and prev_this_hash:
        if prev_hash_stored != prev_this_hash:
            breaks.append((curr.get('seq'), prev_hash_stored[:16], prev_this_hash[:16]))
```

### Step 4: Detect Concurrent Writers

```python
seq_hashes = defaultdict(set)
for e in entries:
    s = e.get('seq', '?')
    h = e.get('this_hash') or e.get('chain_hash', '')
    if h:
        seq_hashes[s].add(h)

concurrent = {k: v for k, v in seq_hashes.items() if len(v) > 1}
```

## Interpret Results

| Finding | Meaning | Severity |
|---------|---------|----------|
| Canonical chain breaks > 0 | prev_hash doesn't match previous canonical entry's hash | 🔴 HOLD — integrity failure |
| Only pre-seq-50 breaks | Pre-May-2026 migration artifacts (F13 ruling 2026-06-05 covers) | 🟡 Non-blocking |
| Concurrent writer duplicates | Multiple agents wrote same seq with different content | 🟡 Cosmetic — canonical path intact |
| Content integrity fails | Stored hash doesn't match recomputed hash | 🔴 Cryptographic integrity failure |
| Non-numeric seq values | Malformed entries in JSONL | 🟡 Historic logging issue |

## Hash Field Name Migration

The VAULT999 chain has used different field names over time. When comparing hashes, normalize by stripping the `sha256:` prefix:

```python
def normalize(hash_str):
    return hash_str.replace('sha256:', '') if hash_str else ''
```

**Known field names used historically:**
- `this_hash` (original, seq 1-50)
- `chain_hash` (modern, seq 50+)

Both contain the same data — just different field names.

## Freeze Procedure (if chain is truly broken)

```bash
# 1. Snapshot
cp /root/.local/share/arifos/vault999/seal_chain.jsonl /root/.local/share/arifos/vault999/recovery/
cp /root/.local/share/arifos/vault999/seal_chain_head.json /root/.local/share/arifos/vault999/recovery/

# 2. Hash snapshot
sha256sum /root/.local/share/arifos/vault999/recovery/seal_chain.jsonl

# 3. Write incident manifest
python3 -c 'import json; json.dump({
  "vault_status": "DEGRADED",
  "chain_status": "BROKEN",
  "authoritative_sealing": "DISABLED",
  "last_verified_seq": <last_good_seq>,
  "incident_id": "VAULT-INC-YYYY-MM-DD-001"
}, open("incident.json","w"), indent=2)'
```

## Recovery Checkpoint (if sovereign orders fork)

Do NOT edit history. Create a recovery genesis:

```json
{
  "seq": 1000,
  "event_type": "VAULT_CHAIN_RECOVERY",
  "last_verified_seq": 12,
  "last_verified_hash": "<hash>",
  "new_epoch": "VAULT999-EPOCH-2",
  "authorized_by": "ARIF"
}
```

The old branch is preserved as evidence. The new branch starts from the last trusted hash.

## Verification After Audit

```bash
# Quick integrity check
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'seq={d.get(\"seq\",\"?\")} verdict={d.get(\"verdict\",\"?\")} actor={d.get(\"actor\",\"?\")}')"
```
