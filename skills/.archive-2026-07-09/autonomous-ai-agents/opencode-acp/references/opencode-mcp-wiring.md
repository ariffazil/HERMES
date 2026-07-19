# MCP Wiring in OpenCode (opencode.json)

OpenCode's MCP config lives at `/root/.config/opencode/opencode.json` under the `mcp:` key.

## Format

```json
{
  "mcp": {
    "server-name": {
      "type": "stdio|remote",
      "command": ["npx", "-y", "package-name"],
      "environment": {
        "DATABASE_URL": "postgresql://user:pass@host:port/db",
        "API_KEY": "sk-..."
      },
      "enabled": true
    }
  }
}
```

## Key differences from Hermes

| Aspect | OpenCode (opencode.json) | Hermes (config.yaml) |
|--------|--------------------------|----------------------|
| Key | `mcp:` | `mcp_servers:` |
| Type field | `type: stdio\|remote` | `transport: stdio\|streamable-http` |
| Command | `command: [...]` (array) | `command:` + `args:` (separate) |
| Environment | `environment: {...}` | `env: {...}` |
| URL (remote) | `url: http://...` | `url: http://...` |

## Wiring MCP servers with credentials

When an MCP server needs credentials (DATABASE_URL, API_KEY), add them to the `environment` block:

```python
# Python pattern for wiring credentials
import json

with open('/root/.config/opencode/opencode.json') as f:
    config = json.load(f)

mcp = config.get('mcp', {})

# Wire postgres MCP
if 'postgres' in mcp:
    mcp['postgres']['environment'] = {
        "DATABASE_URL": "postgresql://user:pass@127.0.0.1:5432/dbname"
    }

# Wire brave-search MCP
if 'brave-search' in mcp:
    mcp['brave-search']['environment'] = {
        "BRAVE_API_KEY": "BSA..."
    }

config['mcp'] = mcp
with open('/root/.config/opencode/opencode.json', 'w') as f:
    json.dump(config, f, indent=2)
```

## Credential sourcing

- **Docker containers:** `docker inspect <container> | grep POSTGRES` for env vars
- **Hermes .env:** `/root/.hermes/.env` — check for existing keys
- **System secrets:** `/root/.secrets/KEY_REGISTRY.md` — canonical key index
- **Environment:** `env | grep -i <provider>` for runtime keys

## Pitfalls

- OpenCode does NOT read Hermes `.env` — credentials must be in `opencode.json` `environment` block or in the shell env when OpenCode starts
- `environment` values are literals, not env var references — `{"KEY": "$ENV_VAR"}` does NOT expand
- `type: "remote"` = SSE/HTTP endpoint; `type: "stdio"` = subprocess
- Changing MCP config requires restarting OpenCode (next session picks it up)
