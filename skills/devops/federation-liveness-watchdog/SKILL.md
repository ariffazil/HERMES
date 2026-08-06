---
name: federation-liveness-watchdog
description: >-
  Build and operate OBSERVE_ONLY federation liveness monitoring — determining whether
  an agent, organ, or compute service is alive (process → endpoint → semantic → trace),
  the 5-bit Alive Vector, the DEAD/DORMANT/ZOMBIE/DEGRADED/ALIVE verdict grammar,
  the agent_liveness.json artifact, and the systemd timer deployment pattern.
category: devops
forged: 2026-08-01
---

# Federation Liveness Watchdog — arifOS Federation

> **Purpose:** answer "is this agent/organ/compute actually alive?" — as a single
> truth artifact, automatically, without trusting HTTP 200 alone.
> **Authority:** OBSERVE_ONLY. Never restarts, repairs, rolls back, or seals.
> **Artifact:** `/var/lib/arifos/agent_liveness.json` | **Timer:** every 5 min

## When to Use This Skill

- "How do we know if an agent/code/compute is alive?" (the liveness question)
- Building, extending, or debugging `federation-watchdog`
- Adding a new organ/service to the probe registry
- Distinguishing "process is running" from "agent is doing useful work"
- Wiring liveness telemetry into WELL or other consumers

## Core Doctrine: "Running" ≠ "Alive"

systemd answers only *is the body breathing*. It does NOT answer *is the mind awake*.
A service can be `systemctl active` ✅ + `/health` 200 ✅ + tools listed ✅ yet be
stale, silent, or producing garbage. Liveness is layered:

| Layer | "Alive" means | Witness |
|---|---|---|
| Process | PID/service active, not crashed | `systemctl is-active` |
| Endpoint | `/health` responds | curl + HTTP 200 |
| Semantic | health body actually says ok/healthy/pass | content grep (never trust 200 alone) |
| Trace | recent work happened | `journalctl --since 10min` |
| Output | expected artifact/cron output produced | timer/heartbeat file |
| Value | output aligned, fresh, useful | arifOS/AAA/Arif judgment — NOT the watchdog |

## The 5-Bit Alive Vector

```json
{
  "agent": "hermes",
  "process_alive": true,
  "endpoint_alive": true,
  "tool_surface_alive": true,
  "trace_alive": false,
  "output_alive": true,
  "verdict": "DEGRADED"
}
```

## Verdict Grammar (canonical)

| Verdict | Condition |
|---|---|
| **DEAD** | service inactive or missing |
| **DORMANT** | process alive, but no endpoint expected AND no scheduled output expected |
| **DEGRADED** | process alive but endpoint/semantic stale |
| **ZOMBIE** | process + endpoint alive, but no trace/output freshness |
| **ALIVE** | process + endpoint + semantic health pass |
| **UNKNOWN** | unmapped port/service — never name organs from port numbers alone |

**ZOMBIE is the key signal**: process running + endpoint answering but journal silent.
Two interpretations: idle worker that only logs on activity (false alarm) OR genuinely
stuck (real signal). The watchdog reports the observation; the human interprets.

## Deployment (systemd timer pattern)

```
/usr/local/bin/federation-watchdog.sh        # probe script (see scripts/ in this skill)
/etc/systemd/system/federation-watchdog.service   # Type=oneshot, SuccessExitStatus=0 1 2
/etc/systemd/system/federation-watchdog.timer     # OnBootSec=2min, OnUnitActiveSec=5min
/var/lib/arifos/agent_liveness.json               # output artifact
```

Unit essentials:

```ini
# .service — never let observation look like a fault
[Service]
Type=oneshot
ExecStart=/usr/local/bin/federation-watchdog.sh
SuccessExitStatus=0 1 2
```
```ini
# .timer
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
Unit=federation-watchdog.service
```

Exit codes: 0=HEALTHY, 1=DEGRADED, 2=CRITICAL (any DEAD → CRITICAL; any ZOMBIE/DEGRADED → DEGRADED).

## Organ Registry (name|service|port|has_endpoint|has_trace)

Current as of 2026-08-01. Probe `systemctl list-units --type=service --state=running` first — registry drifts.

```
well|well.service|18083|true|true
arifos|arifos.service|8088|true|true
a-forge-mcp|a-forge-mcp.service|18084|true|true
kabarkan-worker|kabarkan-worker.service|0|false|true
hermes-asi-gateway|hermes-asi-gateway.service|0|false|true
openclaw-gateway|openclaw-gateway.service|0|false|true
forge-gateway|forge-gateway.service|0|false|true
```

**Classification rule:** ports 18085/18086 were found live-responding but unidentified —
they stay UNKNOWN until classified. Never guess an organ's name from its port.

## Guardrails (hard)

1. **OBSERVE_ONLY** — no restart/repair/rollback/SEAL in the watchdog. Mutation stays
   with A-FORGE after explicit SEAL; systemctl start/restart/stop remain constitutionally gated.
2. **No "USEFUL" verdict** — ALIVE only means "active + responding". Usefulness requires
   arifOS/AAA/Arif judgment. Do not add a usefulness heuristic to the probe.
3. **WELL stays REFLECT_ONLY** — the watchdog is federation observability, NOT a WELL feature.
   WELL may *consume* the artifact (federation_liveness = healthy/degraded/critical) as
   telemetry input, but must not become the federation judge. "WELL reflects. arifOS judges. Arif decides."

## Consumers

- **WELL**: may read `overall` + per-agent verdicts as readiness telemetry
  ("don't execute high-impact tasks while federation is degraded")
- **Kabarkan**: candidate owner of the observability plane (watchdog currently standalone systemd)
- **Arif**: reads the artifact directly for a one-glance federation verdict

## Pitfalls

- **HTTP probe to a non-HTTP port reports false DEAD (PROVEN 2026-08-05).**
  `curl :5432/health` on Postgres, `:6379/health` on Redis, `:6380/health` on FalkorDB,
  or `:11434/` on Ollama returns nothing because those services don't speak HTTP. A naive
  probe loop then declares the entire data plane "down" when Docker has them up and
  healthy (`docker ps` shows `Up 4 days (healthy)`). Three corrections, in order:
  1. **Probe by transport, not by habit.** HTTP services (`/health` → JSON) are different
     from DB services (TCP-only / custom protocol / binary line protocol). Don't loop one
     curl shape across all ports and call the negative space "down."
  2. **Cross-check with `docker ps` and `ss -tlnp`.** If the port is in LISTEN state and
     the container says `healthy`, the service IS up — your probe is wrong, not the service.
  3. **Per-organ probe table.** Maintain a `probes: {http: [...], tcp: [...], custom: [...]}`
     map. Each row names its protocol + expected response shape. Never iterate a single
     pattern over a heterogeneous port list.
  Lesson: a probe that lies is worse than no probe. A false DEAD verdict triggers human
  attention, an unnecessary restart, and possibly a SEAL-grade commitment — all from a
  category error in the probe script. The checkup loop's first move must be
  `for port in $PORTS: do curl -sf http://127.0.0.1:$port/ || check_tcp_$port || docker_inspect_$container; done` —
  HTTP-or-fallback, not HTTP-or-DOWN.

- **Ollama is not dead when systemd says `inactive` (PROVEN 2026-08-05).**
  `/root/scripts/ollama-idle-shutdown.sh` is a deliberate idle-killer: stops Ollama when
  there are no active connections AND swap > 50%. It is triggered by cron/systemd timer
  and logs "freed ~656MB swap." This is **DORMANT, not DEAD** by the verdict grammar
  above — the binary is installed, the unit is enabled, the service simply has no work.
  `systemctl start ollama.service` brings it back in <1s when needed. Witness pattern:
  1. `systemctl is-active ollama` returns `inactive`
  2. `ls /opt/arifos/data/ollama/models/` shows manifest blobs
  3. `cat /root/scripts/ollama-idle-shutdown.sh` exists and matches the design
  → verdict is DORMANT, not DEAD. Restarting without demand wastes ~656MB swap.
  Lesson: `systemctl is-active inactive` is one of five bits, not a verdict. An organ
  designed to sleep when idle must be classified DORMANT, not DEAD, and must not be
  restarted without demand. If memory says "Ollama is part of the stack" but the daemon
  is inactive, check for `*-idle-shutdown.sh` and the models dir before recommending
  `systemctl enable --now`. Same pattern applies to any organ with `*idle-shutdown*` or
  `*sleep*` scripts in `/root/scripts/` or `/usr/local/bin/`.

- **Auto-generated telemetry files dirty the repo → false RED (PROVEN 2026-08-01).** If a liveness/sense probe includes a "repo clean" check (`git status --porcelain | wc -l`), build-generated files (e.g. `ns_live_telemetry.json` rewritten by the prebuild script on every `npm run build`) will trip it repeatedly. Each cron run of Sense then emits 🔴 "Repo: N uncommitted files" even though everything is healthy. Fixes, in order of preference:
  1. `.gitignore` the generated file(s) — the build output is derived state, not source.
  2. Patch the probe script to exclude the generated path from the dirty count (e.g. filter `git status --porcelain` through a path ignore list).
  3. If the file must be tracked (telemetry history in git), commit it from a post-build hook so it's always committed by the time the probe runs.
  Whatever the choice, the probe should distinguish "uncommitted *generated* files" (benign, ignore) from "uncommitted *source* files" (real drift, alert).
- **`write_file`/`patch` refuse `/etc/systemd/system/*`** (sensitive-path guard).
  Write the unit to `/tmp/<name>.service`, then `cp /tmp/<name>.service /etc/systemd/system/`.
  The terminal tool is allowed where the file tools refuse. Clean up the /tmp copies after.
- **ZOMBIE false positives on quiet workers**: services that only log on activity
  (e.g. kabarkan-worker) will read ZOMBIE between jobs. Don't treat as outage; note the
  service's logging cadence when interpreting.
- **Health body formats differ per organ**: semantic grep expects `"status": "ok|healthy|pass|..."`
  in the body. If an organ's /health uses a different shape (e.g. `"status": "degraded"` is
  valid-but-warned), extend the grep pattern rather than forcing one format.
- **Don't build jq dependency**: the assembly step uses Python stdlib (`json.dump`) so the
  script runs anywhere; the probe fragments are written to per-organ temp files then merged.
- **Registry drift**: adding an organ = one line in the ORGS array. Removing one = delete the
  line. Re-run the script and check the artifact before re-enabling the timer.

## Files

- `scripts/federation-watchdog.sh` — the deployed probe script (canonical copy)
- `references/probe-transport-taxonomy.md` — port-class table + correct probe pattern
  (HTTP vs TCP vs designed-dormant). Use before writing any multi-port probe loop.
