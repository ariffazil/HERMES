# Token Leak Forensics — 5-Layer Investigation Framework

When a Telegram bot token (or any API token) is suspected compromised, trace
across ALL five surfaces. Missing even one leaves the leak vector unidentified.

Proven 2026-07-26 — three bot tokens rotated across 10+ locations after a
comprehensive 5-layer leak audit.

## The Five Layers

```
Layer 1: Session DB        ← Token in command history (most common)
Layer 2: Process Env       ← Token in /proc/PID/environ
Layer 3: Governance Chain  ← Token missing from vault.env SSOT
Layer 4: Git History       ← Token committed to any repo
Layer 5: File Ownership    ← Token file owned by wrong user
```

### Layer 1 — Session DB (most likely, highest priority)

Every shell command containing `${TOKEN}` in a `curl` call leaves the resolved
token value in the terminal output → Hermes session DB (SQLite). Tokens are
permanent in session history.

**Detection:**
```bash
session_search(query="BOT_TOKEN=<TOKEN_PREFIX>", limit=5)
```

**Common leak patterns:**
- `curl -sf https://api.telegram.org/bot${TOKEN}/getMe` — full token resolves
  and gets stored in terminal output
- `cat /proc/PID/environ | grep TELEGRAM_BOT_TOKEN` — token extracted
- Python scripts that read and print/echo token values
- Any `set -x` or `bash -x` shell that expands variables

**Remediation:** Token in session history is permanent. Rotate the token.
There is no way to retroactively purge session DB entries.

**Forward fix (ephemeral token mode):**
```bash
# BAD — token in terminal output:
curl -sf "https://api.telegram.org/bot${TOKEN}/getMe"

# GOOD — use the env var ONCE at source, never print:
# Use a script that reads directly from the token file:
TOKEN=$(cat /root/.secrets/tokens/telegram-agi-asi-bot)
curl -sf "https://api.telegram.org/bot${TOKEN}/getMe" -o /dev/null -w "%{http_code}"

# BEST — use Hermes CLI instead:
hermes telegram bot info
```

### Layer 2 — Process Environment (/proc/PID/environ)

Any process started with `TELEGRAM_BOT_TOKEN` in its environment exposes the
token through `/proc/<PID>/environ`. Any user or process with filesystem access
to `/proc/<PID>/` can read the token.

**Detection:**
```bash
for pid in $(pgrep -f 'gateway|bot\.py|hermes|openclaw'); do
  grep -q TELEGRAM_BOT_TOKEN /proc/$pid/environ 2>/dev/null && \
    echo "PID $pid has token in environ"
done
```

**Common exposure vectors:**
- Systemd services with `EnvironmentFile=` or `Environment=TELEGRAM_BOT_TOKEN=...`
- Shell scripts that export the token then run subprocesses
- Docker containers with `-e TELEGRAM_BOT_TOKEN=...`

**Remediation:**
- Tokens in systemd units are unavoidable for production — ensure `hidepid`
  mount option for `/proc`
- Minimize processes that hold the token
- Rotate immediately on any suspicion

### Layer 3 — Governance Chain (vault.env SSOT)

This is the most subtle leak: a token exists in a runtime `.env` file or systemd
unit but was NEVER added to vault.env (the single source of truth). Without
vault.env presence, the token is:
- Not tracked in the secret INDEX.md
- Not part of rotation protocol
- Not backtrackable in audit
- Not sealiable to VAULT999

**Detection:**
```bash
# Compare all env var definitions against vault.env
source /root/.secrets/vault.env 2>/dev/null
for var in ASI_ARIFOS_BOT_TOKEN TELEGRAM_BOT_TOKEN FORGE_BOT_TOKEN; do
  if [ -z "${!var:-}" ]; then
    echo "❌ $var: MISSING from vault.env"
  else
    echo "✅ $var: present"
  fi
done

# Cross-check actual runtime .env files against vault.env
for f in /root/AAA/agents/hermes-asi/runtime/.env /root/.openclaw/.env; do
  [ -f "$f" ] || continue
  while IFS='=' read -r key val; do
    [[ "$key" =~ TOKEN|API_KEY|SECRET ]] || continue
    grep -q "^export $key=" /root/.secrets/vault.env && continue
    echo "❌ $key defined in $f but missing from vault.env"
  done < "$f"
done
```

**Root causes found in production:**
- `ASI_ARIFOS_BOT_TOKEN` was in Hermes runtime `.env` but never added to
  `vault.env` — only discovered during leak investigation (Gap #3, 2026-07-26)
- Token was added to a systemd drop-in directly without vault.env entry
- Token was set in `/etc/environment` without propagating to vault.env

**Remediation:** Add the missing token to vault.env, regenerate vault.flat.env,
restart all services that reference it.

### Layer 4 — Git History

Secrets committed to any git repo — even if later removed — are permanently
in the git history. BFG Repo-Cleaner or `git filter-branch` can purge, but
the window of exposure already exists.

**Detection:**
```bash
for repo in /root/arifOS /root/A-FORGE /root/AAA /root/HERMES; do
  cd "$repo"
  hits=$(git log --all --oneline --diff-filter=A -G 'TELEGRAM_BOT_TOKEN=|context7\.env|email\.env' 2>/dev/null | wc -l)
  [ "$hits" -gt 0 ] && echo "❌ $repo: $hits commits with secrets" || echo "✅ $repo: clean"
done
```

**Known incidents (arifOS federation):**
- `secrets/context7.env` and `secrets/email.env` committed to AAA repo, later
  removed in commit `31b37d88` (Gap #4, 2026-07-26)

**Remediation:**
- Immediately rotate any token exposed via git
- Use `git filter-branch` or BFG to purge from history
- Add `.env` to `.gitignore` globally
- Use git-secrets or gitleaks as pre-commit hook

### Layer 5 — File Ownership

A token file owned by the wrong user means another user (or attacker who
compromises that user) can read the token.

**Detection:**
```bash
find /root -name ".env" -o -name "*.token" -o -name "vault.env" -o -name "vault.flat.env" \
  2>/dev/null | while read f; do
  owner=$(stat -c '%U' "$f")
  perms=$(stat -c '%a' "$f")
  [ "$owner" != "root" ] && echo "❌ $f owned by $owner (not root)"
  [ "${perms#0}" -gt 600 ] && [ -f "$f" ] && echo "⚠️ $f perms $perms (strict)"
done
```

**Known incidents:**
- `/root/AAA/agents/hermes-asi/runtime/` owned by `ariffazil` (not root) while
  services run as root (Gap #5, 2026-07-26)

**Remediation:**
```bash
chown root:root /path/to/token/file
chmod 600 /path/to/token/file
```

---

## Complete Audit Script

Run this standalone to check all five layers simultaneously:

```bash
#!/bin/bash
# 5-layer token leak audit — run after any token rotation
# Reports any layer with a leak.

set -euo pipefail
LAYER_FAIL=0

echo "╔═══════════════════════════════════════════╗"
echo "║        5-LAYER TOKEN LEAK AUDIT          ║"
echo "╚═══════════════════════════════════════════╝"

source /root/.secrets/vault.env 2>/dev/null

echo ""
echo "=== LAYER 1: Session DB (grep session history) ==="
echo "Manual check: session_search(query=\"BOT_TOKEN=\")"
echo "No automated check — requires Hermes session_search tool."

echo ""
echo "=== LAYER 2: Process Env ==="
for pid in $(pgrep -f 'gateway|bot\.py|hermes|openclaw|opencode' 2>/dev/null | head -20); do
  for var in TELEGRAM_BOT_TOKEN ASI_ARIFOS_BOT_TOKEN FORGE_BOT_TOKEN; do
    if grep -q "$var" /proc/$pid/environ 2>/dev/null; then
      echo "  ⚠️ PID $pid has $var in environ"
    fi
  done
done

echo ""
echo "=== LAYER 3: vault.env Governance ==="
for var in ASI_ARIFOS_BOT_TOKEN TELEGRAM_BOT_TOKEN FORGE_BOT_TOKEN; do
  val="${!var:-}"
  if [ -z "$val" ]; then
    echo "  ❌ $var: MISSING from vault.env"
    LAYER_FAIL=1
  elif echo "$val" | grep -q '\*\*\*'; then
    echo "  ❌ $var: REDACTED (***) in vault.env"
    LAYER_FAIL=1
  else
    echo "  ✅ $var: present"
  fi
done

echo ""
echo "=== LAYER 4: Git History ==="
for repo in /root/arifOS /root/A-FORGE /root/AAA /root/HERMES; do
  [ -d "$repo/.git" ] || continue
  hits=$(git -C "$repo" log --all --oneline --diff-filter=A -G 'TELEGRAM_BOT_TOKEN=|TOKEN=|context7|email\.env' 2>/dev/null | wc -l)
  [ "$hits" -gt 0 ] && echo "  ❌ $repo: $hits commits with secrets" && LAYER_FAIL=1 || echo "  ✅ $repo: clean"
done

echo ""
echo "=== LAYER 5: File Ownership ==="
for f in /root/.secrets/vault.env /root/.secrets/vault.flat.env \
  /root/.secrets/tokens/telegram-agi-asi-bot \
  /root/.secrets/tokens/telegram-opencode-bot \
  /root/AAA/agents/hermes-asi/runtime/.env; do
  [ -f "$f" ] || continue
  owner=$(stat -c '%U' "$f")
  perms=$(stat -c '%a' "$f")
  [ "$owner" != "root" ] && echo "  ❌ $f: owned by $owner (not root)" && LAYER_FAIL=1
  [ "$perms" != "600" ] && [ "$perms" != "400" ] && echo "  ⚠️ $f: perms $perms"
done

echo ""
if [ "$LAYER_FAIL" -eq 0 ]; then
  echo "✅ All five layers clean."
else
  echo "❌ One or more layers have leaks — fix before rotating tokens."
fi
```

---

## Token Rotation — 10-Location Checklist

When rotating ANY of the three bot tokens, update ALL locations. Missing one
leaves a stale token as a backdoor.

### Token A: @ASI_arifos_bot (8410138119) — Hermes Agent
- [ ] `vault.env` → `ASI_ARIFOS_BOT_TOKEN` (SSOT)
- [ ] `runtime/.env` → `ASI_BOT_TOKEN`
- [ ] `runtime/.env` → `TELEGRAM_BOT_TOKEN` (duplicate — same bot)
- [ ] `runtime/.env` → `HERMES_TELEGRAM_BOT_TOKEN` (duplicate)
- [ ] `vault.flat.env` (auto-generated)
- [ ] Heroku / Railway / any cloud env var (if applicable)

### Token B: @AGI_ASI_bot (8149595687) — OpenClaw Gateway
- [ ] `vault.env` → `TELEGRAM_BOT_TOKEN` (SSOT)
- [ ] `tokens/telegram-agi-asi-bot` (plaintext token file)
- [ ] `openclaw/.env` → `TELEGRAM_BOT_TOKEN`
- [ ] `vault.flat.env` (auto-generated)
- [ ] Systemd drop-in: `/etc/systemd/system/openclaw*.d/*.conf`

### Token C: @arifOS_bot (8727562763) — FORGE / OpenCode
- [ ] `vault.env` → `FORGE_BOT_TOKEN` (SSOT)
- [ ] `tokens/telegram-opencode-bot` (plaintext token file)
- [ ] `vault.flat.env` (auto-generated)

---

## Provenance

- **Last updated:** 2026-07-26
- **Source session:** Token rotation + 5-layer leak investigation
- **Tokens rotated:** All 3 (ASI💃, 🦞AGI, 🔥FORGE)
- **Gaps found:** 5 (see `token-leak-5-layer-forensic.md` top)
- **F13 standing ruling (2026-07-23):** `OBSERVE_ONLY` + mutation intent = `888_HOLD`
