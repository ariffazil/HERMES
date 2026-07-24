# Scam Investigation Technical Patterns

## QR Code Decoding from Images

When a person shares a QR code card (common in romance/investment scams), decode it programmatically:

```bash
apt-get install -y libzbar0
pip install --break-system-packages pyzbar Pillow

python3 -c "
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('/path/to/image.jpg')
results = decode(img)
for r in results:
    print(f'DATA: {r.data.decode(\"utf-8\")}')
"
```

If pyzbar fails on raw image, try grayscale conversion:
```python
img_gray = img.convert('L')
results = decode(img_gray)
```

### Interpreting Results

| QR Link Pattern | Meaning |
|---|---|
| `t.me/contact/<user_id>:<hash>` | Telegram contact share link |
| `t.me/<username>` | Telegram username/channel |
| `https://t.me/+<invite_hash>` | Telegram group invite |

**t.me/contact links:** The `<hash>` after the colon is the user's access_hash (base10, NOT base36). Use it directly as `InputUser(user_id=..., access_hash=...)` in Telethon.

### Embedding icons in QR centers

Paper airplane → Telegram. Play button → TikTok. Camera → Instagram. These are visual hints — always decode electronically, never guess from the icon.

## Bank Account Tracing (Malaysia)

### GX Bank Account Format
- Prefix: `8888` for individual accounts
- 10-12 digits total
- Digital bank — easy to open, common mule account choice

### Check Databases
```
1. SemakMule (PDRM CCID) — https://semakmule.rmp.gov.my/
2. Bank Negara Malaysia — https://www.bnm.gov.my/financial-consumer-alert-list
3. Web search: "[account number] scam OR penipuan OR keldai akaun"
4. Try different formats: "XXXXXXXXXX", "XXXX XXXX XXXX", "XXXX-XXXX-XXXX"
```

### Pattern: Account number NOT in any public database
This does NOT mean the account is clean. Most mule accounts never appear in public databases. The absence of scam reports is expected, not reassuring. The flag is in the surrounding evidence (mismatched persona, Telegram-only contact, QR code direction).

## Persona Cross-Reference Checklist

When investigating a named person + bank account:

| Source | What to Check | Flag If |
|---|---|---|
| LinkedIn | Job title, company, timeline | Job doesn't match claimed persona |
| Facebook (public) | School, location, friends | Private/locked is normal; fake profiles are often sparse |
| Facebook (groups) | Aktiviti dalam group lokal | Orang Dungun aktif dalam group Dungun = likely real person |
| Web search (full name) | Bodybuilder, askar, ATM, tentera | If claims bodybuilder/askar but zero search hits = fake persona |
| Web search (bank account) | Scam, penipuan, keldai akaun | Rarely in public DB even for real mules |
| Telegram QR decode | t.me link destination | Telegram-only contact = classic scam isolation tactic |
| Photo analysis | Gym pose, uniform, face consistency | Stolen fitness photos are the #1 scammer asset |

## Red Flag Scoring

| Signal | Weight |
|---|---|
| Mismatched job vs claimed persona | HIGH |
| Telegram-only contact (no WhatsApp, no phone) | HIGH |
| QR code link-in-bio card (generated, not real profile) | MEDIUM |
| GX Bank / digital bank (easy mule account) | MEDIUM |
| Bank account NOT in scam databases | LOW (expected even for mules) |
| Real name matches LinkedIn + Facebook + school | LOW (identity likely real, but account may be used by others) |

A real person with a real LinkedIn/Facebook history can still have their identity stolen or be recruited as a mule. "The person exists" ≠ "the account is clean."
