# Two-Layer Telegram Auth — Prefilter vs Full Path

When a Telegram bot identity is "active" (polling, getMe returns 200, process is running) but messages from that bot identity never reach the LLM, the failure mode is almost always in the **adapter auth prefilter**, not the network, token, or process tree.

## The Two Layers (adapter.py, ~line 921 vs ~line 763)

```
Message arrives
    ↓
[1] _handle_message / _ensure_forum_commands
    ↓
    calls _is_user_authorized_from_message()        ← PREFILTER
       reads: os.getenv("TELEGRAM_ALLOWED_USERS")
       on empty allowlist → returns True (allow all)
       on non-empty → checks user_id in set
       ❌ DOES NOT honor GATEWAY_ALLOW_ALL_USERS
    ↓
[2] (only if prefilter passes) _is_user_authorized()
       reads: GATEWAY_ALLOWED_USERS, GATEWAY_ALLOW_ALL_USERS
       ✅ Honors GATEWAY_ALLOW_ALL_USERS
```

The prefilter is **layer 1**. Layer 2 is never reached if layer 1 blocks.

## Why Both Layers Exist (defensive design)

The prefilter is an **early reject** to avoid expensive session/auth work for users we already know are unauthorized. The full path is the authoritative authorization (handles `GATEWAY_*` env vars from the gateway core). They are *supposed* to be consistent, but in practice the prefilter was added before the `GATEWAY_*` env vars existed in the gateway and never got updated.

## Real Symptom in Journal

```
Aug 05 05:01:41 hermes-asi-gateway[196054]:
  WARNING hermes_plugins.telegram_platform.adapter:
  [Telegram] Blocked unauthorized user 8149595687 in chat -1003753855708
```

Both numbers are correct:
- `8149595687` is `@AGI_ASI_bot` (OpenClaw AGI bot)
- `-1003753855708` is the AAA group (`@arifOS`)

The chat IS in `allowed_chats`. The user_id is NOT in `TELEGRAM_ALLOWED_USERS`.

## Diagnosis Recipe (Single Pass)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# State of all relevant allowlists
for var in TELEGRAM_ALLOWED_USERS TELEGRAM_GROUP_ALLOWED_USERS \
           TELEGRAM_GROUP_ALLOWED_CHATS GATEWAY_ALLOW_ALL_USERS \
           GATEWAY_ALLOWED_USERS; do
  val=$(eval echo \$$var)
  [ -n "$val" ] && echo "$var=$val"
done

# Recent blocks
journalctl -u hermes-asi-gateway --since '30m ago' --no-pager \
  | grep -i "Blocked unauthorized" | tail -5

# Confirm bot identity in the chat
curl -sf -m 5 \
  "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChatMember?chat_id=-1003753855708&user_id=8149595687" \
  | python3 -c "import sys,json; d=json.load(sys.stdin).get('result',{}).get('user',{}); print(f'@{d.get(\"username\")} ({d.get(\"id\")}) — admin: {json.load(sys.stdin).get(\"result\",{}).get(\"status\")}')"
```

## Three Failure Modes That Look The Same From Outside

| Symptom | Failure mode | Distinct signal |
|---|---|---|
| Bot process running, getMe 200, journal shows `Blocked unauthorized` | **Prefilter blocking** (this pitfall) | user_id != chat_id in the warning |
| Bot getMe 401 | Token invalid/revoked | curl fails on first call |
| Bot polling getUpdates but never responds in chat | **Running direct, NOT via Hermes relay** (OpenClaw) | process is `openclaw-gateway`, not `hermes-asi-gateway` |

## Decision Tree (Which Fix?)

```
User says "blocked unauthorized" / "bot not replying":
├─ Verify bot ownership FIRST (scripts/bot_ownership_lookup.py --user-id <id>)
│  ├─ Bot owned by Hermes (token matches hermes-asi-gateway process env)
│  │  └─ Prefilter blocking — append user_id to TELEGRAM_ALLOWED_USERS
│  ├─ Bot owned by OpenClaw / FORGE (different process)
│  │  ├─ Want Hermes to also handle it? Add to TELEGRAM_ALLOWED_USERS
│  │  └─ Want bot to keep direct routing? Leave as-is (fail-closed is correct)
│  └─ Bot owned by Unknown
│     └─ Do NOT add without Arif confirmation — could widen trust surface
│
User says "allow all" / "buka semua" / "fail-open":
└─ See "Allow-All Pattern" section below — sets TELEGRAM_ALLOWED_USERS="*"

Is the bot a Hermes bot (e.g., @ASI_arifos_bot)?
├─ YES: prefilter blocking — add to TELEGRAM_ALLOWED_USERS
└─ NO: is it @AGI_ASI_bot or @arifOS_bot?
       ├─ OpenClaw AGI: prefilter blocking at Hermes adapter
       │  ├─ Want AGI routed via Hermes? Add bot ID to TELEGRAM_ALLOWED_USERS
       │  └─ Want OpenClaw direct? Leave as-is (both designs work as fail-closed)
       └─ FORGE bot: not in any group, only tool-call — irrelevant
```

## Forward-Fix Candidates (Upstream)

1. **Best**: have prefilter also check `GATEWAY_ALLOW_ALL_USERS` after the
   `TELEGRAM_ALLOWED_USERS` check fails. One-line patch in adapter.py.
2. **Better**: remove prefilter entirely, call `_is_user_authorized()` from both
   `_handle_message` and `_ensure_forum_commands`.
3. **Acceptable**: keep both layers but document `TELEGRAM_ALLOWED_USERS` as
   authoritative for bot identity — clarify in upstream README that
   `GATEWAY_ALLOW_ALL_USERS` only applies to chat-level access, not per-user.

## Lessons Learned (2026-08-05 incident)

- **Don't assume `GATEWAY_ALLOW_ALL_USERS=true` means "all users allowed"**.
  The prefilter has its own allowlist that's stricter than the full auth path.
- **Chat being in `allowed_chats` is necessary but not sufficient**. Bot
  identity also needs to be authorized.
- **Bot appearing "active" is not a connection-state signal**. A bot can
  poll `getUpdates` actively but still never reach LLM if both layers reject.
- **User mental model: "Hermes not connected to Telegram" is usually
  "Hermes not routing messages for THIS bot identity"**. Reframe the question.
- **For the federation's three-bot design**: each bot has independent auth.
  Diagnosing "which bot is this message for" comes BEFORE diagnosing
  "is the auth path passing".

## Allow-All Pattern — `TELEGRAM_ALLOWED_USERS="*"` (NEW 2026-08-05)

When Arif explicitly says "allow all" / "buka semua", the fastest path is to set
both `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_GROUP_ALLOWED_USERS` to literal `"*"`.

**Why this works** (prefilter code at line 921-925):

```python
allowed_ids = {uid.strip() for uid in allowed_csv.split(",") if uid.strip()}
return "*" in allowed_ids or normalized_user_id in allowed_ids
```

The literal `"*"` is checked first via set membership. Any user_id passes
including bot identities, regardless of `GATEWAY_ALLOW_ALL_USERS`. This is a
**fail-open** override of the otherwise strict prefilter.

**Execution protocol (proven 2026-08-05):**

```bash
# 1. Edit SOT directly — never edit service drop-ins
set -a && source /root/.secrets/kunci-mas.env && set +a
sed -i 's|^export TELEGRAM_ALLOWED_USERS=.*|export TELEGRAM_ALLOWED_USERS="*"|' \
  /root/.secrets/kunci-mas.env
sed -i 's|^export TELEGRAM_GROUP_ALLOWED_USERS=.*|export TELEGRAM_GROUP_ALLOWED_USERS="*"|' \
  /root/.secrets/kunci-mas.env

# 2. Regenerate flat env (systemd EnvironmentFile consumer)
make -f /root/.secrets/Makefile vault-generate
# Expect: "✅ Generated: /root/.secrets/kunci-mas.flat.env (262 keys, 0 drift)"

# 3. STOP + START (restart alone may not reload — see pitfall below)
systemctl stop hermes-asi-gateway.service
sleep 2
systemctl start hermes-asi-gateway.service
sleep 8

# 4. Verify env delivered to new process (ground truth)
NEW_PID=$(systemctl show hermes-asi-gateway.service -p MainPID --value)
cat /proc/$NEW_PID/environ 2>/dev/null | tr '\0' '\n' | grep "^TELEGRAM_ALLOWED_USERS="
# Expect: TELEGRAM_ALLOWED_USERS=*
# If old value: daemon-reload missing or wrapper script shadowed it
```

**F2 caveat (reversibility note):** allow-all widens trust surface to any user
or bot identity that can reach the AAA group chat. Arif is comfortable with this
pattern when explicitly requested. Default to tight allowlist (3 user IDs)
unless Arif re-requests. Document the deviation in `memory` so future sessions
see "currently in allow-all mode" as session state.

**Common pitfall — `restart` vs `stop+start` for env propagation:** If the
systemd unit has `EnvironmentFile=/root/.secrets/kunci-mas.flat.env`, a
`restart` is supposed to re-read it. But `hermes-asi-wrapper.sh` may fork a
child that inherits stale env from the parent's process tree. **`stop`+
`start`** (not `restart`) guarantees a fresh PID reading the new flat env.
Proven 2026-08-05: first `systemctl restart` attempt appeared to succeed but
journal still showed old blocked warnings — `stop`+`start` resolved it.

## Verifying Allow-All is Live — Three Probes (NEW 2026-08-05)

After applying allow-all, **don't trust journal silence alone**. The prefilter
might not be reached for some messages (Telegram bot-to-bot mention doesn't
trigger webhook due to loop prevention). Run three independent probes:

**Probe 1: env delivered to running process** (above step 4)

**Probe 2: webhook listener responding on :8444 with secret check:**

```bash
# Should return 403 (wrong secret) — proves path is alive and verifying
curl -s -m 5 -X POST http://127.0.0.1:8444/telegram/webhook \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: hermes_webhook_secret_2026" \
  -d '{"update_id":99999,"message":{"message_id":1,"date":1785907532,"chat":{"id":-1003753855708,"type":"supergroup"},"from":{"id":267378578,"is_bot":false,"first_name":"Arif"},"text":"/help"}}'
# Expected: HTTP 403 with "Wrong secret token" body
# If 404: path wrong (default path may differ across deployments)
# If 502: listener dead — check process tree
```

**Probe 3: prefilter passes for known blocked ID:**

```bash
# Send test message FROM the previously-blocked bot identity
AGI_TOKEN="8149595687:REDACTED"  # getMe it first to confirm token
curl -s -X POST "https://api.telegram.org/bot${AGI_TOKEN}/sendMessage" \
  -d "chat_id=-1003753855708" -d "text=🧪 allow-all verification"
sleep 15
journalctl -u hermes-asi-gateway --since '1m ago' --no-pager \
  | grep -E "Blocked unauthorized.*8149595687" | tail -3
# Expected: NO new "Blocked" warnings since the test message
```

If all three probes pass, allow-all is live end-to-end. If only Probe 1 passes
(env delivered) but Probe 2 fails (502 on :8444), the wrapper script or
process didn't bind the webhook port — check `ss -tlnp` for the actual listener.

**Loop prevention gotcha (don't waste cycles on this):** bot-to-bot mentions
in group chats do NOT trigger webhooks for other bots in the same chat
(Telegram prevents infinite bot reply loops). So sending "@ASI_arifos_bot"
from `@AGI_ASI_bot` will arrive in the chat but **won't** trigger Hermes to
respond. To verify LLM-level processing, the test message must come from a
user account (Arif's personal ID 267378578) or trigger via a slash command
(`/help`, `/status`). This is a Telegram-side limitation, not a gateway bug.

## Provenance

- Date: 2026-08-05 (early session UTC)
- Trigger: User reported "Hermes agent not connected to Telegram, AGI_ASI_bot
  is OpenClaw AGI supposedly"
- Discovered by: perfunctory check → journalctl → adapter code grep
- Fix proposed (deferred to user choice): append `8149595687` to
  `TELEGRAM_ALLOWED_USERS` in `/root/.secrets/kunci-mas.env` + regenerate
  `kunci-mas.flat.env` + `systemctl restart hermes-asi-gateway.service`
- Updated 2026-08-05 (later session): user said "allow la" then "need restart
  allow all" → applied `TELEGRAM_ALLOWED_USERS="*"` + `TELEGRAM_GROUP_ALLOWED_USERS="*"`
  via `sed -i` on KUNCI-MAS SOT + `make vault-generate` + `systemctl stop/start`.
  Verified end-to-end via /proc/<pid>/environ probe, webhook :8444 secret check,
  and 3 bot identities posting to AAA group without prefilter block warnings.