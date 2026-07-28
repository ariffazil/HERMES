# BloodHound MCP Architecture Reconnaissance — Track B Worked Example

> Session: 2026-07-25
> Purpose: Cross-domain architecture reverse-engineering of BloodHound MCP, mapped to arifOS federation topology
> Pattern: Track B of external-wisdom-integration skill

## External System Analysed

**BloodHound MCP** (github.com/mwnickerson/bloodhound_mcp) — MCP server that wraps BloodHound CE Neo4j graph queries as REST API endpoints exposed to Claude Desktop via MCP protocol. Used for AI-assisted Active Directory security assessment.

## Architecture Description

The system has three layers:

1. **BloodHound CE** — Neo4j graph database + web UI on :8080, stores AD relationship topology
2. **bloodhound_mcp** — Python MCP server that wraps Cypher queries as `find_*` REST endpoints
3. **Claude Desktop** — MCP client that routes natural language prompts through the tool surface

Key architectural fact: the LLM NEVER writes Cypher queries. The MCP server exposes parameterised endpoints (`find_kerberoastable_users`, `find_shortest_path_to_da`) that the LLM calls as tools. The LLM's role is Intent Router + Context Synthesizer, not query compiler.

## Eureka Principles Extracted

| # | Principle | Description | arifOS Mapping |
|---|---|---|---|
| 1 | Intent Router over Query Compiler | LLM calls bounded parameterised tools, not writing free-form Cypher | arifOS tool schema as bounded ontology — tool definitions constrain LLM reasoning |
| 2 | Graph Topology over Flat Records | Risk lives in edges (GenericAll->DCSync->DA), not node attributes | Federation risk lives in tool->floor edges, not organ health status |
| 3 | Template Propagation = Hidden Transitive Closure | AdminSDHolder: write to template -> SDProp auto-propagates to all protected accounts | FLOOR_TABLE.json: write to constitutional template -> all consumer docs potentially drift |
| 4 | Dual-Authority Mismatch | DCSync rights exist on LDAP ACLs orthogonal to group-based RBAC | WEALTH capital_entropy should detect declared vs actual authority surfaces |
| 5 | Severity as Compressed Graph | BloodHound table collapses entire attack surface into User->Edge->Target->Severity | arifOS needs equivalent: Actor->Floor->Action->Severity matrix |

## Ground-Truth Verification Results

Checked files against live filesystem on 2026-07-25:

| Claim | File Checked | Reality | Finding |
|---|---|---|---|
| Transport topology exists | `/root/arifOS/arifosmcp/runtime/federation_edges.py` | 969 lines, 11 declared edges, TCP+identity+session probes | TRANSPORT_WELL_COVERED |
| Privilege topology exists | `/root/arifOS/arifosmcp/constitutional_map.py` | 3219 lines, tool access levels, NO floor-violation mapping | PRIVILEGE_PARTIAL |
| Floor canon exists | `/root/arifOS/GENESIS/FLOOR_TABLE.json` | 197 lines, 13 floors, F6 dual-register bridge, consumers list | CANON_EXISTS_UNGATED |
| Cross-organ probe exists | `/root/arifOS/arifosmcp/abi/cross_organ_probe.py` | 203 lines, HTTP health fetch from A-FORGE | TRANSPORT_ONLY |
| Organ capability probe exists | `/root/arifOS/arifosmcp/boot/capability_surface.py` | _probe_tool(), _probe_organ_health() | CAPABILITY_PROBE_EXISTS |

## Gap Analysis

| Gap | Severity | Existing Workaround | Closure Path |
|---|---|---|---|
| No shortest-path-to-F13 query | CRITICAL | Manual trace through tool access levels | Add governance distance metric to constitutional_map.py |
| No floor-violation-per-tool mapping | HIGH | Manual interpretation from tool type | Add TOOL_FLOOR_VIOLATION_MAP dict |
| No privilege reachability matrix | HIGH | Manual severity assessment | Extend federation_edges.py with privilege-level edges |
| No consumer drift auto-audit | MEDIUM | Manual FLOOR_TABLE.json diff | Add cron script to verify consumer sync |
| FLOOR_TABLE.json not chattr+i | MEDIUM | File is rw-r--r-- | Single chattr +i command |

## User Preferences Captured

From Arif's corrections during the session:

1. **Concrete over abstract** — "Make sure ALLIGNED with reality of the state." Before proposing any operationalisation, verify against live filesystem paths. Abstract theorising without file paths is rejected.
2. **Meaningful names only** — "No nama2 pelik2." Every filename, function, and concept must carry clear descriptive meaning. Session-specific codenames or "fix-X" labels are forbidden in persistent code.
3. **Structured Malay tables** — Comparison tables with Malay headers (e.g., "Pemerhatian | Seni Bina arifOS | Padanan") preferred over prose paragraphs for architectural mapping.
4. **Delegate for implementation** — "Spawn coding age ta for execution if needed." Does not want hand-holding on tool selection; delegate coding tasks to subagents with full context.
