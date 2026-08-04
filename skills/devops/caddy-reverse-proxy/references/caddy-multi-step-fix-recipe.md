# Caddy Multi-Step Fix Recipe — Duplicate Matcher + `log` Placement (2026-08-04)

When a single error masks a cascade, the disciplined path is **one fix per `caddy validate` cycle**. Three errors emerged from a single observed Caddyfile corruption — the second and third only surfaced after the first was fixed.

## The Three-Error Cascade

**Symptom chain:**
```
1. Error: matcher is defined more than once: @static_client_id_mcp
   ↓ fix: combine matcher conditions on one line
2. Error: directive 'log' is not an ordered HTTP handler, so it cannot be used here
   ↓ fix: wrap handle in route block
3. Error: parse error or unexpected 'log' at the wrong nesting level
   ↓ fix: nest log INSIDE the route block (not outside as orphan)
```

## Step-by-Step Walkthrough

### Original (broken) state — TWO lines defining the same matcher

```caddyfile
@static_client_id_mcp path /mcp*
@static_client_id_mcp header X-MCP-Client-Id "geox-claude-conn-20260804-a01"
handle @static_client_id_mcp {
    reverse_proxy 127.0.0.1:8081 {
        header_up Host geox.arif-fazil.com
        header_up X-Static-Client-Id "geox-claude-conn-20260804-a01"
        header_up X-Auth-Method "p3_auth_lite_static"
    }
    log {
        output file /var/log/caddy/geox-static-auth.log {
            roll_size 10mb
            roll_keep 5
        }
        format console
    }
}
```

### Step 1 — Combine matcher conditions (fixes error #1)

```caddyfile
@static_client_id_mcp path /mcp* header X-MCP-Client-Id "geox-claude-conn-20260804-a01"
handle @static_client_id_mcp {
    reverse_proxy 127.0.0.1:8081 { ... }
    log { ... }
}
```

Validate:
```bash
/usr/bin/caddy validate --config /etc/caddy/Caddyfile 2>&1
# Now reveals: directive 'log' is not an ordered HTTP handler
```

### Step 2 — Wrap in `route` block (fixes error #2)

`log` is allowed inside `route` blocks but not `handle` blocks.

```caddyfile
@static_client_id_mcp path /mcp* header X-MCP-Client-Id "geox-..."
route @static_client_id_mcp {
    reverse_proxy 127.0.0.1:8081 { ... }
    log { ... }
}
```

⚠️ **Do NOT do this with `sed`:** If you naively `sed 's/handle @matcher {/route @matcher {/'`, the `log` block may end up OUTSIDE the new `route` block as an orphan if the original block had `log` at the same indentation level as `handle`. The orphan generates a new parse error.

**Use Python `str.replace()` for atomic block replacement** when restructuring multiple lines together:

```python
old_block = '''\t@static_client_id_mcp path /mcp* header X-MCP-Client-Id "geox-..."
\troute @static_client_id_mcp {
\t\treverse_proxy 127.0.0.1:8081 { ... }
\t}
\t\tlog { ... }
\t}'''
# ^ this is the ORPHAN pattern — sed produced this

new_block = '''\t@static_client_id_mcp path /mcp* header X-MCP-Client-Id "geox-..."
\troute @static_client_id_mcp {
\t\treverse_proxy 127.0.0.1:8081 { ... }
\t\tlog { ... }
\t}'''
# ^ log is NESTED inside route, not orphaned

with open('/etc/caddy/Caddyfile') as f: c = f.read()
c = c.replace(old_block, new_block)
with open('/etc/caddy/Caddyfile', 'w') as f: f.write(c)
```

### Final Validation

```bash
/usr/bin/caddy validate --config /etc/caddy/Caddyfile 2>&1 | grep -i "valid\|error"
# Must say: "Valid configuration"

/usr/bin/caddy reload --config /etc/caddy/Caddyfile 2>&1
# OR (preferred):
bash /root/.hermes/scripts/caddy-safe-reload.sh
# Last output: "RESULT: all endpoints healthy" + per-URL 200 verification
```

## Key Discipline Points

1. **One fix per `validate` cycle.** The cascade exists because each fix reveals the next. Don't batch.
2. **Don't use `sed` for multi-line block restructuring.** Use Python `str.replace()` or write/read the whole file.
3. **Always run `caddy-safe-reload.sh`** after a fix lands — it does backup + validate + reload + verify (catches regressions).
4. **Backup before any Caddyfile mutation** — `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%Y%m%dT%H%M%S)-<reason>`.

## Failure Patterns to Recognize

| Pattern | Probable cause |
|---|---|
| Three different errors in cascade after one fix | Caddyfile has multiple compounding structural issues — fix in order, don't assume one edit clears everything |
| `log` at top-level (not inside any block) | sed/awk replaced the parent `handle`/`route` opener but not the body structure |
| `parse error` with no clear line number | Look at the previous `log`/`header_up` block — orphan content from prior fix |
| `matcher is defined more than once` returns again after fix | The conditions weren't combined on a single line — check there's only ONE `@<name>` line per name |
