# Ed25519 Identity Gap — Debugging Pattern

> Captured 2026-07-19. Verified by independent kernel probe.

## The Pattern

When an agent claims "identity gap closed, actor_verified=True" but the live kernel probe
shows `actor_verified: false`, the gap is NOT in the crypto — it's in the **code path**.

## The Bug (arifOS session.py)

The `mode="light"` path has an auto-sign block (lines 1320-1368) that verifies localhost
calls by signing the challenge nonce with the local Ed25519 key. This works: arif, forge,
opencode, hermes all verify via `mode="light"`.

The `mode="init"` path does NOT have the auto-sign block. It skips verification entirely.
Most agent harnesses call `mode="init"` for boot — so they get OBSERVE_ONLY.

## Root Cause

Copy-paste gap between two modes. The fix is one code block (~50 lines) from light→init.
Blast radius: LOW. Reversibility: FULL. T1 AUTO-DO.

## How to Verify

1. **Canary probe (always anon):** `arif_init(mode="canary")` → should return OBSERVE_ONLY.
   This is correct behavior — canary is observation only.

2. **Light probe (auto-signs):** `arif_init(mode="light", actor_id="kimi")` → should return
   LIMITED_MUTATE if the agent is registered.

3. **Init probe (MISSING auto-sign):** `arif_init(mode="init", actor_id="kimi")` → currently
   returns OBSERVE_ONLY (bug). Should return LIMITED_MUTATE after fix.

## Red Flags When Auditing Identity Claims

- ✅ "Tests pass" → check which function was tested (crypto_auth.py in isolation vs MCP transport)
- ✅ "actor_verified=True" → check which mode was used (mode="light" vs mode="init")
- ✅ "Identity gap closed" → check ALL 8 agents, not just sovereign
- ✅ "11/11 PASS" → check what the tests actually test (function-level vs integration-level)

## The Principle

Code exists ≠ code is reached. Crypto works ≠ every mode path calls it.
When one mode works and another doesn't, the gap is always a missing call site — never a crypto failure.
