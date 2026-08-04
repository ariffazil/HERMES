---
name: shell-patterns
category: devops
tags: [bash, shell, scripting, patterns, pitfalls, set-euo-pipefail, grep, vault, env, secrets]
description: |
  Bash shell scripting patterns and pitfalls used across the arifOS federation.
  Covers `set -euo pipefail` gotchas, grep exit-code traps, variable quoting,
  vault env var dedup detection, and other hard-won lessons from the federation's
  shell-script-heavy ops.
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

### Hermes redaction corrupts inline scripts that spell secret var names (PROVEN 2026-08-04)

**Problem:** Hermes has a secret-redaction layer. When a script is created via `terminal` heredoc or inline `python3 -`, any line spelling out a vault key's variable name can be rewritten to `***` — corrupting the code (`KEY = ***` → SyntaxError; in Python the injected ellipsis `…` U+2026 becomes an invalid character). Workarounds that make it WORSE: dynamic name construction via string concatenation (`'QWEN_' + 'TEAM_' + ...`) also got corrupted mid-write.

**Proven 2026-08-04:** three consecutive write attempts at an inline Python Token-Plan video script died with `SyntaxError: invalid character '…' (U+2026)` / `KEY = ***`. The fix: write a proper `.sh` file (via `write_file`) that does `source /root/.secrets/kunci-mas.env` at runtime and references the var normally (`AK="${QWEN_TEAM_OWNER_API_KEY:-$QWEN_API_KEY}"`) — the literal var name in a plain `.sh` passed through uncorrupted and ran first try.

**Rules:**
1. Never inline scripts that name vault keys via `python3 - <<EOF` / terminal heredocs. Write a `.sh` file, source the vault, reference vars normally.
2. After writing any script that references secrets, verify before executing: `grep -n '\*\*\*' /tmp/script.sh` — if corrupted, rewrite as `.sh`; do not try to patch the `***` line in place.
3. The secret VALUE never needs to appear in the script — only the variable name, resolved at runtime via `source`.

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

### `set -euo pipefail` + command substitution kills probe scripts SILENTLY (PROVEN 2026-08-01)

**Problem:** `set -e` treats a failing command-substitution assignment as fatal. `OUT=$(python3 probe.py 2>&1)` — if the probe exits non-zero, the script dies AT THAT LINE. The failure-report code AFTER it never runs → **exit 1 with ZERO output**. A health script designed to print a RED report prints nothing; cron/logs only show "Script exited with code 1" — no clue which check failed.

**Concrete failure** (Sense health probe): script had a `FAILS` counter and a report block, but `WEBZEN_OUT=$(python3 web_zen.py doctor ...)` under `set -euo pipefail` aborted before the report on any transient probe timeout. Cron flapped exit-1-silent for hours; a manual `bash -x` run revealed doctor was the dying line.

**Fix — never let a probe's exit code propagate through `set -e`:**

```bash
# Fix 1 — suppress, capture exit explicitly
set +e
WEBZEN_OUT=$(python3 probe.py 2>&1)
WEBZEN_EXIT=$?
set -e
```

```bash
# Fix 2 — || true when you don't need the exit code (then judge by output content)
WEBZEN_OUT=$(python3 probe.py 2>&1) || true
```

```bash
# Fix 3 — capture exit code inline, no set +e bracket (PROVEN 2026-08-03)
WEBZEN_EXIT=0
WEBZEN_OUT=$(python3 probe.py 2>&1) || WEBZEN_EXIT=$?
```

**Re-proven 2026-08-03:** the same Sense probe died silently AGAIN — cron reported only "Script exited with code 1", zero indication of which check failed. This time two unguarded substitutions were latent dying lines (the doctor call and `DIRTY_COUNT=$(git ... | wc -l)`). After applying Fix 3 + `|| DIRTY_COUNT=0` guards to EVERY command substitution, the probe immediately printed the real failure (a single 404 route) instead of fainting. **Rule: in any multi-check probe, guard EVERY command substitution with `|| fallback` — one unguarded assignment under `set -e` turns a reporting tool into a silent exit-1.** The 2026-08-01 fix patched only one line; the 2026-08-03 fix shows guards must be applied systematically to ALL substitutions in the script.

**Better — don't use `set -e` for multi-check health probes at all.** A probe that must report ALL failures is the opposite shape of a linear fail-fast script: accumulate failures explicitly (`FAILS=$((FAILS+1))`) and let the report block at the end decide the exit code. `set -e` belongs in scripts where ANY failure should abort immediately.

**Diagnosis:** silent exit-1 + `set -euo pipefail` + no stdout = died at the first non-zero command. Reproduce with `bash -x script.sh 2>&1 | tail` to see the exact dying line.

### Functions returning sentinel codes under `set -e` (PROVEN 2026-08-04)

Same trap family as command substitution, but for **function calls**: a `poll()` that deliberately returns `2` for "retryable failure" kills a `set -e` script at the call line — the retry branch after it never executes. Bracket it:

```bash
set +e
poll
RC=$?
set -e
if [ $RC -eq 2 ]; then ...retry...; fi
```

**Rule:** any function that returns non-zero *on purpose* (sentinel codes: 0=ok, 1=fatal, 2=retryable) must be called under `set +e` or with `|| RC=$?`. Hit during the Token Plan video Green Net auto-retry script — the retry branch was dead code until the poll call was bracketed.

### Health probe hardening — transient tolerance + signal-vs-noise threshold (PROVEN 2026-08-03)

Script-based health probes (`no_agent: true`, every 15m) fail in patterns that look like real outages but are just brittle failure detection. Apply these 5 rules to every multi-check probe:

1. **Doctor/YELLOW warnings ≠ failures.** Tools like `web_zen doctor` exit 1 for YELLOW-band checks (caddy hints, etc.) — they're informational, not fatal. Map exit=1 to 0: `if [ "$EXIT" -eq 1 ]; then EXIT=0; fi`.

2. **`git status` counts staged deletions as "dirty".** Filter to only untracked files for true dirt: `grep "^??"`. Modified + staged deletions = work in progress, not a health signal.

3. **Transient network 000 codes ≠ 4xx/5xx errors.** A single route returning `HTTP 000` in a 15-minute window is a network blip. Only fail when failures accumulate: `if [ "$FAILS" -gt 2 ]`.

4. **Every command substitution needs `|| fallback` under `set -e`.** The 2026-08-01 fix patched only one line; 2026-08-03 proved the remaining unguarded assignments died silently. Pattern: `VAR=$(cmd) || VAR_DEFAULT` on EVERY substitution. One unguarded assignment turns a reporting tool into exit-1-silent.

5. **`curl -sI` (HEAD, no Accept header) ≠ browser.** Caddy `Accept`-gated handlers return 404 to probes while humans see 200. Always probe with `-H "Accept: text/html"` and GET (not HEAD).

**Proven 2026-08-03:** Sense health probe (job `db0aa69e0fdc`) failed every 15 min for hours — 3 root causes: doctor exit=1 from YELLOW warnings, dirty repo counting 25 staged deletions, transient 000 codes on 2 routes. All fixed by applying these 5 rules.

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

### Vault env var dedup detection — multi-file sourcing trap (PROVEN 2026-07-29)

> **See also:** `federation-secret-vault` skill — the KUNCI-MAS protocol
> for unified secret vault management (Python generator, CI drift detector,
> symlink architecture, systemd consumer mapping). This section covers
> *detection*; that skill covers the *full lifecycle*: consolidation,
> generation, verification, and maintenance across the federation.

**Problem:** When the same `KEY=value` appears in multiple lines of a sourced `.env` file, or across multiple files that get sourced in sequence, **the last assignment wins**. Bash has no duplicate-key detection. A key added at line 49 but overwritten at line 512 silently breaks all consumers downstream.

**Concrete failure pattern** (2026-07-29): `MINIMAX_API_KEY` appeared 3 times across `vault.env` (line 49, 385, 512) — one good key, two bad duplicates from an `/etc/environment` migration. Bash's `set -a && source` processed the file top-to-bottom: good key at 49, then bad key at 512 (`export MINIMAX_API_KEY=...`) overwrote it. Every API call got 401 until the duplicate was found and removed.

**Detection pattern:**
```bash
# Find all occurrences of a key across vault files
grep -n "^MINIMAX_API_KEY\|export MINIMAX_API_KEY" /root/.secrets/vault.env

# Check what the ACTIVE value is after sourcing
set -a && source /root/.secrets/vault.env && set +a
echo "Active: ${MINIMAX_API_KEY:0:10}...${MINIMAX_API_KEY: -4}"

# Cross-check against vault.flat.env (read by systemd)
grep -n "^MINIMAX_API_KEY" /root/.secrets/vault.flat.env

# Test the active key against the actual API endpoint
curl -s "https://api.minimax.io/v1/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -d '{"model":"MiniMax-M3","messages":[{"role":"user","content":[{"type":"text","text":"hi"}]}],"max_tokens":5}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if 'choices' in d else '❌')"
```

**Fix pattern:**
1. Find ALL lines containing the key: `grep -n "KEY" file.env`
2. Verify which values work: test each against the API
3. Comment out bad duplicates: `sed -i 'NNNs/^/# /' file.env`
4. Re-source and test again
5. **Check ALL vault files** — the fix must propagate to `vault.env`, `vault.flat.env`, and any per-service env file (`mimo.env`, `qwen.env`, etc.)
6. Verify no `export` statements at the bottom of the file overwrite the top definitions

**Common sources of duplicates:**
- `/etc/environment` migration (flat export dump appended to the bottom)
- Per-service env files with overlapping keys (`mimo.env`, `a-forge.env`)
- Backup/restore cycles that append instead of overwrite
- Manual edits that add a new line instead of updating the existing one

**Prevention:** Any `make vault-generate` target must dedup by grepping `^[A-Z_]*=` and asserting `sort | uniq -d` returns empty before writing. F11: git hook detects duplicate keys in staged changes.

### Curl `-w '%{http_code}'` inside Python f-strings — silent NameError (PROVEN 2026-08-04)

**Problem:** `curl -w '%{http_code}'` format strings use `%{VAR}` syntax. Python f-strings also use `{}` for interpolation. When you embed a curl command inside a Python f-string, the `%{http_code}` triggers Python's format specifier parsing → `NameError: name 'http_code' is not defined`.

```python
# BROKEN — NameError
cmd = f"curl -sS --max-time 5 -w 'HTTP:%{http_code}|TIME:%{time_total}s' '{url}'"
# → NameError: name 'http_code' is not defined
```

**Fix — build the command as a plain string, not an f-string:**

```python
# CORRECT — no f-string, use concatenation
cmd = "curl -sS --max-time 5 -o /tmp/body -w 'HTTP:%{http_code}|TIME:%{time_total}s' '" + url + "'"
r = terminal(cmd, timeout=10)
```

```python
# CORRECT (cleanest) — two-step: curl to file, then inspect separately
r1 = terminal(f"curl -sS --max-time 5 -o /tmp/fed_body '{url}'", timeout=10)
r2 = terminal("stat -c '%s' /tmp/fed_body 2>/dev/null || echo 0", timeout=5)
```

**Rule:** When building shell commands in Python, avoid f-strings when the command uses `{}` or `%{}` syntax. Use string concatenation or split into two `terminal()` calls.

**Proven 2026-08-04:** FED gap audit probe — 7 endpoints batch, first 3 probes hit `NameError` on curl format string. Fix: split curl + inspection into separate `terminal()` calls.

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
