# Arif Pattern-Aware Auditing — Reference

This reference captures **patterns validated in the A2B IJCAI 2026 audit (2026-07-03)** that are likely to repeat in any future submission-readiness audit involving Arif. Read it before starting the next one.

## The Single Most Important Pattern

**Arif "sprints then seals".** This is the operational risk that dominates every audit. Validated by:

1. **Git history at A2B**:
   - 3 commits total / 30 days (vs arifOS 643, A-FORGE 274, AAA 351)
   - All 3 on the same day (2026-06-27)
   - Commit message #2 was `feat: IJCAI 2026 submission package — paper, notebook, dataset loader`
   - Commit message #3 was `seal: A2B IJCAI 2026 session closure — handoff to AGI hardening`
   - **Then 6 days of silence before the 2026-07-03 audit session**

2. **Message tone evolution**:
   - First messages in the audit cycle: technical, asking for research ("deep research the requirements")
   - Mid-cycle messages: confusion signals ("still not clear here"), frustration ("enough coding stuff, talk to me in reality human language")
   - Late-cycle messages: meta-framing ("I'm not a coder btw", "I only enter game I can win")
   - Final message: "I already reply daval email btw" (lowercase, casual, decisive)

3. **Real-world stakes indicator** — the actual commitment signal:
   - Direct email to research lead (Dhaval Patel) sent DURING the audit cycle
   - This was the moment that moved the recommendation from "decline Korea" to "Track B sprint with forced stop"

## Practical Implications for Future Audits

### Format your output three ways (validated 2026-07-03 second pass)

The 2026-07-03 audit cycle produced a second-pass refinement. Arif pushed back on Shape B with "Are we ready or not?? My question is very simple!" — meaning the conversation had moved past the table format into pure decision mode. The right answer was **"No. But start anyway."** Two sentences, nothing else.

**Shape A — ultra-short binary** (when Arif demands brevity, e.g. "Tulis pendek", "are we ready or not?? My question is very simple!"):
- ONE sentence verdict
- ONE move (if needed)
- Full stop. No tables. No bullets. No menus.

**Shape B — verdict + 5-row table** (default for "are we ready?"):
- Verdict sentence
- 5-row table
- Compressed tiered list
- Single-word prompt

**Shape C — full 12-section written artifact** (posterity / docs/ / agent-to-agent):
- Full 12-section structure
- Tier 1/2/3 prioritization
- All numbers, all paths, all timestamps
- This is what gets sealed to VAULT999

**The escalation rule:** if Arif says "no" to the current shape, escalate UP (A→B→C). NEVER escalate DOWN. If he asked for ultra-short and you gave him a 5-row table, that's a §14 violation. The shape is bound to the question, not to the skill.

Three modes, three shapes:
- **Decision mode** ("just give me the answer") → Shape A
- **Learning mode** ("show me what I'm deciding") → Shape B
- **Posterity mode** (artifact to seal) → Shape C

Match the shape to the mode.

Arif reads conversation artifacts in Bahasa Melayu + English casual register. Don't prepend technical preamble. He skims and decides.

### When to call the user a "coder" or not

He says "I'm not a coder btw". His actual git history says otherwise. **Don't correct him in writing.** He is telling you his *relationship to this specific code* at this specific moment. The honest output format:
- "Here is the state, here are the 9 missing things, here is what to do tonight"
- Not: a tutorial on what an MCP bridge is

### The stake-check question

Always ask or infer: **"Has the user made a real-world commitment that makes abandoning more expensive than continuing?"** If no, the audit must include a step that creates the stake (one-cite-of-email, one-portal-registration, one-name-on-paper) BEFORE recommending a sprint.

### Don't recommend what the user prefers

In the A2B audit, Arif's stated preferences shifted:
- "Want to go to Korea" (early)
- "Are we ready?" (mid — testing if even starting is possible)
- "I need you to evaluate whether we can do it or not" (late — explicitly asking for truth)
- "I only enter game I can win" (final — binding himself to outcome)

The audit's recommendation moved through Track A → B → forced-stop as more data emerged. **Never commit to a final recommendation until the stake is verified.**

### The Margins Principle (validated 2026-07-03)

Arif's closing line of the session: **"Eureka is always at the margins remember"**.

This is an operating principle, not a pleasantry. It applies to:

1. **Track selection** — Track 2 (16 submissions, governance-as-differentiator) over Track 1 (137 submissions, MIT/Columbia closed-book). Track 2 is the margin.
2. **Positioning** — arifOS as named substrate is the margin. "Yet another MCQ benchmark" is the center.
3. **Co-authorship** — AOB co-authorship on KDD paper is the margin. Standalone IJCAI submission is the center.
4. **Submission timing** — Jul 15 re-submit slot (after the chaos of Jul 7 first cut) is the margin. Aug 1 final is the center.

**Diagnostic question for any audit recommendation:** *Is this the margin or the center?* If the recommendation is the center (where everyone else is competing), reconsider. Margin moves are: lower competition, harder to replicate, aligned with the user's distinctive capability (governance, not raw model performance).

When the audit has 3 options, the **margin option** should be highlighted explicitly so Arif can see it. Not all margin moves are right — but a recommendation that ignores the margin principle is failing to use Arif's own lens.

### The forced-stop pattern is non-negotiable

For any 4-7 day sprint, the audit must include:
1. Daily tick from agent to user (Telegram, ≤1 line)
2. Day-3 ratification gate (agent halts if user hasn't signed off)
3. Track C unopposed fallback (agent drives submission alone if user goes silent)

Without these, the audit is a wish list. With them, it is a working plan.

### Three categories of state to always inventory

1. **Claimed numbers** — abstract fixed? Section 3 corrected? If only abstract fixed, contradiction sweep returns 5+ sites.
2. **Disk state** — git log, dirty trees, eval results count, file timestamps
3. **Real-world stakes** — emails sent, registrations filed, slots booked

The audit converges when all three say "consistent". The audit fails when any one of them differs from the others. The audit is dishonest when it hides the failure of one.

### The Communication Protocol That Worked

| User said | What they actually wanted |
|---|---|
| "deep research the requirements" | Comprehensive audit with sources cited |
| "still not clear here" | Drop the tables, talk to me like a person |
| "ok enough coding stuff, talk to me in reality human language" | Drop everything technical, lead with the verdict |
| "I'm not a coder btw" | Don't lecture me on the technical layer |
| "I'm serious wanna go to Korea" | All the formality ends here, give me a real plan |
| "I only enter game I can win" | Don't recommend Option A if disk says A won't fly |
| "I need you to evaluate whether we can do it or not" | I trust your judgment, be honest |
| "I already reply daval email btw" | I've already committed, the stake is real, now plan around it |
| "Now tell me are we ready to even start???" | Don't optimize for the deadline — optimize for the FIRST irreversible move |
| "I don't start game that I can't even compete here" | Chicken-and-egg framing. The right answer is the Big Bang reframe: "Ready" never arrives as a switch. Commit first, then find out. |
| "Are we ready or not?? My question is very simple!" | ONE sentence verdict. No tables. No bullets. If "No" is the verdict, the second sentence is "But start anyway." |
| "Tulis pendek" | Honor the request, do not rationalize verbosity as thoroughness |
| "Eureka is always at the margins remember" | **Operating principle.** Winning moves are at the edge (Track 2 vs Track 1, governance differentiator, AOB co-authorship) — not where everyone else is standing. When recommending a path, ask: is this the margin or the center? |

The hidden ordering is: research → clarify → humanize → honor the human's identity → take the goal seriously → demand real-game audit → trust the agent → recognize the commitment → **reframe the readiness question → compress the verdict → pick the margin**.

A future audit should arrive at the conversation phase already past the research phase, asking the real question.

## The Disk Truth Today (snapshot 2026-07-03 15:14 UTC, T-28d to IJCAI Aug 1)

- A2B: 4 eval runs on disk (smoke + run001_gov + run002_gov + run002_nogov), 152 trajectories total
- T1 identity: arifbench-eval registered in agent_identities.json (config fix completed)
- Paper: +803ms in abstract (line 14), -278ms still in 4 other locations (lines 125, 135-136, 267, 326)
- AssetOpsBench: cloned at /tmp/aob_ref but uv-sync pending, bridge.py (19KB, written 15:08) never tested
- Kaggle final-round deadline: Jul 7 (not Aug 1 — earlier deadline dominates)
- Real-world stake: 1 email sent to Dhaval Patel (IBM AssetOpsBench lead) — soft-hard boundary crossed
- Recommendation moving: from "decline Korea" → "Track B (sprint + forced stop + Track C unopposed fallback)"

This snapshot will be stale by next week. The pattern persists. Re-verify state every audit.

*DITEMPA BUKAN DIBERI — Pattern forged, audit arrived.*

*Captured 2026-07-03 by Hermes agent on F13 SOVEREIGN directive, mid-conversation during A2B IJCAI 2026 audit.*
