# Live Floor Score Benchmarks — arifOS Kernel

> Captured 2026-07-10. Source: `curl :8088/health` direct probe.

## What Clean State Looks Like (2026-07-10)

```
runtime_drift:  false ✅
contract_drift: false ✅
build_commit:   198398c == live_commit: 198398c ✅
git_dirty:      null ✅
surface:        CONSISTENT — 11/11 tools match canonical hash ✅
```

## Live Floor Scores (2026-07-10 @ 12:44 UTC)

| Floor | Score | Classification | Status |
|-------|-------|---------------|--------|
| F1  AMANAH | **0.5** | hard | ⚠️ HALF — true failure |
| F2  TRUTH | 0.99 | hard | ✅ |
| F3  NAMING | 0.75 | soft-doctrinal | ⚠️ |
| F4  CLARITY | -0.0 | hard | ✅ |
| F5  PEACE² | 1.0 | hard | ✅ |
| F6  MARUAH | 0.7 | soft | ⚠️ |
| F7  ANTI-BEHAVIOR-SINK | **0.04** | hard | ✅ (correct by design) |
| F8  GENIUS | 0.8 | derived | ✅ |
| F9  ANTI-HANTU | **0.0** | hard | ✅ (optimal) |
| F10 BOUNDARY | 1.0 | hard | ✅ |
| F11 BRIDGE | 1.0 | hard | ✅ |
| F12 INEQUALITY | **0.425** | hard | ⚠️ BELOW 0.5 — true fail |
| F13 SOVEREIGN | 1.0 | hard | ✅ |

## Known-Good Ranges (These Are NOT Failures)

- **F7 0.03–0.05** → ✅ Correct by design. Anti-behavior-sink calibrated low means the system isn't gaming itself.
- **F9 < 0.30** → ✅ Correct. 0.0 = zero hallucination detected, which is optimal.
- **F4 = -0.0** → ✅ Correct. Entropy reduction achieved.

## True Failure Thresholds

| Floor | True Fail Below |
|-------|----------------|
| F1  AMANAH | 0.80 |
| F2  TRUTH | 0.80 |
| F3  WITNESS | 0.80 |
| F5  PEACE² | 0.80 |
| F6  MARUAH | 0.80 |
| F8  GENIUS | 0.80 |
| F10 BOUNDARY | 0.80 |
| F11 AUDIT | 0.80 |
| F12 INJECTION | 0.80 |
| F13 SOVEREIGN | 0.80 |

## F1=0.5 vs F12=0.425 — What These Actually Mean

**F1 0.5 = "AMANAH half"**: The reversibility gates exist but are not fully enforced. This is a *constitutional scoring* issue, not a code-drift issue. Redeploying will not fix it. Requires kernel-level F1 audit to raise.

**F12 0.425 = "INEQUALITY below 0.5"**: Injection sanitization is incomplete. External content not fully flagged. Requires F12 audit of MCP input paths.

**Rule discovered (2026-07-10):** Clearing runtime drift fixes runtime_drift. It does NOT fix constitutional scoring gaps. These are orthogonal problems.

## Endpoint Cheatsheet

| Endpoint | Returns | Use For |
|----------|---------|---------|
| `GET /health` | `runtime_floors`, `thermodynamic`, `surface_consistency`, `build_commit`, `live_commit`, `runtime_drift`, `contract_drift` | ✅ Floor scores, drift, build sync |
| `GET /api/status` | Metadata + empty `runtime_floors` | ❌ Do NOT use for floor scores |
| `GET /health?detail=full` | Everything above + diagnostic tools | Verbose debug only |
