# MOTD Rendering Pattern — arifOS Federation

> Dual-write SSH login banner: ANSI for humans, JSON/env for agents.
> Verified on af-forge VPS (Ubuntu 25.10), `/etc/update-motd.d/05-arifos`.

## Architecture

```
                  MOTD Script (05-arifos)
                    ├── stdout ──▶ ANSI color output ──▶ HUMAN (SSH terminal)
                    ├── /var/run/arifos_state.json ──▶ AGENT (machine-readable)
                    └── /var/run/arifos_env.sh ──────▶ AGENT (source-able env vars)
```

## Core Patterns

### 1. Timeout Killer (never block SSH login)

```bash
#!/bin/bash
TIMEOUT_PID=$$
cleanup() {
  kill "$BACKGROUND_PID" 2>/dev/null
  wait "$BACKGROUND_PID" 2>/dev/null
  printf '\033[0m'
}
trap cleanup EXIT

(
  # All MOTD content here
  # If this block takes >8s, the killer fires
) 2>/dev/null

# Background killer process
(
  sleep 8
  kill -9 "$TIMEOUT_PID" 2>/dev/null
) &
KILLER_PID=$!
wait "$BACKGROUND_PID" 2>/dev/null
kill "$KILLER_PID" 2>/dev/null
```

**Key principle:** All probe-heavy work (curl, jq, docker) happens in a subshell. A background `sleep 8; kill` fires if the subshell doesn't complete. Exit 0 always, regardless of probe results.

**Bug history (2026-07-05):** Original killer was 4s, but organ probes with `--max-time 2 --retry 1` could collectively need 6-8s under cold-start. Killer fired mid-render, producing 1-line stdout. Bumped to 8s; healthy organs render in <2s.

### 2. Background Self-Logging (RSI performance tracking)

```bash
# Record render time (non-blocking, background)
(
  START=$SECONDS
  # main work already happened above
  END=$SECONDS
  echo "$((END - START))" >> /var/run/motd_perf.log 2>/dev/null
  tail -100 /var/run/motd_perf.log > /var/run/motd_perf.log.tmp 2>/dev/null
  mv /var/run/motd_perf.log.tmp /var/run/motd_perf.log 2>/dev/null
) &>/dev/null &
```

This runs completely detached — its only side effect is the log file. The tail+mv rotation keeps the log bounded to 100 lines.

### 3. ANSI Color Without tput

```bash
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'
B='\033[1;34m'; C='\033[0;36m'; W='\033[1;37m'
D='\033[2;37m'; X='\033[0m'

printf "  ${G}●${X} arifOS  ${D}(healthy)${X}\n"
```

No `tput` calls, no external dependencies. Pure `\033` escape codes. The `2>/dev/null` at the end of the subshell swallows any escape code issues on terminals that don't support color.

### 4. Ghost MOTD (Machine-Readable JSON Twin)

```bash
_write_ghost_json() {
  # Probe kernel and organs (same endpoints as visual render)
  local kdata=$(curl -sf --max-time 2 http://127.0.0.1:8088/health 2>/dev/null)
  local state=$(printf '%s' "$kdata" | jq -r '.state_axes.receipt_state // "UNKNOWN"' 2>/dev/null)

  # Write JSON state
  cat > /var/run/arifos_state.json << JSONEOF
{
  "ts": $(date +%s),
  "constitutional": {"state":"${state}","verdict":"${verdict}","vitality":${vitality:-0}},
  "system": {"mem_pct":${mem_pct:-0},"disk_pct":${disk_pct:-0},"load":"${load}"},
  "organs": {"arifOS":"healthy","A-FORGE":"healthy","WELL":"degraded"},
  "nodes": {"phone_keys":4,"total_keys":36},
  "degraded_organs": "WELL",
  "cascade_blocked_organs": ""
}
JSONEOF

  # Write env vars for agents
  cat > /var/run/arifos_env.sh << ENVEOF
#!/bin/sh
export AF_STATE="${state}"
export AF_VERDICT="${verdict}"
export AF_VITALITY="${vitality}"
export AF_DEGRADED_ORGANS="${degraded}"
export AF_BLOCKED_ORGANS="${blocked}"
export AF_MEM_PCT="${mem_pct}"
export AF_DISK_PCT="${disk_pct}"
ENVEOF
  chmod 644 /var/run/arifos_env.sh /var/run/arifos_state.json 2>/dev/null
}
_write_ghost_json &
```

Both files written in background (`&`) — never blocks login. Paths are hard-coded and script-owned (644 mode).

### 5. Cross-Organ Dependency Injection

The Ghost MOTD also injects **cross-organ dependency constraints** from the Dependency Registry (`/etc/arifos/organ_dependencies.json`) into both the JSON state and ENV vars. This gives agents zero-latency knowledge of what each organ requires from its upstream.

**ENV vars injected into `/var/run/arifos_env.sh`:**

```bash
export AF_DEP_WEALTH_REQUIRES_GEOX="healthy"
export AF_DEP_WEALTH_REQUIRES_WELL="clarity>=7"
export AF_DEP_FORGE_REQUIRES_ARIFOS="healthy"
export AF_DEP_FORGE_REQUIRES_WELL="clarity>=7"
export AF_DEP_GEOX_REQUIRES_WELL="clarity>=7"
export AF_DEP_AAA_REQUIRES_ARIFOS="healthy"
```

**How agents use it:**

```bash
# Fast-path shell check (zero-latency)
source /var/run/arifos_env.sh
if [ "$AF_DEP_GEOX_REQUIRES_WELL" = "clarity>=7" ] && [ "$AF_DEGRADED_ORGANS" = "WELL" ]; then
  echo "⚠️ GEOX→WEALTH bridge: WELL clarity check FAILED — HOLD"
fi

# Structured check for complex routing decisions
arif-dependency-check
# → exit 0: all dependencies satisfied
# → exit 1: cascade risk detected
```

**Dependency manifest (canonical source):** `/etc/arifos/organ_dependencies.json`

### 6. Contextual INIT/Triage Prompt

After probing all organs, detect which are degraded and tailor the session prompt:

```bash
local DEGRADED=""
for pair in "arifOS:8088" "A-FORGE:7071" "AAA:3001" "GEOX:8081" "WEALTH:18082" "WELL:18083"; do
  local n="${pair%%:*}" p="${pair##*:}"
  local result=$(curl -sf --max-time 1 "http://127.0.0.1:${p}/health" 2>/dev/null)
  local st="?"
  [ -n "$result" ] && st=$(printf '%s' "$result" | jq -r '.status // "healthy"' 2>/dev/null)
  if [ "$st" != "healthy" ] && [ "$st" != "?" ]; then
    DEGRADED="${DEGRADED}${DEGRADED:+ }${n} (${st})"
  fi
done

if [ -n "$DEGRADED" ]; then
  printf "  ⚠ TRIAGE RECOMMENDED\n"
  printf "  Degraded: ${DEGRADED}\n"
  printf "  → arif_think --mode diag --target '${DEGRADED%% *}'\n"
else
  printf "  ⚡ SESSION RESUME\n"
  printf "  → arif_think --mode reason --query '<your intent>'\n"
fi
```

Zero extra dependencies — re-uses the same `--max-time 1` curl probes.

### 7. Circuit Breaker (F1 anti-infinite-loop)

When a triage or repair action is initiated, the circuit breaker tracks attempts and auto-locks after 2 failures:

```bash
/usr/local/bin/arif-circuit-breaker

# Usage:
arif-circuit-breaker start WELL       # Begin attempt tracking
# ... attempt fix ...
arif-circuit-breaker success           # ✅ Reset on success
arif-circuit-breaker fail              # ⚠️ Increment counter

# After 2 failures → LOCKED:
# 🔒 CIRCUIT TRIPPED — 888_HOLD required.
# Reset: rm -f /var/run/arifos_circuit_breaker.json
```

**State file:** `/var/run/arifos_circuit_breaker.json` — JSON tracking attempts/retries/locked.
**Log:** `/var/log/arifos_circuit_breaker.log` — timestamped attempt history.
**Design principle:** The breaker caps entropy growth at ΔS=+0.15. After 2 failed attempts, the system escalates to 888 (human) before entropy exceeds threshold. This prevents:
- Infinite RSI loops (agent keeps trying same failing fix)
- Resource exhaustion (unbounded curl/restart cycles)
- Cascade failures (broken organ keeps getting hammered while other organs depend on it)

### 8. F4 Runtime Monitor — auto-HOLD on reasoning loops

When `arif_think --mode diag` is called repeatedly with zero state change, the F4 monitor detects the reasoning loop and triggers auto-HOLD after 3 cycles:

```bash
# /usr/local/bin/arif-f4-monitor
arif-f4-monitor check    # → exit 0 (proceed), exit 2 (F4 HOLD), exit 1 (locked)
```

**Mechanism:** `md5sum /var/run/arifos_state.json` → compare with previous hash. If unchanged for 3 consecutive checks → LOCK. Any state change (new MOTD, organ status flip) resets counter.

**Separate from circuit breaker:** Reasoning loops and action loops use distinct lock files. A reasoning hold does not block a repair action.

**Why state-hash over token-count:** Token tracking needs LLM API calls — F1 violation. State-hash is 100% local bash, zero external deps.

### 9. Golden Hash Drift Detection (RSI Loop)

```bash
THIS_HASH=$(md5sum "$THIS_FILE" 2>/dev/null | cut -d' ' -f1)
GOLDEN_HASH=$(grep 'GOLDEN_HASH:' "$REF_FILE" 2>/dev/null | head -1 | cut -d' ' -f2)

if [ -n "$GOLDEN_HASH" ] && [ "$THIS_HASH" != "$GOLDEN_HASH" ]; then
  printf "  ⚠ MOTD GOLDEN HASH MISMATCH\n"
  printf "  → update golden hash in ${REF_FILE} after verification\n"
elif [ "$AGE_DAYS" -gt 30 ]; then
  printf "  ⚠ MOTD stale — last modified ${AGE_DAYS} days ago\n"
else
  printf "  ✓ MOTD fresh — last modified ${AGE_DAYS} day(s) ago\n"
fi
```

The golden hash is stored in a companion document (`/root/AAA/governance/001_MOTD_RSI.md`). When the script is modified, the hash mismatches — alerting the user to update the golden hash after verification. This creates a deliberate friction against ungoverned edits.

## File Layout

| Path | Purpose |
|------|---------|
| `/etc/update-motd.d/05-arifos` | Main MOTD script (chmod +x) |
| `/var/run/arifos_state.json` | Ghost JSON — machine-readable state |
| `/var/run/arifos_env.sh` | Source-able env vars (`AF_STATE`, `AF_DEGRADED_ORGANS`, `AF_BLOCKED_ORGANS`, `AF_DEP_*`) |
| `/var/run/arifos_circuit_breaker.json` | Circuit breaker state (attempts/locked) |
| `/var/log/arifos_circuit_breaker.log` | Circuit breaker audit trail |
| `/var/run/arif_think_last_hash` | F4 monitor: state hash (last known) |
| `/var/run/arif_think_cycles` | F4 monitor: consecutive unchanged cycles |
| `/var/run/arif_think_f4_locked` | F4 monitor: lock file when circuit tripped |
| `/var/log/arifos_f4_monitor.log` | F4 monitor: audit trail |
| `/var/run/motd_perf.log` | Render time history (last 100 entries) |
| `/etc/arifos/organ_dependencies.json` | Cross-organ dependency manifest |
| `/usr/local/bin/arif-circuit-breaker` | F1 circuit breaker CLI |
| `/usr/local/bin/arif-dependency-check` | Dependency validation CLI |
| `/usr/local/bin/arif-f4-monitor` | F4 runtime monitor (state-hash cycle counter) |
| `/root/AAA/governance/001_MOTD_RSI.md` | RSI companion doc with golden hash |

## Verification

```bash
# Test the MOTD
run-parts /etc/update-motd.d/ 2>/dev/null

# Check ghost JSON
cat /var/run/arifos_state.json | python3 -m json.tool

# Check env vars
source /var/run/arifos_env.sh && echo $AF_STATE $AF_DEGRADED_ORGANS $AF_BLOCKED_ORGANS

# Check dependency health
arif-dependency-check

# Check render performance
tail -5 /var/run/motd_perf.log

# Test circuit breaker cycle
arif-circuit-breaker start WELL && arif-circuit-breaker fail
arif-circuit-breaker status

# Overlapping MOTDs → remove execute bit on old scripts
chmod -x /etc/update-motd.d/06-arif-live
```

## Pitfalls

- **`PrintMotd no` in sshd_config**: If set, PAM MOTD still runs via `pam_motd`, but the SSH server skips `PrintMotd`. Verify with `sshd -T | grep -i 'printmotd\|pam'`. If PAM MOTD is disabled (`session optional pam_motd.so`), the scripts in `/etc/update-motd.d/` never execute.
- **Timeout too short**: 4s killer is too aggressive when all 6 organs are probed with `--max-time 2`. Total worst-case is ~12s. Use 8s as a balanced default. Use `--max-time 2` per probe, not `2>&1` suppression alone.
- **Foreground `&` in terminal tool**: Writing a script with `_write_ghost_json &` via `terminal()` will trigger "Foreground command uses '&' backgrounding" error. Workaround: write the script to a file (via Python or heredoc), then execute it — the `&` inside the file is fine.
- **ANSI colors in non-TTY**: When `run-parts` output is piped, ANSI escape codes become garbage. Always `2>/dev/null` and use `[ -t 1 ]` if you need to conditionally output color. The `2>/dev/null` on the subshell is sufficient — color codes are valid for most terminals.
- **Duplicate MOTD content**: If old MOTD scripts (e.g., `06-arif-live`) aren't disabled, every SSH login shows duplicates. Disable via `chmod -x`, never delete — preserves F1 reversibility.
- **Circuit breaker state persistence**: `/var/run/` is tmpfs — cleared on reboot. This is intentional: a reboot resets the breaker. If persistent breaker state is needed, move to `/var/lib/arifos/`.
- **Dependency registry drift**: The manifest at `/etc/arifos/organ_dependencies.json` is a static file. It must be manually updated when organ dependencies change. No auto-discovery exists yet.
