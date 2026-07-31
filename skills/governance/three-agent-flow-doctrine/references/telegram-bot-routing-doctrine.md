# Telegram Bot Routing Doctrine — Forged 2026-07-25

> **Three bots, one federation. Zero chaos.**
> F13-graded doctrine — one token, one owner. One group, one primary agent.
> Jika dua process guna token sama → VOID. Jika dua agent claim group sama → 888_HOLD.

## The Three Principles

### P1 — Token Sovereignty (F2 TRUTH + F11 AUDITABILITY)

Bot token = Ed25519 identity key. Never shared. Never borrowed.

**Hard Rules:**
- ❌ Pinjam token agent lain (409 Conflict — proven with OpenClaw using ASI token)
- ❌ Dua process guna token sama (Telegram kicks one randomly)
- ❌ Hardcode token in code (vault.env is the ONE home)
- ✅ `ps aux | grep gateway` must show exactly ONE process per token
- ✅ All tokens sourced from vault.env or secrets files (mode 600)

**Enforcement:** If conflict found → `systemctl stop` the intruder process.

### P2 — Channel Ownership (F1 AMANAH + F4 CLARITY)

Setiap group/chat has one primary agent. Agent lain dalam group = guest — respond only on explicit mention or domain.

| Group | Primary Agent | Guest Agent(s) | Guest Rule |
|-------|--------------|----------------|------------|
| AAA (-1003753855708) | ASI💃 (Hermes) | 🦞AGI (OpenClaw) | Gov/FQ/drift/seal/HOLD only |
| SADO (-1003815535761) | ASI💃 | ❌ None | OpenClaw not in SADO |
| Kanak-kanak | ASI💃 | ❌ None | — |
| Dear NABILAH | ASI💃 | ❌ None | — |
| arifOS channel (-1004446358629) | ASI💃 | ❌ None | — |
| BODYBUILDER | ASI💃 | ❌ None | — |
| makcikGPT | ASI💃 | ❌ None | — |
| Arif DM (267378578) | ASI💃 + 🔥FORGE | 🦞AGI | FORGE=tool notifications. AGI=governance alerts |

**AAA Guest Rule (critical):**
- Default: **SILENT** in AAA
- Speak ONLY when:
  1. Message contains governance/FQ/drift/seal/HOLD/federation/genesis/organs signal
  2. Arif explicitly @mentions the bot
  3. Federation anomaly detected that needs immediate attention
- Else → let Hermes (ASI💃) handle it. **No double-reply.**
- Enforced via system prompt, not code (Option A — 2 min fix, ~95% coverage)

### P3 — Identity Contract (F9 ANTIHANTU + F10 ONTOLOGY)

Jangan claim jadi agent lain. Setiap bot declare nama betul.

| Bot | Declare As | Bot Username |
|-----|-----------|-------------|
| Hermes Agent | Hermes / ASI💃 | @ASI_arifos_bot |
| OpenClaw | OpenClaw / 🦞AGI | @AGI_ASI_bot |
| FORGE/OpenCode | FORGE / 🔥FORGE | @arifOS_bot |

**Hard Rules:**
- ❌ OpenClaw jangan tulis "Hermes" or "arifOS_bot" in description/bio
- ❌ Hermes jangan tulis "aku OpenClaw"
- ✅ Every bot has unique `bot_username` and `service name` in every response header

## Teleport Group Naming Convention

Arif's convention: single sigil + single lexical unit.
- Examples: `🔥 FORGE`, `🌊 BASIN`, `🧠 DREAM`, `💎 SEAL`, `⚖️ MARUAH`, `🌀 SABAR`
- Never multi-word. Never sentence.
- Always **one emoji + one word**.

## Operational Checklist (Setup New Bot)

1. □ New token? — Must be fresh, never reuse existing token
2. □ Register in `channel_directory.json`? — Single source of truth
3. □ Declare group membership? — Primary vs guest
4. □ Topic filter for guest bots? — Must not spam
5. □ Conflict test? — `ps aux | grep gateway` shows exactly one process per token
6. □ Identity declared? — Bot description, README, AGENTS.md all synced

## Conflict Detection

```bash
# Quick conflict scan
ps aux | grep -E "gateway|bot" | grep -v grep | grep -c python3
# Should show 1 per token

# Detailed
ps aux | grep -E "gateway|bot" | grep -v grep \
  | awk '{print $2, $11, $12, $13, $14, $15}'
```

If a bot token appears in two processes, Telegram will randomly kick one.
Fix: `systemctl stop` the duplicate, verify webhook, restart clean.

## AAA Group — Double-Bot Protocol

Two bots in one group → requires explicit protocol:

```
Message masuk AAA group
    │
    ├─ ASI💃 (Hermes) — Default handler
    │   Responds to EVERYTHING else
    │
    └─ 🦞AGI (OpenClaw) — Guest
        Checks: gov/FQ/drift/seal/HOLD keywords
        If yes → respond. If no → silent.
        Never double-reply the same topic.
```

**Technical guard:** Gateway kena ada topic_filter — process only messages matching `FQ|drift|governance|floor|888|seal|HOLD|federation|genesis|organs`. Yang lain ignore terus.

## Process Map (Live 2026-07-25)

```
PID 2930910  openclaw gateway        🦞AGI   @AGI_ASI_bot    8787+18789
PID 2932535  hermes gateway (ASI)    ASI💃   @ASI_arifos_bot
PID 2982511  hermes gateway (dup)    ASI💃   —                ⚠️ Fixed
PID 2998156  opencode-bot            🔥FORGE @arifOS_bot
PID 2998235  opencode-bot (dup)      🔥FORGE @arifOS_bot     ⚠️ Fixed
```

## Known Issues

| Issue | Status | Fix |
|-------|--------|-----|
| Hermes gateway double start | Fixed | `--replace` flag prevents races |
| Token collision @arifOS_bot | P2 carry-forward | opencode-bot + forge-gateway share same bot |
| OpenClaw 429 rate limit | Fixed | Gateway restart cleared backlog |
| Webhook unset regression | Fixed | Re-register on detection |
| Heartbeat delivery wrong | Fixed | Should be delivery=none, not to DM |

## AGI_NUMERICAL_FABRICATION Scar

> **Discovered 2026-07-25:** OpenClaw fabricated numbers (2056h stale, 9 restarts, wrong boot time) from narrative state instead of live source.

**Constraint:** For any numeric claim (time, count, hours, %, ID), MUST cite live source within same turn or label UNKNOWN. If no live source available, use `UNKNOWN` explicitly — do not fabricate plausible numbers.

**Severity:** HIGH — F2 TRUTH violation. Applies to ALL federation agents (Hermes, OpenClaw, OpenCode).

**Scar registered:** `AGI_NUMERICAL_FABRICATION` — federation-wide pattern.

## References

- HEARTBEAT.md — Silent-on-green protocol (HEARTBEAT_OK pattern, delivery=none)
- `three-agent-flow-doctrine` — Tri-Agent Protocol (FQ, governed execution, zen directives)
- `/root/docs/TELEGRAM_BOT_ROUTING_DOCTRINE.md` — Canonical saved doctrine
