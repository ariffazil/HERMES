# A2A v1.0.0 / v1.0.1 Specification Facts

Discovered during AAA A2A audit (2026-07-13). Condensed spec knowledge for future conformance audits.

## AgentCard Schema (Official, §8.1)

**Required fields:** `name`, `description`, `url`, `provider` (with `organization`), `version`, `capabilities`, `skills`

**Optional fields:** `documentationUrl`, `id`, `protocolVersion` (string like "1.0.0"), `securitySchemes` (Map), `security` (OR-array), `defaultInputModes`, `defaultOutputModes`, `supportsAuthenticatedExtendedCard` (deprecated → `capabilities.extendedAgentCard`), `extendedAgentCardUrl`, `agentCardSignature` (JWS), `extensions`

**Capabilities** (exact spec fields, no extras): `streaming` (bool), `pushNotifications` (bool), `stateTransitionHistory` (bool), `extendedAgentCard` (bool)

**Skills** each require: `id`, `name`, `description`. No bare-string entries in the array — that's a type violation.

**`agentCardSignature`** (§8.1): JWS-signed blob with `jws`, `issuer`, `iat`, `exp`, `subject`, `purpose`. MUST be present for signed agent cards. Verification is server-side.

## Task Lifecycle (§3.1)

**Official A2A v1.0.0 states** (8 total):
```
SUBMITTED → WORKING → COMPLETED
                    → FAILED
                    → CANCELED
                    → REJECTED
                    → INPUT_REQUIRED
                    → AUTH_REQUIRED  ← OFTEN MISSING
```

`AUTH_REQUIRED` is the most commonly missed state — used when additional authentication is needed mid-task (token expiry, re-auth).

**`referenceTaskIds`** — Present in `SendTaskRequest` for multi-turn refinement. Often unimplemented.

## Transport / Wire Format (§9)

**JSON-RPC 2.0** — `jsonrpc: "2.0"` field REQUIRED on all request/response messages.

**`A2A-Version` header** (§9.4.2) — Servers MUST accept and validate the `A2A-Version` HTTP header. Clients MUST send it. Values: `"1.0.0"`, `"1.0.1"`, etc.

**SSE event types** — Not just generic `data:` frames. Spec defines distinct event types: `task`, `message`, `error`, `done`. Each event should carry the type so clients can route without parsing.

**Push Notification Config CRUD** — `/tasks/pushNotificationConfig/set|get|list|delete` — lifecycle for push notification URLs per task.

## Discovery (§8)

**Canonical endpoint:** `GET /.well-known/agent-card.json`

**Capability-based discovery** — `/a2a/discover` or similar. Response MUST include: `securitySchemes`, `defaultInputModes`, `defaultOutputModes` — not just `capabilities`.

**Extended card** — Served at a URL declared in `extendedAgentCardUrl` field. Auth-protected, contains additional metadata only visible to authenticated callers.

## Proto / Serialization (§1.4)

**`spec/a2a.proto`** is the SINGLE authoritative normative definition of all protocol data objects. Not JSON Schema. Not OpenAPI. The `.proto` file is normative.

**No committed JSON.** The spec says `spec/a2a.json` is a non-normative build artifact, MUST be regenerated from proto, NOT committed or edited manually.

**gRPC binding** (§9.5): `A2AService` with RPCs: `SendMessage`, `GetTask`, `CancelTask`, `SendTask`, `GetAgentCard`. These are REQUIRED for full spec compliance alongside JSON-RPC.

## Security (§8.3)

**`securitySchemes`** is a Map (not array in JSON-RPC binding). Keys are scheme IDs, values are scheme objects with `type`, `description`, and type-specific fields.

**`security`** is an OR-array of AND-arrays: `[{ "bearer": [] }, { "api_key": [] }]` means "EITHER bearer token OR API key".

**JWS agent card signatures:** The spec defines AgentCardSignature with full JWS lifecycle. Verifying agent card signatures is a server responsibility.
