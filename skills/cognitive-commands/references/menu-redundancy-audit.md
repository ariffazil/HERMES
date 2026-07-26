# Telegram Menu Redundancy Audit — Methodology

> Performed: 2026-07-26 | Result: 46 commands → 21 (15 cognitive + 6 built-in)

## The Contrast Check

Every command in the Telegram menu must answer **one unique question** — the same question no other command answers. If two commands answer the same human need, one must leave the menu (triggers stay active for backward compat).

### Step 1 — Map each command to its core question

```
/000_salam   → "Reset everything. Start fresh."
/111_tengok  → "What's actually there right now?"
/333_forge   → "Execute this. Make it real."
/555_betul   → "Is this really right? Challenge it."
/666_rasa    → "How do I/we feel?"
/777_faham   → "Connect the dots. What's the pattern?"
/888_adil    → "What's the right verdict?"
/999_ingat   → "Make this permanent. Seal it."

/ask_curious → "Explore freely. No agenda."
/tell_share  → "Teach me something."
/dream_what  → "Connect distant ideas creatively."
/feel_state  → "How are we doing right now?"
/forget      → "Let this go. Release."
/learn_today → "Capture this insight."
/see_world   → "What's happening out there?"
/rest_now    → "Pause. Take a break."
/grow_better → "What did I learn? What's better?"
/flow        → "Where's the energy? What's moving?"
/brief_now   → "Quick intel. Right now."
/seal_it     → "Seal this moment to VAULT999."
/think_deep  → "Think hard about this."
/forge       → "Build something. Create."
/padu        → "Show me everything. Federation mirror."
```

### Step 2 — Group questions that overlap

| Overlap group | Commands | Decision |
|---------------|----------|----------|
| State check | `/feel_state`, `/666_rasa` | `/666_rasa` wins (zen spine). `/feel_state` → menu out, trigger stays. |
| World view | `/see_world`, `/111_tengok` | `/111_tengok` wins (zen spine). `/see_world` → menu out. |
| Seal/permanent | `/seal_it`, `/learn_today`, `/999_ingat` | `/999_ingat` wins (zen spine). Both others → menu out. |
| Quick status | `/brief_now`, `/padu` | `/padu` wins (more comprehensive). `/brief_now` → menu out. |
| Presence/energy | `/flow_alive`, `/flow` | `/flow` wins (bare verb, canonical). `/flow_alive` → trigger removed entirely. |
| Exploration | `/ask_curious`, general queries | Not actionable — `/ask_curious` → menu out (dangling entity). |

### Step 3 — Verify survivors have zero overlap

After stripping, the remaining 15 custom commands have distinct core questions:

```
000_salam    AWAKEN     — reset/start
111_tengok   PERCEIVE   — see what's real
333_forge    FORGE      — execute
555_betul    DOUBT      — challenge
666_rasa     FEEL       — vitality
777_faham    UNDERSTAND — insight
888_adil     JUDGMENT   — verdict
999_ingat    REMEMBER   — seal
flow         BE         — presence/witness
forge        BUILD      — create
forget       RELEASE    — let go
padu         ZEN FED    — reflect all
think_deep   REASON     — analyze
dream_what   CREATE     — imagine
rest_now     PAUSE      — stop
```

## Key Principle

**A command in the menu must be irreplaceable.**
If another command can do its job with one more word or one more probe, it doesn't need its own menu slot. The test: "If I removed this from the menu, would the user lose functionality or just convenience?" If convenience, strip it.

## Evolution

| Date | Menu count | Change |
|------|-----------|--------|
| 2026-07-10 | 46 (24+22) | Full cognitive set |
| 2026-07-26 | 21 (15+6) | Redundancy audit. Stripped: brief_now, feel_state, see_world, seal_it, learn_today, grow_better, ask_curious, tell_share, dream_what removed from menu. /flow_alive removed from triggers. |
