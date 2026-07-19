# A2A Protocol Spec — Deep Dive (2026-07-13)

> **Source:** `a2a-protocol.org/latest/specification/` (v1.0.1, spec v1.2)
> **SDK:** `a2a-sdk` v1.1.0 on PyPI
> **Upstream repo:** `github.com/a2aproject/A2A` (24.7k ★, 587 commits, 11 releases)
> **Python SDK repo:** `github.com/a2aproject/a2a-python` (720 commits, 55 releases)
> **License:** Apache 2.0, Linux Foundation project (contributed by Google)

---

## 1. Protocol Architecture — 3 Layers

```
L1: CANONICAL DATA MODEL (Protocol Buffers — `spec/a2a.proto`)
    Core objects: Task, Message, Part, Artifact, AgentCard, TaskStatus
    All protocol bindings MUST provide functionally equivalent representations.

L2: ABSTRACT OPERATIONS (binding-independent)
    11 core operations: SendMessage, SendStreamingMessage, GetTask, ListTasks,
    CancelTask, SubscribeToTask, Create/Get/List/Delete PushNotificationConfig,
    GetExtendedAgentCard

L3: PROTOCOL BINDINGS (concrete)
    JSON-RPC 2.0 (primary/default), gRPC, HTTP+REST
```

**Key: `a2a.proto` is the single authoritative normative definition.** Not Markdown docs. Not JSON schemas. All SDKs regenerate from proto.

---

## 2. Task State Machine — 9 States

```
TASK_STATE_SUBMITTED     — acknowledged
TASK_STATE_WORKING       — being processed
TASK_STATE_COMPLETED     — success (terminal)
TASK_STATE_FAILED        — error (terminal)
TASK_STATE_CANCELED      — cancelled (terminal)
TASK_STATE_REJECTED      — agent refused (terminal)
TASK_STATE_INPUT_REQUIRED — needs user input (interrupted)
TASK_STATE_AUTH_REQUIRED — needs authentication (interrupted)
TASK_STATE_UNSPECIFIED   — unknown/indeterminate
```

**Execution modes:**
- `returnImmediately: false` (default) — blocking: waits for terminal or interrupted state
- `returnImmediately: true` — non-blocking: returns SUBMITTED/WORKING immediately, client must poll/stream/subscribe

---

## 3. Agent Card — Canonical Schema (v1.0 spec)

**Note: NO `agentId` field in the upstream spec.** The spec uses `name` as the primary identifier. Our `agentId` is a custom arifOS extension.

### Required fields (8):

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable agent name (acts as logical identifier) |
| `description` | string | What the agent does |
| `version` | string | Agent version, e.g. "1.0.0" |
| `capabilities` | object | `{streaming, pushNotifications, extendedAgentCard}` — all booleans |
| `supportedInterfaces` | [{url, protocolBinding, protocolVersion}] | Ordered list, first = preferred |
| `defaultInputModes` | string[] | MIME types accepted |
| `defaultOutputModes` | string[] | MIME types produced |
| `skills` | [{id, name, description, tags, examples?, inputModes?, outputModes?}] | ≥1 skill required |

### Optional fields:

`provider` ({organization, url}), `documentationUrl`, `iconUrl`, `securitySchemes` (OpenAPI-style map), `securityRequirements` (array of security), `signatures` (JWS detached signatures).

### Discovery paths:
- `GET /.well-known/agent-card.json` — public agent card (RFC 8615)
- `GET /.well-known/agent.json` — alternate/deprecated
- `GET /a2a/discover` — list all agents (versioned, requires `A2A-Version` header)

---

## 4. Part Data Model

```
Part:
  oneof content:
    text: string       — plain text content
    raw: bytes         — base64-encoded binary (for files)
    url: string        — URL pointer to content
    data: any          — arbitrary JSON value
  metadata: object     — optional
  filename: string     — optional, e.g. "diagram.png"
  mediaType: string    — MIME type, e.g. "text/plain", "image/png"
```

---

## 5. Core Operations

| Operation | Description | JSON-RPC Method |
|-----------|-------------|-----------------|
| SendMessage | Initiate task or return direct message | `tasks/send` |
| SendStreamingMessage | Stream updates during processing | `tasks/sendSubscribe` |
| GetTask | Poll task status | `tasks/get` |
| ListTasks | List with filtering + pagination | `tasks/list` |
| CancelTask | Request cancellation | `tasks/cancel` |
| SubscribeToTask | Stream updates on existing task | `tasks/subscribe` |
| GetAgentCard | Fetch public card | `.well-known/agent-card.json` |
| GetExtendedAgentCard | Auth-gated detailed card | `agent/getExtendedCard` |

---

## 6. Security Model

- **Bearer tokens** in `securitySchemes` (OpenAPI-style, per-card)
- **Signed agent cards** via detached JWS (`signatures` array, Ed25519 EdDSA recommended)
- **No mandatory encryption** in protocol — relies on TLS at transport layer
- **Push notification auth** via webhook token (`AuthenticationInfo.scheme` + `credentials`)
- **Extended agent card** gated by auth (`capabilities.extendedAgentCard: true`)
- **Versioning via header:** `A2A-Version: 1.0` in HTTP headers or request params
- **Service parameters:** `A2A-Extensions` and `A2A-Version` as standard service params

---

## 7. MCP vs A2A — Upstream Framing

From the official spec (Appendix B) and the A2A & MCP guide:

> **A2A and MCP are complementary protocols for different aspects of agentic systems.**
> MCP = agent interacts with individual tools/resources.
> A2A = agents collaborate with each other as peers.

### Auto Repair Shop Analogy (canonical upstream example)

```
Customer (A2A) → Shop Manager Agent (A2A conversation)
  → Mechanic Agent (A2A delegated task)
    → Diagnostic Scanner (MCP tool call)
    → Repair Manual (MCP resource)
  → Parts Supplier Agent (A2A external agent)
```

### Key differences (from spec):

| Dimension | MCP | A2A |
|-----------|-----|-----|
| **Relationship** | Agent → Tool | Agent ↔ Agent |
| **Opacity** | Internal state visible via tools | Opaque — no internal state exposure |
| **Statefulness** | Stateless tool call | Stateful task lifecycle |
| **Multi-turn** | No | Yes — `contextId`, `INPUT_REQUIRED` state |
| **Update delivery** | Synchronous response | Polling / Streaming / Push notifications |
| **Strength** | Using capabilities | Partnering on tasks |

### Upstream quote (verbatim):
> "An A2A Client agent might request an A2A Server agent to perform a complex task. The Server agent, in turn, might use MCP to interact with several underlying tools, APIs, or data sources to gather information or perform actions necessary to fulfill the A2A task."

### Our architecture matches this exactly:
```
Internal agents (Hermes ASI, 333-AGI, 555-ASI) use MCP to call arifOS/GEOX/WEALTH/WELL tools.
AAA Gateway (port 3001) exposes the federation via A2A for external agent discovery + interop.
```

---

## 8. Python SDK — Key Details

**Package:** `a2a-sdk` v1.1.0
**Install:** `pip install a2a-sdk` or `uv add a2a-sdk`
**Requires:** Python ≥3.10
**Extras:** `[all, http-server, fastapi, grpc, telemetry, encryption, signing, postgresql, mysql, sqlite, sql]`

### Architecture:
- Async-native (built on modern async Python)
- Core package: `src/a2a/`
- Key abstractions: `A2AServer` (wraps agent logic), `TaskManager` (persists task state via SQL), `AgentCard` (configured at startup)
- Transport support: FastAPI/Starlette (HTTP), gRPC
- Database backends: PostgreSQL, MySQL, SQLite (via SQLAlchemy)
- Telemetry: OpenTelemetry tracing
- Signing: Ed25519 EdDSA via `[signing]` extra
- Sigstore-signed on PyPI (keyless signing via GitHub Actions)

### Compatibility:
- v1.0 spec (primary) — JSON-RPC, HTTP+REST, gRPC
- v0.3 spec (compat mode) — JSON-RPC, HTTP+REST, gRPC

---

## 9. Gap Analysis — Our Implementation vs Upstream v1.2

| # | Gap | Status | Fix |
|---|-----|--------|-----|
| 1 | **Protocol version** — cards say "1.0.0" or "a2a.v1", spec is "1.2" | 🟡 Gateway metadata says "1.2" but individual cards may be stale | Audit all 21 cards with `grep protocolVersion` |
| 2 | **Signed agent cards** — no JWS signatures. Keys exist at `/root/.secrets/aaa-identity/keys/` | 🔴 `"pending-ed25519"` since June 2026 | Implement `crypto.sign()` + sigstore |
| 3 | **Standard method aliases** — we have them ✅ | 🟢 Working in gateway server.js | Verify with `curl -X POST ... -d '{"method":"sendTask"}'` |
| 4 | **Card shape drift** — 3 divergent schemas across codebase | 🟡 Canonical source at `/root/AAA/agents/<id>/` | Normalise all to flat A2A v1.2 shape |
| 5 | **securitySchemes coverage** — only ~10/41 have it | 🔴 Missing auth metadata for external callers | Every card needs `bearer` + `apikey` schemes |
| 6 | **Task state alignment** — our custom `agent_lifecycle.js` vs 9-state canonical model | 🔴 Status mismatch when bridging external A2A agents | Audit and alias our states to canonical names |
| 7 | **W3C DID wiring** — `gen_did.py` exists but not referenced from agent cards | 🔴 Missing decentralized identity anchor | Add `verificationMethod` DID ref to agent cards |
| 8 | **Extended agent card** — auth-gated detailed card | 🔴 Not implemented | Add full card behind auth |
| 9 | **Push notifications** — we use Redis+NATS instead of webhooks | 🟡 Parallel approach, functionally equivalent | Document the mapping |

### What's NOT a gap (our differentiators):
- Governance layer (F1-F13, seal chain) — A2A has no constitutional layer
- Organ federation (GEOX, WEALTH, WELL) — external A2A exposes opaque agents, ours have governance
- Seal chain as arrow of time — no A2A equivalent

---

## 10. Quick Reference — Commands

```bash
# Check gateway health
curl -s http://localhost:3001/health | jq

# Protocol version
curl -s http://localhost:3001/.well-known/agent-card.json | jq '.protocolVersion'

# Total agents
curl -s http://localhost:3001/.well-known/agents.json | jq '.total'

# Check signed card count
grep -rl '"signatures"' /root/AAA/a2a-server/agent-cards/ 2>/dev/null | wc -l

# Check security schemes coverage
grep -rl '"securitySchemes"' /root/AAA/a2a-server/agent-cards/ 2>/dev/null | wc -l

# Check protocol version drift across cards
grep -rn '"protocolVersion"' /root/AAA/a2a-server/agent-cards/ | awk -F: '{print $3}' | sort | uniq -c

# Check our custom task lifecycle vs canonical
grep -rn 'TASK_STATE\|taskState' /root/AAA/a2a-server/*.js | head -20

# Restart gateway (with stale process kill)
lsof -ti:3001 | xargs -r kill -9 && sleep 1 && systemctl restart aaa-a2a.service
```
