# Langfuse Assessment — 2026-07-24

**Context:** arifOS hit 50,381/50,000 Langfuse Cloud free tier events. Ingestion suspension imminent unless action taken. Grace period to July 30 reset.

## What Langfuse Is

Open-source (MIT) LLM observability platform — tracing, prompt management, evals, dashboards, datasets, playground. YC W23, now part of ClickHouse.

### Core features

| Feature | Description |
|---------|-------------|
| Tracing | Span-tree per LLM call with prompt/response/tokens/latency/cost |
| Sessions | Multi-turn grouping of traces |
| Prompt Mgmt | Version-controlled prompts with labels (prod/staging), client-side cached |
| Evals | LLM-as-judge, code evaluators, user feedback, manual labeling |
| Datasets | Test sets + experiments for benchmarking |
| Dashboard | Cost/latency/quality metrics, per-user breakdown |
| Playground | Interactive prompt testing in browser |
| MCP Server | Agent interface via Model Context Protocol |
| API | REST + Python/JS SDKs + OpenTelemetry native |

### Architecture

```
SDK -> Langfuse Web -> S3 (buffer) -> Queue (Redis) -> Langfuse Worker -> ClickHouse (OLAP)
                                                                             + PostgreSQL (metadata)
                                                                             + Redis (cache/queue)
                                                                             + S3 (blob)
```

**Storage:** ClickHouse (traces, observations, scores), PostgreSQL (metadata), Redis (queue+cache), S3 (event buffer + multimodal)

**Low-scale self-host:** Docker Compose with all 4 storage + 2 app containers. Needs ~2GB RAM, ~10GB disk.

## Current arifOS Integration (Deep)

The Langfuse SDK is **woven into the kernel** — not a surface integration:

| File | Role |
|------|------|
| `arifosmcp/runtime/telemetry.py` | Singleton `Telemetry` class. Wraps every `arif_*` tool call as a Langfuse span via `start_as_current_observation`. Records verdict, latency, input/output hashes (PII-redacted), session/actor IDs. Also has Prometheus counters/histograms/gauges. |
| `arifosmcp/memory_engine.py` | `LangfuseTrace` / `LangfuseSpan` async tracer classes. `get_langfuse_tracer()` singleton. Marked as "NOT deprecated" — canonical async tracer. |
| `arifosmcp/runtime/rest_routes.py` | Probes Langfuse health in `/health` endpoint. Feeds `langfuse_tracing` field into observatory/snapshot data. |

**Env vars (from vault.env):**
```
LANGFUSE_BASE_URL=https://jp.cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=pk-lf-ff07b5de-3650-4c9a-82e7-70bf8661ff89
LANGFUSE_SECRET_KEY=***
LANGFUSE_POSTGRES_PASSWORD=***
```

**Observatory status (pre-limit):** `"langfuse_traces": "ACTIVE"` — active traces flowing to Japan region cloud.

## Federation Infrastructure Mapping

| Langfuse feature | Existing federation asset | Assessment |
|-----------------|--------------------------|------------|
| Trace ingestion | `Telemetry.record_tool_call()` in `telemetry.py` — already captures all tool calls with span metadata | ✅ REUSE — just redirect endpoint |
| Trace storage (OLAP queries) | Supabase (already connected) + VAULT999 (immutable chain) | 🟡 ADAPT — Supabase can serve OLAP at 50K events/mo scale; VAULT999 for immutable chain |
| Prompt management | Git-based configs, arifOS stored prompts | 🟡 ADAPT — prompt registry in Supabase with version labels |
| LLM-as-judge | F8 GENIUS + `arif_judge` — constitutional evaluation | ✅ REUSE — already more disciplined than Langfuse evals |
| Dashboard/UI | AAA Cockpit (React 19 + Vite) | 🔴 BUILD — trace tree viewer + cost/latency dashboard |
| SDK | `telemetry.py` wraps Langfuse SDK. Change endpoint OR write shim | 🟡 ADAPT — one-file change in Telemetry class |
| Cost tracking | All provider/model pricing known via TokenRouter | ✅ REUSE — compute token cost from model + usage |
| Event queue | NATS (if active) or Redis streams | ✅ REUSE |
| Blob storage | MinIO :9000 | ✅ REUSE |
| Cache | Redis :6379 | ✅ REUSE |

## Three Options

### Option 1: Self-host Langfuse (hours)

Add ClickHouse + Langfuse Web + Langfuse Worker to Docker Compose. Point env vars to local MinIO + Postgres + Redis.

**Pros:** Drop-in SDK compat (zero code changes), unlimited events, data sovereignty, $0
**Cons:** ClickHouse operational overhead (2GB RAM/10GB disk), maintain upgrades, EE features need license key
**Effort:** 1 hour setup, ~$0/mo infra overhead (already have RAM allocated)

### Option 2: Forge own in-house (weeks)

Redirect `Telemetry.record_tool_call()` to a local ingestion endpoint on arifOS (:8088). Store traces in Supabase (OLAP at our scale) + VAULT999 (immutable). Build trace viewer in AAA cockpit.

**Pros:** Full sovereignty, zero vendor dependency, integrates with F1-F13 governance, $0 forever
**Cons:** ~5 days v1 (ingestion + trace viewer), ~2 more weeks for full feature set (prompts, evals, playground)
**Effort:** 3-5 days for working v1

### Option 3: Pay $29/mo Core tier

Upgrade Langfuse Cloud to Core. Unlimited users, 90-day retention, unlimited evals.

**Pros:** Zero effort, everything keeps working, support channel
**Cons:** $29/mo recurring, data on Japan cloud, SLA dependency
**Effort:** 5 minutes credit card

## Recommendation (given to Arif)

**Short term (this week):** Self-host Langfuse. Fastest path to sovereignty — 1 hour, no code changes, already have all dependencies except ClickHouse. Data stays on our infra.

**Medium term (next 2 months):** Forge own in-house. The foundation is 40% done (VAULT999 for immutable traces, Telemetry class for instrumentation, AAA for UI, NATS for event streaming). The trace viewer + dashboard is the main delta. Redirect Langfuse calls to local ingestion endpoint.

## Key URLs

- GitHub: https://github.com/langfuse/langfuse
- Self-hosting: https://langfuse.com/self-hosting
- Docs: https://langfuse.com/docs
- Observability overview: https://langfuse.com/docs/observability/overview
- OpenTelemetry integration: https://langfuse.com/docs/opentelemetry/get-started

## Live Probe Findings (2026-07-24)

Actual infrastructure state discovered during assessment. These are NOT assumptions — they were probed with live commands.

### NATS — Alive but Orphaned

```
Status:      LIVE (port 4222 listening)
Systemd:     MASKED (inactive dead since 2026-07-23)
Process:     Started directly, not via systemd
Version:     nats-server v2.10.27
JetStream:   ✅ Enabled (-js flag)
Data dir:    /root/.local/share/nats
Monitoring:  :8222
Max payload: 1MB
Auth:        None (127.0.0.1 only)

# Live command:
ps aux | grep nats-server
ss -tlnp | grep 4222
curl -s http://127.0.0.1:8222/varz
```

**Implication:** NATS is available as an event queue for telemetry ingestion, but it has NO current subscribers consuming telemetry events. It's a free bus waiting for work.

### Redis — No Authentication

```
Status:      LIVE (:6379, no auth)
requirepass: EMPTY (no password set)

# Live command:
docker exec redis redis-cli CONFIG GET requirepass
```

**Implication:** If self-hosting Langfuse (which expects `REDIS_AUTH`), we need to either set a password on existing Redis (breaking existing consumers that connect without auth) or run a second Redis container for Langfuse.

### Grafana Conflict on Port 3000

```
ss -tlnp | grep 3000  →  grafana on port 3000
```

**Implication:** Langfuse Web defaults to port 3000. Must use port 4000 (or another free port) for Langfuse Web.

### Prometheus Metrics — Already Exposed

```
Available at: http://127.0.0.1:8088/metrics
Contains:     python_gc counters, arifos_tool_calls_total, arifos_floor_breaches_total,
              arifos_tool_latency_seconds, arifos_active_sessions, arifos_ledger_size

# Live command:
curl -s http://127.0.0.1:8088/metrics | head -5
```

### APEX SQLite Metrics — Third Telemetry Path

Separate from Langfuse and Supabase L4, `apex_primitives.py` writes to a SQLite `tool_calls` table for G-score computation:

| Field | Value |
|-------|-------|
| Table | `tool_calls` |
| Columns | `tool_name, actor_id, session_id, timestamp, success, has_evidence, within_lease, dry_run_first, reversible, failure_code, metadata_json` |
| Writer | `apex_primitives.record_tool_call()` |
| Consumer | `compute_apex_from_metrics()` — computes A, P, E, X, Φ, G, C_dark |

```python
# Write path: arifosmcp/runtime/apex_primitives.py:64
conn = _get_db()
conn.execute("""INSERT INTO tool_calls (...) VALUES (?, ...)""", (...))
conn.commit()
```

### Supabase L4 — Fourth Telemetry Path

`kernel.py` has `_record_tool_call_to_supabase()` that fires tool call data to Supabase:

```python
# kernel.py:545 (fire-and-forget, never blocks)
await record_tool_call(
    session_ref=session_id or "anon",
    tool_name=canonical_name,
    organ_code="ARIFOS",
    arguments=arguments,
    risk_tier=risk_tier,
    status=status,
    verdict=verdict,
    floor_triggered=floors_data,
    duration_ms=int(latency_ms) if latency_ms else None,
    actor_ref=actor_id,
    service_ref="arifOS-MCP",
    mcp_method="tools/call",
)
```

### Canonical Telemetry Architecture (Four Paths)

```
kernel.py (every arif_* tool call)
  │
  ├── trace_tool_call() ──→ Telemetry ──→ Langfuse SDK v4.6.1 ──→ jp.cloud.langfuse.com
  │                            (trace/span store — will be replaced)
  │
  ├── _record_tool_call_to_supabase() ──→ Supabase L4
  │                            (structured receipt — canonical record of every tool execution)
  │
  ├── Telemetry Prometheus ──→ :8088/metrics
  │                            (live counters, histograms, gauges — live dashboard source)
  │
  └── apex_primitives.record_tool_call() ──→ local SQLite
                               (APEX G-score computation — A, P, E, X, Φ)
```

### Resource Headroom

```
Memory:  RAM 31G total, 26G used, 5G available  →  ClickHouse OK (needs 2-3G)
Disk:    /dev/sda1 387G, 189G used, 199G free   →  ClickHouse OK (needs ~10G)
```

### Runtime Environment

| Aspect | Detail |
|--------|--------|
| arifOS runs via | systemd (bare-metal) — NOT Docker |
| Service file | `/etc/systemd/system/arifos.service` |
| Working dir | `/opt/arifos/app/` |
| Python venv | `/opt/arifos/venv/` |
| Langfuse SDK | `v4.6.1` in runtime venv |
| Langfuse in dev | **NOT** installed in uv dev venv (`uv run python -c "import langfuse"` fails) |
| Env file | `/root/.secrets/vault.flat.env` (flat format for systemd EnvironmentFile) |
| Vault env | `/root/.secrets/vault.env` (bash format, NOT systemd-compatible) |
| Health check | `curl -s http://127.0.0.1:8088/health` shows `"langfuse_traces": "ACTIVE"` |
| Traced tools | 13 constitutional tools (arif_init, arif_judge, arif_seal, arif_forge, etc.) |
