# Institutional Intelligence Research Framework

Proven: 2026-07-20 — Arif asked "what makes an institution intelligent for civilization, what's the literature said?" across Ostrom, North, Sanchez Borboa, Mnemoria, MultiA, ContextGraph, Dalio, mapped back to AAA.

## When to Use

- User asks about institutional design, institutional intelligence, governance theory, or what makes institutions survive vs collapse
- User wants literature synthesis on governance/civilizational questions
- User asks to map external governance frameworks to AAA/arifOS architecture
- "What does the literature say about [institutional/governance/civilizational X]?"

## The Six-Tradition Research Spine

Always cover these research traditions when the question is about institutional/governance theory. Not all are needed for every question. Prioritize by relevance:

### 1. Ostrom's Core Design Principles (CDPs) — Empirical Gold Standard

**Source:** Elinor Ostrom, "Governing the Commons" (1990), Nobel Prize 2009
**Strength:** Validated across thousands of communities worldwide
**The 8 CDPs:**

| CDP | Principle | Civilization-Scale Meaning |
|-----|-----------|---------------------------|
| 1 | Clearly defined boundaries | Who is in the institution? Who is outside? |
| 2 | Proportional equivalence | Cost-bearers must share in benefits. Extraction ≠ institution. |
| 3 | Collective-choice arenas | Those affected by rules participate in modifying them |
| 4 | Monitoring | Continuous observation, not annual audit |
| 5 | Graduated sanctions | Proportional consequences, not zero-tolerance / zero-consequence |
| 6 | Conflict-resolution mechanisms | Fast, fair, accessible. Delay = compound harm |
| 7 | Minimal recognition of right to organize | Local autonomy. Central authority can't micromanage everything |
| 8 | Polycentric governance | Nested layers: local → regional → civilizational |

**Search corner:** Hound smart_search for "Ostrom design principles polycentric governance", fetch from ostromworkshop.indiana.edu (official) and sanchezborboa.com (first-principles derivation).

### 2. North's Institutional Economics — Credible Commitment

**Source:** Douglass North, "Institutions, Institutional Change and Economic Performance" (1990), "Violence and Social Orders" (2009, with Wallis & Weingast)
**Key concepts:**
- Institutions = "rules of the game"; organizations = "players"
- Credible commitment = the state can't arbitrarily change rules after investment
- Natural state (limited access) vs Open access order
- Path dependence: institutions persist even when inefficient
- Formal (legal) vs informal (norms) constraints

**Search corner:** "Douglass North institutions credible commitment", "Violence and Social Orders natural state"

### 3. Sanchez Borboa's Ethical Geometry — First-Principles Derivation

**Source:** Sanchez Borboa, "From Ethical Geometry to Institutional Design" (sanchezborboa.com)
**Key contribution:** Derives Ostrom's 8 CDPs from ethical first principles (syntegrity = Good × Right × Virtue mutually reinforcing). This is the Newton-to-Kepler derivation — explains WHY the CDPs must hold, not just that they do.

**CDP structural hierarchy (from derivation):**
- CDPs 1-3: Ensure the field is well-defined and positively coupled (conditions for syntegrity's existence)
- CDPs 4-6: Prevent perturbations from triggering vicious spirals (protect stability)
- CDPs 7-8: Allow syntegrity to be sustained across levels (enable scaling)

**Search corner:** Hound smart_search for "Ostrom design principles derivation ethical geometry", fetch sanchezborboa.com/deriving-ostroms-cdps

### 4. Mnemoria Civilization Systems Model — Five-Level Learning

**Source:** mnemoria.org/system-properties/adaptation
**Key insight:** Institutions that survive span 5 nested learning levels:

| Level | What Learns | Timescale |
|-------|------------|-----------|
| 1. Individual Cognitive | One mind | Seconds–years |
| 2. Collective Intelligence | Distributed knowledge sharing | Months–decades |
| 3. Organizational Routines | Encoded practices that survive turnover | Years–centuries |
| 4. Institutional Codification | Formal rules, standards, policies | Decades–centuries |
| 5. Cultural Worldview | Fundamental values, epistemic frameworks | Centuries–millennia |

**Search corner:** Hound smart_fetch https://mnemoria.org/system-properties/adaptation

### 5. Organizational Intelligence — ContextGraph & MultiA

**ContextGraph** (contextgraph.tech/learn/institutional-intelligence): Institutional intelligence = compounding organizational decision knowledge. Four capabilities: Auditability, Consistency, Reusability, Evolution.

**MultiA** (multia.ai): "Institutions accumulate civilization. A conversation forgets. An institution remembers."

### 6. Ray Dalio's Principles — The Practitioner's Lens

**Source:** Dalio's published principles, social media output
**Key concepts:** Radical truth + radical transparency, meaningful work + meaningful relationships, 1+1=3 teamwork, tough love, "play jazz"

**Search corner:** Hound smart_search for "Ray Dalio principles institutional", smart_fetch his X/Threads output for recent posts. See also `references/public-figure-social-scan.md` for platform-specific extraction.

## WEALTH Organ Integration

When the question involves institutional analysis, always attempt WEALTH organ calls alongside literature:

1. **`capital_diagnose(mode="stress_index")`** — institutional stress scoring across financial/governance/workforce/legal/exploitation dimensions
2. **`capital_entropy(mode="power_consequence_map")`** — maps decision-maker incentives, benefit concentration, and consequence gaps
3. **`capital_wisdom(mode="wisdom")`** — 6-dimension wisdom scoring (dignity, sovereignty, resilience, inequality, ecological, optionality)

**Pitfall:** WEALTH now requires `session_id`. Always run `arif_init(mode="init")` first and pass the session token. If WEALTH returns SESSION_REQUIRED, you missed this step.

**Pitfall:** WEALTH wisdom may return all-neutral (0.45-0.55) when proposal text is abstract/theoretical — treat as UNCLEAR not balanced. This happened 2026-07-20: civilizational-scale institutional analysis returned 6/6 neutral dimensions because the proposal text was too general.

## The Crosswalk Mapping Technique

After synthesizing the literature, always build a crosswalk table mapping each framework's principles to the user's system architecture:

```
| Literature Requirement | System Implementation | Verdict |
|------------------------|----------------------|---------|
| Ostrom CDP 1 (boundaries) | F1 AMANAH, session tokens | ✅ PRESENT |
| North credible commitment | arifOS kernel, immutable floors | ✅ PRESENT |
| Polycentric governance | 7 organs, nested session model | ✅ PRESENT |
| Monitoring (CDP 4) | Health probes, RSI | ⚠️ REACTIVE, not predictive |
```

Score each cell: ✅ PRESENT / ⚠️ GAP / ❌ MISSING / 🔄 EMERGING

## The Six Properties of an Intelligent Institution (Synthesis Template)

After cross-referencing all traditions, synthesize down to the properties that converge across traditions:

1. **Memory Over Intelligence** — Institutions remember what individuals forget
2. **Separation of Powers** — Judge ≠ Execute ≠ Observe
3. **Feedback Loops at Every Level** — Reinforcing + balancing
4. **Immutable Audit Trail** — Can't learn from history you can't verify
5. **Built-in Challenge Mechanism** — If it can't say "this might be wrong," it's a cult
6. **Proportional Equivalence** — Cost-bearers must share benefits

## Pitfalls

- **Tavily (web_search/web_extract) may fail (432/402).** Use Hound MCP (`mcp__hound__mcp_smart_search` + `mcp__hound__mcp_smart_fetch`) as first choice for research-grade web queries. Hound has better recall, neural reranking, and cross-engine consensus signals.
- **Don't stop at one tradition.** The value of this research class is the convergence across independent frameworks. A single-source answer misses the structural convergence.
- **Always do the crosswalk back to the user's system.** Research without application is trivia. The crosswalk table is where research becomes actionable.
- **WEALTH tools need session context.** Run arif_init first.
- **Don't skip the counter-narrative.** Every synthesis should include "What's Missing" — explicit gaps, traditions you couldn't cover, and what would strengthen the analysis.
