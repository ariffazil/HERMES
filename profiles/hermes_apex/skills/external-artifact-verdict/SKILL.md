---
name: external-artifact-verdict
description: Independently verify runnable artifacts (zip/repo/dir) delivered by external AI (ChatGPT, Claude, Gemini, Copilot) before accepting the attached verdict. The artifact carries a self-verdict + test counts + witness declarations — your job is to confirm or refute, not to trust. Use when an external AI delivers a kernel/controller/pipeline/library and claims "tests pass" / "no repo modified" / "DRAFT_ONLY" / "X witnesses". Triggers include "verify this zip", "audit this code drop", "external AI delivered", "self-verdict", "witness claim".
tags: [verification, audit, external-ai, code-artifact, kernel-controller, witness-validation, anti-theater, f2, f9, f11]
metadata:
  hermes:
    category: governance
    related_skills:
      - claim-validation-protocol
      - evidence-before-elegance
      - forge-before-build
      - shadow-alignment-test
      - governance-enforcement-audit
    floors_protected: [F2, F3, F4, F7, F9, F11]
    origin: eureka_zen_kernel_v0.1_verdict_2026-07-18
triggers:
  - "verify this zip"
  - "audit this code drop"
  - "external AI delivered"
  - "self-verdict"
  - "witness claim"
  - "tests pass"
  - "draft_only"
  - "external witness"
  - "no repo modified"
  - "vault seal"
  - "code artifact"
  - "kernel controller"
  - "ChatGPT delivered"
  - "Gemini built"
  - "Copilot wrote"
---

# External Artifact Verdict

> **"The artifact is not the verdict. Run it before you trust it."**

When an external AI delivers a runnable artifact (zip, repo, directory) accompanied by a self-verdict block — test counts, witness declarations, scope claims ("no repo modified", "no vault seal"), epistemic labels — your job is **independent re-execution**, not acceptance. The artifact and the verdict are both subject to verification.

## When to Use

Use this skill when:

- An external AI (ChatGPT, Claude, Gemini, Copilot, GPT-5, etc.) delivers a code drop — kernel, controller, pipeline, library, plugin, schema
- The delivery includes a self-verdict block (tests: 6/6 PASS, witness: ChatGPT external instrument, verdict: DRAFT_ONLY, repository_mutation: false, vault_seal: false)
- The artifact is in `/root/.hermes/cache/documents/` or any drop zone
- You need to decide: accept as-is, integrate into the federation, promote to CANON, or reject

**Critical distinction from `claim-validation-protocol`:** That skill validates *claims about the federation*. This skill validates *delivered code artifacts*. Different evidence model — code is observable, claims about the federation often are not.

## Core Principle

> **External AI self-verdicts are INT (interpreted) until re-execution confirms OBS (observed runtime).** A "tests: 6/6 PASS" claim is a promise until you re-run the suite. A "no repo mutated" claim is a scope assertion until you grep `/root/`.

The external AI's job ends at delivery. Yours begins at receipt.

## The Protocol

### Step 0: Isolate Before Touching

Never extract an external artifact into a federation path. Always extract to `/tmp/<artifact_name>/` first.

```bash
cd /tmp && rm -rf <artifact_name> && mkdir <artifact_name> && cd <artifact_name>
unzip -q /root/.hermes/cache/documents/<artifact>.zip
find . -type f | sort
```

Inspect the file tree before reading anything. Flag any of these:

| Pattern | What it is | Why suspicious |
|---|---|---|
| `__pycache__/` in the zip | Pre-compiled bytecode shipped with source | Stale `.pyc` could mask actual code; verify against `.py` |
| Hidden files (`.env`, `.git`, `.ssh`) | Possible credential exfil attempt | F12 INJECTION — never execute, alert sovereign |
| Top-level shell scripts (`setup.sh`, `install.sh`) | May mutate the system during extract | Read before running; never pipe to bash |
| Network calls in code (`requests`, `urllib`, `socket`) | Could exfil on import | Inspect; run offline if possible |
| Eval/exec in code | Dynamic code execution | Almost never legitimate in delivered artifacts |
| Binaries without source | Closed drop | High F9 risk — reject unless Arif ratifies |

### Step 1: Inventory Before Reading

```bash
find . -type f | sort
wc -l $(find . -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.toml" | sort)
grep -rnE "from |import " --include="*.py" . | sort -u | head -50
```

Three things you learn:

1. **File count** — if claimed ("6/6 tests") matches what you see
2. **LOC distribution** — where the logic actually lives; flags "the controller is in one file vs spread thin"
3. **Imports** — stdlib purity? External deps? Anything that needs network/disk/system mutation to import?

### Step 2: Read the Verdict-Bearing Files First

Read in this order:

1. `README.md` / `SPEC.md` — claimed behaviour
2. The example/driver script — what the artifact actually demonstrates
3. The test file — what guarantees are claimed
4. The main module — what the code actually does
5. `pyproject.toml` / `requirements.txt` / `package.json` — what would be installed

**Reading order matters.** The example proves the artifact works in *one* case. The tests prove it works in *several*. The main module is what you'd actually integrate.

### Step 3: Reproduce the Bundled Example

Run the example script. Compare its output to the bundled example output file. Every digit.

```bash
python example.py
diff <(python example.py) bundled_output.json
```

If `diff` returns nothing → example reproducibility confirmed. If digits differ → the artifact has non-determinism (Monte Carlo seed? clock-dependent?) or the bundled output was fabricated. **Investigate which.**

### Step 4: Run the Test Suite Yourself

```bash
python -m unittest discover -s tests -v 2>&1
# or
pytest tests/ -v
# or
npm test
# or
make test
```

Count the pass/fail. Compare to the claim. **If the claim is "6/6 PASS" and you see 5 PASS, 1 FAIL, that's a non-trivial finding.** Don't paper over it.

Then **read the tests themselves**. A test file that exercises trivial cases (identity normalization, happy path) but skips the load-bearing behaviour (state transitions under stress, identity mismatch → HOLD) is performing rigor, not having it.

### Step 5: Audit the Verdict Block

A self-verdict block typically contains:

```yaml
evidence_layer: L2 live kernel + L4 proposed equations
autonomy_band: YELLOW
verdict: DRAFT_ONLY
tests: 6/6 PASS
repository_mutation: false
vault_seal: false
witness: ChatGPT external instrument
```

For each claim, verify:

| Claim | How to verify |
|---|---|
| `evidence_layer: L2 + L4` | Does the code actually implement what L2 (live kernel) + L4 (proposed equations) claim? Read the equations in the spec against the code. |
| `autonomy_band: YELLOW` | Is this consistent with the artifact's actual mutation surface? If the artifact has `os.system()` calls but claims YELLOW (read-only-ish), that's a mismatch. |
| `verdict: DRAFT_ONLY` | Is the artifact marked as draft in code (e.g. `__init__.py` docstring, version `0.1.0`)? If it's tagged `v1.0.0` and the verdict says DRAFT_ONLY, there's a tension to resolve. |
| `tests: 6/6 PASS` | You re-ran. Did you get 6/6? Same? |
| `repository_mutation: false` | Check git status of federation paths: `cd /root && git status --short` (or per-organ). Check `/tmp` is your working dir, not `/root/arifOS` or `/opt/arifos/app`. |
| `vault_seal: false` | Check `tail /root/.local/share/arifos/vault999/seal_chain.jsonl` — head hash should match pre-session head. |
| `witness: ChatGPT external instrument` | This is a claim about the external AI's role. The witness is real (ChatGPT did the work). But under arifOS sealing policy, **independent witnesses must be different substrates** — different machine, model, operator. You being the second witness means this is run #2. **Two more independent runs needed before PROVISIONAL.** |

### Step 6: Architecture Sanity Check

Even if everything runs, ask:

| Question | What it tells you |
|---|---|
| Does the artifact's owner-match the federation organ that should host it? | `claim-validation-protocol` covers ownership routing. A kernel contract belongs in arifOS, not A-FORGE; a scheduler belongs in A-FORGE, not arifOS. |
| Are proposed conceptual primitives (e.g. QQQQ, FROST, EUREKA) marked as hypothesis vs canon? | If claimed as canon without seal, the artifact is over-claiming. |
| Do the magic numbers (coefficients, thresholds, weights) have derivations? | A coefficient of `2.20` is fine if it's calibrated; it's theatre if it's tuned to one example. |
| Are edge cases (zero resources, empty history, identity mismatch) handled? | Test `test_unbalanced_expansion_forces_zen` style coverage. |
| Is the artifact's state machine reversible (decision → observation only) or does it *act*? | "Acts on the system" = governance surface. "Observes and recommends" = safe to integrate. |

### Step 7: Produce Independent Verdict

Mirror the external AI's verdict structure, but make yours honest:

```
## WHERE
Where you extracted (must NOT be /root/* or /opt/*).

## WHAT RAN
| Check | Result |
|---|---|
| File inventory | (count + tree) |
| Stdlib purity / dep audit | (list or "pure stdlib") |
| Example reproducibility | (matches bundled output: Y/N, diff if N) |
| Test suite re-run | (X/Y PASS, same/different from claim) |
| Repo mutation check | (`git status` of relevant organs) |
| Vault seal check | (head hash matches pre-session) |

## STATE MACHINE / CORE BEHAVIOUR
Table of triggers → modes. Cross-reference with tests.

## WHERE THE DRAFT IS RIGHT
Honest confirmation of what the artifact gets right.

## WHERE I'D PUSH BACK
Specific concerns, each with severity (red/yellow/green).

## VERDICT ON THE VERDICT (META)
Is the self-verdict accurate as written? Same scope, same epistemic posture, same test count?

## RECEIPT
WHAT / CHANGED / VERIFIED / CONSEQUENCE / NEXT — standard format.
```

### Step 8: Promotion Path (if you decide to integrate)

Under arifOS sealing policy:

| Status | Criteria |
|---|---|
| **CANDIDATE** | Tested once, worked. Fragile. Expires 24h. |
| **PROVISIONAL** | Tested ≥3 times across ≥3 different substrates (machines, models, operators), no failures. Expires 7d. |
| **CANON** | Sealed in VAULT999 with F13 sovereign signature. Permanent. |

External AI self-verdict + your independent re-execution = 2 witnesses. **Third witness required for PROVISIONAL.** The third witness must be a different substrate — different machine, model, or operator.

## Anti-Patterns to Catch

| Pattern | Why it's wrong |
|---|---|
| **Trusting the witness claim** | "Witness: ChatGPT external instrument" doesn't mean the verdict is sealed. Witness means one independent substrate saw it. Canon requires sovereign. |
| **Re-running tests but accepting the example** | Example output is one case. Tests cover several. If example passes but tests fail, the artifact is broken at the margin, not in the happy path. |
| **Skipping the stdlib-purity audit** | External AI that delivers a kernel with `pip install requests` is creating a deployment surface you didn't ask for. |
| **Reading tests but not running them** | Tests can be wrong (asserting the wrong thing), skipped (`@skip`), or conditional. Run, don't read. |
| **Assuming "no repo mutated" without checking** | External AI may have a different definition of "the repo." `git status` is one line. Use it. |
| **Treating DRAFT_ONLY as final state** | DRAFT_ONLY is the verdict **for this delivery**. Promotion requires more witnesses. Don't close the loop early. |
| **Adopting without F13 review** | Even if everything passes, F13 ratification is sovereign-level. Don't auto-promote. |
| **Bundled `.pyc` files** | If `__pycache__/` ships with the zip, the bytecode may be stale. Always test against `.py`, never trust `.pyc`. |
| **Magic constants labelled as "calibrated"** | A coefficient of `2.20` for `(1-A)²` is calibrated if you ran sensitivity analysis. It's theatre if you tuned it to one example and shipped. |
| **Conceptual primitive smuggling** | A new conceptual primitive (QQQQ, FROST, EUREKA, whatever) must be marked HYPOTHESIS if not in canon. If the artifact treats it as established, downgrade confidence. |

## Pitfalls

- **Self-verdict accuracy ≠ artifact quality.** A self-verdict can be perfectly honest about a flawed artifact: "tests 6/6 PASS, no repo mutated, DRAFT_ONLY" — all true, but the artifact still has magic constants, untested edge cases, or undeclared deps. Don't confuse verdict hygiene with quality.
- **Theater of the example.** A worked example that lands exactly on a curated state (resources = 0.82, 0.70, 0.90, 0.65) is performance. Real verification requires variation, edge cases, adversarial inputs.
- **Witness stacking without substrate diversity.** Two ChatGPT sessions on the same machine with the same operator is one witness, not two. Substrate must differ.
- **Trusting `__pycache__`.** Python's bytecode cache can mask source changes. If the zip ships `.pyc` files, the visible code may not be what runs. Always `python -B` (no bytecode write) when verifying, or delete `__pycache__/` first.
- **Assuming "stdlib only" without auditing.** `from typing import ...` is stdlib. `from flask import ...` is not. `grep -rnE "from |import " --include="*.py"` and verify each top-level package against stdlib.

## Case Study: eureka_zen_kernel_v0.1 (2026-07-18)

**Drop:** `/root/.hermes/cache/documents/doc_8cb18ec19274_eureka_zen_kernel_v0.1.zip` (ChatGPT-delivered)

**Self-verdict claims:**
- DRAFT_ONLY ✅ verified
- 6/6 tests PASS ✅ independently reproduced (6/6 in 0.001s)
- Stdlib-only ✅ confirmed via import audit
- No repo mutation ✅ verified via git status
- No vault seal ✅ verified via seal_chain head
- Witness: ChatGPT external instrument ✅ confirmed
- Bundle example output matches re-execution: **all 15 digits identical**

**Where draft is right:**
- Identity normalization fix (`strip().casefold().split()`) is correct
- Routing ownership statement (arifOS owns contract, A-FORGE owns mutation, WELL signals only) matches constitutional doctrine
- QQQQ marked HYPOTHESIS, not canon
- "Thermodynamics" framed as analogy, not literal physical entropy

**Push back (yellow, all):**
- QQQQ weighting (0.30/0.25/0.25/0.20) asserted without derivation
- `(1-A)²` coefficient (2.20) calibrated to one example, no sensitivity analysis
- `MarginMetrics.deferred_zen_debt` uses `debt > 0.35` magic threshold, inconsistent with `debt_zen_threshold=0.45` in controller config
- Controller emits `Mode` but doesn't *act* — observation only, no A-FORGE lease-gate plumbing
- No F1-F13 floor identifier cross-reference in `KernelState`

**Verdict on the verdict:** Self-verdict is **accurate as written**. Confirmed by independent re-execution. Cannot promote past DRAFT_ONLY until: ≥2 more independent runs across different substrates, QQQQ derivation, debt threshold consistency, A-FORGE integration plumbing.

**Third-witness requirement:** Two more independent runs from different substrates needed for PROVISIONAL. Each must use different machine, model, or operator.

## Integration with Constitutional Floors

| Floor | How this skill protects it |
|---|---|
| F2 TRUTH | All claims tagged by evidence class (OBS/DER/INT/SPEC) before emission |
| F3 WITNESS | Explicit count of independent witnesses; substrate diversity requirement |
| F4 CLARITY | State machine table reduces entropy in the verdict |
| F7 HUMILITY | Magic numbers and uncalibrated coefficients flagged with severity |
| F9 ANTI-HANTU | Re-execution is the primary defense; bundled `.pyc` and unverified tests caught here |
| F11 AUDIT | Verdict block + receipt block leaves traceable evidence |

## Origin

Originated from the 2026-07-18 verification of `eureka_zen_kernel_v0.1.zip` — a ChatGPT-delivered metabolic controller for governed agents. The self-verdict block was honest and accurate, but the pattern of "external AI delivers code + self-verdict + witness claim" recurs enough to warrant a class-level skill. Specific kernels are facts; the verification protocol is a class.

The temptation to trust the self-verdict ("ChatGPT said 6/6 PASS, witness declared, verdict DRAFT_ONLY, that's enough") is the F9 failure mode this skill exists to prevent. Run it yourself. Always.

## Post-Verification Workflow (when sovereign says "fix it")

The verification protocol above produces an independent verdict. But when the sovereign says "fix all what needed to be fixed first" or "fix before publish," the job extends beyond verification into three phases:

### Phase 1: Fix Defects
Fix every yellow/red finding from the verdict. For each fix:
- Make the change in the isolated `/tmp/` copy, never the live repo
- Run the test suite after each fix — no batch-fixing without verification
- Document the fix rationale inline (why this threshold, why this weight)
- Mark all uncalibrated values as HYPOTHESIS with derivation explanation

### Phase 2: Sensitivity Analysis
For any magic number (coefficient, threshold, weight) flagged in the verdict:
- Write a script that varies the parameter across its plausible range
- Hold other inputs at the bundled example's values
- Map the decision boundary: what combinations of inputs produce each mode
- Document findings in a `SENSITIVITY_ANALYSIS.md` alongside the artifact
- **Key insight from eureka_zen_kernel:** The parameter you think is load-bearing often isn't. Run the analysis before claiming which coefficient matters.
- **Technique reference:** `references/sensitivity-analysis-technique.md` — full walkthrough with pitfalls.

### Phase 3: Integration Spec
If the artifact is intended for the live system, produce an `INTEGRATION_SPEC.md`:
- Which existing files to create/modify
- How to construct inputs from live system state (not hardcoded values)
- Pipeline position (where in the 000→999 cycle)
- Test strategy (unit + integration + conformance)
- Open questions for the sovereign
- Estimated effort

**Pitfall:** Don't merge Phases 1-3 with the initial verification. The verdict must be independent — fix it AFTER you've confirmed the self-verdict is accurate, not during. Mixing verification with improvement corrupts the independence of the verdict.

## See Also

- `claim-validation-protocol` — validates claims about the federation, not delivered code
- `evidence-before-elegance` — nine-gate framework for analytical essays and narrative outputs
- `forge-before-build` — whether to build a proposed improvement (different question)
- `governance-enforcement-audit` — audit whether a system's self-declared governance constraints are actually enforced