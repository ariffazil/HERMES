# APEX Baseline Audit — 2026-07-06

## Quantitative Drift (pre-fix)

| Organ | README Count | AGENTS.md Count | Drift | Fixed |
|-------|-------------|-----------------|-------|-------|
| arifOS | kernel | kernel | 0 | — |
| A-FORGE | 72 | 79 | -7 | ✅ |
| AAA | 11 | 11 | 0 | — |
| GEOX | 54 | 35 | +19 | ✅ |
| WEALTH | 26 | ~45 | -19 | ✅ |
| WELL | 22 | 22 | 0 | — |

## APEX Quantum Scores (post-fix)

| Organ | A | P | E | X | Φ | G | C_dark | Verdict |
|-------|---|---|---|---|---|---|---|---|
| arifOS | 0.7 | 0.9 | 0.8 | 0.9 | 0.9 | 0.408 | 0.014 | SEAL |
| A-FORGE | 0.8 | 0.8 | 0.9 | 0.8 | 0.7 | 0.323 | 0.032 | SEAL |
| AAA | 0.7 | 0.8 | 0.7 | 0.9 | 0.8 | 0.282 | 0.028 | SABAR |
| GEOX | 0.8 | 0.9 | 0.8 | 0.7 | 0.8 | 0.323 | 0.024 | SEAL |
| WEALTH | 0.8 | 0.9 | 0.9 | 0.7 | 0.8 | 0.363 | 0.024 | SEAL |
| WELL | 0.7 | 0.9 | 0.6 | 0.7 | 0.9 | 0.238 | 0.021 | SABAR |

**Federation G (max):** 0.408 (arifOS). **C_dark max:** 0.032 (A-FORGE). **Verdict: SEAL.**

## Key Findings

1. GEOX had worst drift (+19, inflated by backward-compat aliases)
2. WEALTH had worst negative drift (-19, tools added but README not updated)
3. WELL is actually complete — has Quick Start, Architecture, Authority boundary
4. A-FORGE was 7 tools behind (72→79)
5. All organs pushed and aligned after fix
