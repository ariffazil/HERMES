# Deployment Reversion Diagnosis

> **When:** A service keeps reverting to old code despite manual file edits, rsync, or wheel installs.
> **Claim:** "I changed the files but the runtime doesn't reflect it."
> **First question:** "Which copy is the runtime actually loading? Prove it."

## The Chain (trace in this order)

```
systemd unit → ExecStart → Python binary → sys.path → module.__file__ → git HEAD → build_info
```

### Step 1 — systemd unit

```bash
systemctl cat <service>.service
```

**What to check:**
- `ExecStart=` — which Python binary? Which entry point?
- `WorkingDirectory=` — this becomes `sys.path[0]` (cwd) unless `-P` flag used
- `User=` — which user context? Affects file permissions
- `EnvironmentFile=` — env overrides
- `Environment=` — PYTHONNOUSERSITE, PATH overrides

**Drop-ins:** Files in `/etc/systemd/system/<service>.service.d/*.conf` are applied AFTER the main unit and can OVERRIDE any directive.

```bash
ls /etc/systemd/system/<service>.service.d/
systemctl show <service>.service -p Environment | tr ' ' '\n' | sort -u
```

**Critical check:** Look for environment variables that override Python module defaults (e.g., `ARIFOS_ALLOW_FREE_NONCE=1` overriding `crypto_auth.py`'s default of `0`).

### Step 2 — Python binary and module path

```bash
# Find the running process
pgrep -f '<service-entry-point-string>'

# Or use systemd
systemctl show <service>.service -p MainPID
PID=$(systemctl show <service>.service -p MainPID | cut -d= -f2)

# Get the actual Python binary
cat /proc/$PID/cmdline | tr '\0' ' '

# Get the Python path
cat /proc/$PID/environ | tr '\0' '\n' | grep -E '^PATH|^PYTHON'
```

**Confirm which Python resolves your module:**

```bash
# Use the service's Python, not the system one!
/opt/<service>/venv/bin/python -c "
import <mymodule>
print('Module file:', <mymodule>.__file__)
print('Module dir:', pathlib.Path(<mymodule>.__file__).parent)
"
```

**Expected:** Path inside `/opt/<service>/venv/`. If it resolves to a source tree (`/root/<repo>/`), the wheel isolation is defeated (see Pitfalls in SKILL.md).

### Step 3 — sys.path resolution order

```bash
/opt/<service>/venv/bin/python -c "
import sys
for i, p in enumerate(sys.path):
    print(f'{i}: {p}')
"
```

**Critical check:** Is the source tree BEFORE the venv's site-packages? If so, source tree shadows the wheel.

**Why this happens:**
- `WorkingDirectory` = source tree root → `''` (cwd) at `sys.path[0]` → `import <mymodule>` finds `/opt/<service>/app/<module>/` first
- `arifosmcp/__init__.py` has `sys.path.insert(0, /root/arifOS/)` which defeats isolation
- Editable `.pth` file in site-packages points to source tree

### Step 4 — git HEAD vs health endpoint

```bash
# Source git HEAD
SOURCE_HASH=$(git -C /root/<repo> rev-parse HEAD)

# Running module's git HEAD
IMPORT_PATH=$(/opt/<service>/venv/bin/python -c "import <mymodule>; print(<mymodule>.__file__)")
MODULE_DIR=$(dirname "$(dirname "$IMPORT_PATH")")
RUNTIME_HASH=$(git -C "$MODULE_DIR" rev-parse HEAD 2>/dev/null || echo "no-git")

# Health endpoint hashes
HEALTH=curl -sf http://localhost:<port>/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
r = d.get('software_release', {})
print(f'source={r.get(\"source_commit\",\"\")[:12]}')
print(f'built={r.get(\"built_commit\",\"\")[:12]}')
print(f'deployed={r.get(\"deployed_commit\",\"\")[:12]}')
print(f'drift={r.get(\"drift\")}')
"

echo "Source HEAD: $SOURCE_HASH"
echo "Runtime HEAD: $RUNTIME_HASH"
echo "Health:"
echo "$HEALTH"
```

**Interpretation:**

| Pattern | Meaning |
|---------|---------|
| `source=built=deployed` | Aligned. Drift claim is likely about `build_info.py` hardcoded hash |
| `source≠built` | Merge commit: one field reads first parent, other reads actual HEAD |
| `source≠deployed` | Rsync path: `.git/HEAD` in deploy dir is stale |
| Module file ≠ venv path | `__init__.py` sys.path manipulation is active |
| Module file inside source tree | CWD or editable install shadows the wheel |

### Step 5 — build_info.py staleness

If `source=built=deployed` but `drift=true`, check:

```bash
cat /root/<repo>/<module>/runtime/build_info.py
# Look for hardcoded BUILD_COMMIT string
```

If `build_info.py` has a hardcoded hash from months ago, the health endpoint's `software_release` block reads git HEAD separately but some other code path may use the stale `build_info.py`. The drift might be cosmetic — the code is correct but the metadata is stale.

### Step 6 — Wheel content verification

```bash
cd /root/<repo>
# Build fresh
python3 -m build --wheel

# Verify wheel content matches source
WHEEL=$(ls dist/*.whl)
python3 -c "
import zipfile
with zipfile.ZipFile('$WHEEL') as z:
    # Check the critical file
    try:
        content = z.read('arifosmcp/path/to/keyfile.py').decode()
        assert 'expected_feature' in content
        print('✅ Wheel has expected feature')
    except KeyError:
        print('❌ Wheel MISSING key file')
"

# Install into venv
/opt/<service>/venv/bin/pip install --no-deps --force-reinstall "$WHEEL"

# Verify post-install
/opt/<service>/venv/bin/python -c "
import <module>
import pathlib
p = pathlib.Path(<module>.__file__)
assert '/opt/<service>/venv' in str(p), f'NOT in venv: {p}'
print(f'✅ Module resolves from venv: {p}')
"
```

## Full diagnostic one-liner

```bash
SVC=arifos; PORT=8088; REPO=/root/arifOS; MOD=arifosmcp; VENV=/opt/arifos/venv
echo "=== systemd ===" && systemctl cat $SVC.service | head -5
echo "=== Python ===" && cat /proc/$(systemctl show $SVC.service -p MainPID | cut -d= -f2)/cmdline 2>/dev/null | tr '\0' ' '
echo "=== Module ===" && $VENV/bin/python -c "import $MOD; print($MOD.__file__)"
echo "=== Git ===" && git -C $REPO rev-parse HEAD
echo "=== Health ===" && curl -sf http://localhost:$PORT/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
r=d.get('software_release',{}); print(f'source={r.get(\"source_commit\",\"\")[:12]} built={r.get(\"built_commit\",\"\")[:12]} deployed={r.get(\"deployed_commit\",\"\")[:12]} drift={r.get(\"drift\")}')"
```

## Common root causes

1. **Partial rsync** — Only some files copied. The running source tree has mismatched signatures between caller and callee → `TypeError: unexpected keyword argument`

2. **Wheel vs source tree shadowing** — `__init__.py` inserts source tree into sys.path. Wheel install appears successful but runtime loads source tree code.

3. **Stale `.git` in deploy directory** — Rsync copies files but doesn't update `.git/HEAD`. Health endpoint reads `.git/HEAD` → reports old commit → `drift=true`.

4. **Systemd drop-in overrides** — A drop-in sets an env var that overrides a Python module default (e.g., `ARIFOS_ALLOW_FREE_NONCE=1`).

5. **Merge commit divergence** — After merging, `source_commit` reads from first parent but `built_commit` reads from actual HEAD → cosmetic drift.
