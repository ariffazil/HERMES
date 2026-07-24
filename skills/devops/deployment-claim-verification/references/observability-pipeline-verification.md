# Observability Pipeline Verification — Audit Pattern

When a deployment report claims observability system health (Kabarkan or similar), the claim involves a **multi-layer data pipeline** where one working layer can mask another's failure.

## The Three-Layer Pipeline

```
Kernel (arifOS)
  └── Telemetry.record_tool_call()
        ├── Path A: Flat dict ──→ NATS ──→ Standalone Worker ──→ Postgres
        ├── Path B: ObservationRecord.model_dump ──→ NATS* ──→ Standalone Worker ──→ Postgres
        └── Path C: ObservationRecord ──→ Local Backend (in-process) ──→ Postgres
```

- **Path C** (local backend) writes directly to Postgres inside the arifOS process — bypasses NATS entirely.
- **Paths A + B** go through NATS JetStream, then the standalone systemd worker writes to Postgres.
- Paths A and B are independent — Path A sends a flat dict without UUID fields, Path B sends the full ObservationRecord model.

## Verification Sequence

### Step 1: Independent probe per layer

```bash
# Layer 1 — What does Postgres actually contain?
PGPASSWORD="..." psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*) FROM observability.observations;"
PGPASSWORD="..." psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT id, tool_name, actor_id, verdict_class FROM observability.observations ORDER BY created_at DESC LIMIT 5;"

# Layer 2 — NATS stream health
nats stream info kabarkan-ingest | grep -E "Messages|Bytes|Subjects|Last Sequence"

# Layer 3 — Standalone worker health
systemctl is-active kabarkan-worker
journalctl -u kabarkan-worker --no-pager | grep -c "PG write failed"
journalctl -u kabarkan-worker --no-pager | tail -20
```

### Step 2: Classify the state

| Layer | Symptom | Interpretation |
|-------|---------|----------------|
| PG has rows | ✅ Observations counted | At least one path is working |
| NATS has messages | ✅ Data is streaming | Kernel telemetry is publishing |
| Worker active WITHOUT PG write failures | ✅ Full pipeline healthy | All three layers functional |
| PG has rows BUT worker shows PG failures | ⚠️ **Local backend working, standalone worker broken** | NATS→worker path has a bug; in-process path masks it |
| No PG rows, NATS has messages | ❌ Worker cannot persist | Schema mismatch or ID mapping issue |
| No PG rows, no NATS messages | ❌ Hooks not firing | trace_tool_call() never called |

### Step 3: Verify VAULT999 seal claims independently

```bash
# Check the actual outcomes.jsonl — never trust the session seal document alone
grep -i "<CLAIMED_SEAL_NAME>" /root/.local/share/arifos/vault999/outcomes.jsonl

# Also check forge_work for seal receipts
find /root/forge_work/$(date +%F) -name "*SEAL*" 2>/dev/null | head -10
```

A "VAULT999 seal" is a real entry in `outcomes.jsonl` with `"verdict": "SEAL"` — not a markdown file in `forge_work/`. If the only evidence of the seal is a mention in a session seal document, the seal was **declared but never executed**.

## Proven edge cases

### Dual NATS paths (Kabarkan 2026-07-24)

`Telemetry.record_tool_call()` had two independent NATS publishes:
1. `_nats()` with a flat dict (no UUIDs) → subject `kabarkan.ingest.span.{tool}`
2. `_publish_nats(record)` with `ObservationRecord.model_dump()` → subject `kabarkan.ingest.span.{trace_id}`

Both hit `kabarkan.ingest.>`. The standalone worker received both. Path A messages **always failed** with `null value in column "id"` because the flat dict had no `observation_id`. Path B messages would have succeeded if the worker correctly mapped `observation_id → id`.

The in-process local backend (Path C) wrote 17 observations successfully, creating the appearance of a working pipeline while the standalone worker failed on all 28 NATS messages.

**Lesson**: Always check `journalctl` for PG write failures in the worker, not just the observation count in the DB.

### Fake VAULT999 seal (Kabarkan 2026-07-24)

The session seal declared "VAULT999 seal: KABARKAN-ATLAS333-HOOK-SEALED written" but `outcomes.jsonl` had zero matches. The seal was written as a text claim in a markdown file, not as a real `arif_seal` call. Always verify against the actual append-only ledger.

## Automation

For repeatable verification, script the three-layer probe:

```bash
#!/bin/bash
# observability-health-check.sh
set -e

# Layer 1: PG
PG_COUNT=$(PGPASSWORD="$PGPASSWORD" psql -h 127.0.0.1 -U arifos_admin -d vault999 -tA \
  -c "SELECT count(*) FROM observability.observations;" 2>/dev/null)
echo "Layer 1 (Local backend → PG): $PG_COUNT observations"

# Layer 2: NATS
NATS_MSGS=$(nats stream info kabarkan-ingest -j 2>/dev/null | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(d.get('state',{}).get('messages',0))")
echo "Layer 2 (NATS stream): $NATS_MSGS messages"

# Layer 3: Worker
WORKER_ACTIVE=$(systemctl is-active kabarkan-worker 2>/dev/null || echo "inactive")
WORKER_FAILURES=$(journalctl -u kabarkan-worker --no-pager 2>/dev/null | grep -c "PG write failed" || echo "0")
echo "Layer 3 (Standalone worker): $WORKER_ACTIVE, $WORKER_FAILURES PG failures"

# Cross-check
if [ "$PG_COUNT" -gt 0 ] && [ "$WORKER_FAILURES" -gt 0 ]; then
  echo "WARNING: PG has data but standalone worker is failing — in-process path masks broken worker"
fi
```
