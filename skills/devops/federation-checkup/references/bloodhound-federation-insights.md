# BloodHound → arifOS Federation Insights

> Captures the Transport ≠ Privilege doctrine from BloodHound MCP analysis (2026-07-24).
> For operational execution, see `federation-checkup` SKILL.md.

## Core Doctrine: Transport Topology ≠ Privilege Topology

BloodHound proves: TCP connectivity (0 hops transport) ≠ governance access (0 hops privilege).

In AD: every host is TCP-reachable from Kali, but only specific ACE paths grant DCSync.
In arifOS: every organ is port-reachable from localhost, but only 3 tools (`arif_forge`, `arif_judge`, `arif_seal`) are 1-hop from F13.

### What This Means

- `probe_all_edges()` showing 11/11 transport reachable ≠ federation secure
- The real security surface is: **which tools can mutate constitutional state?**
- F1-F13 violations come through privilege edges, not transport edges

## 3-Phase Audit Architecture

| Phase | Name | What | Tool |
|---|---|---|---|
| Fasa 1 | Drift & Seal Check | Verify FLOOR_TABLE consumers are synced, files are immutable | `federation-checkup` SKILL.md §Constitutional Source Drift Audit |
| Fasa 2 | Tool Scope Sweep | Classify every MCP tool by F13 mutation scope | `federation_reality_probe.py --scope` |
| Fasa 3 | Skill Sealing | Document doctrine as governance skill | `bloodhound-federation-mapping` SKILL.md |

## Key Findings (2026-07-24)

### 3 Tools = 1 Hop to F13
- `arif_forge` — Constitutional mutation (execution)
- `arif_judge` — Constitutional verdict (SEAL/HOLD/VOID)
- `arif_seal` — VAULT999 append (immutable write)

### Consumer Drift Pattern (AdminSDHolder analog)
FLOOR_TABLE.json is the template. Its 4 consumers (AAA AGENTS.md, Wealth.tsx, wealth-static-render.py, GEOX claim workflow) each have drifted from canonical. The GEOX SPEC rejection gate absence is the most critical — allows SEAL without truth_class check.

### Streamable HTTP Protocol Mismatch
WEALTH, WELL, GEOX, A-FORGE use Streamable HTTP transport that returns HTTP 400/0 tools on raw `tools/list` POST. `federation_reality_probe.py` needs SSE client framing for future full coverage.

## BloodHound AD → arifOS Mapping

| BloodHound Concept | arifOS Analog |
|---|---|
| Tier Zero / DA | F13 SOVEREIGN |
| ACE / Hidden Edges | Tool Scope / Floor Violations |
| AdminSDHolder Propagation | FLOOR_TABLE / Constitutional Templates |
| DCSync Right | Single over-broad MCP tool |
| Cypher Shortest Path | Governance distance to F13 |

## Remediation Priorities

1. `chattr +i` on FLOOR_TABLE.json (no files are currently immutable)
2. Patch GEOX claim state machine to reject SPEC for SEAL
3. Fix Wealth.tsx F9 naming (ANTI-CASCADE → ANTIHANTU) and color
4. Fix wealth-static-render.py F9 color
5. Upgrade federation_reality_probe.py for Streamable HTTP
6. Rewrite AAA AGENTS.md from stub (7 lines) to full F1-F13 render
