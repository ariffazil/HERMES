# F7 Gödel Lock Implementation

> **Source:** `/root/A-FORGE/src/domain/governance/godelLock.ts`
> **Tests:** `/root/A-FORGE/test/godelLock.test.ts`
> **Runs on:** Every MCP tool response in A-FORGE (Express middleware + direct wrapper)

## Constitutional Basis

- **F7 HUMILITY** — No autonomous agent can certify absolute certainty under Gödel's First Incompleteness Theorem.
- **Gödel Gate (Lock #1)** — External witness must verify self-SEAL. The F7 Gödel Lock is the *code* that enforces this at the output layer.

## Constants

| Symbol | Value | Meaning |
|--------|-------|---------|
| `MIN_UNCERTAINTY` | 0.03 | Floor of Gödel uncertainty band |
| `MAX_UNCERTAINTY` | 0.05 | Ceiling of Gödel uncertainty band |
| `MAX_CONFIDENCE` | 1 - 0.03 = 0.97 | Structural maximum; claims above this are blocked |

## API

### `applyGodelLock(input: GodelLockInput): GodelLockOutput`

Core gate. Input → output pipeline:

1. If `claimedConfidence > MAX_CONFIDENCE` (0.97) → `godelBlocked: true` with F7 VIOLATION reason
2. Otherwise: inject `uncertainty = random(MIN_UNCERTAINTY, MAX_UNCERTAINTY)` using `crypto.randomBytes` for flat distribution
3. Append `[Ω₀ = {uncertainty}] Gödel Lock (F7): this output carries mandatory uncertainty...` to content
4. Auto-downgrade epistemic label:
   - No label → SPECULATIVE
   - OBSERVED (internal) → DERIVED
   - All others preserved
5. Strip absolute certainty phrases: `100%` → `97% (structural max)`, `absolutely certain` → `highly (within Gödel bound)`, `guaranteed` → `strongly indicated (Gödel bound applies)`

### `extractUncertaintyContribution(output: GodelLockOutput): number`

Returns `Ω₀` for use in the E dial of `G = (A × P × E × X)^(1/4)`.

### `createGodelMiddleware(): Express middleware`

Overrides `res.json` to inject `_godelLock` field with `{uncertainty, epistemicLabel, f7Timestamp}` into every JSON response. Blocked outputs return 400-level error with `_godelLock.blocked: true`.

### `applyGodelLockToToolResponse(response): Record<string, unknown>`

Direct wrapper for non-Express MCP response chains. Injects `_godelLock` envelope.

## Test Profile (15 tests, all pass)

| Test | Assertion |
|------|-----------|
| rejects claims with confidence > 0.97 | `claimedConfidence: 1.0` → blocked |
| rejects claims with confidence exactly 0.98 | `claimedConfidence: 0.98` → blocked |
| accepts claims with confidence ≤ 0.97 | `claimedConfidence: 0.97` → passes |
| accepts claims with no confidence | no `claimedConfidence` → passes with uncertainty |
| appends uncertainty band to every output | output contains `Ω₀ =`, `Gödel Lock`, `mandatory uncertainty` |
| auto-downgrades no label → SPECULATIVE | missing epLabel → `SPECULATIVE` |
| auto-downgrades OBSERVED → DERIVED | internal `OBSERVED` → `DERIVED` |
| preserves DERIVED/INTERPRETED/SPECULATIVE | labels survive unchanged |
| F7 is not overridable | any claimedConfidence > 0.97 always blocked |
| cryptographic randomness | 100 calls produce ≥2 unique uncertainty values |
| strips certainty language | `100% certain` → `97% (structural max)` |
| valid f7Timestamp | every output has parseable ISO date |

## Key Design Decisions

1. **crypto.randomBytes** for uncertainty generation, not Math.random(). Ensures non-deterministic output even in deterministic execution environments.
2. **Two-layer certainty stripping**: regex replace BEFORE suffix append so the Gödel annotation itself never gets double-processed.
3. **No override mechanism** — not even the sovereign can bypass the Gödel bound (F7 is a mathematical invariant, not a policy). Changing the band requires a constitutional floor modification (F1–F13 amendment path), which itself requires F13 Ed25519 signature.
