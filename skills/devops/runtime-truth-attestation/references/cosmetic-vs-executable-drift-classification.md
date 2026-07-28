# Cosmetic vs Executable Drift Classification

> Proven 2026-07-28 — arifOS kernel drift diagnosis session.

## Session Context

Arif observed `software_release.drift = true` on the arifOS health endpoint. The system reported:
- **source_commit:** `88f5eb7d4f3c` (from `/opt/arifos/app/.git_commit`)
- **built_commit:** `711f8f5ff2fe` (from `/root/arifOS/.git` HEAD)
- **deployed_commit:** `88f5eb7d4f3c` (set = source_commit)
- **drift:** `true`

## Root Cause

The `.git_commit` stamp file was written at deploy time (commit `a999446cf`, Jul 17) and was never bumped after ~240 subsequent commits. The file does not exist in git tracking at any commit — it's a **deploy-time artifact**, not a version-controlled file.

## The Critical Insight: `build.py` Priority Chain

The `build.py` module (`/root/arifOS/arifosmcp/runtime/build.py`, lines 190-237) reads `source_commit` and `built_commit` from **different sources**:

```
source_commit:
  Priority 1: /opt/arifos/app/.git_commit  (stamp file, static)
  Priority 2: $DEPLOY_GIT_COMMIT / $ARIFOS_BUILD_SHA env vars
  Priority 3: /root/arifOS/.git/HEAD        (live git state)

built_commit:
  Always:     /root/arifOS/.git/HEAD        (live git state, line 143)

deployed_commit:
  Always:     Set = source_commit           (line 144)
```

Since `source_commit` reads from a static stamp and `built_commit` reads from live git HEAD, any commit made after the last stamp write causes `drift=true` — even if the running code is identical.

## Code Identity Verification

All 4 key deployed files had identical md5sums to source HEAD:
- `tools/session.py`: `dfff65c3` (same)
- `tools/judge.py`: `f8b9a44f` (same)
- `runtime/kernel/judge.py`: `580ded3c` (same)
- `runtime/boot_attestation.py`: `9ce860a4` (same)

## Git Ancestry

```
88f5eb7d4f3c  (deployed)  →  ...240 commits...  →  711f8f5ff  (HEAD)
  "forge: auto-remediation pipeline"                "[ZEN] auto-wrap: seal session"
                                                        ↑ ANCESTOR (normal forward drift)
```

No `arifosmcp/*.py` files changed between the two commits — only docs, CI workflows, and config files.

## Classification

**VERDICT: COSMETIC METADATA DEBT** — not executable code drift.

The drift flag is correct behavior (F2 TRUTH): the system honestly reports that its recorded metadata doesn't match live git state. The flag is not a bug — it's the system doing its job.

## Arif's Decision Pattern

When presented with this data, Arif chose the following decision flow:
1. **Diagnose first** — SOT report produced
2. **Classify** — cosmetic vs executable
3. **Recommend options** — A/B/C/D/E without execution
4. **Choose** — Arif picks one path

The options presented were:
- **A)** Rebuild artifact from HEAD
- **B)** Redeploy source (rsync + restart)
- **C)** Update health metadata only (bump `.git_commit`)
- **D)** Rotate/verify identity (Ed25519 nonce signing)
- **E)** Leave drift as known cosmetic debt
