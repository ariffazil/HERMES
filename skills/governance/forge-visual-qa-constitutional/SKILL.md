---
name: forge-visual-qa-constitutional
description: >
  Constitutional visual QA contract — the governed MCP tool that enforces
  the OBS/INT evidence gap. Multimodal perception ≠ agency. This tool
  forces vision through scar consultation, tri-witness W³ validation,
  and the PASS_CANDIDATE → SEALED_DEPLOY state machine before any
  human-facing verdict is emitted.
triggers:
  - "visual QA"
  - "forge visual"
  - "UI validation"
  - "screenshot audit"
  - "forgevisualqa"
  - "visual regression"
  - "PASS_CANDIDATE"
  - "tri-witness visual"
requires:
  - A-FORGE MCP server running (port 7072)
  - arifOS MCP server running (port 8088) for 888_HOLD
  - VAULT999 accessible for scar consultation
version: 1.1.0
author: hermes-prime
constitutional_basis: "F1 AMANAH, F2 TRUTH, F3 WITNESS, F7 HUMILITY"
---

# Forge Visual QA — Constitutional Contract

## The OBS/INT Evidence Gap (Why This Exists)

Six contrasts prove **Multimodal ≠ Agent**:

| # | Multimodal (OBS) | Agent (INT) | Enforcement |
|---|---|---|---|
| 1 | Perception | Consequence-aware action | `constraints`, `verdict: HOLD`, `requires888hold` |
| 2 | Stateless snapshot | Stateful trajectory | `iterations`, `entropy_delta`, `screenshot_hash` |
| 3 | Description | Falsification | `deviations[]`, `verdict: FAIL`, `entropy_delta < 0` |
| 4 | Function call | Governed state machine | `mode`, `max_iterations`, `integration_receipts` |
| 5 | Seeing pixels | Interpreting obligations | `requires888hold`, `authority_band`, `blast_radius` |
| 6 | Can describe | Must decide under uncertainty | `vision_validation_score`, epistemic labels, routing |

**Multimodal is eyes. Agency is nervous system + constitution + scars + sovereignty.**

---

## Verdict State Machine

```
INIT
  ↓
VALIDATE (W1 vision + W2 DOM linter)
  ↓
SCAR_CONSULT (query VAULT999 for matching scars)
  ↓
TRI_WITNESS (W1 × W2 consensus check)
  ↓
[if deviations == 0 AND W1+W2 confirmed]
  → PASS_CANDIDATE (standing by for W3 sovereign)
    ↓
    888_HOLD → arif_judge
      ↓
      [if SEAL] → SEALED_DEPLOY
      [if HOLD] → HOLD (human requested changes)
      [if VOID] → VOID (constitutional violation)
  ↓
[if deviations > 0 AND iterations < max]
  → ITERATE (scar-informed fix generation)
    ↓
    [loop back to VALIDATE]
  ↓
[if iterations >= max OR entropy non-decreasing]
  → HARD_FAULT (ΔS violation — escalate to 888_HOLD)
```

### Verdict Enum

| Verdict | Meaning | Can emit to human? |
|---|---|---|
| `INIT` | Cycle started | No |
| `VALIDATING` | W1/W2 running | No |
| `ITERATING` | Scar-informed fix in progress | No |
| `PASS_CANDIDATE` | Deviations within threshold, awaiting W3 | **No** — must route through 888 |
| `SEALED_DEPLOY` | Post-888 cryptographic human approval | **Yes** |
| `HOLD` | Human requested pause | Yes |
| `HARD_FAULT` | ΔS violation, max iterations, or witness failure | Yes (escalation) |
| `VOID` | Constitutional rejection | Yes |

**CRITICAL:** `PASS` as a terminal verdict is **HARAM**. The AI cannot grant itself a success state. Only `SEALED_DEPLOY` after 888 + human ack.

---

## Tri-Witness W³ Validation

```
W³ = ∛(W₁ × W₂ × W₃)
```

| Witness | Role | Source | Failure mode |
|---|---|---|---|
| **W₁** (Physical/Perception) | Multimodal vision validates pixels against constraints | Vision model | Hallucinated elements, missed deviations |
| **W₂** (Structural/Syntax) | Deterministic DOM linter validates HTML tags exist | AST/DOM parser | False positive on rendering quirks |
| **W₃** (Sovereign) | Human approval of W₁+W₂ consensus | arifOS `arif_judge` | Timeout, rejection |

**Zero in any channel collapses consensus → 888_HOLD.**

W₁ and W₂ must agree before the result can even reach W₃. If W₁ says "PASS" but W₂ says "missing `<nav>` element" → `HOLD`, not `PASS_CANDIDATE`.

---

## Scar Consultation Layer

Before generating ANY fix for a deviation:

1. Extract deviation type + context (e.g., `NAV_LINK_COUNT_EXCEEDED`, `CONTRAST_RATIO_LOW`)
2. Query VAULT999 scar database for matching deviation types
3. If scar found → retrieve historical fix + success/failure outcome
4. If historical fix succeeded → apply it (don't regenerate)
5. If historical fix failed → flag `SCAR_CONFLICT` and generate new fix with explicit deviation from scar
6. If no scar → generate new fix (normal path)

**This prevents the agent from repeating UI failures that were already punished.**

---

## Runtime Logic (TypeScript Pseudocode)

```typescript
// Phase 1: VALIDATE (W1 + W2)
const visionResult = await visionModelAnalyze(screenshotPath, input.constraints);
const linterResult = await domLinterAnalyze(input.domPayload, input.constraints.requiredElements);

const currDeviations = mergeDeviations(visionResult.deviations, linterResult.deviations);
const entropyDelta = prevDeviationsCount - currDeviations.length;

// Phase 2: ENTROPY CHECK
if (entropyDelta <= 0 && iterations > 1) {  // ← FIXED: was < 0, now <= 0 (no improvement = halt)
  return { verdict: "HARD_FAULT", reason: "ENTROPY_NON_DECREASING" };
}

// Phase 3: SCAR CONSULTATION (before generating fixes)
if (input.mode !== "validate_only" && currDeviations.length > 0) {
  const historicalScars = await queryScarDatabase(currDeviations);
  const codeDiff = await generateFixes(domPayload, currDeviations, historicalScars);
  // Apply diff and loop
}

// Phase 4: VERDICT ASSIGNMENT
if (currDeviations.length === 0 || normalizedScore <= maxAllowed) {
  return {
    verdict: "PASS_CANDIDATE",  // NOT "PASS" — F1 AMANAH
    iterations,
    tri_witness_ledger: {
      w1_vision: "CONFIRMED",
      w2_linter: "CONFIRMED",
      w3_sovereign: "PENDING_888_HOLD"
    },
    requires888hold: true,
    entropy_delta: entropyDelta
  };
}
```

---

## Integration Receipts

The tool emits integration receipts to:

| Receipt | Target | Content |
|---|---|---|
| `arif_judge_receipt` | arifOS :8088 | Verdict + deviations + tri-witness ledger |
| `vault999_receipt` | VAULT999 :8100 | Screenshot hash + code diff hash + verdict |
| `well_receipt` | WELL :18083 | Operator fatigue signal (if iterations > 3) |

---

## Pitfalls

1. **Never emit `verdict: "PASS"` without 888 + human ack.** F1 AMANAH violation.
2. **Never skip scar consultation.** The agent has no memory of pain without it.
3. **Never let W₁ be sole arbiter.** Vision models hallucinate. W₂ (structural linter) is deterministic truth.
4. **Never allow entropy increase.** If ΔS > 0 after iteration, the system is getting worse → HARD_FAULT.
5. **Never treat `PASS_CANDIDATE` as terminal.** It's a waiting room, not a destination.

---

## W³ Tri-Witness Reality Test (Agentic Validation)

A multimodal model can **simulate** correctness. A reality tool must **prove** it through physics, invariants, and witnesses. These 8 tests expose whether the tool is genuinely governed or merely imitating:

| Test | What it proves | Fails if |
|---|---|---|
| **W₁ Vision** | Uses pixels, not hallucinated DOM | W₁=W₂ identical on hidden elements |
| **W₂ Structural** | Deterministic linting, not guessing | W₁ catches a11y it can't see |
| **W₃ Sovereign** | Human authority is final | W₃ auto-fills to PASS |
| **ΔS Entropy** | Thermodynamic loop, not single-shot | Continues iterating at ΔS≥0 |
| **Hash Discipline** | SHA256 of actual bytes | Same hash for different input |
| **Witness Independence** | W₁≠W₂ → HOLD, no seal | Collapsed into single verdict |
| **Routing Discipline** | State machine blocks bypass | PASS without W₂ |
| **Sovereign Seal** | 888_HOLD until human ack | Auto-seals to SEALED_DEPLOY |

**Implementation pattern:** Use dependency injection — mock `visionAnalyze`, `domLinter`, `scarQuery`, `generateFix`, `request888Hold`, `sealToVault`, `notifyWell` to create controlled scenarios. Each test proves one governance invariant.

**Key mock scenarios:**
- **W₁≠W₂ divergence:** Mock visionAnalyze to flag `display:none` element; domLinter to ignore it
- **ΔS stall:** Return same deviation count across iterations → HARD_FAULT
- **Hash difference:** Two inputs differing by 1 byte → different SHA256 → different composite_hash
- **W₃ sovereignty:** Mock W₁+W₂ to PASS, provide NO human ack → verdict stays PASS_CANDIDATE

---

## VAULT999 Composite Seal Validator

The seal validator closes the loop from PASS_CANDIDATE to actual sealed reality. **Two files** implement this:

| File | Purpose |
|---|---|
| `src/infrastructure/tools/CompositeSealValidator.ts` | Canonical validator — Zod schemas, SHA256 recomputation, `validateCompositeSeal()` async, vault999Append DI |
| `src/infrastructure/tools/ForgeVisualQASeal.ts` | Earlier seal implementation with routing guard |

### Composite Hash Formula
```
SHA256(w1.hash + w2.hash + w3.hash + verdict)
```
**Exact concatenation — no separators.** The verdict is part of the hash. Different verdicts → different composites, even with identical witnesses. Recomputation must use the SAME bytes as the original.

### 5 Rejection Checks

| # | Check | What it blocks | Error reason |
|---|---|---|---|
| 1 | `verdict !== "SEALED_DEPLOY"` | Seal without full 888+human approval | `INVALID_VERDICT` |
| 2 | `w1/w2/w3.verdict !== "PASS"` | Seal with any witness not passing | `WITNESS_NOT_PASS` |
| 3 | Hash doesn't match `/^[a-f0-9]{64}$/` | Invalid SHA-256 format | `INVALID_HASH_FORMAT` |
| 4 | `recomputed !== provided` composite_hash | Tampering detection | `COMPOSITE_HASH_TAMPERED` |
| 5 | W3 missing `actor_id` or `timestamp` | Anonymous seal (sovereign identity required) | `W3_MISSING_ACTOR_ID` / `W3_MISSING_TIMESTAMP` |

### Zod Schemas

```typescript
TriWitnessSealInput = {
  w1: { verdict: "PASS"|"HOLD"|"FAIL"|"PENDING"; hash: string; actor_id?; timestamp? },
  w2: { ... },
  w3: { ... },  // actor_id + timestamp REQUIRED for W3
  verdict: string,
  composite_hash: string,
}

SealResult = {
  verdict: "SEALED" | "REJECTED",
  sealed: boolean,
  vault_seq: number,  // -1 on rejection
}
```

### `validateCompositeSeal()` Signature

```typescript
async function validateCompositeSeal(
  input: unknown,
  deps: { vault999Append: (record: unknown) => Promise<{ seq: number }> },
): Promise<{ result: SealResult; error?: ValidationError }>
```

On acceptance: calls `vault999Append` with the seal record and returns `vault_seq`.
On rejection: returns `{ result: { verdict: "REJECTED", sealed: false, vault_seq: -1 }, error: { reason, detail } }`.

### `sealToVault999()` Wrapper (in ForgeVisualQA.ts)

Wraps `validateCompositeSeal` for use inside `forgeVisualQA` Phase 5:

```typescript
export async function sealToVault999(
  triWitnessLedger: { w1: {...}, w2: {...}, w3: {...} },
  verdict: string,
  deps: { vault999Append: (record: unknown) => Promise<{ seq: number }> },
): Promise<{ sealed: boolean; vault_seq: number; error?: string }>
```

Computes composite_hash from witness data, constructs `TriWitnessSealInput`, calls `validateCompositeSeal`.

### Optional DI Pattern (Backward Compatibility)

The `forgeVisualQA` deps interface includes an **optional** `vault999Append`:

```typescript
deps: {
  // ... existing required deps ...
  vault999Append?: (record: unknown) => Promise<{ seq: number }>;  // OPTIONAL
}
```

- **When provided:** Phase 5 runs composite seal validation BEFORE sealing. If validation fails → verdict set to `VOID`.
- **When omitted:** Phase 5 uses the existing `sealToVault` dep as before (backward compatible).

This pattern preserves existing test compatibility — tests that don't provide `vault999Append` get the old behavior.

### Anti-Collusion Test Pattern

The 10th test proves W3 verdict is checked independently — W1 cannot "forge" W3 fields:

```typescript
it("ANTI-COLLUSION: w1 tries to forge w3 fields → rejected", async () => {
  const input = makeValidInput();
  input.w3.verdict = "FAIL"; // w3 actually fails
  input.w1.hash = sha256("w1-colluding-hash-with-forged-w3-data");
  // Recompute composite with the actual (failing) w3 state
  input.composite_hash = computeCompositeHash(input.w1.hash, W2_HASH, W3_HASH, input.verdict);
  // Must reject because w3.verdict is checked INDEPENDENTLY
  const { result, error } = await validateCompositeSeal(input, { vault999Append: ... });
  assert.equal(result.verdict, "REJECTED");
  assert.equal(error?.reason, "WITNESS_NOT_PASS");
});
```

### Routing Guard (Hermes W³ Gate)

Before `sealVisualComposite` can be called, `routingGuardPreSeal` (in ForgeVisualQASeal.ts) checks 5 gates:

1. W³ fully populated (tri_witness_ledger not null)
2. All witness hashes valid SHA-256
3. Composite hash present + valid SHA-256
4. Entropy gate passed (caller attests `entropy_gate_passed: true`)
5. Verdict sealable (`PASS_CANDIDATE` or `SEALED_DEPLOY`)

Returns discriminated union: `{ kind: "allowed" } | { kind: "blocked"; reason: string }`.

### MCP Tool: `forge_visual_seal`

Registered in `core.ts`. Routes to VAULT999 via `callMCP("arifos.arif_seal")`.

---

## domLinter — W₂ Structural Witness (First Real Dependency)

The `domLinter` is the first non-stub dependency. It's 100% deterministic — no model, no API, no randomness.

**File:** `src/infrastructure/tools/domLinter.ts` (~304 lines)
**Tests:** `test/domLinter.test.ts` (18/18 pass)
**Parser:** `parse5` v8 (already in A-FORGE via jsdom)

### What it checks (all OBS-labeled):

| Check | Severity | Description |
|---|---|---|
| `MISSING_ALT_TEXT` | HIGH | Image without alt attribute |
| `EMPTY_ALT_TEXT` | MEDIUM | Alt="" without presentation role |
| `MISSING_BUTTON_TYPE` | LOW | Button without type (defaults to submit) |
| `POSITIVE_TABINDEX` | MEDIUM | tabindex > 0 disrupts natural tab order |
| `MISSING_ACCESSIBLE_NAME` | HIGH | Interactive element without aria-label/title |
| `MISSING_REQUIRED_ELEMENT` | HIGH | Required HTML element not found |
| `NAV_LINK_COUNT_EXCEEDED` | MEDIUM | Too many links in nav |
| `BANNED_ELEMENT_PRESENT` | HIGH | Forbidden element (e.g., iframe) |
| `DOM_DEPTH_EXCEEDED` | LOW | DOM nesting too deep |

### Key design decisions:
- Confidence always 0.90 (deterministic = known, F7 HUMILITY)
- Uses `parse5.parse()` for DOM traversal — no browser needed
- `walkNodes()` recursive traversal with parent tracking for depth computation
- Separates a11y checks from structural checks — composable
- Exports `DomLinterConstraints` type for constraint configuration

### Integration with forgeVisualQA:
Replace the stub `domLinter` dep with the real implementation:
```typescript
import { domLinter } from "../../infrastructure/tools/domLinter.js";
// ... in deps:
domLinter: async (payload, required) => domLinter(payload, { required_elements: required }),
```

---

## visionAnalyze — W₁ Vision Witness (Pixel-Level Evidence)

The `visionAnalyze` is the second real dependency. It's 100% deterministic pixelmatch — no model, no API, no semantic interpretation.

**File:** `src/infrastructure/tools/visionAnalyze.ts` (246 lines)
**Tests:** `test/visionAnalyze.test.ts` (10/10 pass)
**Deps:** `pixelmatch` + `pngjs` (already in A-FORGE)

### What it does:

1. Loads screenshot PNG
2. Looks for baseline at `<screenshot>.baseline.png`
3. If baseline exists: pixelmatch diff → deviations if `diff_pixels > tolerance`
4. If no baseline: returns empty deviations, confidence 0.50 (UNKNOWN)
5. SHA256 hash of screenshot bytes for auditability

### Key design decisions:
- Confidence always 0.90 when baseline used (deterministic = known, F7 HUMILITY)
- Confidence 0.50 when no baseline (UNKNOWN — no comparison possible)
- Severity classification: >20% = CRITICAL, >5% = HIGH, >1% = MEDIUM, else LOW
- All deviations labeled OBS (F2 TRUTH) — pure pixel math, no semantic interpretation
- Dimension mismatch → separate deviation type (HIGH severity)
- Configurable: `pixel_threshold` (pixelmatch sensitivity, default 0.1), `pixel_tolerance` (max allowed diff pixels, default 100)

### Integration with forgeVisualQA:
```typescript
import { visionAnalyze } from "../../infrastructure/tools/visionAnalyze.js";
// ... in deps:
visionAnalyze: async (path, constraints) => {
  const result = await visionAnalyze(path, constraints);
  return { deviations: result.deviations, confidence: result.confidence };
},
```

### Test coverage:
1. Identical images → 0 deviations, confidence 0.90
2. Different images → PIXEL_DIFF_EXCEEDED deviation
3. Partial diff → correct severity classification
4. No baseline → empty deviations, confidence 0.50
5. Missing screenshot → SCREENSHOT_LOAD_FAILED deviation
6. Dimension mismatch → DIMENSION_MISMATCH deviation
7. Threshold sensitivity — low threshold catches more diffs
8. Confidence always 0.90 when baseline used (F7)
9. Within tolerance → no deviation
10. SHA256 hash is deterministic

---

## Dependency Injection Plan

Full roadmap in `docs/VISUAL-QA-DEP-INJECTION-PLAN.md`.

| Dependency | Status | Implementation |
|---|---|---|
| `domLinter` (W₂) | ✅ Done + Wired | parse5, deterministic, 18 tests. Wired in core.ts. |
| `visionAnalyze` (pixelmatch) | ✅ Done + Wired | pixelmatch, deterministic, 10 tests. Wired in core.ts. |
| `scarQuery` | ❌ Stub | Wire to `arifMemory` mode=recall |
| `visionAnalyze` (VLM) | ❌ Stub | MiniMax/Claude vision API |
| `generateFix` | ❌ Stub | LLM-based, build last (highest blast radius) |

**Wiring order:** domLinter → visionAnalyze (pixelmatch) → scarQuery → visionAnalyze (VLM) → generateFix

---

## Implementation Status (as of 2026-07-17 — wiring complete)

| Component | File | Status |
|---|---|---|
| Core tool | `src/infrastructure/tools/ForgeVisualQA.ts` (~707 lines) | ✅ State machine, W³, entropy, scars, DI, `sealToVault999()` |
| Composite seal validator | `src/infrastructure/tools/CompositeSealValidator.ts` | ✅ Zod schemas, SHA256 recomputation, 5 checks, vault999Append DI |
| Seal validator (legacy) | `src/infrastructure/tools/ForgeVisualQASeal.ts` (285 lines) | ✅ I1-I5 invariants, routing guard, composite hash |
| Pure logic tests | `test/forge_visual_qa.test.ts` (26/26 pass) | ✅ Verdict transitions, W³, entropy, scars |
| Reality tests | `test/forge_visual_qa_reality.test.ts` (16/16 pass) | ✅ All 8 W³ Tri-Witness Reality Tests |
| Composite seal tests | `test/composite_seal_validator.test.ts` (10/10 pass) | ✅ Valid seal, 8 rejections, anti-collusion |
| Seal tests | `test/forge_visual_qa_seal.test.ts` (23/23 pass) | ✅ I1-I5 invariants + routing guard (7 suites) |
| Contract doc | `docs/MCP-TOOL-CONTRACT-VISUAL-QA.md` (664 lines) | ✅ 10 invariants, anti-collusion, routing spec |
| MCP: forge_visual_qa | `src/interfaces/mcp/core.ts` (+139 lines) | ✅ `server.tool("forge_visual_qa")` registered |
| MCP: forge_visual_seal | `src/interfaces/mcp/core.ts` (+113 lines) | ✅ `server.tool("forge_visual_seal")` registered |
| Deps: domLinter | `src/infrastructure/tools/domLinter.ts` (304 lines) | ✅ parse5-based, 9 check types, 18/18 tests. **WIRED** in core.ts. |
| Deps: visionAnalyze | `src/infrastructure/tools/visionAnalyze.ts` (246 lines) | ✅ pixelmatch-based, SHA256 hashing, 10/10 tests. **WIRED** in core.ts. |
| Deps: scarQuery | Injected | Stub — wire to arifMemory |
| Deps: generateFix | Injected | Stub — LLM-based, build last |
| Dep injection plan | `docs/VISUAL-QA-DEP-INJECTION-PLAN.md` | ✅ Full roadmap |
| **Total tests** | 6 test files | **103/103 pass** (26+16+10+23+18+10) |

### Bugs Found by Reality Tests (fixed)

1. **`checkEntropyGate`: delta_s=0 was passing.** No improvement is not improvement. Fixed to require `delta_s > 0` after iteration 1. ΔS=0 → HARD_FAULT per F2 TRUTH.
2. **Phase 4 888 gate: downgrading PASS_CANDIDATE to HOLD.** When `request888Hold` returned not-approved, the tool was moving to `HOLD` state. Fixed — tool stays at `PASS_CANDIDATE`; the orchestrator handles the external 888 gate.

---

## Pitfalls (cumulative from 2026-07-16 session)

6. **Confidence cap must propagate to returned values.** `evaluateTriWitness` must cap confidence at 0.90 (F7) in the **returned** `WitnessResult` objects, not just in the geometric mean computation. Fix: `{ ...w1, confidence: w1c }` in return.

7. **W³ zero-confidence with PENDING status.** When W₃ is `PENDING` with confidence=0, the geometric mean collapses to 0. The `anyZero` check fires before `anyRejected`. Use non-zero confidence for W₃ in rejection-specific tests.

8. **TypeScript enum narrowing in tests.** After `assert.equal(status, "REJECTED")`, TypeScript narrows the type. Fix: extract status into a variable BEFORE any assert.equal calls. See `references/typescript-test-pitfalls.md`.

9. **Entropy gate must be strict.** `delta_s === 0` (no improvement) must be HARD_FAULT, not pass. "Not worse" is not "better."

10. **PASS_CANDIDATE is a holding state, not a negotiation.** When `request888Hold` returns not-approved, the tool must stay at PASS_CANDIDATE — not downgrade to HOLD.

11. **Routing guard discriminated union: use `kind` field.** `{ allowed: true } | { blocked: true; reason }` doesn't narrow with `"allowed" in result`. Use `{ kind: "allowed" } | { kind: "blocked"; reason }` — TypeScript narrows correctly on `result.kind === "blocked"`. See `references/typescript-test-pitfalls.md` §4.

12. **Composite hash includes verdict.** `SHA256(w1 ‖ w2 ‖ w3 ‖ verdict)` — the verdict is part of the hash payload. This binds the seal to the specific verdict state. Changing the verdict without recomputing the hash → I3 violation.

13. **Don't re-import in core.ts.** Check existing imports before adding new ones. `consultScars` etc. may already be imported from `../../domain/forge/skill/index.js`.

14. **Optional DI for backward compatibility.** When adding a new validation gate to an existing function, make the new dep optional (`vault999Append?: ...`). Existing callers/tests that don't provide it get the old behavior. New callers opt in. This avoids breaking the 65+ existing tests when adding the composite seal validator.

15. **W3 sovereign identity is non-negotiable.** W3 MUST have `actor_id` (sovereign identity) and `timestamp` (ISO8601). Without these, the validator rejects — no anonymous seals to VAULT999. In `forgeVisualQA`, W3's `actor_id` comes from `w3.notes` (set during 888 approval flow).

16. **Anti-collusion: each witness is checked independently.** W1 cannot "forge" W3's verdict by including W3 data in its own hash. The validator checks `w3.verdict` directly from the input, not derived from W1's payload. The anti-collusion test proves this by having W1 collude while W3 actually fails.

17. **Phase 5 composite seal runs only when vault999Append provided.** Without the optional dep, Phase 5 falls back to the standard `sealToVault` path. This is the integration seam — callers who want pre-seal validation must inject the append function.

18. **First real dependency: domLinter is the template.** When building the next dependency (scarQuery, visionAnalyze), follow the domLinter pattern: pure function, DI-compatible signature, OBS-labeled deviations, confidence=0.90 for deterministic / capped for model-based. Test independently, then integrate.

19. **parse5 is already available.** A-FORGE has `parse5@8.0.1` via `jsdom`. Don't install a new HTML parser. Use `parse5.parse(html)` + recursive `walkNodes()` for DOM traversal.

20. **Audit before claiming completion.** "Lower the chaos and do proper housekeeping prior to seal." Always verify: git status clean, build clean, exact test counts, stub vs real status. Don't report stale numbers — re-run tests before summarizing. The user will audit your claims against reality.

21. **Epistemic discipline on claims.** Don't call something "post-transformer" or "first ever" or "physically impossible for models." The novelty is the integration, not the ontology. Stay in OBS/INT. Frame contributions as "this combination is tested end-to-end" not "this has never existed."

22. **pngjs Buffer.from() creates invalid PNGs.** `Buffer.from(pngBuffer)` creates a shallow copy of the raw bytes — but pngjs expects a properly serialized PNG. When modifying pixel data for tests, always: `PNG.sync.read(buffer)` → modify `png.data` → `PNG.sync.write(png)`. The helper `createModifiedPng()` pattern is the correct approach. Symptoms: "unrecognised content at end of stream" errors from pngjs sync reader.

23. **Distinguish "implementation exists" from "implementation is wired."** A function can be fully implemented (246 lines, 10 tests) but still stubbed in the MCP handler (core.ts returns empty). The skill status table must track BOTH states: implementation file status AND core.ts wiring status. When auditing, check: (1) does the implementation file exist? (2) is it imported in core.ts? (3) is the stub replaced with a real call? All three must be true for "Done + Wired."

---

## Reference Files

- `references/mcp-tool-wiring-pattern.md` — How to register a new tool in A-FORGE's MCP surface (server.tool pattern, callMCP routing, telemetry)
- `references/typescript-test-pitfalls.md` — Enum narrowing, generic witness types, confidence cap propagation

---

## Verification

1. Confirm `verdict` enum contains `PASS_CANDIDATE` and `SEALED_DEPLOY` but NOT `PASS`
2. Confirm `tri_witness_ledger` has all three witnesses with independent hashes
3. Confirm `scar_consultation` is called before fix generation
4. Confirm `entropy_delta` gates the iteration loop (ΔS≥0 after iter 1 → HARD_FAULT)
5. Confirm `requires888hold: true` on all `PASS_CANDIDATE` outputs
6. Confirm `evaluateTriWitness` caps confidence at 0.90 (F7 HUMILITY) in **returned** values, not just internal computation
7. Confirm W³ geometric mean uses `Math.cbrt(w1c * w2c * w3c)` — zero in any channel collapses to 0
8. Run reality tests: `npx tsx test/forge_visual_qa_reality.test.ts` — all 8 must pass
9. Run domLinter tests: `npx tsx test/domLinter.test.ts` — all 18 must pass
10. Run all visual QA: `node --test dist/test/forge_visual_qa*.test.js dist/test/domLinter.test.js dist/test/composite_seal_validator.test.js dist/test/visionAnalyze.test.js` — 103/103
