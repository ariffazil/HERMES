---
name: paper-to-code-validation
description: "Validate that a research paper's equations and claims are properly implemented in code, tested, and numerically verified. The 'close the loop' pattern: read paper → extract equations → search codebase → map to implementations → check test coverage → identify gaps → propose what to build. Use when Arif asks 'is this embedded in our code', 'does this match the paper', 'close the loop', 'validate the equations', or shares a .tex/.pdf and asks if the theory is implemented."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [paper, validation, equations, code-mapping, testing, geoscience, research, verification]
    category: software-development
    related_skills: [external-artifact-verdict, submission-readiness-audit, geoscience-artifact-rigor, scientific-manuscript-forge, geox-federation-mcp-driver]
    floors_protected: [F2, F7, F9, F11]
    origin: 2026-07-18 AVO paper → GEOX validation session
---

# Paper-to-Code Validation

> **"The equation on paper is a CLAIM. The equation in code is a CLAIM. Only the test with known inputs and expected outputs is OBS."**

When a research paper (your own or external) makes mathematical claims, and those claims should be implemented in a codebase, this skill closes the loop: paper → code → tests → numerical verification.

## When to use

- Arif asks: "Is this embedded in our code?" / "Does this match the paper?" / "Close the loop" / "Validate the equations"
- Arif shares a .tex or .pdf and asks if the theory is implemented
- A paper was just compiled and needs to be checked against existing implementation
- OpenCode/Codex is being spawned to "embed the equations and test"
- A new algorithm or derivation needs to be verified against its reference implementation

**Do NOT use when:**
- The paper has no code implementation (use `submission-readiness-audit` instead)
- The artifact is a code drop from external AI (use `external-artifact-verdict`)
- The question is about paper quality, not code mapping (use the reference checklist in `submission-readiness-audit/references/research-paper-quality-checklist.md`)

## The 5-Phase Protocol

### Phase 1: Extract — What does the paper claim?

Read the .tex source (preferred) or PDF. Extract:

1. **Core equations** — every numbered equation with a name or role
2. **Decomposition tables** — any side-by-side comparison (e.g., six-stage decomposition)
3. **Assumptions** — every "Assumption A1/A2/A3..." block (these define the validity boundary)
4. **Claims** — every "We show..." / "We derive..." / "We prove..." statement
5. **References to prior work** — what the paper builds on (this tells you what might already exist)

Output format:
```
| # | Equation | Paper Line | Role |
|---|----------|------------|------|
| 1 | R(θ) ≈ A + B sin²θ | L76 | Shuey approximation |
| 2 | ΔB = B_obs - B_bg(A_obs) | L87 | AVO anomaly measure |
| 3 | ΔF = B - mA - c | L94 | Fluid factor |
```

### Phase 2: Map — Where does it live in code?

For each equation/claim from Phase 1:

1. **Search the codebase** — `grep -rn "equation_name\|symbol\|formula_fragment" --include="*.py" --include="*.ts"`
2. **Check the MCP tool surface** — does a tool implement this? (e.g., `geox_seismic_compute` mode=`anomalous_contrast`)
3. **Check internal tools** — some implementations are internal, not public-facing
4. **Map the function** — which function/class implements which equation?

Output format:
```
| Paper Equation | Code File | Function | Status |
|---|---|---|---|
| ΔF = B - mA - c | anomalous_contrast.py:134 | _compute_attention_residual() | ✅ Implemented |
| δ_i = e_i - ē | anomalous_contrast.py:107 | _compute_attention_residual() | ✅ Implemented |
| ACRisk baseline | — | — | ❌ Not built |
```

### Phase 3: Test — Do tests verify the math?

For each mapped equation:

1. **Find existing tests** — `grep -rn "def test_" tests/ | grep -i "equation_name\|function_name"`
2. **Check test quality** — do tests verify numerical correctness, or just structure?
3. **Identify gaps** — equations without tests, or tests that only check key-exists-not-value

**Three levels of test quality:**

| Level | What it checks | Example |
|---|---|---|
| **Structural** | Output has expected keys, correct types | `assert "delta_f" in result` |
| **Behavioral** | Output is in correct range, monotonic, bounded | `assert 0 <= softmax_alpha <= 1` |
| **Numerical (golden)** | Exact value matches hand-calculated reference | `assert result["delta_f"] == pytest.approx(-0.14, abs=1e-6)` |

**Rule:** Structural tests are necessary but not sufficient. A paper's equations need at least behavioral tests. Golden tests (numerical regression) are the gold standard for closing the loop.

### Phase 4: Gap Analysis — What's missing?

Classify gaps:

| Gap Type | Severity | Action |
|---|---|---|
| Equation not implemented | **T1 — MUST FIX** | The paper claims something the code doesn't do |
| Equation implemented, no test | **T1 — MUST FIX** | Implementation could be wrong; no way to know |
| Test is structural only | **T2 — SHOULD FIX** | Implementation exists but isn't numerically verified |
| Paper references concept, code has partial impl | **T2 — SHOULD FIX** | Needs completion or honest scoping |
| Paper's assumptions don't match code's usage | **T1 — MUST FIX** | Silent validity boundary violation |
| Cross-domain bridge (paper maps A→B, code only has A) | **T3 — NICE TO HAVE** | The novel contribution may not be implemented yet |

### Phase 5: Validate — Run the numbers

For critical equations, compute golden test values by hand:

```python
# Example: ΔF = B - mA - c
A_obs = 0.05
B_obs = -0.08
m = 1.2
c = 0.02
delta_F = B_obs - m * A_obs - c  # = -0.08 - 0.06 - 0.02 = -0.16

# Then in the test:
assert compute_fluid_factor(A_obs, B_obs, m, c) == pytest.approx(-0.16, abs=1e-10)
```

**Every golden test must include:**
1. Input values (explicit, not computed)
2. Expected output (hand-calculated)
3. Tolerance (abs=1e-6 for floats, exact for integers)
4. Source reference (paper equation number + page)

## Spawning OpenCode/Codex for This Task

When spawning a coding agent to "close the loop":

**DO include:**
- The paper's .tex source (not PDF — agents can't read PDFs well)
- The exact file paths to the existing implementation
- The exact file paths to existing tests
- The specific equations that need golden tests
- The paper's assumptions (A1, A2, A3) — these define validity boundaries

**DO NOT include:**
- The full paper as context (too large; extract the equations instead)
- Vague instructions like "validate everything" (specify which equations)
- Instructions to "write a new tool" when the implementation already exists

**Template prompt for spawning:**
```
Read the paper at [PATH].tex. The core equations are [EQUATION LIST].
The existing implementations are at [CODE PATHS].
The existing tests are at [TEST PATHS].

For each equation:
1. Verify the code implements it correctly
2. Add golden tests with hand-calculated expected values
3. Run the test suite and confirm all pass
4. Report: which equations have golden tests, which don't, what's missing

Do NOT write new tools. Focus on testing existing implementations.
```

## Pitfalls

1. **Don't trust "the code looks right."** The code matching the paper's LaTeX is a structural match, not a numerical match. Only running with known inputs/outputs verifies correctness.

2. **Don't skip the assumptions.** If the paper says "under assumption A1 (linear background)" and the code uses a nonlinear model, the equivalence doesn't hold at runtime even if the equation matches symbolically.

3. **Don't confuse "tests pass" with "equations verified."** Tests can pass with wrong expected values. Golden tests must be hand-calculated from the paper's equations, not from the code's output.

4. **Don't implement what's already there.** Phase 2 (Map) exists precisely to prevent rebuilding existing functionality. Always search before building.

5. **Don't treat the paper's "future work" as gaps.** If the paper says "empirical validation is needed" and the code doesn't have it, that's a known limitation, not a bug. Distinguish "not yet done" from "should be done."

6. **The six-stage decomposition is a thinking tool, not always an implementation target.** Some papers decompose a concept into stages for clarity. The code may implement the whole pipeline without explicit stage boundaries. That's fine — don't force artificial separation.

## Case Study: AVO-Attention Bridge (2026-07-18)

**Paper:** "Contrast-Governed Anomaly Detection: A Formal Bridge between Seismic AVO and Transformer Attention" (Essay #11)

**What existed:**
- `anomalous_contrast.py` (731 lines) — full AVO-attention bridge
- `contrast_detect.py` (839 lines) — contrast detection
- 4 test files (1825 lines), 40 tests passing
- Code referenced Essay #13 extensively but not Essay #11

**What the mapping revealed:**
- All 6 stages of the paper's decomposition were implemented
- The core equation (ΔF ↔ δ_i) was in the code header comment
- Tests were behavioral (range checks) not numerical (golden values)
- ACRisk governance framework was proposed in the paper but not implemented as a tool

**What OpenCode was asked to do:**
- Add golden tests with hand-calculated expected values
- Verify the six-stage decomposition maps to code
- Add cross-domain verification test (same input → AVO pipeline AND attention pipeline → verify structural equivalence)

**Lesson:** The implementation was far deeper than expected. The "close the loop" turned out to be "add numerical regression tests to existing deep implementation" — not "build the implementation from scratch."

## See Also

- `external-artifact-verdict` — for verifying code artifacts from external AI (different question)
- `submission-readiness-audit` — for deadline-driven gap analysis (different framing)
- `geoscience-artifact-rigor` — for geological artifact quality (domain-specific)
- `scientific-manuscript-forge` — for producing the paper itself (upstream)
