# Telegram Bots — Federation Inventory (2026-07-24)

## Three Bots — Role Mapping

| Bot ID | Username | Token Prefix | Owner | Role |
|--------|----------|-------------|-------|------|
| 8410138119 | @ASI_arifos_bot | 84101... | **Hermes Agent** | Conversation, judgment, memory |
| 8149595687 | @AGI_ASI_bot | 81495... | **OpenClaw (🦞 AGI)** | Machine ops, search, forge |
| 8727562763 | @arifOS_bot | 87275... | **777 FORGE** | Sovereign execution, seals |

**Key rule:** The **running process's environment** (`/proc/PID/environ`) is the single source of truth for which token is actually in use. Config files (vault.env, vault.flat.env, openclaw.json) can drift, be stale, or have `$VAR` references that resolve differently per process.

## Multi-Source Bot Liveness Verification

**Critical discipline:** Do NOT declare a bot dead from a single failed probe. Cross-reference ALL sources before concluding.

### Source 1 — Running Process Env (AUTHORITATIVE)

```bash
# Find the process
PID=$(pgrep -f "opencode-bot/bot.py" | head -1)
# Or for gateway: PID=$(pgrep -f "openclaw.*gateway" | head -1)

# Extract the actual token in use
cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep '^TELEGRAM_BOT_TOKEN='
```

### Source 2 — Telegram API Probe

```bash
TOKEN=$(cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep '^TELEGRAM_BOT_TOKEN=' | cut -d= -f2-)
# Use Python (not shell) for reliable token parsing — tokens contain colons
python3 -c "
import urllib.request, json
t = open('/proc/$PID/environ','rb').read().decode('latin-1').split('\x00')
for e in t:
    if e.startswith('TELEGRAM_BOT_TOKEN='):
        token = e.split('=',1)[1]
        resp = urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
        data = json.loads(resp.read())
        print(f'getMe ok={data[\"ok\"]} | @{data[\"result\"][\"username\"]} | {data[\"result\"][\"first_name\"]}')
"
```

### Source 3 — Static Config Files

```bash
# vault.env — exported vars (may differ from flat)
grep 'TELEGRAM_BOT_TOKEN' /root/.secrets/vault.env
# vault.flat.env — used by systemd EnvironmentFile
grep 'TELEGRAM_BOT_TOKEN' /root/.secrets/vault.flat.env
# openclaw.json — may have $VAR reference, not literal token
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); print(d.get('channels',{}).get('telegram',{}).get('botToken','?'))"
```

### Source 4 — Webhook Info

```bash
TOKEN=<token from process env>
python3 -c "
import urllib.request, json
resp = urllib.request.urlopen(f'https://api.telegram.org/bot{TOKEN}/getWebhookInfo', timeout=10)
info = json.loads(resp.read())['result']
print(f'URL: {info.get(\"url\")}')
print(f'Pending: {info.get(\"pending_update_count\")}')
print(f'Last error: {info.get(\"last_error_message\")}')
print(f'Max connections: {info.get(\"max_connections\")}')
"
```

### Cross-Reference Matrix

| Source | What It Tells You | Pitfall |
|--------|-------------------|---------|
| `/proc/PID/environ` | Actual token the process uses | `cut -d=` can fail on tokens with colons — use Python |
| Telegram `getMe` | Bot is alive + token valid | 401 = token revoked/different; not a connection error |
| Telegram `getWebhookInfo` | Webhook URL, error history | `last_error_message` can show 502 = gateway issue, not token issue |
| `vault.env` | Exported env var (for Hermes) | Multiple `TELEGRAM_BOT_TOKEN` lines exist; order matters |
| `vault.flat.env` | Systemd EnvironmentFile | Auto-generated; may have stale token if not regenerated |
| `openclaw.json` | Gateway config | `botToken: \${VAR}` is a reference, not a literal — resolve at runtime |

### False-Death Prevention (Proven 2026-07-24)

**NEVER** declare a bot dead from a single 401/502 unless you have verified:
1. The token matches what the **running process** has (not what vault.flat.env says)
2. `getMe` was called with the exact token from Source 1
3. The error is 401 (Unauthorized = token problem), not 502 (Bad Gateway = webhook/network problem)

**Common false flags:**
- 502 Bad Gateway on webhook → gateway port unreachable, Caddy misrouted, or gateway process crashed — **not** token revocation
- `curl` with shell token extraction failing → check if `cut -d=` parsed correctly; tokens contain `:` and alphanumeric chars
- Vault.env having both `export TELEGRAM_BOT_TOKEN=84101...` AND `TELEGRAM_BOT_TOKEN=81495...` (non-exported) → they serve different processes; OpenClaw's opencode-bot uses vault.flat.env which has the 81495 token, while Hermes uses the exported 84101 token

## Webhook Diagnosis Pattern

```bash
# 1. Check gateway process and port
ps aux | grep openclaw | grep -v grep
ss -tlnp | grep <port>

# 2. Check Caddy config
grep -A10 '<domain>' /etc/caddy/Caddyfile

# 3. Test local endpoint
curl -sf -m 5 http://127.0.0.1:<port>/telegram-webhook \
  -X POST -H "Content-Type: application/json" \
  -d '{"update_id":0}' 2>&1

# 4. Check Telegram's view
getWebhookInfo (see Source 4 above)

# 5. If 502, check gateway logs
journalctl -u openclaw-gateway --no-pager -n 20
```

## Model Chain Diagnostic (OpenClaw)

OpenClaw's model chain lives in `/root/.openclaw/openclaw.json` at `agents.defaults.model`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax/MiniMax-M3",
        "fallbacks": ["groq/llama-3.1-8b-instant", "..."]
      }
    }
  }
}
```

**CRITICAL SCHEMA PITFALL — Model must be at `agents.defaults.model`, NOT root level (Proven 2026-07-24).**

OpenClaw gateway rejects configs with a `model` key at the JSON root:
```
Invalid config: <root>: Unrecognized key: "model"
```
The gateway then silently falls back to its last valid config or startup defaults. The primary model never changes — only the fallback latency grows as the dead hops spew errors no operator sees.

**Correct location:** `openclaw.json.agents.defaults.model`
**Wrong location:** `openclaw.json.model`

When using `python3` to write model config:
```python
# WRONG — root level, gateway rejects
d['model'] = {'primary': '...', 'fallbacks': [...]}

# CORRECT — under agents.defaults
d.setdefault('agents', {}).setdefault('defaults', {})['model'] = {
    'primary': 'minimax/MiniMax-M3',
    'fallbacks': [...]
}
```

If you accidentally put it at root (e.g., after copying from a template that had `model` as top-level):
1. Pop root model: `d.pop('model')`
2. Move to `agents.defaults.model`: `d['agents']['defaults']['model'] = model_config`
3. Restart gateway: `systemctl restart openclaw-gateway`
4. Verify: journalctl output shows `agent model: <new-primary>` (not "Invalid config")

### Current Chain Status

Check primary + fallbacks:
```bash
python3 -c "
import json
d = json.load(open('/root/.openclaw/openclaw.json'))
m = d.get('agents',{}).get('defaults',{}).get('model',{})
print(f'Primary: {m.get(\"primary\")}')
for i, fb in enumerate(m.get('fallbacks',[])):
    print(f'  Fallback {i+1}: {fb}')
"
```

Common failure codes: 402 (payment required / quota), 404 (route not configured / model name wrong), 429 (rate limited), 401 (invalid key). The cascade is silent — OpenClaw falls through without reporting which step failed.

Known broken chain (2026-07-24):
- `kimi-coding/k3` via openrouter → **402 billing** (quota exhausted)
- `bailian-token-plan/kimi-k3` → **404 model not found** (not available on Bailian)
- Falls through to `minimax/MiniMax-M3` → **200 OK** (working fallback, slower)

Fix: swap primary to a working model or top up OpenRouter credits.

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

**Root cause (historical):** Gateway restart loop — systemd keeps trying to start new instance, hitting "port already in use" (exit code 78), repeating. Each failed attempt = "LLM request failed" visible to Arif. Also: model cascade failing at primary and first fallback before hitting a working model (slow).

**Fix:**
```bash
systemctl restart openclaw-gateway
sleep 5
systemctl status openclaw-gateway --no-pager | head -10
journalctl -u openclaw-gateway --no-pager -n 10 | grep -v "^--"
```

**To improve model cascade latency:** Swap the primary to a model that works (e.g. `deepseek/deepseek-v4-flash` or `minimax/MiniMax-M3`), or fix the failing API keys.

## OpenCode Bot Model — Separate from CLI Config

`/root/.config/opencode/opencode.json` controls CLI and ACP delegate_task.
`/root/.openclaw/workspace/bots/opencode-bot/bot.py` controls the Telegram bot.

Both must be updated independently when switching models.

## Bot Logo / Profile Photo Management

Telegram bot profile photos are set via the `setMyPhoto` API method:

```bash
# Set new profile photo (requires curl + multipart upload)
TOKEN=<process token from /proc/PID/environ>
curl -F "photo=@/path/to/photo.png" "https://api.telegram.org/bot${TOKEN}/setMyPhoto"
```

### Requirements
- Photo must be **square** (Telegram crops to circle)
- Minimum: 128×128px
- Maximum: 640×640px (recommended: 512×512)
- Format: PNG or JPEG
- **Cannot delete a bot's profile photo via API** — only `setMyPhoto` (update) is available; there is no `deleteMyPhoto`. To "remove" a photo, set a transparent/placeholder image.

### Workflow for Upgrading Bot Logo

When Arif asks to "upgrade telegram logo" for bots:

1. **Identify what's wanted** — new custom design vs existing asset
2. **Existing assets** (on VPS):
   - `/root/arif-sites/sites/shared/arifos-logo.png` — 1024×1024, stone A+fire, for arifOS branding
   - `/root/arifOS/static/arifos/apex-theory-logo.jpg` — 960×960, geometric Y
   - `/root/arif-sites/sites/shared/profile-avatar.jpg` — 1024×1024, Arif silhouette+brain
3. **Image generation** (for NEW designs) — use lightweight-image-generation skill or token-plan-image skill
4. **Resize to 512×512** — optimal for Telegram profile photos
5. **Upload via API** to each bot's token

### View Current Photo

```bash
# Download current photo (getUserProfilePhotos works for bots too)
TOKEN=<process token>
curl -sf -m 10 "https://api.telegram.org/bot${TOKEN}/getUserProfilePhotos?user_id=<BOT_ID>&offset=0&limit=1"
# Get the largest file_id, then getFile + download
```

### Federation Bot Photo Reference (2026-07-24)

| Bot ID | Username | Current Photo | Design |
|--------|----------|--------------|--------|
| 8410138119 | @ASI_arifos_bot | ✅ Ω + ASI neon circuit logo | Black bg, red/blue Ω with circuit patterns, "AUTONOMOUS • SOVEREIGN • INFINITE" tagline |
| 8149595687 | @AGI_ASI_bot | ✅ Penrose triangle AGI logo | Black bg, red/blue/yellow impossible triangle with circuit traces, "AGI • ADAPT • GENERATE • INTEGRATE" |
| 8727562763 | @arifOS_bot | ⚠️ Default/no photo | 777 FORGE bot — no branded photo set |
| AAA group | -1003753855708 | ? | Group avatar cannot be set via API — must be uploaded manually in Telegram app by a group admin |

### AAA Group Avatar Constraint
Group/supergroup avatars CANNOT be set via the Bot API. Only a group admin with Telegram client (mobile/desktop) can upload a group photo. An agent cannot automate this. If Arif wants a new AAA group logo, the image must be delivered as a file for manual upload via Telegram app.

### Sops/Secrets Token Redaction Pattern (Discovered 2026-07-24)

**The vault.env file is NOT the runtime source of truth for secrets.** All token values in both `vault.env` and `vault.flat.env` are redacted with `***`. The real tokens exist in a sops/age-encrypted layer:

- Decryption binaries: `/usr/local/bin/sops` + `/usr/local/bin/age`
- Key file: `/root/.config/sops/age/`
- Runtime: systemd services load `vault.flat.env` as `EnvironmentFile`, but the decryption happens via secure launch scripts (`openclaw-gateway-secure.sh`, `hermes-gateway-secure.sh`) BEFORE the process executes

### Implications for Debugging
- `grep TELEGRAM_BOT_TOKEN vault.env` returns `***` — this is EXPECTED, not a sign of corruption
- `source vault.env` in a **fresh** shell also resolves to `***` — the real tokens aren't stored in plaintext
- The only reliable source of truth for a running process's token is `/proc/PID/environ`
- **Backup files** (`vault.flat.env.bak-*`) may contain historical plaintext tokens — these are NOT authoritative current state
- All three `TELEGRAM_BOT_TOKEN` lines (lines 139, 140 with 84101..., line 377 with 81495...) are equally valid at source time — the LAST exported line wins for `$TELEGRAM_BOT_TOKEN`, but Hermes uses `HERMES_TELEGRAM_BOT_TOKEN`/`ASI_BOT_TOKEN` which is its own variable
- **Do NOT grep vault.env to conclude a token is dead.** Source it in a subshell and test the resulting env, or check `/proc/PID/environ` on the running process

### Token Recovery Path
If a running bot's token was lost or suspected dead:
1. Find the running process: `pgrep -f openclaw-gateway` or `pgrep -f hermes.*gateway`
2. Extract from `/proc/PID/environ`: `cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep 'TELEGRAM_BOT_TOKEN'`
3. If process isn't running, check sops-encrypted backups in `/root/.secrets/*.bak*`
4. The gateway launch scripts source `vault.env` which has access to the decrypted layer via sops — `systemctl restart <service>` re-decrypts automatically
