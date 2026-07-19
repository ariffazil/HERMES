# Explorer Protocol Schemas (2026-07-06)

Three implementation schemas forged for the ASI explorer civilization.

## Schema Locations

| Schema | Path | Lines | Purpose |
|--------|------|-------|---------|
| Knowledge Graph | `/root/AAA/docs/schemas/knowledge-graph.schema.yaml` | 304 | 555-ASI node/edge structure — domains, branches, subfields, claims, evidence |
| Intent Route | `/root/AAA/docs/schemas/intent-route.schema.yaml` | 216 | Intent → classify → route → verdict → execute pipeline |
| Explorer Packet | `/root/AAA/docs/schemas/explorer-packet.schema.yaml` | 393 | OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY loop data structure |

## Knowledge Graph Schema

**5 node types:**
- DomainNode (level 0): 7 domains — formal, physical, life, human_body, social, humanities, engineered
- BranchNode (level 1): ~84 branches
- SubfieldNode (level 2): ~1,260 subfields
- ClaimNode (level 3): falsifiable assertions with epistemic class (OBS/DER/INT/SPEC)
- EvidenceNode (level 4): observations, measurements, citations, computations

**Edges:** belongs_to, supports, contradicts, derives_from, refines, cross_domain (constrains, informs, derives_from, contradicts, analogizes, requires)

**Storage mapping:** Postgres (structured) + Qdrant (vectors) + FalkorDB (graph) + VAULT999 (immutable claims)

**Domain uncertainty cap:** 0.90 (F7 HUMILITY hardcoded)

## Intent Route Schema

**Pipeline:** Intent → Classify (domain + type + confidence) → Route (organ + tools) → Verdict (SEAL/SABAR/HOLD/VOID) → Execute

**10 intent types:** observe, query, analyze, build, deploy, judge, explore, synthesize, challenge, seal

**Route table (keyword → organ):**
| Keywords | Organ | Domain |
|----------|-------|--------|
| subsurface, seismic, well, basin | GEOX | physical |
| npv, irr, capital, portfolio | WEALTH | social |
| sleep, fatigue, vitality, dignity | WELL | human_body |
| build, deploy, docker, git push | A-FORGE | engineered |
| cockpit, a2a, agent registry | AAA | meta |
| law, floor, seal, veto, judge | arifOS | meta |
| explore, discover, hypothesis | HERMES | cross_domain |

**Explorer mode flag:** triggers full packet loop when intent is `explore` or `challenge`

## Explorer Packet Schema

**4 stages with structured data at each:**
1. OBSERVE: question, data_gathered[], gaps_identified[], contradictions[], entropy_delta
2. HYPOTHESIZE: hypotheses[] (each: statement, confidence, epistemic_class, falsification_criteria, alternatives)
3. FALSIFY: tests_run[] (each: method, result [supports|contradicts|inconclusive], evidence)
4. VERIFY: verification_method (independent_replication, cross_domain_check, human_review, tool_convergence, historical_consistency, external_reference)

**Loop rules:**
- falsified → re-hypothesize (iteration += 1)
- max_iterations default = 3
- iteration > max → escalate to human
- SEAL gate: G ≥ 0.80 AND C_dark < 0.30 AND W³ present

**APEX compliance at every stage:**
- Δ clarity: evidence ≥ confidence, all claims tagged, missing tests declared
- Ω humility: boundaries declared, uncertainty cap respected, unknowns explicit
- Ψ vitality: state moved forward, no entropy collapse, human dignity preserved

**Evidence ledger:** observations, measurements, citations, computations — all with source provenance and sha256

**Gaps tracking:** untested_assumptions, unresolved_contradictions, missing_external_validation, domain_boundary_unclear
