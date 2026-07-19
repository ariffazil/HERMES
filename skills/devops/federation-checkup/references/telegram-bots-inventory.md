# Telegram Bots — Federation Inventory (2026-07-10)

## Three Bots, Three Owners

| Bot | Token Env | Owner | Purpose |
|-----|-----------|-------|---------|
| `@ASI_arifos_bot` | Hermes config | **Hermes** | This session (Arif ↔ Hermes) |
| `@arifOS_bot` | `TELEGRAM_BOT_TOKEN` | **OpenCode** | Code execution via Telegram |
| `@AGI_ASI_bot` | `TELEGRAM_BOT_TOKEN` | **OpenClaw** | AGI gateway, LLM requests |

## Telegram Conflict Diagnostic (OpenCode/OpenClaw)

**Symptom:** `telegram.error.Conflict: terminated by other getUpdates request`

**Root cause:** Multiple bot instances fighting for Telegram polling connection. Telegram allows exactly ONE polling connection per bot token.

**Check:**
```bash
# How many Telegram connections per bot?
lsof -i :443 2>/dev/null | grep python3 | grep telegram
# Should be 2 (long poll + webhook fallback) per bot instance
# 4 lines = 2 bots both running = conflict

# Which process owns what?
ps aux | grep -E "bot.py|openclaw.*gateway" | grep -v grep
```

**Resolution — systematic:**
```
Step 1: systemctl stop opencode-bot
Step 2: pkill -9 -f "opencode-bot/bot.py"   # kill ALL orphans
Step 3: pkill -9 -f "openclaw.*gateway"     # also kill orphans if needed
Step 4: lsof -i :443 | grep telegram         # should be 0 connections now
Step 5: systemctl start opencode-bot
Step 6: sleep 5 && lsof -i :443 | grep telegram  # verify 2 connections restored
```

**Key rule:** Never `python3 bot.py` manually. Systemd must own the single instance.

**Post-restart behavior:** Telegram holds the old polling session for ~60s after kill. New instance gets Conflict errors during this window. Self-clears automatically — do NOT keep restarting during the 60s window.

## OpenClaw Gateway — LLM Request Failed

**Root cause (historical):** Gateway restart loop — systemd keeps trying to start new instance, hitting "port already in use" (exit code 78), repeating. Each failed attempt = "LLM request failed" visible to Arif.

**Fix:**
```bash
systemctl restart openclaw-gateway
sleep 5
systemctl status openclaw-gateway --no-pager | head -10
journalctl -u openclaw-gateway --no-pager -n 10 | grep -v "^--"
```

**Model switch (2026-07-10):** OpenClaw primary switched from `xiaomi-coding/mimo-v2.5-pro` (exhausted) to `bailian-token-plan/deepseek-v4-pro`. Config at `/root/.openclaw/openclaw.json` → `agents.defaults.model.primary`.

## OpenCode Bot Model — Separate from CLI Config

`/root/.config/opencode/opencode.json` controls CLI and ACP delegate_task.
`/root/.openclaw/workspace/bots/opencode-bot/bot.py` controls the Telegram bot.

Both must be updated independently when switching models.
