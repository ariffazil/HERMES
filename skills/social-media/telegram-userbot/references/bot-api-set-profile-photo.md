# Telegram Bot API — setMyProfilePhoto

Upload a profile photo for a bot via the Bot API (Bot API 7.x+).

## Correct Format

The `setMyProfilePhoto` endpoint requires `InputProfilePhotoStatic` as a JSON object with `attach://` for multipart file upload:

```python
import requests, json

with open("logo.jpg", "rb") as photo:
    r = requests.post(
        f"https://api.telegram.org/bot{token}/setMyProfilePhoto",
        data={"photo": json.dumps({"type": "static", "photo": "attach://myfile"})},
        files={"myfile": ("logo.jpg", photo, "image/jpeg")},
        timeout=15
    )
# Returns: {"ok": True, "result": True}
```

## Wrong Approaches (all failed)

1. **Direct file upload without JSON wrapper** — `files={"photo": ...}` → `"photo isn't specified"`
2. **JSON without `attach://`** — `{"type": "static"}` → `"can't find field 'photo'"`
3. **`setUserProfilePhotos`** (plural) — doesn't exist in Bot API
4. **`setMyProfilePhoto` with raw file** — `-F "photo=@file.jpg"` → `"photo isn't specified"`

## Key Insight

The `photo` parameter must be a JSON string `{"type": "static", "photo": "attach://<filekey>"}`, and the multipart file must use the matching `<filekey>` name. This is the same pattern as `sendPhoto` with `attach://` but nested inside a JSON object for `InputProfilePhoto`.

## Removing Profile Photo

```python
r = requests.post(f"https://api.telegram.org/bot{token}/removeMyProfilePhoto")
# Also removes the bot's profile photo entirely
```

## Verification

```python
r = requests.get(f"https://api.telegram.org/bot{token}/getUserProfilePhotos",
                 params={"user_id": bot_id, "limit": 1})
count = r.json().get("result", {}).get("total_count", 0)
# Should be >= 1 after upload
```

## Proven

2026-07-24 — 3 bot profile photos uploaded (Hermes, OpenClaw, Forge) using this exact format.