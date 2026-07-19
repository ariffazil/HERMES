---
name: hermes-prime-federation-map
description: Consolidated federation map — topology, A2A protocol, safety wiring, observability, and AAA control plane. Single-source truth for all federation organs, ports, protocols, invariants, and instrumentation.
license: Proprietary
tags: [federation, topology, a2a, mcp, observability, safety-wiring, aaa, organs, ports, governance]
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
version: 1.0.0
forged: 2026-07-08
status: ACTIVE
floor_scope: [F1, F2, F4, F7, F8, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "federation map"
  - "topology"
  - "dependency graph"
  - "hermes-prime-federation-map"
  - "A2A"
  - "safety wiring"
  - "observability"
---

# Hermes-Prime Federation Map

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> Consolidated from 5 federation fragments: a2a-federation-builder, aaa-cockpit, federation-observability, federation-safety-wiring, federation-topology-map.

## §PROVENANCE

| Fragment | Version | Unique Contribution |
|----------|---------|---------------------|
| `a2a-federation-builder` | 1.1.0-2026.06.27 | A2A protocol, Agent Cards, 10 invariants, AGENT_REGISTRY.json, HOLD/SEAL workflow, task lifecycle |
| `aaa-cockpit` | 1.0.0-2026.06.25 | AAA control-plane boundaries, approval ticket format, anti-patterns |
| `federation-observability` | 1.1.0-2026.06.27 | OpenTelemetry + Prometheus + Grafana (LGTM), span attributes, metrics |
| `federation-safety-wiring` | 1.0.0-2026.07.03 | 10 error classes, 6 memory classes, 4 epistemic layers, tool handler wiring |
| `federation-topology-map` | 1.0.0-2026.07.03 | Dependency graph, critical-path order, live probe script |

**Forged:** 2026-07-08 | **Consolidation:** Hermes autonomous subagent | **Predecessors absorbed:** none (both targets were empty)

---

## 1. Federation Topology — The Complete Map

```
                    ┌──────────────┐
                    │   ARIF (F13) │
                    │   Human DM   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────▼───┐  ┌────▼─────┐  ┌──▼──────────┐
     │  @ASI_bot  │  │ @AGI_bot │  │ @arifOS_bot │
     │  Hermes    │  │ OpenClaw │  │ opencode-bot│
     │  :gateway  │  │ :18789   │  │ :4096       │
     └─────┬──────┘  └────┬─────┘  └──────┬──────┘
           │              │               │
     ┌─────▼──────────────▼───────────────▼──────┐
     │           FEDERATION ORGANS                │
     │                                            │
     │  arifOS  :8088   — governance, judge, vault│
     │  A-FORGE :7072   — execution, 72+ tools    │
     │  AAA     :3001   — control plane, A2A mesh │
     │  GEOX    :8081   — earth intelligence      │
     │  WEALTH  :18082  — capital intelligence    │
     │  WELL    :18083  — human readiness         │
     └────────────────────────────────────────────┘
```

### Organ Registry

| Organ | Port | Role | Authority | Blast Radius | MCP Surface |
|-------|------|------|-----------|-------------|-------------|
| **arifOS** | 8088 | Constitutional kernel | governance | CRITICAL | `:8088/mcp` |
| **AAA** | 3001 | Control plane | hold_seal | HIGH | A2A gateway |
| **A-FORGE** | 7071/7072 | Execution engine | execution | HIGH | `:7072/mcp` |
| **GEOX** | 8081 | Earth intelligence | domain_intelligence | MEDIUM | `:8081/mcp/` |
| **WEALTH** | 18082 | Capital intelligence | domain_intelligence | MEDIUM | `:18082/mcp` |
| **WELL** | 18083 | Human readiness auditor | audit | LOW | `:18083/mcp` |
| **OpenClaw** | 18789 | Agentic coder (26 tools + cron) | agentic | MEDIUM | `:18789/mcp` |

### Critical-Path Dependency Order

```
1. arifOS :8088        ← GOVERNANCE (everything depends on this)
2. A-FORGE :7072       ← EXECUTION (most tools route through here)
3. AAA :3001           ← CONTROL PLANE (federation registry, A2A)
4. OpenClaw :18789     ← AGENTIC CODER
5. GEOX :8081          ← EVIDENCE (domain)
6. WEALTH :18082       ← CAPITAL (domain)
7. WELL :18083         ← VITALITY (domain)
```

**If arifOS is down:** Nothing works. Stop. Read-only mode.
**If A-FORGE is down:** Can't execute. Can still observe, plan, judge.
**If AAA is down:** Federation registry empty. Organs can't register. Can still use MCP directly.

---

## 2. The A2A Protocol — Civic Layer Between Agents

> **MCP = roads (agent → tool). A2A = diplomacy (agent → agent).**

### Three Surfaces Every Site Must Expose

1. **Human Surface** — HTML, UI, content
2. **Agent Surface** — `llms.txt`, `agents.md`, WebMCP tools
3. **Inter-Agent Surface (A2A)** — Agent Card + JSON-RPC endpoint

### A2A Is Three Files Per Site

1. `/.well-known/agent.json` — Agent Card (identity + capabilities, NOT implementation)
2. `/a2a` endpoint — JSON-RPC 2.0 surface (Bearer auth, HOLD gate)
3. `AGENT_REGISTRY.json` — Federation directory published from canonical repo

### Trust Hierarchy (Never Violate)

```
Human (Arif) > arifOS > AAA > A-FORGE > Specialists
```

### The 10 Canonical A2A Invariants

| ID | Invariant |
|----|-----------|
| **I-1** | No agent calls another without valid Bearer token |
| **I-2** | No irreversible action without valid `seal_id` from AAA |
| **I-3** | A-FORGE MUST reject all tasks lacking `seal_id` |
| **I-4** | All inter-agent task completions MUST emit a Vault999 receipt |
| **I-5** | Network position grants zero authority — trust is explicit |
| **I-6** | WELL is read-only — never given execution authority |
| **I-7** | Canon is append-only — never overwrite existing canon |
| **I-8** | arifOS governs — never executes user code |
| **I-9** | Every HOLD must surface to human at aaa.arif-fazil.com within 60s |
| **I-10** | Agents must write session state before compaction |

### Task Lifecycle

```
SUBMITTED → WORKING → COMPLETED
                    → FAILED → (optional rollback)
                    → CANCELLED
           → INPUT_NEEDED (HOLD awaiting human)
```

Rules: poll `tasks/get` at 10s intervals on INPUT_NEEDED, never timeout before 300s, CANCELLED must write Vault999 receipt.

### HOLD/SEAL Workflow

```
Agent A → PERMIT (low blast, reversible) → proceed
Agent A → HOLD (high blast OR irreversible) → AAA hold.request → Human reviews → SEAL (forge.delegate → A-FORGE → Vault999) OR REJECT
```

### A2A vs MCP — Protocol Boundary

| Interaction | Protocol |
|-------------|----------|
| arifOS calling a tool | **MCP** |
| AAA delegating to A-FORGE | **A2A** |
| GEOX publishing dashboard data | **MCP** (WebMCP) |
| WELL auditing AAA decision log | **A2A** |
| External agent calling federation | **A2A** via Agent Card |
| Human seeing HOLD panel | **MCP Apps** (SEP-1865) |

---

## 3. AAA Control Plane — Cockpit Boundaries

### What AAA Is NOT

- ❌ NOT a governance layer — arifOS judges
- ❌ NOT an execution layer — A-FORGE executes
- ❌ NOT a domain computer — GEOX/WEALTH/WELL compute
- ❌ NOT a memory organ — VAULT999 remembers

AAA **routes** and **displays**. It shows state, surfaces tickets, routes A2A.

### Approval Ticket Format (888_HOLD)

```json
{
  "ticket_id": "888_xxx",
  "type": "IRREVERSIBLE_ACTION",
  "blast_radius": "HIGH",
  "reversibility": "NONE",
  "status": "PENDING_APPROVAL",
  "human_action_required": "Approve or Deny"
}
```

### AAA Anti-Patterns

- ❌ Routing governance decisions through AAA
- ❌ Using AAA as judgment authority
- ❌ Executing through AAA instead of A-FORGE
- ❌ Storing durable memory in AAA (use VAULT999)

---

## 4. Safety Wiring — Every MCP Tool Handler

### The 9 Discoveries Every Tool Must Wire

1. **Surface truth** — schema fingerprinting
2. **Operator truth** — WELL gate
3. **Failure truth** — structured error envelopes
4. **Chain truth** — progress/cancel
5. **Route truth** — file type routing
6. **Execution truth** — authority ladder
7. **Remote truth** — git preflight
8. **Memory truth** — freshness classification
9. **Epistemic truth** — evidence quality signals

### On Success (Python)

```python
return {
    **result,
    "_memory": {
        "class": "LIVE_PROBE",
        "last_verified": iso_timestamp,
        "is_fresh": True,
        "source": "tool_name",
    },
    "_epistemic": {
        "evidence_layer": "OBS",
        "confidence": 0.85,
        "source": "tool_name",
        "reversible": True,
        "authority_claim": "EVIDENCE",
    },
}
```

### 10 Error Classes

| Class | Recoverability | When |
|-------|---------------|------|
| BAD_INPUT_SHAPE | AGENT_CAN_RETRY | Missing required fields |
| BAD_INPUT_VALUE | AGENT_CAN_RETRY | Valid structure, wrong values |
| DOWNSTREAM_FAILURE | AGENT_CAN_ROUTE | External API/DB failed |
| RESOURCE_EXHAUSTED | RETRY_SAME_LATER | Timeout, rate limit, OOM |
| INTERNAL_ERROR | ESCALATE_TO_888_HOLD | Server bug |
| AUTHORITY_BLOCK | ESCALATE_TO_888_HOLD | No lease/permission |
| FLOOR_BLOCK | ESCALATE_TO_888_HOLD | F1-F13 violation |
| TOOL_SURFACE_DRIFT | ESCALATE_TO_888_HOLD | Schema changed |

### 6 Memory Classes

| Class | TTL |
|-------|-----|
| LIVE_PROBE | 5 min |
| SESSION_STATE | Session |
| CACHED_MEMORY | Configurable |
| INFERRED | N/A |
| SEALED_RECEIPT | Infinite |
| STALE | Expired |

### 4 Epistemic Layers

| Layer | Meaning | Max Confidence |
|-------|---------|---------------|
| OBS | Directly observed | 0.90 |
| DER | Computed/derived | 0.90 |
| INT | Interpreted | 0.90 |
| SPEC | Speculative | 0.30 |

---

## 5. Observability — LGTM Stack (Open-Source Only)

### Architecture

```
Organs → OpenTelemetry Collector → Prometheus (metrics) + Loki (logs) + Tempo/Jaeger (traces)
                                 → Grafana (unified dashboards)
```

**Zero SaaS** — no Logfire, no Datadog, no New Relic.

### Federation Span Attributes (every span MUST carry)

- `federation.organ` (arifos | aaa | aforge | geox | wealth | well | vault999)
- `federation.session_id`
- `federation.actor_id`
- `federation.seal_verdict_id` (if sealed)
- `federation.receipt_id` (if vault write)

### Custom Federation Metrics

```
federation.tool.invocations  — counter per organ
federation.tool.latency_ms   — histogram per organ
federation.seal.requests     — arif_seal calls
federation.hold.triggers     — 888_HOLD escalations
federation.a2a.tasks         — inter-agent delegations
```

### Prometheus Scrape Targets

```yaml
- job_name: 'arifos'    → localhost:8088
- job_name: 'aforge'    → localhost:7071
- job_name: 'wealth'    → localhost:18082
- job_name: 'well'      → localhost:18083
- job_name: 'geox'      → localhost:8081
```

### Instrumentation

- **Python** (arifOS, GEOX, WEALTH, WELL): `opentelemetry-api` + `opentelemetry-sdk` + `structlog`
- **TypeScript** (A-FORGE, AAA): `@opentelemetry/sdk-node` + `@opentelemetry/exporter-prometheus` + `prom-client`

---

## 6. Live Probe — Session Init Script

Run at session start or before any "fix X" task. From `federation-topology-map`:

```bash
# Organ health
for svc in "arifos:8088" "aforge:7071" "aforge-mcp:7072" "geox:8081" "wealth:18082" "well:18083" "aaa:3001" "openclaw:18789"; do
  name="${svc%%:*}"; port="${svc##*:}"
  status=$(curl -sf "http://localhost:$port/health" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "DOWN")
  printf "  %-15s :%-5s %s\n" "$name" "$port" "$status"
done
```

### Entropy Reduction

Without this skill: 3–5 reactive discovery steps per fix task.
With this skill: 1 upfront probe + targeted fix.
Estimated ΔS: −40% wasted computation per session.

---

## 7. Quick Reference — Key Ports & Services

| Service | Port | Protocol | Health Check |
|---------|------|----------|-------------|
| arifOS | 8088 | MCP + REST | `curl :8088/health` |
| A-FORGE API | 7071 | REST | `curl :7071/health` |
| A-FORGE MCP | 7072 | MCP | `curl :7072/mcp` |
| AAA | 3001 | A2A + REST | `curl :3001/health` |
| GEOX | 8081 | MCP | `curl :8081/health` |
| WEALTH | 18082 | MCP | `curl :18082/health` |
| WELL | 18083 | MCP | `curl :18083/health` |
| OpenClaw | 18789 | MCP | `curl :18789/health` |

---

*DITEMPA BUKAN DIBERI — Forged from 5 federation fragments, 2026-07-08.*
*Consolidation subagent: Hermes autonomous delegation | Sources absorbed: a2a-federation-builder, aaa-cockpit, federation-observability, federation-safety-wiring, federation-topology-map*
