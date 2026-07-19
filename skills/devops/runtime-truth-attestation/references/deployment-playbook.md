# Runtime Truth Attestation — Deployment Playbook

> Field-tested sequence from 2026-07-13 E2 deployment. Use this as the
> canonical pre-deploy checklist + post-deploy verification.

---

## Symptom: arifOS crash-looping after wheel install

If `journalctl -u arifos` shows `FileNotFoundError: Prompt registry not
found at /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/registry/prompt_registry.yaml`
in a restart loop:

**Root cause:** wheel did not bundle YAML/data files. `python -m build`
silently drops files that are not Python modules.

**Two-step fix:**

### Step A — Add MANIFEST.in

The wheel build uses `MANIFEST.in` to bundle non-Python files. Create at
repo root (`/root/arifOS/MANIFEST.in`):

```bash
cat > /root/arifOS/MANIFEST.in <<'EOF'
include arifosmcp/registry/*.yaml
include arifosmcp/registry/*.yml
include arifosmcp/**/*.yaml
include arifosmcp/**/*.json
include arifosmcp/**/*.csv
EOF
```

Also enable package-data in `pyproject.toml`:
```toml
[tool.setuptools]
include-package-data = true
```

**Do NOT** add `[tool.setuptools.package_data]` — newer setuptools (>=70)
rejects this section. Use `MANIFEST.in` instead.

### Step B — Stop loop, rebuild, reinstall, restart

```bash
systemctl stop arifos
cd /root/arifOS
rm -f dist/*.whl
python3 -m build --wheel 2>&1 | tail -5
sha256sum dist/arifos-*.whl  # record as new wheel_hash
/opt/arifos/venv/bin/pip install --no-deps --force-reinstall dist/arifos-*.whl
ls /opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/registry/prompt_registry.yaml
# If MISSING: the YAML was not bundled — check MANIFEST.in glob
systemctl restart arifos
sleep 5
curl -sf http://localhost:8088/health | python3 -m json.tool | head -10
```

**Verification that YAML actually got bundled** (before reinstalling):
```bash
python3 -c "
import zipfile
z = zipfile.ZipFile('/root/arifOS/dist/arifos-*.whl')
yamls = [f for f in z.namelist() if f.endswith('.yaml')]
print(f'YAML files in wheel: {len(yamls)}')
for f in sorted(yamls): print(f'  {f}')
"
```

If `prompt_registry.yaml` not in list → MANIFEST.in glob wrong → fix glob → rebuild.

---

## Post-deploy: 5-layer Runtime Verification

After every wheel-based restart, run all five layers. ANY failure = rollback.

```bash
echo '=== L1: Module Path ==='
/opt/arifos/venv/bin/python -c "
import arifosmcp, pathlib
p = pathlib.Path(arifosmcp.__file__).resolve()
print(f'  path: {p}')
print(f'  in venv: {\"/opt/arifos/venv\" in str(p)}')
" 2>&1 | grep -v 'MemoryEngine\|deprecated'
# PASS: in venv = True

echo '=== L2: Package Metadata ==='
/opt/arifos/venv/bin/pip show arifos 2>&1 | grep -E 'Version|Location'
# PASS: Location = /opt/arifos/venv/lib/python3.12/site-packages

echo '=== L3: Source/Runtime Drift ==='
SOURCE=$(git -C /root/arifOS rev-parse HEAD)
echo "  source HEAD: $SOURCE"
# Runtime commit comes from /health endpoint:
curl -sf http://127.0.0.1:8088/health 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  runtime git_commit: {d.get(\"git_commit\",\"?\")}')
print(f'  runtime path: {d.get(\"runtime_path\",\"?\")}')"
# ACCEPTABLE: source-ahead documented as non-blocking if uncommitted patches exist

echo '=== L4: Duplicate Distribution ==='
find /usr/local/lib/python3.13/dist-packages -name 'arifosmcp' -type d 2>/dev/null | wc -l
# PASS: 0
# Source path leaks in venv python sys.path:
/opt/arifos/venv/bin/python -c "
import sys; print(sum(1 for p in sys.path if '/root/arifOS' in p))" 2>/dev/null
# PASS: 0

echo '=== L5: Critical Imports ==='
/opt/arifos/venv/bin/python -c "
for n in ['arifosmcp.runtime.forge_session_runtime',
          'arifosmcp.runtime.governance_identity',
          'arifosmcp.runtime.constitutional_map',
          'arifosmcp.registry']:
    try: __import__(n); print(f'  ok {n}')
    except Exception as e: print(f'  FAIL {n}: {e}')" 2>&1 | grep -v 'MemoryEngine\|deprecated'
# PASS: all ok
```

If all 5 layers pass → mark **CONVERGED**. If L1 or L4 fail → rollback immediately.

---

## Ceremony Canary (A3 narrow capability verification)

After runtime convergence, verify the A3 narrow capability path works —
sovereign key + Ed25519 signature on nonce + payload-bound single-use
capability. **Do not** check that sovereign key alone escalates the session.

```bash
# 1. Session init returns challenge nonce
NONCE_RESP=$(curl -sf -N -X POST http://127.0.0.1:8088/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"arif_init",
                 "arguments":{"mode":"init","actor_id":"ARIF"}}}' 2>&1)
echo "$NONCE_RESP" | python3 -c "
import json,sys
d = json.loads(sys.stdin.read())
inner = json.loads(d['result']['content'][0]['text'])
nonce = inner.get('meta',{}).get('challenge_nonce','MISSING')
auth = inner.get('authority',{}).get('runtime_authority','?')
print(f'  nonce: {nonce[:24]}...')
print(f'  band:  {auth}')
print(f'  next:  {inner.get(\"meta\",{}).get(\"next_safe_action\",\"?\")[:60]}')"
# EXPECT: nonce present, band=OBSERVE_ONLY, next_safe_action mentions signing nonce
```

**CORRECT A3 behavior:** Kernel returns nonce + `next_safe_action` saying
"Sign the nonce with your Ed25519 key and re-init with nonce+signature for
full sovereign authority." This is the narrow path — verification must be
provided BEFORE runtime authority upgrades.

**WRONG A3 behavior (red flag):** If the kernel returns `authority: SOVEREIGN`
or `mutation_allowed: true` based on a claimed actor_id without signature,
that is the "sovereign identity = unrestricted runtime" anti-pattern. Roll back.

---

## File Locations (for forensic comparison)

| Purpose | Path |
|---|---|
| Source (SOT) | `/root/arifOS/` |
| Live deploy clone | `/opt/arifos/app/` (often stale, behind SOT) |
| Production venv | `/opt/arifos/venv/` |
| Wheel dist dir | `/root/arifOS/dist/` |
| Release manifest | `/opt/arifos/release_manifest.json` |
| systemd unit | `/etc/systemd/system/arifos.service` |
| nouser-site drop-in | `/etc/systemd/system/arifos.service.d/nouser-site.conf` |
| VAULT chain | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |
| Crash log | `journalctl -u arifos -n 30 --no-pager` |