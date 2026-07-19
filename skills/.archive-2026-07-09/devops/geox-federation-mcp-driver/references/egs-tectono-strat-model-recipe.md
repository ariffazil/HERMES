# Tectono-Stratigraphic EGS Model — Sabah NSPW Example

## Overview
Registering a multi-box tectono-stratigraphic model as machine-readable JSON in GEOX EGS,
with epistemic labels per panel and the full claim→evidence→challenge chain.

## Workflow (proven 2026-07-07)

### Step 1: Define the model structure
Each "box" in the tectono-stratigraphic panel becomes a structured JSON object:
```json
{
  "id": "NW_SABAH::S1_35_20Ma::LITHOSPHERE",
  "stage": 1,
  "layer": "LITHOSPHERE",
  "time_window": {"top_ma": 35, "base_ma": 20, "midpoint_ma": 27.5},
  "process_type": "subduction",
  "process_description": "PSCS oceanic plate descends beneath NW Borneo...",
  "epistemic_band": "CLAIM",
  "confidence": 0.9,
  "sources": ["hall_pscs", "hazebroek_tan"],
  "requires_888_hold": false,
  "key_facts": ["PSCS was oceanic", "Subduction beneath Borneo"]
}
```

### Step 2: Add epistemic bands per box
- **CLAIM** (green, 0.85+): Well supported by published data
- **PLAUSIBLE** (blue, 0.7-0.85): Consistent, not uniquely constrained
- **ESTIMATE** (amber, 0.6-0.7): Timing/numbers approximate
- **HYPOTHESIS** (red, 0.5-0.6): Conceptually sound, not proven at scale → 888_HOLD
- **SCHEMATIC** (gray, <0.6): Simplified cartoon

### Step 3: Register synthesis claim in EGS
```
geox_egs_claim_create(
  title="NW Sabah Tectono-Stratigraphic Evolution Model",
  statement="NW Sabah deepwater is a post-subduction collisional continental margin...",
  domain="tectono-stratigraphy",
  confidence_score=0.88,
  tags=["NSPW", "mud_canopy", "PSCS"]
)
→ Returns claim_id (e.g., bf5d1e78ebfb497b)
```

### Step 4: Attach evidence (at least 3 for governance)
```
geox_egs_evidence_attach(claim_id, description="Morley 2023...", 
  evidence_kind="published_paper", source="Geosphere", strength="strong", supporting=True)
geox_egs_evidence_attach(claim_id, description="nBOSS crustal data...",
  evidence_kind="geophysical_data", strength="strong", supporting=True)
geox_egs_evidence_attach(claim_id, description="Hall PSCS...",
  evidence_kind="published_paper", strength="strong", supporting=True)
```

### Step 5: Write machine-readable JSON model
Write the full model (all boxes + synthesis + sources + deep_time_refs) to a JSON file.
This is the human-front-end for a live, queryable tectono-strat model.

### Step 6: Generate epistemic-label panel (matplotlib)
Each panel box gets a colored tag (CLAIM/PLAUSIBLE/etc.) with source citation.
Include coordinate verification disclaimer on maps.

## Key Pitfalls
1. **EGS claims are session-scoped** — claim_id may not persist across daemon restarts
2. **Deep time state refs** — link to `VAULT999::DTC::*` seal hashes from GEOX deep_time_state runs
3. **Macrostrat calibration** — offshore returns WEAK_PASS with 0 units (expected, not error)
4. **Coordinate verification** — NEVER plot from memory. See geoscience-verification-protocol skill.
5. **Block names ≠ structural labels** — L-B-P trend ≠ PSC block names. Verify before attributing.

## Sabah Model Reference
- Claim ID: bf5d1e78ebfb497b
- 15 boxes (5 stages × 3 layers) + 1 synthesis
- 9 CLAIM, 2 PLAUSIBLE, 1 ESTIMATE, 2 HYPOTHESIS (888_HOLD), 1 SCHEMATIC
- 3 evidence items attached (Morley 2023, nBOSS, Hall PSCS)
- JSON: /tmp/suci_dossier/nw_sabah_tectono_strat_model.json
