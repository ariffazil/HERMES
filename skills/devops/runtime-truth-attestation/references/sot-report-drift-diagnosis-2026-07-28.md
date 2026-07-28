# SOT Report — Drift Diagnosis + Marker Correction

**Proven 2026-07-28** — Complete State-of-Truth report for cosmtic metadata drift on arifOS kernel.

## Session Summary

Arif observed `software_release.drift = true` on the arifOS health endpoint. Three commits were involved:

- **source_HEAD** = `711f8f5ff` (live git HEAD)
- **deployment_marker** = `88f5eb7d4` (`/opt/arifos/app/.git_commit`, last written Jul 18)
- **health source_commit** = `88f5eb7d4` (read from marker)
- **health built_commit** = `711f8f5ff` (read from live HEAD)

## Report Structure Arif Received

### Commit Chain Table
| Field | Value | Source |
|---|---|---|
| source_HEAD | `711f8f5ff` | `git rev-parse HEAD` |
| health source_commit | `88f5eb7d4` | Release metadata |
| health built_commit | `711f8f5ff` | Live git HEAD |
| health deployed_commit | `88f5eb7d4` | `.git_commit` file |
| deployment_marker | `88f5eb7d4` | Last written Jul 18 |

### Code Identity (sha256 comparison)
| Module | Health | Source | Deployed | Match? |
|---|---|---|---|---|
| session.py | `657bba5c` | `657bba5c` | `657bba5c` | ✅ |
| judge.py | `fbd6492d` | `fbd6492d` | `fbd6492d` | ✅ |
| forge.py | `6c4ba19a` | `6c4ba19a` | `6c4ba19a` | ✅ |
| crypto_auth.py | `73547523` | `73547523` | `73547523` | ✅ |
| +12 more | ... | ... | ... | ✅ all 16 |

### Git Ancestry
88f5eb7 → ANCESTOR of 711f8f5 → NORMAL FORWARD DRIFT
Diff: ~400 files, 0 runtime .py changes (docs/CI/configs only)

### Classification
COSMETIC METADATA DEBT — NOT executable code drift

### Remediation Options (A/B/C/D/E)
- **A)** Rebuild artifact — unnecessary, no code divergence
- **B) ✅ CHOSEN** — Update `.git_commit` marker only
- **C)** Hash-based drift detection — architecturally correct, separate patch
- **D)** Ed25519 identity verify — independent, nonce pending
- **E)** Leave as documented debt — LOW risk

### 8-Point Verification After Fix
| # | Check | Before | After |
|---|-------|--------|-------|
| 1 | `.git_commit` | 88f5eb7d4 | 711f8f5ff ✅ |
| 2 | source_commit | 88f5eb7d4 | 711f8f5ff ✅ |
| 3 | built_commit | 711f8f5ff | 711f8f5ff ✅ |
| 4 | deployed_commit | 88f5eb7d4 | 711f8f5ff ✅ |
| 5 | deployment_drift_status | aligned | aligned ✅ |
| 6 | software_release.drift | true | false ✅ |
| 7 | arifOS health | healthy | healthy ✅ |
| 8 | GEOX proxy drift | true | false ✅ |

### Collateral Damage
arifFlow restarted (dependency restart) — FQ reset from 2.0 to 0.0 STUCK, 0 receipts.
Known gap: arifFlow does not persist FlowReceipts to disk.

## Key Lessons

1. **Drift flag is F2 TRUTH, not a bug** — the system honestly reports metadata mismatch
2. **Three independent drift fields** can contradict each other in a single health response
3. **GEOX proxies arifOS build-info** — fixing arifOS heals GEOX drift report too
4. **Always classify before fixing** — cosmetic vs executable is the critical distinction
5. **Mark the `.git_commit` file with `git rev-parse HEAD`, never `cp .git/HEAD`** — the latter copies the `ref:` prefix
