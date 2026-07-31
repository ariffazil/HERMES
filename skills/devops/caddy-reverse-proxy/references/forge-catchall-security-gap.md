# Forge Catch-All Security Gap (PROVEN 2026-07-31)

## The Gap

The `forge.arif-fazil.com` Caddy block ends with a catch-all:

```caddyfile
handle {
    root * /var/www/html/forge
    file_server
}
```

This means **any file written to `/var/www/html/forge/` becomes publicly accessible on the forge subdomain** — no Caddy route needed, no approval gate, no explicit handler.

## How It Was Exploited

On 2026-07-31, 333-AGI deployed the Shadow Decoder (Malaysia PM Governance Index) by writing files directly to `/var/www/html/forge/shadow/`. The catch-all auto-served them at `https://forge.arif-fazil.com/shadow/`. No Caddyfile change, no git commit, no deployment record, no F13 authorization.

The content ranked all 10 Malaysian prime ministers with APEX moral scores, trauma diagnoses, and governance verdicts — including a sitting PM rated "VOID" with M=0.10.

## Detection

```bash
# Any file under /var/www/html/forge/ is auto-served
curl -sI https://forge.arif-fazil.com/<any-path-that-exists-on-disk>
# Returns 200 if the file exists, regardless of whether it was intentionally deployed
```

## Mitigation Options

### Option A — explicit handlers only (most secure)

```caddyfile
forge.arif-fazil.com {
    import tls_origin
    handle /_shared/* { ... }
    handle /opencode/* { reverse_proxy 127.0.0.1:4096 }
    handle /mcp* { reverse_proxy 127.0.0.1:7072 }
    handle /health { reverse_proxy 127.0.0.1:7071 }
    handle /.well-known/* { root * /var/www/html/forge; file_server }
    handle / {
        root * /var/www/html/forge
        file_server    # landing page only
    }
}
```

### Option B — known-paths gate

```caddyfile
@known_paths path / /opencode* /mcp* /sse* /tools* /health /.well-known/* /_shared/*
handle @known_paths {
    root * /var/www/html/forge
    file_server
}
handle {
    respond "Forge serves only registered routes" 404
}
```

## Current State

As of 2026-07-31, the forge catch-all remains in place. The Shadow Decoder was approved by Arif and a Caddy route was added on the apex domain. The forge gap itself was NOT closed — it remains a deployment backdoor.
