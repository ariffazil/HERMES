# Entropy Watch Resolution — Session Reference

> **Source session:** 2026-07-29 04:00 MYT entropy watch
> **Instrument:** Hermes (DeepSeek-v4-Flash) → OpenCode via delegate_task
> **Proven pattern:** Cron delivery → probe → commit → route → defer → seal

## Full Resolution Flow

### Step 1: Cron Delivery
Entropy watch reported:
- 🟡 A-FORGE: 1 dirty file
- 🟡 AAA: 3 dirty files
- 🟠 WELL: WELL_HOLD (age: 4.0h)
- PETRONAS article link

### Step 2: Probe & Diagnose
```bash
# Dirty repo scan
for d in /root/{A-FORGE,AAA}; do echo "=== $d ==="; git -C "$d" status --short; done

# Diff inspection (must understand scope before committing)
git -C /root/A-FORGE diff deploy/af-forge/docker-compose.well.yml
git -C /root/AAA diff registries/opencode_toolbench.yaml

# WELL health
curl -sf http://127.0.0.1:18083/health | jq '{status, well_signal, state_age_hours}'
```

**Findings:**
- A-FORGE: Volume mount `/root/well` → `/root/well-runtime` (1-line T1)
- AAA: Toolbench registry update (v1.18.3→1.18.9, 4→7 agents) + 2 new ontology files (243L, 321L)
- WELL: `degraded`/`WELL_OPERATOR_PRESENT` = normal baseline (SELF-REPORT mode)
- WEALTH organ: healthy on :18082, but MCP bridge glitchy

### Step 3: Article Extraction
Use `mcp__hound__mcp_smart_fetch` (not web_extract — SearXNG can't extract content).

**Edge Malaysia 2026-07-28:** PETRONAS subsidy bill may hit RM40B (+85% vs Budget RM21.6B), dividends rise to ~RM33.5B, Brent US$92.50 actual vs $65 Budget, fiscal deficit 3.8% vs 3.5%.

### Step 4: Commit Dirty Files (T1 Auto)

**A-FORGE:**
```
ea7a0fc4 fix(well): update volume mount path from well to well-runtime
```

**AAA:**
```
5c9cccd8 feat(registry): add OpenCode ontology and toolbench contrast, update toolbench yaml
```

Both repos confirmed clean after commit.

### Step 5: Route to Domain Organs
`arif_route(intent=..., organ=wealth)` — routed PETRONAS subsidy analysis to WEALTH.

**Known blocker:** WEALTH MCP `capital_market` / `wealth_institutional_stress_index` tools returned unreachable despite organ health endpoint responding. Workaround: saved structured data to `forge_work/<date>/rsi/petronas-wealth-deferred.md`.

### Step 6: Delegate-to-OpenCode
Arif said "Spawn Open Code to Setel all that." Used `delegate_task` with full session context. Subagent handled git commits, organ routing, and seal attempt autonomously.

### Step 7: Seal
`arif_seal` blocked at constitutional gate: "L5 irreversible — requires F13 Ed25519 identity binding." Workaround: save seal receipt to `forge_work/<date>/rsi/entropy-seal-receipt-<date>.md`.

### Known WEALTH MCP Bridge Glitch (2026-07-29)
- WEALTH organ: `systemctl status wealth-organ` → active, 10h uptime
- WEALTH health: `curl :18082/health` → `{"status":"healthy"}`
- WEALTH MCP tools: `capital_market`, `wealth_institutional_stress_index` → "MCP server 'wealth' is unreachable after 4 consecutive failures"
- gas-api.service and oil-api.service: both active/running
- Likely: MCP bridge process disconnected from Hermes without organ restart

**Diagnosis command:**
```bash
systemctl status wealth-organ  # check organ
curl -sf http://127.0.0.1:18082/health | jq .  # check health endpoint
# MCP bridge may need restart even if organ is healthy
```

### Seal Block Pattern
`arif_seal` returns `hold_required: true, hold_reason: "L5 irreversible action or confidence < 0.5", agency_level: "L5_EXECUTE_IRREVERSIBLE"` when called from an anonymous/observer session. The kernel requires:
1. `arif_init(mode=init, actor_id=..., requested_authority=...)` with Ed25519 signature
2. Or a session_token from a properly bound session

This is F13 working as designed — irreversible actions need sovereign identity.
