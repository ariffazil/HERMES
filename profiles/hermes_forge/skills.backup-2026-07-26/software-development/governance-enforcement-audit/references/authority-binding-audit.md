# Authority Binding Audit — Execution Token Field Check

**Sub-pattern of governance-enforcement-audit.** Use when auditing whether execution tokens (leases, receipts, authorization envelopes) bind all required fields to prevent replay, forgery, scope creep, or authority drift.

## The 8 Required Fields

Every execution token that authorizes mutation/execution must bind:

| # | Field | What It Prevents | What "Missing" Looks Like |
|---|-------|-----------------|---------------------------|
| 1 | **Actor** | Unauthorized agent | Token has no `actor_id` or uses anonymous/default |
| 2 | **Session** | Cross-session replay | Token valid across sessions; no session binding |
| 3 | **Exact Operation** | Scope creep | Token authorizes "any tool" instead of specific tool name |
| 4 | **Exact Arguments Hash** | Input tampering | Token doesn't hash-bind the approved inputs |
| 5 | **Expiry** | Indefinite authority | Token never expires or TTL is unreasonably long |
| 6 | **Reversibility Class** | Misclassified blast radius | Irreversible action classified as reversible |
| 7 | **Judgment Reference** | Detached authority | Token issued but no link to the judgment that authorized it |
| 8 | **Single-Use Nonce** | Replay attacks | Nonce generated but never tracked/consumed |

## Audit Procedure

### Step 1 — Find All Authority Surfaces

Search for execution token types, lease records, authorization envelopes:

```bash
# Find type definitions for tokens/receipts/leases
search_files(pattern='interface.*Receipt|interface.*Lease|interface.*Envelope|interface.*Token', target='content', file_glob='*.ts')

# Find validation functions
search_files(pattern='validate.*Receipt|validate.*Lease|verify.*Token|checkAuthority', target='content', file_glob='*.ts')
```

### Step 2 — Field Presence Check

For each authority surface, check which of the 8 fields exist in the type definition:

```
| Surface | Actor | Session | Operation | Args Hash | Expiry | Reversibility | Judgment Ref | Nonce |
|---------|-------|---------|-----------|-----------|--------|---------------|--------------|-------|
| Receipt | ✅ actorId | ✅ sessionId | ✅ toolName | ✅ inputHash | ✅ validUntil | ✅ reversible | ❌ | ❌ |
| AAE     | ✅ actor_id | ❌ | ✅ action_class | ⚠️ intent_hash | ✅ expiry | ✅ reversibility | ❌ | ⚠️ nonce (no tracking) |
| Lease   | ✅ agent_id | ❌ | ✅ scope[] | ❌ | ✅ expires_at | ✅ max_action_class | ❌ | ❌ |
```

### Step 3 — Enforcement Path Trace

For fields that EXIST in the type, verify they're actually validated at runtime:

```typescript
// Check: does validation function actually reject missing field?
if (!receipt.authority?.actorId) violations.push("Missing authority.actorId");
// ↑ HARD GATE — field validated

// vs

nonce: string;  // field exists in type
// but no code checks nonce uniqueness → SOFT FLAG
```

### Step 4 — Cross-System Coherence Check

When multiple authority surfaces exist (common in governed systems), check:
- Do they share the same field semantics? (e.g., "actor" means the same thing)
- Can a token from surface A be used to bypass validation on surface B?
- Is the weakest surface the actual enforcement layer?

### Step 5 — Nonce/Replay Check (Field 8)

The most commonly missing field. Check:
1. Is a nonce generated? (`crypto.randomUUID()`, `Math.random()`)
2. Is there a nonce store? (Set, Map, database table)
3. Is the nonce checked for prior use before execution?
4. Is the nonce consumed (marked as used) after execution?

If nonce is generated but never tracked → **decorative nonce, replay possible**.

### Step 6 — Judgment Reference Check (Field 7)

Check whether the execution token links back to the specific judgment/verdict that authorized it:
- Does the token carry a `judgment_id`, `verdict_id`, or `seal_verdict_id`?
- Does the validation function verify this reference?
- Can a token be forged without a prior judgment?

Common gap: system has `receiptId` (token identity) but no `judgmentId` (what authorized the token).

## Common Findings

| Pattern | Frequency | Severity |
|---------|-----------|----------|
| Nonce generated but never tracked | Very common | HIGH — replay attacks undetected |
| No judgment reference binding | Common | MEDIUM — authority can be detached from judgment |
| Session missing from one surface | Common | MEDIUM — cross-session replay on weakest surface |
| Local fallback bypasses kernel authority | Common in federated systems | HIGH — degraded mode has weaker binding |
| Args hash covers intent but not exact args | Common | LOW — intent-level tamper detection sufficient for most cases |

## Real-World Example: A-FORGE (2026-07-18)

A-FORGE has 3 authority surfaces (ExecutorReceipt, AAE v1, Lease). Results:
- **4/8 fully implemented**: actor, operation, expiry, reversibility
- **2/8 partial**: session (missing from AAE), args hash (intent not exact args)
- **2/8 critically missing**: judgment reference (no field), single-use nonce (generated, never enforced)
- **Cross-system gap**: local lease fallback (`LCL-*` prefix) bypasses kernel authority

## Pitfalls

1. **Don't confuse "field exists" with "field enforced."** A nonce field in a type definition that's never validated is a decoration, not a security property.

2. **Don't confuse "validated at one layer" with "validated at all layers."** If surface A validates nonce but surface B (the weaker one) doesn't, the system is only as strong as surface B.

3. **Local fallbacks are the weakest link.** In federated systems where a local fallback mints tokens when the kernel is unreachable, the fallback often has weaker binding. Always audit the fallback path.

4. **Intent hash ≠ args hash.** An intent hash (BLAKE3 of "deploy webapp") catches intent tampering but not argument tampering (changing the target server). Check which level the system operates at.
