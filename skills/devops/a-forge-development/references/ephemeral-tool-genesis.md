# Ephemeral Tool Genesis — Operational Reality

**Forged 2026-07-30** (architecture). **Updated 2026-08-02** (operational proof via canary).

## Canonical Engine

`src/infrastructure/tools/EphemeralGenesis.ts` (~1310 lines) — singleton via `getEphemeralGenesis()`.

## API Signatures (verified 2026-08-02)

```typescript
generate(templateId: string, params: Record<string, unknown>, sessionId: string, actorId: string, missionIntent: string): Promise<GenesisResult>
sandboxTest(toolId: string, testInput?: Record<string, unknown>): Promise<GenesisResult>
invoke(toolId: string, args: Record<string, unknown>): Promise<GenesisResult>
verify(toolId: string, verifierMethod: VerifierMethod, ctx?: VerifierContext): Promise<GenesisResult>
retire(toolId: string): Promise<GenesisResult>
proposePromotion(templateId: string): { shouldPropose: boolean; count: number; threshold: number }
```

**Pitfall:** `generate()` takes positional args, NOT an object. First arg is templateId string.

## Templates (8 registered, verified 2026-08-02)

| Template ID | Type | Implementation format | Sandbox path |
|---|---|---|---|
| mulerouter_image_gen | api_wrapper | JSON config | curl in bwrap |
| mulerouter_tts | api_wrapper | JSON config | curl in bwrap |
| mulerouter_music | api_wrapper | JSON config | curl in bwrap |
| mulerouter_vision | api_wrapper | JSON config | curl in bwrap |
| generic_api_wrapper | api_wrapper | JSON config | curl in bwrap |
| data_parser | data_parser | Raw JS function string | node in bwrap |
| compute_fn | compute_fn | Raw JS function string | node in bwrap |
| format_converter | format_converter | Raw JS function string | node in bwrap |

## Implementation Format Duality (Gap 8, fixed 2026-08-02)

**api_wrapper** templates emit `JSON.stringify({url, method, headers, body, timeoutMs, authRef})`.
**Code-generating** templates emit raw JS: `(input) => { ... }`.

`buildNonApiLauncher()` (line ~577) handles both:
1. Try `JSON.parse(implementation)` → if success, use `{language, code}` path
2. If parse fails AND `templateType` is in approved set (`data_parser`, `compute_fn`, `format_converter`) → wrap in Node.js runner
3. If parse fails AND type NOT approved → throw fail-closed error

**Invoke args unwrapping:** Code templates expect raw values, but `invoke()` sends `{input: ...}`. The launcher unwraps: `const input = (raw && 'input' in raw) ? raw.input : raw;`

## Sandbox

Uses bubblewrap (`/usr/bin/bwrap`, v0.11.0). Policy: `READONLY_BUILD`. No network access unless lease explicitly grants `allowedDomains`. Sandbox logs: `[sandbox:provision]`, `[containment:bwrap]`, `[sandbox:complete]`, `[sandbox:deprovision]`.

## Promotion Gate

`EvidencePromotionGate.ts` thresholds:
- minInstances: 5
- minSuccessRate: 0.95
- minIndependentVerifierPasses: 3
- minEmpiricalCapabilityScore: 0.80

**P1-AA patch (2026-08-02):** `computeEmpiricalScore()` in EphemeralGenesis.ts computes score from:
- instantiation_count ≥ 5 → 0.25
- success_rate × 0.35
- independent_verifier_passes ≥ 3 → 0.25
- verifier diversity → 0.15
Max = 1.0. Promotion NOT automatic — requires F13 sovereign ratification.

## Canary Procedure (verified 2026-08-02)

```javascript
const { getEphemeralGenesis } = require('./dist/src/infrastructure/tools/EphemeralGenesis.js');
const g = getEphemeralGenesis();
const gen = await g.generate('data_parser', { format: 'csv', sample: 'a,b\n1,2' }, 'session', 'ARIF', 'canary');
const st = await g.sandboxTest(gen.tool.id, 'a,b\n1,2');
const inv = await g.invoke(gen.tool.id, { input: 'a,b\n1,2' });
const ver = await g.verify(gen.tool.id, 'schema_invariant');  // needs schema param
const promo = g.proposePromotion('data_parser');
const ret = await g.retire(gen.tool.id);
```

## Canary Results (2026-08-02, post-Gap-8 fix)

Full lifecycle canary — data_parser (csv):

| Step | Result | Evidence |
|---|---|---|
| GENERATE | ✅ | id=eph_data_parser_*, hash recorded, state=generated |
| SANDBOX_TEST | ✅ | bwrap exit=0 wall=77ms |
| INVOKE | ✅ | bwrap exit=0 wall=59ms receipt=e3b0c44298fc1c14 |
| VERIFY | ⚠️ | "no schema supplied" (expected — schema_invariant needs schema param) |
| PROMOTION | ✅ | shouldPropose=false count=1/5 (gated correctly) |
| RETIRE | ✅ | cleaned |

Multi-template verification (all SANDBOX ✅ INVOKE ✅):
- data_parser(csv), compute_fn(sum), compute_fn(stats), format_converter

Fail-closed verification:
- Malformed code string → exit=1, fail-closed ✅
- Unsupported template type with non-JSON impl → exit=1, fail-closed ✅
- api_wrapper regression → sandbox works, DNS blocked = correct network policy ✅

## Gap Status (2026-08-02)

| Gap | Description | Status |
|---|---|---|
| 1 | No agent actually calls forge_ephemeral | CRITICAL — open |
| 2 | empirical_capability_score = 0.0 forever | FIXED (P1-AA) |
| 3 | worldModelTraining/multiModelEvaluator disconnected | HIGH — open |
| 4 | MCP not network-accessible (stdio only) | HIGH — open |
| 5 | Templates all MuleRouter | FIXED (8 templates) |
| 6 | 3 duplicate EphemeralGenesisRunner files | MEDIUM — open |
| 7 | No end-to-end promotion tested | LOW — gate works |
| 8 | Code-string templates crash sandbox_test | FIXED (2026-08-02) |

## Test Infrastructure

Tests use `node:test` (NOT vitest). Some test files have pre-existing module resolution issues (`.js` imports from `.ts` files). Run with: `node --test test/ephemeralComputeFn.test.ts`

## Build

```bash
cd /root/A-FORGE && npx tsc --noEmit  # type check
cd /root/A-FORGE && npx tsc            # build dist/
```

**Critical:** After patching source, MUST rebuild dist/ before canary. Stale dist/ = canary tests old code.

## Doctrine

```
Agent Zero gives the agent a computer.
A-FORGE gives the federation a forge.
Temporary by default. Evidence before permanence. Retirement as normal. Promotion as earned.
```
