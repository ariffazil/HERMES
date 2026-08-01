# Runtime Env vs Vault Tracing — service env chain

## The chain (SOT → process)

```
SOT file → generator → flat file → systemd EnvironmentFile → launcher `source` → /proc/<pid>/environ
```

A key can be correct at every earlier link and still missing from the
process. The process env is fixed at boot; nothing re-reads the vault per
request.

## Trace recipe

```bash
# 1. Which unit, which PID
systemctl is-active <unit>
PID=$(systemctl show <unit> -p MainPID --value)

# 2. What systemd injected
systemctl show <unit> -p EnvironmentFile --value
systemctl cat <unit>          # full unit incl. ExecStart launcher script

# 3. What the launcher script sources
cat /usr/local/bin/<launcher>.sh   # look for `source` / `.` lines

# 4. What the process ACTUALLY holds (root can read this)
tr '\0' '\n' < /proc/$PID/environ | grep -iE 'KEY|TOKEN' \
  | sed -E 's/(sk-[A-Za-z0-9]{6})[A-Za-z0-9]*/\1****/g'

# 5. Hermes' own dotenv loader path
# env_loader.py: user_env = Path(HERMES_HOME or ~/.hermes) / ".env"
ls -la ~/.hermes/.env    # absent on arifOS boxes → env comes ONLY from launcher
```

## Worked example — Qwen seat wiring (2026-08-01)

- `kunci-mas.env`: `QWEN_HERMES_API_KEY` REAL (Standard seat sk-sp-D.IPRH),
  `QWEN_OPENCODE_API_KEY` + `QWEN_INDIVIDUAL_API_KEY` REAL (Pro sk-sp-H.DIEXP)
- `config.yaml`: primary `qwen-token-plan/qwen3.7-plus`, key_env
  `QWEN_HERMES_API_KEY` — all correct on disk
- BUT `hermes-asi-gateway.service`:
  - `EnvironmentFile=/root/.secrets/vault.flat.env` (had QWEN_API_KEY /
    QWEN_BAILIAN_KEY, NOT the three new names)
  - launcher `/usr/local/bin/hermes-gateway-secure.sh` sources
    `/root/AAA/agents/hermes-asi/runtime/.env` (22 vars, zero QWEN keys)
  - `~/.hermes/.env` absent → Hermes dotenv loader found nothing
- `/proc/<gateway-pid>/environ`: no `QWEN_HERMES_API_KEY` → restart alone
  would NOT activate the new primary.

**Fix:** add the QWEN_* vars to a file the launcher actually sources
(runtime/.env), OR point the unit's EnvironmentFile at the flat that
contains them — then restart. Verify via `/proc/<pid>/environ` after.

## Worked example — FORGE two-token drift (2026-08-01)

- `/root/.forge/.env` had BOTH:
  - `FORGE_BOT_TOKEN=8727562763:AAA...` → getMe OK (bot @arifOS_bot)
  - `TELEGRAM_BOT_TOKEN=8727562763:BBB...` → 401 Unauthorized
- Gateway reads `TELEGRAM_BOT_TOKEN` (gateway/config.py:1471) → the dead
  one won; gateway stuck in "Telegram rejected" retry loop since Jul 31.
- Fix: sync `TELEGRAM_BOT_TOKEN` to the working value, restart; after
  `systemctl restart` the old PID persisted (`--replace` didn't take) →
  `kill -9 <old-pid>` then restart; verify MainPID changed.

**Detection:** on any token-rejection, test EVERY token var in the env
file against `https://api.telegram.org/bot<TOKEN>/getMe` before
suspecting the bot itself.

## Zen fix pattern (proven 2026-08-01)

Collapse env sprawl to one SOT → one flat → one reader:

```bash
cp vault.flat.env vault.flat.env.bak-zen-fix-$(date +%Y%m%dT%H%M%S)   # backup real file
mv generate-flat.py generate-flat.py.disabled-$(date +%Y%m%dT%H%M%S)  # one generator
rm vault.flat.env && ln -s kunci-mas.flat.env vault.flat.env           # symlink, not copy
sed -i 's|EnvironmentFile=.*vault.flat.env|EnvironmentFile=/root/.secrets/kunci-mas.flat.env|' /etc/systemd/system/<unit>.service
systemctl daemon-reload
readlink -f vault.flat.env && systemctl show <unit> -p EnvironmentFile --value
```
