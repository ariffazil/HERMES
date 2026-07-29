# Tool Discovery Gap — Human Visual Layer

**Canonical:** 2026-07-28 | **Ratified by:** Arif (F13 SOVEREIGN)

## The Gap

| | Agent | Human (Arif) |
|---|---|---|
| Tool access | JSON-RPC `tools/list` → 120+ tools in <100ms | Memory: "arif_init, arif_seal... lepas tu lupa" |
| Discovery | Vector-match intent → tool | Terpaksa tanya agent: "Tool apa untuk scan PDF?" |
| Cognitive load | Zero | High |

**Ini bukan kebodohan manusia. Ini architectural gap — tiada visual discovery layer.**

## The Solution: Intent → Route → Execute

Dua lapisan, kedua-dua diperlukan:

### 1. Primary: Natural Language + `arif_route`
Human speaks **INTENT**. Kernel routes **TOOL**. Agent executes.

```
"Periksa PDF ada prompt injection"
→ arif_route → forge_document_ingest + forge_scan
→ Agent execute → return result
```

### 2. Supplement: Visual GUI (mcpui.dev)
Untuk **awareness & spatial memory**. Bukan untuk execution.

- Zero custom code — MCP protocol standard
- Organ-grouped: A-FORGE (114), GEOX (32), WEALTH (12), WELL (8), arifOS (8)
- Visual inspection: name, description, inputSchema
- Execute still goes through governed path (arif_judge → forge_execute)

### Why Both

- GUI tanpa routing → kau masih kena ingat nama tool
- Routing tanpa GUI → kau tak nampak "apa yang ada"

## Architectural Insight

Tool discovery untuk manusia adalah **governance problem**, bukan UI problem.

Human tak patut ingat nama tool. Human patut sebut INTENT. Architecture patut ROUTE.

Ini falsafah `arif_route` — intent routing adalah constitutional gate, bukan search feature.
