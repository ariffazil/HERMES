---
name: submission-readiness-audit
title: Submission Readiness Audit — Deadline-Driven Gap Analysis for Federation Submissions
description: "Reverse-engineer the gap between current state and a hard external deadline (conference, journal, internal governance review). Produce a Tier 1/2/3 prioritized gap list, a 3-option recommendation (A submit-as-is, B extend to spec, C defer), and a federated action plan. Use when Arif asks 'are we ready for X', 'what's needed to submit', 'list down what's needed', 'is the deadline realistic', or names a specific submission target with a date."
version: 1.1.0
author: arifOS Federation (Hermes agent, on F13 SOVEREIGN directive, 2026-07-03; v1.1 supplements stake-aware + output-shape + forced-stop patterns, 2026-07-03)
license: MIT
metadata:
  hermes:
    tags: [submission, readiness, audit, deadline, ijcai, kdd, conference, gap-analysis, planning, federation]
    category: research
    related_skills: [scientific-manuscript-forge, geox-federation-mcp-driver, institutional-epistemic-sink-forensics, seven-zen-organs-enforcement, plan, requesting-code-review]
---

# Submission Readiness Audit

A class-level discipline for **reverse-engineering the gap between current state and a hard external deadline**. Distinct from `plan` (which writes a forward implementation plan from a clear spec) and from `scientific-manuscript-forge` (which produces a single falsifiable artifact). This skill audits the *submission-ready state* of an existing work-in-progress.

## Companion files
- `references/a2b-ijcai-2026-audit-2026-07-03.md` — canonical worked example (29 days to deadline)
- `references/kaggle-spa-deadline-extraction.md` — browser_navigate + browser_console DOM text extraction
- `references/arif-pattern-aware-auditing.md` — **Arif's operational pattern (sprint-then-seal), real-world-stake diagnostic, communication-shape rules** — read before starting the next audit that involves Arif as the human
- `references/research-paper-quality-checklist.md` — **3-tier checklist (minimum viable / research-grade / publication-ready)** for evaluating paper quality. Use when the question is "is this paper good enough" alongside the deadline question.

## When to use

Use when Arif (or a federation agent) asks:
- "Are we ready for [conference/deadline]?"
- "What's needed to submit?"
- "List down what's needed"
- "Is the [date] deadline realistic?"
- "What do we have / what's missing / what's chaos?"
- "Deep research the requirements"
- "Can we make [date]?"
- Names a specific submission target with a date (e.g. "IJCAI 2026", "NeurIPS 2026", "KDD 2026", "AAAI 2026", "internal audit 2026-Q3")

Do NOT use when:
- The work has not started (use `plan` instead to scope it)
- The submission target is clear but the work is one task (use `plan` for the task)
- The user wants a general health check (use `federation-organ-liveness-probe`)

## Multi-Track Awareness (added 2026-07-03 IJCAI IAC audit)

When a competition or conference has **multiple tracks** with different rules:

| Symptom | Action |
|---|---|
| Track 1 (closed-book, proprietary-LLM-banned) + Track 2 (open, tool-augmented) | Disqualification risk on Track 1. **Verify your model category before submitting.** |
| Multi-track Kaggle competition has `(1 July) ...` update notices referencing one track only | Probe BOTH tracks separately. Each has independent rules. |
| Different CSV column sets per track (`id,option,option_desc` vs `id,option,option_desc,model_name,model_param_size,...`) | Match format to track BEFORE building the submission file. |

Pattern: read the Kaggle "Tracks" tab/section + competition `Overview` per-track + sibling `competitions/.../track-N` URLs. Don't infer a track's format from another.

**Kaggle SPA deadline extraction technique:** when the deadline lives behind a JS SPA, see `references/kaggle-spa-deadline-extraction.md` — uses `browser_navigate` + `browser_console(expression=...)` to read rendered DOM text. Validated 2026-07-03.

## The 10-section structure

Every audit follows this structure. Length 200-350 lines, 10-20 KB.

### 1. TL;DR — Verdict First
One paragraph. Are we ready? Why? Single biggest risk? Recommendation.

### 2. What You Have (Current State — Disk-Verified)
For every artifact: path, lines, last modified, purpose, honest verdict. Use `[OBS]` markers for disk-verified facts.

### 3. What's Missing — Tier 1/2/3
- **Tier 1 — MUST DO** (without these, submission has integrity holes)
- **Tier 2 — SHOULD DO** (strengthens the work)
- **Tier 3 — NICE TO HAVE** (v2 or follow-up)
Each item: effort estimate, why, first move.

### 4. What's Chaos
Three sub-sections: (a) submission claims vs disk reality, (b) architectural misalignments, (c) tooling drift. **The most important section** — the difference between polished and useful audits.

### 5. What's Needed — Concrete List
Tier 1 + critical Tier 2 from §3, with effort and first move. Plus honest time budget table.

### 6. The Risk Matrix
Table of risks with likelihood, impact, mitigation.

### 7. Recommended Path — 3 Options
Always exactly 3, never more. Each option: What it is, Pros, Cons, Probability of acceptance. End with one explicit recommendation.

### 8. The Critical Unknown
The agent's honesty boundary — what it cannot verify. Action item for the human with specific time budget.

### 9. The Federated Action Plan
Day-by-day with owner and why. Include buffer (10-20% of total).

### 10. What's Chaos — Call It Out
The most important section. Names the unresolved chaos. Recoverable if named early. Catastrophic if hidden.

11. Constitutional Receipt
Fixed-shape block: file, author, verdict, deadline, tier_efforts, buffer, critical_unknown, push.

12. One-line kernel
One falsifiable, actionable sentence. Always last.

## §13. The Real-World Stake Diagnostic (added 2026-07-03)

Arif's repeated operational pattern, validated through git history:

| Pattern | What it looks like |
|---|---|
| **Sprint-then-seal** | 12-hour focused session, then commit message "session closure / handoff to AGI hardening", then 6+ days of silence. |
| **Sealed-before-substantive** | `seal` or `closure` commit message landing on the same day as the initial scaffold. |
| **Public repo velocity vs submission velocity** | arifOS: 643 commits / 30d (sustained). A2B: 3 commits / 30d (sprint-only). Submissions live in the gap. |

**The diagnostic question**: *Has the user already made a real-world commitment that makes abandoning more expensive than completing?*

| Stake level | Indicator | Audit adjustment |
|---|---|---|
| **NONE** | No external contact made, no registration filed, no slot booked | Cap recommendation at "defer" until stake is formed |
| **SOFT** | Internal teams know (AAA, A-FORGE agents working) | Use Track A (sprint with daily tick) |
| **HARD** | External contact exists (email sent to research lead, submission portal registered, ticket booked) | Use Track B (sprint with forced stop; commits the user to acknowledge gap if they bounce) |

**Why this matters**: an audit that produces a "ready to start" plan without verifying a hard stake is **the most common failure mode of this skill**. The recommendation must include a stake-assessment step. Reference: A2B IJCAI 2026 audit — the user replied to Dhaval Patel *during* the audit cycle, which moved the recommendation from "decline Korea" to "Track B sprint with forced stop + Track C unopposed backup".

## §14. Output Format When Talking to Arif Directly (added 2026-07-03, tightened 2026-07-03)

Arif reads in Bahasa Melayu + English, terse, no preamble. He does not process long technical reports natively — he processes:
- A short "real answer" first
- A table or checklist he can tick
- A single-word sovereign signal at the end ("GO" / "DECLINE" / "T2")

**There are now THREE output shapes — pick based on how Arif asked:**

### Shape A: Ultra-short binary (when Arif demands brevity)

Triggers: "Tulis pendek", "Are we ready or not?? My question is very simple!", "Just give me the answer", explicit frustration with verbosity, "stop doing X" / "this is too verbose".

Format:
- ONE sentence verdict
- ONE move (if needed)
- Full stop. No tables. No bullets. No menus.

Example (validated 2026-07-03): User asked "Are we ready or not?? My question is very simple!" — the correct answer was **"No. But start anyway."** Two sentences. Nothing else. The user accepted and moved on.

If the user complains after this shape, the next shape (B) is needed. If they accept and act, the shape was right.

### Shape B: Verdict + table (default for "are we ready?" / readiness questions)

Format:
1. **Lead with the verdict.** One sentence. "No, we are not ready" / "Yes, with conditions" / "Yes".
2. **Then a 5-row table** with: deadline | days remaining | what's missing (T1) | what blocks (T0) | sovereign call needed.
3. **Then the tiered list** but compressed. Bullet form, not paragraphs.
4. **End with a single-word prompt** for the next action.

### Shape C: Full 12-section written artifact

When delivering this audit **as a written artifact** (commit to docs/, share with another agent), use the full 12-section structure + §13 + §14. This is for posterity, not the human's chat.

### The escalation rule

If Arif says "no" to the first shape, escalate UP to shape B or C. NEVER escalate DOWN — if Arif asked for ultra-short and you gave him 5-row table, that's a §14 violation. If he asked for a verdict and you gave him a §3 tiered list, that's also a violation. The shape is bound to the question.

### Why this matters (validated 2026-07-03)

The same audit cycle produced BOTH Shape A (binary "No. But start anyway.") and Shape B (5-row table + tiered list + single-word prompt) in the same session. Arif accepted Shape A. Arif pushed back on Shape B with "Are we ready or not?? My question is very simple!" — meaning the conversation had moved past the table format into decision mode.

**The lesson:** when the user is in DECISION mode (not learning mode), Shape A wins. Shape B is for LEARNING mode ("show me what I'm deciding"). Shape C is for POSTERITY mode (artifact to seal).

Three shapes, three modes. Match the shape to the mode.

## §15. The Forced-Stop Pattern (added 2026-07-03)

When a recommendation could plausibly trigger abandonment at Day 2-5, **build in a forced stop.** The audit should explicitly include:

- A "Day 3 ratification gate" — if the user has not signed off on a draft by Day 3, the agent halts regardless of state and reports where it is
- A "Track C unopposed fallback" — even if the user goes silent, the agent drives the submission unopposed, with daily ticks the user can ignore

This is not optional. The user-pattern reality **demands** this. Audits without forced-stop patterns will read like good plans and abandon like bad ones.

## Pitfalls (Discovered 2026-07-03, supplemented 2026-07-03)

1. **Don't fabricate verification.** If the agent cannot verify (e.g. external format, reviewer criteria), name it as a critical unknown. The human verifies.

2. **Don't recommend the loudest option.** The recommendation is the most honest option for the actual time budget, not the option that sounds best.

3. **Don't count buffer as 0.** Every deadline has unknowns. If the plan uses 100% of available days, it will slip. Include 10-20% buffer.

4. **The 3-option table is not optional.** If you can't fill all 4 columns (What/Pros/Cons/Probability), you don't understand the situation yet. Go back to §2.

5. **The "what's chaos" section is the most important.** It's the difference between a polished audit and a useful audit. Audits that hide chaos are false confidence.

6. **The critical unknown is the agent's honesty boundary.** If the agent cannot verify, the human must. The audit should make this explicit and actionable.

7. **The day-by-day plan must be bite-sized (2-5 min tasks) and include explicit owner.** A plan that says "FORGE does the work" without breaking it down is a wish, not a plan.

8. **The recommendation is not the user's preference.** If the user wants Option A but the disk doesn't support A, recommend B or C anyway. The audit serves truth, not deference.

9. **Use Tier 1/2/3 not "Critical/High/Medium/Low".** T1 is what you must do; T2 is what you should do; T3 is what you'd love to do.

10. **Submission claims vs disk reality is a separate audit pass.** Every claim in the submission must be checked against the disk. Three integrity risks caught in the IJCAI 2026 A2B audit (2026-07-03): "negative latency" (−278ms claimed, actual +803ms), "A-bias 74%" (paper+companion, disk 42%), "3 evals on disk" (companion, disk 4). The audit catches all three with one table-merge.
11. **Paper retraction > paper correction when contradiction is structural.** If a paper claim cannot be reconciled with disk (e.g. wrong direction of effect, magnitude off by 1 order), mark it for retraction, not correction. Correcting a -278ms to +803ms requires re-running statistics; correcting a methodology error requires re-submission. **Don't paper over with a footnote.** Mark with `[INT]` (inferred-corrected) vs `[OBS]` (disk-verified) in any audit output.
12. **The 3-option recommendation must include "defer".** If the deadline is unrealistic for current state, deferring to the next submission cycle (Option C) is the honest recommendation — but always cite the next submission date as fallback.

13. **The "victory declaration" pattern (Arif-specific operational risk).** Validated 2026-07-03 across A2B git history: a sprint-then-seal pattern over 12 hours followed by 6 days of silence. **Recommendation must include a 'real-world stake' check** — a contact already made (an email sent, a registration filed, a slot booked) that makes aborting more expensive than continuing. Without that stake, the user will abandon between Day 2 and Day 5 of any sprint. See §13 below.

14. **The audit is half-true without the contradiction sweep.** Three patterns recur in submission artifacts: (a) abstract fixed but body unchanged (line 14 says +803ms, line 135 says "278ms faster"), (b) companion file claims different numbers from primary doc (paper says "74% A-bias", disk says 42%), (c) N artifacts claimed, N+1 (or N−1) actually exist. **Always grep for the disputed number across every artifact file before claiming the audit is complete.** Add an explicit `grep -rn '<disputed_string>' /root/<repo>/` step in the reproduction recipe.

15. **The "are we ready?" loop is sometimes an axis problem, not a capability problem (validated 2026-07-03, A2B / IJCAI-KDD session).** If Arif asks "are we ready" three different ways in one session and the disk-side answer doesn't change, the answer is not on the disk — it's the **direction**. Three diagnostic tells that the loop is an axis problem, not a capability problem:

    - **Tell A:** Arif volunteers a non-submission reason (e.g. "I don't want to die in PETRONAS", "I don't know what I want", "I don't do hobby stuff", "pening bila ada options") inside the same session. The submission is a **vehicle**, not the goal.
    - **Tell B:** Arif's "are we ready" phrasing shifts from deadline-driven ("can we make 1 August") to identity-driven ("what does winning mean to me at this conference"). The audit's question has moved under it.
    - **Tell C:** Arif pushes back on the recommendation not because it's wrong but because it doesn't name the underlying frame. E.g. "I only enter game I can win" + a recommendation he agrees with on paper + continued paralysis = the recommendation is right, the axis is missing.

    **Operational rule (new):** when axis-problem tells fire, do NOT escalate the audit (don't go to Shape C full artifact, don't add more tiers). Instead, **state the axis question explicitly** and **stop the audit until the human answers**. The question is one of:

    - "What do you want from [arifOS / this submission / this conference] in 24 months?"
    - "What would you lose by NOT doing this?"
    - "Demonstrator or narrator?" (i.e. ship a thing, or talk about shipping a thing)

    Each of these is a **frame-setting question** the audit cannot answer. The audit's job is to name that the question is missing, not to fill it in. Forcing the audit forward without the axis produces the "Pening bila ada options" paralysis and the "chicken-and-egg" loop.

    **Tactical pause point:** when an axis problem is detected, the audit's §1 TL;DR should be replaced with a single sentence of the form: *"The deadline is solvable. The axis is not. Ask the human: [one frame question]."* Then stop. The audit does not continue past this point until the human replies.

16. **Contamination reflex drift (validated 2026-07-03).** The `seven-zen-organs-enforcement` skill encodes a contamination case from earlier the same day. In a later session-block, **a second contamination of the same shape arrived and the agent answered it as Arif's question again**. The contamination class was: a long formatted block (100+ lines, APEX SWOT table style, academic register) inserted between Arif's short messages, with no clear "save this" instruction.

    **The fix is not "catch more contamination"** — it's that **the reflex arc itself is failing**. If the same contamination shape gets past the reflex twice in one session, the reflex has been overridden by a more attractive output mode (e.g. "this looks like a structured deliverable, I should answer it"). The operational correction: when a contamination is caught, **append it to the contamination-incident log AND restart the reflex arc explicitly** (e.g. re-load the seven-zen-organs skill, re-state "Reality: is this Arif's current message or a prior block?"). Don't trust the reflex to self-correct. Re-run it. See `seven-zen-organs-enforcement` §"The contamination case" + this pitfall for the joint lesson.


## Worked example (canonical)

The A2B IJCAI 2026 audit (2026-07-03, 29 days to deadline) is the canonical worked example. See `references/a2b-ijcai-2026-audit-2026-07-03.md` for the full 17.9 KB audit. Lessons:
1. Disk-verified inventory at §2
2. Tier 1 = 11 days, Tier 2 = 15 days, buffer = 3 days = 29 days
3. Option B recommended (Tier 1 + multi-step workflow demo)
4. Critical Unknown: IJCAI 2026 submission format (Tavily returned 402)
5. 3 chaos items named explicitly

## Reproduction recipe

```bash
# 1. Probe disk state
git -C /root/<repo> status -sb
find /root/<repo> -maxdepth 3 -type f -not -path '*/.git/*' | wc -l

# 2. Probe federation liveness
for p in 8088 8081 3001 7072 18082 18083; do
  curl -sf -o /dev/null -w "$p -> %{http_code}\n" http://localhost:$p/health
done

# 3. Read project tracker
cat /root/<repo>/docs/PROJECT_TRACKER.md 2>/dev/null

# 4. Pull eval results
ls /root/<repo>/evals/*/eval_aggregate.json 2>/dev/null

# 5. Probe external format (try once, then declare as critical unknown if Tavily 402)

# 6. (NEW 2026-07-03) Contradiction sweep — catch every disputed number across all artifacts
# Pick the 3-5 most-cited numerical claims from the submission. For each:
grep -rn '<disputed_string>' /root/<repo>/ /root/<repo>/docs/ /root/<repo>/reports/ 2>/dev/null
# Paper claims -278ms → grep returns 5 sites. Each one is a contradiction. List them all.

# 7. (NEW 2026-07-03) Git history pattern check — surface the abandonment risk
git -C /root/<repo> log --format='%ai | %an | %s' --since='90 days ago' 2>/dev/null
# Look for: 'session closure', 'seal', 'handoff', 'final', 'done' commits followed by silence

# 8. Write the audit following the 12-section structure + §13/§14/§15

# 9. End with the constitutional receipt + one-line kernel
```

## The 4 files this skill composes with

- `scientific-manuscript-forge` — for the artifact being audited (the manuscript / submission draft)
- `geox-federation-mcp-driver` — for the live federation probes + the EGS claim/evidence audit
- `institutional-epistemic-sink-forensics` — for the audit's "what's chaos" section
- `plan` — for the day-by-day action plan
- `seven-zen-organs-enforcement` — for the per-step Reality / Governance / Witness / Meaning checks

## Why this skill (vs. the existing `plan` skill)

`plan` writes a *forward* implementation plan from a clear spec. It assumes the work has not started.

`submission-readiness-audit` is the *reverse*: the work is partially done, the spec is the external deadline, and you need to know what's missing to bridge the gap. Different inputs, different output, different timing.

The A2B audit was the trigger. The 29-day deadline + Tier 1 = 11 days + Tier 2 = 15 days + 3 days buffer matched exactly — but only because the audit made the math explicit. Without the audit, the work would have been under-scoped and missed the deadline.

## One-line kernel

> An audit that doesn't name chaos is false confidence. An audit that doesn't tier the gap is wishful thinking. An audit that doesn't end with 3 options and a recommendation is incomplete. Audit = disk-verified inventory + tiered gap + named chaos + 3 options + critical unknown + day-by-day plan + constitutional receipt.

*DITEMPA BUKAN DIBERI — The audit is forged, not given.*

*Skill created 2026-07-03, Hermes agent, on F13 SOVEREIGN directive. Pattern validated by A2B IJCAI 2026 audit (29 days to deadline, Option B recommended). v1.1 (2026-07-03) adds §13 stake-diagnostic, §14 output-shape rules, §15 forced-stop pattern, pitfalls #13+#14, and the `references/arif-pattern-aware-auditing.md` companion. Trigger this skill when Arif asks "are we ready for X" — and read the companion reference to learn his operational pattern first.*