# Telegram Bot Token Verification

Verify which Telegram bot a token actually controls, detect redacted tokens, and understand the multi-bot architecture in the arifOS federation.

## Why This Matters

The arifOS federation runs **three distinct Telegram bots** with separate tokens. Misidentifying which token controls which bot causes routing failures and bot downtime. `vault.env` can have duplicate or redacted token definitions — trusting `grep` or `source` alone is insufficient.

## Three-Bot Architecture

| Bot | Username | Token Bot ID | Purpose | Env Var |
|---|---|---|---|---|
| **Hermes Agent** | @ASI_arifos_bot | 8410138119 | Arif's DM + group gateway | `ASI_BOT_TOKEN` / `HERMES_TELEGRAM_BOT_TOKEN` |
| **OpenClaw AGI** | @AGI_ASI_bot | 8149595687 | Public AGI gateway | `TELEGRAM_BOT_TOKEN` (line 377) |
| **777-FORGE** | @arifOS_bot | 8727562763 | OpenCode forge execution | `FORGE_BOT_TOKEN` |

## Token Verification Pattern

### Step 1: Get the raw token value

```bash
# From vault.env - get the actual value, not the masked version
python3 << 'PYEOF'
with open('/root/.secrets/vault.env') as f:
    for line in f:
        if 'TELEGRAM_BOT_TOKEN' in line and '=' in line:
            val = line.split('=', 1)[1].strip().strip('"').strip("'")
            # Skip redacted tokens
            if '***' in val:
                print(f"❌ REDACTED: {val}")
                continue
            bot_id = val.split(':')[0]
            print(f"Token: {val[:15]}...{val[-5:]}")
            print(f"Bot ID: {bot_id}")
            # Test against API
            import subprocess, json
            result = subprocess.run(
                ['curl', '-sf', '-m', '5', f'https://api.telegram.org/bot{val}/getMe'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                d = json.loads(result.stdout)
                r = d['result']
                print(f"✅ @{r['username']} — {r['first_name']}")
            else:
                print("❌ Token invalid or network issue")
            print()
PYEOF
```

### Step 2: Check for **duplicate definitions**

```bash
# vault.env can have MULTIPLE lines defining the same var
grep -n 'TELEGRAM_BOT_TOKEN' /root/.secrets/vault.env
```

**Behaviour:** When `source`-ing, **the LAST definition wins**. If earlier lines are valid and the last is redacted (`***`), the valid ones are shadowed.

```bash
# Check how many definitions exist for each token var
for var in TELEGRAM_BOT_TOKEN ASI_BOT_TOKEN FORGE_BOT_TOKEN HERMES_TELEGRAM_BOT_TOKEN; do
    count=$(grep -c "^export ${var}=" /root/.secrets/vault.env 2>/dev/null || echo 0)
    echo "$var: $count definition(s)"
done
```

### Step 3: Detect redacted tokens

A token value containing `***` has been **manually redacted** — the secret portion is literally the characters `*`, not the real secret. This is distinct from a token that expired; a redacted token will **always** fail API calls.

**Recovery:** Check backups — vault.env backups often contain the working token that was later replaced with a redacted one:
```bash
# Find working tokens in all vault backups
python3 << 'PYEOF'
import os, requests, glob

# Search all vault.env sources
sources = ["/root/.secrets/vault.env"] + \
    sorted(glob.glob("/root/.secrets/vault.env.bak-*"), reverse=True) + \
    ["/root/AAA/agents/hermes-asi/runtime/.env"]

target_bot_id = "8149595687"  # the bot ID you need

for src in sources:
    if not os.path.exists(src):
        continue
    with open(src) as f:
        for line in f:
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if target_bot_id in line and "=" in line:
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if "***" in v:
                    continue  # skip redacted
                try:
                    r = requests.get(f"https://api.telegram.org/bot{v}/getMe", timeout=5)
                    d = r.json()
                    if d.get("ok"):
                        print(f"✅ FOUND: {os.path.basename(src)} — @{d['result']['username']}")
                        print(f"   Token: {v[:15]}...{v[-10:]}")
                    else:
                        print(f"❌ {os.path.basename(src)}: {d.get('description','')[:50]}")
                except:
                    print(f"⚠️ {os.path.basename(src)}: network error")
PYEOF
```
This pattern proved essential when the current `vault.env` had a revoked token but the backup `vault.env.bak-pre-copilot-byok-20260702T052733` contained the working one. **Proven 2026-07-24.**

### Step 4: Check bot profile photos

```bash
TOKEN="<the actual token>"

# Check if bot has a profile photo
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getUserProfilePhotos?user_id=<BOT_ID>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"result\"][\"total_count\"]} photo(s)')"

# Download the largest photo
FILE_ID=$(curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getUserProfilePhotos?user_id=<BOT_ID>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['photos'][0][-1]['file_id'])")
FILE_PATH=$(curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getFile?file_id=${FILE_ID}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['file_path'])")
curl -sf -m 10 "https://api.telegram.org/file/bot${TOKEN}/${FILE_PATH}" -o bot_photo.jpg
```

### Step 5: Set a new bot profile photo via `setMyProfilePhoto`

The correct endpoint is `setMyProfilePhoto` (NOT `setMyPhoto`). It requires an `InputProfilePhotoStatic` JSON object with `attach://` file reference in multipart format:

```bash
TOKEN="<the actual token>"

# Upload profile photo — correct format (Bot API 10.x)
python3 << 'PYEOF'
import requests, json

with open("/tmp/bot_photo.jpg", "rb") as photo:
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/setMyProfilePhoto",
        data={"photo": json.dumps({"type": "static", "photo": "attach://myfile"})},
        files={"myfile": ("logo.jpg", photo, "image/jpeg")},
        timeout=15
    )
d = r.json()
print("✅ Uploaded!" if d.get("ok") else f"❌ {d.get('description')}")
PYEOF
```

**Key format details:**
- `data` contains JSON: `{"type": "static", "photo": "attach://myfile"}`
- `files` contains the actual file with key matching `attach://` reference
- The file key in `attach://` and `files` dict must match (e.g., `myfile`)
- Returns `{"ok": true, "result": true}` on success

**curl equivalent (NOT recommended — curl struggles with nested JSON + multipart):**
```bash
# Avoid curl for this — use Python requests.
# The JSON-in-multipart format is tricky with curl's -F flag.
```

### Step 5b: Remove a profile photo

```bash
curl -sf -m 5 -X POST "https://api.telegram.org/bot${TOKEN}/removeMyProfilePhoto" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if d.get('ok') else f'❌ {d.get('description')}')"
```

### Step 5c: Verify profile photo after upload

```bash
BOT_ID="<bot_numeric_id>"
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getUserProfilePhotos?user_id=${BOT_ID}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"result\"][\"total_count\"]} photo(s)')"

## Common Pitfalls

### Pitfall: `setMyProfilePhoto` format pitfalls

The endpoint is `setMyProfilePhoto` (note: `Profile` not just `Photo`). Common mistakes:

- **Wrong method name**: `setMyPhoto` → 404 Not Found. Use `setMyProfilePhoto`.
- **Wrong file format**: Just `-F "photo=@file"` → `"photo isn't specified"`. Must use JSON `{"type": "static", "photo": "attach://myfile"}` + multipart.
- **Wrong JSON key**: `{"type": "static"}` without `"photo"` key → `"can't find field 'photo'"`.
- **Mismatched attach key**: `attach://myfile` in JSON must match the key in `files=` dict.

**There is no way to upgrade a bot's API version** — the server manages this.
If `setMyProfilePhoto` is unavailable (very old bots), fall back to @BotFather:
1. Open @BotFather
2. Send `/setuserpic`
3. Select the bot
4. Upload the image (square, 512x512, PNG/JPEG)

### Pitfall: Confusing 502 gateway error with 401 token rejection

When a bot stops responding:
1. Run **`getMe`** first — if ok:true, the token is valid
2. Run **`getWebhookInfo`** — check `last_error_message` and `pending_update_count`
3. Check the **local gateway process** — is it running, is the port listening?
4. Check the **reverse proxy** (Caddy/Nginx) — does the handle block point to the correct port?

**502 Bad Gateway** in the webhook = gateway connection issue, not token issue.
**401 Unauthorized** on getMe = token invalid/revoked, need @BotFather.

### Pitfall: Webhook last_error_message is a lagging indicator

Telegram's `getWebhookInfo` returns the **last error** the bot encountered. If the
gateway was restarted after the error, the old error message persists in Telegram's
cache until the next inbound update. A stale `last_error_message` with 0 pending
updates usually means "fixed, just not cleared yet."

## Webhook Health Diagnosis

Verify the full Telegram → Caddy → Gateway chain when webhook errors appear:

```bash
TOKEN="<your_token>"

# Step 1: Token validity
echo "=== 1. Token valid? ==="
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getMe" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅' if d.get('ok') else '❌')"

# Step 2: Webhook info
echo "=== 2. Webhook status ==="
curl -sf -m 5 "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)['result']
print(f'URL: {d.get(\"url\")}')
print(f'Pending: {d.get(\"pending_update_count\")}')
print(f'Last err: {d.get(\"last_error_message\", \"none\")}')
print(f'Max conn: {d.get(\"max_connections\")}')
"

# Step 3: Local gateway
echo "=== 3. Gateway process + ports ==="
ps aux | grep -i openclaw | grep -v grep
ss -tlnp | grep -E '8787|8788|18789'

# Step 4: Caddy reverse proxy
echo "=== 4. Caddy route ==="
grep -A5 'telegram-webhook' /etc/caddy/Caddyfile
```

### Pitfall: Multiple definitions of same env var

```bash
# vault.env might have:
export TELEGRAM_BOT_TOKEN="8410138119:VALID"      # line 139
export TELEGRAM_BOT_TOKEN="8410138119:VALID"      # line 140 (duplicate)
export TELEGRAM_BOT_TOKEN=8149595687:***          # line 377 (redacted)
```

**Last one wins** when sourced. The redacted version at line 377 shadows the valid ones. To fix, remove the redacted line and restore from backup.

### Pitfall: `source` vs `grep` give different answers

- `source vault.env` → gives you the **last** definition
- `grep TELEGRAM_BOT_TOKEN vault.env` → shows **all** definitions (including duplicates and redacted ones)

Always verify with the Telegram API: `curl https://api.telegram.org/bot$TOKEN/getMe`

### Pitfall: OpenClaw's openclaw.json references env var by name

OpenClaw's `openclaw.json` uses `${TELEGRAM_BOT_TOKEN}` — it reads from the environment, not the token directly. If `$TELEGRAM_BOT_TOKEN` resolves to a redacted or wrong value, OpenClaw's bot is dead. Fix the env var, not openclaw.json.
