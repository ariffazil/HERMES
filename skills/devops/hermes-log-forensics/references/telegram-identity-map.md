# arifOS Federation — Telegram Identity Map

> Known mappings between Telegram display names (as logged in gateway logs)
> and actual human identities. The gateway log truncates display names at the
> first space (`user=` field), so `user=No` means "No name", etc.
>
> Last updated: 2026-07-28

| `user=` (log) | Actual Person | Telegram Chat ID | Channels Used | Notes |
|---|---|---|---|---|
| `No` | **Syed** (Abang Sado @rico_ricaldo_33) | 1042200555 | DM + Group -1003815535761 | Heavy daily user — nasi lemak ops, supplements, social. 964 msgs since Jul 3. |
| `Mohd` | **Izzu** (Izzudin Tajjudin) | 1237635275 | DM + Group -1003521544074 | Burst user — test drove Jul 27, then politics in group. 18 msgs. |
| `al` | **Aliff** (Muhammad Aliff Al Husna) | 1024343313 | DM only | Access granted 28 Jul via F13. 8 msgs first day. |
| `ARIF` | **Arif** (F13 SOVEREIGN) | 267378578 / 8410138119 / multiple | All channels | Owner. 5,395+ msgs. Sovereign. |
| `🦞` / `AGI🦞` | **OpenClaw** (bot agent) | 8149595687 | DM + Group | Not human. |
| `777` / `FORGE🔥` | **OpenCode** (bot agent) | 8727562763 | DM only | Not human. |

## Resolution command

To resolve any Telegram chat ID to a display name:

```bash
grep -A10 '"chat_id": "<CHAT_ID>"' /root/HERMES/sessions/sessions.json | grep display_name
```

## Resolution pitfall

The `sessions.json` shows the Telegram-displayed name at account creation, not necessarily the person's actual name. For example:
- Izzu's Telegram display = "Mohd" (not his actual name)
- Syed never set a display name = "No name" (appears as `No` in logs)

Combine `sessions.json` with context from message content to resolve real identities.
