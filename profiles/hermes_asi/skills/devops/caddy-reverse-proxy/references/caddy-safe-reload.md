# Caddy Safe Reload — F1 Reversibility Protocol

## Script location

`/root/.hermes/scripts/caddy-safe-reload.sh`

## What it does

1. **Backup** current Caddyfile to `/var/log/caddy-backups/Caddyfile.<timestamp>`
2. **Validate** with `caddy validate --config`
3. **Reload** via `systemctl reload caddy`
4. **Verify** 3 key endpoints (arif-fazil.com, mcp.arif-fazil.com/health, aaa.arif-fazil.com)
5. **Report** success/failure to `/var/log/caddy-safe-reload.log`
6. **Prune** old backups (keep last 20)

## Usage

```bash
# Standard reload (backs up, validates, reloads, verifies)
bash /root/.hermes/scripts/caddy-safe-reload.sh

# With custom Caddyfile path
bash /root/.hermes/scripts/caddy-safe-reload.sh /etc/caddy/Caddyfile.staging
```

## No email policy

All receipts go to local log (`/var/log/caddy-safe-reload.log`), NOT email. VAULT999 reads from here. This was a sovereign correction: Arif rejected "mail -s arif@arif-fazil.com" as "entropi luar."

## When to use

ALWAYS use `caddy-safe-reload.sh` instead of bare `systemctl reload caddy`. The safe reload catches:
- Invalid Caddyfile syntax (validate before reload)
- Endpoint failures after reload (verify after reload)
- Provides rollback path (backup exists)

## Pitfall

If the validate step fails, the script exits WITHOUT reloading. This is correct — don't override it. Fix the Caddyfile first, then re-run.

Proven 2026-07-16: Script tested end-to-end. Backup created, validated, reloaded, 3 endpoints verified.
