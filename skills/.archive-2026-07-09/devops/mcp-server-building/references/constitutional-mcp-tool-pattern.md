# Constitutional MCP Tool Pattern — F1-F13 Enforcement BY DESIGN

> **Created 2026-07-16** — from forge_visual_qa build session
> **Stack:** A-FORGE TypeScript, Zod schemas, @modelcontextprotocol/sdk

## When to Use This Pattern

Standard A-FORGE tools rely on FloorEnforcer (external gate) for constitutional compliance. Use this pattern when the tool's **internal logic** must enforce F1-F13 invariants — i.e., the constitutional constraint IS the algorithm, not a wrapper.

## The Pattern: 5 Constitutional Components

### 1. Verdict State Machine (F1 AMANAH)

The tool cannot grant itself a terminal success state. Use explicit state transitions:

```typescript
export const VerdictState = z.enum([
  "INIT",           // Cycle started
  "VALIDATING",     // Witnesses running
  "ITERATING",      // Fix in progress
  "PASS_CANDIDATE", // Deviations within threshold, awaiting sovereign
  "SEALED_DEPLOY",  // Post-888 cryptographic human approval (ONLY terminal success)
  "HOLD",           // Human requested pause
  "HARD_FAULT",     // ΔS violation or max iterations
  "VOID",           // Constitutional rejection
]);

// Explicit valid transitions — any other = constitutional violation
const VALID_TRANSITIONS: Record<VerdictState, VerdictState[]> = {
  INIT:             ["VALIDATING"],
  VALIDATING:       ["PASS_CANDIDATE", "ITERATING", "HARD_FAULT"],
  ITERATING:        ["VALIDATING", "HARD_FAULT"],
  PASS_CANDIDATE:   ["SEALED_DEPLOY", "HOLD", "VOID"],  // ONLY 888 can transition
  SEALED_DEPLOY:    [],  // Terminal
  HOLD:             ["VALIDATING", "VOID"],
  HARD_FAULT:       ["VALIDATING", "VOID"],
  VOID:             [],  // Terminal
};

export function isValidTransition(from: VerdictState, to: VerdictState): boolean {
  return VALID_TRANSITIONS[from]?.includes(to) ?? false;
}
```

**Key rule:** `PASS` does not exist in the enum. The AI cannot grant itself a terminal success state. Test this explicitly:
```typescript
it("PASS is not a valid verdict state (HARAM)", () => {
  const validStates = ["INIT", "VALIDATING", ...];
  assert.ok(!validStates.includes("PASS"));
});
```

### 2. Tri-Witness W³ (F3 WITNESS)

Three independent witnesses must agree. Zero in any channel collapses consensus.

```typescript
// W³ = ∛(W₁ × W₂ × W₃) — geometric mean
const w3Score = Math.cbrt(w1c * w2c * w3c);

// Zero in any channel collapses consensus
const anyZero = w1c === 0 || w2c === 0 || w3c === 0;
```

**Anti-collusion:** Each witness sees different substrate. W₁ sees pixels only. W₂ sees DOM/spec only. W₃ sees both + history. Neither W₁ nor W₂ can write W₃ fields.

**F7 HUMILITY:** Cap all confidence values at 0.90 — both in computation AND in the returned result:
```typescript
return {
  w1_vision: { ...w1, confidence: w1c },  // capped in output
  w2_linter: { ...w2, confidence: w2c },
  w3_sovereign: { ...w3, confidence: w3c },
  consensus_confidence: w3Score,
};
```

**Pitfall:** Capping only in the geometric mean but returning uncapped values violates F7. The output struct must reflect capped values.

### 3. Entropy Metabolism (F4 CLARITY)

ΔS must be non-increasing. If entropy increases after the first iteration → HARD_FAULT.

```typescript
export function computeEntropyDelta(prev: EntropyState, currentDeviationCount: number): EntropyState {
  const deltaS = prev.deviation_count - currentDeviationCount;
  return {
    iteration: prev.iteration + 1,
    deviation_count: currentDeviationCount,
    delta_s: deltaS,  // positive = improvement, negative = degradation
    cumulative_delta: prev.cumulative_delta + deltaS,
  };
}

export function checkEntropyGate(entropy: EntropyState): { pass: boolean; reason?: string } {
  if (entropy.iteration <= 1) return { pass: true };  // baseline exempt
  if (entropy.delta_s <= 0) return {  // ΔS=0 also fails — thermodynamic proof required
    pass: false,
    reason: `ENTROPY_NON_DECREASING: ΔS=${entropy.delta_s} at iteration ${entropy.iteration}. No improvement — system must reduce deviations.`,
  };
  return { pass: true };
}
```

### 4. Scar Consultation (Temporal Memory)

Before generating fixes, query the scar database for matching deviation patterns. If a scar shows FAILURE → don't repeat the fix.

```typescript
export async function consultScars(
  deviations: Deviation[],
  scarQueryFn: (type: string) => Promise<Scar | null>,
): Promise<ScarConsultationResult[]> {
  for (const deviation of deviations) {
    const scar = await scarQueryFn(deviation.type);
    if (!scar) → GENERATE_NEW
    if (scar.outcome === "SUCCESS") → APPLY_HISTORICAL
    if (scar.outcome === "FAILURE") → SCAR_CONFLICT (don't repeat)
    if (scar.outcome === "PARTIAL") → APPLY_HISTORICAL with caution
  }
}
```

**Pitfall:** A-FORGE already has `consultScars` in `domain/forge/skill/index.js`. Don't duplicate — use the existing domain layer or document why a new implementation is needed.

### 5. Dependency Injection for External Substrates

Vision analysis, DOM linting, fix generation — these are injected as functions, not hardcoded:

```typescript
export async function forgeVisualQA(
  input: ForgeVisualQAInput,
  deps: {
    visionAnalyze: (path: string, constraints: unknown) => Promise<{ deviations: Deviation[]; confidence: number }>;
    domLinter: (payload: string, required: string[]) => Promise<{ deviations: Deviation[]; confidence: number }>;
    scarQuery: (type: string) => Promise<Scar | null>;
    generateFix: (payload: string, deviations: Deviation[], scars: ScarConsultationResult[]) => Promise<string>;
    request888Hold: (context: unknown) => Promise<{ approved: boolean; receipt_id: string }>;
    sealToVault: (data: unknown) => Promise<{ receipt_id: string }>;
    notifyWell: (signal: unknown) => Promise<{ receipt_id: string }>;
  },
): Promise<z.infer<typeof ForgeVisualQAOutput>> {
```

This allows testing the governance logic independently of the actual vision model or DOM linter.

## Test Pattern

Test each constitutional component independently:

1. **State machine transitions** — valid and invalid transitions, terminal states, PASS exclusion
2. **W³ evaluation** — all confirmed, one rejected, zero collapse, confidence capping
3. **Entropy metabolism** — baseline exempt, improvement pass, degradation fault, cumulative tracking
4. **Scar consultation** — no scar, success scar, failure scar, multiple deviations

```bash
cd /root/A-FORGE && npx tsx test/forge_visual_qa.test.ts
# 26 tests, 4 suites — all constitutional invariants covered
```

## Wiring Into A-FORGE

After the tool file is complete, follow the standard 3-step registration:
1. `actionClassifier.ts` — classify as `EXECUTE_REVERSIBLE` (render + screenshot are ephemeral)
2. `ForgeVisualQA.ts` — already created
3. `core.ts` — import + `registerForgeVisualQA(server)`

See `aforge-mcp-tool-registration.md` for the standard wiring pattern.

## Reference Implementation

`/root/A-FORGE/src/infrastructure/tools/ForgeVisualQA.ts` — 604 lines, 42/42 tests passing (26 pure logic + 16 reality).

## Composite Seal Validator (Pre-SEAL Gate)

After PASS_CANDIDATE → human ack → SEALED_DEPLOY, a pre-seal gate validates before VAULT999:

```typescript
// composite_hash = SHA256(w1.hash + w2.hash + w3.hash + verdict)
const recomputed = SHA256(
  tri_witness.w1.hash + tri_witness.w2.hash + tri_witness.w3.hash + verdict
);
if (recomputed !== tri_witness.composite_hash) {
  return { verdict: "REJECTED", error: "COMPOSITE_HASH_MISMATCH" };
}
```

5 rejection checks: verdict ≠ SEALED_DEPLOY, any witness ≠ PASS, hash format invalid, recomputed ≠ provided, W3 missing actor_id/timestamp. Anti-collusion: W₃ checked independently.

## W³ Reality Tests (8-test methodology)

Pure logic tests prove the code runs. Reality tests prove the tool is a **governed physical system**. The 8 tests: W₁ vision divergence, W₂ structural witness, W₃ sovereignty, ΔS entropy, hash discipline, witness independence, routing discipline, sovereign seal.

Each test mocks dependencies to create controlled divergence scenarios. Full methodology: see `a-forge-development` → `references/w3-reality-test-methodology.md`.
