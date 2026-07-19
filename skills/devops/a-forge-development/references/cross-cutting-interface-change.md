# Cross-Cutting Interface Change Pattern

**Context:** Adding a mandatory/optional field that spans the executor and governance layers of A-FORGE.

**Proven:** 2026-07-18, `judgment_reference` addition across 4 files.

---

## Dependency Order (must touch in this sequence)

```
1. src/executor/types.ts              ← Interface definition (ExecutorReceipt)
2. src/executor/forge.ts              ← Validation (validateReceipt) + hard-fail comment
3. src/domain/governance/amanahEnvelope.ts  ← AAEV1 interface + buildAAE + computeSignature + extendAAE
4. src/domain/governance/McpPolicyGate.ts   ← Layer 5 policy enforcement
5. test/judgmentReference.test.ts      ← New test file
```

## Per-File Checklist

### 1. `types.ts` — Interface definition
- Add field to the interface (e.g., `judgment_reference: string` for mandatory, `judgment_reference?: string` for optional)
- Add JSDoc comment explaining the field's constitutional purpose

### 2. `forge.ts` — Receipt validation
- Add hard-fail check in `validateReceipt()`:
  ```typescript
  if (!receipt.judgment_reference) violations.push("Missing judgment_reference — ...");
  ```
- Update the hard-fail set JSDoc comment above `validateReceipt`

### 3. `amanahEnvelope.ts` — AAE envelope (4 touch points!)
- **Interface:** Add field to `AAEV1` (optional `?` for low-severity actions)
- **Options:** Add field to `AAEV1Options` builder input
- **`computeSignature`:** Add field to the `body` object inside the function — this is the HMAC-SHA256 signed body. Missing this = tamper detection gap.
- **`buildAAE`:** Destructure from options, pass to envelope object
- **`extendAAE`:** Add field to the `extended` object — preserves through TTL extensions

### 4. `McpPolicyGate.ts` — Layer 5 enforcement
- Add validation in the Layer 5 AAE section (after action_class checks)
- Only require for high-severity actions (EXECUTE_HIGH_IMPACT, IRREVERSIBLE)
- Low-severity (OBSERVE, SUGGEST) should pass without the field

### 5. Tests
- Test missing field → violation / REFUSED / DENY
- Test present field → valid / ALLOW
- Test field in HMAC body (tamper detection — changing it invalidates signature)
- Test low-severity actions pass without the field
- Test `extendAAE` preserves the field
- Use real tool names from `actionClassifier.ts` registry (not fabricated ones)

## Gotchas

| Gotcha | Detail |
|--------|--------|
| **Import path** | `ExecutorReceipt` is in `types.ts`, NOT re-exported from `forge.ts`. Import from `../src/executor/types.js` in tests. |
| **Tool names in tests** | Must match `actionClassifier.ts` registry. `forge_deploy` does NOT exist — use `forge_execute` for HIGH_IMPACT, `forge_shell` for IRREVERSIBLE, `forge_memory` for OBSERVE. |
| **`computeSignature` body** | The field MUST be added to the `body` object inside `computeSignature()`. Forgetting this means the field is not part of the HMAC — tampering goes undetected. |
| **`extendAAE` carrier** | The field must be added to the `extended` object. Forgetting this means extensions lose the field. |
| **`npm test` is narrow** | Only runs `AgentEngine.test.js`. Run each test file individually: `node dist/test/<name>.test.js`. |
| **`make test` pre-existing failures** | May fail on missing files (e.g., `engine.test.js`). Verify your changes didn't cause new failures by running the relevant test files individually. |

## Test Pattern

```typescript
import { validateReceipt, forgeExecute } from "../src/executor/forge.js";
import type { ExecutorReceipt } from "../src/executor/types.js";  // ← from types, not forge
import { buildAAE, verifyAAE, extendAAE, type AAEV1 } from "../src/domain/governance/amanahEnvelope.js";
import { McpPolicyGate } from "../src/domain/governance/McpPolicyGate.js";

function makeReceipt(overrides?: Partial<ExecutorReceipt>): ExecutorReceipt {
  return {
    receiptId: "rcpt-001",
    kernelSignature: "kern-sig-abc123",
    verdict: "SEAL",
    ccId: "cc-2026-07-18-001",
    judgment_reference: "verdict-888-seal-001",  // ← new field
    allowedActions: ["forge_execute"],            // ← real tool name
    toolName: "forge_execute",                    // ← from actionClassifier
    inputHash: "blake3-input-hash",
    bounds: { reversible: true, blastRadius: "MEDIUM", maxTools: 5 },
    authority: {
      actorId: "arif", sessionId: "sess-001",
      validUntil: new Date(Date.now() + 300_000).toISOString(),
      scope: "EXECUTE",
    },
    lineage: { evidenceIds: ["vault-e-001"], collapseTimestamp: new Date().toISOString() },
    ...overrides,
  };
}
```
