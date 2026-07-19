# GEOX Audit Methodology for Scientific Documents

> Learned: 2026-07-05 (APEX Theory Review audit using GEOX MCP tools)
> Updated: 2026-07-05 (added biostrat_ruling_check, APEX claims mapping)
> Use when: auditing a scientific document's claims using live GEOX tools.

## The Pattern

When auditing a document for geological/scientific accuracy, use this combination of GEOX tools:

### Step 1 — Forbidden Claims Scan
```python
geox_forbidden_claims_scan(text=extracted_text)
```
Checks against 16 canonical forbidden geological/economic certainty patterns (8 block, 8 warn). Returns flagged claims with severity. If any BLOCK-level claims found → document needs downgrade.

### Step 2 — Contrast Detect (Theory of Anomalous Contrast)
```python
geox_contrast_detect(
    dimension="all",
    mass_predicted=X, mass_observed=Y,
    energy_predicted_stress=X, energy_observed_stress=Y,
    time_expected_ma=X, time_measured_ma=Y,
    absence_expected_thickness=X, absence_observed_thickness=Y,
    threshold=0.2
)
```
Tests predicted-vs-observed across 7 dimensions. Returns `contrast_magnitude`, `anomaly_class`, `severity`, `five_part_violation`. This IS the C_dark hallucination detector in practice.

### Step 3 — Rock Physics (if document makes velocity/density claims)
```python
geox_egs_rock_physics(vp_mineral=X, vp_fluid=Y, porosity=Z, rho_mineral=X, rho_fluid=Y)
```
Returns Voigt-Reuss-Hill bounds — validates whether claimed rock properties are physically possible.

### Step 4 — Seismic Compute (if document makes AI/EI claims)
```python
geox_egs_seismic_compute(vp_m_s=X, rho_g_cc=Y, compute_ai=True)
```
Returns acoustic impedance, Vs, Vp/Vs ratio. Validates seismic property claims.

### Step 5 — Deep Time State (if document makes age/paleoclimate claims)
```python
geox_deep_time_state(age_ma=X, query="topic description")
```
Returns full Earth State Vector with per-variable `epistemic_level` (OBSERVED/DERIVED/UNKNOWN/NO_DATA), `confidence` (0-1), and F9 fabrication guard. This IS the OBS/DER/INT/SPEC grading system in practice.

### Step 6 — Evidence Synthesis
```python
geox_evidence(query="topic", reasoning_mode="abductive", scale="parasequence")
```
Returns with embedded APEX gate scores (A, P, H, S, U, E dials) and verdict.

### Step 7 — Biostrat Ruling Check (if document makes biostratigraphic claims)
```python
geox_biostrat_ruling_check(
    biozone="NN5",
    lithology="sandstone",
    environment="deltaic",
    claim="interpretation text"
)
```
Returns `PASS | WEAK_PASS | CONTRADICTION | HOLD | REJECT`. The facies veto (B4 rule) catches deep marine biozones in shallow facies — exactly the kind of "hard constraint outperforms aggregate scoring" that APEX Theory's kill matrix describes.

### APEX Theory claims → GEOX tool mapping

| APEX Claim | GEOX Tool | Status |
|------------|-----------|--------|
| OBS/DER/INT/SPEC grading | `geox_deep_time_state` (epistemic_level per variable) | VALIDATED |
| C_dark hallucination detector | `geox_contrast_detect` (7-dimension anomaly) | VALIDATED |
| F9 ANTI-HANTU | `geox_forbidden_claims_scan` (16 patterns) | VALIDATED |
| Hard constraints > aggregate scores | `geox_biostrat_ruling_check` (facies veto) | VALIDATED |
| Multi-witness averaging | `geox_egs_rock_physics` (VRH Hill average) | CONSISTENT |
| Kill matrix governance | `geox_forbidden_claims_scan` + `geox_biostrat_ruling_check` | VALIDATED |

When auditing theoretical papers, check whether the paper's "open questions" are already answered by existing implementations.

## Pitfalls

- **SESSION_REQUIRED errors**: `geox_simulate_surfaces`, `geox_simulate_sequences`, `geox_evidence` (compute mode) require an active GEOX session. Use `geox_evidence` with `reasoning_mode="abductive"` for read-only synthesis.
- **Basin data not found**: `geox_basin(basin_name="Sabah")` returns NO_VALID_EVIDENCE — Sabah basin profile isn't ingested yet. Fall back to document data.
- **No detailed geological map layers**: For SE Asia, GEOX only has Natural Earth coastline/country boundaries. No geological layer coverage. Use document data for cross-sections.
- **Biostrat ruling check is a COMPUTE tool, not OBSERVE.** It requires a session for the reasoning lane. If you get SESSION_REQUIRED, the GEOX session isn't initialized. Use `geox_biostrat_parse` first (evidence lane, no session needed) to extract biozones, then try the ruling check.
