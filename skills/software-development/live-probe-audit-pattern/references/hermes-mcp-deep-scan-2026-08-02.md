# Hermes MCP Deep Scan — 2026-08-02

Worked example for the "Component / Server Existence Scan" section of the parent skill.

## The failure

Arif: "what is HERMES MCP and can we test all."

I answered from context: no product named "Hermes MCP" exists; there is only
Hermes Agent (the MCP client) plus six wired organ servers (arifOS, GEOX,
WEALTH, WELL, MAGE, HOUND). Arif pushed twice ("so there is no hermes mcp?",
then "u deep scan internal"). The scan found the server. My absence claim was
false and cost two turns.

**Root cause:** I answered an internal-inventory question from prior/context
instead of probing the box. My toolset showed 6 organs, so I concluded only 6
existed. But toolset visibility reflects what is *wired and enabled*, not what
is *on disk and running*.

## What the four-surface scan found

| Surface | Probe | Finding |
|---|---|---|
| Config | `hermes mcp` | `hermes  custom — disabled  http://127.0.0.1:18086/mcp` |
| Filesystem | `find /root/.hermes -path '*mcp*'` | `/root/.hermes/mcp_servers/hermes_mcp.py` (608 lines) |
| Process | `ps aux \| grep hermes_mcp` | live python process serving it |
| Port | `ss -tlnp \| grep 18086` | LISTEN on 127.0.0.1:18086 |

The server was live but disabled in config, so it never appeared in the agent
toolset. Disabled ≠ dead.

## What Hermes MCP actually is

- Standalone FastMCP server, header says "Extracted from arifOS kernel 2026-06-28"
- Transport: Streamable HTTP (MCP 2024-11-05), self-reported version 3.4.4
- 7 read-only governance tools:
  - `hermes_system_status` — federation organ health via live TCP probe (6/6 alive)
  - `hermes_epistemic_check` — heuristic confidence gate on a claim
  - `hermes_fact_check` — claim vs VAULT999 + heuristic
  - `hermes_cross_verify` — multi-organ attestation
  - `hermes_plan_review` — plan safety + injection scan
  - `hermes_memory_steward` — classify content into memory tiers (KSR/Ledger/Vault/Telemetry)
  - `hermes_health` — self health
- Built-in prompt-injection scanner gates all confidence-bearing tools before
  return (forged 2026-08-01 after a boundary audit found FLAME heuristics passed
  injection payloads)
- Organ registry it probes: arifOS, GEOX, WEALTH, WELL, A-FORGE, AAA

**Why it exists / why it matters:** it is a META-layer auditor over the other
organs. The six organs each do domain work and most are constitutionally gated
(require arif_init Ed25519 session). Hermes MCP does federation-wide health,
epistemic gating, and injection scanning WITHOUT a session — read-only,
advisory, ungated. That is the capability the individual organs do not expose.

## MCP Streamable HTTP test recipe (used to test all 7 tools)

```bash
BASE=http://127.0.0.1:18086/mcp
H1='Content-Type: application/json'
H2='Accept: application/json, text/event-stream'   # REQUIRED else 406

# 1. initialize — capture the session id from response HEADERS
SID=$(curl -s -D - -m 5 "$BASE" -X POST -H "$H1" -H "$H2" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r')

# 2. tools/list — needs the session id header
curl -s -m 5 "$BASE" -X POST -H "$H1" -H "$H2" -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# 3. call a tool
curl -s -m 10 "$BASE" -X POST -H "$H1" -H "$H2" -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"hermes_health","arguments":{}}}'
```

**Pitfalls hit:**
- Missing the dual `Accept` header → `406 Not Acceptable: Client must accept both application/json and text/event-stream`
- Calling `tools/list` without the session id → `400 Bad Request: Missing session ID`
- Responses arrive as SSE (`event: message` / `data: {...}`); grep `^data:` to extract the JSON

## Decision left open

Whether to `hermes mcp enable hermes` (adds the 7 tools to the agent toolset)
or keep it disabled as a manual standalone auditor. Enable = convenient but
adds ungated read tools to the default surface; disabled = deliberate, called
only when needed. Arif had not decided at session end.

## Lesson

Internal "what is X / do we have X" questions get a four-surface scan
(config, filesystem, process, port), never a from-prior answer. Absence is the
expensive claim — it requires all four surfaces probed clean.
