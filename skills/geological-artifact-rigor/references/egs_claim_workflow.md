# GEOX EGS Claim Registration Workflow

> Used during NW Sabah tectono-stratigraphic model registration (2026-07-07)
> Tools: geox_egs_claim_create, geox_egs_evidence_attach, geox_egs_claim_challenge

## Workflow

### Step 1: Create Claim
```python
geox_egs_claim_create(
    title="...",
    statement="...",  # Full synthesis statement
    domain="tectono-stratigraphy",  # or appropriate domain
    confidence_score=0.88,  # Must be justified
    tags=["tag1", "tag2"],
    author="hermes-prime"
)
# Returns: claim_id (e.g., "bf5d1e78ebfb497b")
```

### Step 2: Attach Evidence (repeat for each source)
```python
geox_egs_evidence_attach(
    claim_id="bf5d1e78ebfb497b",
    description="What this evidence proves",
    evidence_kind="published_paper",  # or geophysical_data, field_observation
    source="Author (Year) Journal/Institution",
    strength="strong",  # strong/moderate/weak
    supporting=True  # True = for, False = against
)
# Returns: evidence_id
```

### Step 3: Register 888_HOLD items
For HYPOTHESIS-level claims that need human confirmation:
- Set `requires_888_hold: true` in the claim
- Document `888_hold_reason` explaining what data would upgrade to CLAIM
- Name the specific dataset/well/measurement needed

### Step 4: Challenge (if needed)
```python
geox_egs_claim_challenge(
    claim_id="...",
    challenge="New evidence or reasoning that questions the claim"
)
```

## Epistemic Band Assignment

| Band | Meaning | When to Use |
|------|---------|-------------|
| CLAIM | Well supported by published data | Multiple independent sources agree |
| PLAUSIBLE | Consistent, not uniquely constrained | One strong source, no contradiction |
| ESTIMATE | Timing/numbers approximate | Published ranges, not well-specific |
| HYPOTHESIS | Conceptually sound, not proven at scale | Geodynamics/modeling, not direct observation |
| SCHEMATIC | Simplified cartoon | No real data available, used for illustration |

## Example: NW Sabah Synthesis Claim

```
Claim ID: bf5d1e78ebfb497b
Title: NW Sabah Tectono-Stratigraphic Evolution Model
Confidence: 0.88
Evidence: 3 attached (Morley 2023, nBOSS, Hall PSCS)
888_HOLD: 2 boxes (slab drip, overpressure trigger)
Status: draft
```

## Pitfalls

- Don't create claims before evidence exists — the claim wraps content, not generates it
- Don't use "CLAIM" band for things that are actually ESTIMATE or HYPOTHESIS
- Always name what would upgrade each HYPOTHESIS (rule 5 of geological-artifact-rigor)
- Session may expire between claim creation and evidence attachment — re-init if needed
