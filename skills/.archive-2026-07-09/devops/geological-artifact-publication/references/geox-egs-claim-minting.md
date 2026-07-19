# GEOX-EGS Claim Minting — Visual Model → Machine-Readable Governance

Last proven: 2026-07-07, NW Sabah tectono-stratigraphic model (15 boxes + 1 synthesis, claim `bf5d1e78ebfb497b`).

## The Pattern

Convert a visual geological model (panel, cross-section, map) into GEOX-EGS claim objects for governance, audit, and queryability.

**The trinity:**
1. **Visual panel** = human front-end (PNG/PDF)
2. **JSON model** = queryable machine-readable structure
3. **EGS claims** = governance backbone (claim IDs, evidence, provenance)

## Step 1: Define the box structure

Each cell/element in the visual model becomes a JSON object:

```python
box = {
    "id": "MODEL_NAME::STAGE::LAYER",  # e.g. "NW_SABAH::S3_15_11Ma::CRUST_WEDGE"
    "stage": 3,
    "layer": "CRUST_WEDGE",
    "time_window": {"top_ma": 15, "base_ma": 11, "midpoint_ma": 13},
    "process_type": "overpressure_buildup",
    "process_description": "NSPW behaves as post-subduction shale wedge...",
    "epistemic_band": "CLAIM",  # CLAIM | PLAUSIBLE | ESTIMATE | HYPOTHESIS | SCHEMATIC
    "confidence": 0.85,
    "sources": ["morley2023", "nboss"],  # keys into source registry
    "deep_time_state_ref": "VAULT999::DTC::...",  # from geox_deep_time_state
    "requires_888_hold": False,
    "888_hold_reason": None,  # required when requires_888_hold=True
    "key_facts": ["fact 1", "fact 2"],
    "governance_note": "Why this band was assigned"
}
```

## Step 2: Build the source registry

```python
SOURCES = {
    "morley2023": {
        "author": "Morley, C.K.", "year": 2023,
        "title": "A major Miocene deepwater mud canopy system...",
        "journal": "Geosphere", "doi": "10.1130/GES02558.1",
        "epistemic_weight": 0.9
    },
    # ... one entry per cited source
}
```

## Step 3: Create the synthesis claim

```python
synthesis = {
    "id": "MODEL_NAME::SYNTHESIS",
    "type": "SYNTHESIS_CLAIM",
    "statement": "One-paragraph summary of the entire model...",
    "epistemic_band": "CLAIM",
    "confidence": 0.88,
    "box_count": 15,
    "claim_boxes": 10,
    "hypothesis_boxes": 2,
    "888_hold_boxes": ["S3::LITHOSPHERE", "S5::LITHOSPHERE"],
    "created_at": timestamp,
    "panel_version": "v2_governance_grade",
    "graphic_ref": "/path/to/panel_v2.png"
}
```

## Step 4: Write the JSON model

```python
output = {
    "schema": "geox-egs-tectono-strat-v1.0",
    "model_id": "MODEL_NAME",
    "created_at": timestamp,
    "created_by": "hermes-prime",
    "session_id": "SEAL-...",
    "total_boxes": len(boxes),
    "sources": SOURCES,
    "deep_time_references": {"20Ma": "VAULT999::...", "10.5Ma": "VAULT999::..."},
    "epistemic_summary": {"CLAIM": 9, "PLAUSIBLE": 2, "ESTIMATE": 1, "HYPOTHESIS": 2, "SCHEMATIC": 1},
    "888_hold_count": 2,
    "boxes": boxes,
    "synthesis": synthesis
}

with open('/path/to/model.json', 'w') as f:
    json.dump(output, f, indent=2)
```

## Step 5: Register in GEOX EGS

```python
# 1. Create the synthesis claim
claim = geox_egs_claim_create(
    title="Model Name — Stage 1 → Stage 2 → ... → Stage N",
    statement=synthesis["statement"],
    confidence_score=0.88,
    tags=["tag1", "tag2", "tag3"],
    author="hermes-prime"
)
# Returns claim_id (16-hex like "bf5d1e78ebfb497b")

# 2. Attach evidence (one per major source)
geox_egs_evidence_attach(
    claim_id=claim_id,
    description="Detailed evidence description with specific findings",
    evidence_kind="published_paper",  # or "geophysical_data", "well_data", etc.
    source="Author (Year) Journal doi:...",
    strength="strong",
    supporting=True  # or False for corrective/challenging evidence
)

# 3. Optionally challenge with corrective evidence
geox_egs_claim_challenge(
    claim_id=claim_id,
    challenge_statement="What the new evidence contradicts or weakens",
    challenger="reviewer_name_date"
)
```

## Step 6: Link deep time states

Use `geox_deep_time_state` for each time window to provide climate/ocean context:

```python
dts = geox_deep_time_state(age_ma=10.5, query="NSPW mud canopy event")
# Returns: CO₂ ~355 ppm, temp +4.6°C, sea level +21m, ice-free
# Store the VAULT999 seal ID as deep_time_state_ref in each box
# These are external consistency checks on your tectonic narrative
```

**Example consistency checks:**
- Mud canopy at 10.5 Ma in warm high-CO₂ ocean → consistent with high productivity ✓
- Mud canopy during glacial lowstand → would need different explanation ✗
- Source rock maturation during MCO → enhanced by high heat flow ✓

## Epistemic Band Assignment Rules

| Evidence quality | Band | 888_HOLD? |
|---|---|---|
| Published paper + well data + seismic | CLAIM | No |
| Published paper, consistent but not uniquely constrained | PLAUSIBLE | No |
| Timing/numbers approximate | ESTIMATE | No |
| Conceptually sound, not proven at scale | HYPOTHESIS | Yes |
| Simplified cartoon / teaching diagram | SCHEMATIC | No |

## Proven Example (2026-07-07, NW Sabah)

**Claim ID:** `bf5d1e78ebfb497b`
**Status:** draft → 3 supporting evidence attached, 0 against

| Band | Count | Examples |
|---|---|---|
| CLAIM | 9 | NSPW geometry, mini-basins, Rotan reservoirs, mud canopy |
| PLAUSIBLE | 2 | DG arrival timing, fossil slab at rest |
| ESTIMATE | 1 | Flexural basin sedimentation timing |
| HYPOTHESIS | 2 | Slab drip/breakoff → overpressure (888_HOLD) |
| SCHEMATIC | 1 | Trench fill model |

**Evidence attached:**
1. Morley 2023 Geosphere — mud canopy (CLAIM)
2. nBOSS + tomography — crustal architecture (CLAIM)
3. Hall PSCS + Hazebroek & Tan — subduction history (CLAIM)

**JSON model:** `/tmp/suci_dossier/nw_sabah_tectono_strat_model.json`
**Graphic:** `/tmp/suci_dossier/tectono_strat_panel_v2.png`

## Pitfalls

1. **Don't register every cell as a claim.** Register the synthesis + the 5-7 structurally important ones. The JSON model carries the per-cell detail.
2. **EGS claims are session-scoped.** A claim created in one session may return `GEOX_404_DATA` in a later session if the daemon restarted. Treat claim_id as a receipt, not a permanent handle. Create new claims rather than trying to update old ones.
3. **HYPOTHESIS ≠ wrong.** It means "conceptually sound but not uniquely constrained." Label it clearly; don't hide it. The hypothesis is often the interesting part.
4. **888_HOLD is for irreversible decisions.** A HYPOTHESIS about slab-drip timing is fine for exploration concepts, but should be flagged before well commitment or capital allocation.
5. **Source registry is reusable.** Keep it as a Python dict and reference it across sessions. The epistemic_weight field helps when computing aggregate confidence.
6. **Deep time state integration is optional but powerful.** It provides climate/ocean context as external consistency checks. Store the VAULT999 seal ID, not the raw values (which are INTERPRETED, not OBSERVED).
7. **Evidence kind matters.** Use "published_paper" for journal articles, "geophysical_data" for tomography/receiver functions, "well_data" for well results. EGS uses this for evidence quality scoring.
