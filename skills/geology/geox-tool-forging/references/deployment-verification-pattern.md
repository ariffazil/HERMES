# GEOX Deployment Verification Pattern

Canonical sequence for deploying GEOX code changes after a git commit, verified in the 2026-07-29 forge session.

## 1. Build Verification

```bash
cd /root/GEOX

# Frozen dependency check (no unexpected upgrades)
uv sync --frozen

# Import test — verifies the package loads
uv run python3 -c "from geox_mcp.tools_wiring import register_tools_on; print('OK')"

# Expected: "Phase 2 unified tools wired: 82 runtime tools registered with FastMCP"
```

## 2. Deploy

Two strategies depending on scope:

### Strategy A — Full rsync (preferred for forge sessions with new static files)

```bash
cd /root/GEOX
rsync -a --delete \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  /root/GEOX/ /opt/geox/app/
```

Use when you added static files (GUI dashboards, agent surfaces), changed deps (pyproject.toml/uv.lock), or want a clean mirror.

### Strategy B — Source-only (lighter, for code-only changes)

```bash
rsync -a --delete /root/GEOX/src/ /opt/geox/app/src/
```

### Deployment provenance stamp

```bash
cd /root/GEOX && git rev-parse HEAD > /opt/geox/app/git_version.txt
```

## 3. Restart + Verify

```bash
systemctl restart geox-mcp && sleep 3
systemctl is-active geox-mcp

# Full health probe
curl -sf http://127.0.0.1:8081/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Status: {d[\"status\"]}')
print(f'Tools: {d[\"canonical_tools\"]}')
print(f'Surface drift: ok={d[\"surface_drift\"][\"ok\"]}')
"
```

### arifOS dependency recovery

If GEOX shows `Status: degraded` + `Kernel: UNKNOWN`, arifOS is down:
```bash
systemctl restart arifos && sleep 5
# GEOX auto-recovers within one health check
curl -sf http://127.0.0.1:8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{d[\"status\"]} kernel={d[\"kernel_verdict\"]}')"
```

## 4. GUI Under Existing Route (No Caddyfile Modification)

The existing Caddyfile for `geox.arif-fazil.com` handles:
```caddy
handle /gui/* {
    uri strip_prefix /gui
    root * /var/www/html/geox/gui
    try_files {path} /index.html
    file_server
}
```

**Any subdirectory** under `/var/www/html/geox/gui/` is automatically served without Caddyfile changes:

```bash
mkdir -p /var/www/html/geox/gui/<surface-name>
cp -r <source>/ /var/www/html/geox/gui/<surface-name>/
```

Accessible at `https://geox.arif-fazil.com/gui/<surface-name>/`.

**Caveat:** `try_files {path} /index.html` means missing paths fall back to the parent GUI's index.html. Always verify `curl -s https://geox.arif-fazil.com/gui/<name>/ | head -3`.

## 5. Auth Gate Fix Pattern (E2)

When OBSERVE_ONLY tools return `SESSION_MISSING` despite declaring `required_authority = "OBSERVE_ONLY"`:

**File:** `src/geox_mcp/authority_gate.py`
**Function:** `enforce_authority()`

Insert after `required = required_authority_for(tool_name, arguments or {})`:
```python
    if required == "OBSERVE_ONLY":
        logger.debug("AUTH_GATE: OBSERVE_ONLY tool=%s — session gate skipped", tool_name)
        return
```

## 6. Image Serving Endpoint for GUIs

When a renderer (geox_geological_model_generate) outputs PNGs to `/tmp/geox/`, add to `server.py`:

```python
async def geox_preview_handler(request: Request):
    path = request.query_params.get("path", "")
    if not path or ".." in path or not path.startswith("/"):
        return PlainTextResponse("Invalid path", status_code=400)
    resolved = os.path.normpath(path)
    if not resolved.startswith(os.path.normpath("/tmp/geox/")):
        return PlainTextResponse("Forbidden", status_code=403)
    if not os.path.isfile(resolved):
        return PlainTextResponse("Not found", status_code=404)
    return FileResponse(resolved, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=60"})
```

## 7. Full Verification Sequence

```bash
echo "=== YAML AUDIT ==="
python3 -c "
import yaml
for f in ['surface.yaml', 'tools_manifest.yaml']:
    with open(f'src/geox_mcp/{f}') as fh:
        d = yaml.safe_load(fh)
    pub = sum(1 for t in d['tools'] if t.get('visibility') == 'public')
    target = d.get('public_count_target', len(pub))
    print(f'{\"✅\" if pub == target else \"❌\"} {f}: {pub} public (target={target})')
"

echo "=== DEPLOY ==="
rsync -a --delete --exclude='.git' --exclude='.venv' --exclude='__pycache__' /root/GEOX/ /opt/geox/app/
systemctl restart geox-mcp && sleep 3

echo "=== HEALTH ==="
curl -s http://127.0.0.1:8081/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Status={d[\"status\"]} Tools={d[\"canonical_tools\"]} Drift={d[\"surface_drift\"][\"ok\"]}')
"

echo "=== GIT SEAL ==="
cd /root/GEOX && git status -s && git log --oneline -1
```
