# <SUBMISSION NAME> — Submission Readiness Audit

**Date:** YYYY-MM-DD
**Author:** arifOS Federation · <ORGANS> bridge
**Deadline:** YYYY-MM-DD (**<N> days remaining**)
**Scope:** <what is being submitted, to whom, in what format>
**Markers:** `[OBS]` disk-verified · `[DER]` derived · `[INT]` interpreted · `[U]` unknown

---

## TL;DR — Verdict First

<One paragraph: are we ready, why, what's the single biggest risk, what's the recommendation>

---

## 1. What You Have (Current State — Disk-Verified)

### 1.1 Repo `<repo-name>` (path)

```
<output of find . -maxdepth 3 -type f -not -path '*/.git/*'>
```

### 1.2 <Eval/Run/Submission> Results (Disk-Verified Numbers)

| Item | Value | Marker |
|---|---|---|
| <metric> | <value> | `[OBS]` |

### 1.3 Federation / System Status (live, all healthy)

| Component | Port/Path | Health |
|---|---|---|
| <name> | <port> | ✅ |

### 1.4 Submission Draft Status

<Paragraph: sections 1-N, line count, what's written, what's draft>

---

## 2. What's Missing

### 2.1 Tier 1 — MUST DO (<N> days)

| # | Item | Effort | Why |
|---|---|---|---|
| T1.1 | <item> | N days | <reason> |

### 2.2 Tier 2 — SHOULD DO (<N> days)

| # | Item | Effort | Why |
|---|---|---|---|
| T2.1 | <item> | N days | <reason> |

### 2.3 Tier 3 — NICE TO HAVE (weeks)

| # | Item | Effort |
|---|---|---|
| T3.1 | <item> | N weeks |

---

## 3. What's Chaos (Misalignments + Risks)

### 3.1 <Submission> Claims vs Disk Reality

| Claim | Disk Reality | Verdict |
|---|---|---|
| <claim> | <disk> | VERIFIED / NEEDS RECOMPUTE / UNVERIFIABLE |

### 3.2 Architectural Misalignments

<Bullets>

### 3.3 Tooling Drift

<Bullets>

---

## 4. What's Needed — Concrete List

### 4.1 For <DEADLINE> Submission (Hard Deadline)

<Tier 1 + critical Tier 2 from §2, with effort and first move>

### 4.2 Honest Time Budget

| | Days |
|---|---|
| Tier 1 | <N> |
| Tier 2 | <N> |
| Buffer | <N> |
| Total needed | <N> |
| Remaining | <N> |

**Verdict:** <doable if you start now / tight / not realistic>

---

## 5. The Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk> | L/M/H | L/M/H | <mitigation> |

---

## 6. Recommended Path — 3 Options

### Option A — <approach 1>
- **What it is:** <description>
- **Pros:** <list>
- **Cons:** <list>
- **Probability of acceptance:** <X%>

### Option B — <approach 2>
- **What it is:** <description>
- **Pros:** <list>
- **Cons:** <list>
- **Probability of acceptance:** <X%>

### Option C — <approach 3>
- **What it is:** <description>
- **Pros:** <list>
- **Cons:** <list>
- **Probability of acceptance:** <X%>

### My recommendation

**[INT] Option <X>.** <one paragraph justifying the pick>

---

## 7. The Critical Unknown — <UNVERIFIABLE THING>

**[U] I cannot verify <X> from this environment.** <Why> You must confirm:

1. <item>
2. <item>

**Action T<N>:** <specific action with time budget>

---

## 8. The Federated Action Plan

| Day | Action | Owner | Why |
|---|---|---|---|
| 1 | <action> | <Arif/FORGE> | <reason> |

---

## 9. What's Chaos — Call It Out

**[INT] <N> things are chaos right now:**

1. <item>
2. <item>
3. <item>

---

## 10. Constitutional Receipt

```
file:        <path>
author:      arifOS Federation (<organs> synthesis)
verdict:     <GREEN/YELLOW/RED> — <one-line summary>
deadline:    <date> (<N> days)
tier_1_effort: <N> days
tier_2_effort: <N> days
buffer:      <N> days
critical_unknown: <list>
push:        <LOCAL ONLY / READY / PENDING ARIF>
```

---

*DITEMPA BUKAN DIBERI — The audit is forged, not given.*

**One-line kernel:** <one falsifiable, actionable sentence>.

---

## Section-by-section guide

| Section | What goes here | Length |
|---|---|---|
| TL;DR | Verdict, biggest risk, recommendation. One paragraph max. | 5-10 lines |
| 1. What You Have | Disk-verified inventory. Every entry has a path or `wc -l` or `find` receipt. | 50-80 lines |
| 2. What's Missing | Tier 1/2/3 categorization. Each item has effort estimate and first move. | 30-50 lines |
| 3. What's Chaos | Three sub-sections: claims-vs-disk, architectural, tooling. | 20-40 lines |
| 4. What's Needed | Concrete list with Tier 1 + critical Tier 2, plus honest time budget. | 20-30 lines |
| 5. Risk Matrix | Table of risks with likelihood, impact, mitigation. | 10-20 lines |
| 6. 3 Options | Three options with all 4 columns filled (What/Pros/Cons/Probability). | 30-50 lines |
| 7. Critical Unknown | The agent's honesty boundary — what it cannot verify. | 5-15 lines |
| 8. Action Plan | Day-by-day plan with owner and why. | 15-30 lines |
| 9. What's Chaos | The most important section. Names the unresolved chaos. | 10-20 lines |
| 10. Receipt | Fixed-shape block with the audit's metadata. | 8-12 lines |
| One-line kernel | One falsifiable, actionable sentence at the very end. | 1 line |

**Total length:** 200-350 lines, 10-20 KB.