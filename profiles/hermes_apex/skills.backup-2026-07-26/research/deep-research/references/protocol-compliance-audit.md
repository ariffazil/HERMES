# Protocol/Standard Compliance Audit Pattern

> **Forged:** 2026-07-13 — A2A v1.0 spec vs AAA implementation gap analysis
> **Class:** External standards auditing + living implementation gap analysis

## When to Use

User says "deep research on [protocol]" or "tell me everything about [standard]" and the result needs to be mapped against our living implementation (AAA, arifOS, federation organs).

**Signals:**
- "Deep research about [protocol] and map to our [system]"
- "Find any gaps or chaos need to fix"
- "Close the eureka margin to zero"
- User shares a GitHub repo / spec URL for an external protocol standard

**Distinct from plain deep-research:** The deliverable is a GAP ANALYSIS, not a synthesis of the topic alone. The research serves the audit, not the other way around.

## Two-Loop Methodology

### Loop 1: Research + Gap Identification

#### Phase 1: Fetch the Spec
- Official docs site (e.g., `a2a-protocol.org`)
- GitHub repo — look for `specification/`, `docs/`, `adrs/`, `proto/` directories
- Raw proto files (`a2a.proto`, `mcp.proto`) — these are the normative source
- JSON schemas (often generated from proto at build time)
- README for key features, architecture diagram, version history
- Release notes / CHANGELOG — identify latest stable version
- GOVERNANCE.md — who's on the steering committee, what's the maturity model
- ADRs (Architecture Decision Records) if they exist

#### Phase 2: Fetch the Ecosystem
- Implementation guides (Tyk.io, Zuplo, Atlan) — these are practical, not theoretical
- Security analyses (Palo Alto, arXiv papers)
- Official SDKs (Python, JS, Go, Rust, Java, .NET) — understand the library support
- Comparison articles ("X vs Y") — understand competitive positioning
- Community docs (agent2agent.info, a2acn.com) — often more readable than official spec
- Industry analysis (Gartner, IBM, Microsoft) — understand enterprise adoption

#### Phase 3: Extract Normative Requirements
Build a structured table per domain:

| Spec Requirement | Our Implementation | Gap Severity |
|---|---|---|
| Exact field/path/format spec | What we have | 🔴/🟡/🟢/✅ |

**Key domains to audit:**
1. Discovery path (e.g., `/.well-known/agent-card.json` vs custom route)
2. Schema/field compliance (list ALL required fields, mark which we have)
3. Transport layer (JSON-RPC methods, headers, encoding)
4. State machine / lifecycle (task states, transitions)
5. Security model (auth schemes, signatures, key management)
6. Identity model (DIDs, WebFinger, etc.)

#### Phase 4: Classify Gaps by Severity

| Label | Meaning | Action |
|---|---|---|
| 🔴 Critical | External clients following spec CANNOT use us | Fix before claiming compliance |
| 🟡 Major | Works but wrong semantics, or missing non-required field | Fix soon |
| 🟢 Minor | Nice-to-have feature not implemented | Defer |
| ✅ Compliant | Matches spec | Keep |

#### Phase 5: Write Structured Report

Write to `forge_work/YYYY-MM-DD/{PROTOCOL}-AAA-GAP-ANALYSIS.md` with:

1. **Executive Summary** — what we found, top 3 gaps
2. **Discovery** — path compliance
3. **Schema Compliance** — field-by-field audit
4. **Transport** — protocol methods, headers, encoding
5. **State/Lifecycle** — state machine gaps
6. **Security** — auth, signatures, identity
7. **P2P Capability** — centralized vs peer to peer
8. **What We KEEP** — our unique value that should not be removed
9. **Priority-Ordered Fix List** — 🔴P0 → 🟡P1 → 🟢P2
10. **Architecture Decision** — recommended integration path

### Loop 2: Close Gaps (Optional, If User Wants)

1. **Design fix architecture** — how to integrate (wrap SDK, build connector, etc.)
2. **Write PRDs** for each P0 gap
3. **Spawn execution agent** (Kimi Code, OpenCode, etc.) with the PRDs as context

## Pitfalls

- **Don't confuse protocol versions.** Latest SDK version ≠ latest spec version. Check the proto file date and release notes.
- **Don't assume our custom fields are wrong.** Our constitutional extensions (class, bound_to, power_band, f1_boundary, rollback_plan) are VALUE-ADD, not noise. Keep them and layer them ON TOP of required fields.
- **Don't conflate audit trail with protocol state machine.** Our seal chain serves a different purpose than A2A task lifecycle. Keep both — they're complementary, not redundant.
- **Don't delete our custom routes.** `/a2a/discover` can stay as a federation registry extension. Just ADD the required `/.well-known/agent-card.json`.
- **The official SDK may already have what you need.** Before building custom handlers, check if `@a2a-js/sdk` (or the equivalent) provides Express integration with `agentCardHandler`, `jsonRpcHandler`, SSE streaming out of the box.
- **Proto files are the normative source.** JSON schemas in a `specification/json/` directory are usually a generated artifact. Don't edit them — edit the proto and regenerate.

## Example: A2A v1.0 Key Spec Locations

| Asset | URL |
|---|---|
| Official spec | `a2a-protocol.org/latest/specification/` |
| GitHub repo | `github.com/a2aproject/A2A` |
| Proto file | `github.com/a2aproject/A2A/blob/main/specification/a2a.proto` |
| JS SDK | `npm install @a2a-js/sdk` |
| Express integration | `@a2a-js/sdk/server/express` — `agentCardHandler`, `jsonRpcHandler` |
| AGENT_CARD_PATH | `/.well-known/agent-card.json` (constant in SDK) |
| Validation tool | `agent-ready.dev/agent-card-validator` |
| Agent Card community docs | `agent2agent.info/docs/concepts/agentcard` |
| Agent protocol stack analysis | Subhadip Mitra's blog (Jan 2026) — MCP+A2A+A2UI as TCP/IP stack |
