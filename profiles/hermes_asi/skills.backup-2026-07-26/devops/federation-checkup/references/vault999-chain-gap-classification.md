# VAULT999 Chain Gap Classification

**Forged: 2026-07-19 | Pattern from authority recovery mission**

## The Core Insight

VAULT999 seals use PostgreSQL SERIAL/IDENTITY columns for IDs. Gaps in the ID sequence are a **database artifact**, not data corruption. The health indicator to check is **`tip_linkage`** (whether predecessor hash chain validates), not whether IDs are contiguous.

## Quick Classification

```bash
curl -s http://localhost:8100/vault/status | python3 -c "
import json, sys
d = json.load(sys.stdin)
gaps = d.get('chain_gaps', 0)
total = d.get('vault_seals_total', 0)
id_range = d.get('id_range', {})
expected = id_range.get('max', 0) - id_range.get('min', 0)
gap_pct = (gaps / expected * 100) if expected else 0

print(f'Seals: {total}')
print(f'ID range: {id_range.get(\"min\")}–{id_range.get(\"max\")} ({expected} slots)')
print(f'Gaps: {gaps} ({gap_pct:.1f}%)')
print(f'Tip linkage: {d.get(\"tip_linkage\")}')  # THIS is the real health indicator
print(f'Chain integrity: {d.get(\"chain_integrity\")}')
print(f'Sovereign ruling: {d.get(\"known_migration_gap_ruling\", \"none\")}')

# Classification
if d.get('tip_linkage') == 'tip_linked':
    print('VERDICT: Hash chain intact — gaps are DB artifact, not corruption')
elif d.get('tip_linkage') == 'tip_broken':
    print('VERDICT: CRITICAL — hash chain broken, investigate immediately')
else:
    print(f'VERDICT: Unknown — tip_linkage={d.get(\"tip_linkage\")}')
"
```

## Chain State Classification Matrix

| Classification | `tip_linkage` | ID Continuity | Meaning |
|---------------|---------------|---------------|---------|
| `CHAIN_VALID_MULTI_EPOCH` | `tip_linked` | Multiple schemes coexist | Mixed sequence types; contiguous within each epoch |
| `CHAIN_CONTIGUOUS` | `tip_linked` | No gaps | Single numeric sequence, fully populated |
| `CHAIN_VALID_SEQUENCE_SPARSE` | `tip_linked` | Gaps present | DB auto-increment gaps (rollbacks, failed txs). No corruption. |
| `CHAIN_CORRUPT` | `tip_broken` | Any | Hash chain broken — P0 alert |

## Gap Causes (All Benign)

1. **Failed transactions**: PostgreSQL SERIAL sequences advance even on ROLLBACK
2. **Pre-migration records**: Old DB IDs (1-16) not migrated to Supabase
3. **Concurrent write conflicts**: Two writers racing for the same sequence value
4. **Test/dry-run seals**: Rolled-back test seals consume sequence slots

## When To Escalate

- `tip_linkage` = `tip_broken` → P0 — hash chain integrity loss
- `chain_gaps` > 50% of expected → P1 — investigate for systematic write failure
- `last_seal` age > 7 days → P2 — may indicate write path blockage
- `pending_holds` > 0 → P1 — seals waiting for human approval

## Anti-Patterns

- **Never re-sequence IDs to close gaps** — destroys multi-epoch provenance
- **Never trust sequential IDs for integrity** — use predecessor hash chains instead
- **Never flag gaps as corruption** without checking `tip_linkage` first
- **Never assume `total_seals` = `max_id - min_id`** — always check `chain_gaps` count
