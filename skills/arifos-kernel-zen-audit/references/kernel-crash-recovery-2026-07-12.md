# Kernel Crash Recovery — 2026-07-12

## Root Cause

`/opt/arifos/app/.env` was owned by `ariffazil:ariffazil` (mode 600), but the systemd service runs as user `arifos`. The arifOS kernel uses `WorkingDirectory=/opt/arifos/app` and reads `.env` at startup via `python-dotenv`.

Log signature:
```
PermissionError: [Errno 13] Permission denied: '.env'
```

## Fix

```bash
chown arifos:arifos /opt/arifos/app/.env
chmod 640 /opt/arifos/app/.env
systemctl restart arifos
```

## Cascade Impact

When the kernel crashed, `mcp__arifos__*` tools disappeared from Hermes agent context. They return on next agent session start (`/reset` or new `hermes` invocation). The MCP server's tool list is re-fetched on session bootstrap.

## Checking Service Status

```bash
systemctl is-active arifos         # active / inactive / activating
ss -tlnp | grep 8088               # confirm listening
curl -sf http://127.0.0.1:8088/health | python3 -m json.tool
```

## Key Service Config

```
User=arifos
WorkingDirectory=/opt/arifos/app
ExecStart=/bin/sh -c 'export ARIFOS_VAULT_DIR=/var/lib/arifos/vault; exec /opt/arifos/venv/bin/python -c "from arifosmcp.runtime.__main__ import main; main()"'
```

## Corollary: `chown -R` Can Make Things Worse

Recursive `chown root:root /opt/arifos/app/` re-created the permission issue after the initial `chown arifos:arifos .env` had fixed it. Fix only the specific file, not the entire tree.

## Probe Sequence

1. `systemctl is-active arifos`
2. `journalctl -u arifos --no-pager -n 30 | grep -i "error\|failed\|listening"`
3. `curl -sf http://127.0.0.1:8088/health`
4. If kernel is up but MCP tools are gone: start a new Hermes session
