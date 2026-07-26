# MCP/A2A Constitutional Split — 2026-07-12

> Sovereign verdict by Arif. Two separate constitutional planes inside arifOS.

## The Split

- **MCP** = capability execution (hands and senses) — tools, schemas, sessions, auth
- **A2A** = agent federation (relationships with other minds) — discovery, delegation, artifacts

## Bridge Split

`arif_route` dispatches to:
- `mcp_capability_call` → MCP tools/call
- `a2a_agent_delegate` → A2A task delegation

Do not disguise one as the other.

## Authority Law

Neither protocol carries sovereign authority by assumption.
- MCP tool call = "tool executed" ≠ "constitutionally approved"
- A2A agent response = "result produced" ≠ "accepted as truth"

Every cross-boundary result reclassified by arifOS before action.

## Full Architecture

```
ARIF / F13 → arifOS Kernel
    ├── MCP Control Plane (tools/resources/prompts/schemas/sessions)
    ├── A2A Federation Plane (agent discovery/tasks/delegation/artifacts)
    └── Evidence → Judge → Forge → Vault
```

GEOX as identifiable agent (not 20 remote MCP tools):
```yaml
agent:
  id: GEOX
  role: earth_evidence_intelligence
  capabilities: [basin_interpretation, seismic_reasoning, geological_uncertainty]
```

## Implementation Changes

1. Rename bridge semantics: `mcp_capability_call` + `a2a_agent_delegate`
2. Publish two cards: MCP server metadata + A2A Agent Card
3. One trace across both protocols
4. Protocol-specific conformance tests

## Provenance

Sovereign verdict 2026-07-12. Full spec at `forge_work/2026-07-12/MCP-A2A-PROTOCOL-SPLIT.md`.
