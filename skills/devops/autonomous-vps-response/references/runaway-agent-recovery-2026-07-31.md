# Runaway Agent Recovery — 2026-07-31 Incident

## Timeline

- 21:33 UTC: OpenClaw gateway + OpenCode bot started via systemd
- 22:15 UTC: Bot bridge (opencode-bot) spawned agent PID 1239442
- 22:54 UTC: Arif sent screenshot of arif-fazil.com homepage (stale cached)
- 22:54–23:30 UTC: OpenClaw agent enters cognitive loop
  - 60+ duplicate "Receipt sealed" / "Berhenti" posts in AAA group
  - Agent fixates on "11 kategori chaos" nav that doesn't exist in live code
  - Agent claims "F2 build stale" despite 3 successful rebuilds deployed
  - Agent proposes "Zen plan" for work already completed and live-probed
- 23:13–23:30 UTC: Two OpenCode agent processes burn 180% CPU combined
  - PID 1354256: 103% CPU
  - PID 1355740: 78% CPU
- 23:26 UTC: Hermes kills runaway agents (signal first, then -9)
  - Attempts `systemctl stop` on both services
- 23:27 UTC: OpenClaw gateway auto-restarts (Restart=always in unit file)
  - New agent PID 1374489 spawns at 107% CPU
- 23:30 UTC: Hermes escalates to `systemctl mask`
  - `ln -sf /dev/null /etc/systemd/system/openclaw-gateway.service`
  - `ln -sf /dev/null /etc/systemd/system/opencode-bot.service`
  - `systemctl daemon-reload`
  - Verified: "Failed to start ... Unit is masked."

## Root Cause

Agent received a screenshot of a **Cloudflare-cached stale page**. The image transcript described UI elements (11-category organ nav with Greek letters, "Masuk sini" persona-gating cards, 8xl italic logo wall) that had been removed from source code over an hour earlier. The live bundle (`index-LDtlISZm.js`) had none of these elements — verified by `curl + grep` multiple times. But the agent could not distinguish the screenshot from live state.

## Services Involved

| Service | Role | Restart Behavior |
|---|---|---|
| `opencode-bot.service` | Telegram bridge (777-FORGE, HANDS layer) | Restart=always |
| `openclaw-gateway.service` | Multi-agent message router | Restart=always |
| `opencode.service` | OpenCode server (localhost:4096) | Single instance, NOT auto-restart |

## Recovery Commands Used

```bash
# Kill runaway agents
kill 1354256 1355740

# Stop services (temporary — they auto-restarted)
systemctl stop opencode-bot.service openclaw-gateway.service

# Mask to prevent auto-restart
ln -sf /dev/null /etc/systemd/system/openclaw-gateway.service
ln -sf /dev/null /etc/systemd/system/opencode-bot.service
systemctl daemon-reload

# Kill orphan agent spawned during restart window
kill 1374489
```

## Restore Commands

```bash
systemctl unmask opencode-bot.service openclaw-gateway.service
systemctl daemon-reload
systemctl start opencode-bot.service openclaw-gateway.service
```

## Verification After Recovery

```bash
# Confirm no agent processes
ps aux | grep opencode | grep -v grep | grep -v serve
# Should be empty

# Confirm services masked
systemctl is-enabled opencode-bot.service  # "masked"
systemctl is-enabled openclaw-gateway.service  # "masked"

# Attempted start should fail
systemctl start openclaw-gateway.service 2>&1
# "Failed to start openclaw-gateway.service: Unit is masked."
```

## Key Lessons

1. **Stop alone isn't enough for Restart=always services.** Mask is required.
2. **Verify masking worked** by attempting `systemctl start` — it should fail.
3. **Always save the restore commands** so the user doesn't need to reconstruct them.
4. **One evidence-backed correction, then stop engaging.** If agent ignores 2+ corrections with exact bundle hash + timestamp + probe results, find the PID and kill.
5. **Screenshots are NOT live state.** When an agent diagnoses from a screenshot that contradicts `curl` probes, it's already stuck.
