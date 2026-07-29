# Hardened Localhost-Only Systemd Deployment

> Pattern for deploying Python stdlib HTTP servers (or any localhost-only tool UI) as hardened systemd services. Proven on forge_mcp_ui (arifOS Radar, 127.0.0.1:7777).

## When to Use

- A Python stdlib `http.server` or `ThreadingHTTPServer` needs to run as a systemd service
- The service must bind **only** to `127.0.0.1` (LOCALHOST_IS_PASSWORD doctrine)
- The service is **read-only** by design (F1 AMANAH — no POST/PUT/DELETE)
- The service needs hardening beyond basic systemd defaults

## Hardened Service Template

```ini
[Unit]
Description=<Name> — <Purpose> (read-only, 127.0.0.1:<port>)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=<codebase_dir>
ExecStart=/usr/bin/python3 <script>.py --port <port> --host 127.0.0.1
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
# F1 AMANAH: no writable paths
ReadWritePaths=
# No new privileges (su, sudo escalation blocked)
NoNewPrivileges=true
# Read-only root filesystem after startup
ProtectSystem=strict
# Isolate /tmp from host
PrivateTmp=true
# Home directories read-only — no write access
ProtectHome=read-only
# Drop all capabilities (no raw sockets, no sys_admin, etc.)
CapabilityBoundingSet=
# LOCALHOST_IS_PASSWORD: loopback-only networking
PrivateNetwork=false
IPAddressDeny=any
IPAddressAllow=127.0.0.1

[Install]
WantedBy=multi-user.target
```

## Security Directives Explained

| Directive | Effect | Why |
|-----------|--------|-----|
| `NoNewPrivileges=true` | Prevents `su`, `sudo`, capabilty escalation from within the process | A read-only UI should never need privilege escalation |
| `ProtectSystem=strict` | Mounts `/usr` and `/etc` read-only. Only `/var`, `/tmp`, `/dev` writable. | Fails closed if a code path tries to write to system |
| `PrivateTmp=true` | Gives the service its own `/tmp` namespace | Isolates from other processes' temp files |
| `ProtectHome=read-only` | `/root`, `/home/*` mounted read-only | Prevents accidental reads/writes to user data |
| `CapabilityBoundingSet=` | Drops ALL kernel capabilities | No raw sockets, no sys_admin, no setuid — minimal surface |
| `IPAddressDeny=any` with `IPAddressAllow=127.0.0.1` | Blocks all network except loopback | Enforces LOCALHOST_IS_PASSWORD at kernel level, not just application bind |

## Forward-Reference Bug Fix (Python stdlib servers)

Python stdlib HTTP servers with precomputed HTML strings often have a forward-reference bug:

```python
# BUG: Called before function is defined
HTML_DOC = _render_html()     # ← NameError at import time

def _render_html() -> bytes:
    return b"<html>..."
```

**Fix:** Move the assignment to AFTER the function definition:

```python
def _render_html() -> bytes:
    return b"<html>..."

# OK: Called after function is defined
HTML_DOC = _render_html()
```

This happens because `_render_html()` is a module-level call that depends on module-level data (ORGANS, FLOORS, _CSP) — those are available at import time, but the function itself must be defined first.

## Endpoint Testing Pattern

After deployment, test all expected endpoints systematically:

```bash
# 1. Health probe
curl -s http://127.0.0.1:<port>/health
# Expect: {"status":"UP", ...}

# 2. Main page
curl -s -o /dev/null -w "HTTP %{http_code}, Size: %{size_download} bytes, CT: %{content_type}" \
  http://127.0.0.1:<port>/
# Expect: HTTP 200

# 3. Data API
curl -s http://127.0.0.1:<port>/data.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(...)"
# Expect: valid JSON with expected structure

# 4. Mutation rejection (F1 AMANAH)
curl -s -X POST http://127.0.0.1:<port>/
# Expect: 405 with error message containing "F1 AMANAH" or "read_only"
echo "---"

# 5. PUT rejection
curl -s -X PUT http://127.0.0.1:<port>/
# Expect: 405

# 6. DELETE rejection
curl -s -X DELETE http://127.0.0.1:<port>/
# Expect: 405

# 7. Unknown path
curl -s -o /dev/null -w "HTTP %{http_code}" http://127.0.0.1:<port>/nonexistent
# Expect: 404
```

## Pitfalls

- **Restart counter exhaustion:** systemd defaults to 5 restart attempts in 10s. If the server fails on startup (e.g., port in use), `systemctl reset-failed <service>` must be called before restart.
- **import-time NameError:** If the server precomputes HTML at import and the rendering function is defined AFTER the call, the module fails to load. Always define functions before calling them at module level.
- **`IPAddressDeny` vs `IPAddressAllow` order:** systemd applies the deny first, then the allow. `IPAddressDeny=any` + `IPAddressAllow=127.0.0.1` correctly allows only loopback. Reverse order would block everything.
- **systemd hardening breaks common patterns:** `ProtectSystem=strict` prevents file writes. `ProtectHome=read-only` prevents writing to user home dirs. If the service needs temp write access, `PrivateTmp=true` gives it an isolated `/tmp`. If it needs cache writes, add `CacheDirectory=<name>` directive.
