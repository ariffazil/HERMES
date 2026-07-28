# Dual-Surface MOTD: SOT Enforcement at the POSIX Layer

**Pattern forged 2026-07-27 during Honor 600 Pro → af-forge bootstrap session.**  
Three enforcement layers built directly into the SSH login flow, not into Python guardrails or agent prompts.

## Problem

Three blindspots in arifOS v2026.07:

1. **F1 (Reversibility):** No architectural enforcement that H_WELL (human fatigue) is distinguished from M_WELL (machine failure) before routing decisions are made. Agents could skip the recognition that a degraded human cannot be "repaired" with code.
2. **F4 (Clarity/ΔS):** F4 was a specification, not a runtime monitor. READ-only reasoning loops (repeated `arif_think --mode diag` calls returning identical results) could run indefinitely without entropy reduction past iteration 1.
3. **Cross-organ cascade:** GEOX→WEALTH bridge passes geological parameters without checking WELL (human readiness) health — a dependency gap that propagates silently.

## Solution: Three-Layer Enforcement

All three layers share a common substrate: **the MOTD system as a dual-surface truth pipeline**.

### Layer 1: Static — Organ Manifest

`/etc/arifos/organ_dependencies.json` declares every organ's dependencies, thresholds, and actions:

```json
{
  "organs": {
    "WEALTH": {
      "depends_on": {
        "GEOX": {"required_status": "healthy", "action": "HOLD"},
        "WELL": {"min_clarity": 7, "action": "HOLD_if_below"}
      }
    },
    "A-FORGE": {
      "depends_on": {
        "arifOS": {"required_status": "healthy", "action": "HOLD"},
        "WELL": {"min_clarity": 7, "action": "HOLD_if_below"}
      }
    }
  },
  "routing_rules": [
    {
      "from": "GEOX", "to": "WEALTH",
      "via": "geox_to_wealth_bridge",
      "requires": {"WELL": {"min_clarity": 7}},
      "action_if_unmet": "HOLD"
    }
  ]
}
```

This is the **declarative source of truth** — agents read this to know the topology before executing.

### Layer 2: Runtime — Dependency Check

`/usr/local/bin/arif-dependency-check` reads the manifest + live organ state from Ghost JSON, validates every edge:

```bash
$ arif-dependency-check
═══ Cross-Organ Dependency Check ═══
  WELL clarity: 7.0
  A-FORGE → WELL: ✅ degraded (clarity met)
  A-FORGE → arifOS: ✅ healthy
  AAA → arifOS: ✅ healthy
  GEOX → WELL: ✅ degraded (clarity met)
  WEALTH → GEOX: ✅ healthy
  WEALTH → WELL: ✅ degraded (clarity met)
✅ All dependencies satisfied
Exit: 0
```

Returns exit 0 (ok) or 1 (broken). `--json` mode for agent consumption.

### Layer 3: Reasoning — F4 Runtime Monitor

`/usr/local/bin/arif-f4-monitor` detects reasoning loops via state-hash comparison:

```bash
Cycle 1/3: ⚠️ state unchanged
Cycle 2/3: ⚠️ state unchanged  
Cycle 3/3: 🔒 [F4 VIOLATION] AUTO-HOLD → ESCALATE TO 888
```

**Unlike token-based throttling** (which requires LLM API integration), this works at the POSIX level:
- `md5sum /var/run/arifos_state.json` → detects if reality has changed
- If hash unchanged after 3 cycles → `exit 2` → pipeline dead
- Circuit breaker lock file → even hallucinated exit impossible
- Max 3 cycles per reasoning session (configurable via `MAX_CYCLES`)

The enforcement is **state-driven, not cost-driven** — aligns with Arif's axiom: "Aku benci token. Ni bukan casino."

## The Dual-Surface MOTD Architecture

The MOTD system (`/etc/update-motd.d/05-arifos`) writes **three surfaces** from a single probe cycle:

| Surface | Path | Consumer | Format |
|---------|------|----------|--------|
| Visual | stdout (ANSI) | Arif (888) SSH login | Colored boxes, emoji, tables |
| JSON | `/var/run/arifos_state.json` | Agents (LLM, A-FORGE, AAA) | Machine-parseable, no ANSI |
| ENV | `/var/run/arifos_env.sh` | Shell scripts | `source` → `$AF_STATE`, `$AF_DEGRADED_ORGANS` |

**Key invariant:** ALL three surfaces are generated from the SAME probe cycle (same `curl` calls, same `jq` parsing). F2 (Truth) is synchronized 1:1 across human and machine views.

### Why profile.d, not pam_motd

Ubuntu's `PrintMotd no` + `pam_motd.so` configuration means the SSH MOTD doesn't render on login. The fix:

```bash
# /etc/profile.d/arifos-motd.sh
#!/bin/sh
if [ -n "$SSH_CONNECTION" ]; then
    /usr/bin/run-parts /etc/update-motd.d/ 2>/dev/null
fi
```

This forces MOTD render on every interactive SSH login. Set `chmod +x` for the profile.d script.

### Timeout Guard

The 05-arifos script wraps the entire render in a subshell with an 8-second timeout killer:

```bash
cleanup() { kill "$BACKGROUND_PID" 2>/dev/null; }
trap cleanup EXIT
(  # render
) 2>/dev/null &
# 8s killer
( sleep 8; kill -9 "$PID" 2>/dev/null ) &
```

Without this, slow organ probes (cold-start containers, down services) could delay SSH login indefinitely. F1 rule: "Slow probe never blocks login."

## Deploy Sequence

1. Write organ manifest → `/etc/arifos/organ_dependencies.json`
2. Wire Ghost JSON + ENV injection into 05-arifos MOTD script
3. Install `arif-dependency-check` → `/usr/local/bin/`
4. Install `arif-f4-monitor` → `/usr/local/bin/`
5. Create profile.d MOTD driver → `/etc/profile.d/arifos-motd.sh`
6. Remove execute from overlapping scripts → `chmod -x /etc/update-motd.d/06-arif-live`
7. Update golden hash → `GOLDEN_HASH: <md5>` in RSI reference
8. Test: `run-parts /etc/update-motd.d/` + interactive SSH

## Circuit Breaker Integration

The circuit breaker (`arif-circuit-breaker`) provides the **action-level complement** to the F4 monitor:

| Breaker | Target | Max Attempts | Lock Mechanism | Reset |
|---------|--------|-------------|----------------|-------|
| `arif-circuit-breaker` | Action/write loops | 2 failed attempts | `/var/run/arifos_circuit_breaker.json` `.locked=true` | `rm -f <file>` |
| `arif-f4-monitor` | READ/reasoning loops | 3 cycles hash-unchanged | `/var/run/arif_think_f4_locked` | `rm -f <file>` |

Combined, they prevent both action loops (infinite restart/repair attempts) and reasoning loops (infinite diag calls with no state change).

## Files Reference

| File | Purpose |
|------|---------|
| `/etc/arifos/organ_dependencies.json` | Canonical dependency manifest |
| `/etc/update-motd.d/05-arifos` | MOTD renderer with Ghost JSON + ENV |
| `/etc/profile.d/arifos-motd.sh` | Force MOTD on SSH login |
| `/usr/local/bin/arif-dependency-check` | Runtime dependency validation |
| `/usr/local/bin/arif-f4-monitor` | State-hash reasoning loop detector |
| `/usr/local/bin/arif-circuit-breaker` | Action loop breaker (2 attempts) |
| `/var/log/arifos_f4_monitor.log` | F4 audit log |
| `/var/log/arifos_circuit_breaker.log` | Circuit breaker audit log |
| `/root/AAA/governance/001_MOTD_RSI.md` | RSI reference with golden hash |

## Key F1/F2/F4 Design Decisions

| Principle | Implementation | Why not alternatives |
|-----------|---------------|---------------------|
| State-hash detection, not token tracking | `md5sum state.json` | No API integration needed. POSIX-level. Aligns with "token = casino" axiom. |
| `exit 2` hard kill, not soft prompt | Pipeline stops physically | Agent can't ignore or hallucinate past `exit 2`. |
| Max 3 cycles, not configurable threshold | Hardcoded constant | Keep it simple. Can't drift via agent-environment injection. |
| Dual-surface from single probe | Same `curl` used for visual + JSON + ENV | F2 synchronized. No drift between what human sees and agent reads. |
| profile.d not pam_motd | Override `PrintMotd no` | Works regardless of PAM configuration. Also catches non-SSH logins. |
