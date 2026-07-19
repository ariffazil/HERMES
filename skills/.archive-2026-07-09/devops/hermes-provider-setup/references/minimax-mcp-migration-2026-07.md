# MiniMax MCP Migration — SSE → stdio (2026-07-06)

## What happened

MiniMax had THREE MCP processes running, all problematic:

| Process | Type | PID | Status | Problem |
|---|---|---|---|---|
| minimax-code-mcp | systemd SSE :18091 | 1476 | running5 days, DEAD health | SSE server not responding |
| minimax-media-mcp | systemd SSE :18090 | 1477 | running5 days, DEAD health | SSE server not responding |
| minimax-coding-plan-mcp | uvx stdio | ****8 | running since Jul 4 | Memory leak zombie |

## Migration steps executed

### Phase 1: Kill leaky processes

```bash
# Kill uvx zombie + child
kill ****8 ****22

# Stop and disable systemd services
systemctl stop minimax-code-mcp.service minimax-media-mcp.service
systemctl disable minimax-code-mcp.service minimax-media-mcp.service
```

Left `/opt/minimax-mcp-code/` and `/opt/minimax-mcp-media/` on disk (no rm -rf without explicit OK).

### Phase 2: Update opencode.json

OpenCode config at `/root/.config/opencode/opencode.json`. Uses `mcp:` key (not `mcpServers:`).

**Before (broken SSE pair):**
```json
"mcp": {
  "minimax-media": { "type": "remote", "url": "http://127.0.0.1:18090/mcp", "enabled": true },
  "minimax-code": { "type": "remote", "url": "http://127.0.0.1:18091/mcp", "enabled": false }
}
```

**After (stdio):**
```json
"mcp": {
  "minimax": {
    "type": "stdio",
    "command": ["uvx", "minimax-coding-plan-mcp", "-y"],
    "environment": {
      "MINIMAX_API_KEY": "{env:MINIMAX_API_KEY}",
      "MINIMAX_API_HOST": "https://api.minimax.io"
    },
    "enabled": true
  }
}
```

### Phase 3: Install mmx-cli skill

```bash
# Symlink from hermes skill to claude + openclaw
ln -sf ~/.hermes/skills/minimax-cli/SKILL.md ~/.claude/skills/minimax-cli.md
mkdir -p ~/.openclaw/skills/
ln -sf ~/.hermes/skills/minimax-cli/SKILL.md ~/.openclaw/skills/minimax-cli.md
```

`npx skills add MiniMax-AI/cli -y -g` fails with "PromptScript does not support global skill installation" — use manual symlink instead.

### Phase 4: Verify

```bash
# No minimax processes
ps aux | grep -i minimax | grep -v grep

# Systemd inactive
systemctl is-active minimax-code-mcp minimax-media-mcp

# mmx-cli works
mmx auth status
mmx quota

# Skills installed
ls -la ~/.claude/skills/minimax-cli.md ~/.openclaw/skills/minimax-cli.md
```

## Key lessons

1. **SSE MCP servers as systemd services are fragile** — they can be "running" but dead (process alive, HTTP dead). Health checks on the port are the real indicator.

2. **uvx stdio MCP can leak** — the minimax-coding-plan-mcp had a child process that survived parent restart. Need explicit `kill` of both parent and child PIDs.

3. **Hermes quarantine ≠ stop** — the `minimax-coding-plan-mcp` was quarantined in Hermes config (disabled + reason) but the uvx process was still running. Quarantine prevents Hermes from spawning it, doesn't kill existing instances.

4. **OpenCode config format differs from Hermes** — OpenCode uses `mcp:` with `type: stdio|remote`, Hermes uses `mcp_servers:` with `transport: streamable-http|stdio`. Don't conflate them.

5. **mmx-cli skill install** — `npx skills add MiniMax-AI/cli -y -g` fails for global install. Manual symlink from `~/.hermes/skills/<name>/SKILL.md` to `~/.claude/skills/<name>.md` and `~/.openclaw/skills/<name>.md` works.

6. **minimax-coding-plan-mcp covers web_search + understand_image** — same surface as mmx-cli's `mmx search` and `mmx vision describe`. Either works; mmx-cli is cleaner for Hermes integration (terminal tool), MCP is cleaner for OpenCode integration (native tool calls).

## Cross-reference

- `references/mmx-cli-minimax-multimodal-2026-07.md` — mmx-cli usage and commands
- `references/minimax-direct-provider-2026-07.md` — MiniMax as Hermes LLM provider
- `references/mcp-stdio-leak-and-hermes-standalone-2026-07-04.md` — stdio subprocess leak pattern
