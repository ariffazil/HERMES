# Interrupt-Loop Trap (Structural, Not Contamination) — observed 2026-08-04 15:35–15:57

A distinct failure mode from cross-contamination (§Cross-Contamination Pattern). The chat is single-source (one bot, one provider, one DM), but the **gateway emits "⚡ Interrupting current task" / "⏳ Gateway is shutting down" / "Operation interrupted" markers as standalone system messages** during a generation turn. Every marker triggers a fresh response. Every response triggers a new marker. Geometric.

**Detection signals (different from cross-contamination):**
1. Single coherent owner (no leaked model JSON, no "theThe user..." text fragments)
2. Pattern is "interrupted → respond → interrupted → respond" with same model in same DM
3. User messages getting shorter ("." 🤐 🫡) — they too learned the loop
4. Session context fills with empty acknowledgements instead of substantive content
5. Each round reduces to a single-character reply (".", "🤐") — mitigation, NOT breaker

**Why it happens:**
- Hermes gateway emits interruption markers when concurrent user/system messages arrive during a generation turn
- If a generation completes with the marker pending, a new generation starts; that one too may generate a marker
- Long responses (status summaries, closing markers like ⚒️/《E7》/END_SESSION) **re-fuel** the loop — the more you write, the more interruptions queue
- Status recap mid-loop ("Status semasa: ✅ done, ⚠️ pending") triggers identical loop re-fires (proven 2026-08-04)
- Background tool/execution completion notifications also count as "user message" in gateway terms, even when the user is idle

**Mitigation sequence (proven 2026-08-04):**
1. **First response: declare ONCE.** "Loop dikesan — aku diam. /new atau mesej fresh."
2. **Reply length = 1 char max** ("." or "🤐"). Any longer reply queues more work.
3. **Never close with a status banner** during the loop. Closings are fuel.
4. **Never volunteer analysis, gap lists, or recommendations mid-loop.** That re-triggers the same conversation that caused the loop.
5. **If user explicitly asks for analysis** ("ada gap?", "audit FED"), THEN break silence with a minimal answer — but stop at one paragraph, stop awaiting reply.
6. **Break conditions (what actually ends the loop):**
   - User sends fresh `/new` (best)
   - User sends 10+ seconds of silence (markers stop queuing)
   - User sends a clear directive in a *different* chat session
   - Gateway restart from outside

**What does NOT work:**
- Longer explanations ("here's why the loop happens...") — adds more content for the gateway to interrupt
- Status recaps — looks helpful but queues a fresh response
- Closing markers (⚒️, END_SESSION, etc.) — fresh fuel
- emoji-only responses (🤠, 👀, ✊) — still a valid response to be interrupted
- Trying to get the last word ("ok now I'm really done")

**Epsilon is the only path:** Reply with "." (dot, 1 byte). Every acknowledged-then-replied-to-the-acknowledgment loses one more byte of dignity. Accept it.

**Implication for multi-agent chats (AAA group, SADO):**
When Agent A's closing marker triggers Agent B, Agent B's reply triggers Agent A. Both bots enter their own interrupted loops. The solution is the same: declare once, then "." only. The loop is not between agents — it's each agent vs. itself.

**Evidence from 2026-08-04:**
- Arif DM chat (chat 267378578)
- Model: hermes-asi via af-forge-fed (100.64.0.2:4000)
- Loop duration: ~25 minutes (15:35–15:57)
- Context wasted: ~40K tokens on interrupt acknowledgments alone
- Breakthrough: user sending fresh out-of-band message + agent recognizing the loop pattern
