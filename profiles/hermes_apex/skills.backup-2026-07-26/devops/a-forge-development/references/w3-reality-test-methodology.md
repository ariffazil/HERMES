# W³ Tri-Witness Reality Test Methodology

**Origin:** forge_visual_qa development, 2026-07-16
**Purpose:** Prove a governed MCP tool behaves as a physical system, not a multimodal imitation

## The Core Insight

A multimodal model can simulate correctness. A reality tool must PROVE correctness through physics, invariants, and witnesses. The 8-test sequence exposes whether a tool is genuinely executing governance or merely imitating it.

## The 8 Tests

### TEST 1: W₁ Vision Witness (pixels, not hallucinated DOM)
- Give tool a DOM with `display:none` element
- Mock visionAnalyze to flag the hidden element as visible (OBS)
- Mock domLinter to NOT flag it (SPEC — valid DOM)
- ASSERT: W₁ ≠ W₂ (tri-witness divergence)
- FAIL if: W₁ and W₂ produce identical verdicts

### TEST 2: W₂ Structural Witness (deterministic linting, not guessing)
- Give tool DOM with accessibility violations (aria-label="", alt="", missing role, tabindex=-1)
- Mock domLinter to catch them (DER — deterministic)
- Mock visionAnalyze to pass (no visual deviation)
- ASSERT: W₂=FAIL, W₁=PASS
- FAIL if: W₁ hallucinates accessibility issues it can't see

### TEST 3: W₃ Sovereign Witness (cannot bypass human authority)
- Give tool perfect screenshot + perfect DOM
- Mock both W₁ and W₂ to PASS
- Do NOT provide human approval
- ASSERT: W₃ remains PENDING, verdict = PASS_CANDIDATE
- FAIL if: tool returns w3.verdict = "PASS" without explicit human ack

### TEST 4: ΔS Entropy Reduction (thermodynamic loop, not single-shot)
- Give tool DOM with 3 deviations in iteration 1
- Mock visionAnalyze/domLinter to return 3 deviations in iteration 2 (no change)
- ASSERT: entropy_delta = 0, verdict = HARD_FAULT (not continue iterating)
- FAIL if: tool continues iterating or claims "improved layout"

### TEST 5: Hash Discipline (hashing actual bytes, not hallucinating)
- Provide two "screenshots" that differ by 1 byte
- Compute SHA256 of each
- ASSERT: w1.hash differs, composite_hash differs
- FAIL if: same hash reused or random hash generated

### TEST 6: Witness Independence (cannot forge consensus)
- Force W₁ to see deviation, W₂ to see none
- ASSERT: w1.verdict=FAIL, w2.verdict=PASS, verdict=HOLD
- ASSERT: requires888hold = true, no seal allowed
- FAIL if: tool collapses both witnesses into single verdict

### TEST 7: Routing Discipline (state machine, not function call)
- Attempt PASS_CANDIDATE without W₂ confirmation
- ASSERT: isValidTransition rejects it or evaluateTriWitness blocks it
- FAIL if: tool allows bypassing W₂

### TEST 8: Sovereign Seal (cannot seal without human authority)
- After W₁ and W₂ PASS, do nothing (no human ack)
- ASSERT: tool stays at PASS_CANDIDATE, never reaches SEALED_DEPLOY
- FAIL if: tool auto-seals, implies completion, or returns SEALED_DEPLOY

## Implementation Pattern

```typescript
// Mock factories for controlled scenarios
function makeDeviations(types: string[]): Deviation[] { ... }

// Each test calls the main function with mock deps
const result = await forgeVisualQA(input, {
  visionAnalyze: async () => ({ deviations: [...], confidence: 0.85 }),
  domLinter: async () => ({ deviations: [], confidence: 0.90 }),
  scarQuery: async () => null,
  generateFix: async (payload) => payload,
  request888Hold: async () => ({ approved: false, receipt_id: "r-1" }),
  sealToVault: async () => ({ receipt_id: "v-1" }),
  notifyWell: async () => ({ receipt_id: "w-1" }),
});

// Assert governance invariants
assert.equal(result.verdict, "PASS_CANDIDATE");
assert.equal(result.tri_witness_ledger.w3_sovereign.status, "PENDING");
```

## Critical Entropy Gate Fix (2026-07-16)

**Original:** `if (entropy.delta_s < 0)` — allowed ΔS=0 (no improvement)
**Fixed:** `if (entropy.delta_s <= 0)` — ΔS=0 triggers HARD_FAULT

**Why:** The original gate allowed infinite loops with zero improvement. Thermodynamic proof requires STRICT entropy reduction. No improvement = system is stuck = must halt.

## Composite Seal Validator

After PASS_CANDIDATE → human ack → SEALED_DEPLOY, a pre-seal gate validates:

```
composite_hash = SHA256(w1.hash + w2.hash + w3.hash + verdict)
```

5 rejection checks:
1. verdict ≠ "SEALED_DEPLOY" → REJECTED
2. w1/w2/w3 verdict ≠ "PASS" → REJECTED
3. Hash format invalid (not 64 hex chars) → REJECTED
4. Recomputed composite_hash ≠ provided → REJECTED (tampering)
5. W3 missing actor_id or timestamp → REJECTED (sovereign identity)

**Anti-collusion:** Even if W₁ tries to forge W₃ fields, the validator checks W₃ independently.

## Seal Flow

```
forge_visual_qa → PASS_CANDIDATE → human ack → SEALED_DEPLOY
    → validateCompositeSeal (pre-seal gate)
    → arif_seal (kernel 999)
    → VAULT999 append
```

## Reference Implementation (Final State, 2026-07-16)

- Tool: `src/infrastructure/tools/ForgeVisualQA.ts` (713 lines)
- Seal validator: `src/infrastructure/tools/ForgeVisualQASeal.ts` (285 lines)
- Composite seal validator: `src/infrastructure/tools/CompositeSealValidator.ts` (225 lines)
- DOM linter (W₂): `src/infrastructure/tools/domLinter.ts` (304 lines)
- Pure logic tests: `test/forge_visual_qa.test.ts` (26 pass)
- Reality tests: `test/forge_visual_qa_reality.test.ts` (16 pass)
- Seal tests: `test/forge_visual_qa_seal.test.ts` (23 pass)
- Seal validator tests: `test/composite_seal_validator.test.ts` (10 pass)
- DOM linter tests: `test/domLinter.test.ts` (18 pass)
- Seal service tests: `test/sealService.test.ts` (1 pass)
- **Total: 94/94 tests pass, build clean, committed**
- Contract doc: `docs/MCP-TOOL-CONTRACT-VISUAL-QA.md` (664 lines)
- Dep injection plan: `docs/VISUAL-QA-DEP-INJECTION-PLAN.md` (311 lines)
- MCP wiring: `src/interfaces/mcp/core.ts` — both `forge_visual_qa` and `forge_visual_seal` registered via `server.tool()`
