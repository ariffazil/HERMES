# Runaway Agent Recovery — 2026-07-31 → 2026-08-01 Incident

## Timeline — Wave 1 (2026-07-31 evening)

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
- 23:30 UTC: Hermes escalates to masking
  - `systemctl mask openclaw-gateway.service` → **FAILED**: "File '/etc/systemd/system/openclaw-gateway.service' already exists" (unit is hand-written at /etc/systemd/system/, not a symlinked unit — mask only works on symlinks)
  - Workaround: `ln -sf /dev/null /etc/systemd/system/openclaw-gateway.service` + same for opencode-bot + `daemon-reload`
  - Verified: `systemctl start` → "Unit is masked."

## Timeline — Wave 2 (2026-08-01, after masking)

- 23:31–23:35 UTC: Gateway **still respawned despite masking** — a supervisor (opencode-bot bridge / openclaw-gateway watchdog) kept starting agents:
  - New agent PID 1378204 at 107% CPU
  - New agent PID 1374489 respawned
- 23:35 UTC: Hermes killed tmux session `work` (window `kimi`) — **this was the final kill layer**
  - `tmux list-windows -t work` → `0: kimi*`
  - `tmux kill-session -t work`
  - After this: 0 openclaw procs, 0 opencode agents, only `opencode serve` (PID 1201614) remained
- Residual: a few queued "final receipt" messages drained post-kill (expected backlog, not a failed kill)
- Later: OpenClaw gateway came back ONLINE again ("Back online · clean resume") — re-mask + kill agents + kill tmux again; verify `systemctl is-active` after EVERY kill round

## Root Cause

Agent received a screenshot of a **Cloudflare-cached stale page**. The image transcript described UI elements (11-category organ nav with Greek letters, "Masuk sini" persona-gating cards, 8xl italic logo wall) that had been removed from source code over an hour earlier. The live bundle (`index-LDtlISZm.js`) had none of these elements — verified by `curl + grep` multiple times. But the agent could not distinguish the screenshot from live state.

## Services Involved

| Service | Role | Restart Behavior |
|---|---|---|
| `opencode-bot.service` | Telegram bridge (777-FORGE, HANDS layer) | Restart=always |
| `openclaw-gateway.service` | Multi-agent message router | Restart=always |
| `opencode.service` | OpenCode server (localhost:4096) | Single instance, NOT auto-restart |

## Full Recovery Command Sequence (the order that worked)

```bash
# 1. Kill runaway agents
kill 1354256 1355740

# 2. Stop services (temporary — they auto-restarted)
systemctl stop opencode-bot.service openclaw-gateway.service

# 3. Mask — DO NOT use `systemctl mask` (fails: "File already exists" for hand-written units)
#    Go straight to symlink-to-/dev/null:
ln -sf /dev/null /etc/systemd/system/openclaw-gateway.service
ln -sf /dev/null /etc/systemd/system/opencode-bot.service
systemctl daemon-reload

# 4. Kill orphan agents spawned during restart windows
kill 1374489 1378204

# 5. FINAL LAYER — kill the tmux/screen session hosting the agent
tmux ls                       # "work" session with window "kimi"
tmux kill-session -t work
screen -ls                    # same check for screen

# 6. Verify — after EVERY round
systemctl is-active opencode-bot.service openclaw-gateway.service  # inactive inactive
ps aux | grep opencode | grep -v grep | grep -v serve              # empty
tmux ls                                                             # no sessions
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
2. **`systemctl mask` fails on hand-written units** (`File already exists`). Use `ln -sf /dev/null <unit-path>` directly — it force-overwrites and achieves the same permanent block.
3. **Masking services ≠ stopping tmux-hosted agents.** The agent that kept posting after both PIDs and services were dead was inside `tmux` session `work`/window `kimi`. tmux kill was the final layer that ended the loop. Check `tmux ls` in the SAME pass as `systemctl list-units`, not after.
4. **Verify masking worked** by attempting `systemctl start` — it should fail.
5. **A masked service can still come back** (supervisor, manual start, gateway re-registration). Re-check `is-active` after every kill round; a 3-second respawn means a supervisor is involved — hunt it down.
6. **Always save the restore commands** so the user doesn't need to reconstruct them.
7. **One evidence-backed correction, then stop engaging.** If agent ignores 2+ corrections with exact bundle hash + timestamp + probe results, find the PID and kill.
8. **Screenshots are NOT live state.** When an agent diagnoses from a screenshot that contradicts `curl` probes, it's already stuck.
9. **Queued messages outlive the process.** Identical "final receipt" messages after the kill are backlog drain, not a failed kill — verify by process table, not message silence.
