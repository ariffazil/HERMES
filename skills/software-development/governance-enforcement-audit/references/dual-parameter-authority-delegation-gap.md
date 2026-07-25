# Dual-Parameter Authority Delegation Gap

**A-FORGE forge gate seal_verdict_id audit — July 2026**

## Pattern

When a system declares TWO parameters that both carry an F13 (sovereign/unreversible) burden, but only ONE of them is cryptographically verified, the unverified parameter is a **decoration** — any non-empty string bypasses the gate.

## The Gap

| Parameter | Declared Purpose | Actual Verification | Verdict |
|---|---|---|---|
| `seal_verdict_id` | "Required for arifos domain — F13 SOVEREIGN" | Truthiness check only (non-empty string?) | **Shape-check — not crypto** |
| `constitutional_chain_id` | "Authorization chain from arif_judge SEAL" | Delegated to `arif_judge validate` mode (Ed25519-backed) | **Crypto — real enforcement** |

The system is NOT broken overall — `constitutional_chain_id` is properly crypto-verified via arifOS. But `seal_verdict_id` is declared as an independent F13 gate and is enforced solely by `!args.seal_verdict_id` — any truthy string passes.

## Code Paths

### Presence-only checks of `seal_verdict_id`

**File: `src/interfaces/mcp/forgeTools.ts` — Line 997**
```ts
if (args.domain === "arifos" && !args.seal_verdict_id) {
    return { status: "DORMANT", ... message: "...requires seal_verdict_id..." };
}
```

**File: `src/domain/forge/skill/skillForge.ts` — Line 213**
```ts
if (irreversibleDomains.includes(req.domain) && !req.seal_verdict_id) {
    return { status: "DORMANT", ... message: "...requires seal_verdict_id..." };
}
```

Both check only: is the string truthy? Any non-empty value — including a randomly generated UUID — passes the gate.

### Real crypto verification of `constitutional_chain_id`

**File: `src/interfaces/mcp/core.ts` — Lines 1287–1369**
```ts
// Step 1: presence check (line 1287)
if (!constitutional_chain_id) {
    return { verdict: "VOID", error_code: "FORGE_GATE_NO_AUTHORIZATION" };
}

// Step 2: delegated crypto validation via arif_judge (line 1307)
const validationResult = await callMCP("arifos.arif_judge", {
    mode: "validate",
    constitutional_chain_id,
    judge_state_hash,
    ...
});
// Checks: chain_valid, judge_hash_matches, candidate_matches,
//         actor_matches, replay_safe, execution_grant
```

### Where `seal_verdict_id` flows (never validated)

- `forgeSkill()` passes it to `sealToVault()` where it's **stored as metadata** in a JSON file (`.runtime/vault/seals/seal_*.json`, line 398)
- `forge_evaluate` passes it through as an opaque field (line 1330)
- `forge_skill` MCP handler passes it through to `forgeSkill()` (line 1025)
- `register.ts` — **never reads it at all**; the four registration gates (GATE, WITNESS, HARAM, SCAR) don't reference it

## Root Cause

The `seal_verdict_id` was designed as a token from the arifOS judge+seal pipeline — the expectation being "arifOS issued it, so it's valid by provenance." But in A-FORGE, the value is never **returned to arifOS for verification**. It's treated as an opaque trust token whose validity is assumed from the caller.

Meanwhile, `constitutional_chain_id` IS sent to arifOS for full ED25519-backed validation, including replay protection (`replay_safe`), actor binding (`actor_matches`), and candidate binding (`candidate_matches`).

## How to Fix

Two options, depending on design intent:

1. **Eliminate `seal_verdict_id` as a separate parameter.** Merge its semantic burden into `constitutional_chain_id`. The chain already carries the judge → seal verdict reference; `seal_verdict_id` is redundant.

2. **Validate `seal_verdict_id` against arifOS.** Before accepting it, call `arif_judge validate` with the seal_verdict_id to verify it's a real, non-revoked verdict from the constitutional kernel. Currently no such call exists.

## When This Pattern Matters in Audits

When auditing a governed system with multiple declared authorization parameters:

1. **Identify every declared constraint parameter** — especially F13-labeled ones.
2. **Trace each one's verification path independently.**
3. **Check if they all route through a single crypto-verified parameter** while the rest are decorations.
4. **Classify each independently** — don't assume that because one parameter has real crypto, all do.

Common variants of this gap:
- An `auth_token` that's just a non-empty string check while `signature` is properly verified
- A `session_token` that's presence-checked while `actor_signature` carries the real crypto
- A `verdict_id` that's stored-but-never-validated alongside a `chain_id` that's verified against a remote oracle

## Related

- Governance Enforcement Audit skill — Pitfall #1: "Don't confuse 'field exists' with 'field enforced'"
- This is a concrete example of pitfall #1 extended: **"Don't confuse 'field X is enforced' with 'a different field Y is enforced'."**

## Source

Audited 2026-07-25: `/root/A-FORGE/src/` — `forgeTools.ts`, `skillForge.ts`, `core.ts`, `register.ts`, `client.ts`
