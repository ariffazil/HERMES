---
name: telegram-bot-routing-doctrine
description: arifOS Federation Telegram bot routing — 3 bots, 9 groups, P1-P3 doctrine, AAA guest rule, token sovereignty, channel ownership, identity contract
---

# Telegram Bot Routing Doctrine — arifOS Federation

> Ratified: 2026-07-25 | F1-F13 graded | Source: `/root/docs/TELEGRAM_BOT_ROUTING_DOCTRINE.md`

## The 3 Bots

| Bot | Username | Token Prefix | Service | Role |
|-----|----------|-------------|---------|------|
| **ASI💃** | @ASI_arifos_bot | 8410138119 | `hermes-asi-gateway.service` | Primary agent — all groups |
| **🦞AGI** | @AGI_ASI_bot | 8149595687 | OpenClaw Node.js gateway | Guest — AAA only |
| **🔥FORGE** | @arifOS_bot | 8727562763 | opencode bot.py | DM-only tool interface |

## P1 — Token Sovereignty (F2 TRUTH + F11 AUDITABILITY)

- One token = one process. Never shared, never borrowed.
- `ps aux | grep gateway` must show **exactly one process per token**.
- 409 Conflict = two processes polling same token → systemctl stop intruder.
- All tokens in `/root/.secrets/vault.env` (SSOT). Never hardcoded.

## P2 — Channel Ownership (F1 AMANAH + F4 CLARITY)

| Chat ID | Name | Primary | Guest | Rule |
|---------|------|---------|-------|------|
| -1003753855708 | AAA | ASI💃 | 🦞AGI | AGI = governance-only, silent default |
| -1003815535761 | SADO | ASI💃 | — | No AGI |
| -1003768847825 | Kanak-kanak | ASI💃 | — | — |
| -1003792478194 | Dear NABILAH | ASI💃 | — | — |
| -1003521544074 | 🅰❗️🅰 | ASI💃 | — | — |
| -1003721331017 | Al AMIN | ASI💃 | — | — |
| -1004446358629 | arifOS channel | ASI💃 | — | — |
| -5561731065 | BODYBUILDER | ASI💃 | — | — |
| -1003890512851 | makcikGPT | ASI💃 | — | — |
| 267378578 | Arif DM | ASI💃 + 🔥FORGE | 🦞AGI | FORGE=notifications, AGI=alerts |
| 1042200555 | Syed DM | ASI💃 | — | — |
| 5316953867 | Aminol? DM | ASI💃 | — | — |
| 5250473787 | Aminol friend? DM | ASI💃 | — | — |
| 8798431893 | Amin Al DM | ASI💃 | — | — |

## P3 — Identity Contract (F9 ANTI-HANTU + F10 ONTOLOGY)

- ASI💃 = Hermes Agent. Never claims to be OpenClaw.
- 🦞AGI = OpenClaw. Never writes "Hermes — saya".
- 🔥FORGE = FORGE/OpenCode. Tool interface only.
- Every bot declares correct username in system prompt + responses.

## AAA Guest Rule (system prompt enforced)

OpenClaw system prompt at `/root/.openclaw/agents/main/system.md`:
- **Default: SILENT** in AAA group
- Speak only: governance/FQ/drift/seal/HOLD/federation signals, @AGI_ASI_bot mention, federation anomaly detected
- Let Hermes (ASI💃) handle everything else. No double-reply.

## FORGE → AAA Group = HOLD

FORGE in AAA group is noise (deploy/forge notifications flooding chat) + security risk (tool execution accessible via group). Keep restricted to Arif DM.

## Troubleshooting

```bash
# Check no token conflict
ps aux | grep gateway

# Verify vault token consistency
grep 'TELEGRAM_BOT_TOKEN\|FORGE_BOT_TOKEN\|ASI_ARIFOS_BOT_TOKEN' /root/.secrets/vault.env

# Check Hermes config
grep -A20 '^telegram:' /root/.hermes/config.yaml

# Check OpenClaw config
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); tg=d['channels']['telegram']; print('Groups:', list(tg['groups'].keys()))"

# Verify runtime channels
grep 'HOME_CHANNELS' /root/AAA/agents/hermes-asi/runtime/.env

# Test token against Telegram API
curl -sf "https://api.telegram.org/bot${TOKEN:0:15}.../getMe"

# Check require_mention
grep 'require_mention' /root/.hermes/config.yaml
```

## References

- **`references/telegram-media-pipeline.md`** — how images, voice, video, and documents are downloaded, cached, batched, and routed to the agent when a user sends them via Telegram. Covers native vision vs Path B (model-swap to Qwen-VL) and the legacy IMAGE TRANSCRIPT pipeline. Source-of-truth code paths in the Hermes gateway.

## Associated Skills

- **cognitive-commands** (`/root/.hermes/skills/cognitive-commands/`) — audience voice doctrine (BM per group, cognitive-load-adaptive DM), `/padu` command, operating rules. **Canonical audience voice table** at `cognitive-commands/references/telegram-routing-doctrine.md`.
- **cognitive-commands/references/zen-spine-evolution.md** — why the Telegram slash menu is 21 commands, not 46.
- **cognitive-commands/references/padu-workflow.md** — full execution sequence for the `/padu` zen federation probe.
- **cognitive-commands/references/menu-redundancy-audit.md** — contrast-check methodology for stripping overlapping slash commands.

## Scripts

- **`scripts/federation-health.sh`** — cannonical no_agent watchdog script. Silent on green, alert on red. Copy and modify `ORGANS` list for any multi-service health check.

## Cron Job Routing (ASI💃)

| Job | ID | Schedule | Delivery | Purpose |
|-----|-----|----------|----------|---------|
| `federation-health` | `4fc70930b508` | Every 2h | Arif DM `267378578` | Watchdog. Silent on green. ❌ → DM alert. |
| `daily-digest` | `4735f2106f96` | 07:00 MYT | Arif DM `267378578` | Morning brief: organ, nadi, segel, dunia. |
| `nightly-seal` | `2c9027d99b3b` | 23:00 MYT | Arif DM + arifOS ch | EOD receipt: kerja, segel, pending, tenaga. |
| `morning-brief` | `4b2d9690c7d9` | 07:00 MYT | Arif DM `267378578` | Script-only watchdog (pre-existing). |
| `drift-alert` | `3abb4871b0e1` | Every 4h | AAA home `-1003753855708` | F2 TRUTH drift detection. |
| `evening-digest` | `1937c75c683c` | 18:00 MYT | Arif DM `267378578` | LLM evening summary. |
| `ASI World Sensorium (AM)` | `b6834cb92045` | 07:30 MYT | Arif DM `267378578` | Daily sensorium morning. |
| `ASI World Sensorium (PM)` | `8f9a465be0d5` | 23:00 MYT | Arif DM `267378578` | Daily sensorium evening. |
| `SyedOS Ringkasan Harian` | `c651a7e5b758` | 21:00 MYT | Syed DM `1042200555` | Daily summary in BM. |
| `weekly-deep-brief` | `6b667dfaaf28` | Sun 23:00 MYT | Arif DM `267378578` | Weekly synthesis. |
| `daily-news-briefing` | `38edd9ba33e6` | 08:00 MYT | Arif DM `267378578` | World news. |

## Routing Rules

1. **Arif DM** (`267378578`) — sovereign channel. Federation health, daily briefs, nightly seals, sensoriums. All autonomous deliveries.
2. **AAA Home** (`-1003753855708`) — federation ops channel. Drift alerts, model watchdog, system broadcasts.
3. **SADO** (`-1003815535761`) — trading + social only. No federation deliveries.
4. **arifOS channel** (`-1004446358629`) — governance audit trail. Nightly-seal only.
5. **Syed DM** (`1042200555`) — personal assistance. SyedOS ringkasan only.

## Telegram Webhook Troubleshooting

If the bot stops receiving messages (pending_updates accumulates, last_error shows `401 Unauthorized`):

### Check Webhook Status
```bash
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | \
  python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'url: {d[\"url\"]}'); print(f'pending: {d[\"pending_update_count\"]}'); print(f'last_error: {d.get(\"last_error_message\",\"none\")}')"
```

### Root Cause: Missing Secret Token

The OpenClaw gateway config (`/root/.openclaw/openclaw.json`) defines:
```json
"webhookSecret": "${TELEGRAM_WEBHOOK_SECRET}"
```

If the Telegram webhook was registered WITHOUT `secret_token`, Telegram sends webhook POSTs without the `X-Telegram-Bot-Api-Secret-Token` header. The gateway returns `401 Unauthorized`.

### Fix: Re-register with Secret Token
```bash
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/telegram-webhook&secret_token=${TELEGRAM_WEBHOOK_SECRET}"
```

### Token-to-Webhook Map
| Bot | Token Var | Webhook URL |
|-----|-----------|-------------|
| ASI💃 (Hermes) | `ASI_ARIFOS_BOT_TOKEN` | Via Hermes gateway |
| 🦞AGI (OpenClaw) | `TELEGRAM_BOT_TOKEN` | `https://openclaw.arif-fazil.com/telegram-webhook` |
| 🔥FORGE | `FORGE_BOT_TOKEN` | DM-only proxy |

### Full Reset
```bash
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook"
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=https://openclaw.arif-fazil.com/telegram-webhook&secret_token=${TELEGRAM_WEBHOOK_SECRET}"
```

## Known Gaps / Caveats

- OpenClaw's system prompt uses AAA guest rule via text instruction — no code-level topic_filter. ~95% coverage.
- `-1004446358629` (arifOS channel) — now active for nightly-seal deliveries (2026-07-26). ASI bot covers default Hermes responses too.
- FORGE bot needs Telethon setup to be usable in groups (currently DM-only tool interface).
