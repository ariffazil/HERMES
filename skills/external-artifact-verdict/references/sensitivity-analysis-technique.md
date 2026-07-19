# Sensitivity Analysis Technique for Governed Controllers

> Reference for `external-artifact-verdict` skill — Phase 2 of post-verification workflow.

## When to Use

When an artifact contains magic numbers (coefficients, thresholds, weights) flagged as HYPOTHESIS during verification, and the sovereign wants them validated before promotion.

## Technique: Decision Boundary Mapping

### Step 1: Identify load-bearing parameters

Read the controller's decision function. For sigmoid-based controllers:
```
P(decision) = sigmoid(bias + w1*x1 + w2*x2 + ... + wn*xn)
```

The parameter with the highest `|w * x_typical|` product is most influential. But don't assume — measure.

### Step 2: Write a sweep script

Vary ONE parameter across its plausible range. Hold ALL other inputs at the bundled example's values. Record the output for each combination.

**Pitfall:** If internal functions (sigmoid, clamp) are not exported from the package, import from the module directly: `from module.model import sigmoid, clamp01`.

### Step 3: Map the decision boundary

For each combination of (param, input), record which MODE the controller outputs. Print as a cross-tabulation table.

### Step 4: Vary MULTIPLE inputs

Write a second script that varies 2-3 inputs simultaneously to find mode transitions. Use a "reasonable agent" baseline for fixed inputs — NOT the bundled example, which may be curated.

### Step 5: Document findings

Write `SENSITIVITY_ANALYSIS.md` alongside the artifact:
- Which parameter was actually load-bearing (often different from intuition)
- Where the decision boundary lies
- Dead zones (combinations where no mode triggers correctly)
- Calibration priorities for PROVISIONAL promotion

### Pitfalls

- **Assuming the obvious parameter matters.** In EUREKA-ZEN, the depletion coefficient (2.20) appeared important but was secondary to debt (2.60).
- **Dead zones.** Ranges where the controller falls to STEADY by default. May be intentional or design gap — flag it.
- **Bundled example extremes.** If the example uses extreme values, parameters look unimportant when they matter at moderate inputs. Test the full range.
- **Not running analysis at all.** A coefficient "calibrated to one example" is theatre. A coefficient validated across a grid with documented dead zones is evidence.
