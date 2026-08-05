# arifOS Gateway Drift — 2026-08-05 incident

Session: "Why Gateway Configuration Was Difficult" + Syed reply task. Three sessions the same morning hit the same class: token sweep → identity confusion → blocked users.

## The 6-layer drift stack (all hit simultaneously)

| # | Trap | Evidence |
|---|---|---|
| 1 | Two config homes | `/root/.hermes/config.yaml:916` legacy `bot_token_env: ASI_ARIFOS_BOT_TOKEN` vs active `HERMES_HOME=/usr/local/lib/hermes-agent/config.yaml` (2KB, NO telegram block). Editing visible file = editing dead file. |
| 2 | Adapter hardcodes env name | `adapter.py:9776` reads `TELEGRAM_BOT_TOKEN`; `:9965` requires it. `bot_token_env:` decorative. |
| 3 | Token zoo | 5 vars for 3 bots: generic `TELEGRAM_BOT_TOKEN` (held OpenClaw's @AGI_ASI_bot token at one point), `ASI_BOT_TOKEN` (duplicate), `HERMES_TELEGRAM_BOT_TOKEN` (broken `${ASI_BOT_TOKEN}` literal, later fixed to real alias), `ASI_ARIFOS_BOT_TOKEN`, `FORGE_BOT_TOKEN`. |
| 4 | Shared webhook | Both @AGI_ASI_bot and @ASI_arifos_bot registered `arifos.arif-fazil.com/telegram/webhook` → cross-delivery, looked like one entity. |
| 5 | Prefilter ≠ allowlist | `GATEWAY_ALLOW_ALL_USERS=true` does NOT bypass prefilter; prefilter reads `TELEGRAM_ALLOWED_USERS`. A bot ID (8149595687) was allowlisted as a user → OpenClaw messages entered Hermes LLM pipeline. |
| 6 | Caddy source↔runtime drift | Source Caddyfile 1 telegram ref, runtime 3. Fixed by copying runtime → source (2263 lines, diff-clean). |

## Root cause discovered: systemd drop-in stale env

- `/etc/systemd/system/hermes-asi-gateway.service.d/zzz-webhook-override.conf` (created 06:26, before the 06:30 restart) hardcodes 9 `Environment=` lines incl. `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_URL/PORT/SECRET`, `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_GROUP_ALLOWED_USERS`, `TELEGRAM_ALLOWED_CHATS`, `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_REACTIONS`.
- Vault + flat.env had already dropped bare `TELEGRAM_BOT_TOKEN`, but the drop-in kept injecting it.
- **Key correction**: getMe on the injected value → `@ASI_arifos_bot (8410138119)` — the CORRECT identity. Generic name = discipline smell, NOT wrong identity. Don't panic-restart on seeing the var name; verify the value first.
- `TELEGRAM_ALLOWED_USERS` drop-in value matched vault exactly: `267378578,1042200555,5316953867,5250473787,8798431893,5444180135` — so the 03:39-03:41 "Blocked unauthorized user 1042200555" events were from a pre-drop-in stale runtime, fixed by the 06:30 restart.

## Process evidence

- `hermes-asi-gateway.service` MainPID = 417929, owns `:8444`, started 06:30, full token env (6 vars incl. stale-name one).
- PID 402154 (started 06:21, cmdline `hermes gateway run --replace`, env `TELEGRAM_BOT_TOKEN`+`FORGE_BOT_TOKEN`) = **`forge-gateway.service` MainPID (@arifOS_bot, :8445)** — NORMAL topology, NOT an orphan. Morning probe mislabeled it "orphan/hermes-real-bridge"; killing it would have taken down 777-FORGE. **Rule: before killing ANY `hermes gateway run` process, check `systemctl show forge-gateway -p MainPID` + `ss -tlnp` + getMe first. Two gateway processes on different ports (:8444 ASI vs :8445 FORGE) = normal, not double-processing.**
- Double-processing proof: one user message at 06:29 spawned TWO sessions (20260805_062322_92754431 + 20260805_062323_4954421c), visible as two `agent.turn_context` lines in agent.log.
- Orphan kill attempt from inside the gateway session → tool guard BLOCKED: "cannot restart or stop the gateway from inside the gateway process... Run `hermes gateway restart` from a separate shell". This guard is CORRECT behavior — SIGTERM propagates to children and kills the executing turn.

## Useful data points

- Syed ("Abang sado") = TG user 1042200555, @rico_ricaldo_33, DMs @ASI_arifos_bot. Blocked 03:39-03:41 (3 attempts), then "Hello ASI, reply to me." / "hello" answered 03:44/03:47 (180/112 chars).
- Outbound reply sent via `sendMessage` with `ASI_ARIFOS_BOT_TOKEN` → chat_id 1042200555, `ok:true`, message_id 103957 — API-verified, bypasses gateway processing entirely.
- getMe on `TELEGRAM_BOT_TOKEN` from a shell sourcing the current vault = `@INVALID` (var no longer defined → empty token). Don't read "INVALID" as "token revoked"; check whether the var exists first.
- Gateway log patterns: `[Telegram] Flushing text batch agent:main:telegram:dm:<uid>` = inbound DM; `Blocked unauthorized user <uid> in chat <uid>` = prefilter reject; `Suppressing normal final send ... final delivery already confirmed` = streamed delivery OK.
