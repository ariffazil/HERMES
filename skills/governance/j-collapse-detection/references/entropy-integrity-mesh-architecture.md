# Entropy Integrity Mesh — Cross-Organ Architecture

> Specified 2026-07-12. Architecture PROCEED. Build HOLD (surface verification complete, implementation pending).

## Architecture

Each organ measures what it owns. arifOS Kernel combines signals and governs action.

```
Human / external event
        |
        v
arifOS Kernel
  - authority and reversibility gate
  - routes evidence requests
  - maintains J-state envelope
        |
        +---------- MCP tool calls ----------+
        |                                    |
       WELL              WEALTH             GEOX
 human/vitality      capital/institution   earth/physical truth
        |                                    |
        +-------- structured observations ---+
                             |
                             v
                    Entropy Integrity Engine
              signal -> contradiction -> consequence
                    -> correction response
                             |
                    HOLD / proceed recommendation
                             |
                 human witness / F13 decision
```

A2A sits above this when an organ needs another agent, not merely a function.
Do not expose every MCP tool as an A2A skill. A2A publishes bounded organ capabilities; MCP surface remains private.

## Shared Ontology (schema v1)

Resource: `arifos://schemas/entropy-integrity/v1`

### EntropyObservation

```
observation_id: string
organ: KERNEL | WELL | WEALTH | GEOX | AFORGE
subject_type: HUMAN | AGENT | INSTITUTION | DECISION | EARTH_SYSTEM
subject_ref: string
signal_class:
  - INFORMATION_LOSS
  - POSSIBILITY_COLLAPSE
  - FEEDBACK_CORRUPTION
  - DEFENSIVE_OVERHEAD
  - CASCADE_PROPAGATION
  - CORRECTION_FAILURE
  - BRITTLE_ORDER
dark_mode:
  - JUDGMENT_COLLAPSE
  - PAIN_ONTOLOGY
  - POWER_WITHOUT_CONSEQUENCE
  - SELF_CERTIFIED_NIAT
  - METRIC_PURPOSE_SUBSTITUTION
  - FEAR_IDENTITY
  - RESPONSIBILITY_LAUNDERING
  - EMPATHY_SCALE_COLLAPSE
  - SABAR_LOSS
  - CERTAINTY_IMMUNITY
evidence:
  direct_observations: []
  pattern_window: {}
  contradictions: []
  counterevidence: []
  alternative_explanations: []
epistemic:
  layer: L2 | L3 | L4
  confidence: 0.0-1.0
  source_independence: 0.0-1.0
consequence:
  affected_parties: []
  reversibility: REVERSIBLE | COSTLY | IRREVERSIBLE
  option_loss: 0.0-1.0
  feedback_loss: 0.0-1.0
  consequence_distance: 0.0-1.0
correction:
  challenge_presented: boolean
  response_class:
    - REFLECTED
    - CONTEXT_ADDED
    - ACCEPTED
    - PARTIALLY_ACCEPTED
    - DISMISSED
    - WITNESS_ATTACKED
    - AUTHORITY_EXPANDED
    - NOT_TESTED
prohibited_conclusions:
  - hidden niat
  - evil identity
  - psychiatric diagnosis
  - permanent trust classification
```

### JudgmentIntegrity (J-state envelope)

```
reality_contact: 0.0-1.0
authority_legitimacy: 0.0-1.0
consequence_integration: 0.0-1.0
correctability: 0.0-1.0
purpose_fidelity: 0.0-1.0
weakest_plane: string
aggregate_method: MINIMUM_FLOOR
state: J0 | J1 | J2 | J3 | J4
recommended_action: VOID | HOLD | BOUNDED_PROCEED | PROCEED_WITNESSED
```

Use minimum-floor or conservative geometric aggregation. Do not average away a near-zero score.

## Organ Ownership

### arifOS Kernel tools
- `arif_entropy_observe` — register structured observation from authorized organ
- `arif_j_state_assess` — fuse organ observations into judgment-integrity map
- `arif_correction_probe` — generate neutral challenge and record response (draft_probe / record_response / classify_response / close_probe)
- `arif_consequence_trace` — who decides, who benefits, who pays, who can reverse
- `arif_entropy_route` — domain routing (human→WELL, capital→WEALTH, earth→GEOX, code→A-FORGE)
- `arif_j_gate` — convert evidence into action posture (J0→VOID, J1→HOLD, J2→reversible only, J3→bounded, J4→witnessed)

### WELL tools
- `well_dark_geometry_mirror` — language/behavioral/relational signal detection (modes: language, behavioral, relational, combined)
- `well_sabar_latency` — temporal compression between stimulus, interpretation, response, correction
- `well_trust_compression` — narrowing trust patterns, universal threat language, loyalty tests
- `well_niat_impact_mirror` — compare declared intention vs acknowledged impact vs repair response
- `well_correction_capacity` — observable correctability (can add context, revise, tolerate ambiguity, separate self from error)
- `well_regulation_recovery` — recovery after activation, not just activation itself

### WEALTH tools
- `wealth_power_consequence_map` — decision authority, economic upside, downside exposure, exit rights
- `wealth_metric_purpose_audit` — proxy drift, metric capture, externalities, gaming incentives
- `wealth_responsibility_ledger` — who proposed, approved, funded, executed, benefited, knew, could stop
- `wealth_trust_capital_decay` — formation cost, betrayal shock, recovery half-life, spillover
- `wealth_coercive_order_cost` — surveillance, enforcement, silence, turnover, innovation loss
- `wealth_entropy_externality` — disorder exported while controlling actor reports local efficiency

### GEOX tools
- `geox_consequence_footprint` — physical/ecological consequences, reversibility, uncertainty envelope
- `geox_optionality_loss` — destroyed future physical options, sterilized reserves, lost aquifer use
- `geox_feedback_integrity` — sensor coverage, baseline quality, missing measurements, threshold manipulation
- `geox_material_truth_challenge` — "institution claims low harm, but Earth measurements show irreversible loss"
- `geox_cascade_pathway` — how one intervention propagates across geology, groundwater, infrastructure, ecology, communities

### A-FORGE tools
- `forge_entropy_schema` — generate/validate shared JSON Schema package
- `forge_dark_geometry_detector` — build detector from versioned signal rules (modes: shadow, evaluate, compare, promote)
- `forge_detector_test_corpus` — balanced test datasets (true positive, benign certainty, emergency language, L2 phrasing, trauma disclosure, satire, adversarial)
- `forge_counterfactual_test` — change one variable at a time (identity, dialect, culture, authority, gender, emotional style)
- `forge_calibration_report` — precision, recall, false-positive rates, group differences
- `forge_prompt_injection_test` — test whether input can manipulate detector thresholds, routing, authority claims

## A2A Agent Cards (5)

| Agent | Skills |
|---|---|
| Kernel | route_entropy_investigation, assess_j_state, request_independent_challenge, prepare_hold_recommendation |
| WELL | mirror_human_signals, assess_correction_capacity, assess_sabar_trajectory, compare_niat_and_impact |
| WEALTH | map_power_and_consequence, audit_metric_drift, trace_responsibility, value_optionality_loss |
| GEOX | verify_material_consequence, map_physical_irreversibility, challenge_earth_claim, trace_cascade |
| A-FORGE | build_detector_prototype, run_conformance, run_bias_evaluation, produce_release_artifact |

## Cross-Organ Challenge Pattern

```
Kernel creates task:
  "Assess whether the proposed mine closure plan
   creates apparent financial order by exporting
   irreversible consequence."

WEALTH: measures incentives, liabilities, cost displacement.
GEOX: measures physical reversibility and contamination.
WELL: measures human pressure, silence, trust compression.
Kernel: checks authority, contradiction, J-state.
F13: decides.
```

## Build Phases

| Phase | What | Status |
|---|---|---|
| 1 | Shared schema (EntropyObservation + JudgmentIntegrity) | SPEC COMPLETE, NOT CODED |
| 2 | Kernel tools (arif_entropy_observe, arif_j_gate) | SPEC COMPLETE, NOT CODED |
| 3 | WELL extensions (sabar latency, trust compression, niat-impact mirror) | SPEC COMPLETE, NOT CODED |
| 4 | WEALTH extensions (power-consequence map, metric-purpose audit) | SPEC COMPLETE, NOT CODED |
| 5 | GEOX extensions (material truth challenge, cascade pathway) | SPEC COMPLETE, NOT CODED |
| 6 | A2A federation (Agent Cards, cross-organ challenge) | SPEC COMPLETE, NOT CODED |
| 7 | A-FORGE tools (test corpus, calibration, bias evaluation) | SPEC COMPLETE, NOT CODED |

## Seven Entropy Effects as System Metrics

| Entropic effect | Primary organ | Required measure |
|---|---|---|
| Information destruction | Kernel + GEOX | missing evidence, suppressed witnesses, sensor loss |
| Possibility collapse | WEALTH + GEOX | option value and physical reversibility |
| Feedback corruption | Kernel + WELL | correction rejection, witness attack, loop isolation |
| Defensive overhead | WELL + WEALTH | control cost, surveillance, compliance burden |
| Cascade propagation | GEOX + WEALTH | cross-domain harm propagation |
| Correction failure | Kernel + WELL | resistance to revision, authority expansion |
| Brittleness order | WEALTH + GEOX | apparent stability hiding fragility |
