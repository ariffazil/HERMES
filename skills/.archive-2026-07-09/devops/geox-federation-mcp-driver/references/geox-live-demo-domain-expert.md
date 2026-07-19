# GEOX Live Demonstration — Domain Expert Pattern

> Proven: 2026-07-06, KLCC, with Raja (geologist, Sabah Ventures)
> Arif asked Hermes to "prove GEOX has macrostrat data" in real-time during a social meeting.

## When To Use

- Arif is with a domain expert and wants to demonstrate GEOX capability
- Someone asks "does this actually work?" about GEOX tools
- Need to prove real-time geological computation, not just describe it

## The Rule: Show, Don't Tell

Domain experts don't care about your architecture. They care about **outputs they can evaluate**. Run the tools, show the results, admit the gaps. A honest WEAK_PASS with clear reasoning builds more credibility than a fabricated PASS.

## Proven Tool Chain: Sabah Deepwater (3-tool sequence)

### Sequence 1: Basin Profile

```
Tool: geox_basin
Args: basin_name="Sabah", mode="profile", profile_mode="overview"
Expected: "Basin data not found for: Sabah"
Why: Sabah is not a registered basin entity in GEOX. This is HONEST — say it.
Fallback: Use macrostrat_calibrate with lat/lng instead.
```

### Sequence 2: Macrostrat Biozone Calibration (offshore)

```
Tool: geox_macrostrat_calibrate
Args:
  biozone="NN19"
  discipline_hint="calcareous nannofossil"
  lat=6.5, lng=118  (offshore Sabah, Block 3K area)
  radius_km=100

Result (2026-07-06):
  age_top_ma: 1.04
  age_base_ma: 1.73
  ruling: WEAK_PASS
  ruling_confidence: 0.6
  macrostrat_units_found: 0
  macrostrat_unit_match: null
  macrostrat_interval: null
  calibration_source: geox_internal

Key insight: WEAK_PASS because GEOX internal NN-age table returned a result
but Macrostrat had NO units at offshore coordinates within 100km.
This is EXPECTED for deepwater locations — Macrostrat has surface geology,
not offshore subsurface. The internal calibration still works.

Honest presentation to domain expert:
"NN19 calibrates to 1.04–1.73 Ma Pleistocene. Macrostrat cross-reference
is empty because it's offshore — that's a known limitation. The calibration
uses GEOX internal GPTS2020 table, which is solid."
```

### Sequence 3: Deep Time State

```
Tool: geox_deep_time_state
Args: age_ma=5.0  (or any age of interest)

Result (2026-07-06, Pliocene):
  epoch: Pliocene (4.0-6.0 Ma)
  geomagnetic_polarity: mixed (C2A, C3 chrons, 9 subchrons)
  supercontinent: Modern (Pangaea fragments dispersed)
  ice_extent: Ice-free (warm-house state)
  solar_luminosity: 0.9996 L/L0
  day_length: 23.985 hours
  orbital_eccentricity: 0.04
  obliquity: 23.4°
  biotic_realm: Modern mammal families, grassland expansion, hominid evolution
  mass_extinctions: None in window
  overall_confidence: 0.84
  variables_with_real_data: 9/14
  variables_pending: 5 (CO2, temperature, d18O, sea_level, O2)
  verdict: SEAL

Sources: Gough 1981, Laskar 2011 (La2011), Bradley 2011,
Gradstein 2020 (GTS2020), Ogg 2020, Davies 2020.

What to highlight for geologists:
- Geomagnetic polarity chrons are OBSERVED (GTS2020 frozen CSV)
- Ice-free state at 5 Ma = known warm Pliocene
- Pending datasets (CO2, sea level) are honest gaps, not failures
- F9 fabrication guard marks truly unknowable params as NO_DATA
```

## Offshore Macrostrat Limitations (Known Pattern)

When querying macrostrat_calibrate at offshore coordinates:

| Location Type | Expected Macrostrat Result | Why |
|---|---|---|
| Onshore, well-mapped | PASS with unit matches | Macrostrat has surface geology |
| Onshore, remote | WEAK_PASS or 0 units | Sparse coverage |
| Nearshore/shelf | WEAK_PASS, 0 units | Limited offshore mapping |
| Deepwater (e.g., Block 3K) | 0 units, WEAK_PASS | Macrostrat is surface-only |

The internal NN-age table still works regardless — it's a lookup, not a spatial query. Present this honestly: "The biozone-age lookup is solid. The spatial cross-reference is empty because we're offshore."

## Presentation Tips for Domain Experts

1. **Lead with the most impressive output.** Deep Time State at 5 Ma with 9 variables, 0.84 confidence, VAULT999 seal — that's the hook.

2. **Admit limitations before they find them.** "Basin profile doesn't have Sabah" — say it first. Builds trust.

3. **Use their language.** Don't say "the tool returned a structured JSON envelope." Say "NN19 gives you 1.04 to 1.73 Ma Pleistocene."

4. **Show the governance layer.** Mention that every output has provenance, confidence bands, and F9 fabrication guard. Domain experts care about reproducibility.

5. **Offer to test THEIR data.** "Give me a biozone or coordinate — I'll query now." This turns a demo into a conversation.

## Quick Reference: Biozone Examples for Demo

| Biozone | Age Range | Epoch | Good For |
|---|---|---|---|
| NN19 | 1.04–1.73 Ma | Pleistocene | Sabah deepwater, Malay Basin Plio-Pleistocene |
| NN5 | 11.0–12.8 Ma | Mid-Miocene | Malay Basin main reservoir section |
| NN1 | 22.0–23.0 Ma | Early Miocene | Older section, pre-rift |
| P22 | 28.0–33.0 Ma | Late Oligocene | Deep carbonate targets |

## What NOT To Do

- Don't claim basin profile "works" for Sabah — it doesn't, say so
- Don't hide WEAK_PASS results — they're more honest than fabricated PASS
- Don't dump raw JSON — extract the human-readable values
- Don't promise tools that aren't live (e.g., simulate_* may be RT1_GUARD blocked)
- Don't forget to mention TotalEnergies partnership if discussing Block 3K — domain experts know the deal structure

## Session Provenance

- Date: 2026-07-06
- Location: KLCC (social setting with Raja, geologist, Sabah Ventures)
- Tools tested: geox_basin, geox_macrostrat_calibrate, geox_deep_time_state
- All three returned valid structured output
- Basin profile: expected failure (Sabah not registered)
- Macrostrat: WEAK_PASS (offshore limitation, internal cal still works)
- Deep time: SEAL with 0.84 confidence
