---
name: kabarkan-observability
description: "Kabarkan — arifOS sovereign observability plane. Langfuse self-host (insurance) + Kabarkan Postgres backend (sovereign). Covers the full lifecycle: kernel telemetry hooks, NATS JetStream pipeline, standalone worker, schema management, VAULT999 seal pattern, and the three-layer dispatch verification technique."
tags: [observability, telemetry, langfuse, kabarkan, tracing, atlass333, kernel, dispatch, jetstream]
triggers:
  - "langfuse limit"
  - "observability down"
  - "kabarkan"
  - "traces not showing"
  - "telemetry not working"
  - "observability pipeline"
  - "tools not tracing"
  - "dispatch not hooked"
  - "observation_id null"
  - "NATS worker failing"
  - "zero traces"
  - "healthy but no data"
  - "white box not working"
  - "backend configured but empty"
---

# Kabarkan — Sovereign Observability Plane

## Current State (2026-07-24 — SOVEREIGN)

**Postgres `vault999.observability.observations`: 240+ rows and growing.**
**NATS `kabarkan-ingest`: 63+ messages, consumer at latest.**
**Worker `kabarkan-worker.service`: active, 0 restarts.**

The pipeline is sovereign and sealed. All three layers are independently verified.

**This skill documents the deployed instance.** For the class-level forge pattern (how to build this from scratch), see `devops/observability-forge`.

### What's LIVE
| Component | State | Details |
|-----------|-------|---------|
| **Kernel telemetry** (`telemetry.py`) | ✅ | `record_tool_call()` creates `ObservationRecord` with auto-generated UUIDs, publishes via `_publish_nats(record)` |
| **NATS JetStream** | ✅ | Stream `kabarkan-ingest`, subjects `kabarkan.ingest.>`, file storage |
| **Standalone worker** | ✅ | `kabarkan-worker.service` consuming + writing to Postgres idempotently |
| **Postgres schema** | ✅ | `observability.observations` in `vault999` database |
| **Systemd drop-ins** | ✅ | 3 confs: `env-fix.conf`, `pg-fix.conf`, `python-path.conf` — explicit libpq vars bypass POSTGRES_URL |
| **Consumer** | ✅ | `kabarkan-worker-fresh` — correct env, ack_floor at latest |
| **ObservationRecord model** | ✅ | Auto-generates `observation_id`, `trace_id`, `span_id` |
| **ATLAS333 dispatch hooks (L1 Airlock)** | ✅ | `ingress_middleware.py:1422` — covers ALL tools including wrap_legacy_call path |
| **ATLAS333 hooks (L2+L3)** | ✅ | `_wrap_handler` + `_wrap_with_canonical_normalization` |
| **Tools traced** | ✅ | All 8 canonical tools trace on first invocation. Zero-trace tool = NOT CALLED, not UNHOOKED |
| **Langfuse** | ❌ QUOTA EXHAUSTED — Kabarkan now canonical | Free tier 50k/month hit 50,381 on 2026-07-24. Ingestion suspended. Kabarkan is primary. Langfuse dead unless upgraded to Core ($29/mo). See `devops/observability-forge` Phase 4 for Langfuse cutover pattern. |

### What WAS broken (resolved)
| Issue | Fix |
|-------|-----|
| Wrong password in `POSTGRES_URL` | Systemd drop-in with explicit `PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD` — bypasses URL entirely |
| `observability/__init__.py` mode 600 (root) → permission denied | `chown arifos + chmod 644` at runtime |
| Worker writing to wrong database | Drop-in `pg-fix.conf` updated to target `vault999` (both DBs have the schema, but worker writes to vault999) |
| Old consumer had stale ack state, old malformed messages | Service restart created fresh consumer `kabarkan-worker-fresh` with correct env vars |
| Kernel running old bytecode (pre-ObservationRecord .pyc) | `systemctl restart arifos` — bytecode refreshed, correct ObservationRecord path used |
| Path A flat-dict NATS publish (no UUID fields, missing `observation_id/trace_id/span_id/timestamps`) | Removed — all NATS publishing routes through single `_publish_nats(record)` using `ObservationRecord.model_dump(mode="json")` |
| `metadata` and `reasons` fields as raw dicts (psycopg2 "can't adapt type 'dict'") | ObservationRecord's `model_dump(mode="json")` converts to JSON types; worker `json.dumps()` for JSONB columns |
| SEQ 62 published as 0-byte test message | Nak'd by worker (invalid JSON), consumer advanced past it |

### Diagnostic: Telemetry Backend Verification

Always verify actual data stores, not just configured endpoints. 2026-07-24 audit found:

| Backend | Configured? | Actual traces | Why |
|---------|-------------|---------------|-----|
| **Langfuse Cloud** (`jp.cloud.langfuse.com`) | ✅ CUT | **50,381 events** (free tier exhausted) | Historical data from before OBSERVABILITY_BACKEND change |
| **Langfuse self-host** (`localhost:4000`) | ✅ Running v3.224.1 | **0 traces** | REST emitter silently failed (`try/except pass`), OTEL_SDK_DISABLED suppressed SDK path |
| **Kabarkan** (PG local) | ✅ OBSERVABILITY_BACKEND=dual | **240+ observations** | Sovereign path — in-process backend writes directly to PG, NATS stream for worker |

**White box != working.** A backend can be configured, running, and responding to health checks while producing zero traces. Langfuse self-host showed `status: OK` at `:4000/api/public/health` but had zero traces because:
- The REST emitter's `httpx.post()` silently fails (line 94 `except Exception: pass`)
- The OTEL SDK path is suppressed by `OTEL_SDK_DISABLED` env var
- No error surfaces anywhere — the `trace_tool_call()` function uses fire-and-forget for all backends

**Rule:** Always verify by checking the actual data store (PG `SELECT count(*)`, Langfuse `GET /api/public/traces`, NATS stream info), not just the backend status endpoint.

### Verification Commands
```bash
# Source secrets
set -a && source /root/.secrets/vault.env && set +a

# Layer 1: In-process backend (Postgres direct)
PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*) FROM observability.observations;"

# Layer 2: NATS stream
nats stream info kabarkan-ingest 2>&1 | grep -E "Messages|Last Message"

# Layer 3: Standalone worker
systemctl is-active kabarkan-worker
journalctl -u kabarkan-worker --no-pager -n 5 | grep -E "WARNING|ERROR"

# Consumer state (non-interactive via nats-py)
python3 -c "
import asyncio
from nats import connect
async def check():
    nc = await connect('nats://127.0.0.1:4222')
    js = nc.jetstream()
    info = await js.consumer_info('kabarkan-ingest', 'kabarkan-worker-fresh')
    print(f'Delivered stream_seq={info.delivered.stream_seq}')
    print(f'Ack floor stream_seq={info.ack_floor.stream_seq}')
    print(f'Pending: {info.num_pending}')
    await nc.close()
asyncio.run(check())
"

# Tools tracked
PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT tool_name, count(*) as cnt FROM observability.observations GROUP BY tool_name ORDER BY cnt DESC;"

# All 3 layers must show green. Layer 1 can have data while Layer 3 fails silently.
```

## Architecture

### Dispatch Flow (all 3 layers wired — SOVEREIGN)
```
Tool call enters kernel via MCP
    │
    ├── Layer 1: ingress_middleware.py (Airlock)
    │   └── trace_tool_call() ← CRITICAL: covers ALL tools including
    │       └── wrap_legacy_call path (session-fail/legacy)
    │
    ├── Layer 2: _wrap_handler (non-canonical tools)
    │   └── trace_tool_call() → ObservationRecord → _publish_nats(record)
    │       └── model_dump(mode="json") → NATS `kabarkan.ingest.span.{trace_id}`
    │
    └── Layer 3: _wrap_with_canonical_normalization (KERNEL_ABI_8)
        └── trace_tool_call() → same ObservationRecord path
```

**Layer 1 (Airlock) was the last gap closed.** Before the sovereign forge (2026-07-24), only Layers 2-3 were wired — tools that bypassed `_wrap_handler` (like `arif_judge`, `arif_forge`, `arif_seal`, `arif_route`, `arif_memory`) went untraced through the Airlock path. Hook at `ingress_middleware.py:1422` closed this. Verified: `arif_judge` now appears in observations (was 0).

The `ObservationRecord` ships 21 fields:

| JSON Key | Source | PG Column |
|----------|--------|-----------|
| `observation_id` | `uuid.uuid4()` | `id` (mapped via worker `payload.get("observation_id")`) |
| `trace_id` | `uuid.uuid4()` | `trace_id` |
| `span_id` | `uuid.uuid4()` | `span_id` |
| `parent_span_id` | `None` | `parent_span_id` |
| `session_id`, `actor_id`, `tool_name`, `organ_id` | From kernel context | Same |
| `verdict_class`, `delta_s`, `reasons`, `next_safe_action` | From governance verdict | Same |
| `uncertainty_tag`, `input_hash`, `output_hash`, `vault_receipt` | Evidence hashes | Same |
| `cost_usd`, `model_name`, `latency_ms` | Cost attribution | Same |
| `start_time`, `end_time` | `datetime.now(timezone.utc)` | Same |
| `metadata` | Extensible dict → `json.dumps()` | `metadata` (jsonb) |
| `created_at` | `datetime.now(timezone.utc)` | Same |

### Three-Layer Pipeline (verify each independently)
```
Layer 1 (in-kernel): Telemetry.record_tool_call() → PostgresBackend.store()
                                                      └→ _publish_nats(record) → NATS
Layer 2 (stream):    NATS JetStream kabarkan-ingest (file storage, 7-day retention)
Layer 3 (worker):    kabarkan-worker.service → pull 10 at a time → PG idempotent UPSERT → MinIO
```

**CRITICAL: Layer 1 (Postgres direct) can work while Layer 3 (worker) silently fails.**
Always verify all three layers independently. The in-process backend writes directly — it does NOT use NATS. Its success proves only that the kernel telemetry shim works, NOT that the standalone pipeline (NATS → worker → PG) is healthy.

## Worker Payload Contract

The standalone worker at `/opt/kabarkan/worker.py` does:
```python
payload.get("observation_id") or payload.get("id")  # maps to PG column `id`
```

Fragile fallback. Always send `observation_id`. The ObservationRecord model defines it as:
```python
observation_id: UUID = Field(default_factory=_new_id)  # uuid.uuid4()
```

When serialized via `model_dump(mode="json")`, it becomes `"observation_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`.

### Common worker failure modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| `null value in column "id"` | NATS message missing `observation_id` | Ensure all publishes use `ObservationRecord` model, not flat dict |
| `can't adapt type 'dict'` | Raw dict hitting JSONB column without `json.dumps()` | Use `ObservationRecord.model_dump(mode="json")` or `json.dumps()` before insert |
| `invalid JSON` | 0-byte or malformed NATS message | Check publishing code for empty payloads; Nak'd messages auto-retry |
| Consumer shows 0 pending but PG has 0 rows | Consumer ack'd without successful write | Check journal for `PG write failed` warnings |
| PG has data but worker log shows no activity | In-process backend (Layer 1) is working — standalone worker (Layer 3) may not be the active writer | Compare observation timestamps against worker journal timestamps |

### 🚨 Pitfall: Stale bytecode — file correct, kernel running old .pyc

**Symptom:** NATS stream has new messages (SEQ advancing) with correct `observation_id` fields, but worker log shows "PG write failed: null value in column 'id'" for those new messages. The code in `telemetry.py` uses `ObservationRecord` correctly, but it's not the code the running kernel loaded.

**Root cause:** The telemetry.py file was fixed (ObservationRecord model, `_publish_nats` path), but the arifOS kernel process started BEFORE the fix and still has the old .pyc bytecode in memory.

**Diagnostic:**
```bash
# Check when the kernel started
systemctl show arifos -p ActiveEnterTimestamp --value

# Check when the telemetry file was last modified
stat -c '%y' /opt/arifos/arifosmcp/runtime/telemetry.py

# If kernel start < file modification, kernel has stale bytecode
```

**Fix:**
```bash
systemctl restart arifos   # bytecode refresh → new .pyc → correct ObservationRecord path
```

**Verify fix:** The consumer should now be consuming NEW messages (SEQ advancing) with successful PG writes. Check:
```bash
PGPASSWORD="$POSTGRES_PASSWORD" psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*) FROM observability.observations;"
```

**The counter-intuitive part:** `grep trace_tool_call` on the runtime file shows the hooks exist. The code IS correct on disk. But the running process doesn't read from disk every call — it loads the module once at startup. A restart is the only fix. This caught the 2026-07-24 audit session: the file was already fixed, the kernel was not restarted, all claims checked out on disk but zero data flowed.

### Consumer State Diagnostic

When the worker says "active" and NATS shows 0 pending, but PG has no new rows:

1. **Check consumer delivery vs ack:**
```python
info = await js.consumer_info('kabarkan-ingest', 'kabarkan-worker-fresh')
# delivered.stream_seq shows what the worker has pulled
# ack_floor.stream_seq shows what the worker has confirmed written
# If delivered >> ack_floor, worker is pulling but failing to write
# If delivered == ack_floor == latest stream seq, worker is current
```

2. **Inspect message payload:**
```python
msg = await js.get_msg('kabarkan-ingest', seq=N)
data = json.loads(msg.data)
print('Has observation_id:', 'observation_id' in data)
print('Has trace_id:', 'trace_id' in data)
print('Keys:', sorted(data.keys()))
```

3. **Check worker journal for silent failures:**
```bash
journalctl -u kabarkan-worker --no-pager -n 50 | grep -E "WARNING|ERROR|Nak|invalid"
```

4. **Cross-reference timestamps:** Compare observation `created_at` values against worker journal timestamps. If observations exist but predate the worker's last restart, they came from the in-process backend (Layer 1), not the worker (Layer 3).

## NATS JetStream Debugging (non-interactive)

When `nats CLI` can't run interactively (no TTY), use `nats-py`:

```python
import asyncio, json
from nats import connect

async def check():
    nc = await connect('nats://127.0.0.1:4222')
    js = nc.jetstream()

    # Stream info
    si = await js.stream_info('kabarkan-ingest')
    print(f'Messages: {si.state.messages}, first={si.state.first_seq}, last={si.state.last_seq}')

    # Get specific messages by SEQ
    msg = await js.get_msg('kabarkan-ingest', seq=63)
    data = json.loads(msg.data)
    print('Has observation_id:', 'observation_id' in data)

    # Consumer info
    info = await js.consumer_info('kabarkan-ingest', 'kabarkan-worker-fresh')
    print(f'Delivered: stream_seq={info.delivered.stream_seq}')
    print(f'Ack floor: stream_seq={info.ack_floor.stream_seq}')
    print(f'Pending:   {info.num_pending}')
    print(f'Waiting:   {info.num_waiting}')

    await nc.close()
asyncio.run(check())
```

## VAULT999 Seal Pattern

To seal a Kabarkan state snapshot to VAULT999:

```bash
# 1. INIT session
curl -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_init","arguments":{"actor_id":"ARIF","mode":"light","intent":"KABARKAN-SEAL"}},"id":"1"}'

# 2. JUDGE the seal (gather evidence first)
# Extract session_token from arif_init response, then:
curl -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_judge","arguments":{"session_token":"<sct>","actor_id":"ARIF","intent":"KABARKAN-SEAL","reversibility_level":"IRREVERSIBLE","blast_radius":"LOW","domain":"arifOS","evidence":[{"content":"PG 230+ observations","type":"observation"},{"content":"NATS 63+ messages, consumer at latest","type":"observation"},{"content":"Worker active, 0 restarts","type":"observation"},{"content":"6/6 organs healthy","type":"observation"}]}},"id":"2"}'

# 3. SEAL (requires F13 SOVEREIGN 888_HOLD — Arif must confirm)
curl -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"arif_seal","arguments":{"session_token":"<sct>","actor_id":"ARIF","mode":"seal","nonce":"kabarkan-seal-YYYYMMDD-NN","payload":"KABARKAN-ATLAS333-HOOK-SEALED: <state summary>","session_id":"<sid>"}},"id":"3"}'
```

**Blockers:**
- `arif_seal` requires `constitutional_chain_id` from prior `arif_judge SEAL` verdict
- `arif_judge` needs proper evidence payload + session context
- F13 SOVEREIGN blocks auto-seal — requires Arif's explicit 888_HOLD
- Must pass `nonce` parameter (4-128 char alphanumeric with optional dash/underscore) — defeats HTTP/SSE retry double-fire
- **`chattr +a` on outcomes.jsonl**: File has append-only attribute. `write_file` (which uses mv temp→target) fails with "Operation not permitted." APPEND works — Python `open(file, 'a')` or shell `>>` succeeds. Never try to overwrite or move the file.

## Reference Files
- `references/path-a-fix.md` — Fixing Path A flat-dict NATS publish
- `references/dispatch-chain-analysis.md` — Analysis of all three dispatch layers
- `references/tool-distribution-verification.md` — How to verify which tools are actually being traced vs missing
- `references/langfuse-zero-trace-forensic.md` — NEW 2026-07-24: The "white box isn't working" diagnosis — debugging a running, healthy backend that produces zero traces. Key lesson from Langfuse self-host (0 traces) vs Kabarkan (240+).
- `templates/forge-prompt.md` — Template for subagent forge prompts

## Known Paths
| Item | Path |
|------|------|
| Telemetry module (source) | `/root/arifOS/arifosmcp/runtime/telemetry.py` |
| Telemetry module (runtime) | `/opt/arifos/arifosmcp/runtime/telemetry.py` |
| Worker source | `/root/arifOS/arifosmcp/runtime/observability/worker.py` |
| Worker run | `/opt/kabarkan/worker.py` |
| Worker systemd unit | `/etc/systemd/system/kabarkan-worker.service` |
| Systemd drop-ins | `/etc/systemd/system/kabarkan-worker.service.d/` |
| Schema DDL | `/root/arifOS/arifosmcp/runtime/observability/schema.sql` |
| Pydantic model | `/opt/arifos/arifosmcp/runtime/observability/models.py` |
| Postgres connection | Systemd drop-in `pg-fix.conf` — explicit PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD |
