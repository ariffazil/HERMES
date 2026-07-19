# Public MCP Ingress Audit — 2026-07-18

**Origin:** A-FORGE write surface (`forge.arif-fazil.com/mcp`) was found publicly
callable without authentication via an unauthenticated JSON-RPC `initialize`
probe. This recipe documents the audit pattern, findings template, and the
three valid postures when exposure is found.

## The Probe Pattern (5-second recipe)

For every public organ route, run two probes. The first tests liveness; the
second tests capability advertisement. **Both must pass for the surface to be
considered safe.**

```bash
# 1. Liveness + envelope size baseline
curl -sf https://<organ>.arif-fazil.com/health \
  | python3 -c "import sys; b=sys.stdin.buffer.read(); print('bytes:', len(b))"

# 2. JSON-RPC initialize — does the server advertise tools + write capability?
curl -sX POST https://<organ>.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' \
  | python3 -m json.tool
```

**Output to inspect (probe 2):**

| Field in `result` | Risk if present |
|---|---|
| `capabilities.tools` | Read or write surface available — probe tools/list |
| `capabilities.tasks.requests.tools.call` | Tasks can call tools — confirm scope |
| `capabilities.registration.tool` | A specific write tool is the registration entry — confirm gate |
| `capabilities.experimental.*` | New protocol features — check what they enable |

**Output to inspect (probe 1):**

| Bytes | Verdict |
|---|---|
| < 500 | Lean — `/health` is doing its job |
| 500–2000 | Acceptable if documented (identity, version) |
| 2000–10000 | Over-rich — move metadata to `/manifest` or `/.well-known/` |
| > 10000 | Envelope bloat — Tier 1 fix candidate |

## The Findings Template

```yaml
finding:
  surface: <organ>.arif-fazil.com
  port_internal: <port>
  posture: intentional | misconfiguration | already-known
  tools_exposed: [<list from tools/list>]
  write_tools: [<list, if any>]
  auth_required: true | false
  envelope_bytes_health: <number>
  envelope_bytes_initialize: <number>
  envelope_bytes_tool_call: <number>
  ratified_by: <sovereign ruling ref, if already-known>
  fix_required: true | false
  fix_tier: T1 | T2 | T3
```

## Worked Audit (2026-07-18)

Three organ routes probed:

| Surface | Internal Port | Initialize Result | Envelope `/health` | Posture |
|---|---|---|---|---|
| `mcp.arif-fazil.com/mcp` | :8088 (arifOS) | success, tools+resources+prompts+registration | 11,150 bytes | TBD — read/judge surface, less concerning |
| `forge.arif-fazil.com/mcp` | :7071 (A-FORGE) | success, tools + registration.tool=forge_agent | 1,149 bytes | TBD — write surface, P0 candidate |
| `geox.arif-fazil.com/mcp` | :8081 (GEOX) | success, identity domain | — | TBD — domain organ, read-only by doctrine |

**Pending decision (held 2026-07-18):** intentional / misconfiguration /
already-known for each. Until ratified, Path A (MCPJam external inspector) is
on hold because pointing a public inspector at an unauthenticated write surface
without a sovereign ruling is itself a T3 violation.

## Posture Decision Matrix

When `tools` capability is advertised publicly, three postures are valid:

### Intentional

**Meaning:** Public MCP by design. Governance is enforced via kernel judge
+ audit chain + confirmation gates. Every write tool has a confirm-window that
unauthenticated callers cannot bypass.

**Test:** does `forge_agent` (or any write tool) require an actor signature,
challenge-response, or confirmation token before mutating? If yes, posture
is intentional. If no, posture is **misconfiguration**, not intentional —
even if someone said "it's fine" in chat.

**Documentation:** sovereign ruling in `/root/SESSION.md` or `/root/AAA/governance/`.

### Misconfiguration

**Meaning:** Route should be auth-gated or only expose read surface. The
Caddyfile or upstream config needs a fix.

**Fix tier:** T2 (10s announce) for read surface separation; T3 (888_HOLD)
for Caddy reload affecting all HTTPS routes.

**Verification after fix:** re-run the probe. `capabilities.tools` should
either be absent or advertise only read tools (`tools/list`, `resources/read`,
`prompts/get`).

### Already-known and accepted

**Meaning:** Sovereign ruling already exists. The exposure is documented
risk, not a finding.

**Documentation:** pointer to the ruling in the audit receipt. No fix needed
beyond citing the source.

## Anti-Patterns

| Anti-pattern | Why wrong |
|---|---|
| "Kernel enforces floors so public surface is fine" | Floors are advisory until a write happens. Public caller triggers the floor *after* the call lands. |
| "HTTPS is encrypted so it's secure" | Encryption ≠ authorization. The point is who can call, not how the bytes travel. |
| "Nobody knows the URL anyway" | URLs are discoverable. DNS, certificate transparency logs, the llms.txt file. Assume public. |
| "It's internal — we don't put auth on it" | Internal-facing assumes a network boundary. Cloudflare + Caddy = public. |
| "Audit by reading code" | The live wire is the surface (Pitfall 8). Code is intent. Wire is reality. |

## Envelope Audit Pattern (Companion Recipe)

When the critique is "responses are too big," `wc -c` is the audit:

```bash
# Three measurements, runnable in 10 seconds
for ep in /health /mcp /tools/list; do
  printf "%-15s %s bytes\n" "$ep" "$(curl -sf -X POST http://127.0.0.1:<port>$ep -H 'Content-Type: application/json' -d '{}' | wc -c)"
done
```

**Rule:** `/health` under 500 bytes = lean. Over 2000 bytes = audit candidate.
The fix is moving metadata to dedicated endpoints (`/manifest`, `/.well-known/`),
not removing the metadata.

**Tiered verbosity:** when init accepts `verbosity: minimal|standard|full`,
enforce it on every tool that emits an envelope. One tool honoring the knob
while others ignore it = the knob is decorative. Test the rule by setting
`verbosity: minimal` and verifying that subsequent calls return
`<500 bytes` envelope payload.

## Origin

Forged 2026-07-18 during the GPT-5.6 audit response. The conversation moved
from "your envelopes are bloated" (critique) to "slim them" (commitment) to
"stop describing, start measuring" (a tool reference: MCPJam inspector) to
"public write surface is exposed" (the finding that actually mattered).
The probe sequence above is the minimum-viable audit that surfaced the
finding in <30 seconds.
