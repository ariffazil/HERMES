# t.me/contact Links & QR Code Pipeline

## Contact Link Format

```
https://t.me/contact/<user_id>:<contact_token>
Example: https://t.me/contact/1784809722:12ivBOOsRdnokBdd
```

### What Each Part Means

| Part | Type | Notes |
|------|------|-------|
| `user_id` | Telegram user ID (int) | The target user's numeric ID |
| `contact_token` | Sharing token (string) | NOT an access_hash — different format entirely |

### Why You Can't Resolve Programmatically

The `contact_token` is a one-time sharing token used by Telegram's "Share Contact" feature. It is:

- **NOT** the MTProto `access_hash` (which is a 64-bit signed integer)
- Base64/base62/base36 decoding produces values way outside the int64 range
- Only usable by the official Telegram client to open the "Add Contact" dialog

### The Workaround

1. **Decode the QR code** (see below)
2. **User opens the link on their phone** — Telegram app opens "Add Contact" dialog
3. **User taps Add** — contact is now in their contact list
4. **Programmatic access now works:**

```python
# After manual add, scan dialogs for the user
dialogs = await client.get_dialogs()
for d in dialogs:
    if d.entity.id == TARGET_USER_ID:
        entity = d.entity  # resolvable now
        break
```

---

## QR Code Decoding

### Dependencies

```bash
apt-get install -y libzbar0
pip install --break-system-packages pyzbar Pillow
```

### Decode Script

```python
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('image.jpg')
results = decode(img)

for r in results:
    print(f'Type: {r.type}')     # 'QRCODE'
    print(f'Data: {r.data.decode("utf-8")}')  # URL / text

# Fallback: convert to grayscale if raw fails
if not results:
    img_gray = img.convert('L')
    results = decode(img_gray)
```

### Common QR Code Targets

| Center Icon | Platform | Typical URL |
|-------------|----------|-------------|
| Paper airplane | **Telegram** | `https://t.me/...` |
| Camera | **Instagram** | `https://www.instagram.com/...` |
| Music note | **TikTok** | `https://www.tiktok.com/...` |
| Green bubble | **WeChat** | WeChat ID |
| Blue chat | **WhatsApp** | `https://wa.me/...` |

---

## Scam Investigation: QR → Telegram Pattern

Common in love/investment scams:

1. Scammer shares a promotional card with:
   - Stolen bodybuilder/military photo
   - QR code linking to Telegram contact
2. Victim scans QR → directed to Telegram (encrypted, harder to trace)
3. Scammer uses fake persona (bodybuilder, soldier, doctor overseas)
4. Money sent to mule account (often digital banks: GX Bank, BigPay, etc.)

### Investigation Steps

1. **Decode QR** → get Telegram contact/user ID
2. **Search name + user ID** in scam databases (SemakMule, CCID)
3. **Cross-reference** against LinkedIn/Facebook for identity mismatch
4. **Reverse image search** the profile photo to find the real person
5. **Check bank account** against known mule account lists
