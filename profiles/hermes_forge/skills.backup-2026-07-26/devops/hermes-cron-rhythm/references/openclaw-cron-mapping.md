# OpenClaw Cron Mapping — Observatory vs Actuator

> Relationship between Hermes cron (observatory/reporting) and OpenClaw cron (actuator/repair).

## Architecture Split

| Layer | Platform | Role | Delivery |
|-------|----------|------|----------|
| Observatory | Hermes | Reads state, interprets, briefs Arif | Telegram DM (human) or AAA group (alerts) |
| Actuator | OpenClaw | Reads state, acts, repairs, restarts, promotes | AAA group via AGI_ASI_bot |

**Key insight:** Hermes tells you WHAT. OpenClaw DOES something about it. They don't duplicate — they complement.

## OpenClaw Job Map (verified 2026-07-12)

| Job | Schedule | Delivery | Status | Overlap with Hermes |
|-----|----------|----------|--------|---------------------|
| WELL freshness 12h | */12h | none→AAA | 🟢 ok | morning-brief WELL pulse (READ); this WRITES to memory |
| INTEL · Intelligence Pulse | 14:00 MYT | announce→AAA | 🟢 ok | daily-news-briefing (external); this is INTERNAL signal detection |
| AF-FORGE Infrastructure Sentinel | */6h UTC | none→AAA | 🟢 ok | drift-alert (organ TCP); this checks deeper (Docker, services) |
| JWT-violations-monitor | daily | none→AAA | 🟢 ok | NONE — unique security monitoring |
| STEEL · Machine Steel Pulse | 22:00 MYT | announce→AAA | 🟢 ok | morning-brief (reports); this AUTO-RESTARTS failed services |
| Memory Dreaming Promotion | 03:00 MYT | announce→AAA | 🟢 ok | NONE — OpenClaw internal memory management |
| SILICA · Code Governance Pulse | 06:00 MYT | announce→AAA | 🟢 ok | NONE — workspace code governance |
| MCP Lifeguard Probe | 09:00 MYT | none→AAA | 🟢 ok | drift-alert (organ TCP); this RESTARTS broken MCPs |
| FORGE ⟁ Weekly Governance Roll-up | Sat 19:00 MYT | announce→AAA | 🟢 ok | weekly-deep-brief (system review); this aggregates internal receipts |

## Delivery Routing

All OpenClaw jobs deliver to AAA group (`telegram:-1003753855708`) via AGI_ASI_bot.

Two delivery modes:
- **announce** — agent's final response goes to AAA group directly
- **none** — only sends when agent explicitly calls the `message` tool (NO_REPLY = silent)

Both routes use the OpenClaw Telegram bot (AGI_ASI_bot), NOT the Hermes bot.

## Overlap Analysis

Functions where BOTH Hermes and OpenClaw have jobs:

| Function | Hermes (report) | OpenClaw (act) |
|----------|----------------|----------------|
| WELL health | morning-brief WELL pulse | WELL freshness 12h |
| Infrastructure | drift-alert | AF-FORGE Sentinel |
| MCP health | drift-alert | MCP Lifeguard Probe |
| System review | weekly-deep-brief | FORGE Weekly |

Functions unique to OpenClaw (no Hermes equivalent):
- JWT violation monitoring
- Code governance (SILICA)
- Memory promotion (Memory Dreaming)
- Internal signal detection (INTEL)
- Service auto-restart (STEEL)

## Constitutional Boundary

- Hermes jobs = OBSERVATORY only (constitutional scope header on all scripts)
- OpenClaw jobs = ACTUATOR (can restart services, write to memory, run probes)
- Both are subordinate to arifOS kernel (F1-F13) and sovereign veto (F13)
- OpenClaw is NOT a "parallel constitution" — it's the actuator layer under one constitution

## Diagnosing Failing OpenClaw Jobs

When an OpenClaw job shows `error` status:
1. `openclaw cron runs --id <jobId> --limit 3` — check recent run history
2. Look at `cause` field: timeout, LLM request failed, context overflow
3. Check `lastDiagnosticSummary` for the specific failure
4. Common fixes: reduce prompt size, increase timeout, fix script path, check model availability

### Proven Fixes (2026-07-12)

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `job execution timed out (last phase: model-call-started)` | timeoutSeconds=60 too short for LLM+MCP | `--timeout-seconds 180` (or 600 for complex jobs) |
| `LLM request failed` | model/provider down (e.g. bailian-token-plan/deepseek-v4-pro) | `--model minimax/MiniMax-M3` + `--fallbacks` |
| `Context overflow: prompt too large` | workspace 37KB + prompt > model context window | `--light-context` + larger-context model (`minimax/MiniMax-M3`) |

**Key learning:** OpenClaw workspace AGENTS.md alone is 13KB. With SOUL.md, MEMORY.md, USER.md, TOOLS.md = ~37KB total. Jobs using smaller-context models (deepseek-chat 64K) often overflow. Use `--light-context` to skip workspace bootstrap, or switch to `minimax/MiniMax-M3` (larger context).

### Delivery Mode Semantics

- `announce` → agent's final response sent to target channel. NO_REPLY suppressed.
- `none` → only sends when agent explicitly calls `message` tool. NO_REPLY = silent.
- Both modes respect NO_REPLY token suppression — "NO_REPLY" in agent output = no message sent.

### Model Override for Cron Jobs

```bash
# Switch model
openclaw cron edit <jobId> --model "minimax/MiniMax-M3"

# Add light-context (skip workspace bootstrap)
openclaw cron edit <jobId> --light-context

# Increase timeout
openclaw cron edit <jobId> --timeout-seconds 600

# Set delivery
openclaw cron edit <jobId> --announce --channel telegram --to "-1003753855708"

# Manual test run
openclaw cron run <jobId>
```
