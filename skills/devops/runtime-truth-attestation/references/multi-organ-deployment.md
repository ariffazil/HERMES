# Multi-Organ Deployment — Federation-Wide Pattern

> For arifOS-specific deployment (Python wheel → venv), see `SKILL.md` and `references/deployment-playbook.md`.
> This covers the other 5 federation organs.

## The Core Problem

Every organ has up to **three code locations** that can drift apart:

| # | Location | Source | Priority in sys.path |
|---|----------|--------|---------------------|
| 1 | Venv site-packages | Installed wheel | 1st (site-packages) |
| 2 | CWD `/opt/<ORGAN>/app/` | rsync/make-deploy | 2nd (empty string) |
| 3 | Source `/root/<ORGAN>/` | git clone | 3rd (if editable/path-injecting) |

A `git push` only fixes #3. A `pip install` fixes #1 but not #2. An `rsync` fixes #2 but not #1. **All three must converge** for deployment to be coherent.

## Organ Build + Deploy Matrix

### A-FORGE (TypeScript, Node 22+)

```bash
# Build
cd /root/A-FORGE
npm ci && npm run build        # tsc -p tsconfig.json → dist/

# Deploy
rsync -a --delete dist/ package.json node_modules/ /opt/a-forge/app/
git rev-parse HEAD > /opt/a-forge/app/.git_commit

# Restart
systemctl restart a-forge a-forge-mcp

# Verify
curl -sf http://localhost:7071/health
```

**Canonical deploy command:** `make deploy` (runs build + rsync + systemctl)
**Deployment marker:** `/opt/a-forge/app/.git_commit`
**Health endpoint:** `:7071/health` — reports compile-time commit string in `deployed_commit`, not runtime .git_commit file

### AAA (React 19 + Vite)

```bash
# Build
cd /root/AAA
npm ci && npm run build        # vite build → dist/

# Deploy
rsync -a --delete dist/ package.json node_modules/ /opt/aaa/app/
git rev-parse HEAD > /opt/aaa/app/.git_commit

# Restart
systemctl restart aaa-a2a

# Verify
curl -sf http://localhost:3001/health
```

**Deployment marker:** `/opt/aaa/app/.git_commit`
**Known pitfall:** Three-way divergence possible (source HEAD ≠ deployed marker ≠ health compile string). Always check marker matches source.

### GEOX (Python, uv)

```bash
# Sync dependencies
cd /root/GEOX
git pull origin main
uv sync --frozen

# Deploy
rsync -a --delete . /opt/geox/app/ --exclude=.git --exclude=__pycache__ --exclude=.venv
git rev-parse HEAD > /opt/geox/app/.git_commit

# Restart
systemctl restart geox-mcp

# Verify
curl -sf http://localhost:8081/health
```

### WEALTH (Python, uv)

```bash
cd /root/WEALTH
git pull origin main
uv sync --frozen
rsync -a --delete . /opt/wealth/app/ --exclude=.git --exclude=__pycache__ --exclude=.venv
git rev-parse HEAD > /opt/wealth/app/.git_commit
systemctl restart wealth-organ
curl -sf http://localhost:18082/health
```

### WELL (Python, minimal)

```bash
cd /root/WELL
git pull origin main
uv sync --frozen
rsync -a --delete . /opt/well/app/ --exclude=.git --exclude=__pycache__ --exclude=.venv
git rev-parse HEAD > /opt/well/app/.git_commit
systemctl restart well
curl -sf http://localhost:18083/health
```

## Verifying Deployment Coherence

### For arifOS (has full software_release block)

```bash
curl -sf http://localhost:8088/health | python3 -c "
import sys,json; d=json.load(sys.stdin); sr=d.get('software_release',{})
print(f'source={sr.get(\"source_commit\",\"?\")[:12]}')
print(f'built={sr.get(\"built_commit\",\"?\")[:12]}')
print(f'deployed={sr.get(\"deployed_commit\",\"?\")[:12]}')
print(f'drift={sr.get(\"drift\")}')
print(f'rdrift={d.get(\"runtime_drift\")}')
"
```


### For other organs (no software_release block)

Compare source HEAD against deployment marker:

```bash
for organ in A-FORGE AAA GEOX WEALTH WELL; do
  repo=$(echo "$organ" | tr '[:upper:]' '[:lower:]')
  src=$(cd /root/$organ && git rev-parse HEAD)
  marker=$(cat /opt/$repo/app/.git_commit 2>/dev/null || echo MISSING)
  match=$([ "$src" = "$marker" ] && echo MATCH || echo DRIFT)
  echo "$organ: src=$src  marker=$marker  $match"
done
```


## The rsync Trap

After `rsync -a --delete . /opt/<organ>/app/ --exclude=.git`, the `.git` directory is NOT synced (by design). But the `.git_commit` marker file IS updated via `git rev-parse HEAD > ...`. 

**Always verify with the marker file, not with `git -C /opt/<organ>/app rev-parse HEAD`** — the latter reads the deployment `.git` (if one exists from a previous full clone), which WILL be stale.

## Systemd Drop-In Auditing

Drop-in files in `/etc/systemd/system/<service>.service.d/*.conf` are applied AFTER the main unit. Any `Environment=` directive in a drop-in OVERRIDES the same variable from the main unit.

```bash
# List ALL environment variables the service will see
systemctl show <service>.service -p Environment | tr ' ' '\n' | sort -u

# Check for dangerous overrides
grep -r 'ARIFOS_ALLOW_FREE_NONCE\|ARIFOS_SENTINEL' /etc/systemd/system/*.service.d/
```


**Known trap (2026-07-25):** Drop-in `f13-identity.conf` set `ARIFOS_ALLOW_FREE_NONCE=1`, silently disabling replay protection in production. The Python module's safe default (`false`) was overridden.

## The Three-Location Fix Pattern

When code changes don't seem to take effect:

1. **Find all copies:**
   ```bash
   python3 -c "import <module>; print(<module>.__file__)"
   pip show <package> | grep Location
   find /opt/<organ> -name "<module>" -type d 2>/dev/null
   ```
2. **Fix each copy in priority order:**
   - Rebuild wheel from source, install into venv
   - Rsync source to /opt/<organ>/app/
   - Verify git commit marker matches source HEAD
3. **Restart and verify drift=false**

## Restart Timing

After `systemctl restart <service>`, the service may take 3-6 seconds to become available. Health endpoint may return empty response during startup. Use `sleep 5` between restart and probe, or use a retry loop with max 3 attempts.

```bash
for i in 1 2 3; do
  sleep 3
  curl -sf --max-time 3 http://localhost:<PORT>/health && break
done
```
