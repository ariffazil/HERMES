# iPhone Storage Troubleshooting — Syed (iPhone 11 Pro Max, 64GB)
## Apple ID: khairuddinkudin@yahoo.com | Proven: 2026-07-22/23

## Symptom Checklist

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Telegram can't open chats | App cache >2GB, phone <5GB free | Clear cache or reinstall |
| "Agent banned my Telegram" | **Never a ban. Always storage.** | Check gateway logs to prove |
| WhatsApp stuck loading | Documents & Data >4GB | Clear media from inside app |
| App Store asks password | Face ID not enabled for purchases | Reset password then enable |
| Phone says "Storage Full" | 58GB+ used of 64GB | 3-step cleanup below |

## Diagnosis (agent side)

1. Check raw gateway logs: `grep "1042200555" ~/.hermes/logs/gateway.log | grep -i "block\|ban\|denied\|error"`
2. If no blocks → ask for `Settings → General → iPhone Storage` screenshot
3. If top 3 apps >20GB → phone choking, NOT banned
4. Declare: "No ban. Agent takde ego. Phone je penuh."

## Cleanup Sequence

### 1. Quick Wins (no data loss)
- Settings → iPhone Storage → Photos → Recently Deleted → Delete All **(2.12 GB free)**
- Telegram → Settings → Data & Storage → Storage Usage → Clear Cache **(~2 GB free)**
- Messages → Review Large Attachments → delete media **(~730 MB free)**

### 2. WhatsApp (in-app only, NEVER delete from iPhone Storage)
- WhatsApp → Settings → Storage and Data → Manage Storage
- Delete forwarded videos, old memes (target: cut 4GB → 2GB)
- **⚠️ NEVER `Settings → iPhone Storage → WhatsApp → Delete App`** — chat history NOT in iCloud

### 3. Nuclear: Delete & Reinstall Telegram
- Settings → iPhone Storage → Telegram → Delete App
- Chat history SAFE in Telegram cloud — auto-restore on login
- **CRITICAL after reinstall:** Settings → Data & Storage → Auto Media Download → **OFF semua** BEFORE opening any chat
- Open important chats first (SADO, ASI). Archive/Premium last.

## Apple ID Password Reset
Phone passcode method (preferred): `Settings → [name] → Sign-In & Security → Change Password` → enter iPhone passcode → set new
Web: `iforgot.apple.com` → reset link to khairuddinkudin@yahoo.com
**After reset:** Settings → Face ID & Passcode → ON "iTunes & App Store" → never type password again

## Prevention
- Telegram: OFF all auto-download
- Photos: iCloud ON (50GB = RM3.90/mo)
- WhatsApp: monthly media cleanup
