---
name: external-wisdom-integration
description: "Scan external thinkers (X, Threads, articles, podcasts), extract governance principles, evaluate kernel-worthiness, draft constitutional amendments, and assess whether changes need kernel code or just governance docs. The full pipeline from 'someone said something interesting' to 'should this be law?' Use when Arif shares a link to an external thinker, asks to scan someone's social media for ideas, says 'anything worth it for the kernel?', or asks whether a proposed governance change needs code updates."
version: 1.1.0
author: Hermes Agent
tags: [governance, constitution, external-thinkers, kernel, amendments, social-media]
triggers:
  - "anything worth it for the kernel"
  - "scan X/Threads for ideas"
  - "should this be law"
  - "does this need kernel code"
  - "evaluate this for the constitution"
  - "external thinker integration"
  - "governance from external source"
---

# External Wisdom Integration

The full pipeline from external content to constitutional action. Not just research — this is about deciding whether someone else's insight should become arifOS law.

## When to Use

- Arif shares a link to an external thinker (Dalio, Taleb, etc.) and asks "anything for the kernel?"
- Arif asks to scan someone's social media for governance insights
- A proposed principle needs evaluation against existing floors
- Need to determine whether a governance change requires kernel code or just docs

## When NOT to Use

- Simple news/current events → `news-research-briefing`
- Deep research on a topic → `deep-research`
- Propagating an already-decided doctrine → `federation-doctrine-propagation`
- Someone shares an article and just wants a summary → `summarize-pro`

## The Pipeline

### Phase 1: Scan

Multi-platform source gathering. Use `web_search` + `web_extract` + `xurl` for X.

**MANDATORY FIRST ACTION when Arif sends a URL:** Fetch and read the URL content before forming any hypothesis about what the URL means or what Arif wants. URL slugs are designed for human browser-tab scanning — not for agent planning. The URL IS the source material.

```bash
# 1. Fetch the page (HTML or markdown, 3 commands, ~10 seconds)
curl -sL -A "Mozilla/5.0" -m 20 "https://[url]" | sed -n '1,300p' | head -150

# 2. Targeted search for the verb in Arif's message
curl -sL "https://[url]" | grep -i -A 8 "the-verb-keyword\|provider\|install\|export\|set "
```

**Scar (2026-07-19, DeepSeek BYOK session):** Arif sent `https://api-docs.deepseek.com/quick_start/agent_integrations/copilot_cli` with a wiring request. Agent pattern-matched on "copilot_cli" slug for two rounds, gave wrong answers about how Copilot CLI doesn't accept custom models, until Arif asked "Do u even read this??". Fetching the URL revealed a 4-step install + env-var recipe that was the actual instruction set. The reflex should have been `curl` first.

**Pattern for social media scanning** (when no URL provided, just a topic):
1. Search for the person's X profile: `web_search("[Name] site:x.com")`
2. Search for their Threads: `web_search("[Name] site:threads.com")`
3. Search for recent articles/interviews: `web_search("[Name] [topic] 2025 2026")`
4. Extract 3-5 most relevant sources with `web_extract`
5. For X posts: extract directly from `x.com/[handle]/status/[id]` URLs

**Key rule:** Tag every finding with OBS/DER/INT/SPEC. Social media posts are OBS. Article interpretations are INT. Your synthesis is DER.

**Reverse trap:** If Arun/iya already wired a URL into the message, do NOT additionally search for the same topic via web_search. The URL is the authoritative source. Search would re-discover what you should have read.

### Phase 2: Extract Themes

From the raw content, identify the **unified message** across platforms. People often say different things on X (macro/alarm) vs Threads (philosophy/personal). Both matter.

Structure output as:

| Theme | Platform | Evidence Class | Key Quote |
|---|---|---|---|
| ... | X/Threads/Article | OBS/INT | "..." |

### Phase 3: Map to Existing Floors

For each theme, check: does arifOS already have this?

| Theme | Existing Floor? | Gap? |
|---|---|---|
| "Governance is oversight" | F1 AMANAH (partial) | Missing "community over individual" |
| "Raise confidence before acting" | F8 GENIUS (G ≥ 0.80) | Missing enforcement mechanism |
| "Dynamic escalation" | Autonomy Tiers (static) | No system-state awareness |

### Phase 4: Evaluate — The "So What?" Test

This is where most proposals die. Apply ruthlessly:

| Criterion | Question | Kill If |
|---|---|---|
| **Enforceability** | Can this be measured or gated mechanically? | No — it's just better words |
| **Gap fill** | Does this close a real blind spot in current governance? | Already covered by existing floors |
| **Code vs docs** | Does this need kernel code, or just AGENTS.md? | Docs-only = nice-to-have, not critical |
| **Contradiction** | Does this conflict with existing floors? | Yes — resolve before integrating |
| **Source quality** | Is this from lived experience or armchair philosophy? | Armchair — observe but don't codify |

**Three verdicts:**
- **KERNEL-WORTHY** → needs code change, fills real gap, mechanically enforceable
- **DOC-WORTHY** → good philosophy, strengthens existing floors, no code needed
- **OBSERVE-ONLY** → interesting but not actionable, note for future reference

### Phase 5: Draft Amendments (if warranted)

For KERNEL-WORTHY items:
1. Show current floor text
2. Show proposed addition (append, not replace)
3. Specify which file changes (`arif_kernel_intercept.py`, `DECISION_THRESHOLDS`, `AGENTS.md`)
4. Estimate effort (lines of code, files touched)

For DOC-WORTHY items:
1. Show the governance doc update
2. No code changes needed

### Phase 6: Assess Implementation Impact

**Kernel code check** — inspect the actual enforcement points:

| What to Check | File | What You're Looking For |
|---|---|---|
| Intercept gates | `arifosmcp/tools/arif_kernel_intercept.py` | Does `epistemic_state` get checked against thresholds? What gates exist? |
| KernelOutput schema | `arifosmcp/schemas/minimum_kernel.py` | What decision types are in the `Literal`? Does the new gate need a new type? |
| Decision thresholds | `arifosmcp/runtime/tools.py` → `DECISION_THRESHOLDS` | Are they enforced or advisory? |
| Autonomy bands | `arifosmcp/envelope/__init__.py` → `AutonomyBand` | Static or dynamic? |
| Intercept tests | `tests/runtime/test_kernel_intercept.py` | What test patterns exist? Will the new gate break existing tests? |

**Rule of thumb:**
- If the insight is a **threshold** (confidence < X → do Y) → likely needs kernel code
- If the insight is a **definition** (X means Y) → governance doc is enough
- If the insight is a **process** (when A happens, escalate to B) → check if existing tools can express it before adding code

## Pitfalls

- **URL slugs are not the spec.** When Arif sends a URL with a directive, `curl` the URL FIRST before forming any routing hypothesis. The slug ("copilot_cli", "fix_X") is for human bookmarking, not for agent planning. The page itself is the source. (See `evidence-before-elegance` Gate 12 for full protocol + scar case study 2026-07-19.)

- **Don't codify everything that sounds wise.** Most external wisdom is OBSERVE-ONLY. The "so what?" test exists for a reason.
- **Don't confuse philosophy with enforcement.** "Community over individual" is beautiful. "If confidence < 0.80 and irreversible, auto-SABAR" is enforceable. The kernel needs the second kind.
- **Don't skip the code inspection.** Always check whether the kernel already has the mechanism before proposing new code. `DECISION_THRESHOLDS` existed but was advisory-only — that's the kind of gap that matters.
- **Don't replace existing floor text.** Always append. The original floor was ratified for a reason.
- **Don't forget to check contradictions.** A new principle that conflicts with F1-F13 is worse than no principle at all.
- **Social media content is OBS, not authority.** A Threads post is data, not doctrine. It becomes doctrine only after F13 ratification.
- **Don't overclaim system maturity.** When mapping external insights to existing arifOS capabilities, score each as LIVE / PARTIAL / NOT BUILT — not just "we have that." Arif's "U sure???" challenge (2026-07-12) forced a rescore from "5/7 built" to "1/7 fully live, 5 partial, 1 missing." The lesson: enthusiasm inflates maturity. Discipline deflates it. Always present the honest score, especially when the synthesis is exciting. A capability that exists as a principle in AGENTS.md but has no code enforcement is PARTIAL, not LIVE.

### Phase 7: Delegate Implementation (if kernel code needed)

When Phase 6 confirms kernel code changes are needed, delegate to a coding agent (OpenCode/Claude Code) with **full architectural context**. Don't just say "implement X" — give the agent everything it needs.

**Context brief must include:**
1. Exact file paths with line numbers for insertion points
2. The existing gate order (so the agent doesn't break sequencing)
3. The enum values involved (TruthState, ReversibilityClass, etc.)
4. The code pattern to follow (copy the style of adjacent gates)
5. Test file path + test patterns to follow
6. How to run tests (`cd /opt/arifos && python -m pytest tests/runtime/test_kernel_intercept.py -v`)
7. Explicit constraints: "Do NOT modify existing tests", "Do NOT change gate order"
8. **Schema-first rule:** If the new gate returns a decision type not in `KernelOutput.decision` Literal, the schema MUST be updated FIRST. Tell the agent: "Update `minimum_kernel.py` Literal BEFORE adding the gate."

**Pitfall: Don't forget schema changes.** If the new gate returns a decision type not in the current `KernelOutput.decision` Literal (e.g., SABAR), the schema MUST be updated first. The agent needs to know this. **Order: schema → gate → tests.**

- **Don't skip the code inspection.** Always read the actual files yourself before writing the delegation context. Guessing at file structure leads to wrong insertion points.
- **Don't run full test suites on large repos without timeout.** The arifOS test suite times out at 300s. Always find relevant test files first (`grep -rl "genius\|calculate_genius" tests/`) and run targeted. Full suite is for CI, not for agent verification.
- **Don't assume the mechanism is missing just because the doc is.** The kernel already enforced G ≥ 0.80 as a threshold — the gap was *signaling* (probe vs act), not *gating*. Always inspect code before proposing changes.
- **New gates in `arif_kernel_intercept.py` WILL break existing tests.** Any test that uses `epistemic_state` default (UNKNOWN) with R4/R5 will now hit the 17x gate. After adding a new gate, run the full test file (`pytest tests/runtime/test_kernel_intercept.py -v`), identify broken tests, and decide: (a) the breakage is correct behaviour → update the test to set explicit `epistemic_state`, or (b) the breakage is wrong → fix the gate logic. Never leave a broken test without understanding WHY it broke.
- **Sovereignty ≠ epistemic immunity.** Authority tokens (F13) grant PERMISSION. Epistemic state grants CONFIDENCE. They are orthogonal. A valid sovereign token on an UNKNOWN-epistemic R5 action should SABAR, not ALLOW. If a test assumes otherwise, the test is wrong — update it to set `epistemic_state="FACT"` + evidence.

## Proven

### 2026-07-12 Session 1: Ray Dalio Scan → F8 Amendment (Design + Docs)

**Input:** Arif: "scan dalio x or threads. Do full reflection." → "anything worth it for the kernel?"

**Phase 1-2 (Scan + Extract):** 3 parallel search batches (X/Twitter, Threads, articles) → extracted key X posts ("on the brink" video, July 4th reflection, budget bill analysis, capital war warnings) + Threads governance principles + Fortune/CNBC/Bloomberg coverage.

**Phase 3 (Map):** 6 Dalio concepts mapped against F1-F13:

| Dalio Concept | arifOS Coverage | Verdict |
|---|---|---|
| Pain + Reflection = Progress | ✅ Already in scar epistemology | OBSERVE-ONLY |
| Believability-weighted decisions | ⚠️ Partial (F7 caps confidence, no track-record weighting) | KERNEL-WORTHY (future) |
| Radical transparency | ✅ Already in F11 + seal chain | OBSERVE-ONLY |
| Forcing binary choices | ⚠️ Partial (SABAR as escape hatch) | DOC-WORTHY |
| Capital war / money-as-weapon | ❌ Missing (WEALTH has no adversarial model) | KERNEL-WORTHY (WEALTH domain, not kernel) |
| **17x Principle** | ❌ Missing (F8 has threshold but no probe-vs-act signal) | **KERNEL-WORTHY** |

**Phase 4 (Honest Assessment):** Arif demanded "Why is this better?" — forced ranking. Key insight: the 17x math (51%→85% = 17× more EV than 49%→51%) gives F8 a *decision engine* instead of just a quality bar.

| Amendment | Verdict | Why |
|---|---|---|
| F8 17x Rule | **KERNEL-WORTHY** | Mechanical enforcement. Turns F8 from guideline into gate. |
| Believability weighting | KERNEL-WORTHY (future) | Needs track-record data not yet available. |
| Big Cycle awareness | DOC-WORTHY | Governance doc sufficient. Existing entropy signals express it. |

**Phase 5 (Draft Amendments):** Applied F8 upgrade — proposed new gate 2d in `arif_kernel_intercept.py` + `SABAR` in `KernelOutput.decision` + `DECISION_THRESHOLDS` update.

**Phase 6 (Kernel Code Assessment):** Inspected `arifosmcp/tools/arif_kernel_intercept.py` — discovered `epistemic_state` was accepted as input but NEVER checked against `DECISION_THRESHOLDS`. Confidence was decorative. Also checked `arifosmcp/schemas/minimum_kernel.py` — `SABAR` was NOT in the `KernelOutput.decision` Literal. Both changes needed.

**Phase 7 (Delegate → Complete):** Spawned OpenCode with precise spec. **IMPLEMENTED AND VERIFIED.** 26/26 tests pass.

### 2026-07-12 Session 2: F8 17x Kernel Implementation (Code)

**Input:** Arif: "Yes spawn opencode to update the code kernel arifOS"

**Files changed:**
1. `arifosmcp/schemas/minimum_kernel.py` — Added `"SABAR"` to `KernelOutput.decision` Literal
2. `arifosmcp/tools/arif_kernel_intercept.py` — New gate **2d** (17x RULE / F8 GENIUS) between step 2c and step 3
3. `arifosmcp/runtime/tools.py` — Added `"irreversible_below_0_80"` entry to `DECISION_THRESHOLDS`
4. `tests/runtime/test_kernel_intercept.py` — 7 new tests (TestF8_17xRule class)

**Gate logic (2d):**
```python
if t_state in {TruthState.HYPOTHESIS, TruthState.CLAIM, TruthState.UNKNOWN}
   and r_class in {ReversibilityClass.R4_IRREVERSIBLE, ReversibilityClass.R5_SOVEREIGN}:
    → decision="SABAR", floor="F8", reason="17x RULE..."
```

**Critical design insight — Sovereignty ≠ Epistemic immunity:**
The 17x gate fires AFTER the F13 sovereign gate (step 1). This means:
- No sovereign token + R4/R5 → ESCALATE (F13 catches first)
- Sovereign token + UNKNOWN/HYPOTHESIS/CLAIM + R4/R5 → **SABAR** (17x catches)
- Sovereign token + FACT + evidence + R4/R5 → ALLOW

Authority grants permission. Epistemic state grants confidence. They are orthogonal.

**Test breakage (expected):** `test_r5_with_correct_sentinel_allows` broke because it used default `epistemic_state=UNKNOWN` with R5 + sovereign token. Fix: add `epistemic_state="FACT"` + evidence. The breakage was CORRECT behaviour — even sovereign should SABAR on unknown-epistemic irreversible actions.

**Verification:** 26/26 tests pass. No existing tests modified (except the one that needed updating for the new gate's correct behaviour).

**Lessons:**
- **Adding a new gate to `arif_kernel_intercept.py` will break existing tests** that don't specify the new gate's input parameters (especially `epistemic_state`). The default `UNKNOWN` triggers the 17x gate for R4/R5 actions. Always check existing tests for implicit defaults after adding a new gate.
- **Schema change MUST precede gate change.** Adding `SABAR` to `KernelOutput.decision` Literal was required before the gate could return `decision="SABAR"`. Order: schema → gate → tests.
- **Arif's "Ok" = sovereign ack for constitutional changes.** Don't ask for confirmation after. Execute.
- **When Arif says "Why is this better?" he wants the MATH, not the philosophy.** Lead with expected value, not principles. The 17x EV calculation was what convinced him.
- **OpenCode delegation worked best with:** exact file paths, line numbers, existing code patterns to follow, "keep existing X unchanged" constraints, and explicit test commands. Vague specs → vague results.
- **Honest assessment matters.** Arif demanded "Why is this better?" and I had to admit F1 AMANAH text was "nice-to-have, not critical" while F8 17x was "do this." Don't oversell all proposals equally.
- **When Arif says "U sure???" he's testing your honesty, not your knowledge.** During the Dalio session, I claimed "5 of 7 insights are already built" — Arif challenged with "U sure???" and I had to rescore to 1/7 fully live, 5 partial, 1 missing. The lesson: after presenting a synthesis, explicitly score each claim as LIVE/PARTIAL/NOT BUILT. Don't let enthusiasm inflate maturity. The F7 Humility floor applies to your own system's status, not just external claims.
- **After architectural analysis, build the measurement spine first, not all features.** The Eureka session produced 7 insights and a spec for all 7. Arif said "Ok do it" and I built ONE thing: the governed work ledger (WorkBudget + BudgetLedger + TaskReceipt + WorkEvent). That's the correct move — the ledger is the substrate that makes all 7 measurable. Don't try to build 7 features from a 7-insight document. Build the one substrate they all need.
- **When Arif shares a series of related architecture documents, analyze them as a group.** The Eureka session produced 3 documents (Eureka 7-insight, Memory Architecture, Memory Enigma). Each was 0.85-0.90 on insight but had the same structural weakness: excellent diagnosis, underspecified treatment. The pattern across all three was: "scarce resource is not X, it's judgment about X." This through-line only emerges when you read them together. Don't analyze each document in isolation — find the unifying thesis.
- **Verify agent deliveries before celebrating.** When another agent (OpenCode, Claude Code) claims to have built N files with M lines, verify: (1) `wc -l` on each file, (2) `npm run build` / `python -m pytest` for compilation, (3) targeted test execution, (4) spot-check key functions exist (e.g., `isGodelLocked`, `computePromotionScore`). The A-FORGE delivery verification revealed 3912 actual lines vs 4101 claimed (95%) — close enough but not exact. Never report "delivered" without checking.
- **"U sure???" means rescore, don't defend.** When Arif challenges a maturity assessment, the correct response is to rescore each claim as LIVE/PARTIAL/NOT BUILT — not to defend the original score. After "U sure???", I rescored from "5 of 7 built" to "1/7 fully live, 5 partial, 1 missing." The rescoring was more honest and Arif accepted it immediately.

### 2026-07-12 Session 3: Eureka Architecture → P0 Measurement Spine

**Input:** Arif shared a 7-part synthesis ("The industry's deepest discovery is that the model is not the intelligence system") mapping neuroscience, economics, and physics to arifOS architecture.

**Phase 1-2 (Scan + Extract):** This was Arif's own synthesis, not an external thinker. 7 insights: (1) active compute > stored params, (2) context > model, (3) memory for prediction, (4) world models, (5) verification > generation, (6) multi-agent = coordination, (7) physical limits.

**Phase 3 (Map):** Honest rescore after Arif challenged "5 of 7 built":

| Insight | Honest Status |
|---|---|
| Reasoning budget | ❌ Not built |
| Context governance | ⚠️ Rudimentary (static Heptalogy) |
| Predictive memory | ⚠️ Partial (VAULT999 exists, no future-value scoring) |
| World models | ✅ Live (GEOX OBS/DER/INT/SPEC) |
| Verification > generation | ⚠️ Principle exists, not measured |
| Coordination | ⚠️ Architecture exists, cost not measured |
| Physical limits | ⚠️ WELL exists, energy routing doesn't |

**True score: 1/7 fully live. 5 partial. 1 missing.**

**Phase 4 (So What?):** All 7 gaps reduce to ONE missing substrate: a governed work ledger. Build that first, then 6 of 7 become measurable.

**Phase 5-7 (Implement):** Built P0 Measurement Spine — `WorkBudget`, `BudgetLedger`, `TaskReceipt`, `WorkEvent` schemas + 29 tests. Files: `schemas/work_budget.py`, `schemas/budget_ledger.py`, `schemas/work_event_schema.py`, `tests/runtime/test_work_budget.py`. All 55 tests pass (26 kernel intercept + 29 work budget).

**Lesson: The "build the receipt first" pattern.** When faced with N architectural gaps, don't build N features. Build ONE measurement substrate (the ledger) that makes all N gaps visible. The first deliverable is one honest task receipt showing exactly what was spent and what was verified.

### 2026-07-12 Session 4: Memory Architecture → Gödel Lock Design

**Input:** Arif shared a memory architecture document (5 generations of agentic memory, 7 memory paradoxes, industry maturity assessment). Key insight: "Memory may automatically reduce authority. Memory may not automatically increase authority."

**Phase 3 (Map):** 5 separations that most systems collapse:

| Question | Most Systems | arifOS Should |
|---|---|---|
| Is this remembered? | Vector search | L1-L6 + VAULT999 |
| Is it believed? | Embedding similarity | OBS/DER/INT/SPEC |
| Is it verified? | Not checked | F3 WITNESS |
| Is it relevant? | Semantic similarity | Decision-value scoring |
| Is it authorized? | Not distinguished | Kernel floor check |

**Phase 4 (So What?):** The Gödel Lock (memories cannot self-certify) was identified as the key architectural contribution. Trust Bootstrap Paradox: memory needs external authority (F1-F13) to certify itself. arifOS has that authority — but memory isn't connected to it yet.

**Verdict:** KERNEL-WORTHY for the Gödel lock (asymmetric authority rule). DOC-WORTHY for the 5 separations and 7 paradoxes. Implementation deferred to post-P0 measurement spine.

**Lesson: Build measurement before features.** The governed memory system needs the measurement spine (WorkBudget + TaskReceipt) to exist first — that's what tracks whether a memory actually improved a decision. Without the ledger, memory value is vibes-based.

## Related Skills

- `deep-research` — upstream: multi-source research methodology
- `federation-doctrine-propagation` — downstream: propagating ratified doctrines across agents
- `claim-validation-protocol` — parallel: validating external claims against live system state

## References

- `references/kernel-enforcement-architecture.md` — MCP intercept layer (arif_kernel_intercept.py gate order, DECISION_THRESHOLDS, AutonomyBand, KernelOutput schema with SABAR)
- `references/genius-enforcement-architecture.md` — Genius scoring layer (genius.py, calculate_genius, 17x probe signals, CognitionResult)
- `references/godel-lock-memory-design.md` — Gödel lock memory architecture (truth classes, authority levels, 7 paradoxes, 5 generations)
- `references/multi-document-architecture-critique.md` — Pattern for analyzing multiple related architecture documents as a group
- `references/opencode-delegation-pitfalls.md` — OpenCode fabrication detection, kernel gate testing, sovereignty ≠ epistemic immunity (2026-07-12)
