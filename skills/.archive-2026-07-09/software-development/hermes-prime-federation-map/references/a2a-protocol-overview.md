# A2A Protocol Overview — Agent-to-Agent

> **Source:** `https://github.com/a2aproject/A2A` (Apache 2.0, Linux Foundation)
> **Latest release:** v1.0.1 (May 2026)
> **Contributed by:** Google
> **Distinction from MCP:** MCP = agent→tools (vertical). A2A = agent↔agent (horizontal). They complement.

## Governance

Technical Steering Committee (8 seats):

| Company | Rep |
|---------|-----|
| **Google** | Todd Segal (Principal Eng) |
| **Microsoft** | Darrel Miller (Partner API Architect) |
| **Cisco** | Luca Muscariello |
| **AWS** | Abhimanyu Siwach |
| **Salesforce** | Stephen Petschulat |
| **ServiceNow** | Sean Hughes |
| **SAP** | Sivakumar N. |
| **IBM Research** | Kate Blair |

Standard LF governance: TSC meets on Zoom, quorum = 50%, majority vote. Discussions on Discord (discord.gg/a2aprotocol), decisions on GitHub.

## Architecture

| Layer | Mechanism |
|-------|-----------|
| **Transport** | JSON-RPC 2.0 over HTTP(S) |
| **Discovery** | Agent Cards (JSON) — capabilities, auth schemes, endpoints |
| **Interaction** | sync request/response, SSE streaming, async push notifications |
| **Task model** | Full lifecycle with terminal/interrupted states |
| **Data** | Text, raw bytes (base64), URLs, structured JSON |
| **Spec source** | `a2a.proto` (protobuf, single source of truth: `specification/a2a.proto`) |
| **JSON Schema** | Generated from proto via `protoc-gen-jsonschema` (not committed; transient build artifact) |

## Key RPCs (from `a2a.proto` → `A2AService`)

| RPC | HTTP Verb | Path | Purpose |
|-----|-----------|------|---------|
| `SendMessage` | POST | `/message:send` | Send message, get task back |
| `SendStreamingMessage` | POST | `/message:stream` | SSE streaming response |
| `GetTask` | GET | `/tasks/{id}` | Poll task state |
| `ListTasks` | GET | `/tasks` | Filter/query tasks |
| `CancelTask` | POST | `/tasks/{id}:cancel` | Cancel in-progress task |
| `SubscribeToTask` | GET | `/tasks/{id}:subscribe` | Push updates via SSE |
| `CreateTaskPushNotificationConfig` | POST | `/tasks/{id}/pushNotificationConfigs` | Webhook config |
| `GetExtendedAgentCard` | GET | `/extendedAgentCard` | Full agent card w/ auth context |

All paths have `/{tenant}/` variants for multi-tenant routing.

## Task Lifecycle States

```
SUBMITTED → WORKING → COMPLETED (terminal)
                    → FAILED (terminal)
                    → CANCELED (terminal)
                    → REJECTED (terminal)
                    → INPUT_REQUIRED (interrupted — needs user input)
                    → AUTH_REQUIRED (interrupted — needs auth)
```

Interrupted states let the agent pause and request human input/auth before continuing. Terminal states are final.

## Message Model

```
Message {
  message_id: string (UUID, required)
  context_id: string (optional, groups interactions)
  task_id: string (optional, associates with a task)
  role: USER | AGENT
  parts: [Part, ...] (required, at least 1)
  metadata: Struct (optional)
  extensions: [string] (extension URIs)
  reference_task_ids: [string] (cross-task context)
}

Part {
  oneof content: text | raw (base64) | url | data (JSON)
  metadata: Struct
  filename: string
  media_type: MIME type
}
```

## Agent Card (Discovery)

Served at `GET /agent-card` (or `GET /extendedAgentCard`). Contains:
- `name`, `description`, `version`, `protocolVersion`
- `capabilities`: streaming, push notifications, skill names
- `endpoints`: list of `AgentInterface` entries with URL + auth schemes (API key, OAuth 2.0, OIDC)
- `security`: validation schemas
- `provider`: org name + URL
- `skills`: array of `{id, name, description, tags}`

## SDKs

| Language | Install | Repo |
|----------|---------|------|
| Python  | `pip install a2a-sdk` | a2aproject/a2a-python |
| Go      | `go get github.com/a2aproject/a2a-go` | a2aproject/a2a-go |
| JS/TS   | `npm install @a2a-js/sdk` | a2aproject/a2a-js |
| Java    | Maven | a2aproject/a2a-java |
| .NET    | `dotnet add package A2A` | a2aproject/a2a-dotnet |
| Rust    | `cargo add a2a-lf` | a2aproject/a2a-rs |

Samples repo: `a2aproject/a2a-samples`

## A2A vs MCP

| Dimension | MCP | A2A |
|-----------|-----|-----|
| Relationship | Agent → **Tool** (vertical, owner-agent exposes its capabilities) | Agent ↔ **Agent** (horizontal, two opaque agents collaborate) |
| What's exposed | Internal tools, resources, prompts as capabilities | Agent capabilities (skills, auth, endpoints) — NOT internals |
| Unit of work | Resource access / tool call (stateless or sessioned) | **Task** with full lifecycle, history, artifacts |
| Interaction | Query-response (sync or streaming) | Negotiated modalities, long-running, push |
| Opacity | Agent's tools are visible | Agent internals remain hidden (memory, tools, state) |
| Discovery | List resources/tools | Agent Card with capability negotiation |
| Use case | "Read this file / write to DB / call API" | "Collaborate on this project / handle this subtask" |

**They work together.** MCP gives agents tools. A2A lets agents work together.

## How arifOS Implements It

- **AAA organ** (port 3001) runs the A2A v1.0.0 TypeScript gateway (Express 4.x)
- **26 agent cards** registered post-EUREKA-ZEN SUBSTRATE LOCK, all KERNEL-bound
- **Extended schema with constitutional fields:** `class`, `bound_to`, `power_band`, `epistemic_floor`, `f1_boundary`, `rollback_plan`
- **Two-field-whitelist trap:** `normaliseCard()` in `agent-card-registry.js` AND the response mapper in `agent-discovery-routes.js` both strip unknown fields — both must be patched to expose custom fields
- **Seal chain:** Every A2A dispatch appends a hash-chained seal to VAULT999
- **Gateway restart required** for card changes: `systemctl restart aaa-a2a.service`
- **Constitutional overlay:** Agent cards use `$schema: arifOS/agent-card/v2.2.0`

See also: `a2a-agent-card-registration` skill (devops) for operational card registration, and `references/a2a-agent-card-normalization.md` for the two-stage whitelist fix.
