# A2A Protocol Ecosystem — Gap Analysis (2026-07-13)

> **Source:** Deep research session 2026-07-13. External A2A spec research + arifOS AAA implementation audit.
> **Upstream:** A2A Protocol, Google → Linux Foundation, v1.2 (May 2026), 150+ orgs, 24.7k GitHub stars.
> **Our AAA:** A2A v1.0.0 gateway at port 3001, 30+ agent cards, custom constitutional overlay.

---

## The Agent Protocol Ecosystem (2026)

| Protocol | Layer | Creator | Status |
|---|---|---|---|
| **MCP** | Agent → Tool (vertical) | Anthropic → Linux Foundation | 97M+ downloads, de facto standard |
| **A2A** | Agent ⇄ Agent (horizontal) | Google → Linux Foundation | v1.2 (May 2026), 150+ orgs, 24.7k ★ |
| **ACP** | Agent Commerce | OpenAI + Stripe | Feb 2026, ChatGPT Instant Checkout |
| **UCP** | Agent Commerce | Google + Shopify | Jan 2026, distributed commerce |
| **AP2** | Agent Payments | Google | 60+ orgs, W3C Verifiable Credentials |
| **WebMCP** | Browser-native MCP | Google Chrome Labs | Early 2026, emerging |
| **AG-UI** | Agent → UI streaming | CopilotKit | Mid 2025 |
| **A2UI** | Agent → UI composition | Community | Mid 2025 |

---

## A2A v1.2 Spec — Key Primitives

| Component | Standard | Our Status |
|---|---|---|
| Agent Card at `/.well-known/agent-card.json` | RFC 8615, flat JSON | ✅ Present |
| Signed Agent Cards (Ed25519 JWS detached) | v1.2 feature | ❌ Missing (manifestSignature=pending-ed25519) |
| Discovery via Agent Card | OpenAPI-style | ✅ Present |
| Task lifecycle states | 6 states | ⚠️ Custom, not aligned |
| JSON-RPC 2.0 over HTTP(S) | Mandatory | ✅ Present |
| SSE streaming | Optional | ✅ Present |
| Standard methods (sendTask, getTask, cancelTask, sendTaskStreaming, resubscribeTask) | Standard | ❌ Custom names only |
| OpenAPI-style securitySchemes | Required per card | ⚠️ Only 10/30+ cards have it |
| W3C DID or WebFinger identity anchor | Recommended | ⚠️ DID infra exists, not wired to cards |
| Sigstore keyless signing | Emerging best practice | ❌ Not implemented |

---

## Agent Card v1.2 Canonical Shape

Flat JSON: `protocolVersion`, `name`, `description`, `url`, `provider`, `version`, `capabilities`, `defaultInputModes`, `defaultOutputModes`, `skills[]`, `securitySchemes`, `security[]`.

Key differences from our shape:
- **FLAT** — no nested `identity{}`, `endpoints{}`, `interaction{}` wrappers our organ cards use
- **securitySchemes** uses OpenAPI object format, not our flat `authRequired` boolean
- **`protocolVersion`** is `"1.2"` not `"a2a.v1"` or `"1.0.0"`
- `skills[].tags` for capability matching — we have this ✅

---

## A2A vs MCP

| | MCP | A2A |
|---|---|---|
| **Direction** | Vertical (agent → resource) | Horizontal (agent ⇄ agent) |
| **Peer model** | Tool consumer → tool provider | Co-equal agents |
| **Lifecycle** | Request/response | Full task lifecycle (hours, human-in-loop) |
| **Opacity** | Tool is transparent | Agent is opaque (no shared memory) |
| **Boundary** | Same system | Cross-vendor, cross-org |

**Architecture:** MCP below, A2A above. Agent uses MCP for own tools, A2A to delegate.

---

## Agent Identity Stack (2026 Emerging)

```
1. Agent Card              → What the agent claims
2. Signed Agent Card       → Cryptographic provenance (Ed25519 JWS)
3. W3C DID                 → Decentralized identifier anchor
4. Sigstore                → Keyless signing via OIDC (CI/CD pipeline)
5. WebFinger / @handle     → Human-readable resolution
6. ANS                     → Agent Naming Service (skill-based discovery)
```

---

## Our A2A Endpoints

| Custom | Equivalent Standard | Status |
|---|---|---|
| `POST /a2a/tasks/send` | `sendTask` → `POST /tasks` | ✅ Works, wrong method name |
| `GET /tasks/{taskId}` | `getTask` → `GET /tasks/{taskId}` | ✅ Same |
| `POST /tasks/{taskId}/cancel` | `cancelTask` → `POST /tasks/{taskId}/cancel` | ✅ Same |
| `POST /a2a/message/stream` | `sendTaskStreaming` → `POST /tasks/{taskId}/stream` | ✅ Works, different path/name |
| `GET /tasks/{taskId}/subscribe` | `resubscribeTask` → `GET /tasks/{taskId}/subscribe` | ✅ Same |

**Critical gaps:** `sendTask` and `sendTaskStreaming` method names don't resolve in our JSON-RPC router. External A2A clients calling standard names get 404.

---

## Our Differentiators (upstream A2A doesn't have these)

| Feature | File | What It Does |
|---|---|---|
| Constitutional floors | `agent-card-registry.js` | F1-F13 enforced on dispatch |
| Federation envelope | `federation_envelope.js` | Risk tiers + action classes |
| Membrane middleware | `membrane_middleware.js` | ZEN-ALL cross-organ gate |
| Seal chain | `seal_chain.js` | Every dispatch hash-chained |
| Cognitive hierarchy | `cognitive_hierarchy.js` | Ring classification + confidence caps |
| Pre-forge bridge | `preforge_bridge.js` | Gate before code execution |

---

## Gap Priority Matrix

| Tier | Gap | Effort | Impact |
|---|---|---|---|
| T1 | Signed Agent Cards (Ed25519 JWS) | 2-3h | High — identity trust |
| T1 | Protocol version → "1.2" alignment | 30min | Medium — spec compliance |
| T1 | Standard method aliases | 2h | High — external interop |
| T1 | Card format normalisation (flat shape) | 3-4h | High — consistency |
| T2 | securitySchemes on ALL cards | 1h | Medium |
| T2 | Task state machine alignment | 1h | Medium |
| T2 | DID-to-Agent-Card wiring | 3h | Medium |
| T3 | Sigstore CI/CD signing | 2h | Nice-to-have |

**Compliance:** ~55% v1.2 → ~85% after T1 → ~95% after T2.

---

## Key File Reference

| File | Path | Role |
|---|---|---|
| Gateway server | `/root/AAA/a2a-server/server.js` | All A2A endpoints |
| Card registry | `/root/AAA/a2a-server/agent-card-registry.js` | normaliseCard() + Map store |
| Discovery routes | `/root/AAA/a2a-server/agent-discovery-routes.js` | /a2a/discover endpoints |
| Lifecycle | `/root/AAA/a2a-server/agent_lifecycle.js` | Task state machine |
| Federation envelope | `/root/AAA/a2a-server/federation_envelope.js` | Risk tiers |
| Seal chain | `/root/AAA/a2a-server/seal_chain.js` | Hash-chained audit |
| Membrane | `/root/AAA/a2a-server/membrane_middleware.js` | Governance gate |
| Agent cards | `/root/AAA/a2a-server/agent-cards/` | 30+ cards |
| Canonical cards | `/root/AAA/agents/*/agent-card.json` | Source of truth |
| DID auth | `/root/AAA/auth/gen_did.py` | Ed25519 key generation |
| SEA | `/root/AAA/a2a-server/seal_chain.js` | Hash-chained audit |

---

## Sources

- A2A Protocol official: https://a2a-protocol.org/latest/topics/what-is-a2a/
- GitHub: https://github.com/a2aproject/A2A (24.7k ★, v1.0.1)
- Linux Foundation press (Apr 2026): https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations
- Tyk architecture: https://tyk.io/learning-center/a2a-protocol-architecture-and-technical-specification
- Agent Cards v1.2: https://blog.tobira.ai/how-a2a-agent-cards-work
- Agent Naming Service: https://blog.christianposta.com/dynamic-agent-discovery-with-a2a-and-ans
- Sigstore A2A: https://github.com/sigstore/sigstore-a2a
- Protocol ecosystem: https://www.solenya.ai/blog/20-agent-protocols
- NVIDIA A2A auth: https://docs.nvidia.com/nemo/agent-toolkit/1.4/components/auth/a2a-auth.html
- Red Hat A2A security: https://next.redhat.com/2026/05/13/securing-agent-to-agent-communication
- A2A vs MCP analysis: https://www.glukhov.org/ai-systems/comparisons/a2a-protocol-2026-adoption
