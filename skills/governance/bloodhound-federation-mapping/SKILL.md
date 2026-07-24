---
name: bloodhound-federation-mapping
title: BloodHound Federation Mapping
description: Map BloodHound AD attack-path concepts onto arifOS federation privilege topology — transport ≠ privilege, tool scope sweep, F13 reachability, consumer drift audit.
forged: 2026-07-24
authority: F13 SOVEREIGN (Arif)
status: LIVE
related_skills: [federation-checkup]
---

# BloodHound → arifOS Federation Mapping

## Core Architectural Insights

1. **Intent Router over Query Compiler**: bloodhound_mcp wraps Cypher into REST endpoints exposed as parameterised MCP tools. LLM is an Intent Router, not a query compiler. arifOS confirms this: GEOX/WEALTH/WELL follow the same pattern.

2. **Graph Topology vs Flat Records**: BloodHound analyzes edges (relationships between nodes), not isolated records. arifOS federation_edges.py probes 11 directed edges — but these are transport-level, not privilege-level.

3. **Delta-S < 0 Reconnaissance**: A few natural-language prompts map the entire AD attack surface. MCP reduces hundreds of graph edges into a prioritised risk matrix.

4. **888_HOLD Safeguard**: BloodHound MCP reads the graph and provides tactical playbooks but doesn't execute destructive actions. Matches arifOS F1 AMANAH doctrine: irreversible = 888_HOLD.

## Gap: Transport Topology ≠ Privilege Topology

| BloodHound Concept | arifOS Equivalent | Status |
|---|---|---|
| Shortest Path to DA (Domain Admin) | Shortest Path to F13 SOVEREIGN | ❌ No privilege graph — only transport probes |
| ACE/GenericAll/WriteDacl | Tool scope / mutation authority per organ | ❌ Not classified by F13 blast radius |
| AdminSDHolder propagation | FLOOR_TABLE consumer sync / CLAUDE.md inheritance | ⚠️ Drift audit created but not automated |
| DCSync (single principal, full domain) | Single over-broad MCP tool with F13 access | ⚠️ Tools enumerated but F13 privilege not fully mapped |
| bloodhound-python enumeration | arif_observe + federation_reality_probe.py | ✅ Exists and working |

## Tools Created

### Fasa 1: Drift Audit
- `/root/arifOS/scripts/audit_floor_consumers.py` — checks FLOOR_TABLE.json consumers against source of truth
- Usage: `python scripts/audit_floor_consumers.py --write-md`
- Exit codes: 0 (sync), 1 (drift), 2 (error)

### Fasa 2: Tool Scope Sweep
- Extended `/root/arifOS/scripts/federation_reality_probe.py` v2.0.0
- Added: `--scope` flag, `_sweep_tool_scopes()`, `_probe_f13_reachability()`, `_classify_tool()`, `_generate_attack_surface()`
- Usage: `python scripts/federation_reality_probe.py --scope --write-md --write-json`
- Outputs: BloodHound-style attack surface table with CRITICAL/HIGH/MEDIUM/LOW classification + estimated hops to F13

## Running the Full Chain

> **For operational execution with exact commands, probe sequences, and troubleshooting, see `federation-checkup` skill:**
> - Fasa 1 (Drift Audit): §Constitutional Source Drift Audit — FLOOR_TABLE Consumer Checks
> - Fasa 2 (Tool Scope Sweep): §Automated Artifact Generation (`make reality-deep`)
> - Fasa 3: This skill (conceptual mapping)

```bash
# 1. Drift audit (Fasa 1)
cd /root/arifOS && python scripts/audit_floor_consumers.py --write-md

# 2. Tool scope sweep (Fasa 2)
cd /root/arifOS && python scripts/federation_reality_probe.py --scope --write-md --write-json
```

## Key Principles

- **Transport alive != Privilege safe**: TCP health does not mean tool scopes are safely bounded
- **Remove the ACE, not the node**: Fix over-broad tool permissions, don't remove the organ
- **Auto-propagation is AdminSDHolder**: Any template inheritance (FLOOR_TABLE consumers, CLAUDE.md) is a persistence vector if not drift-checked
- **Sweep broad, not narrow**: One full-surface sweep beats N narrow queries for finding hidden edges
