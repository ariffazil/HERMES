---
name: dependency-sovereignty
description: "Assess external SaaS/dependency against arifOS federation infrastructure and determine whether to self-host, forge in-house, or pay. Structured 4-phase evaluation with infrastructure mapping, gap analysis, and 3-option recommendation."
tags: [assessment, evaluation, infrastructure, build-vs-buy, self-host, external-dependency, federation]
triggers:
  - "can we build this ourselves?"
  - "self-host this"
  - "replace this service"
  - "hit [tool/service] limit"
  - "free tier exhausted"
  - "evaluate this dependency"
  - "X usage threshold reached"
  - "should we pay for X"
  - "can we replace X with our own"
  - "this service reached its limit"
  - "LangGraph"
  - "orchestration framework"
  - "replace [tool] with our own"
  - "evaluate dependency"
---

# Dependency Sovereignty Assessment

Pattern for evaluating an external SaaS or dependency and determining whether to self-host the open-source version, forge an in-house replacement using federation infrastructure, or pay the vendor.

Covers Langfuse, LangGraph, OpenRouter, Tavily, and any future external service that hits a cost/limit/sovereignty boundary.

## Workflow

### Phase 1: Research the External Service

Gather these dimensions before any analysis:

| Dimension | Source | What to extract |
|-----------|--------|-----------------|
| **Core features** | Official docs, GitHub README | List every capability: tracing, eval, prompt mgmt, dashboard, SDKs |
| **Architecture** | Self-hosting docs, docker-compose | Storage (Postgres/ClickHouse/S3), components (API server, worker, queue), networking |
| **License** | GitHub LICENSE file | MIT/Apache/AGPL/BSL/Proprietary — determines if self-hosting is even an option |
| **API surface** | API docs, OpenAPI spec | Endpoints, SDKs (Python/JS), OpenTelemetry compatibility, auth model |
| **Pricing** | Pricing page, email alerts | Free tier limits, paid tier costs, per-event billing, grace periods |
| **Self-hosting** | Self-hosting docs | Docker Compose, Helm chart, VM setup, dependencies, resource requirements |
| **Data model** | Schema docs, data export | Trace/span/observation/session models, how scoring works |

**Tooling:**
- `mcp__hound__mcp_smart_crawl` — crawl official docs site at depth 1-2
- `mcp__hound__mcp_smart_fetch` — fetch GitHub README, self-hosting page, pricing page
- `web_search` — find architecture overviews, blog posts, comparisons
- `curl` — probe API endpoints if documented

### Phase 2: Federation Infrastructure Mapping

Map every feature of the external service against what the arifOS federation already has.

**Canonical federation infrastructure:**

| Resource | Available | Notes |
|----------|-----------|-------|
| PostgreSQL | ✅ `postgres:16-alpine` :5432 | Transactional workloads, metadata |
| Redis | ✅ `redis:7-alpine` :6379 | Caching, queueing, session state |
| MinIO (S3) | ✅ `minio/minio` :9000-9001 | Blob/object storage for events, traces, large payloads |
| Qdrant | ✅ `qdrant/qdrant:latest` :6333-6334 | Vector search |
| NATS | ✅ If deployed | Event streaming, governance events |
| Supabase | ✅ (connected) | Structured record storage, OLAP-like queries at moderate scale |
| VAULT999 | ✅ `/root/VAULT999` | Immutable append-only hash chain — canonical truth store |
| Prometheus | ✅ Via arifOS Telemetry | Metrics registry (tool calls, floor breaches, latency) |
| AAA Cockpit | ✅ React 19 + Vite | Build custom dashboards and trace visualisers |
| Postgres with pgvector | ✅ `pgvector/pgvector:pg15` :5433 | A-FORGE database, vector operations |
| FalkorDB | ✅ `falkordb` :6380 | Graph database (Graphiti) |
| LLM inference | ✅ Ollama (local), OpenRouter, DeepSeek, etc. | LLM-as-judge capability via F8 GENIUS |

**Mapping template:**

```
| External feature | Our equivalent | Gap? | Estimate |
|------------------|----------------|------|----------|
| Trace ingestion  | Telemetry.record_tool_call() | Routes to Langfuse Cloud — need to redirect to local | 1 day |
| Trace storage    | VAULT999 + Supabase | Need ingestion endpoint + query layer | 2-3 days |
| ...              | ...            | ...  | ...     |
```

### Phase 3: Gap Analysis

Identify what must be built, what can be reused, and what already exists but needs reconfiguration:

**Categories:**
- ✅ **REUSE** — exists, works, just need to change a config/endpoint
- 🟡 **ADAPT** — exists but needs modification (e.g., add a new mode, extend schema)
- 🔴 **BUILD** — does not exist, must be created from scratch
- ⬜ **SKIP** — feature not needed for our use case

### Phase 4: Three-Option Recommendation

Always present exactly three options with pros/cons/effort:

| | Option 1: Self-host OSS | Option 2: Forge in-house | Option 3: Pay |
|---|---|---|---|
| **Effort** | Hours to half-day | Days to weeks | $/mo recurring |
| **Sovereignty** | Full (data on infra) | Full | None (vendor lock-in) |
| **SDK compat** | Drop-in (same vendor SDK) | Break compat — need shim | Same SDK |
| **Maintenance** | Vendor releases + infra | We own it forever | Zero |
| **Polish** | Vendor quality | Rough at v1, improves | Vendor quality |

**Decision framework (in priority order):**

1. **Can we self-host OSS?** If the tool is open-source (MIT/Apache/AGPL) and our infra can run it, that's the fastest path to sovereignty. Do this first.
2. **Should we forge in-house?** If self-hosting is impossible (proprietary, too heavy, incompatible license), map what we already have. If existing infra covers ≥60% of the features and the remaining gaps are well-understood, forging is viable.
3. **Do we pay?** Only when the cost of building exceeds the value, or the external service has unique capabilities we can't replicate (e.g., exclusive data feeds, regulatory compliance).

### Phase 5: Transition from Self-Host to In-House Forge

When the assessment recommends both self-host (P0 insurance) and forge in-house (P1-P3), use this transition pattern to migrate safely:

**The Three-Plane Architecture:**

```
Plane 1 (Kernel):  Ingestion endpoint — lives in the kernel, zero hops
Plane 2 (Worker):  Processing — standalone NATS consumer, never blocks kernel
Plane 3 (UI):      Visualization — AAA cockpit dashboard
```

**Dual-Write Migration Pattern:**

1. **Phase 0 — Self-host OSS.** Deploy the OSS version using existing infra. Zero code changes. Secures ingestion immediately.
2. **Phase 1 — Kernel shim.** Introduce a backend selector env var (langfuse|arifos|dual). Build a local backend that writes to Postgres alongside the OSS path. Dual mode writes to both — safe for migration.
3. **Phase 2 — Streaming + Worker.** Wire a NATS JetStream producer into the kernel. Build a standalone worker (NATS pull consumer, Postgres batch write, MinIO archive).
4. **Phase 3 — UI.** Build dashboards in AAA cockpit. Cut over only when the UI provides equivalent visibility.
5. **Phase 4 — Cutover.** Flip env var to arifos, remove OSS SDK dependency, decommission self-host.

**Key invariants during transition:**
- Never block the kernel on observability (fire-and-forget writes)
- Never lose telemetry (S3 buffer + replay from NATS)
- Postgres schema must support full data model before cutover (trace_id, span_id, parent_span_id, session_id, actor_id, tool_name, verdict_class, cost, latency, metadata, vault_receipt linkage)
- The OSS tool and in-house backend must share same API keys/credentials during dual-write
- Postgres passwords with special characters (! @ #) in connection URLs cause silent psycopg2 failures — always test URL connections before cutover, keep explicit user/password/host/port fallback vars

**Critical: Telemetry hook placement.** The kernel may have multiple dispatch layers (e.g. ATLAS333 wrapper bypassing ConstitutionalKernel). Telemetry must intercept at the LOWEST common dispatch point — not just at ConstitutionalKernel.dispatch(). Verify by checking ALL tool dispatch paths:

```bash
grep -rn 'trace_tool_call\|record_tool_call' /opt/arifos/arifosmcp/runtime/ --include='*.py'
```

## Pitfalls

- **Don't forget the SDK layer**: Self-hosting the backend is easy. Making SDKs point to localhost can be harder depending on how deeply the SDK is integrated. Check all `import` and `from` statements in the codebase.
- **ClickHouse is hungry**: It needs ~2GB RAM minimum and ~10GB disk. Not all VPS nodes can spare this. Check actual disk/RAM before choosing self-host. Use `free -h` and `df -h /` to measure.
- **Free tier resets**: Note the reset date. Grace periods are temporary — if you don't act before the next billing cycle, ingestion drops.
- **OpenTelemetry protocol**: If the tool speaks OTLP, we may be able to swap the backend without changing SDKs at all. Check if the tool supports OTel exporter configuration.
- **Auth model**: Self-hosted instances often default to no-auth or simple API keys. If the tool will be accessible from agents/VPS, secure it with at minimum a Bearer token.
- **License scope**: Some open-source tools have core (MIT) but enterprise features (source-available/paid). Know what you lose by self-hosting vs paying.
- **Resource cost of forge**: Don't underestimate the UI. Backend ingestion is typically 30% of the work; the visual trace tree viewer and dashboard are the other 70%. If the existing AAA cockpit already has the interaction model (e.g., a timeline or table view), reuse it.
- **Probe the infrastructure before mapping**: Don't assume what's running. Always verify with live probes:
  ```bash
  # Check port listeners
  ss -tlnp | grep -E '<port1>|<port2>|...'

  # Check if a service is actually authenticated
  docker exec <container> <cmd>   # e.g. docker exec redis redis-cli CONFIG GET requirepass

  # Check if a service has the data you expect
  docker exec postgres psql -U postgres -d <db> -c "\dt <table>"

  # Check the actual container state
  docker ps --format '{{.Names}} {{.Image}} {{.Ports}}'

  # Check if systemd service is actually watching (vs. orphaned process)
  systemctl status <service>  # may show "masked" while port is still listening from a manually-started process
  ```
  Example from this session: NATS systemd unit was **masked** and dead, but `ps aux` revealed the process was started directly with `/usr/sbin/nats-server -js -sd <dir> -a 127.0.0.1 -p 4222 -m 8222`. A `ss -tlnp | grep 4222` showed the port was alive. Never trust `systemctl status` alone.
- **Parallel telemetry paths cause confusion**: A system may emit telemetry to multiple destinations simultaneously (Langfuse + Supabase L4 + Prometheus + local SQLite for APEX metrics). When replacing one path, know which is the **canonical observability store** and which are secondary computation stores. For arifOS: Langfuse is the trace store, Supabase L4 is the receipt record, APEX SQLite is the metric computation store, Prometheus is the live dashboard source. These are not interchangeable.
- **Port conflicts with existing infra**: Langfuse Web defaults to port 3000. Check first: `ss -tlnp | grep 3000`. Grafana may already be there. Use port 4000 for Langfuse Web instead.
- **Existing Redis may have no auth**: Run `docker exec redis redis-cli CONFIG GET requirepass`. If empty, you must either add auth (breaking existing consumers) or run a second Redis container for the self-hosted tool (simpler, more containers).
- **Multiple SDK locations**: The SDK may be in the systemd venv but NOT in the uv dev environment. Check both:
  ```bash
  # Runtime venv
  /opt/arifos/venv/bin/python -c "import <pkg>; print(<pkg>.__version__)"
  
  # Dev venv
  cd /root/arifOS && uv run python -c "import <pkg>; print(<pkg>.__version__)"
  ```
- **Check memory headroom before deploying ClickHouse**: `free -h` shows available RAM. ClickHouse minimum is 2GB. If available is under 3GB, the VPS will swap and degrade. Consider lighter alternatives (Supabase queries at moderate scale, materialised views in Postgres).
- **Telemetry hooks must intercept at the lowest dispatch layer**: The kernel may route tool calls through multiple pathways (e.g. ATLAS333 wrapper → tool handlers, bypassing ConstitutionalKernel.dispatch()). If hooks are only in the kernel dispatch path, tool calls via other paths are invisible. Always verify by checking ALL tool dispatch paths after wiring telemetry.

## References

- `references/langfuse-analysis-2026-07-24.md` — Full Langfuse assessment: features, architecture, federation mapping, gap analysis, and 3-option recommendation. Concrete worked example of this methodology.
- `references/langfuse-selfhost-recipe.md` — Docker Compose recipe for self-hosting Langfuse v3 on arifOS infra: ClickHouse, MinIO, Postgres, Redis config, headless init, port mapping, and known pitfalls.
