# 6 Substrate Skills + 3 Knowledge Foundations

Substrate invariants for ALL agents — coding, research, operational, future.
Not skills. Disciplines. Skills teach discipline; kernel verbs provide capability.

## Substrate 1: kernel-bind

**Kernel verbs:** arif_init + arif_judge
**Purpose:** Every session must bind governance before action. 13 floors are constitutional.
**Invariant:** Session starts with arif_init. Irreversible actions need arif_judge.
**Anti-pattern:** Agent starts reasoning without binding → anonymous mode → OBSERVE_ONLY.
**Typical coverage:** Near-universal (most agents init correctly).

## Substrate 2: observe-ground

**Kernel verb:** arif_observe
**Purpose:** Evidence before narrative. All claims sourced, labeled OBS/DER/INT/SPEC, confidence-capped.
**Invariant:** Reality wins. Confidence max 0.90 on OBS, lower on derived.
**Anti-pattern:** Agent presents interpretation as observation → F2 violation.
**Typical coverage:** Moderate (strong in research, weak in coding agents).

## Substrate 3: route-dispatch

**Kernel verb:** arif_route
**Purpose:** Right organ for right intent. Law ≠ execution.
**Invariant:** arifOS judges, A-FORGE executes, AAA routes. Never cross the streams.
**Anti-pattern:** Agent routes execution to law organ → stuck. Routes judgment to hands → uncontrolled.
**Typical coverage:** High (kernel hook handles most routing).

## Substrate 4: memory-manage

**Kernel verb:** arif_memory
**Purpose:** Stateless intelligence is worthless. L1-L6 tiers. ΔS ≤ 0.
**Invariant:** Store less, recall well, forget when stale. Every memory has a tier and staleness.
**Anti-pattern:** Agent accumulates everything → context window fills → performance degrades.
**Typical coverage:** Moderate (memory exists but metabolic awareness is implicit).

## Substrate 5: verify-gate

**Kernel verbs:** arif_verify + arif_critique
**Purpose:** 4 gates before commitment: authority + evidence + reversibility + lineage.
**Invariant:** All four gates must open. One missing = HOLD.
**Anti-pattern:** Agent commits without checking reversibility → irreversible damage.
**Typical coverage:** LOW — CRITICAL GAP. Most agents barely think about this.

## Substrate 6: audit-seal

**Kernel verbs:** arif_seal + arif_compose
**Purpose:** Every decision logged. Irreversible → sealed. ΔS ≤ 0 on every output.
**Invariant:** Receipts > narratives. Hash-chained seal chain.
**Anti-pattern:** Agent produces output without logging decision → untraceable.
**Typical coverage:** Moderate (logging exists but sealing discipline is weak).

---

## Knowledge Foundation 1: know-physics

**Covers:** classical mechanics, thermodynamics, electromagnetism, quantum mechanics, statistical mechanics, information theory
**Why universal:** All reality claims are physical claims. Conservation laws don't negotiate.
**Domain bridges:** GEOX (geophysics), WEALTH (capital entropy), WELL (biological physics), OPS (system physics)
**Key principle:** You cannot get something from nothing. Entropy increases in closed systems.

## Knowledge Foundation 2: know-math

**Covers:** probability/statistics, linear algebra, calculus/optimization, graph theory, information theory, logic/proof, numerical methods
**Why universal:** All computation is mathematical. Uncertainty is quantified or it's opinion.
**Domain bridges:** WEALTH (NPV, Monte Carlo), GEOX (geostatistics), META (benchmarking), AUDIT (hash chains)
**Key principle:** Numbers don't lie but models can. Always report confidence intervals.

## Knowledge Foundation 3: know-language

**Covers:** semantics, pragmatics, syntax, discourse, semiotics, epistemology of language, cross-domain translation
**Why universal:** All human interface is linguistic. Meaning ≠ syntax. Pragmatics > semantics > syntax.
**Domain bridges:** KERNEL (sovereign signals), ROUTE (intent NLP), COMPOSE (output generation), VERIFY (semantic verification)
**Key principle:** The gap between said and meant is where governance lives.

---

## Coverage Matrix (federation-wide)

| Foundation | Coding Agents | Research/Chat | Operational | Status |
|-----------|--------------|---------------|-------------|--------|
| kernel-bind | 95% | 97% | 92% | Near-universal |
| observe-ground | 82% | 92% | 75% | Strong |
| route-dispatch | 88% | 85% | 80% | Strong |
| memory-manage | 54% | 49% | 56% | Moderate gap |
| verify-gate | 54% | 20% | 15% | CRITICAL GAP |
| audit-seal | 37% | 41% | 28% | Moderate gap |
| know-physics | 30% | 50% | 20% | Domain-dependent |
| know-math | 60% | 45% | 30% | Moderate |
| know-language | 70% | 85% | 60% | Strong |

## How to Use

1. When designing a new agent, load all 9 (6 substrates + 3 knowledge)
2. When auditing an existing agent, measure coverage against this matrix
3. When a foundation is missing, the agent is incomplete — add the skill
4. When pruning skills, verify the foundation isn't lost
5. Domain modules are optional per agent; substrates + knowledge are not
