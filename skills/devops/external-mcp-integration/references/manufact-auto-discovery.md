# Manufact Auto-Discovery (2026-07-24)

## How Manufact Found Our Servers

Manufact (mcp-use) crawls the web for MCP servers by:

1. **Scanning `llms.txt`** — the standard AI discovery file at domain roots
2. **Checking `.well-known/mcp.json`** — MCP server manifest with endpoints + routing
3. **Linking to GitHub repos** — if the Manufact GitHub App is installed on the account, auto-creates servers from the repos listed in the manifest

On 2026-07-24, two servers were found auto-deployed on Manufact Cloud:

| Server | ID | Status | Deployments | URL |
|--------|----|--------|-------------|-----|
| **geox** | `95266f6f-dcc2-4913-9f66-f903ee065e7a` | ✅ running | 625+ | `warm-pulse-wczsk.run.mcp-use.com/mcp` |
| **arifos** | `c764a8e3-f046-46b5-8acc-1d2d5416aa12` | ❌ error → 🗑️ deleted | 1,420 (~all failed) | `fast-cloud-4qmmk.run.mcp-use.com/mcp` |

## Source Discovery Files

The file that exposed the federation: `/root/arif-sites/sites/mcp.arif-fazil.com/.well-known/mcp.json`

```json
{
  "server": "gateway",
  "version": "1.0.0",
  "endpoint": "https://mcp.arif-fazil.com/mcp",
  "protocol": "streamable-http",
  "routing": {
    "arifos": "https://arifos.arif-fazil.com/mcp",
    "aforge": "https://forge.arif-fazil.com/mcp",
    "geox": "https://geox.arif-fazil.com/mcp",
    "wealth": "https://wealth.arif-fazil.com/mcp",
    "well": "https://well.arif-fazil.com/mcp",
    "aaa": "https://aaa.arif-fazil.com/mcp"
  }
}
```

Manufact's crawler parsed this manifest and tried to deploy from the linked GitHub repos (`ariffazil/arifos`, `ariffazil/GEOX`).

## Prevention

After finding the auto-deployed servers, a `discovery` block was added to the manifest to signal self-hosting:

```json
{
  "discovery": {
    "registry": "self-hosted",
    "auto_register": false,
    "note": "All federation MCP servers are self-hosted on sovereign infrastructure. External registration via Manufact Cloud or similar platforms is not required and may produce broken deployments (especially Python-based servers)."
  }
}
```

## CLI Login

```bash
npm install -g @mcp-use/cli
mcp-use login --api-key "mcp_xxx..."
mcp-use whoami
# → arifbfazil@gmail.com
```

## Cleanup

The broken arifOS server was deleted:

```bash
mcp-use servers rm c764a8e3-f046-46b5-8acc-1d2d5416aa12 -y
# ✓ Server deleted: arifos
```

GEOX was kept running (no reason to remove it).

## Lesson for Future Sessions

When onboarding email arrives from a crawler-based platform:
1. Authenticate with the provided API key to see what was auto-registered
2. Check for servers that were auto-deployed from repos you didn't intend to deploy
3. Delete broken/accidental servers
4. Update discovery files to indicate self-hosting
5. Document the crawler's discovery path for future reference
