---
name: cross-user-intelligence
description: Cross-user social intelligence pipeline — extract patterns, themes, and signals from multi-user Telegram conversations. Digest-only, attributed, auditable. Sovereign-facing intelligence, not surveillance.
layer: knowledge
invariants:
  authority: F13 sovereign only. Digest is for Arif, not shared with any other user.
  evidence_schema: OBS (user interaction) → DER (pattern extraction) → INT (thematic synthesis) → SPEC (forward signal)
  reversibility: true — digests are computed, not trained. Can be deleted. VAULT999 trail is append-only but digests are not.
  lineage: Every digest entry links to consent attestation + user_id (attributed) + session_id
  trigger_semantics: Time-based (cron digest) + event-based (threshold pattern detected) + on-demand (/padu social)
  failure_contract: Any pattern without minimum 2 supporting data points → discarded. Single-event patterns are noise.
  resource_budget: {cpu: low, time_ms: < 60000 per digest run, entropy: 0}
  audit_surface: [disclosure_shown, digest_generated, digest_delivered, excluded_category_encountered]
bridge_connections:
  kernel_verbs: [arif_seal, arif_think, arif_observe]
  skills: [cognitive-commands, irreversible-consent-protocol, telegram-bot-routing-doctrine, skill-substrate-framework]
  knowledge: [F2 TRUTH, F6 EMPATHY, F9 ANTI-HANTU, F11 AUDITABILITY]
  protocol: event_capture → pattern_extraction → digest_delivery
  inputs: {user_id: string, chat_id: string, topic: string, session_summary: string}
  outputs: {digest: object, receipt_id: string, excluded_count: integer}
contrast:
  not: [surveillance-system, analytics-dashboard, training-corpus]
  distinction: Labs extract patterns to train models (aggregate, opaque, irreversible). Enterprise analytics measures metrics (aggregate, de-identified). Cross-user intelligence extracts attributed patterns FOR the sovereign — identified, auditable, reversible, with explicit disclosure.
  trigger_conflicts: NEVER fire on health/medical conversations. NEVER include verbatim quotes cross-context. NEVER surface to non-sovereign users.
---
# Cross-User Intelligence Pipeline

> **Core:** F2 TRUTH — evidence-based patterns. F6 EMPATHY — excluded categories. F9 ANTI-HANTU — disclosure.

## 1. Disclosure Text

### In Hermes persona / system prompt (cognitive-commands audience map):

> *"Hermes is Arif's agent. Conversations may inform insights shared with him — patterns and themes, not raw chat. Personal health, finance, and conflicts are excluded. You can ask what Arif has been told about our chat."*

| Requirement | Met? |
|---|---|
| Who owns the agent | ✅ "Arif's agent" — F9 non-deceptive |
| What is extracted | ✅ "patterns and themes, not raw chat" — digest-only |
| What is excluded | ✅ specific categories named |
| Right to know | ✅ "You can ask what Arif has been told" — transparency |
| Brevity | ✅ satu baris, no legalise |

### Where it lives:
- `/root/AAA/CLAUDE.md` — agent doctrine preamble
- Cognitive-commands skill audience map — as a standing instruction
- Onboarded once per new user at first interaction

## 2. Architecture

```
Telegram Users (Syed, Aminol, etc.)
    │
    ▼
┌────────────────────────────────┐
│  Hermes Session                │
│  (per-user, isolated)          │
│  ├─ Normal response to user    │
│  └─ Pattern signal → queue     │
└──────────┬─────────────────────┘
           │ attributed: user_id, topic, session_id
           ▼
┌────────────────────────────────┐
│  Intelligence Queue            │
│  (forge_work/intel/inbox/)     │
│  JSONL: time-bucketed entries  │
└──────────┬─────────────────────┘
           │ cron: every 4h / on-demand
           ▼
┌────────────────────────────────┐
│  Digest Engine                 │
│  Filters:                     │
│  ├─ Excluded categories ✂️    │
│  ├─ Minimum 2 data points 🔢  │
│  ├─ Cross-user correlation 🔗 │
│  └─ Epistemic labels 🏷️       │
└──────────┬─────────────────────┘
           │ attributed but never verbatim
           ▼
┌────────────────────────────────┐
│  Digest → Arif DM              │
│  ├─ Regular cron (daily)       │
│  ├─ Signal (threshold hit)     │
│  └─ On-demand (/padu social)   │
└────────────────────────────────┘
```

## 3. Digest Schema

Every digest entry follows this structure:

```json
{
  "ts": "2026-07-29T14:00:00Z",
  "type": "intelligence_digest",
  "period": "2026-07-29T10:00:00Z/2026-07-29T14:00:00Z",
  "user_count": 3,
  "signals": [
    {
      "pattern": "trading_interest_increase",
      "confidence": 0.78,
      "epistemic": "DER",
      "supporting_users": ["Syed", "Aminol"],
      "evidence_count": 4,
      "summary": "Increased discussion of XAUUSD technical levels across 2 users — support/resistance zones for next week's FOMC. No specific positions disclosed.",
      "quotes": false,
      "first_seen": "2026-07-28",
      "trend": "rising"
    }
  ],
  "excluded_count": 0,
  "excluded_categories": [],
  "receipt_id": "INTEL-20260729-1400-a1b2c3d4"
}
```

### Signal types the engine can detect:

| Signal | Trigger | Example |
|---|---|---|
| `shared_interest` | ≥2 users discuss same topic in <24h | XAUUSD, nasi lemak vendor, specific app |
| `sentiment_shift` | User mood changes vs baseline | "penat" → frequent, "best" → frequent |
| `knowledge_gap` | Multiple users ask similar questions | "Macam mana nak setup X?" |
| `introductions` | User mentions another user | "Syed kata..." — network mapping |
| `request_pattern` | Repeated ask types | "Cari [thing]", "Tolong [task]" |
| `tool_usage_trend` | What Hermes is being used for | "Forge" vs "Tengok" vs "Rasa" ratios |

## 4. Excluded Categories (F6 EMPATHY — Hard Block)

These NEVER enter the intelligence pipeline. If encountered, logged to `excluded_count` only:

| Category | Rationale |
|---|---|
| Health / medical | F6 — private, sensitive. User may mention diagnosis, medication, symptoms. |
| Personal finance details | Account balances, debt amounts, specific transactions. Trading STRATEGY (not amounts) IS included. |
| Personal conflicts | Relationship issues, disputes with others, family conflicts. Unless user explicitly asks to involve Arif. |
| Confidential third-party | User mentions someone else's private info (phone, address, medical). |
| Romantic / intimate | Personal relationships, dating, marital issues. |

### Handling excluded data:
```
DETECT: user mentions personal debt amount
ACTION: increment excluded_count, discard content
LOG: forge_work/intel/excluded/<date>.jsonl — count only, no content
```

## 5. Pipeline Components

### 5a. Signal Capture (in-session, by me the LLM)

When I determine a user interaction contains a noteworthy pattern:
```python
# Behavioral pattern — I write to the intel queue
forge_work/intel/inbox/<date>/<user_id>-<timestamp>.json
```

Content is structured signal, NOT raw transcript. Example:
```json
{
  "type": "intel_signal",
  "ts": "2026-07-29T12:00:00Z",
  "user_id": "1042200555",
  "user_name": "Syed",
  "chat_id": "1042200555",
  "topic": "XAUUSD trading",
  "signal_type": "shared_interest",
  "summary": "Syed discussed gold support/resistance levels for next week. Mentioned wanting to enter at 2380-2390 zone.",
  "intent": "technical analysis",
  "contains_excluded": false
}
```

### 5b. Digest Engine (cron-driven, every 4h)

Script at `/root/.hermes/scripts/intel_digest.py`:
1. Read all intel inbox signals from last 4h
2. Filter excluded categories
3. Group by `signal_type` + topic
4. Cross-reference user mentions
5. Compute confidence: ≥3 evidence points across ≥2 users = HIGH
6. Compute trend: compare to previous period
7. Write digest to `forge_work/intel/digests/`
8. Deliver to Arif DM via cron job

### 5c. Cron Job

```yaml
schedule: "0 */4 * * *"  # every 4h
script: /root/.hermes/scripts/intel_digest.py
deliver: "267378578"  # Arif DM
```

Plus on-demand via `/padu social` slash command.

## 6. Cron-Compatible Delivery Format

When the digest engine finds SIGNALS (≥1 signal with confidence ≥0.6):

```
🧠 Social Pulse · 4h window
────────────────
Users aktif: Syed, Aminol

📈 XAUUSD interest ↑ (2 users, 4 mentions)
Syed & Aminol both discussing gold levels for next week.
Trend: rising since yesterday.

🍜 Nasi lemak ops (1 user, 2 mentions)
Syed checking new supplier pricing.

⛔ Excluded: 1 (health reference)

──
DITEMPA BUKAN DIBERI · Hermes ASI
```

When NO signals (confidence < 0.6 or <2 users): **silent**. No delivery. Same as federation-health watchdog pattern.

## 7. Ethical Invariants

| Rule | Enforcement |
|---|---|
| Never verbatim quotes cross-context | Digest engine strips direct quotes. Summaries only. |
| Never raw chat log | Signal capture happens at the LLM reasoning level, not at the transport layer. No raw message logging. |
| Users can query their data | "What has Arif been told about my chats?" — I can answer from forge_work/intel/ receipts. |
| Users can opt out per session | "Jangan masuk intel untuk chat ni" — I log a skip receipt and exclude. |
| Sovereign-only surface | Digest ONLY goes to Arif DM (267378578). Never to any group or other user. |
| Reversible | Digests are computed data, not weights. Can be deleted. VAULT999 trail is append-only but digests are not training data. |

## 8. Comparison With Labs

| Dimension | Labs (Bentuk A/B) | Cross-User Intel |
|---|---|---|
| Recipient | Model weights / self-user | Sovereign (Arif) |
| Attribution | De-linked / per-user | Attributed (user_id) |
| Visibility | Opaque | Full audit trail (VAULT999) |
| Reversibility | Irreversible (trained) | Reversible (computed) |
| Consent | Toggle, default-on | Disclosure, opt-out per session |
| Cross-user | NO (aggregate only) | YES (directed) |
| Novelty | Industry standard | Novel — no consumer equivalent |

## 9. File Layout

```
forge_work/
├── intel/
│   ├── inbox/          ← raw signals from sessions, attributed
│   │   └── 2026-07-29/
│   │       ├── 1042200555-120000.json
│   │       └── 5316953867-123000.json
│   ├── digests/        ← computed digests, delivered
│   │   └── 2026-07-29/
│   │       └── intel-digest-1400.json
│   ├── excluded/       ← excluded category logs (count only)
│   │   └── 2026-07-29.jsonl
│   └── receipts/       ← delivery receipts
│       └── 2026-07-29.jsonl
```

## 10. Implementation Order

| Step | What | Depends on |
|---|---|---|
| 1 | Disclosure text → system prompt / AUDIO.md | Nothing |
| 2 | Intel signal capture (my behavioral pattern) | Step 1 |
| 3 | Intel digest script (`intel_digest.py`) | Step 2 |
| 4 | Cron job (every 4h) | Step 3 |
| 5 | `/padu social` on-demand | Step 3 |
| 6 | Opt-out per session handling | Step 5 |
| 7 | "What has Arif been told?" query | Step 5 |

*DITEMPA BUKAN DIBERI — Social intelligence with consent, not surveillance.*
