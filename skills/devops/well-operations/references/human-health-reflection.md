# Human Health Reflection via WELL — Usage Pattern

> **WELL is REFLECT_ONLY. Never diagnose. Never adjudicate.**  
> This pattern uses WELL's MCP tools as a reflective mirror for human health situations — it does NOT produce clinical diagnoses.

## Trigger

- User shares medical documents (referral letters, reports, images)
- User asks to analyze a human health situation via the federation
- User specifically mentions WELL or asks "analyze through WELL"

## Pre-Check: Source the Session

```bash
set -a && source /root/.secrets/vault.env && set +a
# Verify env is loaded
```

## Step 1 — Read Medical Documents

Use `vision_analyze` to transcribe every field from document images. Look for:
- Patient name, IC, MRN
- Referring doctor, hospital
- Diagnosis text (handwritten — ask vision to read carefully)
- Referral specialist and hospital
- Date of referral (check validity — AIA referrals expire in 30 days)
- Insurance/employer details

**Cross-reference multiple documents** — same patient? different dates? different conditions? Flag discrepancies immediately.

### Handwriting Pitfall
Vision models often misread doctor's handwriting. The first reading is NOT reliable — always verify against anatomy and context. Common errors:
- `4/4` (grading scale) misread as `uL`, `RL`, `LL`, or `u/c`
- `Obstructive Bladder` misread as `Ovarian Bladder` — especially on male patients
- `Urachal Bladder [cyst]` misread as `Ovarian Bladder` or `Ovarian Cyst` — another common path when the word starts with "Ura-" 
- `Treatment` misread as `Monitory`, `Menty`, or `Monitoring`
- `h/o` (history of) misread as `u/s` (ultrasound) — the "h" ascender looks like a "u" to vision models
- If a reading contradicts basic anatomy (e.g. "Ovarian" on a male patient), **re-run vision_analyze** with explicit letter-by-letter instruction. Do not just flag it — actively re-read with the correct anatomy as context.

---

## Step 2 — WELL 4-Tool Parallel Probe

Run these four WELL tools in parallel (they're independent):

### Tool 1: `well_classify_substrate`
```
mode: "classification"
subject: "<patient-name> — <condition>"
description: "<full context from documents>"
evaluation_intent: "assess human readiness and vitality context for <treatment-pathway>"
```

**What you learn:** Substrate class (MACHINE_SYSTEM, HUMAN_BODY, etc.), cultural metadata, medical boundary trigger status.

### Tool 2: `well_assess_homeostasis`
```
mode: "sleep" (or appropriate)
subject: "<patient-name> — <condition>"
decision_class: "C3"
```

**What you learn:** Sleep recovery status, fatigue, stress load, HOLD/DEGRADED signal, telemetry availability.

### Tool 3: `well_validate_vitality`
```
mode: "readiness"
intent: "<treatment-intent>"
reversibility: "reversible" (or as appropriate)
decision_class: "C3"
```

**What you learn:** Vitality gate verdict (REDUCE_LOAD / PROCEED / HOLD), weakest substrate, H_WELL / M_WELL / G_WELL breakdown, biometric snapshot.

### Tool 4: `well_check_repair`
```
mode: "precheck"
task_description: "<full treatment description>"
decision_class: "C3"
```

**What you learn:** Forge readiness, reversibility, risk level, execution recommendation (draft_only / proceed), receipt hash.

---

## Step 3 — Synthesize Into a Table

Present results as a compact table:

| Tool | Verdict | Signal | Confidence |
|---|---|---|---|
| **substrate_classify** | `MACHINE_SYSTEM` | ADVISORY | Medium |
| **homeostasis** | `DEGRADED` | HOLD | LOW |
| **validate_vitality** | `YELLOW (57%)` | REDUCE_LOAD | Medium |
| **check_repair** | `DEGRADED` | HOLD | LOW |

Then write a short synthesis paragraph:

**What WELL says clearly** — the signal it can produce
**What WELL needs** — missing evidence (biometric telemetry, self-report data)
**Boundary notice** — re-state "Not diagnosis. Not therapy. Reflective only. Arif remains final judge."

---

## Step 4 — WELL Cannot Assess Without Telemetry

When WELL returns DEGRADED/HOLD (which it will for any human it has no biometric data on), **do not stop there**. The output still provides:
- Substrate classification (is WELL oriented to this kind of input?)
- Vitality gate verdict (REDUCE_LOAD is a meaningful signal even without patient data)
- Machine/system health vs human data gap distinction

**Key insight:** WELL was designed for the federation operator (Arif), not arbitrary third parties. When assessing someone else, WELL will lack telemetry. This is expected — not a failure.

---

## Step 5 — Fill the Biometric Gap: 3 Structured Questions

After WELL analysis with insufficient telemetry, propose exactly 3 questions for the human to ask the patient:

| # | Domain | Question | Why |
|---|---|---|---|
| 1 | **Symptoms & severity** | Pain? Bleeding? When did it start? | Establish urgency and clinical context |
| 2 | **Sleep & fatigue** | Sleep quality? Interrupted? | WELL's strongest signal is sleep/fatigue; fill this gap |
| 3 | **Logistics & support** | Appointment booked? Insurance confirmed? Transport/companion? | Prevent logistical blockers from delaying care |

Each question needs a **WHY column** — the human needs to understand what you're fishing for, not just the question.

---

## Step 6 — Human Read + Reframe

When the human (Arif) relays the patient's answers, re-synthesize:

```
Old picture (from documents only): [summarize]
New picture (after patient input): [revise]
```

If the patient's symptoms don't match the referral diagnosis, flag it:
- Referral says "obstructive bladder" but patient reports left-sided abdominal pain → note the discrepancy
- Don't contradict the referring doctor — frame as "this may need urology investigation to clarify"

---

## Pitfalls

- **WELL cannot diagnose.** Never write "WELL found X condition" — it's reflective only. Always include the boundary notice.
- **Vision misreads handwriting — actively re-read, don't just flag.** Cross-reference multiple image analyses. If a term makes no anatomical/physiological sense (e.g. "Ovarian" on a male), re-run vision_analyze with letter-by-letter instruction and anatomy context. The correct reading could be "Obstructive Bladder" OR "Urachal Bladder [cyst]" depending on the actual letter strokes — don't assume either without re-verification.
- **"Ovarian Bladder" is not a real medical term.** The vision model hallucinated this from poor handwriting. Possible corrections: "Obstructive Bladder" (4/4 grading for severity) OR "Urachal Bladder [cyst]" (congenital remnant near bladder dome). Determine which by re-examining stroke count and letter shapes.
- **Document dates matter.** AIA referrals expire in 30 days. Multiple documents may span years. Always cross-reference dates.
- **"Ovarian Bladder" is not a real medical term.** The vision model hallucinated this from poor handwriting. The correct reading is almost certainly "Obstructive Bladder" (4/4 grading for severity).
- **WELL's machine_state.json is not the same as human health.** Fresh machine metrics (CPU, RAM) don't mean WELL has usable human data. Check state.json source_type and truth_status separately.
- **Don't over-interpret WELL output.** DEGRADED + HOLD is the normal response when WELL has no biometric data for the subject. This is not a system failure — it's a data gap.
