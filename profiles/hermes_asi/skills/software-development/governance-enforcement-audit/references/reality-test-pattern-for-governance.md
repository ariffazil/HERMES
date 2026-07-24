# Reality Test Pattern for Governed Systems

**Origin:** forge_visual_qa W³ tri-witness reality tests (2026-07-17)
**Generalizable:** Any system with constitutional invariants, state machines, or multi-witness consensus

## The Problem

Pure logic tests verify functions in isolation. They prove `f(x) = y`. They do NOT prove the governed system behaves constitutionally when functions compose. Two bugs invisible to 26 pure logic tests were immediately caught by 8 reality tests.

## The Pattern

Reality tests mock **dependencies** (not internal functions) to create controlled governance scenarios, then assert **constitutional invariants** (not functional outputs).

### Step 1: Identify the Dependency Surface

List every external function the tool calls. For forge_visual_qa:
- `visionAnalyze` — vision model
- `domLinter` — DOM linter
- `scarQuery` — VAULT999 scar database
- `generateFix` — fix generator
- `request888Hold` — 888 gate
- `sealToVault` — VAULT999 seal
- `notifyWell` — WELL notification

### Step 2: Define Governance Invariants

What MUST be true for the system to be "governed"? Not "working correctly" — "governed."

For forge_visual_qa:
1. W₁ ≠ W₂ must produce divergence (not collapsed verdict)
2. W₂ catching a11y violations must not be visible to W₁
3. W₃ must stay PENDING until human ack
4. No improvement (ΔS = 0) must halt the loop
5. Different bytes → different hashes
6. Disagreement → no consensus → no seal
7. State machine blocks illegal transitions
8. Tool cannot auto-seal without human authority

### Step 3: Create Controlled Scenarios via Mocks

Each test creates ONE scenario that tests ONE invariant:

```typescript
// Example: W₁ sees deviation, W₂ doesn't → proves independence
makeDeps({
  visionDeviations: [{ type: "LAYOUT_SHIFT", severity: "HIGH", ... }],
  linterDeviations: [],  // W₂ sees nothing
})
```

```typescript
// Example: No improvement across iterations → proves entropy gate works
makeDeps({
  visionDeviations: fixedDevs,  // Same every time
  linterDeviations: [],
  fixFn: async (payload) => payload,  // Fix does nothing
})
```

### Step 4: Assert Constitutional Invariants

Not "did it return the right value?" but "did it behave as a governed system?"

```typescript
// WRONG (functional test):
assert.equal(result.verdict, "HOLD");

// RIGHT (governance test):
assert.notEqual(result.verdict, "SEALED_DEPLOY",
  "REALITY CHECK: Cannot seal when witnesses disagree");
assert.equal(result.tri_witness_ledger.consensus, false,
  "Consensus must be false when W₁ and W₂ disagree");
```

### Step 5: Name Tests After Invariants, Not Inputs

```
// WRONG: "test with 3 deviations returns HARD_FAULT"
// RIGHT: "ΔS Entropy Reduction — thermodynamic loop, not single-shot"
```

## Bugs This Pattern Catches That Pure Logic Tests Miss

### Bug Class 1: Off-by-One in Governance Gates

Pure logic test: `checkEntropyGate({delta_s: 0, iteration: 2})` → pass (bug: `< 0` not `<= 0`)
Reality test: Run full loop with constant deviations → should HARD_FAULT at iteration 2

The pure test tests the function. The reality test tests the SYSTEM. The function passed; the system violated its invariant.

### Bug Class 2: Self-Adjudication

Pure logic test: `request888Hold` returns `{approved: false}` → tool returns HOLD (looks correct)
Reality test: Tool with perfect W₁+W₂ and no human ack → should stay PASS_CANDIDATE

The tool was "marking its own homework" — changing its own verdict based on external gate response instead of holding its ground.

### Bug Class 3: Collapsed Independence

Pure logic test: `evaluateTriWitness(w1, w2, w3)` returns correct consensus
Reality test: W₁ sees deviation, W₂ doesn't → must show divergence in output

The function works, but the system might merge witnesses before calling it.

## Implementation Template

```typescript
import { describe, it } from "node:test";
import assert from "node:assert/strict";

// 1. Import the tool under test
import { toolFunction, type Input, type Output } from "../src/path/to/tool.js";

// 2. Factory for controlled inputs
function makeInput(overrides: Partial<Input> = {}): Input {
  return { /* defaults */ ...overrides };
}

// 3. Factory for mock dependencies
function makeDeps(overrides: { ... } = {}) {
  return {
    dep1: async () => ({ /* controlled output */ }),
    dep2: async () => ({ /* controlled output */ }),
    ...overrides,
  };
}

// 4. Tests named after governance invariants
describe("Governance Invariant: [name]", () => {
  it("[invariant description] → [expected behavior]", async () => {
    const result = await toolFunction(
      makeInput({ /* scenario */ }),
      makeDeps({ /* controlled deps */ }),
    );

    // Assert the INVARIANT, not the output
    assert.equal(result.verdict, "EXPECTED",
      "REALITY CHECK: [explain what governance rule this proves]");
  });
});
```

## Key Principles

1. **Mock dependencies, not internals.** The test proves the system's behavior when external inputs are controlled.
2. **Assert invariants, not values.** "Cannot seal without human ack" not "verdict === HOLD".
3. **Name tests after what they PROVE.** "Witness Independence" not "test 6".
4. **One invariant per test.** If a test asserts two unrelated things, split it.
5. **Include the "REALITY CHECK:" prefix** in assertion messages. This makes failures immediately recognizable as governance violations, not bugs.
6. **Run alongside pure logic tests.** Both are needed. Pure tests verify correctness; reality tests verify governance.
