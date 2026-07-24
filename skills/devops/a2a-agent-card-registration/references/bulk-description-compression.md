# Bulk Description Compression — Validated Run (2026-07-24)

**Corpus:** 22 A2A agent card JSON files across `a2a-server/agent-cards/`, `dist/`, and `AGENT_INDEX.json`
**Method:** Python script with recursive word-count + targeted compression map + threshold-based truncation
**Result:** 4,249 → 2,622 words — **38.3% reduction** (1,627 words cut)
**All 22 files validate:** `python3 -m json.tool` green on every file

## Per-File Breakdown

| File | Before | After | Cut | % | Notes |
|------|--------|-------|-----|---|-------|
| opencode.json | 481 | 247 | -234 | 48.6% | Heaviest card — verbose description + 15 skill descriptions |
| kimi-code.json | 311 | 130 | -181 | 58.2% | Skill descriptions compressed hardest |
| claude-code.json | 298 | 151 | -147 | 49.3% | Same pattern as opencode — shared skill IDs |
| aider.json | 259 | 112 | -147 | 56.8% | Lean card after compression |
| copilot.json | 260 | 113 | -147 | 56.5% | Same skill set as aider/codex |
| codex.json | 260 | 113 | -147 | 56.5% | Same pattern |
| antigravity.json | 217 | 91 | -126 | 58.1% | v2.1 schema, already leaner base |
| grok-build.json | 181 | 132 | -49 | 27.1% | Different skills from harnesses; less overlap in map |
| dist/*/agent-card.json (×2) | 273 ea | 163 ea | -110 | 40.3% | Gateway cards — needed separate pass (different skill names) |
| A-AUDIT.json | 415 | 346 | -69 | 16.6% | Many unique skill descriptions, less map coverage |
| A-ARCHIVE.json | 369 | 304 | -65 | 17.6% | Deprecated card — fewer shared skills |
| openclaw.json | 372 | 317 | -55 | 14.8% | Gateway — unique skill set, less compression |
| forge cards (8 files) | 25-52 ea | 20-47 ea | -5-8 | ~15% | Already lean from forge template — minimal gain |
| AGENT_INDEX.json | minor | minor | — | — | Prose fields compressed separately |

## Compression Map Used

### Security scheme descriptions (common across ALL harness cards)
```
Before: "arifOS session token issued via arif_session_init"
After:  "arifOS session token (JWT)"

Before: "Static API key for organ-to-organ federation calls"
After:  "Static API key for federation calls"
```

### Skill descriptions (shared across all FI harness cards)
```
Skill Name                    Before (words)  After (words)
───────────────────────────   ──────────────  ──────────────
Hermes/OpenCode Protocol      18              10
Agentic Architecture          14              9
Fabrication Prevention        18              6
Autonomous Governed Exec.     28              6
arifOS Constitutional Audit   22              7
Gödel Humility Lock           14              6
GitHub Workflow               16              5
arifOS MCP Federation         15              7
Agentic Builder               16              7
Reality Skills (F2 Grounding) 12              8
Sovereign Recognition (F13)   12              7
Session Inhabit (Lifecycle)   12              7
RSI Recursive Improvement     10              6
Trinity-33                    10              5
MCP Zen                       14              8
Forge Verbs                   12              7
MCP Builder                   13              7
```

### Gateway card skill descriptions (dist files)
```
Skill Name                    Before (words)  After (words)
───────────────────────────   ──────────────  ──────────────
Task Routing                  14              9
Sovereign Veto Enforcement    15              9
Capability Aggregation        12              7
Webhook Broker                13              8
Injection Defense             12              7
Federated Memory Query        18              4
```

## What NOT to compress

- `mcp_surface` endpoints, tool lists, tool_count, key_lanes — these are structured data
- `subAgentPolicy` — governance policy objects
- `autonomy_tiers` — structured T1/T2/T3 definitions
- Capabilities booleans (streaming, pushNotifications, etc.)
- `floor_scope` arrays
- `tags` arrays
- `securitySchemes` type/name/in fields (only descriptions)
- `a2a_transport` and `mcp_binding` objects
- `signatures` arrays
- `apexMasterSeal` objects
- `skills[].examples` arrays — useful for discovery
- `skills[].inputModes` / `outputModes` arrays
- `skills[].tags` arrays

## Re-run Pattern

To re-run this compression on the current corpus:

```python
SKILL_DESC_MAP = {
    "Hermes/OpenCode Protocol": "Unified governed execution protocol: 777 FORGE under F1-F13 with 888_HOLD.",
    "Agentic Architecture": "Design sovereign agentic agents. 9-skill spine, F8/F11 enforced.",
    "Fabrication Prevention": "Verify before claiming existence. F2/F9 enforced.",
    "Autonomous Governed Execution": "Governed execution: T1/T2 auto, T3→888_HOLD. F1-F13 enforced.",
    "arifOS Constitutional Audit (Light)": "Read-only six-organ audit. F1-F13 enforced.",
    "Gödel Humility Lock": "Epistemic humility before SEAL-grade claims. F2/F7 enforced.",
    "GitHub Workflow": "GitHub ops: repos, PRs, issues, review. F1/F11 enforced.",
    "arifOS MCP Federation": "Route tasks across federation MCP servers. F4/F11 enforced.",
    # ... extend as new skill names are added to cards
}

BEARER_DESC_SHORT = "arifOS session token (JWT)"
APIKEY_DESC_SHORT = "Static API key for federation calls"
```

For each file: load JSON → compress `description` if >25 words → compress each skill description via map → compress security descriptions → write back → validate with `json.tool`.
