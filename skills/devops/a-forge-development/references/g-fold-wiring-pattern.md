# G-fold Wiring Pattern — GovernanceBridge + 4-Layer Forge Gate

**Forged 2026-07-26.** Wires the APEX canonical G scalar from the arifOS kernel health endpoint into A-FORGE's domain-layer gate infrastructure.

## Problem

The forge.evaluate gate computes `G = A·P·E·X·Φ` locally (a Nash-pattern product of estimator scores). But the canonical G-fold — the one produced by `arif_think(mode='apex')` in the arifOS Python kernel — is the constitutionally authorized scalar. Two G values existed with no bridge between them: the actuator-local estimate and the kernel's canonical G.

## Solution: 4-Layer Forge Gate

```
Layer 1: A·P·E·X·Φ product (always available, local)
Layer 2: fetchCanonicalG() → kernel G from /health endpoint
Layer 3: Fallback to local estimate on kernel unreachable
Layer 4: Authority stamp on GateDecision.g_authority
```

## File Changes

### 1. `GovernanceBridge.ts` — Added `fetchCanonicalG()`

```typescript
// Location: src/domain/governance/GovernanceBridge.ts
// Placed after classifyTool(), before private _httpClassify()

async fetchCanonicalG(): Promise<{ G: number; source: string } | null> {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 2000);
    const response = await fetch(`${this.baseUrl}/health`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!response.ok) return null;
    const body = (await response.json()) as Record<string, unknown>;

    // Navigate: body.apex_scalars.G.value
    const apexScalars = body.apex_scalars as Record<string, unknown> | undefined;
    if (!apexScalars) return null;
    const gField = apexScalars.G as Record<string, unknown> | undefined;
    if (!gField || typeof gField.value !== "number") return null;

    return { G: gField.value, source: `${this.baseUrl}/health` };
  } catch {
    return null;
  }
}
```

**Pattern consistency:**
- Same `AbortController` + `setTimeout` + `clearTimeout` pattern as `_httpClassify()`
- Same `catch{}` → `return null` for graceful degradation
- Same `Record<string, unknown>` casting to navigate nested JSON

### 2. `evaluate.ts` — Added `computeGateWithKernelG()`

```typescript
// Location: src/domain/forge/evaluate.ts
// Import added: import { GovernanceBridge } from "../governance/GovernanceBridge.js";
// Placed after computeGate(), before renderVerdict()

async function computeGateWithKernelG(
  scores: Omit<EstimatorScores, "rationale" | "Omega">,
  bridge: GovernanceBridge,
): Promise<{
  G: number;
  C_dark: number;
  g_authority: "arif_think.mode=apex" | "local_estimate";
  g_canonical_source: "arif_think.mode=apex";
}> {
  const C_dark = scores.A * (1 - scores.P) * (1 - scores.X);

  // Layer 2: Try canonical kernel G
  const canonical = await bridge.fetchCanonicalG();

  if (canonical !== null) {
    // Layer 2 hit: kernel G replaces local product
    return {
      G: canonical.G,
      C_dark,
      g_authority: "arif_think.mode=apex",
      g_canonical_source: "arif_think.mode=apex",
    };
  }

  // Layer 3 fallback: local estimate
  const G = scores.A * scores.P * scores.E * scores.X * scores.Phi;
  return {
    G,
    C_dark,
    g_authority: "local_estimate",
    g_canonical_source: "arif_think.mode=apex",
  };
}
```

## Design Invariants

1. **Non-breaking**: `computeGate()` untouched — `evaluateCandidate()` and `evaluateDryRun()` continue using local estimate by default
2. **Additive**: `computeGateWithKernelG()` is a new export; callers opt in by providing a GovernanceBridge
3. **C_dark stays local**: The kernel provides only G; C_dark = A·(1-P)·(1-X) is always a local computation (it's a local misalignment signal, not a kernel scalar)
4. **g_canonical_source is always `"arif_think.mode=apex"`**: This points to the canonical path regardless of whether we reached it
5. **Graceful fallback**: If arifOS is unreachable, local estimate fires — no hard failure

## How to Consume

In a forge pipeline caller (e.g., tool registration):

```typescript
import { GovernanceBridge } from "../governance/GovernanceBridge.js";
import { computeGateWithKernelG, renderVerdict } from "../forge/evaluate.js";

const bridge = new GovernanceBridge({ baseUrl: "http://localhost:8088" });
const gateResult = await computeGateWithKernelG(scores, bridge);
const { verdict, reason } = renderVerdict(gateResult.G, gateResult.C_dark, omega);
```

## Testing Strategy

| Scenario | How to Test | Expected Outcome |
|----------|-------------|------------------|
| Kernel reachable, G present | Mock `fetch` to return `{ apex_scalars: { G: { value: 0.85 } } }` | G = 0.85, authority = `arif_think.mode=apex` |
| Kernel unreachable | Mock `fetch` to throw | Falls back to A·P·E·X·Φ, authority = `local_estimate` |
| Kernel returns 404 | Mock response.ok = false | Falls back to local estimate |
| Kernel returns malformed body | Mock response with missing apex_scalars | Returns null → local fallback |
| Kernel returns non-numeric G.value | Mock G.value = "high" | typeof check fails → null → local |
| Bridge with different baseUrl | Instantiate with dev vs prod URL | Uses instance's baseUrl, not hardcoded |
