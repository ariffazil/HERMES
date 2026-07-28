# Medical Tourism Agentic Surface — Domain Reference

> From session 2026-07-27: Built IZZU Medical Tourism demo under WELL organ.
> Live at: https://well.arif-fazil.com/tourism/

## Domain Invariants (Static Data)

Hospitals need:
- Identity: name, short_name, location (city, state, lat, lng, airport distance)
- Accreditations: JCI, MSQH, ACHS, Temos (list)
- Beds count, international desk flag
- Languages spoken (list — critical for agent matching)
- Specialties with level tags: centre_of_excellence / specialist
- Doctors: name, specialty, experience_years, qualifications, languages
- Pricing: consultation range, procedure pricing with [min,max] in MYR, stay_days
- Outcomes: patient_satisfaction_pct, infection_rate, readmission_rate, procedure-specific success rates
- Rating: overall (1-5), review count

Price benchmarks vs US/UK/Australia (savings percentage) for key procedures.

## Organ Domain: WELL

Medical tourism belongs under WELL (not GEOX, not WEALTH) because:
- WELL handles human readiness, dignity, recovery suitability
- WELL is REFLECT_ONLY — never decides for the patient
- F6 MARUAH protects against misleading claims
- WEALTH handles pricing comparison (bridge)
- A-FORGE handles booking (execution after verdict)

WELL tools to wire:
- `well_guard_dignity` — ethical recommendation check
- `well_assess_homeostasis` — patient readiness check
- `well_validate_vitality` — recovery suitability
- `well_assess_reliability` — hospital verification

## MHTC Red Team Findings (Competitor)

MHTC (malaysiahealthcare.org) weaknesses:
1. **React SPA** — curl returns ~300 chars marketing fluff, zero hospital data
2. **No llms.txt, agent.json, or machine-readable data** — agents completely blind
3. **No pricing transparency** — forms/phone calls required to see costs
4. **Find Hospital filter is JS-only** — redirects to blank page without JavaScript
5. **No doctor profiles** — no way to search by practitioner
6. **Generic marketing copy repeated everywhere** — zero structured comparison data
7. **No outcomes data published** — claims success rates but shows no numbers
8. **No personalization** — same experience for every condition

Strengths to preserve:
- Patient journey flow (Pre-Treatment → Visa → Treatment → Recovery)
- Special Lane immigration facilitation
- Centres of Excellence branding
- Accreditation emphasis (JCI, MSQH)
- Recovery tourism angle

## Data Packing Pattern

One `database.json` file with all entities, linked by ID. Entities:
- `hospitals[]` — full hospital objects with nested doctors[], pricing{}, outcomes{}
- `treatment_categories[]` — grouping procedures by specialty
- `price_benchmarks{}` — savings vs US/UK/AU per procedure
- `meta.agent_discovery{}` — pointers to llms.txt, MCP, agent.json

## AI Recommendation Format

When agents make recommendations, they should output:
```
For [condition], I recommend [Hospital]:
• Doctor: [Name], [X]yr, [qualifications]
• Cost: MYR [min]-[max] (~USD [min]-[max])
• Stay: [X] days treatment + recovery
• Reason: 1-2 sentence match rationale
• Savings: ~[X]% vs [home country]
• Languages: [spoken]
```

## 5 Hospital Quick Guide (from demo)

| Hospital | Best For | Price Tier | Satisfaction |
|---|---|---|---|
| Penang Adventist | Budget, ortho, cardio | Value ★★★ | 94.2% |
| Gleneagles Penang | Premium Penang, cardio | Mid ★★ | 93.8% |
| Prince Court KL | Luxury, oncology, fertility | Premium ★ | 95.1% |
| Sunway Medical | Largest, cancer, neuro | Mid ★★ | 94.5% |
| Pantai KL | Budget KL, dental | Value ★★★ | 92.8% |
