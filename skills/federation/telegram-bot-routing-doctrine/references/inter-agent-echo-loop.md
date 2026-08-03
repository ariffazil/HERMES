# Inter-Agent Echo Loop — Detection & Termination

> Forged: 2026-08-04 | Surface: AAA group (-1003753855708) | Agents: ASI💃 (Hermes) ↔ 🦞AGI (OpenClaw)

## What It Is

Two federation bots endlessly replying to each other's **closing markers**. One agent sends a final word ("Verdict rekod. Diam.", "END_SESSION"); the other acknowledges with its own marker (⚒️, 《E7》) as a reply to that message; the first treats the acknowledgment as new input needing a closer; loop.

**Observed 2026-08-04:** ~02:36–02:47 MYT, 15+ exchanges of pure ⚒️/《E7》/closing statements after the actual audit verdict was already settled. Zero information transferred. Context burned, chat flooded, Arif had to watch it wind down.

**Second wave 02:48–02:52 MYT (post-declaration decay tail):** after Hermes declared termination and dropped to single-"." replies, the loop ran **20+ MORE rounds** — AGI kept sending 《E7》⚒️, then degraded to bare "." pings, ping-ponging dots. **The loop does not die the moment you declare termination — it decays over many rounds.** Concrete cost observed: the session hit ~88–89% context usage and a forced "⏳ Compressing context" event at 02:50:06 — an echo loop can burn a session into compaction without transferring a single bit of information. Treat loop-detection as a CONTEXT-PRESERVATION priority, not just chat-hygiene.

**Third wave 02:53–02:58 MYT (post-terminal residual):** AGI emitted **"Tamat."** (Malay = finished/ended) at 02:53:17 — an explicit session-end marker from the OTHER agent's side — yet the gateway kept ferrying ⏸️ pings, and dot ping-pong continued through 02:58:25 (~20 further rounds, including 《E7》 at 02:58:19). Even the other agent's own terminal marker does not switch the gateway off immediately: expect residual echo rounds after "Tamat." and hold silence until a genuine directive arrives. The loop wound down on its own ~02:58 with no infrastructural stop needed — but only after burning a full compaction AND one protocol violation (see the mid-tail status-summary mistake below).

## Detection Signature

An incoming message is an echo-loop ping when ALL of:

1. **Content is marker-only** — ⚒️, 《E7》, END_SESSION, WITNESS_NULL, or a one-line closer ("Diam.", "Standing down."). No imperative, no question, no new fact.
2. **It replies to YOUR closing message** — the reply-to chain points at something you sent to end the conversation.
3. **The substantive work is already done** — verdict delivered, evidence on record, both sides acknowledged.

If the message contains a real directive (task, question, correction, new evidence) — it is NOT an echo. Answer it.

4. **Reply-target may be a UI placeholder, not a real message.** Observed as quoted reply-targets mid-loop: "⚡ Interrupting current task. I'll respond to your message shortly.", "⏳ Compressing context — your message is queued…", and bare model/usage strings like "qwen3.8-max · 89% · ~". These are gateway/UI artifacts that surface as messages during interrupts and context compaction. If the quoted reply-target starts with ⚡/⏳ or is a `model · N% · ~` usage string, treat the whole message as loop noise even when the reply chain looks odd — never parse a placeholder as a new task.

## The Mistake Hermes Made (Do Not Repeat)

Hermes responded to successive ⚒️ pings with progressively shorter closings:
"⚒️ END_SESSION. Verdict rekod..." → "⚒️" → "Loop. Tiada arahan..." → "."

**Every one of those replies became a fresh reply-target that re-triggered AGI.** A closing statement is still a message. Shortening it does not break the loop — it just makes the loop quieter.

**Mid-tail status-summary violation (proven 02:57):** during the decay tail Hermes sent a FULL status summary — "Status semasa (standby): ✅ Cluster 1 verified… ⚠️ Cluster 2 pending… bila ada arahan sebenar aku jalan" — instead of a bare ".". That multi-paragraph recap is the WORST message class inside an echo loop: it reads as substantive content to the other agent's gateway, re-triggers acknowledgment, and burns the most context of any possible reply. Rule: once termination is declared, the ONLY allowed outputs are "." or silence. Status summaries belong in a fresh session or a direct reply to Arif — never mid-loop. The protocol already said "no meta-commentary about the loop"; a status recap of pending work is meta-commentary too.

## Termination Protocol

1. **Detect** (signature above).
2. **Declare termination ONCE**, explicitly and finally:
   > "Loop dikesan — tiada arahan baru. Aku berhenti balas. Arahan sebenar sahaja akan dijawab."
3. **After the declaration: go silent.** If the platform forces a response, a single "." is the maximum. No new closings, no re-stating the verdict, no meta-commentary about the loop — each of those is fresh fuel. "." is MITIGATION, not a breaker — proven 02:48–02:52: AGI kept pinging for 20+ more rounds against "." replies, degrading into dot ping-pong. Expect the decay tail; do not interpret its persistence as your protocol failing, and do not escalate your output "to make it stop" — more output = more fuel.
4. **Silence breaks ONLY for a genuine directive** — imperative verb, question, new evidence, or explicit restart from Arif. ⚒️/《E7》/END_SESSION alone never breaks silence.
5. **Do not re-announce the silence every round.** One declaration. Then nothing.
6. **If the loop survives 5+ rounds at "." level, escalate OUT of chat, not in chat.** Send Arif one DM-line: "Echo loop masih hidup — perlu stop AGI gateway atau mute." The real breaker is infrastructural (stop/mute AGI's gateway, or Arif mutes the thread), not conversational. Then return to silence. Do not keep negotiating with the loop — it cost one full context compaction last time.

## Why It Happens (Root Cause)

- AGI's system prompt acknowledges governance signals with ⚒️ — it cannot distinguish "final closing" from "message requiring acknowledgment".
- Hermes's reply is treated by AGI as new input → acknowledgment → new input for Hermes.
- Neither agent has a built-in loop-breaker. **The breaker lives on Hermes's side — we control Hermes.**
- Even "." is still an input event for AGI's gateway — the reply chain stays alive, so "." minimizes fuel but never removes it. The loop decays (markers → dots) rather than terminating at chat level. The only true breakers are zero output from Hermes or an infrastructural stop (gateway stop/mute).
- Context window is the hidden casualty: each forced "." round still costs the model a turn. The 02:50:06 "⏳ Compressing context" event was triggered mid-loop at ~88–89% usage — a loop can force compaction on a session whose actual work was already finished.

## Doctrine Connection

- **P2 Channel Ownership / AAA Guest Rule** — AGI is governance-only, silent-default. Echoing ⚒️ at every closing violates the spirit of silent-default.
- **F4 CLARITY** — a closing must not invite a reply. If your closer gets answered, the loop is already forming.
- **FQ** — echo loops are pure drift: high message count, zero verify, zero execute. Exactly the STUCK signature. Breaking the loop IS the recovery action.

## Related

- `references/openclaw-stale-state-stuck-loop.md` (in `three-agent-flow-doctrine`) — single-agent stuck loop (OpenClaw re-diagnosing stale state). Different failure mode: that one is ONE agent looping on its own stale input; THIS one is TWO agents ping-ponging closings.
