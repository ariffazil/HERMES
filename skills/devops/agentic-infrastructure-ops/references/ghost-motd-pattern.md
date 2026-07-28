# Ghost MOTD Pattern — Dual-Write State Architecture

## Problem
Agents and humans need simultaneous, consistent access to system state. Humans want visual ANSI banners. Agents need structured data (no ANSI, no regex parsing). Traditional MOTDs serve only humans.

## Solution
Every SSH login trigger (MOTD script) writes state in TWO mediums:
1. **STDOUT** — ANSI-colored banner for human (888)
2. **`/var/run/arifos_state.json`** — structured JSON for agent analytics
3. **`/var/run/arifos_env.sh`** — bash `export` vars for zero-cost agent consumption

## Architecture

```
SSH Login → run-parts /etc/update-motd.d/
  └── 05-arifos
       ├── stdout: ANSI banner
       ├── /var/run/arifos_state.json  (agent analytics)
       └── /var/run/arifos_env.sh      (agent shell, zero compute)
```

## Source of Truth (F2)
State comes from kernel health endpoint `:8088/health` — NOT from `/tmp` flags. The kernel IS the canonical state authority.

## Agent Env File (the most important output)
```bash
# /var/run/arifos_env.sh
export AF_STATE="UNSEALED"
export AF_VERDICT="HOLD"
export AF_VITALITY="0.5946"
export AF_DEGRADED_ORGANS="WELL"
export AF_BLOCKED_ORGANS=""
export AF_MEM_PCT="41"
export AF_DISK_PCT="44"
export AF_F4_CYCLES="0"
export AF_F4_MAX="3"
```

Agent guardrail (zero-cost):
```bash
source /var/run/arifos_env.sh
[ -n "$AF_BLOCKED_ORGANS" ] && exit 1  # cascade blocked
```

## Strict Timeouts (F1 Safety)
```bash
curl -sf --connect-timeout 1 --max-time 2 http://127.0.0.1:8088/health
```
If kernel down → SSH login still fluid. State defaults to `UNKNOWN - OFFLINE`.

## Verified On
- arifOS federation, af-forge VPS (2026-07-27)
- Honor 600 Pro → SSH → VPS → MOTD cycle
