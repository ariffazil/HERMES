# Shadow Probe Session — 2026-07-29

## What was done

Three workstreams on arifOS kernel fixes:

### Workstream 1: Deployment state in health checks

Added `DEPLOYMENT` state to `seven_state_health()` in `observatory_routes.py`. Previously the health endpoint never checked deployment drift despite `/ready` correctly degrading on drift (the rule in `build.py` line 177 was unenforced).

**New behavior:** When `_compute_runtime_drift()` returns `runtime_drift=True`, or when source/built/deployed commits disagree, DEPLOYMENT reports `"down"` with confidence 0.99. Otherwise `"aligned"`.

### Workstream 2: actor_verified single source of truth

**Bug:** `session_birth.actor_verified` was a duplicate field in a dict literal — could independently drift from the top-level `actor_verified` param. The `_ATTENTION` field in `tools.py` only checked envelope values, never compared against result.

**Fix:**
1. `session_birth.actor_verified` now reads `bool(actor_verified)` with a comment marking it as a derived view
2. Self-audit assertion added before `return out` in `_project_light()`
3. (Planned) `_ATTENTION` in `tools.py` should compare envelope vs result values

### Workstream 3: Shadow probe — real APEX measurement in INIT

**Bug:** `unmeasured_apex()` always returned G=UNMEASURED, C_dark=UNMEASURED, W3=UNMEASURED, h=UNMEASURED. INIT had no real measurement.

**Fix:** Created `arifosmcp/tools/shadow_probe.py` providing `probe_shadow(model_input, reference_domain)`:
- G: Contradiction scan (GEOX proxy or text word-count fallback)
- C_dark: Character-level adaptive entropy
- h: Humility classification via phrase pattern matching
- W3: Evidence source counting (URLs, citations, evidence IDs)
- Falls through to `unmeasured_apex()` on failure

Wired into `_project_light()` — when `intent` is provided, runs probe first; falls through only on probe failure.

## Files created

- `arifosmcp/tools/shadow_probe.py` — 9557 bytes

## Files modified

- `arifosmcp/runtime/rest_routes/observatory_routes.py` — added DEPLOYMENT state
- `arifosmcp/tools/session.py` — actor_verified fix, shadow probe wiring, self-audit assertion, merge conflict fixes (4 conflicts)
- `arifosmcp/runtime/sct.py` — `unmeasured_apex` docstring marked FALLBACK ONLY
- `arifosmcp/runtime/rest_routes/rest_routes.py` — merge conflict fixes (3 conflicts)

## Pre-existing merge conflicts

Both `session.py` (~132 markers) and `rest_routes.py` (~243 markers) had numerous pre-existing merge conflict markers from an incomplete merge of commit `67fb82d5e`. Only conflicts in or adjacent to the patched functions were resolved.

## Not completed (ran out of iterations)

1. `tools.py` `_ATTENTION` logic fix — still checks only envelope, doesn't cross-reference with result
2. `ruff check && ruff format && pytest` — not run
3. Git commit — not done
