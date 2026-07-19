# Nonce Replay Fix — Implementation Pattern

**Date:** 2026-07-18  
**Vulnerability:** AAE v1 nonces generated but never tracked — replay succeeds silently  
**Files:** `nonceStore.ts` (new), `amanahEnvelope.ts`, `McpPolicyGate.ts`, `forgeTools.ts`

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ forgeTools.ts    │     │ McpPolicyGate.ts  │     │ amanahEnvelope  │
│ validateLease    │────▶│ Layer 1b (secret) │────▶│ verifyAAE()     │
│ aaeNonce? ──────▶│     │ Layer 5 (no secret│     │ nonceStore?     │
│ globalNonceStore │     │ globalNonceStore  │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                    ┌─────▼────────┐
                                                    │ NonceStore   │
                                                    │ Map<nonce,   │
                                                    │   {seen_at}> │
                                                    │ TTL: 10min   │
                                                    └──────────────┘
```

## NonceStore Design (`src/domain/governance/nonceStore.ts`)

```typescript
export class NonceStore {
  private seen: Map<string, NonceEntry> = new Map();
  private ttlMs: number;
  private maxEntries: number;

  constructor(ttlMs = 10 * 60 * 1000, maxEntries = 100_000) {}

  // Primary entry point — atomic check-and-record
  checkAndRecord(nonce: string): NonceCheckResult { ... }

  // Read-only check (no recording)
  isReplay(nonce: string): boolean { ... }

  // Record without checking
  record(nonce: string): void { ... }

  // Remove expired entries; evict oldest if over maxEntries
  cleanup(): void { ... }
}

// Singleton for federation-wide use
export const globalNonceStore = new NonceStore();
```

Key decisions:
- **TTL matches AAE max lifetime** (10 min default) — nonces don't need to be remembered forever
- **Cleanup runs on checkAndRecord** when size > maxEntries/2 — bounds memory without separate timer
- **`isReplay` is read-only** — useful for pre-validation without side effects
- **Empty nonce is skipped** (returns `{replay: false}`) — backward compat with optional nonces

## Integration Points

### 1. `verifyAAE()` — optional 3rd param

```typescript
export function verifyAAE(
  envelope: AAEV1,
  organ_secret: string,
  nonceStore?: NonceStore,  // NEW — backward compatible
): VerifyResult {
  // ... existing F1/F8 checks ...
  // After signature verification, before version check:
  if (nonceStore && envelope.nonce) {
    const nonceResult = nonceStore.checkAndRecord(envelope.nonce);
    if (nonceResult.replay) {
      return { valid: false, replay_detected: true, reason: nonceResult.reason, epistemic: "DER" };
    }
  }
}
```

**Placement:** After signature check, before version check. Signature must be valid before we trust the nonce is authentic.

### 2. McpPolicyGate — two layers

**Layer 1b** (when organ_secret provided): Passes `this.nonceStore` to `verifyAAE()`. Nonce checked + recorded during signature verification.

**Layer 5** (defense-in-depth, when no organ_secret): Standalone `nonceStore.checkAndRecord()`. Only runs if Layer 1b didn't already verify (tracked via `nonceVerifiedInLayer1b` flag).

**Critical:** Without the flag, Layer 5 would see the nonce as a replay (Layer 1b already recorded it). The flag prevents double-recording.

### 3. `validateLeaseForTool()` — optional 4th param

```typescript
export async function validateLeaseForTool(
  lease_id: string | undefined,
  tool: string,
  actionClass: string,
  aaeNonce?: string,  // NEW — backward compatible
): Promise<...> {
  if (aaeNonce) {
    const nonceResult = globalNonceStore.checkAndRecord(aaeNonce);
    if (nonceResult.replay) {
      return { ok: false, gate: "REPLAY_DETECTED", reason: nonceResult.reason };
    }
  }
  // ... existing lease validation ...
}
```

## Test Strategy (`test/nonceReplay.test.ts`)

### NonceStore unit tests (1-5)
1. Fresh nonce → not replay
2. Same nonce twice → replay with `REPLAY_DETECTED` reason
3. Expired nonce (short TTL) → not replay after TTL
4. `isReplay()` is read-only (doesn't record)
5. `cleanup()` removes expired entries, caps at maxEntries

### AAE integration tests (6-8)
6. `verifyAAE` with NonceStore: first use passes, nonce recorded
7. `verifyAAE` with NonceStore: second use → `replay_detected: true`
8. `verifyAAE` without NonceStore: backward compat, no replay check

### McpPolicyGate integration tests (9-11)
9. Layer 1b replay detection (with organ_secret)
10. Layer 5 replay detection (without organ_secret)
11. Different nonces pass independently

### Test isolation gotcha (CRITICAL)

`McpPolicyGate` loads policies from disk in constructor. The file
`/root/A-FORGE/config/mcp_policies.json` may contain containment policies
that override the default sovereign policy, causing unexpected DENY verdicts
in tests.

**Fix:** Always add an explicit test policy:

```typescript
const gate = new McpPolicyGate(store);
gate.addPolicy({
  policy_id: "test:arif",
  actor_id: "arif",
  role: "sovereign",
  allow_by_default: true,
  allowed_mcp_servers: { forge: { allow: true, tools: {} } },
});
```

### Action class gotcha (CRITICAL)

`EXECUTE_HIGH_IMPACT` and `IRREVERSIBLE` require `judgment_reference` at
Layer 5. Tests using `forge_execute` with these action classes will fail
unless the AAE includes `judgment_reference`. For nonce replay tests that
don't need to test action_class gating, use `OBSERVE` action class.

## Backward Compatibility

All changes are backward compatible:
- `verifyAAE(aae, secret)` — works exactly as before (no NonceStore)
- `new McpPolicyGate()` — uses `globalNonceStore` by default
- `validateLeaseForTool(lease_id, tool, class)` — works as before (no nonce)
- Existing tests in `amanahEnvelope.test.ts` unchanged
