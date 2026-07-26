# VAULT999 Chain Break Incident — Recovery Protocol

> **Incident:** VAULT-INC-2026-07-12-001
> **Status:** Frozen, recovery pending sovereign authorization

## Detection

Check chain integrity at startup:

```bash
python3 -c "
import json
chain = [json.loads(l) for l in open('/root/.local/share/arifos/vault999/seal_chain.jsonl') if l.strip()]
good = [r for r in chain if isinstance(r, dict) and r.get('seq') is not None]
last_good = 0
for i in range(1, len(good)):
    if good[i]['seq'] != good[i-1]['seq'] + 1:
        print(f'BREAK at seq {good[i][\"seq\"]}')
        break
    last_good = good[i]['seq']
print(f'Last verified seq: {last_good}')
"
```

**Symptoms:** duplicate seq, mixed-format entries (IMAGE_SEAL with entry_type in main chain), prev_hash mismatches.

**Root cause:** GEOX IMAGE_SEAL writer shared the same seal_chain.jsonl with a different schema. No seq field on IMAGE_SEAL entries broke chain continuity.

## Freeze Protocol

1. Stop authoritative sealing
2. Snapshot chain + head to `/root/VAULT999/incident-YYYY-MM-DD/`
3. Identify last verified seq (seq=12 in the incident)
4. Write incident_manifest.json

## Recovery Fork

Do NOT renumber or delete records. Fork explicitly:

- Keep damaged records as QUARANTINED forensic evidence
- Create recovery checkpoint at next seq, anchored to last verified hash
- New epoch: VAULT999-EPOCH-2
- Requires SOVEREIGN authorization (ARIF F13)
- Fix writer: add UNIQUE constraints, one canonical writer leader, idempotency keys

## Status Reporting

Use separate planes:
- **Runtime:** HEALTHY
- **Vault:** DEGRADED — chain integrity FAIL, last verified seq=X
- **Authority:** reversible ALLOWED, consequential HOLD, sovereign sealing DISABLED
