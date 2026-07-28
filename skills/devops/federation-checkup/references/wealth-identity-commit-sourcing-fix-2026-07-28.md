# WEALTH Identity/Git-Commit Sourcing Fix — 2026-07-28

## Problem

Health endpoint showed `version: "UNAVAILABLE"` and `git_commit: "UNAVAILABLE"` despite 12 tools being loaded. MCP clients saw `serverInfo.version: "UNAVAILABLE"` on initialize.

## Three Root Causes

### Cause 1 — identity.toml Stub (version UNAVAILABLE)

`/root/WEALTH/identity.toml` was a stub:
```toml
# This file is superseded by: /root/AAA/identity.toml
# Status: DERIVED — do not update this copy.
```

No `[identity]` section, no `version` field. The `_load_identity_version()` in `wealth_mcp/__init__.py` reads `identity.toml` via `Path(__file__).resolve().parents[1] / "identity.toml"` and returns `"UNAVAILABLE"` when the version key is missing.

**Fix:** Replace the stub with the proper identity manifest (matching the already-correct `/opt/wealth/app/identity.toml`):
```toml
[identity]
canonical_name = "WEALTH Capital Intelligence"
short_name = "WEALTH"
service_id = "wealth-organ"
version = "2026.07.24"
# ... full identity manifest
```

**Verification:** `python3 -c "from wealth_mcp import WEALTH_VERSION; print(repr(WEALTH_VERSION))"` → `'2026.07.24'`

### Cause 2 — _resolve_source_commit() Fallback Bug (git_commit UNAVAILABLE)

`_resolve_source_commit()` in `/root/WEALTH/server_federated.py`:
1. Tries `git -C $repo rev-parse --short=7 HEAD` — **fails inside systemd service** (NoNewPrivileges=true + PrivateTmp=true prevent git from reading .git objects)
2. Falls through to read `.git_commit` file — this worked, found hash `0aba13a`
3. But **never promoted it to `git_commit`** — only populated `git_commit_fallback`

The function returned:
```python
{
    "git_commit": "UNAVAILABLE",        # stayed UNAVAILABLE
    "git_commit_source": "unavailable",
    "git_commit_fallback": "0aba13a",   # file content here but not promoted
}
```

**Fix:** When `.git_commit` file content is valid, promote it to `git_commit`:
```python
if fallback_sha:
    return {
        "git_commit": fallback_sha,               # promoted to primary
        "git_commit_source": "fallback_file",
        "source_sha_available": True,
        "git_commit_fallback": None,
    }
```

**Verification:** `curl :18082/health | jq '.git_commit'` → `"802942d"`

### Cause 3 — Stale .git_commit File

`.git_commit` contained `0aba13a` while `git rev-parse HEAD` returned `802942d`. The file was not updated after the last commit.

**Fix:** `echo "802942d" > /root/WEALTH/.git_commit && cp /root/WEALTH/.git_commit /opt/wealth/app/.git_commit`

## Service Architecture Note

The systemd service runs from `/root/WEALTH/` (not `/opt/wealth/app/`):

```ini
WorkingDirectory=/root/WEALTH
ExecStart=/root/WEALTH/.venv/bin/python3 server_federated.py
Environment=PYTHONPATH=/root/WEALTH
```

With hardening:
```ini
NoNewPrivileges=true
ProtectSystem=strict
PrivateTmp=true
```

`NoNewPrivileges` prevents `git` subprocess from reading all `.git` objects. The `.git_commit` file exists precisely to handle this case — but the code must promote its content.

## Diagnostic Flow

When `version: UNAVAILABLE` or `git_commit: UNAVAILABLE` appears on any organ:

1. **version UNAVAILABLE** → Check `identity.toml` in the organ's source root (`/root/<ORGAN>/`). Is there a `version` field under `[identity]`? If the file is a stub (points to AAA or another file), it needs restoring. The `_load_identity_version()` in `__init__.py` reads `parents[1] / "identity.toml"` — verify the path resolves correctly.

2. **git_commit UNAVAILABLE** → Two paths:
   - Check if `git rev-parse` works: `cd /root/<ORGAN> && git rev-parse --short=7 HEAD`. If it works but the health shows UNAVAILABLE, the service's systemd sandboxing (NoNewPrivileges, PrivateTmp) may be blocking subprocess git access.
   - Check `.git_commit` file: `cat /root/<ORGAN>/.git_commit`. Compare against `git rev-parse HEAD`. If stale, update.
   - Check `_resolve_source_commit()` logic: does the function promote `.git_commit` file content or only store it as fallback?

3. **Both UNAVAILABLE + tools/health fine** → The tools surface is independent from identity metadata. Tools register via `@mcp.tool()` decorators and work regardless of identity.toml. Don't conflate missing identity metadata with broken MCP surface.

## Post-Fix Verification

```bash
# Health
curl -s http://127.0.0.1:18082/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'version={d[\"version\"]} git={d[\"git_commit\"]} tools={d[\"tools_loaded\"]}')"

# MCP initialize + tools/list
SID=$(curl -s http://127.0.0.1:18082/mcp -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"verify","version":"1.0"}}}' | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['serverInfo']['version'])")
curl -s http://127.0.0.1:18082/mcp -H 'Content-Type: application/json' -H 'Accept: application/json' -H "Mcp-Session-Id: $SID" -d '{"jsonrpc":"2.0","id":"2","method":"tools/list","params":{}}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Tools: {len(d[\"result\"][\"tools\"])}')"
```

## Related

- `federation-checkup` skill — Known Common Findings table (updated 2026-07-28 to mark WEALTH git_commit as RESOLVED)
- `mcp-transport-debugging` — Session enforcement patterns for WEALTH/GEOX/arifOS
