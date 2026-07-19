# MCP stdio leak + standalone Hermes MCP (2026-07-04)

Session-specific findings from auditing a live Hermes federation install. Keep these notes
alongside the federation-mcp-bridge reference — they extend that one with what happens AFTER
the bridge is wired.

## The stdio leak pattern

When mcp_servers are registered with `transport: stdio`, each server spawns its own subprocess
per session. On a long-running gateway with many stdio servers, this leaves dozens of orphan
Python/Node processes that don't get reaped.

**Verified count (2026-07-04):** 7 stdio MCP subprocesses running concurrently on the VPS:
- minimax-coding-plan-mcp (Python, uv tool)
- github-mcp-server (stdio mode)
- mcp-server-github (Node)
- context7-mcp (Node)
- brave-search-mcp (Node, npm exec)
- sequential-thinking-mcp (Node, npm exec)
- serena start-mcp-server (Python, uv tool)

**Recipe to detect:**

```bash
ps aux | grep -E "(stdio|mcp-server|serena|coding-plan)" | grep -v grep | wc -l
# Compare against number of stdio entries in config.yaml
grep -c "transport: stdio" /root/.hermes/config.yaml
```

If the count is much higher than the configured stdio servers, you have a leak.

**Fix path (validated 2026-07-04):**

1. Identify which stdio servers have HTTP equivalents (most do)
2. Replace `command:` + `args:` with `url:` + `transport: streamable-http`
3. Move auth from env vars to the URL or a header
4. `hermes --yolo gateway restart`
5. Re-count processes — should drop by N

**When to keep stdio:**
- The binary has no HTTP serve mode (rare — check docs first)
- The binary requires interactive stdin (REPL agents, sequential-thinking)
- You're debugging a connection issue and need direct subprocess control

**When to migrate to HTTP:**
- Server is load-bearing (called every session, not just on-demand)
- Server has been stable for >7 days
- You see accumulating subprocess count in `ps`

## The standalone Hermes MCP server (port 18086)

Located at `/root/.hermes/mcp_servers/hermes_mcp.py`. Implements 6 read-only governance
diagnostic tools using FastMCP. Originally extracted from arifOS kernel on 2026-06-28 to
keep the kernel surface canonical.

**Tools exposed:**
- `hermes_system_status` — federation health snapshot
- `hermes_epistemic_check` — pre-flight confidence + gap analysis
- `hermes_fact_check` — claim verification against evidence
- `hermes_cross_verify` — delegate verification to a second agent
- `hermes_plan_review` — multi-step plan safety audit
- `hermes_memory_steward` — classify content for memory hierarchy

**Status (2026-07-04):** file exists, Python imports cleanly, port 18086 is FREE.
NOT registered in `config.yaml` mcp_servers block. Activation = add the YAML entry +
`hermes --yolo gateway restart`.

## Why this matters

Without hermes_mcp wired, the 6 diagnostic tools are unreachable. Agents in the federation
have to fall back to direct filesystem inspection + memory reads, which loses the structured
return format and the constitutional floor integration.

The activation cost is small (one YAML block + restart). The benefit is that every agent
gets first-class access to epistemic-check, plan-review, and fact-check as proper tools
instead of ad-hoc bash chains.

## See also

- `federation-mcp-bridge-2026-07-04.md` — base recipe for wiring any binary as MCP
- `non-interactive-config-append.md` — Python append pattern when shell heredoc is blocked
- `measure-before-acting` skill (failure modes 4, 5, 6) — same session produced these findings