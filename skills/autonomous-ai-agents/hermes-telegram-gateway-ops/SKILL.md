---
name: hermes-telegram-gateway-ops
description: Diagnose and operate the Hermes Telegram gateway in a multi-bot federation — resolve which bot a gateway actually speaks as (identity truth), trace token/config/env injection sources, reconcile allowlists, send outbound replies via Bot API, and restart safely. Use when "the bot answered as the wrong identity", "config says X but runtime does Y", a Telegram user is silently blocked, a gateway has two processes, or a bot DM needs an outbound reply.
---

# Hermes Telegram Gateway Ops

Operating the Hermes messaging gateway (`hermes gateway run`) inside a multi-bot federation (arifOS: Hermes @ASI_arifos_bot :8444, OpenClaw @AGI_ASI_bot :18789/:8787, FORGE @arifOS_bot). The recurring failure class: **config files lie; only live probes are truth.**

## Core mental model — identity truth hierarchy

When someone asks "which bot is this gateway?" the answer comes from the BOTTOM of this stack, not the top:

```
config.yaml (bot_token_env:)          ← decorative, adapter ignores it
adapter.py hardcodes TELEGRAM_BOT_TOKEN ← env name is hardcoded; config key is fiction
/proc/<pid>/environ                   ← what the RUNNING process actually got injected
Telegram getMe / getWebhookInfo       ← GROUND TRUTH: who the bot really is
```

Diagnose top-down, believe bottom-up. `getMe` per token is the only witness that cannot lie.

## Env injection has 3 sources — check ALL of them

| Source | Path | Notes |
|---|---|---|
| Golden vault | `/root/.secrets/kunci-mas.env` | Only edit here (Iron Rule) |
| Runtime flat | `/root/.secrets/kunci-mas.flat.env` | Generated via `make -f /root/.secrets/Makefile vault-generate`; consumed by systemd `EnvironmentFile=` |
| systemd drop-ins | `/etc/systemd/system/<unit>.service.d/*.conf` | **Sneakiest stale-env source** — e.g. `zzz-webhook-override.conf` hardcodes `Environment=TELEGRAM_BOT_TOKEN=...` directly. Survives vault/flat.env cleanup. Check `systemctl cat <unit>` for the full merged view. |

A var absent from vault+flat.env but present in `/proc/<pid>/environ` = a drop-in is injecting it. Find it with:
```bash
grep -rn "Environment" /etc/systemd/system/<unit>.service.d/
# read values without leaking secrets:
sed -E 's/(Environment="?[A-Z_][A-Z0-9_]*)=[^"]*/\1=<redacted>/g' <drop-in-file>
```

## Config homes trap

- Active home: `HERMES_HOME=/usr/local/lib/hermes-agent` (small, may have NO telegram block → env fallback).
- Legacy home: `/root/.hermes/config.yaml` (40KB+, may still say `bot_token_env: ASI_ARIFOS_BOT_TOKEN`).
- Editing the file you can see may edit a file nothing reads. **MCP server scripts can still run from the legacy home** even though the gateway reads HERMES_HOME — the legacy home is half-alive, not dead. Check `ps aux | grep hermes` for which home each process uses.

## Diagnostic sequence (run in this order)

```bash
# 1. Processes & port ownership
ps aux | grep "hermes gateway" | grep -v grep
ss -tlnp | grep -E ":8444|:8787|:18789"

# 2. Unit → MainPID mapping (find the orphan)
systemctl show <unit> -p MainPID -p ActiveState

# 3. Per-PID injected env (identity of each process)
for pid in <PID...>; do tr '\0' '\n' < /proc/$pid/environ | grep -oE "^(TELEGRAM_BOT_TOKEN|ASI_ARIFOS_BOT_TOKEN|AGI_ASI_BOT_TOKEN|FORGE_BOT_TOKEN|HERMES_TELEGRAM_BOT_TOKEN)="; done

# 4. Identity ground truth (NEVER print token values)
for v in TELEGRAM_BOT_TOKEN ASI_ARIFOS_BOT_TOKEN FORGE_BOT_TOKEN; do
  BOT=$(curl -s "https://api.telegram.org/bot${!v}/getMe" | jq -r '.result.username // "INVALID"')
  echo "$v -> @$BOT"
done

# 5. Shared webhook detection (two bots on one URL = looks like one entity)
for v in ...; do curl -s "https://api.telegram.org/bot${!v}/getWebhookInfo" | jq -r '.result.url'; done

# 6. Allowlist in ALL 3 places (prefilter reads TELEGRAM_ALLOWED_USERS even when GATEWAY_ALLOW_ALL_USERS=true)
#    vault / flat.env / drop-in — diff them
```

## Outbound reply to a user (independent of gateway state)

The gateway may be broken or processing the message; sending via Bot API is direct and verifiable:
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -d chat_id=<user_id> -d text="..." | jq -c '{ok, message_id: .result.message_id, chat: .result.chat.username}'
```
`ok:true` + `message_id` = delivered (API response, not self-report). DM chat_id = the user's numeric ID (not username). For a blocked user, first verify they're in the runtime allowlist (drop-in + flat.env), else the reply lands but their next message still gets blocked.

## ⚠️ Restart discipline — the self-protection guard

**Killing/restarting `hermes gateway run` from inside the gateway session is BLOCKED** by the tool guard: SIGTERM propagates to child processes and would kill the very command/turn executing it. The error explicitly says: run `hermes gateway restart` from a **separate shell outside the running gateway**. Do NOT try to bypass the guard (kill -9 variants, etc.) — it exists because the gateway really will kill your own turn. Reconcile duplicates (orphan `hermes gateway run` processes) only from an external terminal or a scheduled job.

## Double-processing detection

Same inbound message spawning TWO sessions (agent.log shows two `agent.turn_context` lines for one msg) = two gateway consumers alive. Find the orphan: the process NOT matching any unit's MainPID and NOT owning the webhook port. Canonical unit owns `:8444`; orphans typically hold only a stale `TELEGRAM_BOT_TOKEN`+`FORGE_BOT_TOKEN` env mix.

## Agent card registry & A2A discovery (AAA) — the other half of identity

After gateway identity is resolved, the remaining drift point is whether the agents are **discoverable**. The warga identity cards live at `/root/AAA/agents/*/agent-card.json` (hermes, openclaw, forge-bot, 777-forge, 333-AGI, 555-ASI, 888-APEX...), but the registry only auto-scans 2 roots. If `/root/AAA/a2a-server/agent-card-registry.js` lacks a scan path, cards exist on disk but `hermes`/`forge-bot` show `false` in the registry.

- **Patch pattern (verified 2026-08-05):** add a tertiary `loadDirectoryRecursive(path.resolve(__dirname, '..', 'agents'))` block after the CIV-33 scan, mirroring the existing guard style. It recurses subdirs and loads any JSON with `agentId`/`id`/`identity.organId`.
- **Two different endpoints — do not confuse them:**
  - `/api/agents` = **lifecycle registry** (NATS-registered organs/CLI agents with instance state) — NOT the cards. Empty result here after a restart is normal until federation bootstrap re-registers.
  - `/.well-known/agents.json` = **card registry** (generated from `agent-card-registry.js`). This is the acceptance-test endpoint for discovery fixes. **JSON shape gotcha: it uses `agents[].id`, NOT `agentId`** — querying `.agents[].agentId` returns nothing and falsely looks like a failed fix. Use `.agents[].id` or `.total`.
- **Cosmetic load errors:** scanning a broad tree (`agents/`) also picks up non-card JSON (`identity.json` in `_brief/`, `_docs/`, `_external/`). Expect "N load errors" warnings — check the first 5; they're org identity files, not cards. Cards still load.
- **Source ↔ runtime parity:** check the unit's `ExecStart` — `aaa-a2a` runs directly from `/root/AAA/a2a-server/server.js`, so a patch there is live on restart. But `/opt/aaa/app/` holds a parity copy: after patching source, `cp` the file to `/opt/aaa/app/...` and `diff -q` to keep the invariant (deploy doctrine: source = runtime).
- **Commit + verify:** `git -C /root/AAA commit`, then re-curl the well-known endpoint and count total before declaring done.

## Pitfalls

- `bot_token_env:` in config.yaml is **decorative** — `adapter.py` hardcodes `required_env=["TELEGRAM_BOT_TOKEN"]`. Env wins, always.
- A generic env name (`TELEGRAM_BOT_TOKEN`) holding another bot's token = gateway silently runs as the wrong identity with zero errors. getMe is the only way to catch it.
- Two bots sharing one webhook URL cross-deliver updates → looks like one entity. Fix by pointing each bot to its own path.
- `Blocked unauthorized user <id>` in gateway.log = runtime allowlist stale (vault may already have the ID; flat.env/drop-in lag behind). Restart after fixing, or use `getUpdates`-free verification.
- After any token sweep, re-verify the drop-in: a hardcoded `Environment=TELEGRAM_BOT_TOKEN` can survive the vault cleanup — but verify its VALUE with getMe before assuming it's the wrong bot (in 2026-08-05 the injected stale-name token was actually the correct ASI bot — the generic name was a smell, not a wrong identity).
- **Token-bearing systemd drop-ins must be `chmod 600`** (Iron Rule: no secret file > mode 600). Found 2026-08-05: `zzz-webhook-override.conf` was 644 = world-readable live bot token. systemd reads drop-ins as root, so 600 is safe. Check modes of every file containing a token after any gateway change: `ls -la /etc/systemd/system/<unit>.service.d/`.
- **Check `ExecStart` before patching source repos** — a unit may run from the source dir directly (`ExecStart=/usr/bin/node /root/AAA/...`) rather than the `/opt/<organ>/app` runtime copy. Patch the path that actually executes, then sync the parity copy (see registry section above).
- **`hermes gateway run` on :8445 = forge-gateway.service (@arifOS_bot), NOT an orphan.** Verified 2026-08-05: PID 402154 (cmdline `hermes gateway run --replace`, env `TELEGRAM_BOT_TOKEN`+`FORGE_BOT_TOKEN`) is the MainPID of `forge-gateway.service` and speaks as @arifOS_bot on port :8445. A morning probe mislabeled it "orphan/hermes-real-bridge" — killing it would have taken down 777-FORGE. **Before killing ANY `hermes gateway run` process: check `systemctl show forge-gateway -p MainPID`, `ss -tlnp | grep <pid>`, and getMe on its injected token.** Two `hermes gateway run` processes on different ports (:8444 ASI vs :8445 FORGE) is the NORMAL topology, not double-processing.

## Support files

- `references/arifos-gateway-drift-2026-08-05.md` — full incident transcript: token zoo, drop-in discovery, PID evidence, the 6-layer drift analysis.
- `references/aaa-agent-discovery-registry.md` — the AAA agent-card discovery fix: registry scan roots, patch pattern, endpoint semantics (`/api/agents` vs `/.well-known/agents.json`), `id`-vs-`agentId` JSON shape, parity-copy sync, commit evidence.
