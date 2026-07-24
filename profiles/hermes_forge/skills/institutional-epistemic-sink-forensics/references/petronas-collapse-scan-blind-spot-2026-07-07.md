# Proven: PETRONAS collapse_signature_scan returns 0.0 (2026-07-07)

## The Test

Full PETRONAS 2024-2026 narrative fed to `wealth_collapse_signature_scan`:

> "PETRONAS entered 2024 under accumulating structural pressure. Net profit after tax fell 31.7% year-on-year to RM55.1 billion in FY2024, from RM80.7 billion in FY2023. Revenue declined 6.9% to RM320 billion. In June 2025, PETRONAS announced a firm-wide restructuring: approximately 10% of its global workforce — upward of 5,000 positions — would be cut. The governance layer thinned in parallel. By early 2025, the PETRONAS Board of Directors comprised six substantive directors and two company secretaries. Three directors had departed within a three-month window. On 8 June 2024, a BU Performance Manager leaked Q1 2024 upstream performance data to Petros C-suite. On 16 August 2024, Petros signed a competing GSA with Shell MDS. Shell MDS obtained an injunction freezing RM1 billion in gas payments for 13 months. Malaysia Bid Round 2025 offered zero Sarawak blocks. Tengku Muhammad Taufik framed all responses in finance-first language: 'prudent financial management,' 'portfolio diversification,' 'financial discipline.'"

## The Result

```json
{
  "risk": {"score": 0.0, "risk_level": "MINIMAL", "recommendation": "No institutional-collapse signature detected."},
  "acemoglu_axis": {"score": 0.5, "label": "INSUFFICIENT_SIGNAL", "extractive_count": 0, "inclusive_count": 0},
  "calhoun_axis": {"score": 0.5, "label": "INSUFFICIENT_SIGNAL", "sink_count": 0, "healthy_count": 0},
  "total_extractive_signals": 0,
  "total_inclusive_signals": 0,
  "overall_net_drift": 0
}
```

**0 signals across all 7 axes. 0 extractive. 0 inclusive. Risk = MINIMAL.**

## Why

The scanner is calibrated against EXTRACTIVE collapse patterns:
- Enron: CFO manipulation, off-balance-sheet entities
- PDVSA: political appointment replacing technical management
- 1MDB: sovereign wealth fund diversion
- Pemex: chronic underinvestment, political extraction

PETRONAS is none of these. Its collapse is SIMULATIVE — external actors (Shell, Petros) exploiting institutional weakness through legitimate legal procedures (interpleader, competing GSA, BG call). The scanner has no vocabulary for this pattern.

## What the New Tools Detected

| Tool | Result | What it catches |
|---|---|---|
| `wealth_institutional_stress_index` | **0.67 RED** | Composite stress from 5 dimensions |
| `wealth_cascade_model` | LINEAR (not spiral) | CoA intervention broke the feedback loop |
| `wealth_external_exploitation_detect` | **0.62 AGGRESSIVE** | Shell's behavior classified as exploitation |
| `wealth_governance_capacity` | 0.85 ADEQUATE | BOD composition analysis |

## Scenario Modeling (added 2026-07-07)

When a single pending decision creates binary outcomes, run `cascade_model` for both:

```
Model A: No CoA intervention → 99% → 100% (collapse in 2 quarters)
Model B: With CoA (actual) → 57% → 50% → 42% → 35% (recovering)
Model C1: Federal Court wins for Petronas (PDA prevails) → 35% → 25% → 15% → 6% (full recovery)
Model C2: Federal Court loses (Sarawak wins) → 100% → 100% → 100% → 100% (collapse)
```

**One ruling = 94 percentage points of stress difference.** Present the delta explicitly to sovereign.

## CEO-Era Contrast (added 2026-07-07)

| Dimension | Wan Zul (2015-2020) | Tengku Taufik (2018-present) |
|---|---|---|
| Background | Engineer, operations | Accountant, CFO, finance |
| Oil crash response | No mass layoffs, maintained dividend | Rightsizing 10%, profit dropped 32% |
| BOD | Stable, double-digit | 7 people, 3 resignations |
| Shell relationship | Cooperative, no litigation | First-ever lawsuit in 60 years |
| Sarawak management | Managed (2018 FC loss survived) | Escalated to full constitutional war |

**Shadow:** Operations CEO protects by managing relationships. Finance CEO exposes by enforcing contracts. Shell never sued in 60 years under Wan Zul. First lawsuit under Taufik — at the moment of maximum institutional weakness.

## Implication

When `collapse_signature_scan` returns 0.0 for an institution you KNOW is under stress, that's a **vocabulary gap**, not a falsification. Use the new institutional tools (`/root/wealth/wealth_core/institutional/`) to fill the gap.

The paper "The Simulative Shadow" (2026-07-07) is the theoretical framework that explains WHY the scanner missed it — Acemoglu's extractive institutions model is incomplete; needs simulative exploitation layer.
