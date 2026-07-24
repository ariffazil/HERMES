---
name: observability-forge
description: "Build governed, sovereign observability infrastructure for LLM applications — from kernel-level telemetry shims through NATS streaming pipelines to visualization dashboards. Covers the complete forge cycle: kernel shim, dual-write migration, NATS JetStream producer, ingestion worker, and AAA cockpit UI."
tags: [observability, telemetry, tracing, monitoring, llm-observability, kernel, forge, nats]
triggers:
  - "build observability for"
  - "replace [tool] with our own telemetry"
  - "LLM tracing pipeline"
  - "span tree visualization"
  - "telemetry ingestion"
  - "constitutional observability"
  - "Kabarkan"
  - "how do we see our LLM calls"
  - "trace viewer dashboard"
  - "observability UI in AAA"
---

# Observability Forge — Sovereign LLM Telemetry Pipeline

Pattern for building a governed, kernel-native observability substrate that replaces external SaaS tools (Langfuse, Datadog, etc.) with in-house infrastructure tied directly to constitutional physics.

## Architecture: The Three-Plane Surface

```
Plane 1 — Kernel (arifOS :8088)
  Telemetry.record_tool_call()
    ├── Writes to Postgres (fire-and-forget)
    ├── Publishes to NATS JetStream
    └── (Optional) Mirrors to self-hosted OSS tool via dual-write
                     │
Plane 2 — Worker (Standalone systemd service)
  NATS pull consumer ──batch──→ Postgres (idempotent UPSERT)
                        └──→ MinIO (blob archive, 90+ days)
                     │
Plane 3 — UI (AAA Cockpit)
  Trace list, span tree, latency waterfall, cost charts,
  verdict overlays, cooling ledger overlays, receipt linkage
```

## Phase 1: Kernel Shim

### Observer schema (Postgres)

The canonical observation record stores:

| Field | Type | Purpose |
|-------|------|---------|
| `observation_id` | UUID | Primary key (auto-generated) |
| `trace_id` | UUID | Execution context grouping |
| `span_id` | UUID | Individual span identity |
| `parent_span_id` | UUID? | Span tree parent |
| `session_id` | text | arifOS session context |
| `actor_id` | text | Who initiated the call |
| `tool_name` | text | Which arif_* tool |
| `organ_id` | text? | Routing target organ |
| `verdict_class` | text | SEAL/SABAR/HOLD/VOID/OK |
| `delta_s` | float | Entropy change |
| `reasons` | jsonb | Reasoning chain |
| `input_hash` | text | Redacted input SHA |
| `output_hash` | text | Output SHA |
| `vault_receipt` | text | VAULT999 linkage |
| `cost_usd` | float | Token cost |
| `model_name` | text | LLM model |
| `latency_ms` | float | Duration |
| `metadata` | jsonb | Extensible |

### Backend selector

Use an env var to control the telemetry destination:

```python
_OBSERVABILITY_BACKEND = os.getenv("OBSERVABILITY_BACKEND", "langfuse").lower()
# "langfuse" — external/self-hosted OSS (default, safe)
# "arifos"   — local Postgres only (sovereign)
# "dual"     — both (migration safety)
```

The local backend implements `store(ObservationRecord) -> bool` and `store_batch(list[ObservationRecord]) -> int`. Thread-safe singleton with lazy Postgres connection.

### Dual-write safety

During migration, both backends receive the same data. The kernel never blocks on telemetry — all writes are fire-and-forget with silent failure.

### CRITICAL: Hook placement

Telemetry hooks must intercept at the **lowest common dispatch point** in the kernel. If the kernel has multiple dispatch layers (e.g. ATLAS333 wrapper → tool handlers that bypass ConstitutionalKernel), Telemetry calls placed only in one path will miss significant traffic. Verify:

```bash
grep -rn 'trace_tool_call\|record_tool_call' /opt/arifos/arifosmcp/runtime/ --include='*.py'
```

Every dispatch path must call `Telemetry.record_tool_call()` or `trace_tool_call()`.

### Known dispatch paths to hook:

1. **Canonical handlers** (runtime/tools.py: `_wrap_handler`, `_wrap_with_canonical_normalization`) — covers the primary tool execution path. Hook: `trace_tool_call()` called before/after handler execution, with `start_time` timing for `latency_ms`.

2. **Airlock middleware** (runtime/ingress_middleware.py: `IngressToleranceMiddleware.on_call_tool`) — covers tools dispatched through the FederationEnvelope/Airlock gate. Tools going through this path (`arif_judge`, `arif_forge`, `arif_seal`, `arif_route`, `arif_memory`) all previously showed **0 observations** when only the canonical path was hooked. Hook location: in the `finally` block after `call_next(context)` returns, right after `elapsed_ms` calculation. Available variables: `tool_name`, `envelope_session_id`, `envelope_agent_id`, `elapsed_ms`, `result` (ToolResult), `msg.arguments`. Convert `result` to a dict via `structured_content` before passing to `trace_tool_call()`.

**Verify ALL paths independently:**
```bash
# Check observations per tool — if some are 0, their dispatch path is untraced
PGPASSWORD="..." psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT count(*), tool_name FROM observability.observations GROUP BY tool_name ORDER BY count(*) DESC;"
```

## Phase 2: NATS Streaming + Worker

### NATS JetStream Debugging (non-interactive)

When the `nats` CLI can't run interactively (no TTY), use `nats-py` to inspect streams, messages, and consumer state. See `references/nats-jetstream-debugging.md` for full recipes covering:
- Stream info (message count, first/last seq)
- Get specific messages by SEQ, inspect payload schema
- Consumer state (delivered/ack floor/pending/waiting)
- Diagnosis of pipeline health from NATS perspective

### JetStream stream

```python
# Stream config
name = "kabarkan-ingest"
subjects = ["kabarkan.ingest.>"]
storage = "file"
retention = "limits"
max_age = 604800  # 7 days
max_msg_size = 1048576  # 1MB
max_bytes = 4294967296  # 4GB
```

### NATS producer (kernel side)

Fire-and-forget publish after Postgres write. Lazy-init the NATS connection on first call in a background thread so it never blocks the kernel.

```python
def _publish_nats(record: ObservationRecord) -> None:
    # Lazy-init in daemon thread
    threading.Thread(target=_init_nats, daemon=True).start()
    # Subsequent calls use established connection
    js.publish(f"kabarkan.ingest.span.{record.trace_id}", json_payload)
```

### Worker (standalone service)

- NATS pull consumer with JetStream ordered delivery
- Batch merge (customizable: 100 records or 500ms window)
- Idempotent Postgres INSERT (ON CONFLICT DO NOTHING)
- MinIO archive for observations older than 90 days
- Health endpoint (:18902)
- systemd unit with MemoryMax=512M, Restart=always

## Phase 3: UI (AAA Cockpit)

Not yet built in this session. Pattern:

- React 19 + Vite + Recharts + React Flow
- Trace list with filters (actor_id, tool_name, verdict_class)
- Span tree viewer (React Flow / dagre)
- Latency waterfall (horizontal bar chart)
- Cost breakdown per model per organ
- Verdict class overlay (color-coded: SEAL=green, SABAR=yellow, HOLD=red, VOID=black)
- Cooling ledger overlay
- VAULT999 receipt linkage

## Phase 4: Cutover

Full Langfuse cutover decision pattern documented in `references/langfuse-cutover.md`. Summary:

1. Verify Kabarkan is sovereign first (all 3 layers independently passing)
2. Flip `OBSERVABILITY_BACKEND` from `dual` to `arifos`
3. Remove Langfuse SDK dependency from the kernel
4. Decommission self-hosted Langfuse containers
5. Remove LANGFUSE_* env vars from vault.env
6. Restart arifOS kernel
7. Verify zero Langfuse references in kernel logs

**Pitfall**: Don't cut Langfuse until Kabarkan is fully verified sovereign. The in-process backend (Layer 1) can work while the worker (Layer 3) silently fails — you'd lose observability on kernel restart.

## Pitfalls

- **ATLAS333 bypass**: The kernel's ATLAS333 wrapper may dispatch tool calls without going through ConstitutionalKernel.dispatch(). Telemetry hooks placed only in the constitutional path will miss calls. Trace ALL dispatch paths.
- **Postgres password encoding**: Passwords with `!`, `@`, `#` in connection URLs may cause silent psycopg2 failures. Always test URL connections before cutover. Keep explicit `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` env vars as fallback.
- **NATS producer must be fire-and-forget**: Connecting to NATS on every tool call would add latency. Use a background thread for initial connection, then reuse.
- **Worker restart loop**: `PartOf=arifos.service` causes the worker to restart whenever arifOS restarts. Use independent systemd unit without PartOf.
- **Schema first**: The Postgres schema must exist before the worker starts. Use `_ensure_schema()` in the backend init that creates the table if missing.
- **Always use separate Docker Compose project name**: `docker compose -p langfuse -f langfuse.yml` isolates the project from other compose files in the same directory.
- **Dual NATS publish path — Path A (flat dict) bypasses standalone worker**: `Telemetry.record_tool_call()` has TWO independent NATS publishing paths that both fire simultaneously:
  1. **Path A** (line ~385-399): Publishes a flat dict via `_nats()` — contains `tool_name`, `verdict_class`, `actor_id`, `session_id`, `latency_ms`, `delta_s`, `input_hash`, `output_hash` — but **NO `observation_id`, `trace_id`, or `span_id`**.
  2. **Path B** (line ~408-424): Creates an `ObservationRecord` model, calls `self._local.store(record)`, then calls `_publish_nats(record)` — publishes the full `ObservationRecord.model_dump(mode="json")` with `observation_id`, `trace_id`, `span_id`, etc.
  
  Path A messages have a **different subject format** (`kabarkan.ingest.span.{tool}`) vs Path B (`kabarkan.ingest.span.{trace_id}`) but both route to `kabarkan.ingest.>`. The standalone worker receives both. Path A messages **always fail** on Postgres insert because they lack UUID fields — causing `null value in column "id"` errors.
  
  **Verified fix (Option D)**: Replace Path A entirely. Instead of building a flat dict, create an `ObservationRecord` and call `_publish_nats(record)` — the same function Path B uses. This ensures all NATS messages carry the full schema (observation_id, trace_id, span_id, parent_span_id, etc.). Code change in telemetry.py: replace the flat dict + `_nats()` block with ObservationRecord construction + `_publish_nats(record)` call. After deploying, the standalone worker successfully writes all messages from both paths using the same schema.

- **NATS stream purge required after schema changes**: After fixing Path A to use ObservationRecord schema, old flat-dict messages already in the stream will cause the worker to fail on stale messages. The worker (which naks non-JSON or schema-invalid messages via `json.JSONDecodeError` catch) will retry these indefinitely. Fix: purge the stream after the schema fix is deployed:
  ```bash
  nats stream purge kabarkan-ingest -f
  ```
  Verify: `nats stream info kabarkan-ingest | grep Messages` should show 0 remaining messages. All future observations will use the new schema.

- **`observation_id` vs `id` field mapping breaks standalone worker inserts**: The Pydantic `ObservationRecord` model defines the field as `observation_id: UUID = Field(default_factory=_new_id)`. This serializes as `"observation_id"` in JSON via `model_dump(mode="json")`. But:
  - The **local backend** (`PostgresBackend.store()`) correctly uses `record.observation_id` — this is the working path.
  - The **standalone worker** (`worker.py`) does `payload.get("observation_id") or payload.get("id")` — fragile fallback. If `observation_id` is missing (as in Path A flat-dict payloads), `payload.get("id")` also returns None → null-ID crash.
  - The **Postgres table** schema uses `id UUID PRIMARY KEY` — not `observation_id`. This mismatch between model field name (`observation_id`) and column name (`id`) is intentional in the Pydantic-to-SQL mapping (the backend maps `record.observation_id` → `id` column), but the standalone worker copies the JSON key directly.
  
  **Fix**: Either (a) use `observation_id` as the JSON key consistently and add `id` as an alias in the worker, or (b) add `field_alias="id"` to the Pydantic model so `model_dump(by_alias=True)` serializes as `id`, or (c) use SQLAlchemy ORM column naming that maps `observation_id` → `id` transparently.

- **In-process backend can mask a broken standalone worker pipeline**: The local backend (in-process, runs inside the arifOS kernel) writes directly to Postgres via `PostgresBackend.store()`. When this works, observations appear in the DB — creating the appearance of a fully functional pipeline. But the standalone worker (NATS → Postgres via systemd service) can be **completely failing on every message** while the DB still shows growing observations. The two paths are independent: local writes bypass NATS entirely.
  
  **Verify each layer independently:**
  ```bash
  # Layer 1: In-process backend (Postgres direct)
  PGPASSWORD="..." psql -h 127.0.0.1 -U arifos_admin -d vault999 \
    -c "SELECT count(*) FROM observability.observations;"
  
  # Layer 2: NATS stream (messages flowing?)
  nats stream info kabarkan-ingest | grep Messages
  
  # Layer 3: Standalone worker (is it writing?)
  journalctl -u kabarkan-worker --no-pager | grep -c "PG write failed"
  
  # If Layer 1 has data BUT Layer 3 shows failures, the standalone worker is broken
  # while the in-process path works — don't declare "pipeline working" from PG alone
  ```

  Correct verification of observability health requires **all three layers passing independently**.\n\n- **Stale bytecode — file correct, kernel running old .pyc**: The telemetry.py file may be fixed (ObservationRecord model, correct hooks), but the arifOS kernel process started BEFORE the fix and still has the old .pyc bytecode in memory. `grep trace_tool_call` on the runtime file shows the hooks exist (code IS correct on disk), but the running process doesn't re-read modules from disk every call. `systemctl restart arifos` is the only fix. Always verify: check `ActiveEnterTimestamp` against file modification time.\n\n- **Always use separate Docker Compose project name**: `docker compose -p langfuse -f langfuse.yml` isolates the project from other compose files in the same directory.
