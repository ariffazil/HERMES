# Human Tool Discovery — Visual Radar for Sovereign Operators

**Forged:** 2026-07-28 — Arif recognition: human is visual, agents discover via `tools/list`
**Problem:** 120+ MCP tools across 7 organs. Agent knows them all (JSON-RPC handshake). Human sovereign remembers ~3 (arif_init, arif_seal, arif_judge).

---

## The Asymmetry

| Who | Tool Discovery Mechanism | Capacity |
|-----|-------------------------|----------|
| **Agent** (Kimi Code, Hermes) | `tools/list` JSON-RPC call. All tool names + descriptions + schemas in < 1s. | Unlimited. Never forgets. |
| **Human** (Arif, sovereign) | Memory. Visual recognition. Category grouping. | ~5-7 tool names in active recall. Many more with visual cues. |

**This is not a human failing — it's a mode mismatch.** The human doesn't need to remember function signatures. The human needs a **visual radar** that shows what's available, grouped by organ, with live status.

---

## The Solution: Generic MCP UI Dashboard

### Why a Generic MCP UI Works

1. **Standard protocol.** MCP wire format (mcp.json) declares tools uniformly — name, description, inputSchema. Any MCP-compatible UI reads this automatically.
2. **Zero custom code.** No React app to build. `npx @modelcontextprotocol/inspector` or deploy `mcpui.dev` — point at the mcp.json registry and it renders all tools.
3. **Auto-discovery.** Add a new MCP server (Sylphx, Qdrant, etc.), and it appears in the UI without code changes. MCP protocol handles discovery.
4. **One surface covers all organs.** A-FORGE, GEOX, WEALTH, WELL, arifOS kernel — all in one dashboard. Grouped by organ prefix in descriptions.

### Mandatory Constraints

| Constraint | Reason |
|------------|--------|
| **localhost only (127.0.0.1)** | LOCALHOST_IS_PASSWORD doctrine. Never expose tool surface to public web. |
| **Read-only mode (OBSERVE/SUGGEST)** | Dashboard is for discovery, not execution. Tool calls still go through floor gates (F1-F13) and 888_HOLD. |
| **Organ tagging in descriptions** | Prefix tool descriptions with `[A-FORGE]`, `[GEOX]`, `[WEALTH]`, `[WELL]`, `[KERNEL]` so grouping is automatic. |

### How to Start

**Option 0: arifOS MCP Dashboard** (deployed 2026-07-28 — zero-dependency, unified view):
```bash
forge_mcp_ui_start
# Opens http://127.0.0.1:6200 — all 5 organs, 183 tools, dark theme, searchable, grouped
```
Pure Python stdlib, no deps. Reports live tool counts from every organ in single page view.

**Option 1: MCP Inspector** (official, per-server):
```bash
npx @modelcontextprotocol/inspector
```

**Option 2: mcpui.dev** (community, richer UI):
```bash
# Point to ~/.hermes/mcp.json or A-FORGE MCP registry
```

All bind 127.0.0.1 only. The sovereign opens any of these, sees all tools grouped by organ, and says "panggil tool tu" — agent executes intent → tool.

### The Workflow

```
Human opens MCP UI ──► scans tools by organ ──► finds the right tool
      │
      ▼
Human says (natural language): "Panggil forge_document_ingest untuk PDF ni"
      │
      ▼
Agent translates intent ──► floor check (F1–F13) ──► executes tool call
```

The MCP UI is a **discovery layer**, not an execution layer. It closes the gap between "I don't know what tools exist" and "use the right tool for this job."

---

## Key Doctrine

> **Agent discovers via tools/list. Human discovers via visual radar. Both are valid. The system must serve both.**
