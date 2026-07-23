---
name: medical-document-interpretation
description: Interpret Malaysian medical documents (CT reports, radiology forms, procedure reports, blood results) and explain them in simple Bahasa Melayu. Covers common tests, terminology, hospital logistics, and post-surgery recovery guidance.
tags: [medical, malaysia, hospital, report, radiology, surgery, bm]
---

# Medical Document Interpretation (Malaysia)

Interpret Malaysian medical documents for layperson understanding. Convert clinical jargon to plain Bahasa Melayu. Support hospital logistics (HKL, government/private) and post-surgery recovery planning.

## Trigger Conditions

- User shares medical document images (CT reports, radiology forms, procedure reports, blood results, discharge summaries)
- User asks "apa maksud ni", "explain", "translate"
- User discusses hospital procedures, surgery, recovery timelines
- User needs private nurse rates, hospital logistics in KL
- **Chat-fragment reconstruction**: User describes a medical situation via DMs or chat fragments with no document image — reconstruct the full clinical narrative from raw gateway logs when session_search returns empty (see `references/forwardable-recap-template.md` for the standard output format)

## Workflow

### 1. Read the Document

Use vision_analyze to extract all text from the document image. Request complete transcription — every field, every handwritten note.

### 2. Extract Key Findings

Identify and list:
- Patient demographics (name, age, IC)
- Procedure type and date
- Clinical indication (why was it done)
- Key findings (measurements, abnormalities)
- Diagnosis / conclusion
- Recommendation / management plan

### 3. Spot Discrepancies

Cross-reference documents when multiple are shared:
- Name mismatches (common clerical error in government hospitals)
- Date inconsistencies
- Conflicting findings between reports

Flag these to user immediately.

### 4. Explain in BM

For each finding:
- State what was found (in English, exact from report)
- Translate to simple BM analogy
- Answer "kenapa penting" — clinical significance

### 5. Build Timeline

When multiple documents span different dates, construct a chronological timeline to show disease progression.

### 6. Recovery & Logistics

After surgery/procedure, provide:
- Phase-by-phase recovery milestones (ICU/HCU → ward → discharge → home)
- What to ask doctors at each stage
- Warning signs requiring ER visit
- Private nurse rates (KL government hospitals: RM 120-250 per 12hr shift)

### 7. Caregiver Dossier (Full Output Mode)

When the user asks for a full recap, dossier, or "tell me everything" about a hospitalized family member, shift from document interpretation to full caregiver support. Produce a structured 9-section dossier:

1. Cover — patient name, status badge, critical warnings (e.g. name errors)
2. Timeline — chronological evidence table with status column
3. Status Semasa — vital indicators + unknowns flagged
4. Recovery Roadmap — 4 phases: HCU/ICU → Ward → Discharge → Home
5. Soalan Doktor — numbered checklist with "kenapa penting" column
6. Tanda Bahaya — ER warning signs, 7-8 minimum
7. Caregiver Survival — self-care mandate: makan, tidur, workout, delegate
8. Underlying Issues — non-emergency findings for follow-up
9. Hospital Logistics — nurse rates, parking, visiting hours

For PDF: use `scientific-pdf-generation` Mode B (dark/gold dossier theme). For text: inline the structure. Language: user's preferred tone (BM casual / formal / English).

→ Pattern reference: `references/caregiver-support-dossier.md`

## Common Malaysian Medical Terms

| Term | BM Simple |
|---|---|
| CBD dilated | Salur hempedu bengkak |
| ERCP | Scope masuk salur hempedu |
| Perforation | Tebuk/ bocor |
| Free air under diaphragm | Udara bocor dalam perut |
| EUS | Ultrasound dari dalam (endoskopik) |
| MRCP | MRI salur hempedu |
| Ampulla of Vater | Lubang kecik tempat hempedu masuk usus |
| Choledocholithiasis | Batu dalam salur hempedu |
| Sphincter of Oddi | Otot valve kat hujung salur hempedu |
| CEA | Penanda tumor (kanser usus) |
| eGFR | Fungsi buah pinggang |
| WCC | Sel darah putih (tanda jangkitan) |
| NPO / puasa | Tak boleh makan minum |
| NG tube | Tiub hidung ke perut |
| HCU | High Care Unit — antara ICU dan wad biasa |
| ASA score | Skor risiko sebelum bius (1-5) |

## Hospital Logistics (KL Government)

- HKL HCU: high monitoring, limited visitors (30 min slots, 1-2 ppl)
- HKL Wad Biasa: visit hours more flexible, 1 nurse per 10-15 patients
- Private duty nurse in government ward: RM 120-250 per 12hr shift
- Nurse agencies: Private Nurses Caregivers 011-6196-3941, HomeCareApps
- IC/name errors on reports: common clerical issue, flag to doctor for correction

## Post-Surgery Recovery Phases

### ICU/HCU (24-48 hours)
- NPO, IV drip, NG tube, abdominal drain, catheter
- Monitor: vitals, urine output, drain output
- Goal: stable vitals, no fever, pain controlled

### Ward (Day 3-7)
- NG tube removal (when bowel sounds return)
- Start clear fluids → soft diet
- Mobilisation: sit → stand → walk (critical for preventing DVT/pneumonia)
- Drain removal, catheter removal

### Discharge (Day 7-10)
Questions to ask before leaving:
- Wound care instructions
- Antibiotics duration
- Diet restrictions
- Activity restrictions (lifting, driving)
- Warning signs requiring ER
- Follow-up appointment date
- Biopsy results if taken

### Home Recovery (Week 2-6)
- Week 1-2: rest, walk indoors, soft diet, no lifting >2kg
- Week 3-4: light activity, near-normal diet
- Week 5-6: mostly normal, still no heavy lifting

### ⚠️ Rush to ER
- Fever >38°C
- Wound red/swollen/oozing/opening
- Severe abdominal pain
- Persistent vomiting
- Jaundice (yellow eyes/skin)
- No bowel movement >3-4 days

## Epistemic Labels

Medical interpretation is inherently uncertain:
- Tag findings from reports as OBS (observed from document)
- Tag explanations as DER (derived from medical knowledge)
- Tag recovery timelines as EST (estimate — individual variation)
- Never claim diagnostic authority — always frame as interpretation aid

## Reference Files

- `references/hkl-logistics.md` — HKL-specific: ward types, private nurse rates, visitor policies, patient belongings checklist
- `references/forwardable-recap-template.md` — Standard output format for forwardable medical recaps: timeline table, status dashboard, recovery roadmap, doctor question checklist, ER warning signs, and personal encouragement section. Use this template when compiling a medical summary meant to be forwarded directly to a patient's family member.
- `references/caregiver-support-dossier.md` — 9-section dossier pattern for hospitalized family support: cover, timeline, status, recovery roadmap, doctor questions, danger signs, caregiver survival, underlying issues, hospital logistics. Evidence-first, action-oriented, tone-matched to user.

## Pitfalls

- **Name discrepancies — cross-reference memory**: Government hospital clerical errors are common. A hospital document bearing one patient name may actually belong to a different patient. When you have multiple names in persistent memory (e.g. an older profile entry says "SEGARAN" while a recent DM says "Ngenan"), the document in question could be misattributed. Cross-reference ALL names against IC number and against what the patient/family told you in the conversation. A document with the WRONG patient name is a critical safety issue — flag it immediately, not quietly. This session's case: Syed received a hospital letter bearing "ROSNANI" (Arif's mother), not his own mother Ngenan.
- **CT limitations**: Cholesterol gallstones are radiolucent — "no stone on CT" does NOT mean no stone
- **EUS is sensitive but not perfect**: Normal EUS doesn't 100% rule out ampullary pathology
- **Never over-promise timelines**: Recovery varies by age, comorbidities, and complication presence
- **Don't contradict treating doctor**: Frame as "ini cara nak faham apa doctor cakap", not as alternative medical advice
- **Separate acute emergency from underlying condition**: When a patient has both an acute surgical emergency (e.g. perforation) AND a chronic finding (e.g. dilated CBD 6mm), label them clearly as separate tracks. The acute issue takes priority now; the chronic issue is "follow-up after recovery." Don't conflate them.
- **Two-surgery distinction**: When family asks "nak operation lagi ke?" explain: Op 1 was emergency (already done), Op 2 is planned elective (for underlying issue). "Ni dua operation, dua sebab berbeza. Bukan komplikasi baru."
- **Hospital transfer miscommunication — FATAL risk (proven 2026-07-23)**: when patient transfers between hospitals, medical record errors kill. Name mixups common. Three mandatory steps: (1) get discharge summary & operation notes, fotostat, save in phone. (2) sit with admitting doctor, give FULL chronology, do not trust records to arrive. (3) check name/IC/MRN on every new document — if wrong, STOP until corrected.
