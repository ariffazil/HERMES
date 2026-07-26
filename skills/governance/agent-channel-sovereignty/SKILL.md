---
name: agent-channel-sovereignty
description: Multi-agent channel sovereignty doctrine — token ownership, channel primary/guest discipline, and identity contracts for AI agents sharing Telegram/surface communication channels without conflict.
category: governance
authority: F13 SOVEREIGN
forged: 2026-07-25
---

# Agent Channel Sovereignty Doctrine

> **Satu token, satu owner. Satu channel, satu primary agent.**
> Jika dua process guna token sama → `VOID`. Jika dua agents claim channel sama → `888_HOLD` sampai clear.

**DITEMPA BUKAN DIBERI**

---

## When to Load This Skill

Load when:
- Setting up a new bot/agent in a Telegram group where other agents already operate
- Diagnosing 409 Conflict, double-reply, or identity confusion between agents
- Auditing bot routing topology (which agent talks where, with what token)
- Adding a new agent to the federation's communication surface
- Designing multi-agent channel policy for a shared group

---

## The Three Pillars

### P1 — Token Sovereignty (F2 TRUTH + F11 AUDITABILITY)

> **Bot token = Ed25519 identity key. Never shared. Never borrowed.**

| Larangan | Kenapa |
|---|---|
| ❌ Pinjam token agent lain | Telegram 409 Conflict — only one process can poll a token |
| ❌ Dua process guna token sama | Telegram kick one randomly — unpredictable failover |
| ❌ Hardcode token in code | vault.env is the ONE home. Agents read from env, never write. |
| ❌ Paste token in chat/skill/memory | Redacted display only. Full key in vault.env, entered by human hand. |

**Enforcement:** `ps aux | grep gateway` must show exactly ONE process per token. The token ENV var resolves to exactly one running daemon. If conflict found, `systemctl stop` the intruder.

**Verification pattern:**
```bash
ps aux | grep -E 'gateway|bot\.py' | grep -v grep
# Confirm: each bot token maps to exactly one process
```

### P2 — Channel Ownership (F1 AMANAH + F4 CLARITY)

Setiap group/chat ada **satu primary agent**. Agent lain dalam group tu adalah **guest** — respond only under constrained conditions.

| Peranan | Hak | Batasan |
|---------|-----|---------|
| **Primary** | Respond to ALL messages in channel | Must handle general queries, route domain-specific work |
| **Guest** | Respond only on explicit signals | SILENT by default. Topic-filtered. Must not double-reply. |

**Guest rules (enforce in system prompt / gateway filter):**

```
Default: SILENT in [Channel].
Speak ONLY when:
1. Message contains governance/FQ/drift/seal/HOLD signals (topic match)
2. User explicitly @mentions the guest agent
3. Agent detects an anomaly needing immediate attention

Else → let Primary handle it. No double-reply.
```

**Technical guard (when available):** Gateway-level `allowFrom` restriction (only the sovereign's user ID can trigger the agent) + optional `topic_filter` regex pattern.

**Config example:**
```json
{
  "allowFrom": ["267378578"],           // Only Arif triggers
  "groupPolicy": "allowlist",
  "groups": {
    "-1003753855708": {}                 // AAA group only
  }
}
```

### P3 — Identity Contract (F9 ANTI-HANTU + F10 ONTOLOGY)

> **Jangan claim jadi agent lain. Setiap bot declare nama betul.**

| Agent | Declare Diri Sebagai | Bot | Token |
|---|---|---|---|
| Hermes Agent | **Hermes / ASI💃** | @ASI_arifos_bot | `8410138119` |
| OpenClaw | **OpenClaw / 🦞AGI** | @AGI_ASI_bot | `8149595687` |
| FORGE/OpenCode | **FORGE / 🔥FORGE** | @arifOS_bot | `8727562763` |

- ❌ Guest agent jangan tulis "Hermes — saya" dalam bio/description/skill
- ❌ Primary agent jangan tulis "aku bot lain" — causes configuration drift
- ✅ Setiap agent punya **bot_username** dan **service name** consistent across: AGENTS.md, README, systemd unit description, bot description, and skill docs
- ✅ Verify identity via live process check (`ps aux`), not self-report

**Identity verification ritual (required before any audit):**
```bash
# 1. Check running processes
ps aux | grep gateway    # Identify each agent process
systemctl status <unit>  # Verify service identity matches claimed role

# 2. Check token uniqueness
# In config, trace each bot_token_env to vault.env
# Verify tokenFile / env var matches exactly one running process

# 3. Verify no 409 Conflict
# If two processes polled same token recently, Telegram silently
# deauths one. Bot stops responding. Check journalctl for "Conflict"
```

---

## AAA Group — The Multi-Agent Case

Dua (or more) agents in one group is the trickiest pattern. Protocol:

```
Message masuk AAA group
    │
    ├── Primary (ASI💃 / Hermes)
    │   │  Responds to EVERYTHING by default
    │   │  Routes domain intent to appropriate organ
    │   │
    └── Guest (🦞AGI / OpenClaw)
        │  Checks: governance/FQ/drift/seal/HOLD signal?
        │  If YES → respond
        │  If NO  → silent (let primary handle)
        │  Explicit @mention → always respond
```

**Three-layer guard for guests in shared channels:**
1. **Platform level:** `allowFrom` restrict to sovereign's user ID only
2. **Gateway level:** `topic_filter` regex on incoming messages (optional, depends on gateway support)
3. **System prompt level:** "SILENT default, speak only on governance signal or explicit @mention"

---

## Conflict Diagnosis

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Bot stops responding silently | 409 Conflict — two processes on same token | `ps aux` find duplicate → `systemctl stop` intruder |
| Two agents reply to same message | Missing channel ownership rule | Declare primary, add guest system prompt silence rule |
| Agent claims wrong identity | Config sync issue — self-description stale | Verify `ps aux` first, update agent's self-description to match |
| Token rotation breaks bot | Token in 2 places, only one rotated | vault.env is SSOT — update there only, restart gateway |

---

## Setup Checklist (new bot)

| # | Check | Hard Rule |
|---|---|---|
| 1 | Token baru? | ✅ Mestilah — jangan guna token sedia ada |
| 2 | Register in vault.env | ✅ SSOT — single env var, never duplicated |
| 3 | Identity declared everywhere? | ✅ Bot description, README, AGENTS.md, systemd all sync |
| 4 | Channel assignment? | ✅ Declare primary vs guest per group |
| 5 | Guest in group with other bot? | ✅ Kena ada silence-default + topic filter |
| 6 | Conflict test? | ✅ `ps aux | grep token` — confirm unique |
| 7 | Process monitoring? | ✅ systemd unit named clearly, not generic |

---

## Pitfalls

- **"Guest" does NOT mean "secondary priority."** It means constrained scope. A guest that responds to everything defeats the purpose.
- **Do NOT trust self-description.** An agent may claim it is X when it is Y. Always verify by: process, token, service unit, bot username — in that order.
- **tokenFile (OpenClaw pattern)** works, but vault.env is preferred for consistency. If using tokenFile, ensure it's mode 600 and referenced in exactly one gateway config.
- **Double-reply is chaos.** If two agents reply to the same message, users get confused and federation loses credibility. The primary-agent contract must be unambiguous.
- **Skill docs get stale.** After any routing change (new bot, new group assignment, token rotation), update THIS skill's references section with the live config.
