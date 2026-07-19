# OpenClaw Bot Token Rotation — Session Detail

## Symptom
All Telegram API calls returning 404:
```
[telegram] getMe failed: Call to 'getMe' failed! (404: Not Found)
[telegram] [default] channel exited: Call to 'getMe' failed! (404: Not Found)
[telegram] [default] auto-restart attempt 5/10 in 86s
[telegram] sendMessage failed: Call to 'sendMessage' failed! (404: Not Found)
```

Gateway was running (port 18789 healthy) but Telegram channel completely dead.

## Token storage locations (FOUR files, not three)

| # | File | Used by | Format |
|---|------|---------|--------|
| 1 | `/root/.secrets/vault.flat.env` | systemd `EnvironmentFile` | `KEY="value"` (NO `export` prefix) |
| 2 | `/root/.secrets/vault.env` | `openclaw-gateway-secure.sh` (`source`) | `export KEY="value"` |
| 3 | `/root/.openclaw/.env` | OpenClaw node process (dotenv) | Mixed: SOPS `ENC[]` + plain text |
| 4 | `/root/.openclaw/.env.decrypted` | OpenClaw decrypted vault | `KEY=value` |

**Critical discovery (2026-07-06):** The SOPS-encrypted `.env` (#3) **overrides** vault.env (#2). The node process loads `.env` via dotenv AFTER the shell script sources vault.env. If `.env` has `TELEGRAM_BOT_TOKEN=ENC[...]`, the encrypted (possibly stale) value wins.

## Fix sequence (proven 2026-07-06)

### Step 1: Update vault files (Python, NOT sed/regex)
```python
NEW_TOKEN = "1234567890:AAxxxxxx..."  # full token from @BotFather

for fpath in ['/root/.secrets/vault.env', '/root/.secrets/vault.flat.env']:
    with open(fpath) as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if 'TELEGRAM_BOT_TOKEN' in line and not line.strip().startswith('#'):
            if line.startswith('export'):
                new_lines.append(f'export TELEGRAM_BOT_TOKEN="{NEW_TOKEN}"\n')
            else:
                new_lines.append(f'TELEGRAM_BOT_TOKEN="{NEW_TOKEN}"\n')
        else:
            new_lines.append(line)
    with open(fpath, 'w') as f:
        f.writelines(new_lines)
```

**Why Python, not sed:** Regex substitutions on tokens silently truncate them. Verified: `re.sub()` produced a 10-char token instead of 46-char token. Always verify length after edit.

### Step 2: Update the SOPS .env file
```python
# Option A: Add plain-text line (wins over ENC[])
with open('/root/.openclaw/.env') as f:
    lines = f.readlines()
# Insert before first ENC[] or MINIMAX line
for i, line in enumerate(lines):
    if line.startswith('#ENC') or line.startswith('MINIMAX'):
        lines.insert(i, f'TELEGRAM_BOT_TOKEN={NEW_TOKEN}\n')
        break
with open('/root/.openclaw/.env', 'w') as f:
    f.writelines(lines)

# Option B: Remove the line entirely (vault.env takes effect)
# Only works if vault.env has the correct token
```

**Also add `QWEN_API_KEY`** to `.env` if missing — gateway validates required secrets at startup BEFORE vault.env is sourced. The SOPS backup `.env` from before QWEN was added won't have it.

### Step 3: Update .env.decrypted
```python
with open('/root/.openclaw/.env.decrypted') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.startswith('TELEGRAM_BOT_TOKEN='):
        lines[i] = f'TELEGRAM_BOT_TOKEN={NEW_TOKEN}\n'
        break
with open('/root/.openclaw/.env.decrypted', 'w') as f:
    f.writelines(lines)
```

### Step 4: Kill competing gateways
```bash
# Check what's on port 18789
ss -tlnp | grep 18789
ps aux | grep "openclaw.*gateway\|hermes.*gateway" | grep -v grep

# Stop user-level gateway (needs XDG_RUNTIME_DIR)
XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop openclaw-gateway 2>/dev/null
XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable openclaw-gateway 2>/dev/null
XDG_RUNTIME_DIR=/run/user/0 systemctl --user daemon-reload 2>/dev/null

# Kill any remaining zombies
kill -9 <pid> 2>/dev/null
sleep 2

# Verify port is free
ss -tlnp | grep 18789  # should return nothing
```

### Step 5: Restart system-level gateway
```bash
sudo systemctl restart openclaw-gateway
sleep 15
journalctl -u openclaw-gateway --since "30s ago" | grep "starting provider"
# Expected: [telegram] [default] starting provider (@BotName)
```

### Step 6: Verify
```bash
# Health
curl -sf http://localhost:18789/health

# Bot identity
journalctl -u openclaw-gateway --since "30s ago" | grep -i "webhook\|starting provider\|getMe"

# Token length verification (catches truncation)
python3 -c "
for f in ['/root/.secrets/vault.flat.env', '/root/.openclaw/.env']:
    with open(f) as fh:
        for line in fh:
            if 'TELEGRAM_BOT_TOKEN' in line and not line.strip().startswith('#'):
                val = line.split('=', 1)[1].strip().strip('\"')
                print(f'{f}: len={len(val)} bot_id={val.split(\":\")[0]}')
"

# Send test message
openclaw message send --channel telegram --target <your_user_id> --message "🟢 test"
```

## Complication: vault.flat.env format vs vault.env format

| File | Supports `export` prefix? |
|------|--------------------------|
| `vault.env` (sourced by bash) | Yes |
| `vault.flat.env` (systemd EnvironmentFile) | **NO** — silently ignored |

If you add `export QWEN_API_KEY="..."` to vault.flat.env, systemd ignores the line. Gateway reports `Environment variable "QWEN_API_KEY" is missing or empty`. Always strip `export` prefix for vault.flat.env.

## Complication: user-level gateway respawns after disable

`systemctl --user disable` + `stop` doesn't kill a running process if the terminal session doesn't have the user-level D-Bus context. The process (ppid=1247, user-level systemd) keeps respawning.

**Fix:** Use `XDG_RUNTIME_DIR=/run/user/0` to target root's user-level systemd:
```bash
XDG_RUNTIME_DIR=/run/user/0 systemctl --user stop openclaw-gateway
XDG_RUNTIME_DIR=/run/user/0 systemctl --user disable openclaw-gateway
XDG_RUNTIME_DIR=/run/user/0 systemctl --user daemon-reload
```

Then `kill -9 <pid>` any remaining zombies.

## Complication: QWEN_API_KEY missing after .env restore

Restoring `.env` from an old SOPS backup (pre-QWEN era) loses `QWEN_API_KEY`. Gateway validates required secrets at startup and fails with `SecretRefResolutionError: Environment variable "QWEN_API_KEY" is missing or empty`.

**Fix:** Add `QWEN_API_KEY=<value>` to the `.env` file (plain text, before ENC[] lines). Get the value from `vault.env`:
```bash
bash -c 'source /root/.secrets/vault.env; echo "$QWEN_API_KEY"'
```
