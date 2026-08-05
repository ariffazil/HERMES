# Device ecosystem research (verified 2026-08-05)

## Honor Watch X5i — fully closed silo
- BLE-only: no WiFi, no GPS, no NFC, no app store, proprietary OS. 1.97" AMOLED, 420mAh, 21-day battery, BT calling (mic+speaker).
- **HONOR Health app** (`com.hihonor.health`) — Play Store listing checked: **zero mentions of Health Connect or Google Fit**. Permissions only cover local exercise-file import/export (Storage), call reminders, SMS.
- No built-in data export of health metrics. No cloud/web dashboard for watch data (Honor ID cloud = phone files only).
- No public server-side API. **HONOR Health Kit SDK** exists on developer.honor.com (CN portal docs /en/docs/11005/reference/HealthKit, Maven integration) but it is an **Android SDK for app developers** — requires HONOR developer account + building/maintaining your own app. Overkill for a personal 1-watch setup.
- **Gadgetbridge: NOT supported** (as of Aug 2026, announced Apr 2026). Supported Honor devices: Band 3–10, Magic Watch 1/2, Watch 4/4 Pro, GS 3, GS Pro.
- X5i has no on-watch assistant; agent voice channel = BT call through the paired phone (Twilio/SIP → phone → watch rings).

## Xiaomi Smart Band — much more open
- **Mi Fitness app syncs natively to Health Connect** → the "source → Health Connect" leg needs no third-party app. Health Sync only for the Drive CSV export.
- Gadgetbridge supports Xiaomi Smart Band 7/8/9 family well (steps, HR, sleep, SpO2, alarms, watchfaces) — verify exact model at `gadgetbridge.org/gadgets/wearables/xiaomi/`.
- USB BLE dongle (~RM20-30) on the server + bleak = live HR / battery / notifications, fully local.

## Health Sync bridge app
- `nl.appyhapps.healthsync` (Play Store, established, 500k+ downloads). Bridges: vendor health apps ↔ Health Connect / Google Fit / Strava; plus **Health Connect → Google Drive CSV auto-export** (folder "HealthExport", daily).
- Google Fit REST API is **deprecated, shutdown end of 2026** — never build new integrations on it. Drive CSV has no expiry and rclone handles OAuth with a plain Google account.

## Data-flow recap (the architecture that works)
```
watch → vendor app (Mi Fitness natively; HONOR Health needs Health Sync)
      → Health Connect → Health Sync Drive export → Google Drive CSV
      → rclone sync → parser → health_snapshot.json → Hermes cron (20:00 MYT, silent watchdog)
```
