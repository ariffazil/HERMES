# MOTD SOT Dual-Surface Pattern

Dynamic MOTD State-of-Truth system with human (ANSI) + agent (JSON + ENV) surfaces. Verified on Ubuntu 25.10 (update-motd.d + /etc/profile.d/).

## Architecture

```
SSH Login
  │
  ▼
/etc/profile.d/arifos-motd.sh  ─── run-parts /etc/update-motd.d/
  │                                     │
  │                              ┌──────┴──────┐
  │                              ▼             ▼
  │                         Human Surface  Agent Surface
  │                         (ANSI stdout)   (JSON + ENV)
  │                                         
  ▼                                         
Bash prompt (login continues)               
```

## Three Surfaces

| Surface | Consumer | Format | Path |
|---------|----------|--------|------|
| **Human** | 888 (Arif) | ANSI colour, tables, emoji prompts | stdout via profile.d |
| **Ghost JSON** | Agents (A-FORGE, AAA) | Structured JSON, no ANSI | `/var/run/arifos_state.json` |
| **ENV injection** | Shell scripts | Exported vars, zero-cost | `/var/run/arifos_env.sh` |

## Ghost JSON Structure

```json
{
  "ts": 1785181886,
  "constitutional": {"state":"UNSEALED","verdict":"HOLD","vitality":0.5946},
  "system": {"mem_pct":52,"disk_pct":44,"load":"1.82, 1.66, 1.70"},
  "organs": {
    "arifOS":"healthy", "A-FORGE":"healthy", "AAA":"healthy",
    "GEOX":"healthy", "WEALTH":"healthy", "WELL":"degraded"
  },
  "nodes": {"phone_keys":4,"total_keys":36},
  "degraded_organs": "WELL",
  "dependencies": {
    "all_satisfied": true,
    "well_clarity": 7.0,
    "results": ["A-FORGE→WELL: ✅", "GEOX→WELL: ✅", "WEALTH→WELL: ✅"],
    "cascade_risks": []
  }
}
```

## ENV Injection

```sh
# source /var/run/arifos_env.sh
export AF_STATE="UNSEALED"
export AF_VERDICT="HOLD"
export AF_VITALITY="0.5946"
export AF_DEGRADED_ORGANS="WELL"
export AF_MEM_PCT="51"
export AF_DISK_PCT="44"
```

## Enforcement Tools (for connection to MOTD)

These tools are **not run inside the MOTD** but are available on the VPS for use by agents:

| Tool | Function | Max |
|------|----------|-----|
| `arif-circuit-breaker` | Action loop lock | 2 failed attempts → LOCK + 888_HOLD |
| `arif-f4-monitor` | Reasoning loop lock (state-hash based) | 3 cycles → F4 VIOLATION → AUTO-HOLD |
| `arif-dependency-check` | Cross-organ dependency validation | Exit 0=OK, exit 1=blocked |

## Implementation Notes

- **MOTD displays ONLY on interactive SSH login** (via `/etc/profile.d/arifos-motd.sh` with `SSH_CONNECTION` guard). Non-interactive SSH commands (`ssh host 'cmd'`) skip it.
- **Timeout killer**: The MOTD script has an 8-second hard timeout. If probes hang, login still proceeds.
- **`exit 0` in profile.d**: Never put `exit` in profile.d scripts — they're sourced by bash, not executed. `exit` kills the parent shell and disconnects SSH.
- **`run-parts` vs `.` sourcing**: The MOTD script is written as a standalone script (`#!` + `exit 0`), safe for `run-parts`. profile.d sources the script, so `exit 0` in the script would kill the SSH session. Fix: `return 0 2>/dev/null || exit 0` at the end.
