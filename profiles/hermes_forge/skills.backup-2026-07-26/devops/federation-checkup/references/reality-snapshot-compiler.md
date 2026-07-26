# Reality Snapshot Compiler

**Script:** `/root/scripts/reality_snapshot.py` on af-forge (100.64.0.2)
**Cron (ingestion):** `b585201442ca` — 15-min, `no_agent: false`, polls S24, appends to JSONL
**Cron (alerting):** `49d171deeb6d` — 10-min, `no_agent: true`, script-based anomaly detection
**Telemetry source:** `/root/arifos-memory/telemetry/s24_history.jsonl` (polled by cron, consumed by compiler)
**Output:** `/root/forge_work/YYYY-MM-DD/reality_state.md` (markdown) or `--json` for machine-readable
**Purpose:** Produce immutable federation reality artifacts for cloud AI ingestion.
**Ontology:** F2 (Truth) | F12 (Anti-Injection) | F1 (Safety)
**Forged:** 2026-07-24 | Patched: 2026-07-24 (dual pipeline + output path + script name corrected)

## Architecture

The compiler reads local telemetry + probes FLOW via SSH. It does NOT poll S24 directly — it reads the JSONL that the cron pipeline already maintains:

| Source | Method | Data |
|--------|--------|------|
| S24 telemetry JSONL | Read local file (walk backwards past timeout entries) | Battery, temp, charging, health, uptime |
| FORGE organs | HTTP GET `localhost:<PORT>/health` | All 6 organ health endpoints |
| FLOW (100.64.0.4) | SSH read-only commands | System load, disk, memory, UFW rules, Tailscale peers, Caddy, open ports |

All SSH commands are non-mutating: `uptime`, `free -h`, `df -h /`, `ufw status verbose`, `tailscale status`, `systemctl is-active caddy`, `ss -tlnp`.

## Epistemic Bridge Pattern — "Truth Without Vector"

Cloud AI agents (Gemini, ChatGPT, Claude) have no persistent network — they can't SSH or curl into the mesh. The compiler bridges this gap via the **deterministic windows** pattern:

- Agents receive **timestamped live evidence** (F2 Truth) as immutable markdown/JSON context
- Agents have **zero mutation capability** (F12 Anti-Injection) — no shell, no credentials, no access
- Every value carries the epistemic tag `OBS` (live probe) — verifiable, not inferred
- The compiler is **not a cron job itself** — it reads from the telemetry JSONL that the dual-pipeline cron maintains (10-min alert + 15-min ingest)
- No AI agent runs inside the compiler — pure data collection, zero inference

**Three-tier epistemic architecture (from FLOW identity contract):**
1. **MCP Proxy via FORGE** (Option 1) — Tool-call-based, real-time, for local agent runtimes. Not yet deployed (requires NATS infrastructure).
2. **Reality Snapshot Compiler** (Option 2) ← THIS. Compiled on-demand, reads live state, zero public exposure. Human copies artifact into cloud chat.
3. **Hardened HTTP Endpoint** (Option 3) — Public REST API, token-protected. Not yet deployed (requires SCT gate + rate limiting).

## Usage

```bash
# Human + AI readable markdown (default)
python3 /root/scripts/reality_snapshot.py

# Machine-readable JSON
python3 /root/scripts/reality_snapshot.py --json

# Save to dated forge_work directory
python3 /root/scripts/reality_snapshot.py --output /root/forge_work/$(date +%Y-%m-%d)/reality_state.md

# Feed to cloud AI: copy-paste entire artifact as system prompt or first message
```

## Output Structure

The artifact contains 5 sections:
1. **S24 Sovereign Sensing Node** — battery%, charging state, temp°C, health, uptime, warnings
2. **FORGE Central Intelligence** — all 6 organ health endpoints with status + version table
3. **FLOW DMZ Edge Gateway** — SSH reachability, uptime, memory, disk, Caddy, UFW status, Tailscale mesh
4. **Federation Health Summary** — aggregate organ count, S24 status color, FLOW reachability
5. **Isolation Contract Verification** — documented boundary matrix (FORGE→S24, FLOW→FORGE, FLOW→S24, etc.)

## Resilience

- S24 telemetry walks backwards through JSONL past timeout entries to find last valid data point
- FLOW SSH failures degrade gracefully — `uptime` field shows `SSH_FAILED`, remaining fields partial
- arifOS :8088 has a known ~12s cold response time — compiler allows 15s timeout
- WELL returns `degraded` when biometric feed is stale (>12h since last watchdog injection)
- All data paths checked for existence before access; missing organs show `down` not crash

## Pitfalls

- **Script name is `reality_snapshot.py`, not `forge_reality_snapshot.py`.** The original name had a `forge_` prefix that was dropped before deployment. Always use `/root/scripts/reality_snapshot.py`.
- **The compiler is NOT a cron job.** It reads from the telemetry JSONL that the dual-pipeline cron maintains. Run it on-demand when Arif needs a snapshot for cloud AI ingestion. The cron jobs (`b585201442ca` + `49d171deeb6d`) handle the data collection; the compiler handles the formatting.
- **S24 "unreachable" during deep sleep is a design feature, not a bug.** The S24 is a passive sensor in a SCADA-like data diode architecture. It sleeps between poll cycles; the compiler reads the JSONL (which walks backwards past timeout entries) rather than probing live. This is industrial telemetry logic, not consumer app behavior.
- **arifOS :8088 has ~12s cold-start response.** The compiler allows 15s timeout. If arifOS shows `down` but the process is running, retry with a longer timeout.
- **FLOW :8080 returns arifOS health data (not FLOW-specific).** This is expected — arifOS MCP runs on FLOW. The isolation contract means FLOW can't reach FORGE, but FLOW's own arifOS instance is healthy.
