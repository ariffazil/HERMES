# Telegram Allow-List — Bug-First Debug Pattern

Authoritative addendum to `hermes-telegram-group-setup`. Use this **whenever Arif reports a behavioral break** ("bot doesn't reply", "make bot reply in SADO", "add this chat"). It encodes the failure mode where the agent starts asking config questions before confirming the actual symptom is config-related.

## Core lesson (2026-08-05 session — bot-silent-in-SADO case)

Arif wrote: *"weiii akubnaknhermes agebt bokeh reply dalam group sado"*

What actually broke: gateway_state.json `"platforms.telegram.state": "disconnected"` since 11 days, `"active_agents": 0`. The bot wasn't replying because the gateway process was offline. The allow list was fine — `TELEGRAM_ALLOWED_CHATS` already contained `-1003815535761` (SADO group) and `TELEGRAM_ALLOWED_USERS` already contained `1042200555` (Syed @rico_ricaldo_33, "Abang Sado").

What I almost did instead: build a 6-metadata-labeled directory of all 15 Telegram IDs, ask "OK to write?", "pick option 1/2/3/4", then ask again. Three turns of bureaucratic friction on top of a question that had already been answered in plain text in the user's first message.

## The bug-first rule (always do this)

When Arif reports behavior, do this BEFORE asking any clarifying question:

### Step 1 — Distinguish the three failure modes

Map his words to one:
- **"fix access"** → allow list missing X (env mutation territory, F13-gated)
- **"fix behavior"** → bot silent in X (gateway/process territory)
- **"fix format"** → X is allowed but unreadable (UX/display territory)

Do not conflate. Do not silently promote a format ask to an access mutation.

### Step 2 — Verify the symptom is what you think it is

```bash
grep "TELEGRAM_ALLOWED" /root/.secrets/kunci-mas.env
```

If Arif just pasted an ID and called it by name (e.g. "ni sado group. -1003815535761. ni syed. 1042200555"), check whether that ID is already in the list. **If yes, the allow list is not the bug. Move on.**

### Step 3 — Check the gateway, not the config

```bash
cat /root/.hermes/profiles/hermes_asi/gateway_state.json   # or apex/forge
```

Look at:
- `"platforms.telegram.state"` — "connected" / "disconnected"
- `"active_agents"` — process count (0 = dead)
- `"updated_at"` — state file freshness. >24h stale = watchdog itself broken

If any of these is bad, the bot doesn't reply regardless of allow list. Surface that to Arif; don't ask him what to change.

### Step 4 — ONE message: ground truth + fix options

Single report with all the data bundled. Format:

```
Ground truth:
  - SADO -1003815535761 already in TELEGRAM_ALLOWED_CHATS (verified)
  - Syed 1042200555 already in TELEGRAM_ALLOWED_USERS (verified)
  - gateway_state.json: telegram "disconnected" since 11d
  - active_agents: 0

Actual break: gateway process. Allow list OK.

Fix paths:
  (1) systemctl restart hermes-gateway-asi
  (2) check if bot token rotated; re-export
  (3) HOLD — investigate logs first
```

ONE message. Then wait for Arif's choice. Do not re-ask.

## Anti-patterns (do NOT do)

### ❌ Bureaucratic review loop
Asking "OK to write?" / "pick option 1/2/3/4" three times across three turns for a T1 file create. Respect the review-before-apply pattern by asking **once** with all context bundled.

### ❌ Scope creep into "while we're here"
Arif mentions one group. Agent responds by proposing a full directory of all 15 IDs with metadata. No — do the ask. Readability/format is a separate task that Arif explicitly asks for.

### ❌ Asking user to label IDs the agent can derive
If Arif pasted "ni sado group. -1003815535761", you just learned the mapping. Don't ask "which ID is SADO?" back to him.

### ❌ Conflating Q&A with config mutation
Arif pastes Syed's ID answering an earlier question. Don't treat that as a config-change proposal. Confirm: yes, already in list. Move on.

### ❌ Three "are you sure?" confirmations on T1 work
T1 file creation with mode 600 + no systemd restart + no env mutation = safe to do with one confirmation. Save two-of-three for T3 territory.

## Key reference data (snapshot 2026-08-05)

- Allow list SOT: `/root/.secrets/kunci-mas.env` (mode 600, root:root, Iron Rule)
- Channel/group snapshot: `/root/.hermes/profiles/<profile>/channel_directory.json`
- Gateway state: `/root/.hermes/profiles/<profile>/gateway_state.json`
- Active profiles (default = empty husk): `hermes_apex`, `hermes_asi`, `hermes_forge`
- Telegram 2026-08-05 confirmed: SADO group -1003815535761 and Syed 1042200555 are ALREADY allow-listed. No mutation needed unless Arif wants format/readability work.

## When format task IS legitimate

Only when Arif explicitly says "label semua", "senang nak read", "format bangang". Then the work is:
1. Build `/root/.secrets/telegram_directory.json` (separate file, mode 600, root:root)
2. Schema:
   - `_meta` (purpose, role, updated date)
   - `users` map (positive IDs → {name, telegram_handle, role, f13_unrestricted})
   - `groups` map (negative IDs → {name, topic, members})
   - `home_channel_drift` block (HOME vs ALLOWED diffs)
   - `csv_environment_variables_source_of_truth` echo block
3. Do NOT mutate KUNCI-MAS env vars
4. Do NOT restart anything

If the format task has dedup work (e.g. -1003815535761 appears twice in CSV), surface it; do not auto-fix without F13 ack (env mutation = T3).
