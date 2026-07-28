# Deployment Coherence Debugging — F13 Challenge Auth

> **Proven runtime beats source inspection.** This file captures the multi-location
> deployment debugging pattern from the 2026-07-25 session.

## Symptom

Code is correct in `git diff`, unit tests pass, but the live service still runs old
code. After `cp` or `pip install`, the service doesn't load the new functions.

## Root Cause

arifOS imports `arifosmcp` from THREE possible locations, checked in priority order:

```
sys.path[4] = /opt/arifos/venv/lib/python3.13/site-packages/
              └── arifosmcp/   ← installed wheel (LOADED FIRST)

sys.path[0] = ""  (CWD = /opt/arifos/app/)
              └── arifosmcp/   ← manual sync / make deploy-local (SECOND)

/opt/arifos/venv/.../site-packages/arifos/
              └── __getattr__ → arifosmcp  ← namespace bridge (THIRD, fallback only)
```

Patching `/opt/arifos/app/arifosmcp/` (location #2) has **no effect** if the
venv wheel (location #1) still has old code. The venv is loaded first because
site-packages precedes the empty-string CWD in `sys.path`.

## The Reversion Trap

`pip install --force-reinstall --no-deps` builds the wheel from the CURRENT
git HEAD. If the feature branch has a merge conflict or stale code, the wheel
reinstalls the OLD code to `/opt/arifos/venv/lib/.../site-packages/`,
silently restoring the old behavior.

**This is why `git checkout --` appeared to "revert" files:** the checkout
switched branches, then the next `pip install` deployed from the new (old) HEAD.

## Verification Protocol

```bash
# 1. Source tree has the code?
grep -c 'issue_authorization_challenge' /root/arifOS/arifosmcp/runtime/crypto_auth.py

# 2. Venv site-packages has the code?
/opt/arifos/venv/bin/python -c "
from arifosmcp.runtime.crypto_auth import issue_authorization_challenge
print('VENV: OK')
" 2>&1 || echo "VENV: MISSING"

# 3. CWD deploy has the code?
grep -c 'issue_authorization_challenge' /opt/arifos/app/arifosmcp/runtime/crypto_auth.py

# 4. The LOADED module has the code?
/opt/arifos/venv/bin/python -c "
import arifosmcp.tools.arif_kernel_intercept as ki
import inspect
src = inspect.getsource(ki._arif_kernel_intercept)
print('f13_failure_code:', 'f13_failure_code' in src)
print('loaded from:', ki.__file__)
"
```

## Deployment Alignment (health endpoint)

```
source_commit == built_commit == deployed_commit
drift == false
runtime_drift == false
```

NOTE: `built_commit` is the hash of the *build artifact* (wheel), not a git commit.
`drift=true` when `built` ≠ `source` is NORMAL for wheel-based deploys.
`runtime_drift` checks loaded-code vs deployed-metadata — this is the real signal.

## The Fix (apply to ALL three locations)

```bash
# 1. Ensure feature branch has correct code
cd /root/arifOS && git checkout feat/f13-challenge-auth-20260725
# Cherry-pick from main if needed: git cherry-pick <main-sha>
# Resolve conflicts with --theirs for our files

# 2. Build wheel and install to venv
python3 -m build --wheel
/opt/arifos/venv/bin/pip install --force-reinstall --no-deps dist/arifos-*.whl

# 3. Sync to CWD deploy
rsync -a --delete arifosmcp/tools/ /opt/arifos/app/arifosmcp/tools/
rsync -a --delete arifosmcp/runtime/crypto_auth.py /opt/arifos/app/arifosmcp/runtime/crypto_auth.py
rsync -a --delete arifosmcp/runtime/tools.py /opt/arifos/app/arifosmcp/runtime/tools.py

# 4. Update deployment marker
git rev-parse HEAD > /opt/arifos/app/.git_commit

# 5. Restart
systemctl restart arifos
sleep 6
```

## Learnings

- `_arif_kernel_intercept` signature needs `session_id: str | None = None` in
  ALL three location copies
- `tools.py` needs `session_id=session_id` in the `await _arif_kernel_intercept(...)` call
- The venv's `arif_kernel_intercept.py` is the AUTHORITATIVE copy — patching elsewhere
  is wasted effort if the venv still has old code
- After `cherry-pick`, verify `grep -c` for the new functions; merge conflicts can
  silently drop entire functions
- `build_info.py` has a hardcoded `BUILD_COMMIT` that never updates — ignore it
