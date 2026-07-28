---
name: shell-patterns
category: devops
tags: [bash, shell, scripting, patterns, pitfalls, set-euo-pipefail, grep]
description: |
  Bash shell scripting patterns and pitfalls used across the arifOS federation.
  Covers `set -euo pipefail` gotchas, grep exit-code traps, variable quoting,
  and other hard-won lessons from the federation's shell-script-heavy ops.
---

# Shell Patterns — arifOS Federation

Bash scripting conventions and hard-won pitfalls from the federation's operational shell scripts. The federation has dozens of `.sh` files across `/root/scripts/`, cron jobs, deploy hooks, and organ wrappers — these patterns keep them reliable.

## Conventions

### Shebang

```bash
#!/usr/bin/env bash
```

Always `env bash`, never `/bin/bash` — portable across VPS Termux, CI containers, and macOS dev machines.

### Strict mode

```bash
set -euo pipefail
```

- `-e`: exit on error
- `-u`: treat unset vars as error
- `-o pipefail`: propagate pipeline failure

### Source vault.env pattern

```bash
VAULT_ENV="/root/.secrets/vault.env"
if [ -f "$VAULT_ENV" ]; then
  set -a
  # shellcheck source=/dev/null
  source "$VAULT_ENV"
  set +a
fi
```

The `# shellcheck source=/dev/null` suppresses shellcheck warnings about sourced files outside the project. Always `set -a`/`set +a` to export sourced variables.

## Pitfalls

### `grep -c` + `set -euo pipefail` — the double-value trap

**Problem:** `grep -c` exits with code 1 when it finds 0 matches. With `set -euo pipefail`, this causes the entire pipeline to fail. The naive fix `|| echo 0` doubles the captured value because `grep -c` already printed "0" to stdout:

```bash
# BROKEN — captures "0\n0" when 0 matches
ORGANS_DEAD=$(echo "$output" | grep -c '❌' || echo 0)
```

**Fix:** Use `|| true` instead — `grep -c` already prints "0" to stdout, so `|| true` just suppresses the exit code without adding another value:

```bash
# CORRECT — captures "0" when 0 matches
ORGANS_DEAD=$(echo "$output" | grep -c '❌' || true)
```

**Same applies to any command that prints a value but exits non-zero on "empty" results.** `wc -l`, `awk`, and `grep` (without `-c`) all share this pattern.

### Trailing newlines in command substitution

`$()` strips trailing newlines, but `grep -c` (and similar) always terminates output with `\n`. The `|| echo 0` fallback also appends `\n`. When both fire, you get `"0\n0"` which as an integer string becomes `"0\n0"` — invalid in JSON and arithmetic contexts.

### JSONL output from bash

When writing JSONL from bash, use `cat <<EOF` heredocs for the JSON body. Validate after writing with:

```bash
python3 -c "import json; json.load(open('$FILE'))"
```

Always pipe through `python3 -m json.tool` or a Python one-liner — bash-generated JSON frequently has trailing-commas, unquoted keys, or double-values from exit-code gotchas.

### `printf` over heredoc for Termux one-shot delivery

When delivering a one-shot paste to Termux, **NEVER use heredocs** (`cat > file << 'EOF'`). Termux treats each physical line as a separate input, so the heredoc delimiter never reaches `cat` and breaks the entire chain.

```bash
# ✅ CORRECT — single shell command, works in one paste
printf '%s\n' \
  'Host vps' \
  '    HostName 72.62.71.199' \
  '    Port 22888' \
  '    User root' \
  '    IdentityFile ~/.ssh/id_ed25519' \
  > ~/.ssh/config

# ❌ WRONG — heredoc breaks in one-shot Termux paste
cat > ~/.ssh/config << 'EOF'
Host vps
    HostName 72.62.71.199
EOF
```

Use `printf` for config files, `&&` chains for multi-step commands. Never assume Termux paste handles heredocs — verify on the target device.

### Python-on-target for complex remote file patching (shell-quoting escape valve)

When you need to do a complex find-and-replace on a remote file (ssh host) and shell quoting becomes unmanageable — nested variables, JSON in strings, heredocs inside variables — **write a Python script locally, scp it, run it on-target** instead of wrestling inline shell quoting:

```bash
# 1. Write the Python patch script locally
write_file /tmp/patch_remote.py << 'PYEOF'
import re
with open("/etc/target/file", "r") as f:
    content = f.read()

old = "old block with $special 'chars' and \"quotes\""
new = """new block with any
characters, ${variables}, or """nested""" content"""

content = content.replace(old, new)
with open("/etc/target/file", "w") as f:
    f.write(content)
print("PATCH OK")
PYEOF

# 2. SCP to target
scp -P 22888 /tmp/patch_remote.py root@host:/tmp/

# 3. Execute on target
ssh -p 22888 root@host 'python3 /tmp/patch_remote.py'
```

**When to use (signals):**
- 3+ levels of quoting (escaped quotes inside `$()` inside `""`)
- Need to pass JSON, heredocs, or special chars (`$`, `` ` ``, `\`) through SSH
- Inline command fails with `syntax error near unexpected token` or unbound variable errors
- Replacement text is longer than ~10 lines with special characters

**When NOT to use (stay inline):**
- Simple `sed`-style one-liners (`s/old/new/`)
- Single-line string replacements
- Appending a few lines to a file

## Common patterns

### Organs health probe

```bash
for pair in "arifOS:8088" "A-FORGE:7071" "AAA:3001" "GEOX:8081" "WEALTH:18082" "WELL:18083"; do
  name="${pair%%:*}"
  port="${pair##*:}"
  if curl -sf --max-time 2 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    echo "  ✅ $name"
  fi
done
```

### Git dirty check across multiple repos

```bash
for d in /root/arifOS /root/A-FORGE /root/AAA /root/GEOX /root/WEALTH /root/WELL; do
  [ ! -d "$d/.git" ] && continue
  branch=$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
  dirty=$(git -C "$d" status -s 2>/dev/null | wc -l)
  if [ "$dirty" -gt 0 ]; then
    printf "  ⚠️  %-20s @ %-15s %d dirty\n" "$(basename "$d")" "$branch" "$dirty"
  fi
done
```

### SSH-only guard (tmux/screen-aware)

```bash
if [ -z "$SSH_TTY" ] || [ -n "$TMUX" ]; then
  return 0 2>/dev/null || exit 0
fi
```

This double-form works both sourced (`. file.sh`) and executed (`bash file.sh`).

### Cross-Organ Dependency Check

Validates upstream dependency health before bridge operations. Uses `/etc/arifos/organ_dependencies.json`:

```bash
arif-dependency-check
# exit 0 → all dependencies satisfied
# exit 1 → cascade risk detected
```

Zero-latency ENV var check (from Ghost MOTD injection):

```bash
source /var/run/arifos_env.sh
if [ "$AF_DEP_GEOX_REQUIRES_WELL" = "clarity>=7" ] && \
   echo "$AF_DEGRADED_ORGANS" | grep -q "WELL"; then
  echo "CASCADE HOLD — GEOX requires WELL clarity"
  exit 1
fi
```

### Circuit Breaker (F1 Escalation Gate)

Prevents infinite RSI loops. Caps failures at 2 attempts, then 888_HOLD:

```bash
arif-circuit-breaker start WELL     # Track attempt
arif-circuit-breaker success        # Reset on success
arif-circuit-breaker fail           # +1 → auto-lock at 2

# Locked: 🔒 888_HOLD required
# Reset: rm -f /var/run/arifos_circuit_breaker.json
```

State: `/var/run/arifos_circuit_breaker.json`. Log: `/var/log/arifos_circuit_breaker.log`. ΔS capped at +0.15 before escalation.

## MOTD Rendering (SSH Login Banners)

The federation's SSH login banner (`/etc/update-motd.d/05-arifos`) uses several reusable shell patterns documented in full in `references/motd-rendering-pattern.md`:

| Pattern | Purpose |
|---------|---------|
| **Timeout killer** | `trap cleanup EXIT` + `sleep 8; kill $PID` — never block login |
| **Background self-logging** | `( echo "$duration" >> log & )` — non-blocking render timing |
| **ANSI colors without tput** | `R='\033[0;31m'` — pure escape codes, zero dependencies |
| **Ghost MOTD** | Triple-write: ANSI stdout + JSON + ENV vars to `/var/run/` |
| **Dependency injection** | Cross-organ constraints exported as `AF_DEP_*` ENV vars |
| **Contextual prompt** | Auto-detect degraded organs → suggest triage command |
| **Circuit breaker** | `/usr/local/bin/arif-circuit-breaker` — caps retries at 2, then 888_HOLD |
| **F4 Runtime Monitor** | `/usr/local/bin/arif-f4-monitor` — state-hash cycle counter, auto-HOLD at 3 unchanged cycles |
| **Golden hash RSI** | `md5sum` vs reference → detect unauthorized edits |

**Key lesson:** Every external command (curl, docker, df, free, jq) must be shielded with `2>/dev/null`. The timeout killer must be at least 8s when probing 6+ organs. Never use `tput` — use `\\033` escape codes for ANSI (no external deps).

### F4 Runtime Monitor (State-Hash Cycle Counter)

Prevents infinite reasoning loops. Tracks state hash between `arif_think` iterations — if state hasn't changed after 3 consecutive calls, auto-HOLD and escalate to 888.

**Why not token-based:** Token tracking needs LLM API calls — breaks local isolation (F1). State-hash comparison is 100% local, zero external deps, at the wire layer (bash).

**Separate from circuit breaker:** Reasoning loops (F4) and action loops (circuit breaker) use distinct lock files — a reasoning hold doesn't block repair actions, and vice versa.

```bash
# /usr/local/bin/arif-f4-monitor
arif-f4-monitor check    # Exit 0: proceed | Exit 2: F4 VIOLATION, HOLD | Exit 1: already locked
arif-f4-monitor reset    # Clear lock and cycle count
arif-f4-monitor status   # Show cycles/locked/hash
```

**Mechanism:** `md5sum /var/run/arifos_state.json` → compare with previous hash → if same for 3+ cycles → LOCK. Any state change (new MOTD write, organ status flip) resets the counter.

State files: `/var/run/arif_think_last_hash`, `/var/run/arif_think_cycles`, `/var/run/arif_think_f4_locked`. Log: `/var/log/arifos_f4_monitor.log`.

## References

- `references/grep-c-set-e-pipefail.md` — Reproduction recipe for the `grep -c` + `set -euo pipefail` double-value trap
- `references/motd-rendering-pattern.md` — MOTD rendering patterns: timeout killer, ghost JSON, ghost ENV, contextual triage, dependency injection, circuit breaker, golden hash RSI
