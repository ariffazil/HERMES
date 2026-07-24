# Agent Execution Gaps — SyedOS Limitations & Solutions

## Context

Syed's feedback (2026-07-21): "Hang kalau search cari info apa semua dah ok. Tapi bila bab execution suruh buat benda hang x pandai sangat."

Agent is strong at research, analysis, and explanation. Weak at EXECUTION — doing things on the user's behalf. This document catalogs identified gaps and available MCP server solutions to close them.

---

## Gap 1: MT5 Trading Execution — CRITICAL

**Problem:** Agent gives excellent signals (Brent BUY $88.44 → TP $92.00 hit, +3.04%) but cannot execute trades — even paper trades. All execution must be done manually by Syed.

**Solution:** [MetaTrader MCP Server](https://github.com/ariadng/metatrader-mcp-server)

Available tools:
- `mt5_account_info` — balance, equity, margin
- `mt5_open_order` — BUY/SELL with lot size, SL, TP
- `mt5_close_position` — close by ticket
- `mt5_modify_order` — trail SL, adjust TP
- `mt5_get_positions` — list open positions
- `mt5_get_candles` — real-time OHLCV from MT5 terminal

**Setup path:** Windows machine with MT5 terminal → install Python MCP server → wire to Hermes via config. Credentials in `.env`. PowerShell deployment script needed.

**Impact:** Agent upgrades from "consultant who suggests" to "operator who executes on paper." Phase 2 of Syed's trading system.

---

## Gap 2: Mobile Device Control — HIGH

**Problem:** Syed spent 2+ hours clearing Telegram cache manually. Agent could only give step-by-step instructions. Cannot install apps, manage storage, take screenshots, or troubleshoot device issues hands-on.

**Solutions:**

| Tool | Platform | Capability |
|------|----------|-----------|
| [Android MCP](https://mcpmarket.com/server/android-2) | Android | App navigation, UI interaction, clear cache, install/delete apps |
| [Agent Device (Callstack)](https://www.callstack.com/blog/agent-device-ai-native-mobile-automation-for-ios-android) | iOS + Android | System settings, app management, screen control |
| iOS Shortcuts MCP | iOS | Limited — sandboxed, via Shortcuts actions |

**Constraint:** Syed uses iPhone 11 Pro Max (iOS). iOS sandboxing makes direct agent control harder than Android. Agent Device is the most promising cross-platform solution.

---

## Gap 3: WhatsApp Integration — MEDIUM

**Problem:** Syed's WhatsApp has 4.41 GB Documents & Data. Agent cannot clear storage, search messages, or interact with WhatsApp groups from Hermes.

**Solution:** [WhatsApp MCP Server](https://github.com/lharries/whatsapp-mcp)

- Connects via WhatsApp Web multi-device API (whatsmeow library in Go)
- QR code authentication — scan once, works ~20 days before re-auth
- Tools: search contacts, read/send messages, send media files
- Local SQLite database — messages only sent to LLM when accessed through tools

**Setup path:** Already installed at `/root/whatsapp-mcp/`. Go bridge compiled. Need to start bridge → scan QR → wire as MCP server in Hermes config.

---

## Gap 4: Push Notifications (Backup Channel) — MEDIUM

**Problem:** Telegram is the ONLY communication channel. If Telegram is down (like Syed's phone storage crash), zero way to reach him. 8am gold briefing missed.

**Solution:** [ntfy.sh](https://ntfy.sh) — self-hosted push notification server

- Topics: `hermes-alerts` (system), `trade-signals` (trading)
- iPhone: install ntfy app, subscribe to topics
- VPS: already have ntfy-push.py + ntfy-push wrapper at `/usr/local/bin/`
- Need: Caddy route to expose ntfy server externally

**Usage:**
```bash
ntfy-push trading "BUY XAUUSD $4,100" "Entry $4,100 | SL $4,070 | TP $4,150"
ntfy-push system "Telegram Down" "Briefing will resume when service restored"
```

---

## Gap 5: Financial Execution — LOW

**Problem:** Cannot check TnG balance, process payments, or auto-track nasi lemak revenue.

**Solution:** TnG eWallet API is closed. Internet banking MCP servers exist but not tested. Low priority.

---

## Priority Matrix

| # | Gap | Impact | Difficulty | Timeline |
|---|-----|--------|-----------|----------|
| 1 | MT5 MCP Bridge | Critical | Medium | 1-2 days (need Syed's Windows machine) |
| 2 | WhatsApp MCP | Medium | Easy (already compiled) | 1-2 hours |
| 3 | ntfy Push | Medium | Easy (scripts ready) | 30 min (need Caddy route) |
| 4 | Android/iOS MCP | High | Hard (iOS) | Ongoing research |
| 5 | Finance MCP | Low | Hard | Weeks |

---

## For Next Session

1. Expose ntfy via Caddy tunnel → Syed installs app → test push
2. WhatsApp bridge: `cd /root/whatsapp-mcp/whatsapp-bridge && ./whatsapp-bridge` → QR scan
3. Wire both as MCP servers in Hermes config
4. MT5 Windows deployment: create PowerShell script → Syed runs on his machine
5. iOS mobile control: deeper research on Agent Device, test if Syed can connect iPhone to Mac

---

## Gap 6: Telegram DM Initiation — SOLVED (2026-07-23)

**Problem:** Agent cannot send new DM to Syed — `hermes send` requires separate bot token. Gateway only routes replies, not new conversations.

**Solution:** Extract bot token from running gateway process + direct Telegram Bot API:

```bash
TOKEN=$(cat /proc/$(pgrep -f "hermes gateway run" | head -1)/environ | tr '\0' '\n' | grep "^TELEGRAM_BOT_TOKEN=" | cut -d= -f2)
python3 -c "
import json, urllib.request
data = json.dumps({'chat_id': 1042200555, 'text': 'msg'}).encode()
req = urllib.request.Request(f'https://api.telegram.org/bot${TOKEN}/sendMessage', data, {'Content-Type': 'application/json'})
print(json.loads(urllib.request.urlopen(req)).read())
"
```

**Proven:** 4 messages sent Jul 23 (IDs 92250-92253). Token from gateway process environ is the ONLY working token — config ref `bot_token_env: ASI_ARIFOS_BOT_TOKEN` not exported; extract from `/proc/PID/environ`. Never use `hermes send` for Syed DMs — use this direct API pattern.
