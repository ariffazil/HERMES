---
name: hospital-patient-advocacy
description: "Help users navigate Malaysian public hospital systems — interpret medical reports, translate clinical terms to plain BM, draft correspondence, and"
tags: [hospital, medical, malaysia, patient-advocacy, translation, hkl]
---

# Hospital Patient Advocacy (Malaysia)

When a user is dealing with a family member in a Malaysian public hospital (HKL, Hospital Selayang, etc.), this skill governs how to help: interpreting medical documents, explaining clinical terms in plain BM, drafting formal correspondence, and guiding through the hospital process.

## Triggers

- User shares medical reports, radiology forms, procedure notes
- Family member admitted / surgery / emergency
- User asks to interpret hospital documents or explain medical terms
- User asks to draft a letter/email to hospital administration
- User needs help with visitor policies, nurse arrangements, recovery planning

## Core Rules

### 1. Language: plain BM for explanations, English for clinical terms
- **Always explain in BM** unless the user explicitly switches to English. Default conversational BM ("kau", "mak kau", "diorang" — not textbook formal).
- Keep clinical terms in English (CBD, ERCP, WCC, eGFR) but translate the *meaning* into BM.
- When user corrects with "Bahasa melayu" — switch immediately, no questions.

### 2. Report interpretation workflow
When handed a medical document (CT report, EUS/procedure report, radiology form, blood results):
1. Extract and display the key findings in a structured format (organ → finding → status)
2. Highlight abnormalities (bold or emoji markers)
3. Translate medical implications to plain BM
4. Flag any discrepancies (name mismatch, missing fields, date conflicts)
5. Cross-reference with earlier reports to build a timeline

### 3. Correspondence drafting rules
When drafting a formal letter to hospital administration (Pengarah, Ketua Jabatan):
- **NEVER mention procedural details that imply blame** (e.g. "perforasi susulan prosedur endoskopi"). Frame around patient needs, not cause.
- Keep to 3 concise alasan (reasons). Make one about emotional support, one about medical decision-making, one about treatment planning.
- Include full patient identifiers: name, IC, current ward/unit.
- Include phone number for follow-up.
- Accept the visitor policy upfront — "Saya memahami polisi sedia ada dan bersedia mematuhi syarat tambahan."
- Tone: respectful but firm. Not desperate, not aggressive.

### 4. Post-surgery assessment questions
When user wants to assess a post-op patient, prioritise these 5:
| Priority | Question | Why |
|---|---|---|
| 1 | Apa surgeon jumpa? Procedure apa dibuat? | Root cause |
| 2 | WCC (white cell count) | Infection/sepsis detection |
| 3 | Vital signs (BP, pulse, temp, urine) | Stability |
| 4 | Ada biopsy? Result? | Malignancy screen |
| 5 | Comorbid? (DM, HTN, cardiac) | Complication risk multiplier |

### 5. Recovery phase guidance
After surgery, break guidance into phases:
- **HCU/ICU (24-48h):** Tubes/drains explained, NPO, monitoring targets
- **Wad (Day 3-7):** Mobilisation milestones, diet progression, wound care
- **Discharge (Day 7-10):** Questions to ask before leaving, warning signs to watch
- **Home (Week 2-6):** Activity progression by week, ER red flags

### 6. Visitor policy navigation
Malaysian govt hospitals restrict male visitors in female wards. Instead of fighting the policy:
- Approach: talk to Ketua Jururawat (Sister) directly — they hold the practical authority
- Frame: medical decision-making need, not social visit
- Ally: get treating doctor to support with a note
- Backup: formal letter to Pengarah (see rule 3)

### 7. Voice notes
When user is mobile/stressed/at hospital and needs assessment questions or guidance:
- Proactively offer voice via `edge-tts --voice ms-MY-OsmanNeural --rate "+5%"`
- Keep voice notes under 90 seconds
- Use conversational BM — "kau", "mak kau", not "anda/pesakit"

## Pitfalls

- **Never give a diagnosis.** Explain what reports mean, don't declare what the condition IS.
- **Don't over-reassure.** "Don't worry" is not useful. "Here's what the numbers mean and what happens next" IS useful.
- **Don't mention procedure details in formal letters.** The user corrected this — "kecuain waktu endos." Hospitals are defensive about complications.
- **Don't push the user to act.** Present options, let them decide. They're under stress.
- **Verify patient identity across documents.** Name mismatches (e.g. ROSLANAH vs ROSNANI) are common clerical errors in govt hospitals — flag them.
- **Distinguish symptom location carefully.** "Perut mengah" (perut rasa penuh/ketat/tegang) is completely different from "dada mengah" (sesak nafas/chest tightness). The first is ileus/distension, the second is respiratory. Don't conflate them. Confirm dengan user: "Perut ke dada?"
- **For post-procedure complication cases, DON'T DO THIS:** If the user starts expressing anger at the hospital ("bodo punya doc"), do NOT pile on with factual details that justify anger (e.g. "0.03% perforation rate, discharge symptomatic, 12h delay"). This escalates distress. Instead, acknowledge once briefly, redirect to the immediate concern (is the surgery done? is the patient stable?). Escalation/action comes later.

## Iatrogenic Injury Detection Workflow

Use this when a user shares a case where a complication may have occurred during/after a procedure.

### Timeline Reconstruction (first priority)

When user says "X happened, then discharge, then I brought back at 2AM" — reconstruct the formal timeline:

| Parameter | Why it matters |
|-----------|----------------|
| Procedure time + date | Establish baseline |
| Symptom onset time | Was it immediate or delayed? |
| Discharge time despite symptoms | Protocol violation evidence |
| Readmission time | Delay in diagnosis (key metric) |
| Diagnosis time | How many hours between readmission and action |
| Surgery/definitive care time | Time to theatre */

Use `table` format with emoji markers. Present to user for correction: "Timeline ni betul?" Then ask if they want to save it.

### Language Protocol for Complication Discussion

- **When user is in distress (waiting for surgery):** Do NOT discuss negligence, rights, or escalation. The only focus: procedure outcomes, recovery timeline, user self-care (hydrate, rest, eat).
- **When user starts expressing anger ("bodo punya doc"):** Acknowledge with ONE SHORT sentence. Redirect to current concern. Example: "Faham. Mak dah selamat? Operation selesai?"
- **When user is calm and situation stable (post-op, ward phase):** THEN offer the next-step options: request medical report, timeline documentation, complaint to hospital management, MMC complaint.
- **Do not offer escalation pathway unprompted mid-crisis.** Wait for user to ask "lepas ni apa boleh buat?" or similar.

### Documentation for Potential Negligence Case

When user indicates interest in escalation, help them gather:

1. **Full medical report** — request from hospital records office (name, IC, date of procedure)
2. **Timeline** — reconstruct from user's account. Key events with times.
3. **Procedure report** — any EUS, ERCP, endoscopy report
4. **Names** — treating doctor, procedure doctor, ward sister
5. **Agency referral** — Majlis Perubatan Malaysia (MMC) for doctor complaint, or tribunal for consumer claim

Do NOT instruct user to take legal action. Say "simpan semua dokumen. Lepas ni boleh fikir langkah seterusnya."

## Common Malaysian Hospital Context

- Government hospital costs: RM1 outpatient registration, heavily subsidised inpatient
- Private duty nurse in ward: see `references/malaysia-nursing-rates-2026.md` for verified 2026 KL rates, contact numbers, and home nursing visit pricing
- Visitor hours: typically 12:30-14:00 and 16:30-19:00 (confirm at ward)
- HCU has stricter limits than general ward — usually 1-2 visitors, 30 min slots
- ERCP perforation rate: 0.3-0.6% vs gastroscopy: 0.03%
- Common abbreviations: CBD (Common Bile Duct), WCC (White Cell Count), eGFR (kidney function), EUS (Endoscopic Ultrasound), MRCP (MRI bile duct), HCU (High Care Unit), NPO (Nil By Mouth / puasa)

### Distinguishing endoscopic procedures (avoid confusion)

Patients often say "endoscopy" generically, but post-op management differs significantly:

| Procedure | What it does | Perforation risk |
|---|---|---|
| **Gastroscopy** (OGDS) | Scope into esophagus, stomach, duodenum — visual only | 0.03% (1/10,000) |
| **EUS** (Endoscopic Ultrasound) | Gastroscopy + ultrasound probe — images CBD, pancreas, lymph nodes | 0.03-0.1% |
| **ERCP** | Scope to duodenum + wire into bile/pancreatic duct + contrast + X-ray + possible sphincterotomy/stone extraction | 0.3-0.6% (1/200-300) |

**Always cross-reference the actual procedure report** (not just what the patient/family says) to determine which procedure was done. EUS is diagnostic-only (no duct entry), ERCP is therapeutic (enters the duct system). The perforation risk and post-op management differ significantly.

## Private Hospital Cost Benchmarking

When a user shares costs from a private hospital visit, provide a market-rate comparison scale. See `references/private-hospital-costs-malaysia.md` for procedure-specific ranges.

### Tier System (KL/Selangor)

| Tier | Example | Markup vs market |
|---|---|---|
| 🟢 **Klinik biasa** | Klinik swasta kecil | 1x (baseline) |
| 🟡 **Hospital panel sederhana** | KPJ, Pantai, Thomson, Assunta | 1-1.5x |
| 🟠 **Hospital panel utama** | Sunway, Gleneagles | 1.5-2.5x |
| 🔴 **Premium corporate anchor** | Prince Court | 2-4x |

### The Prince Court / PETRONAS Effect

PETRONAS staff have unlimited inpatient coverage through their corporate plan. Prince Court, adjacent to the Twin Towers, is the primary beneficiary — prices inflated 2-4x above market because PETRONAS insurance pays without negotiation, creating a **price anchor** that pulls up rates at other KL private hospitals. Non-PETRONAS patients get charged the same inflated rates. Impact: same procedure at Prince Court can be 2-3x the cost of KPJ or Pantai.

**When a PETRONAS employee shares Prince Court costs:** acknowledge the premium, but focus on clinical outcome — the cost burden falls on the insurer.

### Cost Benchmarking Workflow

When user shares a procedure cost: (1) research market rate (2) build tier table (3) estimate markup (4) layer in insurance coverage — outpatient (limited annual cap RM10k) vs inpatient (unlimited corporate).

### ESWT (Shockwave Therapy) Recognition

ESWT / Li-ESWT in urology is used for **Chronic Prostatitis/CPPS** (reduce inflammation, 4-6 sessions, 10-15 min), **Peyronie's disease** (break plaque, 4-6 sessions, 10-15 min), or **Vasculogenic ED** (angiogenesis, 6+ sessions, 15-20 min).

**If a doctor performs ESWT:** the original referral diagnosis may differ. ESWT is NOT for bladder obstruction or urachal cyst — it implies an **inflammatory** or **vascular** diagnosis. Flag the diagnostic shift, don't diagnose.

## Insurance Coverage Analysis

When user shares an insurance screenshot or referral letter:

### Layer Identification

| Layer | What it covers | Typical limit (PETRONAS AIA) |
|---|---|---|
| **Outpatient (Specialist Care)** | Consultation, diagnostic scans, medication | RM 10,000/year (shared) |
| **Inpatient (Hospitalization)** | Admission, surgery, ward stay, theatre | Unlimited or very high limit |

### GL Process

Referral letter valid 30 days → call insurer verify eligibility + get GL → present GL at admission → hospital bills insurer cashless. For multi-session therapy (e.g. 6x ESWT), confirm billing category.

## Cross-Session Case Tracking

For a person tracked across multiple medical sessions, maintain a timeline:

| Date | Event | Tag |
|---|---|---|
| YYYY-MM-DD | Initial complaint | OBS |
| YYYY-MM-DD | Referral issued | OBS |
| YYYY-MM-DD | Insurance confirmed | DER |
| YYYY-MM-DD | Consultation | OBS |
| YYYY-MM-DD | Procedure | OBS |
| YYYY-MM-DD | Outcome | OBS |

### Diagnosis Shift Detection

When later sessions reveal new info contradicting earlier docs: flag the contradiction explicitly, explain what the new procedure implies about actual diagnosis, let the user/patient confirm. Example: Referral says "urachal cyst" → Doctor does shockwave → Shockwave is for inflammation → Likely diagnosis shifted to prostatitis/CPPS.
