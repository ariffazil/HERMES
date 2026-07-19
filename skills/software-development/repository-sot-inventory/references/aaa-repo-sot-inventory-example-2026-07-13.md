# AAA Repo SOT Inventory — Example (2026-07-13)

This is a concrete example of a repository SOT inventory for an agent governance/cockpit repo. It demonstrates the agent card inspection, federation topology extraction, hardcoded state detection, and schema default auditing techniques.

## Git State

- **HEAD:** `b444eb4a` — "chore(mesa-test-agent): add canonical dash-named pubkey + AGENTS.md key-handling table update"
- **Branch:** `refactor/apex-entropy-20260712` (active, 3 local branches + 7 remotes)
- **Dirty:** 1 file deleted — `FEDERATION_CONTRACT.md.bak.pre-pointer-2026-07-12` (84-line backup removed, content: federation position doc showing organ hierarchy Arif→arifOS→domain organs→AAA→A-FORGE→VAULT999)

## Package Identity

- **Name:** `aaa-control-plane` v2026.06.23, AGPL-3.0
- **Stack:** React 19, TypeScript ~6.0, Vite 8, Tailwind 4, shadcn/ui, Express 5.x
- **Key deps:** lucide-react, recharts, zod, supabase, cmdk, sonner

## Federation Topology

| Code | Port | Role | Status | Notes |
|------|------|------|--------|-------|
| A | 3001 | AAA_A2A_GATEWAY | LIVE | organId: aaa |
| K | 8088 | KERNEL_arifOS | LIVE | organId: arifos |
| F | 8700 | AFORGE_A2A | REGISTERED | live_mcp: 7072, live_health: 7071 |
| W | 18082 | WEALTH | LIVE | organId: wealth |
| L | 18083 | WELL | DEGRADED | organId: well |
| G | 8400 | GEOX_A2A | optional | live_mcp: 8081 |
| P/T/V/E/M | 8100-8600 | Various | optional | VTALS_BRIDGE, MESH, etc. |

Dependency chain (from `explorer_federation_registry.json`): GEOX→WEALTH→WELL→A-FORGE

## Agent Cards & Registry

**Warga lane cards** (schema v2.2.0):
- **333-AGI** (Δ MIND) — 10 reasoning + kernel skills, runtime port 18789 (openclaw)
- **555-ASI** (Ω HEART) — 4 skills (ethical critique, memory synthesis, anti-beautiful-one)
- **888-APEX** (ΦΙ JUDGE) — 9 skills (constitutional arbitration, hold protocol, FFF loop)
- **777-FORGE** — **RETIRED 2026-07-02**, subsumed by 333-AGI per HEXAGON v2.1.0
- A-AUDIT, A-ARCHIVE — support lanes

**External agents:** 18 agent directories including hermes-asi, openclaw, opencode, makcikgpt, and 10 FI forge instruments (claude-code, codex, kimi-code, aider, antigravity, gemini-cli, grok-build, copilot, qwen-code, continue-cli)

**Registry files:**
- `a2a-server/agent-card-registry.js` — dynamic loader, auto-scans `agent-cards/`
- `a2a-server/explorer_federation_registry.json` — dependency graph (GEOX→WEALTH→WELL→A-FORGE)
- `a2a-server/organ-affinity-index.json` — 8 organs with affinity tags and branch counts
- `a2a-port-map.json` — port/role/status map (forged 2026-07-10)

**AGENT_REGISTRY.md** — 401 lines. Contains SCAR-13 documenting category errors (organs mislabeled as agents). Lists ~24 true agents + 6 capability registries + 6 legacy = 36 total entries.

**Public:** `public/a2a/agents.json` v2.1.0 (HEXAGON + WITNESS), sealed HEXAGON-AGENTS-FORGE-20260602

## Hardcoded State Findings

### `GREEN` as literal string

| File | Line | Pattern | Category |
|------|------|---------|----------|
| `src/Cockpit.tsx` | 674 | `health === 'ok' ? 'GREEN' : 'RED' : 'YELLOW'` | Hardcoded status |
| `src/components/cockpit/RealityConsole.tsx` | 36,126,220,231,342 | organ health + overallVerdict + `band \|\| 'GREEN'` | **Default (nullish coalesce to GREEN)** |
| `src/components/cockpit/AgentModelPanel.tsx` | 78,152 | `drift_state?: 'GREEN'` | Type definition |
| `src/envelope.ts` | 103 | `readiness_color?: 'GREEN' \| 'YELLOW'` | Type definition |
| `src/gateway/arep-types.ts` | 84 | `AutonomyBand = 'GREEN' \| ...` | Type definition |
| `a2a-server/server.js` | 2462 | `drift_state: 'GREEN'` | **Hardcoded response** |
| `a2a-server/arep-task-manager.js` | 102,256 | `status: healthy ? 'GREEN' : 'RED'` | Acceptable (live-probed) |
| `schemas/arep-task.schema.json` | 100-101 | `"default": "GREEN"` | **Schema default — flag** |
| `schemas/arep-example-forge-integration.json` | 41 | `"autonomy_band": "GREEN"` | Example file |
| `docs/architecture/UNIFIED_AGENT_B.md` | 93 | `"risk_tier": "GREEN"` | Example in doc |
| `telegram-miniapp/app/src/pages/WellPage.tsx` | 80 | `readiness.color === "GREEN" ? "✅"` | Acceptable (display logic) |

### `SEAL` as literal string

| File | Line | Pattern | Category |
|------|------|---------|----------|
| `src/envelope.ts` | 116 | `verdict?: 'SEAL' \| 'HOLD'` | Type definition |
| `src/gateway/deliberation.ts` | 48,124,372,374,384 | `VerdictType` + conditional logic | Type + verdict engine |
| `src/gateway/arep-types.ts` | 115 | `GovernanceVerdict = 'SEAL' \| ...` | Type definition |
| `src/adapter/router.ts` | 97 | `data.judge?.verdict === 'SEAL' ? 'LOW'` | Verdict routing |
| `src/components/cockpit/ArifOSReceiptViewer.tsx` | 37,84 | verdict label display | Display logic |
| `src/components/cockpit/SupabaseMemoryPanel.tsx` | 98,198 | `s.verdict === 'SEAL' ? 'text-emerald-400'` | Display logic |
| `src/components/cockpit/RealityConsole.tsx` | 537 | `verdicts.filter(v => v.verdict === 'SEAL')` | Display logic |

### Key Concerns

1. **Schema default `"autonomy_band": "GREEN"`** — First render of any task/agent will show GREEN even if no probe has run. This masks probe failures.
2. **`const band = task?.autonomy_band || 'GREEN'`** in RealityConsole.tsx line 342 — nullish coalesce to GREEN means any task missing autonomy_band gets displayed as GREEN.
3. **`drift_state: 'GREEN'` hardcoded** in server.js response — the server always reports GREEN drift regardless of actual state.
4. **WELL organ status DEGRADED** in port map — organ is marked degraded but not why.

## Key State Files

- `wire_state_lineage.json` — verdict→A2A wire mapping (SEAL→COMPLETED, HOLD→INPUT_REQUIRED, VOID→REJECTED)
- `arif_desired_behaviors.json` — F1-F13 positive behavior map
- `haram_enforcement.json` — forbidden behaviors with verdicts (F9_ANTIHANTU, F13_CAPABILITY_REFUSAL, F5_PEACE_HARM, etc.)
- `seal_chain.js` — v2.0.0 enriched envelope format, hash-chained, writes to `/root/VAULT999/seal_chain.jsonl`

## Notable Observations

1. **No Observatory directory** — confirmed absent. Observability configs live in `observability/` (Grafana/Prometheus)
2. **777-FORGE retired** (2026-07-02), subsumed by 333-AGI
3. **WELL organ DEGRADED** — likely impacts readiness checks for A-FORGE execution
4. **`public/status.json` stale** — build_hash `c1d451b` doesn't match HEAD `b444eb4a`
5. **3 schema-level optimism risks** — autonomy_band defaults to GREEN in schema, nullish coalesce to GREEN in code, drift_state hardcoded GREEN in server
