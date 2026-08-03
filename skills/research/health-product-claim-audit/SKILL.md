---
name: health-product-claim-audit
description: "Evaluate health product claims against clinical evidence — supplements, treatments, devices. Structured verdict: what is legit, what is marketing, what is overpriced. Context-aware recommendation considering who is asking."
tags: [health, product, supplement, evidence, audit, malaysia, claim]
---

# Health Product Claim Audit

Evaluate health product claims against clinical evidence. Deliver structured verdict: what is legit, what is marketing, what is overpriced. Context-aware recommendation considering the specific person asking.

## Trigger Conditions

- User asks "bagus x beli ni" about a health product/supplement
- User shares product images/links and asks for evaluation
- User asks about a specific ingredient or treatment
- User wants to know if a product is worth the price
- User describes symptoms and asks for product recommendations

## Workflow

### 1. Identify the Product
- Product name, brand, price
- Active ingredients (extract from images/labels)
- Claims made (on packaging, website, marketing materials)

### 2. Search for Clinical Evidence
- Web search: product name + "clinical trial" OR "study"
- Web search: active ingredient + clinical evidence + dosage
- Web extract: official product website for claims
- Cross-reference with PubMed, medical databases if needed
- Check if claims are for the ingredient or the specific product

### 3. Evaluate Claims vs Evidence
For each claim:
- Is there clinical evidence supporting it?
- Is the evidence for the ingredient or the specific product?
- Is the dosage in the product aligned with clinical studies?
- Are there cheaper alternatives with the same ingredient?
- Is the delivery method (chewable, tablet, capsule) optimal?

### 4. Structured Verdict

Output format:

```
## [Product Name] — Audit Ringkas

**[DER] Active ingredient:** [ingredient name] — [legit/scam/overpriced]

### Yang Betul
| Claim | Verdict |
|---|---|
| [claim] | [Sah/Tidak sah/Partially true] — [brief explanation] |

### Yang Kau Kena Tahu
| Issue | Detail |
|---|---|
| [issue] | [detail] |

### Untuk Siapa Berbaloi?
- **Berbaloi** kalau [conditions]
- **Tak berbaloi** kalau [conditions]

### Bottom Line
[One-line verdict]
```

### 5. Context-Aware Recommendation

If the product is for a specific person (Syed, Aliff, etc.):
- Cross-reference with known conditions, habits, sleep patterns
- Connect to root causes if symptoms are described
- Build causal chains: root cause → symptoms → cascading effects
- Give phased solutions (immediate, short-term, long-term)
- Match the person's profile (language preference, habits, constraints)

## Root Cause Chain Analysis

When symptoms are described, do not just address the symptom. Build causal chains:

```
Root cause (e.g., sleep deprivation)
    ↓
Primary symptom (e.g., bloating)
    ↓
Secondary effects (e.g., brain fog, emotional eating)
    ↓
Tertiary effects (e.g., weight gain, poor trading decisions)
```

Then give solutions at each level:
- **Immediate**: Address the symptom (e.g., simethicone for bloating)
- **Short-term**: Address the primary cause (e.g., fix sleep)
- **Long-term**: Build resilience (e.g., sleep hygiene, boundary setting)

## Pitfalls

- **Branded vs generic**: Many supplements are branded versions of generic ingredients. Always check if cheaper alternatives exist with the same active ingredient and dosage. Example: ZettaCare (branded Zinc L-Carnosine) vs generic Polaprezinc — same ingredient, half the price.
- **Marketing claims vs clinical evidence**: "100 studies" may refer to the ingredient, not the specific product. Clarify this distinction.
- **Do not evaluate in isolation**: If the product is for a specific person, connect to their known context (sleep, stress, eating habits, trading patterns, etc.).
- **Root cause > symptom relief**: If symptoms are described, build causal chains. Do not just address the symptom — address the root cause.
- **No "go see doctor"**: User explicitly said "Hang jgn suruh dia pi doktor. Dia hempuk doc tu nanti." Give practical, agentic solutions instead.
- **Phased solutions**: Break recommendations into immediate (hari ni), short-term (minggu ni), and long-term (next month). Make it actionable.
- **Language match**: If the person is BM-only (like Syed), give the recommendation in BM, not English.
- **Testimonials are not evidence**: Marketing testimonials are not clinical evidence. Flag this when present.
- **Delivery method matters**: Chewable tablets may have different absorption/contact time vs capsules vs slow-release tablets. Consider this in evaluation.

## Common Malaysian Health Product Patterns

| Pattern | Red Flag | Reality |
|---------|----------|---------|
| "100+ scientific studies" | Vague | Studies are for ingredient, not product |
| "Japan patented ingredient" | Sounds impressive | Patent does not equal clinical efficacy |
| "Available at major pharmacies" | Legit distribution | Does not mean product is unique |
| "Endoscopy-proven recovery" | Specific claim | Check if study was on ingredient or product |
| Testimonials in chat/images | Marketing material | Not independent reviews |

## Reference Files

- `references/zinc-l-carnosine-evidence.md` — Clinical evidence for Zinc L-Carnosine (Polaprezinc) — Japanese patented ingredient for gastric health. 30+ years in clinical use. Key studies, dosages, efficacy data.