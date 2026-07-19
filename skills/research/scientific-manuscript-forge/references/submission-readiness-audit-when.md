# When to invoke `submission-readiness-audit` vs `scientific-manuscript-forge`

**Use this decision tree** when the user (or the agent) faces a deadline-driven submission with an existing work-in-progress.

---

## The two skills, side by side

| Dimension | `scientific-manuscript-forge` | `submission-readiness-audit` |
|---|---|---|
| **Direction** | Forward — produce the artifact | Reverse — audit the gap to the deadline |
| **Input** | Falsifiable scientific claim + data + named rival hypotheses | Existing work-in-progress + hard external deadline |
| **Output** | PDF + figures + GEOX claim | 10-section audit + Tier 1/2/3 + 3 options + day-by-day plan |
| **Stage** | Pre-submission artifact creation | Pre-submission gap analysis |
| **Length** | ~14-20 pages, 1.5 MB PDF | ~200-350 lines, 10-20 KB markdown |
| **Time budget** | Days to weeks of forge work | Hours of audit work |
| **Handoff** | Output goes to the audit (or to a submission portal directly) | Output goes to the day-by-day forge work, then back to scientific-manuscript-forge for the artifact |

## The decision tree

```
START
  │
  ├── Is there a hard external deadline (conference, journal, internal review)?
  │     │
  │     ├── NO  → use `plan` (forward implementation plan) or `scientific-manuscript-forge`
  │     │
  │     └── YES → Is the work already partially done?
  │               │
  │               ├── NO  → use `plan` to scope, then `scientific-manuscript-forge` to execute
  │               │
  │               └── YES → Is the deadline realistic (enough time for Tier 1 + 2)?
  │                         │
  │                         ├── UNKNOWN → use `submission-readiness-audit` first
  │                         │
  │                         └── KNOWN REALISTIC → use `scientific-manuscript-forge` directly
  │                         │
  │                         └── KNOWN UNREALISTIC → use `submission-readiness-audit` first,
  │                                                   recommend Option C (defer) honestly
```

## When to use both (in sequence)

**Pattern: audit first, then forge.**

1. **Audit pass** (use `submission-readiness-audit`)
   - Output: 10-section audit with Tier 1/2/3 + 3 options + day-by-day plan
   - Time: hours
   - Verdict: YELLOW band typical (not GREEN, not RED)

2. **Forge pass** (use `scientific-manuscript-forge`)
   - Input: the audit's Tier 1 + critical Tier 2 + the day-by-day plan
   - Output: the artifact (PDF + figures + GEOX claim)
   - Time: days to weeks
   - Verdict: SEAL (when rival-named, falsification-disciplined, evidence-ledgered)

3. **Re-audit** (optional, use `submission-readiness-audit` again)
   - Verifies the disk now matches the submission claims
   - Catches any new gaps introduced by the forge work

## When to skip the audit and go straight to forge

- The deadline is far away (>3 months) and the work is well-scoped
- The submission is a single-artifact deliverable (not a multi-section manuscript)
- The Tier 1/2/3 are obvious from the project tracker alone
- The user explicitly says "just forge it" or "no need for the audit"

## When to skip the forge and go straight to audit

- The deadline is tight (<4 weeks) and the work is multi-organ
- The user is asking "are we ready?" or "what's missing?"
- The submission claims in the draft need verification against the disk
- The institutional or political risk of the submission is high (career, governance, sovereignty)

## Worked example (A2B IJCAI 2026, 2026-07-03)

1. **User asks:** "are we ready for 1 August? what's needed?"
2. **Skill:** `submission-readiness-audit`
3. **Output:** 17.9 KB audit, YELLOW band, Option B recommended (Tier 1 + T2.4 multi-step demo)
4. **Next step (if user says "Option B, start now"):** `scientific-manuscript-forge` for the strengthened manuscript + new GEOX claim + new evidence ledger
5. **Final step:** re-audit to verify the disk now matches the strengthened submission

## Anti-patterns

### Anti-pattern 1: Forge without audit
Symptom: agent dives into Tier 2 work before verifying Tier 1 is complete. Wasted effort on a Tier 2 feature that masks a Tier 1 integrity hole (e.g. adding a multi-step demo when SEAL flow isn't proven).

Fix: always audit first when the deadline is tight.

### Anti-pattern 2: Audit without forge
Symptom: agent produces a beautiful audit but never starts the actual work. Audit becomes a procrastination artifact.

Fix: the audit's day-by-day plan must be actionable on day 1. If the plan is too vague, the audit isn't useful.

### Anti-pattern 3: Audit in place of forge
Symptom: agent re-audits multiple times instead of forging. Each audit finds new gaps; the gap analysis becomes the work.

Fix: cap at 2 audit passes (initial + post-forge). After 2, force a forge step.

### Anti-pattern 4: Forge in place of audit
Symptom: agent forges without checking the deadline, runs out of time, ships a half-finished artifact.

Fix: the audit's day-by-day plan has a hard stop date. After that date, no more forge work — ship what exists or defer.

## Cross-reference

- `submission-readiness-audit/SKILL.md` — full audit skill
- `submission-readiness-audit/references/a2b-ijcai-2026-audit-2026-07-03.md` — canonical worked example
- `scientific-manuscript-forge/SKILL.md` — full forge skill
- `plan/SKILL.md` — for forward plans (no deadline pressure)

---

*DITEMPA BUKAN DIBERI — Audit, then forge. Or just forge. Never audit forever.*