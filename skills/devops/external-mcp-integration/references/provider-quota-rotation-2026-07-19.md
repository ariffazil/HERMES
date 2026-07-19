# Provider Quota Exhaustion & Rotation Protocol (2026-07-19)

## Context

Session diagnosed MiMo Token Plan quota exhaustion across two VPSes (af-forge + A-FLOW), rotated 3 agents to working providers, and cleaned stale config.

## The Pattern

```
1. Symptom: Agent returns HTTP 429 "quota exhausted" or generic "Something went wrong"
2. Probe: curl the /models endpoint (auth check) + /chat/completions (inference check)
3. Cross-check: compare keys across VPSes — same key = shared quota = both exhausted
4. Identify: which providers are actually working? (MiniMax worked, MiMo dead)
5. Rotate: switch primary provider → clean fallbacks → remove stale model aliases → restart
6. Verify: health check on gateway, test inference
```

## Key Learnings

- **Auth ≠ Quota**: `GET /models → 200` proves the key is valid. `POST /chat/completions → 429` means it has no tokens. Both can be true.
- **Shared quota**: Token Plan keys are per-account, not per-VPS. Same key on two machines = shared pool.
- **Stale aliases block startup**: Removing a dead provider from `primary` and `fallbacks` is not enough. Stale entries in `models.*` dict cause OpenClaw to auto-load plugins that fail at startup.
- **OpenClaw doesn't source vault.env**: Must start with `source /root/.secrets/vault.env && /usr/bin/node ...`. Without this, any provider with a key reference (even dead ones) blocks startup with `SecretRefResolutionError`.

## Verdict

Triaged and resolved. Moved OpenClaw from `xiaomi-coding/mimo-v2.5-pro` (dead) → `minimax/MiniMax-M2.7` (working). Cleaned 3 xiaomi-coding aliases from `models.*`. Moved OpenClaw on A-FLOW (WawaBot) was already on MiniMax — unaffected. Hermes was already on DeepSeek — also unaffected. Only af-forge OpenClaw needed the rotation.

## Cross-VPS Key Audit

| VPS | Provider | Key | Status |
|-----|----------|-----|--------|
| af-forge (72.62.71.199) | MiMo Token Plan | `tp-sleu41me6...wfbo` | Quota exhausted |
| A-FLOW (72.61.126.65) | MiMo Token Plan | `tp-sleu41me6...wfbo` | Same key, same exhaustion |
| af-forge | MiniMax | `sk-cp-...UgO4` | ✅ Working |
| af-forge | DeepSeek V4 Pro | Direct API | ✅ Working |
| A-FLOW | MiniMax | Different key (OpenClaw native) | ✅ Working (WawaBot) |
