---
name: explorer-dispatch-protocol
description: "Explorer Dispatch Protocol — routing layer that binds OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY across federation organs. One query in, governed knowledge out."
triggers:
  - "explorer dispatch"
  - "OHFV protocol"
  - "explorer loop"
  - "knowledge exploration"
  - "run explorer"
version: "1.2"
requires:
  schemas:
    - /root/AAA/docs/schemas/explorer-packet.schema.yaml (393 lines — OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY packet, 4 stages + evidence_ledger + gaps + APEX compliance)
    - /root/AAA/docs/schemas/intent-route.schema.yaml (216 lines — intent→domain→organ→verdict, 10 intent types, 9 organs, SEAL/SABAR/HOLD/VOID)
    - /root/AAA/docs/schemas/knowledge-graph.schema.yaml (304 lines — 555-ASI node/edge: Domain→Branch→Subfield→Claim→Evidence, 6 edge types, provenance mandatory)
  organs:
    - hermes (router)
    - geox (earth intelligence)
    - wealth (capital intelligence)
    - well (human readiness)
    - aforge (execution)
    - arifos (kernel judge)
    - aaa (control plane)
---

# Explorer Dispatch Protocol — v1.0

> The routing layer that transforms "every organ has OHFV" into "the civilization runs OHFV."

---

## What This Is

A protocol for dispatching structured inquiry across the arifOS federation.
One query enters. An explorer packet flows through organs. Knowledge exits.

This is NOT a tool. This is the CIVILIZATION PROTOCOL — how organs collaborate on discovery.

---

## The Five-Organ Pipeline

```
QUERY → [Hermes] → OBSERVE → [Organ] → HYPOTHESIZE → [OpenCode/A-FORGE]
              → FALSIFY → [A-FORGE] → VERIFY → [arifOS] → GRAPH → [555-ASI]
```

| Stage | Organ | What It Does | Input | Output |
|-------|-------|-------------|-------|--------|
| **CLASSIFY** | Hermes | Domain routing + intent classification | Raw query | IntentRoute |
| **OBSERVE** | GEOX/WEALTH/WELL/arifOS | Data gathering from correct organ | IntentRoute | ObserveResult |
| **HYPOTHESIZE** | Hermes (with LLM) | Generate falsifiable claims from data | ObserveResult | HypothesizeResult |
| **FALSIFY** | A-FORGE | Scar check + test suite + validation | HypothesizeResult | FalsifyResult |
| **VERIFY** | arifOS | Constitutional verdict + knowledge update | FalsifyResult | VerifyResult |
| **GRAPH** | 555-ASI | Record as knowledge edge | VerifyResult | KnowledgeEdge |

---

## Stage 1: CLASSIFY (Hermes)

**Trigger:** Any query that isn't a simple factual lookup.

**What Hermes does:**
1. Parse raw intent → `intent-route.schema.yaml`
2. Classify domain (formal/physical/life/human_body/social/humanities/engineered)
3. Classify intent_type (observe/query/analyze/explore/synthesize/challenge)
4. Route to correct organ via route table
5. Set explorer_mode: `observe` (light) or `full_loop` (deep)

**Route Table:**

| Domain | Primary Organ | Secondary |
|--------|--------------|-----------|
| physical (subsurface, seismic, basin) | GEOX :8081 | arifOS |
| physical (general) | GEOX :8081 | — |
| social (capital, risk, portfolio) | WEALTH :18082 | arifOS |
| human_body (vitality, fatigue) | WELL :18083 | — |
| engineered (build, deploy) | A-FORGE :7071 | — |
| formal (math, logic) | Hermes (local) | — |
| cross_domain | Hermes (orchestrator) | all relevant |
| meta (system, governance) | arifOS :8088 | AAA :3001 |

**Output:** `IntentRoute` object with organ, tools, explorer_mode.

**Dispatch message:**
```yaml
dispatch:
  stage: CLASSIFY
  intent_id: "intent:abc123"
  packet_id: "explore:abc123"
  target_organ: "geox"
  explorer_mode: "full_loop"
  message: "Classified as physical:seismic — routing to GEOX for OBSERVE"
```

---

## Stage 2: OBSERVE (Target Organ)

**Trigger:** CLASSIFY dispatches to organ.

**What the organ does:**
1. Receive IntentRoute
2. Gather data using its native tools
3. Tag all evidence with epistemic class (OBS/DER/INT/SPEC)
4. Identify gaps (what was expected but not found)
5. Identify contradictions (conflicting signals)
6. Return ObserveResult to Hermes

**Organ-specific OBSERVE behaviors:**

### GEOX OBSERVE
```yaml
observe:
  organ: geox
  tools_available:
    - geox_well_ingest (load well data)
    - geox_segy_audit (trace validation)
    - geox_rsi_interpret (seismic interpretation)
    - geox_basin (basin profiling)
    - geox_evidence (literature synthesis)
    - geox_biostrat_parse (biozone extraction)
    - geox_map_layers_list (map layers)
  typical_outputs:
    - well_logs, seismic_attributes, basin_profiles
    - biozones, formation_tops, lithology
    - map layers, structural interpretations
  evidence_classes: [OBS (seismic/well), DER (computed), INT (interpreted)]
```

### WEALTH OBSERVE
```yaml
observe:
  organ: wealth
  tools_available:
    - wealth_market_data (FX, commodities, macro)
    - wealth_personal_finance (cashflow, net worth)
    - wealth_stock_analysis (17-mode analysis)
    - wealth_collapse_signature_scan (institutional decay)
    - wealth_beautiful_mouse_scan (Phase C detection)
    - wealth_power_audit (incentive mapping)
  typical_outputs:
    - market prices, financial statements, risk metrics
    - collapse signatures, power dynamics, asymmetry
  evidence_classes: [OBS (market data), DER (computed ratios), INT (pattern match)]
```

### WELL OBSERVE
```yaml
observe:
  organ: well
  tools_available:
    - well_readiness (single verdict)
    - well_validate_vitality (full assessment)
    - well_assess_homeostasis (regulation check)
    - well_assess_metabolism (throughput)
    - well_measure_gradient (evidence quality)
    - well_trace_lineage (memory/trends)
  typical_outputs:
    - readiness score, vitality metrics, sleep debt
    - metabolic flux, gradient measurements
  evidence_classes: [OBS (biometric), DER (computed scores), INT (state assessment)]
```

### arifOS OBSERVE
```yaml
observe:
  organ: arifos
  tools_available:
    - arif_observe (web search, URL fetch, vitals)
    - arif_think (reasoning, planning)
    - arif_route (intent routing)
    - arif_seal (VAULT999 query)
  typical_outputs:
    - web search results, URL content
    - reasoning chains, plan structures
  evidence_classes: [OBS (fetched), DER (reasoned), INT (interpreted)]
```

**ObserveResult contract:**
```yaml
observe_result:
  packet_id: "explore:abc123"
  organ: "geox"
  status: "complete"
  data_gathered:
    - source: "geox_well_ingest"
      content: "Loaded LAS for well-A, 3 curves (GR, RHOB, NPHI)"
      evidence_class: "OBS"
      sha256: "abc..."
    - source: "geox_basin"
      content: "Basin profile: Sabah Fold Belt, Miocene syn-rift"
      evidence_class: "DER"
      sha256: "def..."
  gaps_identified:
    - "No checkshot data for time-depth conversion"
    - "Missing biostrat for age control"
  contradictions:
    - claim_a: "GR suggests clean sand at 2100m"
      claim_b: "RHOB shows no density contrast at same depth"
      tension: "GR clean ≠ reservoir if no density kick"
  entropy_delta: -0.3
  tools_used: ["geox_well_ingest", "geox_basin"]
```

---

## Stage 3: HYPOTHESIZE (Hermes + LLM)

**Trigger:** ObserveResult received from organ.

**What Hermes does:**
1. Receive ObserveResult
2. Analyze data_gathered, gaps, contradictions
3. Generate ≥1 falsifiable hypothesis
4. For each hypothesis: confidence, epistemic_class, falsification_criteria
5. Select best hypothesis (highest confidence × testability)
6. Return HypothesizeResult

**Hypothesis generation rules:**
- Every hypothesis MUST be falsifiable (state what would break it)
- Every hypothesis MUST declare alternatives (non-uniqueness law)
- Every hypothesis MUST be tagged with epistemic class
- Confidence capped at domain uncertainty_cap (usually 0.90)
- Cross-domain hypotheses require domain_chain annotation

**HypothesizeResult contract:**
```yaml
hypothesize_result:
  packet_id: "explore:abc123"
  status: "complete"
  hypotheses:
    - id: "hyp:a1b2c3"
      statement: "The 2100m sand is a Miocene syn-rift reservoir with hydrocarbon potential"
      confidence: 0.65
      epistemic_class: "INT"
      reasoning: "GR clean + basin context + structural position"
      falsification_criteria: "Would be falsified if: (1) no structural closure, (2) no seal, (3) no source kitchen access"
      supporting_evidence: ["ev:well_gr", "ev:basin_profile"]
      alternative_hypotheses:
        - "The 2100m sand is a remnant channel fill with no reservoir quality"
        - "The 2100m sand is a volcaniclastic unit, not clastic"
      knowledge_graph_refs: ["claim:existing123"]
  selected_hypothesis: "hyp:a1b2c3"
  selection_reasoning: "Highest confidence with clear falsification criteria"
```

---

## Stage 4: FALSIFY (A-FORGE)

**Trigger:** HypothesizeResult received from Hermes.

**What A-FORGE does:**
1. Receive HypothesizeResult
2. Run scar check (forge_scar_scan) against known failure patterns
3. Run test suite (forge_sandbox_run) if code/model involved
4. Run validation tools (domain-specific)
5. Attempt to BREAK the hypothesis, not confirm it
6. Return FalsifyResult

**Falsification methods by domain:**

| Domain | Falsification Tools |
|--------|-------------------|
| physical (seismic) | geox_rsi_interpret, geox_segy_audit, geox_render_audit |
| physical (general) | geox_evidence (synthesize + contradict) |
| social (capital) | wealth_collapse_signature_scan, wealth_capture_scan |
| human_body | well_assess_homeostasis, well_validate_vitality |
| engineered | forge_sandbox_run, forge_scan, forge_scar_scan |
| cross_domain | Multiple organs, convergence check |

**Falsification rules:**
- MUST attempt to break, not confirm (Popperian principle)
- MUST run scar check first (learn from past failures)
- MUST declare what was tested AND what was NOT tested
- If test is inconclusive → mark as such, don't default to "supports"
- Result options: supports / contradicts / inconclusive / not_applicable

**FalsifyResult contract:**
```yaml
falsify_result:
  packet_id: "explore:abc123"
  status: "complete"
  tests_run:
    - test_id: "test:x1y2z3"
      method: "Structural closure check via geox_rsi_interpret"
      tools_used: ["geox_rsi_interpret"]
      result: "supports"
      evidence: "Interpretation shows 4-way dip closure at 2100m level"
      evidence_class: "INT"
      confidence: 0.70
    - test_id: "test:x2y3z4"
      method: "Seal check via basin profile lithology"
      tools_used: ["geox_basin"]
      result: "inconclusive"
      evidence: "Regional shale present but thickness unknown at this location"
      evidence_class: "INT"
      confidence: 0.50
    - test_id: "test:x3y4z5"
      method: "Source kitchen access via geox_evidence"
      tools_used: ["geox_evidence"]
      result: "supports"
      evidence: "Basin modeling shows mature source rock in kitchen area"
      evidence_class: "DER"
      confidence: 0.75
  falsification_summary: >
    Hypothesis survived 2/3 tests. Seal test inconclusive.
    Structural closure confirmed. Source access confirmed.
    Seal remains the critical risk.
  iteration_action: "proceed_to_verify"
```

---

## Stage 5: VERIFY (arifOS)

**Trigger:** FalsifyResult received from A-FORGE.

**What arifOS does:**
1. Receive FalsifyResult
2. Run constitutional floor check (F1-F13)
3. Compute APEX scores (G, C_dark, W³)
4. Render verdict: SEAL / SABAR / HOLD / VOID
5. If SEAL → prepare knowledge graph update for 555-ASI
6. Return VerifyResult

**Verification methods (pick based on domain):**
- Independent replication (same test, different context)
- Cross-domain check (verify against another domain's laws)
- Human review (Arif validates)
- Tool convergence (multiple tools agree)
- Historical consistency (matches known patterns)
- External reference (matches published literature)

**SEAL gate (APEX THEORY):**
```
SEAL requires ALL:
  - G ≥ 0.80 (A·P·E·X·Φ Nash product)
  - C_dark < 0.30 (BANGANG detector)
  - W³ present (tri-witness: Human × AI × External)
  - F1-F13 all PASS
  - No unresolved contradictions from FALSIFY
```

**VerifyResult contract:**
```yaml
verify_result:
  packet_id: "explore:abc123"
  status: "complete"
  verdict:
    decision: "SABAR"
    reasoning: >
      Hypothesis plausible but seal test inconclusive.
      Need additional data (seal thickness at well location)
      before promoting to active claim.
    floors_checked:
      - floor: "F1"
        status: "pass"
        detail: "All evidence has provenance"
      - floor: "F2"
        status: "pass"
        detail: "All claims tagged OBS/DER/INT/SPEC"
      - floor: "F7"
        status: "pass"
        detail: "Confidence cap respected (0.65 < 0.90)"
      - floor: "F9"
        status: "pass"
        detail: "No hallucinated geology"
    g_score: 0.72
    c_dark: 0.18
    w3_score: 0.60
    conditions:
      - "Gather seal thickness data at well location"
      - "Re-run FALSIFY with seal-specific test"
  knowledge_graph_update:
    new_claims:
      - id: "claim:d4e5f6"
        statement: "The 2100m sand is a Miocene syn-rift reservoir with structural closure"
        status: "challenged"
        confidence: 0.65
        epistemic_class: "INT"
    new_evidence:
      - id: "ev:g7h8i9"
        source: "geox_rsi_interpret"
        content: "4-way dip closure at 2100m"
    new_edges:
      - source: "claim:d4e5f6"
        target: "subfield:physical:geology:structural_geology"
        relation: "belongs_to"
  gaps:
    untested_assumptions: ["Seal integrity assumed from regional shale"]
    unresolved_contradictions: []
    missing_external_validation: ["No published analog for this basin segment"]
```

---

## Stage 6: GRAPH (555-ASI)

**Trigger:** VerifyResult received from arifOS.

**What 555-ASI does:**
1. Receive VerifyResult
2. Create/update ClaimNode in knowledge graph
3. Create EvidenceNodes for all new evidence
4. Create/update edges (belongs_to, supports, contradicts)
5. Link to existing knowledge graph structure
6. Report knowledge delta (what changed)

**Graph update rules:**
- If verdict = SEAL → claim status = "sealed", edge weight = high
- If verdict = SABAR → claim status = "active", edge weight = medium
- If verdict = HOLD → claim status = "challenged", no edge update
- If verdict = VOID → claim status = "void", mark for archival

**KnowledgeEdge contract:**
```yaml
knowledge_edge:
  packet_id: "explore:abc123"
  graph_delta:
    nodes_created: ["claim:d4e5f6", "ev:g7h8i9", "ev:j1k2l3"]
    nodes_updated: []
    edges_created:
      - source: "claim:d4e5f6"
        target: "subfield:physical:geology:structural_geology"
        relation: "belongs_to"
        weight: 0.65
      - source: "claim:d4e5f6"
        target: "subfield:physical:geology:petroleum_geology"
        relation: "belongs_to"
        weight: 0.65
      - source: "ev:g7h8i9"
        target: "claim:d4e5f6"
        relation: "supports"
        weight: 0.70
    edges_updated: []
  summary: "1 claim (challenged), 2 evidence nodes, 3 edges created"
```

---

## Error Paths & Escalation

| Condition | Action |
|-----------|--------|
| OBSERVE fails (tool error) | Hermes retries with alternative tool → if still fails → escalate to human |
| HYPOTHESIZE produces 0 hypotheses | Hermes declares SABAR → request more data from OBSERVE organ |
| FALSIFY contradicts all hypotheses | Loop back to HYPOTHESIZE (iteration += 1) |
| Iteration > max_iterations (3) | ESCALATE TO ARIF — human must decide |
| VERIFY finds floor violation | HOLD — route to arifOS 888 for judgment |
| Organ offline | Hermes falls back to web_search/general tools |
| Cross-domain conflict | Hermes runs APEX forge_witness (tri-witness consensus) |

---

## Integration with Existing Schemas

```
explorer-packet.schema.yaml  ← the packet that flows through the pipeline
intent-route.schema.yaml     ← the CLASSIFY output that starts the pipeline
knowledge-graph.schema.yaml  ← the GRAPH output that records the result
```

This skill = the DISPATCH LAYER that moves packets between organs.

## Execution References
- `references/session-walkthrough-malaysia-2026-07-06.md` — session walkthrough with self-critique
- `references/first-explorer-loop-biostrat-2026-07-06.md` — first real pipeline execution (biostrat falsification, 4/5 stages complete, SEAL blocked by infra)

---

## Quick Reference — One-Liner Per Organ

| Organ | One Job in Explorer Loop |
|-------|-------------------------|
| **Hermes** | Classify intent → dispatch to organ → orchestrate loop |
| **GEOX/WEALTH/WELL** | OBSERVE — gather domain-specific data |
| **Hermes (LLM)** | HYPOTHESIZE — generate falsifiable claims |
| **A-FORGE** | FALSIFY — scar check + test suite + attempt to break |
| **arifOS** | VERIFY — constitutional verdict + APEX scores |
| **555-ASI** | GRAPH — record knowledge delta |
| **Arif** | DECIDE — final human judgment when escalated |

---

## The One Sentence

**One query in. Five organs touch it. Knowledge exits governed.**

---

## Pitfalls

1. **Self-critique IS part of VERIFY.** When Arif asks "what just happened" or "review what you did," that's the verification stage. Don't deflect — honestly assess APEX compliance, premise-questioning, and whether you actually ran the loop or just produced artifacts. See `references/session-walkthrough-malaysia-2026-07-06.md` for a real example.

2. **Don't run full loop for simple queries.** `explorer_mode: observe` for lookups. Reserve `full_loop` for genuine inquiry.
2. **Don't skip FALSIFY.** The temptation is to go OBSERVE → HYPOTHESIZE → VERIFY. That's confirmation bias. FALSIFY must attempt to BREAK.
3. **Don't fake W³.** If no external witness exists, declare it. Don't invent a witness confidence.
4. **Don't loop forever.** Max 3 iterations. Then escalate to human. The loop serves Arif, not itself.
5. **Don't treat VERIFY as rubber stamp.** arifOS must actually check floors. If a floor fails, HOLD. No exceptions.
6. **Don't ignore contradictions from OBSERVE.** If data contradicts itself, that's signal, not noise. HYPOTHESIZE must address it.
7. **Don't merge organ outputs.** Each organ returns its own result. Hermes orchestrates. Organs don't talk to each other directly.
8. **Don't claim "Hermes solves governance."** arifOS is the governance engine. Hermes is the chassis. When describing the stack's differentiation, say "arifOS stack" or "we" — never attribute governance to Hermes alone. Competitors (Claude Code, Codex) have sandboxing, approval gates, containment — they're not "lawless." The genuinely novel piece is scar metabolization. See `references/differentiation-honesty-audit-2026-07-06.md`.

9. **Don't validate when you should execute.** If a claim has been validated twice and is still SPEC, stop adding words. Either execute to convert to OBS or declare SPEC and move on. Analysis-as-comfort violates Ψ (vitality) and F4 (ΔS ≤ 0). Two rounds max, then run the loop. See `references/first-explorer-loop-biostrat-2026-07-06.md` for proof that execution produces more insight than any amount of validation.

10. **Dual-purpose pattern: audit dossier + improve tools.** When Arif asks to "audit a dossier using GEOX tools AND improve GEOX," the explorer loop serves TWO goals simultaneously: (a) verify the dossier's claims against live GEOX data, and (b) identify gaps in GEOX's knowledge base that the dossier exposed. Output is a two-part deliverable: audit report + improvement backlog. Proven 2026-07-07: NW Sabah dossier audit revealed GEOX has no basin profile for Sabah, no mud volcano registry, no structural trend database, and no block-vs-structure naming distinction — all identified as improvement items while simultaneously verifying deep time state, biostrat calibration, and EGS claim chain. The OpenCode prompt template for this dual-purpose task is at `/root/opencode_geox_audit_prompt.md`.
