# Kernel Contrast Assessment — Version Upgrade Audit Pattern

> **Pattern:** Structured before/after comparison across 7 axes to assess what changed between two kernel versions, release tags, or deployment states.
> **Proven:** 2026-07-27 — comparing v2026.06.11-FIQHGEOM vs v2026.07.24-ZEN-SURVIVAL
> **Falsifiable against:** `curl :8088/health`

## When to Use

When asked to evaluate "what changed" after a kernel upgrade, release tag bump, or major commit. Produces an honest delta without relying on release notes (which are often incomplete or aspirational).

## The 7 Axes

| Axis | Probes | Evidence source |
|------|--------|-----------------|
| **1. Shadow** | Apex scalars: G, C_dark, W3, h — measured vs unmeasured | `/health` → `apex_scalars` |
| **2. Surface** | Tool count, registry vs facade, internal filtered | `tools/list`, `/health` → `surface_consistency` |
| **3. Identity** | actor_verified, authority ceiling, self-audit assertions | `arif_init` response, `session_token.allowed` |
| **4. Forge gate** | Preflight, governance pipeline, cooling verbs | `tools/list`, `forge_preflight` |
| **5. Deployment** | Drift fields, source vs built vs deployed | `/health` → `software_release`, `runtime_drift`, `deployment_drift_status` |
| **6. Contradiction** | Known gaps, surface divergences, internal vs external tool count | `/health` → `known_gaps`, `surface_consistency.divergences` |
| **7. Falsification** | Kill Matrix, contradiction scan, evidence truth classes | GEOX tools, health endpoint |

## Template

```
## ⚔️ KERNEL CONTRAST — Apa Yang Berubah

### Sebelum (<old_version>)
| Aspek | Keadaan |
|---|---|
| Shadow | ... |
| Surface | ... |
| Identity | ... |
| Forge gate | ... |
| Deployment | ... |
| Contradiction | ... |
| Falsification | ... |

### Sekarang (<new_version>)
| Aspek | Keadaan |
|---|---|
| Shadow | ✅✅/⚠️ |
| Surface | ✅/⚠️ |
| ... | ... |

### 🔥 Yang Masih Kacau
1. ...
2. ...
3. ...

### ❌ Contradictions Yang Patut VOID/HOLD
| Contradiction | Kenapa | Tindakan |
|---|---|---|
| ... | ... | ... |

### 🏆 Survival of the Fittest Tools
| Yang Bertahan | Yang Gugur |
|---|---|
| tool_A | tool_X → absorbed |
| tool_B | tool_Y → internal |

### The One-Line Verdict
```
```

## Pitfalls

- **Release name is not capability.** A version bump may be cosmetic (bug fixes only) or semantic (new floors, new tools). Probe each axis independently.
- **Healthy endpoint ≠ everything working.** The health endpoint reports what it's designed to report, not all gaps. Always check `known_gaps` field.
- **Tool list from MCP vs from health.** MCP `tools/list` returns public facade; health endpoint reports registry count. If they differ, some tools are diagnostic/internal.
- **`drift` field may contradict other drift fields.** See `runtime-truth-attestation` skill's health endpoint self-contradiction pitfall.
- **`UNMEASURED` is different from `0.0`.** G=0.0 (MEASURED) means the heuristic ran and computed zero — a real measurement with a real value. G=UNMEASURED means the probe was never called — no data. Treat them differently.
