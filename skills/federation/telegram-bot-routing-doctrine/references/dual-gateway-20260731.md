# Dual Gateway Incident — 2026-07-31

## What Happened

Two Hermes gateway processes were running concurrently:

| PID | Started | HERMES_HOME | Token | Origin |
|-----|---------|-------------|-------|--------|
| 1185213 | 21:44 UTC | /root | ASI (8410…) | `hermes-asi-gateway.service` (legitimate) |
| 1201613 | 21:54 UTC | /root/.forge | FORGE (8727…) | `forge-gateway.service` (disabled, manually started) |

## forge-gateway.service

```ini
# /etc/systemd/system/forge-gateway.service
[Unit]
Description=777-FORGE Gateway — @arifOS_bot
After=network.target vault.env.service

[Service]
Type=simple
ExecStart=/usr/local/bin/forge-gateway.sh
Restart=always
RestartSec=5
User=root
Environment=HOME=/root

[Install]
WantedBy=multi-user.target
```

Key facts:
- **Enabled: NO** — `systemctl is-enabled` returns `disabled`
- **Active: YES** — someone ran `systemctl start forge-gateway.service` manually at 21:54 UTC
- **Restart=always** — if killed without stopping the unit, systemd restarts it after 5s
- Drop-in at `forge-gateway.service.d/cron-script-timeout.conf` sets `HERMES_CRON_SCRIPT_TIMEOUT=1200`

## Token Rejection

```json
{
  "gateway_state": "running",
  "platforms": {
    "telegram": {
      "state": "retrying",
      "error_code": "telegram_connect_error",
      "error_message": "The token `8727562763:***` was rejected by the server."
    }
  }
}
```

The FORGE token was rejected because `opencode-bot/bot.py` (PID 1123430) already held the webhook for @arifOS_bot. Telegram blocks a second connection using the same bot token. **Net effect: intruder gateway could not post to AAA group.** Resource waste only.

## Audit Correction

Initial diagnosis incorrectly claimed `opencode-bot` (PID 1123430) was also using FORGE token — the process environ showed no `TELEGRAM_BOT_TOKEN`. The bot.py likely reads the token from its own config/env file rather than inheriting it in the process environment. **Lesson: verify environ before claiming token conflict; absence of token in environ ≠ process isn't using it.**

## Vault Tokens (kunci-mas.env)

| Variable | Prefix | Bot |
|----------|--------|-----|
| `ASI_ARIFOS_BOT_TOKEN` | 8410138119 | @ASI_arifos_bot |
| `ASI_BOT_TOKEN` | 8410138119 | @ASI_arifos_bot (DUPLICATE) |
| `HERMES_TELEGRAM_BOT_TOKEN` | 8410138119 | @ASI_arifos_bot (ALIAS → `${ASI_BOT_TOKEN}`) |
| `TELEGRAM_BOT_TOKEN` | 8149595687 | @AGI_ASI_bot |
| `FORGE_BOT_TOKEN` | 8727562763 | @arifOS_bot |

**3 unique tokens**, 5 variable names. `ASI_BOT_TOKEN` = `ASI_ARIFOS_BOT_TOKEN` (same value).

## Resolution Path

1. `kill -STOP 1201613` — freeze for forensics (SIGSTOP, not SIGKILL)
2. Trace origin → found `forge-gateway.service`
3. `systemctl stop forge-gateway.service` — clean stop with unit awareness
4. If unwanted permanently: `systemctl mask forge-gateway.service`
5. Monitor 60s for rebirth (Restart=always won't fire if unit is stopped, only if process dies while unit is active)
