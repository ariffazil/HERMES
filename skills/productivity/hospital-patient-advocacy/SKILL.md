---
name: hospital-patient-advocacy
description: "Help users navigate Malaysian public hospital systems — interpret medical reports, translate clinical terms to plain BM, draft correspondence, and guide family through admissions/surgery/recovery."
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
