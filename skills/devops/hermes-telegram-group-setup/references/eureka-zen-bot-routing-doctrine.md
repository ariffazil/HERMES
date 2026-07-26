# 🧿 EUREKA Zen — Bot Routing Doctrine

> Three bots, one federation. Zero chaos.
> Ratified 2026-07-26 via Telegram session. F13-graded.

---

## ⚡ The Hard Rule (F13-graded)

> **Satu token, satu owner. Satu group, satu primary agent.**
> Jika dua process guna token sama → **VOID**.
> Jika dua agent claim group sama → **888_HOLD** sampai clear.

---

## 🧬 Tiga Prinsip

### P1 — Token Sovereignty (F2 TRUTH + F11 AUDITABILITY)

Bot token = Ed25519 identity key. Never shared. Never borrowed.

| ❌ What NOT to do | Why |
|-----------------|-----|
| Pinjam token agent lain | 409 Conflict (proven: OpenClaw pinjam token ASI → chaos) |
| Dua process guna token sama | Telegram kick one randomly |
| Hardcode token dalam code | vault.env is the ONE home |

**Enforcement:**
```bash
ps aux | grep gateway
# Must show exactly ONE process per token.
# Conflict → systemctl stop the intruder
```

### P2 — Channel Ownership (F1 AMANAH + F4 CLARITY)

Setiap group/chat ada **satu primary agent**. Agent lain dalam group tu adalah **guest** — respond only on explicit mention or domain.

| Chat | Primary | Guest | Guest Rule |
|------|---------|-------|------------|
| AAA (-1003753855708) | **ASI💃** (Hermes) | 🦞AGI (OpenClaw) | Only on FQ/drift/governance signal |
| SADO (-1003815535761) | **ASI💃** | ❌ None | — |
| Kanak-kanak (-1003768847825) | **ASI💃** | ❌ None | — |
| Dear NABILAH (-1003792478194) | **ASI💃** | ❌ None | — |
| arifOS ch (-1004446358629) | **ASI💃** | ❌ None | Channel (broadcast only) |
| 🅰❗️🅰 (-1003521544074) | **ASI💃** | ❌ None | — |
| Al AMIN (-1003721331017) | **ASI💃** | ❌ None | — |
| BODYBUILDER (-5561731065) | **ASI💃** | ❌ None | — |
| makcikGPT (-1003890512851) | **ASI💃** | ❌ None | — |
| Arif DM (267378578) | **ASI💃** + 🔥FORGE | 🦞AGI | FORGE=notifications only; AGI=governance only |

### P3 — Identity Contract (F9 ANTI-HANTU + F10 ONTOLOGY)

> **Jangan claim jadi agent lain. Setiap bot declare nama betul.**

| Agent | Declare Diri Sebagai | Bot | 
|-------|---------------------|-----|
| Hermes Agent | **Hermes / ASI💃** | @ASI_arifos_bot |
| OpenClaw | **OpenClaw / 🦞AGI** | @AGI_ASI_bot |
| FORGE/OpenCode | **FORGE / 🔥FORGE** | @arifOS_bot |

| ❌ Jangan | ✅ Kena |
|----------|--------|
| OpenClaw tulis "Hermes — saya" dalam bio | Setiap agent guna bot_username + service name sendiri |
| Hermes tulis "aku OpenClaw" | Identity dalam setiap response header mesti jelas |

---

## 🛡️ AAA Group — Dual-Bot Protocol

Dua bot dalam satu group → paling senang chaos. Protocol:

```
Message masuk AAA group
    │
    ├── ASI💃 (Hermes) → DEFAULT handler
    │     Semua message routed here unless flagged
    │
    └── 🦞AGI (OpenClaw) → GUEST, SILENT by default
          Only responds when:
          1. Message matches governance/FQ/drift/seal/HOLD pattern
          2. Arif explicitly @AGI_ASI_bot
          3. Federation anomaly detected
```

**Technical guard:** OpenClaw gateway's `allowFrom: ["267378578"]` restricts to Arif's messages. Additionally, system prompt enforces silence for non-governance content (enforced 2026-07-26 via `/root/.openclaw/agents/main/system.md` edit).

---

## 📋 Operational Checklist — Setup Bot Baru

| # | Check | Hard Rule |
|---|-------|-----------|
| 1 | Token baru? | ✅ Mestilah — jangan guna token sedia ada |
| 2 | Register kat channel_directory.json? | ✅ Wajib — satu source of truth |
| 3 | Group apa dia masuk? | ✅ Declare primary vs guest |
| 4 | Guest dalam group dengan bot lain? | ✅ Kena ada topic_filter — jangan spam |
| 5 | Dah test conflict? | ✅ `ps aux | grep gateway` — satu process per token |
| 6 | Identity declared? | ✅ Bot description, README, AGENTS.md semua sync |

---

## 🧘 Summary — The Zen

> Proses berbeza. Token berbeza. Bot berbeza. Tujuan berbeza.
> Satu federation. Satu Arif. Zero chaos.
