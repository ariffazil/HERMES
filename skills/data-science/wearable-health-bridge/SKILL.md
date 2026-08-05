---
name: wearable-health-bridge
description: "Connect a closed-ecosystem fitness watch (Bluetooth-only, no app store — e.g. Honor/Huawei/Xiaomi budget watches) to Hermes/agent health data. Architecture: phone HONOR Health app → Health Connect → Health Sync bridge app → Google Drive CSV → rclone → parser → silent watchdog cron. Trigger: user wants fitness watch data (steps/HR/sleep/SpO2) flowing to the agent."
---

# Wearable → Agent Health Bridge

## When to use
User has a budget fitness watch (Honor Watch X5i etc.) and wants its data (steps, heart rate, sleep, SpO2) in Hermes — for daily briefings, WELL-organ feeds, or health alerts.

## Hard constraints that shape the design (verified 2026-08)
- **Closed watches can't run agents or sync directly**: X5i = BLE-only, no WiFi/GPS/app store, proprietary OS. The **phone running the vendor Health app is the mandatory hub**. No BLE adapter on a cloud server → direct GATT is off the table (or needs a USB dongle).
- **Google Fit REST API is deprecated — shutdown by end of 2026**. Do NOT build on it. Use Google Drive CSV export instead (no expiry, no custom OAuth project — rclone handles auth with a normal Google account).
- Vendor health apps (HONOR Health) do NOT sync natively to Google Fit — users confirm a third-party bridge app is required.

## Device ecosystem matters — check the watch BEFORE designing
- **Xiaomi Smart Band (Mi Fitness app)**: syncs **natively to Health Connect** — the source bridge is free. Health Sync is only needed for the final Google Drive CSV export leg. **Gadgetbridge supports Xiaomi bands well** (7/8/9) → a USB BLE dongle on the server is a viable fully-local path (no cloud, no Google).
- **Honor/Huawei closed watches (X5i)**: no export, no Health Connect, no cloud API, Gadgetbridge missing recent models → the full Health Sync bridge is mandatory.
- Always check `gadgetbridge.org/gadgets/wearables/<vendor>/` before promising a BLE-direct path — support lags new models by months.
- Verified device-ecosystem research (Play Store evidence, Gadgetbridge lists, HONOR Health Kit status): `references/devices.md`.

## Working architecture (built + tested)
```
Watch → HONOR Health app (Android phone) → Health Connect → Health Sync app
      → Google Drive CSV auto-export (folder "HealthExport") → rclone sync
      → parser → health_snapshot.json → Hermes cron (silent watchdog)
```

**Existing implementation** (built 2026-08-05, Honor Watch X5i):
- `/root/HERMES/scripts/health-bridge/sync_health.py` — `--pull` (rclone sync), `--brief`/`--once` (parse + summarize; silent unless new data)
- `/root/HERMES/scripts/health-bridge/brief.sh` — cron wrapper
- `/root/HERMES/scripts/health-bridge/README.md` — full phone-side setup steps
- Cron: `health-bridge-daily-brief` (job id 4acdf62b53af), daily 20:00 MYT, no_agent, silent when no data

## Parser design notes (sync_health.py)
- Tolerant CSV: auto-detect date column (date/time/timestamp/start) + value column (value/count/bpm/avg/duration/total); filename pattern routes to metric kind (`steps`, `heart_rate`, `sleep`, `spo2`, `stress`).
- Sleep unit auto-detect: total <24 → hours; <1440 → minutes/60; else seconds/3600.
- Processed files → archive/; snapshot JSON append-only per day.

## Setup steps for a new user/watch
1. Pair watch to phone via vendor app (e.g. HONOR Health).
2. Install **Health Sync** (`nl.appyhapps.healthsync`) → source vendor app → target Health Connect → auto-sync.
3. Health Sync → Health Connect → **Google Drive Sync** → CSV export, auto daily.
4. Server: `rclone config` (remote name `healthdrive`, type drive) — needs user's Google OAuth in browser, one time.
5. Test: `python3 sync_health.py --pull && python3 sync_health.py --once`.

## Hermes cron specifics (bite later otherwise)
- Cron script path **must be relative to `~/.hermes/scripts/`** — absolute paths rejected. On this box `~/.hermes` is a symlink to `/root/HERMES`.
- `no_agent=True` + script that prints nothing when there's no new data = perfect silent watchdog (empty stdout → no message sent).
- Hermes cron schedules resolve in **MYT (+08:00)** — `next_run_at` shows +08:00. "0 20 * * *" = 8pm MYT (good for end-of-day data).

## Pitfalls
- Watch must stay in BLE range of the paired phone; vendor app must keep running in background or sync stalls (brief goes silent).
- rclone `--pull` fails silently-ish (stderr only) until OAuth is configured — expected during setup, not a bug.
- Don't promise real-time data over this path — it's daily-batch by design. Live HR needs a BLE dongle + bleak on the server (Gadgetbridge does NOT support recent Honor models yet — X5i missing as of Aug 2026).
- Notification direction (agent → watch) works out of the box once paired: enable notification mirroring in vendor app; Hermes/Telegram messages buzz the wrist. Zero server work.
