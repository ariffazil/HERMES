---
name: runtime-truth-attestation
description: "Ensure deployed code matches source — detect runtime drift, build wheels, clean-install into venv, purge stale dist-packages, verify import paths, add boot-time attestation. Use when: deploying code, debugging patches that 'should work but don't', checking runtime vs source mismatch, fixing editable-install pollution, setting up one-venv-one-wheel deployment."
tags:
  - deployment
  - runtime-truth
  - wheel
  - attestation
  - E2
  - release-engineering
triggers:
  - "runtime drift"
  - "deploy"
  - "wheel build"
  - "dist-packages"
  - "editable install"
  - "PYTHONNOUSERSITE"
  - "import path mismatch"
  - "source != runtime"
  - "module not found"
  - "patch doesn't work"
  - "stale code running"
  - "triple install"
  - "boot attestation"
  - "release manifest"
  - "forge_session_runtime not found"
  - "FileNotFoundError: Prompt registry"
  - "wheel missing YAML"
  - "MANIFEST.in"
  - "build identity"
  - "git_version mismatch"
  - "cross-organ drift"
  - "health endpoint mismatch"
---

# Runtime Truth Attestation — E2 Pattern

> **Core invariant:** `git commit = built wheel = installed wheel = imported runtime`
> **Anti-pattern:** Copying source files manually into dist-packages or site-packages.
> **DITEMPA BUKAN DIBERI** — Runtime truth is forged, not patched.
> **EUREKA 6-plane alignment:** Runtime truth is the boundary between Source plane (development workspace) and Execution plane (production deploy). When this boundary blurs, every plane downstream loses confidence because no patch claim is verifiable.

## Detecting Runtime Drift

### Cross-Organ Build Identity Check

Not just arifOS — **any organ** can drift. Compare the health endpoint's reported git version against the source tree HEAD:

```bash
# Single organ
DEPLOYED=$(curl -s http://localhost:<PORT>/health | jq -r '.git_version // .build_commit // "UNKNOWN"')
SOURCE=$(cd /root/<REPO> && git rev-parse --short=8 HEAD)
[ "$DEPLOYED" = "geox-$SOURCE" ] || [ "$DEPLOYED" = "$SOURCE" ] \
  && echo "MATCH" || echo "MISMATCH: deployed=$DEPLOYED source=$SOURCE"
```

**When mismatch is found:** The deployed artifact is stale. Rebuild and redeploy — do NOT assume the identity kernel is broken. The health endpoint reports what's running; git rev-parse reports what's on disk. The gap is a build pipeline issue, not a kernel bug.

**Proven:** GEOX 2026-07-19 — deployed `geox-43a706f7` ≠ HEAD `6f895126`. Mid-mission rebuild resolved. At session start the health reported the old version; mid-session it updated to the new one because a background process rebuilt.

### Three-Gate Diagnosis

When `arif_seal` or other governance tools fail despite the code appearing correct, there are usually **three independent gates** blocking, not one:

| # | Symptom | Root Cause | Fix | File:line |
|---|---------|------------|-----|-----------|
| 1 | "Rejected Ed25519 signature on nonce" | Stale nonce (60s window) — mint→sign time drift | Extend window or bind nonce to session_id | `governance_identity.py:145` |
| 2 | "Blocked arif_seal (needs SOVEREIGN)" | INV-1_KERNEL_VERIFIED (kernel_verdict=UNKNOWN) — agent claimed `actor_source=self_report` instead of signed proof | Verify key fingerprints match SOVEREIGN_KEY_IDS | `seq=58-61 traces` |
| 3 | "Capped at OBSERVE_ONLY" | Fresh lease defaults to read-only — needs explicit upgrade | `forge_session_init → forge_lease(max_action_class=EXECUTE_REVERSIBLE)` | `forge_lease scope` |

**Bonus gate (SealTokenQuarantineError):** `seal_token_guard.py` quarantines bare seal token input without domain qualifier (`geological_seal` / `constitutional_SEAL` / `vault_seal`). If "seal" appears in payload without qualifier, raises `SealQuarantineError`.

**Critical EUREKA invariant:** Do NOT fix Gate 3 by setting `runtime_band = SOVEREIGN` when Ed25519 passes. This collapses identity proof into unrestricted runtime permission. The correct fix is a **narrow, single-use, payload-bound vault.append capability**, not global session promotion. See `~/AAA/docs/EUREKA-2026-07-13.md` §A3 Authority Composition.

### Diagnostic Commands

Run this diagnostic to identify how many copies of your code exist and which one is actually loaded:

```bash
echo "=== Source git commit ==="
git -C /root/arifOS rev-parse --short=7 HEAD 2>/dev/null
echo "=== Live deploy git commit ==="
cat /opt/arifos/app/.git_commit 2>/dev/null || echo "no .git_commit file"
echo "=== Health endpoint commit ==="
curl -sf http://localhost:8088/health 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'build_commit={d.get(\"build_commit\",\"?\")} live_commit={d.get(\"live_commit\",\"?\")}')" 2>/dev/null || echo "unreachable"
echo "=== Import path ==="
python3 -c "import arifosmcp; print(arifosmcp.__file__)" 2>&1
echo "=== Site packages ==="
pip show arifos 2>/dev/null | grep -E 'Location|Version'
echo "=== Global dist-packages check ==="
ls /usr/local/lib/python3.13/dist-packages/arifosmcp 2>&1
echo "=== Editable .pth files ==="
find /usr/local/lib/python3.13/dist-packages -name '*.pth' -exec grep -l 'arifos' {} \; 2>/dev/null || echo "none"
echo "=== PYTHONNOUSERSITE ==="
grep -r 'PYTHONNOUSERSITE' /etc/systemd/system/arifos* 2>/dev/null || echo "not set"
```

**Interpretation table:**

| Source ≠ health endpoint | Runtime drift | Build wheel from source, install into venv, restart |
| Import path is NOT inside `/opt/arifos/venv/` | Editable install or global dist | Install wheel, clean .pth files |
| Global dist-packages has `arifosmcp/` directory | Dual install pollution | Remove it |
| `.pth` files with editable hooks | Stale dev install | Remove .pth files |
| `PYTHONNOUSERSITE` not set | User site-packages may override | Add to systemd |

> **Discovered 2026-07-13 EUREKA probe bug:** running `convergence_check.py` from CWD `/root/arifOS` produces false-positive `module_path: FAIL` (import resolves to source tree shadowing the wheel). Always `cd /tmp` before probe, or use the `_probe_python()` helper. See "Pitfalls" below.

## Clean Deployment Workflow (Single Venv, Single Wheel)

### Step 1 — Build wheel from SOT

```bash
cd /root/arifOS  # canonical source tree

# Install build tool if needed
pip install build 2>&1 | tail -1

# Build wheel
python3 -m build --wheel 2>&1 | tail -5
```

**WHEEL-BUNDLING PITFALL:** `python -m build` silently drops non-Python
files. If your service needs YAML/JSON/CSV data files, you MUST add
`MANIFEST.in` at the repo root or the wheel will be missing data files
and the service will crash-loop with `FileNotFoundError`. See
`references/deployment-playbook.md` for the full MANIFEST.in pattern.

### Step 2 — Record release manifest

```bash
WHEEL_HASH=$(sha256sum dist/arifos-*.whl | cut -d' ' -f1)
GIT_COMMIT=$(git rev-parse --short=7 HEAD)

cat > /opt/arifos/release_manifest.json <<EOF
{
  "wheel": "$(basename dist/arifos-*.whl)",
  "wheel_hash": "$WHEEL_HASH",
  "git_commit": "$GIT_COMMIT",
  "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "build_host": "$(hostname)"
}
EOF
```

### Step 3 — Install wheel into production venv

```bash
# Install — replaces editable link with immutable wheel
/opt/arifos/venv/bin/pip install --no-deps --force-reinstall dist/arifos-*.whl
```

### Step 4 — Clean global dist-packages (stale .pth + directories)

```bash
# Remove stale editable .pth hooks
find /usr/local/lib/python3.13/dist-packages -name '*.pth' -exec grep -l 'arifos' {} \; -delete 2>/dev/null

# Remove any stale arifosmcp directory from global dist
rm -rf /usr/local/lib/python3.13/dist-packages/arifosmcp 2>/dev/null

# ALSO remove any editable hooks that point to arifOS workspace
find /usr/local/lib/python3.13/dist-packages -name '*editable*arifos*' -o -name '*.pth' -exec grep -l 'arifos\|DITEMPA\|arifosmcp' {} \; -delete 2>/dev/null
```

### Step 5 — Add PYTHONNOUSERSITE to systemd

```bash
cat > /etc/systemd/system/arifos.service.d/nouser-site.conf <<EOF
[Service]
Environment=PYTHONNOUSERSITE=1
EOF
systemctl daemon-reload
```

### Step 6 — Verify single import path

```bash
/opt/arifos/venv/bin/python -c "
import arifosmcp, pathlib
p = pathlib.Path(arifosmcp.__file__).resolve()
print(f'Import path: {p}')
print(f'Inside approved venv: {\"/opt/arifos/venv\" in str(p)}')
assert '/opt/arifos/venv' in str(p), f'Import path {p} NOT inside approved venv!'
print('✅ Single venv, single wheel verified')
"
```

### Step 7 — Restart and verify

```bash
systemctl restart arifos
sleep 2
curl -sf http://localhost:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
pc = d.get('build_commit','?')
lc = d.get('live_commit','?')
print(f'Build: {pc} | Live: {lc}')
v = d.get('thermodynamic',{}).get('verdict','?')
print(f'Verdict: {v}')
print('✅ Health OK' if v else '❌ Health issue')
"
```

**OR run the full 5-layer check:** `python3 scripts/convergence_check.py`
(see `scripts/convergence_check.py` — exit 0=CONVERGED, 1=DEGRADED, 2=ROLLBACK).

## Boot-Time Attestation

Every production service should expose:

```
python_executable: /opt/arifos/venv/bin/python
package_version: 1!2026.07.11
git_commit: <sha>
wheel_hash: <sha256>
module_path: /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py
runtime_manifest_hash: <sha256 of /opt/arifos/release_manifest.json>
```

**Fail-closed rule:** Service MUST refuse readiness when:
- Multiple `arifosmcp` distributions visible
- `module.__file__` is NOT inside approved venv
- Runtime hash differs from release manifest hash
- `systemd ExecStart` uses unapproved Python

Separate health endpoint fields:
```json
{
  "process_health": "HEALTHY",
  "runtime_alignment": "FAIL",
  "readiness": "BLOCKED"
}
```

## Pitfalls

### PITFALL: wheel silently drops non-Python data files (YAML/JSON/CSV)
If your package runtime loads YAML/JSON/CSV config files, `python -m build`
will exclude them by default. Symptom after deploy: `FileNotFoundError`
crash loop, e.g. `Prompt registry not found at
/opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/registry/prompt_registry.yaml`.

**Fix:** Add `MANIFEST.in` at the repo root with the appropriate globs:

```ini
include arifosmcp/registry/*.yaml
include arifosmcp/registry/*.yml
include arifosmcp/**/*.yaml
include arifosmcp/**/*.json
include arifosmcp/**/*.csv
```

Also enable `include-package-data = true` in `[tool.setuptools]` of `pyproject.toml`.
Do NOT add `[tool.setuptools.package_data]` — newer setuptools (>=70) rejects that
section.

**Verification before restart (3 lines, fails-fast):**
```bash
python3 -c "
import zipfile
z = zipfile.ZipFile('dist/arifos-*.whl')
yamls = [f for f in z.namelist() if f.endswith('.yaml')]
jsons = [f for f in z.namelist() if f.endswith('.json')]
print(f'YAML: {len(yamls)} | JSON: {len(jsons)}')
# Critical: prompt_registry.yaml MUST be present
assert 'arifosmcp/registry/prompt_registry.yaml' in z.namelist(), 'prompt_registry.yaml missing!'
"
```
If expected file missing → fix MANIFEST.in glob → rebuild.

**Recover after a bad deploy** (post-mortem 2026-07-13):
After data files were missing from wheel, the service crash-looped on import. Rather than rebuilding immediately, **copy data directories from source to wheel as a fast rescue**:
```bash
WHEEL=/opt/arifos/venv/lib/python3.12/site-packages/arifosmcp
SRC_BAK=/opt/arifos/app/arifosmcp.bak   # pre-rescue backup
for dir in registry config constitution core data evals policies resources runtime schema schemas tools; do
    [ -d "$SRC_BAK/$dir" ] && cp -r "$SRC_BAK/$dir" "$WHEEL/" 2>/dev/null
done
systemctl restart arifos.service
# Then immediately rebuild wheel + reinstall to make it permanent
```
The `.bak` extension is the critical tag — `.bak` is **excluded from the duplicate-detector** in convergence probes (see `references/convergence-tracker.md` PITFALL: `.bak` directories).

### PITFALL: Editable links survive pip uninstall
Uninstalling an editable install (`pip uninstall`) may remove the metadata but leave the `.pth` file. Always check for `.pth` files manually.

### PITFALL: Global dist-packages take precedence over venv
If `PYTHONNOUSERSITE` is not set, Python's user site-packages (`~/.local/lib/python*/site-packages/`) take priority. System `dist-packages` can also override venv packages. Always set `PYTHONNOUSERSITE=1`.

### PITFALL: Three copies, not two
Typical pollution pattern: (1) editable install in venv, (2) source checkout accessible via venv's editable link, (3) stale global dist-packages from earlier `python3 setup.py install`. The `find .pth` step catches these.

### PITFALL: Health endpoint may report stale build commit
If the health handler hardcodes or caches `build_commit`, it can report an older hash than what's running. The import path and git HEAD are more reliable than the health endpoint.

### PITFALL: Venv `__init__.py` inserts source tree into sys.path (defeats wheel isolation)

The venv's `arifosmcp/__init__.py` (installed by the wheel) contains code that deliberately inserts the source tree at `sys.path[0]`:

```python
# Lines ~20-23 of /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py
if _arifos_root not in _ns_sys.path or _ns_sys.path.index(_arifos_root) > 0:
    if _arifos_root in _ns_sys.path:
        _ns_sys.path.remove(_arifos_root)
    _ns_sys.path.insert(0, _arifos_root)
```

Where `_arifos_root` resolves to `/root/arifOS/`. This means:

- Even after a clean wheel install into the venv, `import arifosmcp` resolves to `/root/arifOS/arifosmcp/__init__.py`, NOT the wheel copy in the venv
- The service runs source tree code regardless of which wheel is installed
- `pip show arifos` reports the venv path, but `python -c "import arifosmcp; print(arifosmcp.__file__)"` reports the source path

**Two fixes:**

**Fix A (quick, production):** Remove the path manipulation from the *installed* venv copy only:
```bash
# Patch the venv's __init__.py to NOT manipulate sys.path
sed -i '/_ns_sys\.path\.insert(0, _arifos_root)/d' /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py
sed -i '/_arifos_root not in _ns_sys\.path/,+3d' /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py
```

**Fix B (permanent):** Remove the path manipulation from the source tree's `__init__.py` before building the wheel, so no future wheel carries it. This may affect development workflows that rely on the source tree being importable from anywhere.

### PITFALL: Deployment directory `.git` HEAD diverges from source (rsync deploy)

When using the rsync fast path (`make deploy-local` or manual rsync), the
deployment directory at `/opt/arifos/app/` may have its own `.git` directory
that diverges from the source repo at `/root/arifOS/`. The health endpoint
reads `live_commit` from the deployment `.git` HEAD, not from the rsynced
files. This causes `runtime_drift: true` even after a successful rsync.

**Symptom:** `build_commit` and `live_commit` differ in `/health` despite
rsync completing successfully. The `.git_commit` marker file shows the
correct commit, but `git -C /opt/arifos/app rev-parse HEAD` shows the old one.

**Fix:**
```bash
# Reset the deployment git HEAD to match source
cd /opt/arifos/app && git reset --hard $(cd /root/arifOS && git rev-parse --short=7 HEAD)

# Restart to pick up
systemctl restart arifos

# Verify
curl -sf http://localhost:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'drift={d.get(\"runtime_drift\")} build={d.get(\"build_commit\")} live={d.get(\"live_commit\")}')
"
```

**Why this happens:** `make deploy-local` rsyncs files but doesn't update the
deployment directory's git HEAD. The `.git_commit` marker is updated but the
actual `.git/HEAD` still points to the old commit. The health endpoint reads
from `.git/HEAD`, not from `.git_commit`.

**Prevention:** After rsync, always run `git reset --hard <commit>` in the
deployment dir, or use the full wheel-based deploy path which doesn't have
this issue.

**Proven:** 2026-07-16 kernel audit — runtime_drift was TRUE despite source
and deployment being functionally identical. The `.git` HEAD in the deploy
dir was 2 commits behind source.

### PITFALL: Service import resolves to source tree, not wheel, when WorkingDirectory = source tree

When the systemd service uses `WorkingDirectory=/opt/arifos/app` and an
`ExecStart` with `python -c "from module import ..."`, Python puts `''`
(the current working directory) as `sys.path[0]`. Since the source tree
`/opt/arifos/app/arifosmcp/` exists, imports resolve from source, NOT
from the wheel in the venv.

This causes two classes of failure:

**Class 1: Source tree files are root-only (`-rw-------`)**
The wheel build creates files owned by root. If the source tree has files
with `-rw-------` (root-only), the service user (`arifos`) gets
`PermissionError` on import. The symptom is a crash immediately after
restart.

**Fix:** After building/installing a wheel, check for root-only files in
the source tree and chmod them:
```bash
find /opt/arifos/app/arifosmcp -type f -not -perm /o+r -exec chmod o+r {} \;
chown -R arifos:arifos /opt/arifos/app/arifosmcp 2>/dev/null
```

**Class 2: Wheel and source tree drift apart**
If the source tree has different code than the wheel, the service runs
source tree code even though the wheel was just built. This is why
`runtime_matches_build=false` appears in the health endpoint.

**Structural fix:** Add `-P` (safe path) to the Python invocation to
prevent cwd from being added to `sys.path[0]`:
```bash
ExecStart=/opt/arifos/venv/bin/python -P -c "from arifosmcp.runtime.__main__ import main; main()"
```

Or use `sys.path.remove('')` in the entry point.
`pip show arifos` reports the *first* distribution found in `sys.path`, not necessarily the one that `import arifosmcp` actually loads. Always verify with `python3 -c "import arifosmcp; print(arifosmcp.__file__)"`.

## Convergence Tracker — 9-Layer Pattern

Beyond the basic 5-layer check, production deployments need a structured
**convergence receipt** that maps multiple surface comparisons into one
verdict. The 9-layer pattern emerged from P1.2 (2026-07-13):

```
Mandatory (5) — FAIL collapses overall CONVERGED:
  source          — git commit, branch, dirty flag
  artifact        — installed dist-info version, package SHA256
  installation    — only one installable distribution (count duplicates, .bak excluded)
  import          — key modules resolve from approved site-packages
  process         — sys.executable realpath under approved roots

Conditional (4) — UNREACHABLE does NOT collapse overall:
  service         — systemd active, executable matches approved root
  tool_registry   — health endpoint reachable, 8 tools, stable hash
  database_schema — alembic/migrations or external DB schema resolvable
  vault_writer    — VAULT chain operational, seal count > 0
```

**Layer dataclass:** each probe returns a `ConvergenceLayer` with
`name`, `state` (enum), `observed_value`, `expected_value`,
`evidence_ref`, `failure_code`, `checked_at`.

**Overall state propagation:**
1. If all mandatory layers CONVERGED → overall = CONVERGED regardless of conditional UNREACHABLE
2. If any mandatory layer non-CONVERGED → overall = the worst priority state:
   UNREACHABLE > UNKNOWN_ARTIFACT > DUPLICATE_INSTALL > MODULE_PATH_MISMATCH > MANIFEST_MISMATCH > SOURCE_AHEAD > ... > VAULT_WRITER_DRIFT

**Anti-collapse rule for conditional layers:** UNREACHABLE on
database_schema or vault_writer must NOT collapse overall — the action
may not need DB or sealing. UNREACHABLE means "couldn't probe"; it is
distinct from FAILURE.

**Reusable script structure** (proven 2026-07-13 in `/opt/arifos/venv/bin/python3 -m arifosmcp.runtime.convergence_tracker`):
- Module with `track_convergence()` returning `ConvergenceReport`
- `Telemetry` class with class-method `record()` updating counters
- `report.to_receipt()` produces VAULT999-ready envelope
- CLI entry point dumps JSON for piping to other tools

**Critical fix pattern:** the duplicate-detector must distinguish
**actual importable distributions** from **development source trees**.
The source tree at `/root/arifOS/arifosmcp/` is present for development
but NOT imported by the running service. A probe that counts it as a
duplicate is wrong; a probe that doesn't run an actual import check is
also wrong. The right check is `sys.path` inspection from a fresh
subprocess with cwd NOT inside the source tree:
```python
r = subprocess.run(
    ["/opt/arifos/venv/bin/python3", "-c",
     "import sys; sys.exit(0 if any('/root/arifOS' in p and 'venv' not in p for p in sys.path) else 1)"],
    capture_output=True, timeout=5, cwd="/tmp",
)
```
Exit code 0 means the source tree is being imported from cwd — drift.
Exit 1 means it's properly isolated.

See `references/convergence-tracker.md` for the full implementation.

## arifOS rsync Deploy (Fast Path)

The standard wheel-based deploy (Steps 1-7 above) is the canonical path. But for rapid iteration during development, arifOS supports a fast rsync path. **Use only for T1 (reversible) changes.**

```bash
# 1. Commit + push source
cd /root/arifOS && git add -A && git commit -m "feat: ..." && git push origin main

# 2. rsync source to deploy dir (skipping wheel build)
rsync -av --exclude='.git' --exclude='__pycache__' \
    /root/arifOS/arifosmcp/ /opt/arifos/app/arifosmcp/

# 3. Fix permissions
chmod -R u+rwX,go+rX /opt/arifos/app/arifosmcp/

# 4. Restart
systemctl restart arifos

# 5. Verify
curl -sf http://localhost:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin)['status'])"
```

**Why this works:** The arifOS service's editable install points `/root/arifOS/arifosmcp` → venv. But the service runs from `/opt/arifos/app/` (WorkingDirectory). rsync syncs the deploy dir with source.

**Pitfall:** `make deploy-local` has a prove gate that runs the full proof pack. For quick patches, rsync directly. The prove gate is for production deploys, not iteration.

**Pitfall:** The arifOS editable install (`__editable___arifos_1_2026_7_11_finder.py`) maps to `/root/arifOS/arifosmcp` — NOT `/opt/arifos/app/arifosmcp`. The service uses the deploy dir, not the editable link. Changes to `/root/arifOS/` alone are NOT live until rsynced.

## File References

- Release manifest: `/opt/arifos/release_manifest.json`
- Systemd drop-in: `/etc/systemd/system/arifos.service.d/nouser-site.conf`
- Wheel dist dir: `/root/arifOS/dist/`
- Production venv: `/opt/arifos/venv/`
- Source (SOT): `/root/arifOS/`
- Health endpoint: `http://localhost:8088/health`

## Linked Files

- **Deployment playbook** — `references/deployment-playbook.md`: pre-deploy YAML-bundling fix (MANIFEST.in), post-deploy 5-layer verification, ceremony canary for A3 narrow-capability path
- **Convergence check script** — `scripts/convergence_check.py`: standalone 5-layer verification, exit code 0=CONVERGED / 2=ROLLBACK
- **Convergence tracker pattern** — `references/convergence-tracker.md`: 9-layer architecture with mandatory/conditional split, `.bak` convention, adversarial test matrix pattern, telemetry counters, acceptance gate pattern
- **Adversarial test runner** — `scripts/adversarial_test_matrix.py`: reusable fail-closed test harness with JSON persistence, used for P1.3/P1.4 verification