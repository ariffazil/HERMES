# TypeScript Pitfalls for Governed Tool Tests

## 1. Enum Union Narrowing with assert.equal

**Problem:** When testing enum-like union types (`"REJECTED" | "CONFIRMED" | "PENDING" | "TIMEOUT"`), TypeScript narrows the type after `assert.equal()` calls. A subsequent comparison like `status !== "CONFIRMED"` gets flagged as "unintentional" because TypeScript already knows the type is `"REJECTED"`.

```typescript
// BROKEN — TypeScript error TS2367
assert.equal(w1.status, "REJECTED");
assert.equal(w2.status, "CONFIRMED");
assert.ok(w1.status !== w2.status); // TS: "REJECTED" and "CONFIRMED" have no overlap
```

**Fix:** Extract status values into variables BEFORE any assert.equal calls:

```typescript
// CORRECT — variables hold the union type before narrowing
const w1Status = w1.status;
const w2Status = w2.status;
assert.ok(w1Status !== w2Status, "W₁ ≠ W₂");
assert.equal(w1Status, "REJECTED");
assert.equal(w2Status, "CONFIRMED");
```

**Why:** TypeScript control flow analysis narrows variable types after type guards (including `assert.equal`). The narrowing persists for the rest of the scope. By comparing BEFORE the assertions, the variables still hold the full union type.

## 2. Generic Witness Types for Type-Safe Ledgers

**Pattern:** When building tri-witness or multi-witness systems, use generic type parameters to enforce that each witness slot has the correct literal `witness_id`:

```typescript
interface WitnessResult<ID extends string = "W1" | "W2" | "W3"> {
  witness_id: ID;
  status: "CONFIRMED" | "REJECTED" | "PENDING" | "TIMEOUT";
  confidence: number;
}

interface TriWitnessLedger {
  w1_vision: WitnessResult<"W1">;
  w2_linter: WitnessResult<"W2">;
  w3_sovereign: WitnessResult<"W3">;
  consensus: boolean;
}

function evaluateTriWitness(
  w1: WitnessResult<"W1">,
  w2: WitnessResult<"W2">,
  w3: WitnessResult<"W3">,
): TriWitnessLedger { ... }
```

**Why:** Without generics, `witness_id: "W1" | "W2" | "W3"` allows any witness to go in any slot. With generics, TypeScript enforces that W₁ always has `witness_id: "W1"`.

**In tests:** Use a generic helper:

```typescript
const makeW = <ID extends "W1" | "W2" | "W3">(
  id: ID, status: "CONFIRMED" | "REJECTED" | "PENDING", conf: number
): WitnessResult<ID> => ({
  witness_id: id, status, confidence: conf, deviations: [],
});
```

## 3. Discriminated Union: Use `kind` Field (Not `in` Operator)

**Problem:** `{ allowed: true } | { blocked: true; reason: string }` doesn't narrow with `"allowed" in result` or `"blocked" in result`. TypeScript sees both branches as possible for both properties.

```typescript
// BROKEN — TS2339: Property 'blocked' does not exist on type '{ allowed: true; }'
type GuardResult = { allowed: true } | { blocked: true; reason: string };
const result: GuardResult = ...;
if (result.blocked) { ... } // ERROR
```

**Fix:** Use a `kind` discriminant field:

```typescript
// CORRECT — TypeScript narrows on result.kind
type GuardResult = { kind: "allowed" } | { kind: "blocked"; reason: string };
const result: GuardResult = ...;
if (result.kind === "blocked") {
  console.log(result.reason); // narrowed: reason exists
}
```

**Rule:** Any time you build a result type that represents "proceed or stop with reason", use a string discriminant (`kind`, `status`, `verdict`) — not boolean presence (`allowed`/`blocked`).

## 4. Confidence Cap Must Propagate to Returns

**Problem:** `evaluateTriWitness` computes capped confidence internally (`w1c = Math.min(w1.confidence, 0.90)`) but returns the original uncapped `w1` object. Downstream code sees 0.99 instead of 0.90 — F7 HUMILITY violation.

**Fix:** Spread + override in the return:

```typescript
return {
  w1_vision: { ...w1, confidence: w1c },
  w2_linter: { ...w2, confidence: w2c },
  w3_sovereign: { ...w3, confidence: w3c },
  consensus,
  consensus_confidence: w3Score,
};
```
