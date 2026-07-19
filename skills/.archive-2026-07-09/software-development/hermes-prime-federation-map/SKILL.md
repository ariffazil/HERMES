---
name: hermes-prime-federation-map
description: "Map of the arifOS federation — organs, ports, roles, MCP surfaces, health probes. Load when Arif asks 'what organs are alive', 'show me the federation', 'is X running', 'what port is Y', or when you need to route a task to the right organ."
tags: [federation, arifos, organs, mcp, health, routing]
triggers:
  - "federation"
  - "organs"
  - "what's running"
  - "is X alive"
  - "health check"
  - "arifos"
  - "geox"
  - "wealth"
  - "well"
  - "a-forge"
  - "aaa"
  - "a2a"
  - "cognitive architecture"
  - "LeCun modules"
---

# Hermes Federation Map

## Federation Nodes (Multi-VPS)

| Node | Sigil | IP | Role | SSH | Networking |
|---|---|---|---|---|---|
| **FORGE** ⚒️ | af-forge | 72.62.71.199 | Federation engine, 8 organs, public MCP endpoint | Port 22888 | Hosted Tailscale (arifbfazil@) |
| **FLOW** 🌊 | srv1642546 | 72.61.126.65 | Communication backbone, Telegram gateway, Caddy, Ollama | Port 22 (default) | Headscale (100.64.0.4, tag:hermes, node srv1642546-1) |

**SSH federation:** Bidirectional. FORGE→FLOW via `~/.ssh/id_ed25519`. FLOW→FORGE via `~/.ssh/azwa-forge` on port 22888.

**Headscale:** Self-hosted Tailscale coordination on FORGE — internal `127.0.0.1:8083`, public `https://headscale.arif-fazil.com` (Caddy proxy on port 443). FLOW joined as federation node (100.64.0.4, srv1642546-1, tag:hermes). FORGE stays on hosted Tailscale for personal devices. Migration plan: node-by-node when ready.

**🔴 Provider firewall constraint (Hostinger):** Non-standard ports (including 8083) are blocked between VPSes. All cross-VPS traffic MUST use Caddy-proxied HTTPS on port 443. Never use raw `IP:port` for inter-VPS connections. Diagnostic: tcpdump shows SYN arriving but no SYN-ACK — provider-level DROP, not iptables/UFW. Full pattern: `vps-operations` → `references/hostinger-firewall-constraints.md`.

**Naming convention:** Single sigil + single lexical unit (zen-md). ⚒️ FORGE = hands/engine. 🌊 FLOW = communication/voice.

## The Six Active Organs

| Organ | Repo | Port | Role | MCP Tools |
|-------|------|------|------|-----------|
| **arifOS (Ω)** | ariffazil/arifOS | 8088 | Constitutional kernel — F1-F13, 888 JUDGE, VAULT999 | `arif_*` — 12 exposed via MCP (17 loaded, 58 declared; exposed = public facade) |
| **GEOX 🌍** | ariffazil/geox | 8081 | Earth intelligence — wells, seismic, petrophysics | `geox_*` — 87 tools via /tools (own MCP server, stateful sessions) |
| **WEALTH 💰** | ariffazil/wealth | 18082 | Capital intelligence — NPV, risk, stock analysis | `wealth_*` — 50 tools via /tools (own MCP server, stateless) |
| **WELL 🫀** | ariffazil/well | 18083 | Human readiness — sleep, fatigue, dignity | `well_*` — 18 tools via /tools (own MCP server, stateless) |
| **A-FORGE ⚒️** | ariffazil/A-FORGE | 7071 (HTTP) / 7072 (MCP) | Execution shell — build, deploy, orchestrate, **web access** | `forge_*` — 111 tools (execution, leases, proxies, web search/fetch, browser) |
| **AAA 🖥️** | ariffazil/AAA | 3001 | Control plane — A2A gateway, cockpit dashboard | A2A server, deliberation |

**APEX (:3002)** — DECOMMISSIONED. Deliberation absorbed into AAA a2a-server.

## Health Probe

```bash
for svc in "arifos:8088" "aforge:7072" "aaa:3001" "geox:8081" "wealth:18082" "well:18083"; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name :$port" || echo "❌ $name :$port"
done
```

## Known Anomalies (do NOT touch without 888_HOLD)

| Anomaly | Severity | Fix |
|---|---|---|
| `arif_verify` tool absent from arifOS kernel | 🔴 P0 | Tool not built — `curl :8088/tools` returns 11 tools, `arif_verify` absent. `callArifVerify()` in A-FORGE throws → HARD_DENY (correct conservative default). **Must be built.** This is the cryptographic leash. Without it, the cage has a placeholder hasp. |
| `pre_mcp_call` hook registered but NOT firing | 🔴 P1 | Hermes logs: `WARNING unknown hook event 'pre_mcp_call'`. Gateway expects `pre_llm_call`, not `pre_mcp_call`. Intent routing before A-FORGE calls is silently disabled. | Fix hook event name in `~/.hermes/config.yaml` OR implement `pre_mcp_call` in Hermes gateway. Until fixed: routes by tool-prefix pattern matching. |
| `runtime_drift: true` on arifOS | 🟡 P1 | `build_commit 198398c` ≠ `live_commit 551f156` in running image. `kanon-198398c` vs `kanon-551f156`. | Rebuild container from current source. |
| AAA healthy but 0 orgs registered | 🟡 P1 | `curl :3001/health` → healthy, `orgs: []`. Routing paths exist but federation mesh not bootstrapped. Different from organ down. | Run federation init. |
| `identity_drift: DRIFT` in carry_forward.json | 🟡 P1 | Intentional wake protocol: `ADDRESS_DRIFT_BEFORE_PROCEED`. Nonce not signed this session. Not a bug — self-diagnosis working. | Sign `arif_init` nonce with Ed25519, or reset session. |
| WELL stale biometrics (2026-04-30) | 🟡 P1 | `owner_summary: RED`; last biometric from 2026-04-30. | WELL self-report via `biometric_inject.sh`. Do NOT invent vitals. |
| `witness` fields null in thermodynamic | 🟡 P1 | No tri-witness events yet. Null = no events recorded, not breach. | Accumulates through use. Not actionable until events exist. |
| Hermes built-in tools bypass A-FORGE gate | 🟡 P1 | `terminal()`, `read_file()`, `write_file()` execute directly — no A-FORGE elicitation, no SEAL check. Any agent with access bypasses the cage. | A-FORGE gate works for OpenClaw subagents. Hermes own tools outside the cage by design. |
| GEOX tools/list = 0 but health OK | 🟡 P2 | Separate from seal chain. GEOX MCP handshake issue. | Investigate GEOX MCP registration. Not blocking — health probe confirms alive. |

## Explorer Organ Roles (2026-07-06)

The federation is not just "tools" — it's a governed explorer civilization. Each agent has a structural role in the OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY loop:

| Agent | Explorer Role | Function | Loop Stage |
|-------|--------------|----------|------------|
| **Hermes** | Explorer Intelligence Router | Routes queries, dispatches stages, gap-elicitor, contradiction-surfer | All (orchestrator) |
| **OpenClaw** | Physical Executor | Executes code, runs tests, deploys, falsifies | VERIFY + FALSIFY |
| **OpenCode** | Cognitive Generator | Generates hypotheses, alternative solutions, design exploration | HYPOTHESIZE |
| **arifOS** | Judge | Verdicts (SEAL/SABAR/HOLD/VOID), floor checks | Governance gate |
| **AAA** | Civilization Layer | Identity, leases, domain_law, agent lifecycle | Authority binding |
| **A-FORGE** | Forge | Tool birth, fitness testing, mutation, retirement | Evolution |

**Governance chain:** All three explorer agents are governed by APEX THEORY, judged by arifOS kernel, civilized by AAA, evolved by A-FORGE.

**Schemas:** Knowledge graph, intent route, and explorer packet schemas at `/root/AAA/docs/schemas/`. See `apex-governance` skill → `references/explorer-protocol-schemas.md` for full specification.

## Constitutional Separation (Brain / Hands)

- **arifOS MCP (8088)** = sovereign governor — floors, judgment, VAULT999, INIT→JUDGE→SEAL
- **A-FORGE MCP (7072)** = governed actuator — `forge_*` execution, leases, proxies
- A-FORGE **never** adjudicates. All high-risk execution requires lease + prior arifOS judgment.

## MCP = Capability, arifOS = Authority

```
MCP says: "I can do this."
arifOS says: "Are you allowed to?"
```

## Intent Routing via `arif_route` (Federation Default, 2026-07-04)

For ambiguous intents ("interpret seismic section", "assess portfolio risk"), arifOS kernel tool `arif_route` resolves to the right organ + tool prefix. Verified working:

```bash
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_route",
                 "arguments":{"intent":"interpret seismic section"}}}'
# → {"result":{"intent":"interpret seismic section",
#              "organ":"GEOX","port":8081,"tool_prefix":"geox_",
#              "routing_confidence":0.85,"verdict":"SYUBHAH"}}
```

**Why this matters:** Federation routing should not depend on the agent pattern-matching tool prefixes by hand. `arif_route` makes intent → organ a kernel concern, not an LLM concern.

**Hermes wiring (added 2026-07-04, reversible):**

```yaml
# ~/.hermes/config.yaml
hooks:
  pre_mcp_call:
    enabled: true
    type: intent_route
    endpoint: http://127.0.0.1:8088/mcp
    tool: arif_route
    fallback_on_error: passthrough    # safe default — direct call if router unreachable
    cache_routes: true
    cache_ttl_seconds: 300
    applies_to_toolsets: [federation, mcp, aforge, arifos, geox, wealth, well]

hooks_auto_accept: true   # allow this hook to fire without per-call approval

federation:
  router:
    enabled: true
    default: arif_route
    organs:
      GEOX:    {host: 127.0.0.1, port: 8081,  prefix: geox_}
      WEALTH:  {host: 127.0.0.1, port: 18082, prefix: wealth_}
      WELL:    {host: 127.0.0.1, port: 18083, prefix: well_}
      A-FORGE: {host: 127.0.0.1, port: 7072,  prefix: forge_}
      arifOS:  {host: 127.0.0.1, port: 8088,  prefix: arif_}
      HERMES:  {host: 127.0.0.1, port: 18086, prefix: hermes_}
```

Activates on gateway restart: `systemctl --user restart hermes-gateway` or `hermes gateway run --replace`.

**Pitfall:** This hook is a config declaration. Hermes v0.17.0 must support `pre_mcp_call` hook firing. If gateway rejects the config on restart, the `fallback_on_error: passthrough` keeps federation working — but routing is degraded (manual pattern-matching returns). Verify after restart with a test call that should hit `arif_route` first.

## Tool Discovery

Run `arif_retrieve_tools(query="*")` via arifOS MCP to discover ALL tools across all organs.
Check `https://mcp.arif-fazil.com/manifest/tools.json` for the public 7-tool surface.

## MCP Surfaces (Non-Organ)

| MCP Server | Status | Tools | Purpose |
|-----------|--------|-------|---------|
| **stealth-browser** | ✅ LIVE | 31 | nodriver + CDP. Anti-bot bypass. Navigate, click, type, screenshot, JS eval, cookies, forms, tabs. Idle reaper at 600s. |

Config: `openclaw.json > mcp.servers.stealth-browser`
Server: `/root/stealth-browser-mcp/src/server.py`
Venv: `/root/stealth-browser-mcp/venv/bin/python`

## Telegram Bot Infrastructure (3 bots, verified 2026-07-04)

| Bot Handle | Bot ID | Display Name | Env Var | Gateway |
|---|---|---|---|---|
| `@AGI_ASI_bot` | 8149595687 | AGI🦞 | `TELEGRAM_BOT_TOKEN` | OpenClaw gateway (:18789) |
| `@ASI_arifos_bot` | 8410138119 | ASI💃 | `HERMES_TELEGRAM_BOT_TOKEN` = `ASI_BOT_TOKEN` | Hermes gateway (polling) |
| `@arifOS_bot` | 8727562763 | 777 FORGE | `TELEGRAM_OPENCODE_BOT_TOKEN` | OpenCode bot.py (polling) |

All three can be in the AAA group (-1003753855708) simultaneously. Each has independent model quotas.
Full details: `federation-organ-liveness-probe` → `references/telegram-bot-infrastructure.md`.

## Telegram Mini App (Federation Surface, 2026-07-09)

A Telegram Mini App exists at `/root/AAA/telegram-miniapp/` — MCP-powered intelligence overlay accessible via Telegram WebView.

| Component | Tech | Port | Purpose |
|---|---|---|---|
| API Gateway | Hono | 3100 | Proxies HTTP → MCP JSON-RPC to all organs |
| Mini App | React + Vite | 5173 | Dark-theme UI: Explore, Wealth, Well, Status pages |
| Bot | grammY | — | Entry point, opens WebView |

**MCP session management:** GEOX + arifOS are stateful (initialize → session-id → tools/call); WEALTH + WELL are stateless. 5-min TTL on sessions.

**Deploy:**
```bash
cd /root/AAA/telegram-miniapp
cp .env.example .env  # set BOT_TOKEN
# Docker: docker-compose up -d
# Or direct: pnpm dev:api & pnpm dev:app & pnpm dev:bot
```
Caddy route needed: `app.arif-fazil.com → :5173`.

**No mock data** — every API call hits real MCP servers via JSON-RPC 2.0 protocol.

## Tool-Count Probe Pattern (2026-07-09)

Live tool counts diverge from documented counts. Use this to verify before reporting:

```bash
for port in 8088 8081 18082 18083 7072; do
  count=$(curl -sf "http://localhost:$port/tools" 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    t=d.get('tools',d) if isinstance(d,dict) else d
    print(len(t))
except: print(0)
" 2>/dev/null)
  echo "Port $port: $count tools"
done
```

**Pitfall:** Static gateway pages (e.g. `mcp.arif-fazil.com`) can have hardcoded counts that drift from live `/tools` endpoints. Always probe `localhost:<port>/tools` directly — never trust a static page or AGENTS.md numbers without verification. The canonical distinction for arifOS: `tools_exposed_via_mcp` (public facade, what `/tools` returns) ≠ `loaded` (internal) ≠ `declared` (blueprint).

## LeCun Cognitive Architecture Mapping (2026-07-07)

arifOS implements all 6 of LeCun's cognitive modules for autonomous intelligence (2022 position paper) plus a 7th:

| LeCun Module | arifOS Implementation | Organ |
|---|---|---|
| Configurator | `arif_init()` session config | arifOS |
| Perception | GEOX/WEALTH/WELL observe tools | GEOX/WEALTH/WELL |
| World Model | `arif_think` + `forge_reality_loop` | arifOS/A-FORGE |
| Cost | `forge_evaluate` (APEX: G = A·P·E·X·Φ) | A-FORGE |
| Actor | `forge_execute` + `forge_shell` | A-FORGE |
| Short-term Memory | VAULT999 + seal chain + memory | arifOS |
| **Governance** (LeCun doesn't have) | F1-F13, constitutional floors, sovereign veto | arifOS |

**Implication:** The federation is a cognitive architecture for autonomous intelligence with an additional governance layer that LeCun's design lacks. Full mapping, JEPA family tree, and J-space synthesis in `references/j-space-jepa-synthesis.md`.

## A-FORGE Web Tools (CRITICAL — use these FIRST)

A-FORGE MCP (:7072) has **111 tools** including web search, fetch, and browser capabilities. **USE THESE BEFORE HERMES BUILT-IN TOOLS FOR ANY WEB TASK.**

| Tool | Purpose |
|------|---------|
| `forge_search` | Brave Search — reliable web search from VPS |
| `forge_fetch_url` | Fetch a URL and return content |
| `forge_fetch_json` | Fetch JSON from a URL |
| `forge_fetch_metadata` | Extract metadata from a URL |
| `forge_fetch_links` | Extract links from a URL |
| `forge_research` | Deep research on a topic |
| `forge_browser_*` | Navigate, click, type, screenshot, extract, JS eval |

**Discovery command:**
```bash
curl -s -X POST http://127.0.0.1:7072/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t.get('name','?')) for t in d.get('result',{}).get('tools',[])]"
```

**Pitfall:** Tavily (web_extract) returns 432 on many domains. Bing/DDG/Google hit CAPTCHA on VPS IPs. **Do NOT waste time on these.** Use `forge_search` via Brave — it works reliably.

**Pitfall (SOVEREIGN CORRECTION, 2026-07-18):** Never report "Cloudflare blocked" / "CAPTCHA" / "access denied" as an excuse to the user. The user has provided tools. If one path fails, try another. A-FORGE web tools are the first fallback. Browser with stealth is the second. Report the blocker only after exhausting ALL options. The user explicitly corrected: "Don't ever use cloudflare block as alasan. Semua tool aku dah bagi. Jangan menyusahkan manusia."

## Pitfalls

- If an organ is ❌, proceed read-only on live organs. Do NOT assume dead organ's config is valid.
- Never declare a tool absent without probing the full surface first (`forge_registry_status` + `arif_retrieve_tools` + `forge_docs_lookup` + FS scan + `:port/health`).
- Negative capability is allowed only with proved absence.

### Multi-VPS naming confusion — verify before optimizing
External agents (including wawabot) can misidentify which VPS they're on. **Proven 2026-07-16:** wawabot diagnosed "this machine is FLOW (72.61.126.65)" when it was actually FORGE (72.62.71.199). The hostname said `forge` but the agent trusted its own assumption over the evidence.

**Rule:** Before any cross-VPS operation, verify with `hostname -I | awk '{print $1}'` and match against this map. Don't trust the hostname alone — an IP mismatch means you're on the wrong box.

### SSH port is non-standard on FORGE
AF-FORGE sshd listens on **port 22888**, not 22. Probing port 22 returns REFUSED, which looks like "sshd down" but is actually "wrong port." Always use `-p 22888` when SSHing to FORGE from other nodes.

## Pitfall: startup banner "failed" ≠ service down (2026-07-04)

The Hermes startup banner shows MCP discovery status per server. A `(streamable-http) — failed` line means **discovery probe at boot missed**, NOT that the service is down. Verified by direct curl:

```bash
# Banner said: "openclaw (streamable-http) — failed"
# Reality:
curl -sf http://127.0.0.1:18789/health
# → {"ok":true,"status":"live"}
```

**Rule:** the only ground truth for "is X alive" is `curl -sf http://localhost:PORT/health` (or the equivalent for non-HTTP services). Banner state is a startup snapshot that can be stale, partially probed, or hit during transient service warmup. Always probe live before reporting an organ as down.

## Standalone Hermes MCP (port 18086, hermes_mcp.py)

A standalone Hermes MCP server exists at `/root/.hermes/mcp_servers/hermes_mcp.py` exposing read-only governance tools (`hermes_system_status`, `hermes_epistemic_check`, `hermes_fact_check`, `hermes_cross_verify`, `hermes_plan_review`, `hermes_memory_steward`). Transport: streamable HTTP. Port: 18086.

These were originally embedded in arifOS kernel and extracted 2026-06-28 — they are diagnostic tools, NOT constitutional judgment tools.

**Status (verified 2026-07-04):** Server file exists and is importable, but is NOT registered in `~/.hermes/config.yaml` under `mcp_servers:`. The 6 configured MCPs are the organ ones (arifOS, A-FORGE, GEOX, WEALTH, WELL, OpenClaw). To activate hermes_mcp, add:

```yaml
mcp_servers:
  hermes:
    url: http://127.0.0.1:18086/mcp
    transport: streamable-http
    description: Hermes Agent — read-only governance diagnostics
```

Then `hermes --yolo gateway restart` to pick it up.

## Path symmetry: /root/.hermes ↔ /root/HERMES

`/root/HERMES` is a symlink to `/root/.hermes` — same content, two paths. File writes can land on either depending on which path the tool resolves. `ls -la` to confirm before relying on path-based cleanup or monitoring scripts. Don't try to "consolidate" the two — it's already one filesystem.

## Absorbed Federation Infra Fragments (2026-07-08)

5 standalone federation skills consolidated into this map.

| Fragment | Core Contribution | Status |
|----------|------------------|--------|
| `a2a-federation-builder` | A2A agent card format, federation mesh wiring, agent registration lifecycle | Absorbed |
| `aaa-cockpit` | AAA dashboard architecture, React component map, shadcn/ui primitives | Absorbed |
| `federation-observability` | Prometheus/Grafana config, health probe patterns, Netdata integration | Absorbed |
| `federation-safety-wiring` | Cross-organ safety interlocks, blast radius containment, denylist patterns | Absorbed |
| `federation-topology-map` | Organ port map, dependency graph, routing decision tree | Absorbed — see Six Active Organs table above |

**Provenance:** All 5 fragments archived 2026-07-08 to `.agents/skills/.archive-2026-07-08/`.

## OpenCode Model Resolution Reference

**IMPORTANT:** When troubleshooting `opencode run` model issues, load `references/opencode-model-resolution.md` FIRST. Model resolution has a precedence hierarchy where `agent[forge].model` override wins over top-level `model` field — this caused a 2-hour session of config changes before root cause was found.

```
1. agent[agent_name].model   ← overrides everything
2. opencode run --model FLAG
3. opencode.json model field
4. ~/.local/state/opencode/model.json
```

## References

- `references/multi-perspective-human-mapping.md` — when Arif needs strategic clarity about multi-person institutional dynamics. Ground claims in direct evidence (WhatsApp quotes, not inference). Per-person strategy, never lumped.
- `references/arifos-health-snapshot-2026-07-04.md` — full health envelope captured
  this session: build vs runtime drift, floor weights, capability map, ML/langfuse/
  token-pressure state. Use as baseline when probing "did arifOS drift since last
  audit?".
- `references/agentic-readiness-test-pattern.md` — 5-plane agentic readiness benchmark (Identity/Boundary/Authority/Epistemic/Flow). Self-reported scores are often inflated — probe `/tools/arif_verify` for real authority gate status. True score ~73 vs self-reported 81.2.
- Explorer protocol schemas at `/root/AAA/docs/schemas/` — knowledge-graph.schema.yaml (555-ASI nodes/edges), intent-route.schema.yaml (classify→route→verdict), explorer-packet.schema.yaml (OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY loop). Full spec in `apex-governance` skill → `references/explorer-protocol-schemas.md`.
- **A2A agent card normalization:** `references/a2a-agent-card-normalization.md` — the gateway strips custom constitutional fields through two independent stages (registry normalizer + discover response). Both must be patched to expose fields like `f1_boundary`, `bound_to`, `power_band`. Always restart `aaa-a2a.service` after card changes.
- **A2A protocol overview:** `references/a2a-protocol-overview.md` — what A2A is, governance (TSC, 8 companies), architecture (JSON-RPC 2.0, protobuf), key RPCs (`SendMessage`, `GetTask`, `SubscribeToTask`, etc.), task lifecycle states, A2A vs MCP comparison table, SDKs, and how arifOS implements it (AAA port 3001, 26 cards, constitutional extension, seal chain). Load when the conversation touches A2A as a protocol concept, not just operational card registration.
- **arifOS three-layer A2A model:** `references/arifos-three-layer-a2a-model.md` — doctrinal framing: Transport (A2A) → Governance (F1-F13/888_JUDGE) → Intelligence (Domain Agents). Explains how arifOS differs from standard A2A by inserting a constitutional gate between communication and action. META-MESA passed 8/8 because we govern the connection, not just enable it. Load when explaining the federation architecture to someone or comparing arifOS to standard A2A.
- **999 SEAL procedure:** `references/000-999-SEAL-PROCEDURE.md` — 11-stage pipeline, validity criteria, MCP transport notes, verified working 2026-07-10.


---

## §PROVENANCE · 2026-07-08 Consolidation

This skill absorbed core knowledge from **5** doctrine fragments during the skill library cleanup (Steps 1-4). Source fragments archived to `/root/.agents/skills/.archive-2026-07-08/`.

**Source fragments:**
  - `a2a-federation-builder` (archived 2026-07-08)
  - `aaa-cockpit` (archived 2026-07-08)
  - `federation-observability` (archived 2026-07-08)
  - `federation-safety-wiring` (archived 2026-07-08)
  - `federation-topology-map` (archived 2026-07-08)

**Full enrichment document:** [`references/consolidation-2026-07-08.md`](references/consolidation-2026-07-08.md) — detailed extraction of unique core knowledge from each fragment.

**F4 ΔS verified:** Entropy reduced — 5 fragments merged → 1 surfaced skill.
