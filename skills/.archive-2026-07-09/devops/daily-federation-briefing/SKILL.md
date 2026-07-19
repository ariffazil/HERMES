---
name: daily-federation-briefing
description: "Daily 7:30am MYT federation briefing — health, VAULT999 gossip, TODO queue, and federation newspaper"
triggers:
  - "daily briefing"
  - "federation briefing"
  - "morning briefing"
  - "daily report"
  - "federation newspaper"
  - "what happened yesterday"
  - "daily digest"
args: []
---

# Daily Federation Briefing

## When This Runs
- **Primary schedule:** Every day at 7:30am MYT (23:30 UTC previous day) — Telegram (DM with AGI🦞), newspaper style
- **Overnight cron variant:** runs ~15:00 UTC (23:00 MYT) as `overnight-research` cron — writes to `/root/memory/overnight-YYYY-MM-DD.md`, only escalates to Telegram if a CRITICAL finding needs Arif's attention before morning. The overnight brief is **log-only by default**; silence is a valid outcome. See `references/overnight-cron-output.md` (output shape + criticality gate) and `references/overnight-cron-data-collection.md` (cron-mode probes that work without an arifOS session envelope).

**Output decision tree (overnight variant):**
1. Write the full brief to disk regardless
2. If anything is CRITICAL (organ down, data loss risk, urgent decision): send ONLY the critical finding to Telegram
3. If NO critical findings: log only, do NOT send to Telegram. Silent completion is correct.

## Pre-Flight: Data Collection

Before composing the briefing, run the data collection script:
```bash
bash /root/.hermes/scripts/federation-briefing-data.sh
```
This provides: health status, VAULT999 recent entries, TODO queue, event logs, time context.

## Briefing Sections (in order)

### 1. 🌅 Good Morning Header
- Day, date, MYT time
- One-line "today in the federation" hook (interesting fact from the data)

### 2. ❤️ Federation Vitals
From health check data:
- Table: organ name | port | status (✅/❌)
- Note any degraded or down organs
- If all green, keep it short. If something's down, flag it prominently.

### 3. 📰 Federation Gossip
From VAULT999 recent entries + event logs:
- "What happened while you slept" — notable seals, verdicts, tool executions
- Highlight interesting patterns: many seals = busy night, errors = something broke
- If nothing happened, say so with personality ("The federation slept peacefully")
- Gossip angle: tease about which organs were busiest, any drama

### 4. 📋 Your Queue (TODO)
From TODO.md:
- 🔴 **Ready for you NOW** — items with no blockers, ready to execute
- ⏳ **Waiting on something** — blocked items with what they're waiting for
- ⏰ **Due today** — any items with today's deadline
- If queue is empty: "Your slate is clean. Rare. Enjoy it."

### 5. 💡 Today's Suggestion
Based on what you see in the data:
- If there's a backlog: suggest tackling the top item
- If health issues: suggest investigating
- If all clear: suggest a proactive improvement, exploration, or rest
- Keep it to ONE actionable suggestion

### 6. 📊 Optional: Federation Stats
Only if interesting:
- Most active organ in last 24h
- Seal count trend (busy vs quiet night)
- Any recurring patterns worth noting

## Style Guide
- Write like a **newspaper editor** — informed, slightly witty, concise
- Use Telegram Markdown: **bold**, `code`, tables
- Total briefing: 15-30 lines. Don't pad.
- If nothing interesting happened, own it — "Slow news day. The federation is healthy and boring."
- Add personality: "arifOS was up all night judging things", "GEOX slept like a rock"

## Edge Cases
- If health check fails: lead with that. "⚠️ Health check failed — here's what we know..."
- If TODO.md doesn't exist: skip the queue section gracefully
- If VAULT999 is empty: "No seals in 24h. The vault is quiet. Suspicious."
- If it's Monday: add "Weekly outlook" vibe
- If it's Friday: add "Weekend prep" vibe

## Pitfalls
- Don't hallucinate data — if the script didn't return it, say "no data"
- Don't alarm on single errors — contextualize ("1 error in 500 events = normal")
- Don't suggest dangerous actions without 888_HOLD context
- Don't make the briefing longer than 30 lines — brevity is the soul of wit
- **Probe vs. actual outage:** if a cron health probe logs `HTTP 000000` for a service, verify with `pgrep -af <name>` and `ss -ltn` before declaring an outage. Some "services" (e.g. OpenClaw, opencode-bot) are Python bots, not HTTP daemons — the probe is wrong, the service is fine. Mark as "false alarm, measurement bug" not "outage".
- **"YELLOW" is not an outage.** arifOS `/health` returns `runtime_drift: true` when the container image is behind live code. That's a known state, not an emergency. Same for `tool_registry.json` count mismatches with `matches_canonical: false` when the divergences are F13-ratified (internal tools hidden by design).
- **Don't write Telegram content first.** For the overnight variant, write the file first, decide criticality second. Avoids polluting Telegram with low-signal alerts when a structured disk log is enough.
- **Dual-VAULT architecture trap (verified 2026-07-08).** Two vault ledgers exist on the VPS:
  - `/srv/arifos/VAULT999/SEALED_EVENTS.jsonl` — DORMANT (last activity 2026-04-21, ~3 months stale). Has the canonical `SEALED_EVENTS` schema but no new writes. Grepping this for "today's seals" will always report "no activity."
  - `/root/.local/share/arifos/vault999/seal_chain.jsonl` — ACTIVE. Uses `seq`/`actor`/`verdict`/`hash` schema. Has the seal chain head at `seal_chain_head.json`.
  Always probe the active ledger first; the dormant one is historical context only.
- **MCP policy-gate fallback (verified 2026-07-08).** arifOS and A-FORGE MCPs return `PolicyGateError: L1_IDENTITY:anonymous_actor` when called from a cron (no session envelope, no lease). The MCP is not broken — the cron has no identity. **Fallback ladder, in order:**
  1. `curl http://127.0.0.1:<port>/health` — works without auth, returns full state
  2. `journalctl -u <service> --since "24 hours ago"` — event log
  3. Direct file reads: `/root/.local/share/arifos/vault999/seal_chain.jsonl`, `/root/WELL/state.json`, `/var/arifos/artifacts/outbox/`
  4. `git log --since="24 hours ago"` per repo
  Do NOT retry the MCP call — it will fail identically every 60s.
- **WELL `state.json` TEST-mock truth (verified 2026-07-08).** The WELL organ can report `freshness: expired, age_seconds: 6015728` (70 days) on `/health` while the service is healthy. This is because `/root/WELL/state.json` is a TEST mock (`environment: TEST, reason: "Mocked healthy state for test session"`). The MCP-level "RED" is the freshness band, not a service outage. Always read the state file directly before treating WELL staleness as a real finding.
- **litellm-proxy env-file recovery (verified 2026-07-08).** The LLM failover gateway reads from `/root/.secrets/{qwen,a-forge,mimo,bailian-payg,...}.env`. If any wrapper file is missing, systemd fails with `Failed to load environment files: No such file or directory` and `Restart=always` puts the service in a 5s-loop (71k+ restarts in 3h observed). The actual API keys live in `/root/.secrets/vault.env` and are intact. Recovery: `cp /root/.secrets/archive-YYYYMMDD/<missing>.env /root/.secrets/ && systemctl restart litellm-proxy.service`. 30-second fix, NO new secrets needed. **Verify with `journalctl -u litellm-proxy.service --since "5 min ago" | grep -c "Failed"` after — should drop to 0 within 30s.**
- **15min-clean-restart pattern ≠ outage (verified 2026-07-08).** A service may restart on a strict ~15-minute cycle with no crash trace (`Deactivated successfully` + clean startup). This is a managed external killer (likely a healthcheck SIGTERM or self-restart hook), not a self-failure. Don't escalate as CRITICAL. Note the cadence in the brief as "MONITOR" and check the originating killer next session. Verified pattern: AAA :3001, 13 restarts/24h, no panic.
- **1mcp 2min watchdog + partial MCP load = degraded, not down (verified 2026-07-09).** The 1mcp aggregated MCP runtime on :3050 uses `WatchdogSec=2min` and restarts on timeout — produces 100-400+ restarts/24h with a tight 2-minute cadence in journalctl. **This is by design, not an outage.** What matters is the success rate of child MCP servers reported at boot: `13/15 servers ready (86.7%)` means the service is **degraded but usable**. Known persistent failures across runs: `minimax-code`, `minimax-media` (vendor MCP servers, not federation organs — fix is upstream/vendor, not local). **Do not flag as CRITICAL.** Note in brief as `🟡 DEGRADED — 13/15 servers, X restarts/24h` and move on. Recipe:
  ```bash
  systemctl show 1mcp.service -p NRestarts
  curl -s http://127.0.0.1:3050/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'status={d.get(\"status\")} uptime={d.get(\"system\",{}).get(\"uptime\")}')"
  journalctl -u 1mcp.service --since "5 min ago" | grep -c "MCP loading complete"
  ```
- **Recovery verification pattern — ActiveEnterTimestamp beats restart count (verified 2026-07-09).** When a service was previously CRITICAL and is now GREEN, the proof of recovery is: (1) `ActiveEnterTimestamp` shows continuous uptime since the fix event, (2) `curl /health` returns 200, (3) `journalctl --since "<fix-event>"` shows 0 `Failed`/`Main process exit` lines. Yesterday's overnight said `litellm-proxy DOWN 71k restarts`; today's verification was: `ActiveEnterTimestamp=Thu 2026-07-09 08:21:10 +08` (14.7h stable) + `curl :4000/health/liveliness` → 200 "I'm alive!" → **GREEN confirmed**. The `NRestarts=0` field after restart is by definition reset — it tells you nothing about whether the original outage is fixed. Always verify via uptime + health probe, not the counter. Recipe:
  ```bash
  systemctl show litellm-proxy.service -p ActiveEnterTimestamp,SubState
  curl -s --max-time 3 http://127.0.0.1:4000/health/liveliness
  ```
- **arifOS MCP /mcp is reachable via direct JSON-RPC POST (verified 2026-07-10).** `MEMORY.md` may carry a stale entry "arifOS MCP /mcp broken — transport refused" — that is **outdated**. The endpoint returns HTTP 200 on `POST /mcp` with `Content-Type: application/json` + `Accept: application/json, text/event-stream` headers. Tool *invocation* still fails (`PolicyGateError: L1_IDENTITY:anonymous_actor`), but `tools/list` works — useful for verifying canonical tool surface and catching `tool_registry.json` desync. Recipe:
  ```bash
  curl -s --max-time 5 -X POST http://127.0.0.1:8088/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | head -c 500
  ```
  Detail in `references/overnight-cron-data-collection.md` §11.
- **Stale-memory reconciliation (verified 2026-07-10).** When MEMORY.md or carry-forward-*.md claims something is broken, verify against live state before echoing it into the brief. The cron is the periodic ground-truth check that catches drift between what the agent *remembers* and what the system *actually* looks like. Three stale claims caught on 2026-07-10: "MCP /mcp broken", "arif_verify NOT built", "WELL stale" (the last was correct but contextually wrong — F6 boundary means YELLOW is expected, not a regression). Add a "stale memory" section to the brief when found.
- **carry_forward.json identity_drift probe (verified 2026-07-10).** `/root/.local/share/arifos/carry_forward.json` carries `identity_drift` + `next_safe_action` fields. Healthy = `identity_drift=PASS`, `next_safe_action=PROCEED_OR_SABAR`. Anything else (DRIFT/UNKNOWN) goes into Critical Findings — `DRIFT` may be intentional per F13 sovereignty signal (check the carry-forward note). Detail in `references/overnight-cron-data-collection.md` §13.
- **arif_init(mode=...) valid mode names (verified 2026-07-09).** Calling `mcp__arif_fazil__arif_init(mode='preflight')` returns `"Unknown mode: preflight"` with `allowed_modes: [init, light, resume, validate, epoch_open, epoch_seal, opt_out, opt_out_profiling]`. The `preflight` and `triage` modes are exposed via `arif_triage`, not `arif_init`. Don't call `arif_init` for preflight — call `arif_triage(mode='preflight'|'status'|'triage')` instead. From a cron (no identity), the result is `HOLD` with `actor_verified: false` regardless of mode — the cron-mode fallback is filesystem probes, not MCP.
- **Tavily API 432 → Google News RSS fallback (verified 2026-07-18).** When `web_search` and `web_extract` both fail with Tavily 432 (quota exhausted), switch IMMEDIATELY to Google News RSS via curl. Do NOT retry Tavily — 432 means quota, not transient. Recipe: `curl -s --max-time 10 "https://news.google.com/rss/search?q=<query>&hl=en-MY&gl=MY&ceid=MY:en" | grep -o '<title>[^<]*</title>' | sed 's/<[^>]*>//g'`. For structured extraction with pubDate: pipe raw RSS into `python3 -c "import sys,re,html; ..."`. Note: some queries (geopolitics, AI) may return empty — Google RSS filters by query specificity. Browser is third fallback but news portals often time out at 10s+.
- **WEALTH MCP data-staleness traps (verified 2026-07-18).** Two WEALTH tools return stale/misleading data: (1) `capital_market(mode='commodity', commodity='brent_crude')` — source tag "EIA estimate", can lag days behind live trading. Cross-verify oil prices with news RSS. (2) `capital_diagnose(mode='stress_index')` — returns stress_index=0.0 (GREEN) with "SILENT_DEFAULT_RISK: 16 expected fields absent" when fields aren't populated. GREEN = "no data supplied," not "low stress." Report as UNK, not GREEN.

## Data Collection Recipes

**Federation health (replace the bundled script with these probes when it fails):**
```bash
# All organs at once (port reachability)
for port in 8088 8081 18082 18083 7071 7072 3001; do
  curl -s --max-time 3 "http://127.0.0.1:$port/health" | head -c 200
  echo " — :$port"
done

# arifOS deep probe (surface_consistency, runtime_drift, tool_registry)
curl -s http://127.0.0.1:8088/health | python3 -m json.tool | grep -E "runtime_drift|source_commit|live_commit|divergences|tool_count"

# Process truth (last resort — confirms "is it actually running")
for p in 8088 8081 18082 18083 7071 7072 3001; do
  pid=$(ss -ltnp 2>/dev/null | grep ":$p " | grep -oP 'pid=\K[0-9]+' | head -1)
  [ -n "$pid" ] && cat /proc/$pid/comm 2>/dev/null && echo " → :$p"
done
```

**VAULT999 "what was sealed today":**
```bash
# Last 5 chain entries
tail -5 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    print(f\"seq={d.get('seq')} | {d.get('epoch')} | {d.get('verdict')} | {d.get('actor')}\")
"

# Today's seal files (discrete artifacts, not chain)
ls -lat /root/.local/share/arifos/vault999/seals/ | head -5
```

**Git activity across all organs (24h):**
```bash
for repo in /root/arifOS /root/GEOX /root/wealth /root/WELL /root/A-FORGE /root/AAA /root/arif-sites; do
  cd "$repo" && [ -d .git ] && echo "=== $repo ===" && git log --oneline --since="24 hours ago" | head -5
done
```

**Hermes health log (false-alarm filter):**
```bash
# Most recent probes — if "openclaw HTTP 000000" appears 3+ times consecutively,
# check if openclaw is a bot, not HTTP. Don't page Arif.
tail -30 /var/log/hermes-health.log
```

**arifOS MCP /mcp direct POST probe (verified 2026-07-10):**
```bash
# Transport layer IS reachable. MEMORY.md claim "arifOS MCP /mcp broken" is stale.
curl -s --max-time 5 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | head -c 500
# → HTTP 200 with full 12-tool canonical manifest
# Tool INVOCATION still fails (PolicyGateError L1_IDENTITY) — only list/discovery works for cron
```

**carry_forward.json identity drift probe (verified 2026-07-10):**
```bash
cat /root/.local/share/arifos/carry_forward.json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(json.dumps({k: v for k, v in d.items() if k in ['identity_drift', 'next_safe_action', 'created_at', 'note']}, indent=2))
"
# Healthy: identity_drift=PASS, next_safe_action=PROCEED_OR_SABAR
# DRIFT may be intentional per F13 — check carry-forward note. UNKNOWN is real concern.
```

**Extended cron-mode recipes** (sections 11-13: MCP transport probe, stale-memory reconciliation, carry_forward.json) live in `references/overnight-cron-data-collection.md`.
