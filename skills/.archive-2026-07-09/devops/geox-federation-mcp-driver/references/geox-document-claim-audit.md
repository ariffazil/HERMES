# GEOX Document Claim Audit Pattern

**Use when:** Arif sends a scientific document (PDF, markdown) and asks to "audit", "validate", "improve", or "fact-check" it using GEOX tools.

**Proven:** 2026-07-05, APEX Theory Review audit (24-page PDF, 40 references, 15 open questions).

## The Pattern

The document contains geological/scientific claims. Instead of reading-and-opinionating, use GEOX tools as a **mechanical fact-check** against each claim class.

### Step 1 — Extract text

```bash
pdftotext /path/to/document.pdf - 2>/dev/null | head -500
# Also get total size:
pdftotext /path/to/document.pdf - 2>/dev/null | wc -l
```

### Step 2 — Forbidden claims scan

Scan the full text (or key claims) against GEOX's canonical forbidden-claims list:

```
geox_forbidden_claims_scan(text="...full document text or key claims...")
```

- `block_count > 0` → STOP. Claims must be downgraded before proceeding.
- `warn_count > 0` → Add caveats.
- `total_flagged == 0` → Clean. Proceed.

### Step 3 — Contrast detect (Theory of Anomalous Contrast)

If the document makes quantitative predictions (thickness, stress, temperature, age), test them against `geox_contrast_detect`:

```
geox_contrast_detect(
    dimension="all",
    mass_predicted=..., mass_observed=...,
    energy_predicted_stress=..., energy_observed_stress=...,
    time_expected_ma=..., time_measured_ma=...,
    absence_expected_thickness=..., absence_observed_thickness=...
)
```

The 7 dimensions (mass, energy, time, absence + 3 more) catch mismatches between predicted and observed values. The `cross_dimensional_conflicts` array reveals whether anomalies reinforce each other (CONSISTENT) or contradict (INCONSISTENT).

**Key insight from APEX audit:** Even when individual claims pass, the contrast detect can reveal **system-level mismatches** that no single-claim check catches. The energy dimension showed 300% underprediction (critical) while time showed only 22% — the system's energy budget was the weakest link, not its chronology.

### Step 4 — Domain-specific tool tests

Map the document's claims to the appropriate GEOX tool:

| Claim Type | GEOX Tool | What It Tests |
|------------|-----------|---------------|
| Biostratigraphic age | `geox_biostrat_ruling_check` | Facies veto: does the biozone match the claimed environment/lithology? |
| Deep time / paleoenvironment | `geox_deep_time_state` | Earth state vector at claimed age — what was OBSERVED vs NO_DATA? |
| Rock physics / velocity | `geox_egs_rock_physics` | Voigt-Reuss-Hill averaging — is the multi-witness claim physically grounded? |
| Basin structure | `geox_basin` | Does the basin have registered data? (Many return NO_VALID_EVIDENCE) |
| Geographic location | `geox_atlas` | Point-in-country + land/water classification |
| Stratigraphic correlation | `geox_sequence` / `geox_macrostrat_calibrate` | Age-depth relationship, biozone calibration |

### Step 5 — Synthesize audit table

Produce a table mapping each document claim → GEOX tool tested → result → implication:

```markdown
| Document Claim | GEOX Tool | Result | Implication |
|----------------|-----------|--------|-------------|
| OBS/DER/INT/SPEC grading is unique | geox_deep_time_state | 9/14 vars real data, 5 NO_DATA | VALIDATED — GEOX implements this natively |
| Geological isomorphism holds | geox_contrast_detect + Sabah synthesis | 4/4 anomalies found | STRONGLY SUPPORTED |
| Evidence grading catches raw-score misses | geox_biostrat_ruling_check (NN5/deltaic) | CONTRADICTION returned | VALIDATED — facies veto works |
```

### Step 6 — Write improved document

Use the audit table to:
1. **Upgrade** claims that passed (VALIDATED → STRONGLY VALIDATED)
2. **Downgrade** claims that failed (UNTESTED → FALSIFIED or PARTIALLY RESOLVED)
3. **Add** new GEOX-validated evidence sections
4. **Preserve** claims that couldn't be tested (mark as UNRESOLVED, not dismissed)

## What makes this different from a literature review

A literature review reads papers and opines. This pattern **runs tools against claims**. The output is not "I think this is right" — it's "GEOX tool X returned result Y when given this claim's parameters." The tool output IS the evidence.

## Pitfalls

1. **GEOX tools may not have data for the claimed domain.** `geox_basin(basin_name="Sabah")` returns `Basin data not found`. This is NOT a rejection of the claim — it means GEOX doesn't have that basin registered. Document the gap honestly.

2. **The forbidden_claims_scan is regex-based, not semantic.** It catches explicit forbidden patterns but may miss subtly overclaimed language. Use it as a first pass, not a final authority.

3. **contrast_detect requires numeric inputs.** If the document only makes qualitative claims, this tool can't help. Skip to domain-specific tools instead.

4. **Session required for reasoning-lane tools.** `geox_biostrat_ruling_check`, `geox_deep_time_state`, `geox_egs_rock_physics` all require a session. Use `geox_surface_status` or `geox_atlas` first to validate connectivity (these are evidence-lane, no session needed).

5. **The improved document should cite GEOX tool outputs as evidence.** Not "GEOX validated this" but "`geox_biostrat_ruling_check` returned CONTRADICTION for NN5/deltaic facies, confirming the evidence grading claim."
