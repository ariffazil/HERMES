# Remote HTTP MCP Server Setup Pattern

Verified 2026-07-09 — adding external HTTP MCP servers to Hermes via CLI scalar commands.

## The problem

`hermes mcp add --url` has an interactive auth prompt that blocks agent loops (getpass(), no stdin bypass).

## Working recipe

Use `hermes config set` for each scalar field:

```bash
hermes config set mcp_servers.<name>.url 'https://<host>/mcp'
hermes config set mcp_servers.<name>.transport streamable-http
hermes config set mcp_servers.<name>.description '<human description>'
```

## Verification

```bash
hermes mcp list          # shows server as ✓ enabled
hermes mcp test <name>   # probes connection + discovers tools
```

## Example: arif-fazil.com MCP (2026-07-09)

```bash
hermes config set mcp_servers.arif-fazil.url 'https://mcp.arif-fazil.com/mcp'
hermes config set mcp_servers.arif-fazil.transport streamable-http
hermes config set mcp_servers.arif-fazil.description 'arif-fazil.com public MCP endpoint'
```

Result:
- Connection: 433ms, stable
- 12 arifOS kernel tools discovered
- Same surface as local arifOS :8088, via HTTPS

## Headers (auth)

If the remote MCP needs auth:

```bash
hermes config set mcp_servers.<name>.headers.Authorization 'Bearer sk-...'
```

## stdio vs HTTP

- **HTTP**: `hermes config set` for scalars works (url, transport, description, headers.*)
- **stdio**: need Python read-mutate-write (args/env are nested lists)

## MCP SDK prerequisite

```bash
pip install mcp --break-system-packages   # if system Python
```

Without it: "MCP SDK not available -- skipping MCP tool discovery" (silent skip on startup).
