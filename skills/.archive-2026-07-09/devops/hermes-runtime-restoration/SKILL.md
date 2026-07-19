---
name: hermes-runtime-restoration
description: "Restore Hermes gateway / OpenClaw / cron services after they die. Covers systemd-disabled units (rename .disabled.<ts> back, daemon-reload, enable), background process survival (no `tee` for long-lived servers), and the recurring 'gateway dies when terminal session ends' pattern. Load when: hermes-gateway returns no health, a port that should be listening is silent, cron jobs silently fail, or user says 'X is down'."
version: 1.1.0
author: Hermes-PRIME
created: 2026-07-04
tags: [runtime, systemd, gateway, hermes, openclaw, supervision, restoration, devops]
pinned: false
---

# Hermes Runtime Restoration

The federation has three long-lived services that commonly "die" — but the death is usually a supervision-state problem, not a code problem. This skill teaches how to recognize which kind of death it is and restore it durably.

## The Three Failure Modes

### Mode 1: Service unit was disabled

**Symptom:** `systemctl --user status hermes-gateway` returns `Unit hermes-gateway.service could not be found.` But `ps aux | grep "hermes gateway"` shows the process running. And `curl :18789/health` returns OK.

**Root cause:** Someone renamed the unit to `hermes-gateway.service.disabled.<timestamp>`. Disabling preserves the file but unloads it from systemd. Manual starts work, but the process dies when the parent terminal exits because there's no supervisor to restart it.

**Fix (canonical):**

```bash
cd /root/.config/systemd/user
mv hermes-gateway.service.disabled.<ts> hermes-gateway.service
systemctl --user daemon-reload
systemctl --user enable hermes-gateway.service   # auto-start at boot
systemctl --user start hermes-gateway.service
sleep 5
systemctl --user status hermes-gateway.service   # confirm active (running)
```

**Verify:** `curl :18789/health` + `systemctl --user is-enabled hermes-gateway.service` returns `enabled`.

**Lesson:** A working service + a missing systemd unit = the unit was disabled, not the service. Always `ls /root/.config/systemd/user/*.service*` before assuming the service itself broke.

### Mode 2: Background process killed by parent TTY loss

**Symptom:** Gateway was restarted via `terminal(background=true)` running `/root/.local/bin/hermes gateway run --replace`. Process exits 143 (SIGTERM) within seconds. Log shows `bash: [PID: N (255)] tcsetattr: Inappropriate ioctl for device`.

**Root cause:** Pipeline `command 2>&1 | tee logfile` to a non-TTY stdout. When the parent terminal session ends, the controlling TTY goes away, `tee` can't set terminal attributes, the pipeline breaks, SIGTERM propagates to the gateway. Classic long-running-daemon bug.

**Fix:** Drop `tee` for any process you want to outlive the terminal.

```bash
# BAD — dies when terminal session ends
terminal(background=true): hermes gateway run --replace 2>&1 | tee /tmp/log

# GOOD — survives session end (until next start)
terminal(background=true): hermes gateway run --replace > /tmp/log 2>&1
```

For *durable* survival, also wire systemd (Mode 1).

**Verify:** `ps aux | grep "hermes gateway"` shows process alive after `process(action='poll')` returns.

### Mode 3: "My agent is at /root/arifOS not /root" confusion

**Symptom:** User says "weii why my hermes not at root???" while a working federation is humming on `/root/.hermes`, `/root/arifOS`, `/root/A-FORGE`, etc. Bash prompt shows `/root/arifOS` (or similar).

**Root cause:** Two things — (a) shell `alias arifos='cd /root/arifOS'` in `.bashrc` jumped CWD on tab-completion or session start; (b) arifOS kernel banner hardcodes `ROOT: [/root/arifOS]` regardless of actual cwd. Cosmetic, not functional.

**Diagnostic — measure before answering:**

```bash
pwd                                                    # actual cwd
ls -la /root/ | grep -E "arifOS|hermes|HERMES"         # who's where
realpath /root/.hermes /root/HERMES /root/arifOS       # symlinks
grep "alias.*=" /root/.bashrc                          # navigation aliases
```

If all organs live under `/root/` (possibly with symlinks), federation IS at root. The user's perception is a prompt artifact.

**Lesson:** Don't relocate organs, don't edit the banner, don't strip aliases — answer with evidence and let the user decide what (if anything) to change.

### Mode 5: Duplicate Telegram responses — two root causes

**Symptom:** User sends `/new` (or any command) to the Telegram bot and gets TWO replies (often with different random tips). The bot works, but every command is answered twice.

**This mode has TWO distinct root causes.** Diagnose which one before fixing.

#### 5a. Parent-child fork loop (single gateway software)

**Root cause:** The main `hermes gateway run --replace` (systemd-managed) spawns a child process: `hermes_cli.main gateway run`. Both parent and child connect to the same bot token and both poll Telegram. The child runs at **100% CPU** and **respawns when killed**.

**Diagnostic:**
```bash
ps aux | grep 'hermes.*gateway\|hermes_cli.*gateway' | grep -v grep
# TWO lines: one `hermes gateway run`, one `hermes_cli.main gateway run`
ps -p <child_PID> -o pid,ppid,start,cmd --no-headers
# ppid == main gateway's PID → confirmed parent-child
```

**Fix:** `systemctl restart hermes-asi-gateway.service` from a separate shell. If it recurs, drop `--replace` from ExecStart.

#### 5b. Two independent gateways polling the same bot (different software)

**Root cause:** Two completely separate gateway processes (e.g. Hermes + OpenClaw, or two Hermes instances on different profiles) are both configured with the same Telegram bot token. Each polls Telegram independently, each receives the update, each replies. No parent-child relationship — they're unrelated processes.

**Diagnostic:**
```bash
# Step 1: List ALL gateway-like processes
ps aux | grep -E 'hermes.*gateway|openclaw.*gateway|node.*gateway|hermes_cli.*gateway' | grep -v grep
# Look for DIFFERENT binaries — e.g. python3 hermes_cli.main AND node openclaw/dist/index.js

# Step 2: Confirm same bot token
# Check Hermes config
grep -i 'bot_token\|BOT_TOKEN' /root/.hermes/config.yaml 2>/dev/null
# Check OpenClaw config / env
grep -i 'BOT_TOKEN' /etc/environment /root/.openclaw/.env 2>/dev/null
# Check process environment
cat /proc/<PID1>/environ 2>/dev/null | tr '\0' '\n' | grep -i bot_token
cat /proc/<PID2>/environ 2>/dev/null | tr '\0' '\n' | grep -i bot_token
# Same token = confirmed duplicate handler
```

**Fix:** Kill the gateway you don't need:
```bash
kill <unwanted_gateway_PID>
# Verify it's gone
ps aux | grep 'gateway' | grep -v grep
# Should show exactly ONE gateway process
```

If both are needed (e.g. OpenClaw for its features, Hermes for its own), they MUST use different bot tokens. Create a second bot via BotFather for one of them.

**Verify after fix (either 5a or 5b):**
```bash
ps aux | grep -E 'gateway' | grep -v grep
# Should show exactly ONE gateway process
# Send /new to bot — should get exactly ONE reply
```

**Lesson (2026-07-05):** When the user reports duplicate Telegram responses, the diagnostic MUST check for BOTH causes. Don't assume it's the `--replace` fork-loop (5a) — first check if two different gateway binaries are running (5b). The `ps aux | grep gateway` output tells you immediately which case you're in: same binary twice = 5a, different binaries = 5b. Also: when diagnosing bot issues, compare bot tokens across all gateway configs to confirm whether two different bots are involved or one bot has duplicate handlers.

### Mode 4: User-level vs system-level systemd port conflict

**Symptom:** Service keeps failing with `EADDRINUSE` even after `systemctl restart`. Logs show:
```
Gateway failed to start: gateway already running under systemd; existing gateway is healthy,
exiting with code 78 to prevent a systemd Restart=always loop |
another gateway instance is already listening on ws://127.0.0.1:18789 |
listen EADDRINUSE: address already in use 127.0.0.1:18789
```

**Root cause:** TWO systemd units manage the same service — one system-level (`/etc/systemd/system/`) and one user-level (`~/.config/systemd/user/`). They race for the port. One starts, the other fails with EADDRINUSE, systemd retries, cycle repeats.

**Diagnostic:**
```bash
# Check for competing units
ls /etc/systemd/system/openclaw* 2>/dev/null
ls /root/.config/systemd/user/openclaw* 2>/dev/null
systemctl --user list-units 2>/dev/null | grep openclaw
```

**Fix (keep system-level, disable user-level):**

**CRITICAL:** Use `XDG_RUNTIME_DIR=/run/user/0` to target root's user-level systemd. Without it, `systemctl --user` commands fail silently ("Failed to connect to user scope bus") and the user-level gateway keeps running and respawning.

```bash
# Disable the user-level service (with proper D-Bus context)
XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop openclaw-gateway.service 2>/dev/null
XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable openclaw-gateway.service 2>/dev/null
XDG_RUNTIME_DIR=/run/user/0 systemctl --user daemon-reload 2>/dev/null

# Also stop hermes-gateway if present
XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop hermes-gateway.service 2>/dev/null
XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable hermes-gateway.service 2>/dev/null

# Kill any zombie processes still holding the port
# Check ppid — if ppid=1247 (user-level systemd), it will respawn unless stopped via systemctl
ps aux | grep "openclaw.*gateway\|hermes.*gateway" | grep -v grep
kill -9 <zombie_pid> 2>/dev/null; sleep 2

# Verify port is free
ss -tlnp | grep 18789  # should return nothing

# Restart the system-level service cleanly
systemctl restart openclaw-gateway.service
```

**Verify:** `ss -tlnp | grep <port>` shows exactly ONE process, owned by the system-level unit's PID.

**Lesson (2026-07-05):** When `systemctl restart` fails with EADDRINUSE but the service appears to be "the same one", check for a user-level duplicate. The two units share the same ExecStart but different supervision trees.

### Mode 6: Telegram bot token dead (404 on all API calls)

**Symptom:** Gateway logs show repeated `getMe failed: (404: Not Found)` and `sendMessage failed: (404: Not Found)`. Telegram channel is completely dead — bot can't receive or send messages.

**Root cause:** Bot token is invalid, expired, or revoked. The `TELEGRAM_BOT_TOKEN` env var points to a dead token.

**Diagnostic:**
```bash
# Check logs for 404s
journalctl -u openclaw-gateway --since "5 min ago" | grep -i "404\|getMe\|sendMessage"
# Should show repeated 404 failures

# Verify token is set
grep TELEGRAM_BOT_TOKEN /root/.secrets/vault.flat.env
grep TELEGRAM_BOT_TOKEN /root/.openclaw/.env
grep TELEGRAM_BOT_TOKEN /root/.openclaw/.env.decrypted
```

**Fix:**
1. Get new token from @BotFather
2. Update ALL three locations:
   - `/root/.secrets/vault.flat.env` (systemd env file)
   - `/root/.openclaw/.env` (OpenClaw env)
   - `/root/.openclaw/.env.decrypted` (OpenClaw decrypted env)
3. Restart gateway:
   ```bash
   systemctl restart openclaw-gateway.service
   ```
4. Verify:
   ```bash
   journalctl -u openclaw-gateway --since "30s ago" | grep -i "telegram\|starting provider\|webhook"
   # Should show: [telegram] starting provider (@BotName)
   # Should show: [telegram] webhook advertised to telegram on https://...
   ```

**Lesson (2026-07-05):** When bot token is dead, update ALL three env file locations (vault.flat.env, .env, .env.decrypted). Missing one causes the gateway to start with the old dead token.

**Complication (2026-07-06):** Restoring `.env` from an old SOPS backup may lose required keys added later (e.g. `QWEN_API_KEY`). Gateway fails with `SecretRefResolutionError: Environment variable "QWEN_API_KEY" is missing or empty`. Fix: add the missing key to `.env` as plain text. Get value from `vault.env`: `bash -c 'source /root/.secrets/vault.env; echo "$QWEN_API_KEY"'`. Also, the SOPS `.env` overrides vault.env — if the encrypted `.env` has a stale `TELEGRAM_BOT_TOKEN`, it wins over the correct value in vault.env. Either add a plain-text line to `.env` or remove the encrypted line entirely.

## Diagnostic Sequence (universal)

When ANY federation service looks dead OR misbehaves:

```
1. curl -sf -m 3 http://127.0.0.1:<port>/health     # truth source
2. ps aux | grep <service> | grep -v grep           # process alive? how many?
3. systemctl --user status <unit>                    # supervisor state?
4. ls /root/.config/systemd/user/*.service*          # disabled files?
5. ls /etc/systemd/system/<unit>*                    # competing system-level units?
6. journalctl -u <unit> --since "5 min ago"          # recent errors (system-level)
7. journalctl --user -u <unit> --since "5 min ago"   # recent errors (user-level)
8. THEN decide: restart, re-enable, disable-duplicate, or measure-don't-touch
```

For **duplicate response** complaints, replace step 1 with:
```
1. ps aux | grep -E 'gateway' | grep -v grep        # different binaries = Mode 5b
                                                      # same binary twice = Mode 5a
                                                      # one process = not a duplicate issue
```

Skip any step and you risk acting on assumption. Steps 5-7 catch Mode 4 (dual-unit conflict).

## Common Federation Services (quick map)

| Service | Port | Unit | Health path |
|---------|------|------|-------------|
| arifOS  | 8088 | (native / systemd varies) | `/health` |
| A-FORGE | 7072 | (native) | (varies) |
| GEOX    | 8081 | (native) | `/health` |
| WEALTH  | 18082 | (native) | `/health` |
| WELL    | 18083 | (native) | `/health` |
| OpenClaw | 18789 | `openclaw-gateway.service` | `/health` returns `{"ok":true,"status":"live"}` |
| Hermes gateway | (internal) | `hermes-gateway.service` | via OpenClaw health |
| Hermes MCP | 18086 | (none — orphan process) | probe separately |

## Pitfalls (proven 2026-07-04)

1. **Don't `kill -TERM` a `--replace` mode gateway.** It has internal supervisor that respawns — you end up with TWO gateways fighting for the port. Use `kill -KILL` or fix the systemd unit properly.
2. **Don't `nohup ... &` from foreground `terminal()` tool.** The tool blocks shell-level background wrappers. Use `terminal(background=true)` instead.
3. **Don't trust `systemctl status` alone.** A "loaded but failed" unit can still have a working process if you started it manually. Always cross-check with `ps` + `curl`.
5. **Don't assume one unit per service.** Always check BOTH `/etc/systemd/system/` and `~/.config/systemd/user/` for competing units. Mode 4 port conflicts are invisible until you look at both locations.
6. **`systemctl --user` needs `XDG_RUNTIME_DIR=/run/user/0` in non-login shells.** Without it, commands fail silently ("Failed to connect to user scope bus via local transport") and the user-level gateway keeps respawning. Always prefix: `XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop/disable/daemon-reload`. Verified 2026-07-06: user-level gateway kept respawning after plain `systemctl --user disable` until `XDG_RUNTIME_DIR` was set.
6. **Don't edit the hardcoded banner.** The arifOS `ROOT:` line is a constant in the kernel MOTD. Editing it is constitutional-scope work (`888_HOLD`). If the user is bothered, suggest the alias-removal or cwd-change, not the banner.
7. **Duplicate Telegram responses have TWO root causes.** Don't jump to the `--replace` fork-loop diagnosis. First `ps aux | grep gateway` — if you see different binaries (python + node), it's two independent gateways sharing a token (Mode 5b), not a parent-child loop (Mode 5a). Different root cause, different fix. 5b: kill the unwanted one. 5a: restart via systemd from a separate shell.
8. **When diagnosing duplicate bot responses, compare tokens AND binaries.** Two different bots (`AGI_ASI_bot` via `TELEGRAM_BOT_TOKEN`, `ASI_arifos_bot` via `HERMES_TELEGRAM_BOT_TOKEN`) may both be in the same group. Or two different gateways (Hermes + OpenClaw) may share one token. Check `env | grep BOT_TOKEN | sed 's/=.*/=<SET>/'` AND `ps aux | grep gateway` to distinguish: same-token-different-binaries (Mode 5b), same-token-same-binary (Mode 5a), or different-bots-both-in-group (not Mode 5 at all — separate bots, separate config).
9. **Ed25519 signing uses `pkeyutl`, NOT `dgst -sha256`.** EdDSA doesn't support explicit digest selection. See `references/ed25519-signing.md` for the full pattern.
10. **Never call `systemctl restart <self-unit>` from inside the service's own process.** The restart kills the calling PID before systemd can hand off to the new instance, producing a guaranteed failure. Fix: spawn a detached background call: `execSync("nohup bash -c 'sleep 2 && systemctl restart <unit>' &", { timeout: 5000 })`. This lets the current process finish replying, then systemd replaces it. Pattern from 777-FORGE bot `/restart` command, 2026-07-09.

### Mode 7: `hermes send` CLI fails with token error (gateway is fine)

**Symptom:** `hermes send --to "telegram:<chat_id>" "message"` returns:
```
hermes send: Telegram send failed: You must pass the token you received from https://t.me/Botfather!
```
But the gateway is running and receiving/sending messages normally. The bot token in `.env` is valid.

**Root cause:** `hermes send` resolves the Telegram bot token differently from the gateway adapter. The CLI may not pick up the token from `.env` correctly — intermittent, likely related to env loading order or key name mismatch.

**Fix (direct Telegram Bot API fallback):**

```bash
# Source the env and call Telegram API directly
source /root/.hermes/.env 2>/dev/null
TOKEN="${ASI_ARIFOS_BOT_TOKEN}"
curl -sf -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="<chat_id>" \
  -d text="<message>" | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK' if d.get('ok') else d)"
```

**Verify:** Returns `OK` and message appears in the target chat.

**When to use this fallback:** Any time `hermes send` fails but the gateway is healthy. This is a write-only send — no LLM, no agent loop, no read capability. For reading inbound messages, check gateway logs:
```bash
tail -200 /root/.hermes/logs/gateway.log | grep "<chat_id>"
```

**Real-time message relay pattern (2026-07-07):** When the user is away from their phone and needs to communicate urgently through a Telegram group:
1. Read latest inbound from gateway log: `tail -200 /root/.hermes/logs/gateway.log | grep "<chat_id>"`
2. Send via direct API (above)
3. Confirm send succeeded via curl response
4. Re-check logs for new replies if needed

**Lesson (2026-07-07):** Don't retry `hermes send` more than once — if it fails with token error, go straight to direct API. The gateway adapter works fine; the CLI has a separate token resolution path. Also: `hermes send` is write-only (no read). For reading inbound, gateway logs are the only source.

### Mode 12: Systemd drop-in overrides WorkingDirectory — module import fails (2026-07-13)

**Symptom:** Service crash-loops with `ModuleNotFoundError: No module named 'arifosmcp.runtime.__main__'` even though the module exists and imports fine when run manually (as root or as the service user from the correct directory).

**Root cause:** A drop-in `.conf` file in `/etc/systemd/system/<service>.service.d/` overrides `WorkingDirectory=/` (or another wrong path). The main service file has `WorkingDirectory=/opt/arifos/app` (correct), but the drop-in silently overrides it. Python can't find the package because it's not in `/`.

**The specific drop-in that caused this:** `runtime-truth.conf` contained:
```ini
[Service]
# Wheel runtime must not be shadowed by the dormant deployment copy.
WorkingDirectory=/
```

**Diagnostic:**
```bash
# Show ALL drop-in files
ls /etc/systemd/system/<service>.service.d/*.conf

# Show combined effective config (main + all overrides)
systemctl show <service> | grep WorkingDirectory

# Test import manually from the WRONG directory
cd / && /opt/arifos/venv/bin/python -c "from arifosmcp.runtime.__main__ import main"
# Should FAIL with ModuleNotFoundError — confirms WorkingDirectory issue

# Test import from the CORRECT directory
cd /opt/arifos/app && /opt/arifos/venv/bin/python -c "from arifosmcp.runtime.__main__ import main"
# Should succeed
```

**Fix:**
```bash
# Remove the offending drop-in
rm /etc/systemd/system/<service>.service.d/<offending>.conf

# Reload and restart
systemctl daemon-reload
systemctl restart <service>
```

**Lesson (2026-07-13):** When a service crash-loops with ModuleNotFoundError but the module imports fine manually, check ALL drop-in files for WorkingDirectory overrides. Use `systemctl show <service> | grep WorkingDirectory` to see the EFFECTIVE value after all overrides are applied. The comment "Wheel runtime must not be shadowed" is a valid concern but the fix (WorkingDirectory=/) breaks Python package resolution. If needed, use `PYTHONPATH` or install the package properly instead.

### Mode 13: `.env` file permissions — service user can't read (2026-07-13)

**Symptom:** Service crash-loops with `PermissionError: [Errno 13] Permission denied: '.env'` when running as a non-root user (e.g. `User=arifos`).

**Root cause:** The `.env` file in the service's working directory is owned by a different user (e.g. `ariffazil:ariffazil` with mode `0600`). The service runs as `User=arifos` which can't read it.

**Diagnostic:**
```bash
# Check .env ownership and permissions
ls -la /opt/arifos/app/.env
# -rw------- 1 ariffazil ariffazil 7937 ...  ← wrong: only owner can read

# Test as the service user
sudo -u arifos cat /opt/arifos/app/.env
# cat: /opt/arifos/app/.env: Permission denied
```

**Fix:**
```bash
# Add group read permission and set group to the service user's group
chmod 640 /opt/arifos/app/.env
chown ariffazil:arifos /opt/arifos/app/.env
# -rw-r----- 1 ariffazil arifos 7937 ...  ← correct: owner + group can read

# Restart service
systemctl restart <service>
```

**Permanent fix — `ExecStartPre=+` auto-heal:** If something (git pull, deploy script) keeps reverting `.env` permissions, add a drop-in that fixes them before every start. The `+` prefix runs the command as root (before dropping to `User=`):

```bash
cat > /etc/systemd/system/<service>.service.d/fix-env-perms.conf << 'EOF'
[Service]
ExecStartPre=+/bin/bash -c 'chmod 640 /opt/arifos/app/.env && chown ariffazil:arifos /opt/arifos/app/.env'
EOF
systemctl daemon-reload
```

**Verified 2026-07-13:** Tested by reverting `.env` to `0600 ariffazil:ariffazil`, then `systemctl restart arifos` — service came up clean because ExecStartPre fixed permissions before the main process started.

**Lesson (2026-07-13):** When a service runs as a dedicated user (not root), ALL files it needs to read must be accessible to that user. EnvironmentFile in systemd is loaded by PID 1 (root) before dropping privileges, but `.env` files loaded by the application itself (e.g. pydantic/dotenv) are read AS the service user. Check both paths: systemd EnvironmentFile (root-loaded) vs application .env (user-loaded).

### Mode 8: Stale PID blocks restart — gateway crash-loop (2026-07-11)

**Symptom:** `hermes gateway restart` succeeds but the gateway immediately exits with status 1. Logs show `Gateway already running (PID XXXXX)` even after the restart command. Systemd keeps retrying (`activating (auto-restart)`), creating a crash-loop.

**Root cause:** A stale gateway process (from a previous `--replace` run, another agent, or a manual start) is still alive and holding the PID file or port. The new systemd-managed process detects it and exits. But systemd keeps restarting it, each time hitting the same stale PID.

**Diagnostic:**
```bash
# Check for stale processes
ps aux | grep 'hermes.*gateway\|hermes_cli.*gateway' | grep -v grep
# Two lines = stale + systemd-managed competing

# Check systemd state
systemctl --user status hermes-gateway.service
# Look for "activating (auto-restart)" with repeated failures

# Check logs for the real error
journalctl --user -u hermes-gateway.service --no-pager -n 20
# Look for "Gateway already running (PID X)" or "token rejected"
```

**Fix sequence (order matters):**
```bash
# Step 1: Kill ALL gateway processes (stale + systemd-managed)
pkill -f "hermes.*gateway" 2>/dev/null
pkill -f "hermes_cli.*gateway" 2>/dev/null
sleep 2

# Step 2: Verify they're gone
ps aux | grep 'gateway' | grep -v grep
# Should return empty

# Step 3: Reset systemd failed state
systemctl --user reset-failed hermes-gateway.service 2>/dev/null

# Step 4: Restart cleanly
hermes gateway restart
# Or: systemctl --user restart hermes-gateway.service
```

**Complication — bot token rejection cascade:** If the stale process was started with a different (or expired) bot token, the logs may show `The token 'XXX' was rejected by the server` alongside the stale PID message. This is a red herring — the token error comes from the stale process, not the current config. Fix the stale PID first, then the gateway will start with the correct current token from `.env`.

**Verification:**
```bash
# Gateway should be running as a single process
ps aux | grep 'hermes.*gateway' | grep -v grep | wc -l
# Should be exactly 1

# Telegram should be connected
tail -5 /root/.hermes/logs/gateway.log | grep "connected"
```

**Lesson (2026-07-11):** When adding Telegram group/user IDs for a new collaborator, a config edit corrupted the YAML format (JSON-in-YAML field serialization). Gateway crashed on restart. Then `hermes gateway restart` kept failing because a stale `--replace` process from another agent's fix was still alive. Had to kill all processes first, then restart clean. The cascade of stale-PID + token-rejection in logs made diagnosis harder — the real issue was the stale process, not the token.

### Mode 9: `hermes config set` serializes YAML lists as JSON strings (2026-07-11)

**Symptom:** After using `hermes config set telegram.allowed_chats '[...]'`, the gateway starts but ignores the new chat IDs. Messages from newly added groups/users are silently dropped. Gateway logs may show config parse warnings.

**Root cause:** `hermes config set` serializes list values as JSON strings wrapped in single quotes, not proper YAML lists:
```yaml
# BROKEN — JSON string, not YAML list
allowed_chats: '["-100xxx", "-200xxx"]'

# CORRECT — proper YAML list
allowed_chats:
  - '-100xxx'
  - '-200xxx'
```

The gateway reads YAML and gets a string where it expects a list. It silently ignores the malformed field.

**Fix — Python YAML rewrite:**
```bash
python3 -c "
import yaml, json
with open('/root/.hermes/config.yaml') as f:
    data = yaml.safe_load(f)
ac = data['telegram']['allowed_chats']
if isinstance(ac, str):
    data['telegram']['allowed_chats'] = json.loads(ac)
frc = data['telegram']['free_response_chats']
if isinstance(frc, str):
    data['telegram']['free_response_chats'] = json.loads(frc)
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
print('Fixed — proper YAML lists')
"
```

**Prevention:** After ANY `hermes config set` that touches lists, verify:
```bash
grep -A 10 'allowed_chats' /root/.hermes/config.yaml | head -12
# Should show YAML list items starting with `- '`, NOT a JSON string
```

**Lesson (2026-07-11):** `hermes config set` is safe for scalar values (strings, booleans, numbers) but corrupts list/array values. For lists, either edit the YAML directly or use the Python fix above. Always verify after setting.

### Mode 10: Telegram group migration changes chat ID (2026-07-11)

**Symptom:** `hermes send` to a known group returns: `Telegram send failed: Group migrated to supergroup. New chat id: -100XXXXXXXXXX`. Bot was working in that group before; now silently ignores all messages.

**Root cause:** Telegram upgraded the group to a supergroup. This changes the chat ID. Old ID (e.g. `-5316953867`) is permanently invalid. New ID (e.g. `-1003721331017`) must replace it everywhere.

**Fix:** Update ALL config locations:
1. `telegram.allowed_chats` — replace old ID with new
2. `telegram.free_response_chats` — replace old ID with new
3. Verify no other references to old ID in config

```bash
# Find the new ID from the error message or gateway logs
grep "migrated" /root/.hermes/logs/gateway.log | tail -5

# Update config
hermes config set telegram.allowed_chats '["-1003721331017", ...]'
hermes config set telegram.free_response_chats '["-1003721331017", ...]'

# Fix JSON-in-YAML (Mode 9)
python3 -c "..."  # (see Mode 9 fix)

# Restart gateway
hermes gateway restart
```

**Lesson (2026-07-11):** When a user says "bot stopped working in group X" and it was working before, check for group migration first. The error message includes the new chat ID. Update both `allowed_chats` AND `free_response_chats`.

### Mode 11: `hermes send` fails — bot_token_env mismatch (2026-07-11)

**Symptom:** `hermes send` returns `Telegram send failed: You must pass the token you received from https://t.me/Botfather!` even though the gateway works fine.

**Root cause:** `telegram.bot_token_env` in config.yaml points to `TELEGRAM_BOT_TOKEN` but the actual env var in `.hermes/.env` is `ASI_ARIFOS_BOT_TOKEN`. The CLI resolves the wrong variable name.

**Fix (two parts):**
```bash
# Part 1: Fix config to point to correct env var
hermes config set telegram.bot_token_env ASI_ARIFOS_BOT_TOKEN

# Part 2: For immediate use, export the var before calling
export TELEGRAM_BOT_TOKEN="$ASI_ARIFOS_BOT_TOKEN"
hermes send -t telegram:<chat_id> "message"
```

**Verification:** Check that the env var name matches:
```bash
grep bot_token_env /root/.hermes/config.yaml
grep -E 'BOT_TOKEN' /root/.hermes/.env
# Both should reference the SAME variable name
```

**Lesson (2026-07-11):** The gateway and `hermes send` CLI resolve tokens differently. The gateway reads `.env` directly; the CLI uses `bot_token_env` from config to find the right key. If they disagree, gateway works but CLI fails. Always verify `bot_token_env` matches the actual variable name in `.env`.

## Verification After Restoration

```
✅ systemctl --user is-enabled <unit>          → enabled
✅ systemctl --user status <unit>              → active (running)
✅ curl -sf -m 3 :<port>/health                → OK
✅ ps aux | grep <service>                     → PID present
✅ Survives: terminal session end + reboot     → systemd managed
```

If any check fails, you have a deeper issue — re-probe, don't assume the same fix twice.