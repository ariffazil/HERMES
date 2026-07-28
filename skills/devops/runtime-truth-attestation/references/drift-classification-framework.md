# Drift Classification Framework — Cosmetic vs Executable-Code

> **Proven:** 2026-07-28 — arifOS health endpoint showed `drift=true` while all 16 critical modules had identical hashes across 3 surfaces.
> **Core insight:** Git commit string comparison is NOT the right drift invariant. Module hash comparison IS.

## The Three-Surface Hash Invariant

The only reliable drift check: compare sha256 of every critical runtime module across three surfaces simultaneously.

| Surface | Location | Source |
|---------|----------|--------|
| **Health report** | `health_endpoint.software_release.critical_module_hashes` | Kernel computes at boot |
| **Source tree** | `/root/<organ>/<module_path>` | `sha256sum` directly |
| **Deployed path** | `/opt/<organ>/app/<module_path>` | `sha256sum` directly |

### Critical module selection

Not every file matters. Select modules that are:
1. Loaded at import time (not lazy) — if they're corrupt, the service fails immediately
2. Core to the organ's constitutional function
3. Likely to change between commits

For arifOS, the 16 critical modules include: `session.py`, `judge.py`, `forge.py`, `crypto_auth.py`, `authority.py`, `interceptor.py`, `boot_attestation.py`, `governance_pipeline.py`, `forge_preflight.py`, `phoenix_72.py`, `cooling_verbs.py`, `convergence_tracker.py`, `forge_session_runtime.py`, `governance_identity.py`, `rest_routes.py`, `kernel/judge.py`.

### Verification pattern

```bash
# Fetch health endpoint module hashes
HEALTH_HASHES=$(curl -sf http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
c = d.get('software_release', {}).get('critical_module_hashes', {})
for k, v in c.items():
    print(f'{k}  {v.split(\":\")[1] if \":\" in v else v}')
")

# Compare against source tree
SOURCE_HASHES=$(find /root/arifOS -name '*.py' -path '*/arifosmcp/tools/*' -o -path '*/arifosmcp/runtime/*.py' | sort | while read f; do
    echo "$(basename $(dirname $f))/$(basename $f)  $(sha256sum $f | cut -d' ' -f1)"
done)

# If ALL hashes match -> COSMETIC DRIFT (deploy metadata only)
# If ANY hash differs -> EXECUTABLE-CODE DRIFT (real code divergence)
```

## Classification Table

| Evidence | Classification | Action |
|----------|---------------|--------|
| All critical module hashes IDENTICAL across all 3 surfaces | **COSMETIC METADATA DRIFT** | Update `.git_commit` marker only. No rebuild needed. |
| Source hash ≠ deployed hash, but both ≠ health report | **EXECUTABLE-CODE DRIFT** | Rebuild wheel, reinstall, restart. The running code differs from source. |
| Health report can't fetch hashes (field missing) | **INSUFFICIENT DATA** | Probe directly via sha256sum on source + deployed paths. |
| Hashes match but health reports `drift=true` | **FALSE POSITIVE** | Git commit string comparison is stale. Fix per the three-drift-field pattern below. |

## The Three-Drift-Field Contradiction Pattern

The arifOS health endpoint has **three independent drift checks** that can contradict each other:

```json
{
  "deployment_drift_status": "aligned",      // _check_deployment_drift() — source vs deployed git
  "runtime_drift": false,                     // _check_runtime_drift() — module vs build
  "software_release": { "drift": true }       // build.py — source_commit[:7] != built_commit[:7]
}
```

| Field | Computation | Source of `built_commit` | Source of `source_commit` |
|-------|------------|--------------------------|---------------------------|
| `deployment_drift_status` | `_check_deployment_drift()` in `health_routes.py` | Deployed `.git_commit` file | Source `.git/HEAD` |
| `runtime_drift` | `_check_runtime_drift()` in `runtime_verify.py` | Build registry hash | Runtime module hash |
| `software_release.drift` | `build.py` comparing `source_commit[:7] != built_commit[:7]` | `built_commit` from `software_release.source_commit` (hardcoded release_id prefix) | `built_commit` from live `git rev-parse HEAD` |

**Root cause of `software_release.drift=true` when code is correct:**
- `source_commit` reads from `release_id` (hardcoded string like `arifos-88f5eb7d4f3c` from the deploy epoch)
- `built_commit` reads from `git rev-parse HEAD` at runtime (live source HEAD)
- If source advanced past the deploy epoch, these differ — but the editable install means the running code IS the latest source
- The `release_id` is a metadata artifact, not a code pin

### Fixing the false positive

```bash
# Update the deployment marker to match live HEAD
HEAD=$(git -C /root/arifOS rev-parse HEAD)
echo "$HEAD" > /opt/arifos/app/.git_commit
echo "$HEAD" > /opt/arifos/app/arifosmcp/.git_commit

# No systemctl restart needed — editable install already runs HEAD code.
# The marker update is cosmetic: the drift flag clears on next health probe.
```

## Cross-Organ Metadata Propagation

**Finding (2026-07-28):** GEOX's health endpoint reports `deployment_drift.drift=true` with the same hash mismatch, because it probes arifOS's `/api/build-info`. This means:

- **Organ B can inherit arifOS's metadata drift** even if Organ B's own code is perfectly aligned
- When investigating drift on any federation organ, check whether it reads from its own build metadata OR proxies arifOS's
- GEOX specifically reports: `source: "arifOS:/api/build-info + /root/arifOS/.git HEAD (P0-5 GEOX-side probe)"` — it reads from arifOS endpoint, not from its own git

**Diagnostic:**
```bash
# Check if drift is cross-organ propagated
curl -sf http://127.0.0.1:8081/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
dd = d.get('deployment_drift', {})
src = dd.get('source', 'unknown')
print(f'GEOX drift source: {src}')
print(f'GEOX drifts: {dd.get(\"drift\")}')
print(f'GEOX source_commit: {dd.get(\"source_commit\",\"?\")[:12]}')
print(f'GEOX built_commit: {dd.get(\"built_commit\",\"?\")[:12]}')
print(f'GEOX deployed_commit: {dd.get(\"deployed_commit\",\"?\")[:12]}')
"
```

If GEOX's drift source says `arifOS:/api/build-info`, the drift is an arifOS metadata issue, not a GEOX code issue.

## Editable Install Nuance

When the organ uses an **editable install** (`pip install -e .`, `uv sync --editable`, or a `.pth` file pointing to source):

- The Python runtime imports FROM THE SOURCE TREE, not from a wheel
- The deployment marker (`.git_commit`) is NEVER automatically updated when source commits advance
- The health endpoint's `built_commit` (from live git HEAD) and `deployed_commit` (from marker) WILL diverge
- But the running code IS the latest source — there is NO actual code drift
- **Fix is purely cosmetic:** update the marker. No rebuild. No redeploy. No restart.

**Detection:**
```bash
# Is this an editable install?
/opt/arifos/venv/bin/pip show arifos 2>/dev/null | grep -i editable
# Output: "Editable project location: /root/arifOS" → YES, editable install
# No output → wheel-based install (different drift rules apply)
```

## Pitfall: Don't conflate metadata freshness with code correctness

Just because `drift=true` in the health endpoint does NOT mean the code is wrong. The correct sequence is:

1. Check critical module hashes across all 3 surfaces → establishes ACTUAL drift
2. If hashes match → it's cosmetic metadata drift → update the marker
3. If hashes differ → it's executable-code drift → rebuild and redeploy
4. Never try to "fix" drift by rebuilding a wheel when hashes already match — you're just making work

## When to Use This Framework

- Health endpoint shows `drift=true` but the system seems to work fine
- Multiple organs report the same drift signature
- After an rsync deploy that didn't update the marker
- Before chasing identity/authority bugs that might be deployment artifacts
