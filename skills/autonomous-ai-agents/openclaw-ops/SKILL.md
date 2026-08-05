---
name: openclaw-ops
description: Operate, diagnose, and integrate an OpenClaw installation — gateway health, chat channels, Telegram bot wiring, and chat-bridging. Use when the user asks "is OpenClaw up / down", "I want OpenClaw here/in this chat", OpenClaw stops responding on Telegram, or a new channel/account needs wiring. Federation-specific topology for Arif's arifOS stack lives in references/arifos-federation-map.md.
---

# OpenClaw Operations

OpenClaw (formerly Clawdbot/Moltbot) is a multi-channel AI agent gateway: one agent, many chat surfaces (Telegram, WhatsApp, Discord, Slack…). On this box it runs as **bare-metal systemd services**, not Docker.

## Trigger conditions
- "I want OpenClaw here" / "OpenClaw isn't answering" / "is OpenClaw up?"
- Wiring or fixing a Telegram/Discord/etc. channel
- Deciding whether to bridge OpenClaw into another chat vs. pointing the user at OpenClaw's own bot

## Probe sequence (probe before act — always)

1. **Systemd units** — `systemctl list-units --all | grep -i claw` and `systemctl status openclaw-gateway --no-pager`. Look for the service names: `openclaw-gateway`, `openclaw-bot` (may be a custom Telegram bot, not OpenClaw itself), `openclaw-restart.path`.
2. **Gateway health** — `curl -s http://127.0.0.1:<port>/health` → expect `{"ok":true,"status":"live"}`. Gateway port is typically 18789.
3. **CLI status** — `openclaw status` (fast overview) and `openclaw channels status --probe` (the money command: per-channel live state).
4. **Channel state** — `openclaw channels list`. The probe output tells you everything: `Telegram default (@BOT): enabled, configured, running, connected, mode:webhook, works, audit ok`.
5. **Telegram activity** — `journalctl -u openclaw-gateway --no-pager -n 400 | grep -iE "telegram"` → look for `Inbound message telegram:<id> -> @bot (direct…)` and `outbound send ok … threadId=…` lines. Recent in/out lines = channel is alive end-to-end.
6. **Env/token wiring** — `systemctl cat openclaw-gateway` for `EnvironmentFile` + drop-in overrides; `grep -oE '\$\{[A-Z_]*\}' <config>` to see which env vars the config expects.

## Critical pitfalls

- **`jq '.channels.telegram.token'` returning null does NOT mean no token.** OpenClaw config names the token fields `botToken` (often `${ENV_VAR}`) and `tokenFile` (a path). Check BOTH before concluding the channel is unconfigured. A naive `token_set: false` verdict was wrong here — the channel was fully live via `tokenFile`.
- **The gateway API is WebSocket, not HTTP REST.** `curl :18789/api/v1/status` → `Not Found` is normal. Use the CLI (`openclaw message send …`) for outbound sends, not HTTP.
- **Webhook mode**: local listener on `127.0.0.1:8787/telegram-webhook` (or similar) fronted by a public URL (Caddy/Cloudflare). `openclaw doctor --fix` repairs drifted config.
- **Separate bots = separate DM threads.** If the user is in Hermes' DM and wants "OpenClaw here", OpenClaw cannot join that thread — it's a different bot account. Options: (a) DM OpenClaw's bot directly (user ID must be in `allowFrom`), (b) use a shared group where OpenClaw has `groupPolicy: open, requireMention: false` — both agents respond there. Don't build a bridge before stating this.
- **Non-blocking config warnings**: missing plugins (brave/acpx/discord/exa/firecrawl/perplexity) only disable that optional provider (e.g. `web_search`), they don't kill the channel. Ollama down → L5 memory sync fails (`ECONNREFUSED 127.0.0.1:11434`) but Telegram is unaffected. Report these as footnotes, not as "OpenClaw is broken".
- **Secrets**: tokens live in mode-600 files (e.g. `/root/.secrets/tokens/<name>`); env override via systemd drop-in `Environment="TELEGRAM_BOT_TOKEN=…"`. Never paste token values into chat.

## Verification / response contract
- Lead with the verdict: "OpenClaw is live / down" + one evidence line (probe output or journal line).
- If working: give the user the *instant path* (DM the bot / use the group) and only then offer a bridge as an option — the bridge is a build decision, not a default.
- If down: report the failing unit + last error lines + the repair path (`systemctl restart openclaw-gateway` is T1-class; federation-wide restart is not).

## Support files
- `references/arifos-federation-map.md` — Arif's three-layer Telegram architecture (Hermes SOUL / OpenClaw GUTS / 777-FORGE HANDS), bot handles, token paths, gateway config shape, and observed journal signatures.
