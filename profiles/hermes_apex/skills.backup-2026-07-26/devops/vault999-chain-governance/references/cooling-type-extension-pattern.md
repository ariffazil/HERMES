# COOLING_RECEIPT Type Extension — VAULT999 Pattern (2026-07-13)

> **Context:** EUREKA session 2026-07-13 established the 6-plane Zen architecture.
> The COOLING_RECEIPT (seal_v3) closes the metabolic loop — records what Reality
> observed after execution that the plan didn't predict, and routes the insight
> back through governance, never directly to execution.
>
> This document captures the reusable pattern for adding a new seal type to
> `seal_chain.js` with domain-specific validation invariants.

## The Pattern (4 Steps)

### Step 1: Register `event_type` in `classifyEventType()`

File: `/root/AAA/a2a-server/seal_chain.js`

Add the new event type **before** the generic fallback match:

```javascript
function classifyEventType(payload) {
  const action = (payload.action || '').toLowerCase();
  // ── Specific types first (order matters — match before generic fallback) ──
  if (action.startsWith('a2a.')) return 'a2a.dispatch';
  if (action === 'cooling.receipt' || action.includes('cooling.receipt')) return 'cooling.receipt';
  if (action.includes('shell') || action.includes('forge.execute')) return 'forge.shell';
  // ... more specific types ...
  if (action.includes('seal')) return 'session.seal';       // BEFORE generic
  return 'a2a.general';                                      // generic catch-all
}
```

**Rule:** Specific matches first, generic fallback last. A `cooling.receipt` action
must be caught before it falls through to `session.seal` or `a2a.general`.

### Step 2: Write a Validation Function with Domain Invariants

Pattern for the validation function:

```javascript
function validateNewType(payload, opts = {}) {
  const violations = [];

  // INV-N1: Core invariant for this type
  if (/* condition */) {
    violations.push({
      invariant: 'INV-N1_INVARIANT_NAME',
      detail: `Description of what failed: got ${actual}`,
    });
  }

  // INV-N2: Second invariant
  // ... additional checks ...

  return {
    valid: violations.length === 0,
    violations,
    downgraded: violations.length > 0,
  };
}
```

**Conventions:**
- Invariant names: `INV-{C|N|...}{NUMBER}_{SHORT_NAME}`
  - `C` for cooling types, `N` for generic new types, `I` for infra types
  - Short name describes what was checked (e.g. `ACTION_OBSERVE`, `CALLER_NOT_FORGE`)
- The function returns `{valid, violations, downgraded}` — same shape as `enforceSealInvariants`
- Violations are a list of `{invariant, detail}` objects
- `downgraded` is `true` whenever there are violations — the seal verdict goes from SEAL→HOLD

### Step 3: Wire into `writeSeal()`

Insert the cooling validation **immediately after** `enforceSealInvariants` and
**before** any ledger work:

```javascript
async function writeSeal(payload, opts = {}) {
  // ── Invariant enforcement (G1 fix) — runs BEFORE any ledger work ──
  const invariants = enforceSealInvariants(payload, opts);

  // ── New type validation — runs for matching event types ──
  const eventType = opts.event_type || classifyEventType(payload);
  let typeVal = null;
  if (eventType === 'cooling.receipt') {
    typeVal = validateCooling(payload, opts);
    if (typeVal.downgraded) {
      if (!invariants.violations) invariants.violations = [];
      invariants.violations.push(...typeVal.violations);
      if (!invariants.downgraded) invariants.downgraded = true;
    }
  }

  // ... existing ledger work continues with invariants now including new type violations ...
```

**Key rule:** The new validation violations are merged into the existing
`invariants.violations` array. This means:
- The `enforceSealInvariants` function doesn't need modification for new types
- All violations (invariant + type-specific) appear in a single list
- The final `verdict`, `invariants_violated`, and `invariants_downgraded` reflect
  both layers of enforcement
- The `var eventType` must be declared exactly once and shared between the
  validation block and the enriched envelope fields section

### Step 4: Export from Module

Add to `module.exports`:

```javascript
module.exports = {
  // ... existing exports ...
  validateCooling,
};
```

Also add the new validation result to the return value of `writeSeal()`:

```javascript
return {
  // ... existing return fields ...
  // ── New type validation ──
  cooling_validated: typeVal !== null,
  cooling_downgraded: typeVal ? typeVal.downgraded : false,
  cooling_violations: typeVal && typeVal.violations.length > 0 ? typeVal.violations : null,
};
```

## Reference: COOLING_RECEIPT Invariants

Full spec: `/root/AAA/docs/contracts/COOLING_RECEIPT_SPEC_v1.md`

| Invariant | Check | Violation |
|-----------|-------|-----------|
| INV-C1 | `action_class === 'OBSERVE'` | COOLING-MUST-NOT-SELF-DEPLOY — a cooling receipt must never contain a MUTATE action |
| INV-C2 | `caller` must not contain "forge" | Cooling routes through governance, never execution. Hermes sends, not A-FORGE. |
| INV-C3 | `supersedes.type === 'COLD_LINK'` | Original seal is immutable. COOLING creates a forward reference, not an overwrite. |
| INV-C4 | `judge_required=true` unless authority is AUTO/OBSERVE_ONLY | Governance path must be explicit — every improvement goes somewhere. |

## Testing Pattern

```javascript
const sc = require('./seal_chain.js');

// Test 1: Valid type passes
const valid = sc.validateCooling({
  action_class: 'OBSERVE',
  supersedes: { type: 'COLD_LINK' },
  governance_path: { judge_required: true, required_authority: '888_HOLD' },
  caller: 'hermes-prime',
});
console.assert(valid.valid, 'Valid cooling should pass');

// Test 2: Forge block
const forge = sc.validateCooling({...}, { caller: 'forge-333' });
console.assert(!forge.valid, 'Forge caller should be rejected');
console.assert(forge.violations[0].invariant === 'INV-C2_CALLER_NOT_FORGE');

// Test 3: Event type classification
console.assert(sc.classifyEventType({ action: 'cooling.receipt' }) === 'cooling.receipt');

// Test 4: Chain verify still works (pre-existing anomalies permitted)
const chain = sc.verifyChain();
// Known gaps (seq 18-60, pre-May migration) are non-issue per sovereign ruling
```

## When to Use This Pattern

Use this 4-step pattern whenever a new VAULT999 seal type is needed:
- New governed action class (e.g. human biometric report, scheduled audit)
- New metabolic cycle type (e.g. resource allocation receipt)
- New inter-organ handoff type (e.g. WELL→WEALTH attestation)

Do NOT use this pattern for:
- Routine SEAL types already covered by existing event_types (forge.shell, session.seal, etc.)
- IMAGE_SEAL entries — these go to a separate file (`image_seal_chain.jsonl`)
- Temporary/debug entries — the seal chain is immutable append-only
