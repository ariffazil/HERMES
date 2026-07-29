---
name: federation-alignment-sweep
description: >-
  Sweep agent configuration for naming drift, stale references, and federation
  misalignment after consolidation phases. Covers tool rename audit, handoff
  protocol APEXMax→arif_judge migration, skills federation, and zen alignment
  report. Use when user says "post-consolidation sweep", "alignment sweep",
  "agent config audit", "phase N consolidation sweep", "openclaw sweep".
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, alignment, sweep, consolidation, federation, agent-config, tool-drift]
    related_skills: [federation-checkup, governance-enforcement-audit, a2a-agent-card-registration, mcp-naming-contract]
prerequisites:
  commands: [grep, find, python3]
---

# Federation Alignment Sweep — Post-Consolidation Agent Config Audit

**Audit and repair agent configuration drift after a naming/consolidation phase.**

When tools are renamed (e.g., `arif_session_init` → `arif_init`), protocols updated (APEXMax → arif_judge), or skills consolidated (multiple Nasi Lemak scripts → one canonical skill), every agent's config files must be swept for stale references. This skill provides the systematic protocol.

## When to Load

- User says "post-consolidation sweep", "alignment sweep", "phase N consolidation alignment"
- After tool renaming/consolidation in the arifOS kernel (canonical tool set changed)
- After protocol changes (APEXMax → arif_judge, or similar)
- After skill consolidation (multiple redundant skills → one canonical skill per class)
- "Audit OpenClaw config for drift", "check agent config alignment"
- Before sealing a consolidation phase

## Core Principle

**A consolidation is not complete until every agent config file that references the old names has been updated.** Leaving stale tool names in `config.yaml`, `TOOLS.md`, or `agent-card.json` creates silent failures when agents can no longer call the named tools.

## The 6-Phase Protocol

### Phase 1 — Inventory & Discovery

First, discover the agent's file layout and identify all config files that may contain tool/handoff/skill references:

```bash
# Typical agent directory
ls agent-card.json config/config.yaml config/handoff-protocol.yaml TOOLS.md AGENTS.md SOUL.md IDENTITY.md procedures/

# Federation registry
cat registries/skills.yaml  # or search for the consolidated skill IDs
```

Check the file layout (use `search_files(target='files')` for directory listing).

Extract the canonical tool set from the current kernel definition. The canonical arifOS kernel tools as of 2026-07-29:

```
arif_init    — Session ignition, F1-F13 binding
arif_observe — Reality observation and evidence gathering
arif_think   — Structured reasoning under F2/F7
arif_judge   — 888 constitutional verdict
arif_forge   — Execution gate via A-FORGE
arif_seal    — VAULT999 immutable append
arif_memory  — Governed L1-L6 semantic recall
arif_route   — Intent-to-organ dispatch
```

### Phase 2 — Tool Name Drift Scan

Search each config file for deprecated tool names. Common deprecated → canonical mappings:

| Deprecated | Canonical | Found In |
|---|---|---|
| `arif_session_init` | `arif_init` | config.allowed_tools, TOOLS.md, securitySchemes descriptions |
| `arif_sense_observe` | `arif_observe` | config.allowed_tools, TOOLS.md |
| `arif_kernel_route` | `arif_route` | config.allowed_tools, TOOLS.md |
| `arif_judge_deliberate` | `arif_judge` | config.allowed_tools, TOOLS.md |
| `arif_memory_recall` | `arif_memory` | config.allowed_tools, TOOLS.md |
| `arif_mind_reason` | `arif_think` | config.allowed_tools, TOOLS.md, AGENTS.md (workflow/bootstrap sections) |
| `arif_act` | `arif_forge` | agent-card.json MCP surface, TOOLS.md |
| `arif_vault_seal` | `arif_seal` | AGENTS.md (key tools table), SOUL.md, lane configs |

For each match found, record the file, line number, and deprecated name.

**Pitfall:** `securitySchemes` descriptions in `agent-card.json` often contain stale tool names. Patch `description` fields referencing old names — they're doc strings, not functional tool references, but they show up in federation agent discovery and imply the agent expects the old tool name.

Also check for MISSING canonical tools — tools that should be in the `allowed_tools` or MCP surface list but are absent:

```python
CANONICAL = {"arif_init", "arif_observe", "arif_think", "arif_judge",
             "arif_forge", "arif_seal", "arif_memory", "arif_route"}
```

### Phase 2b — Stale Kernel Skill Reference Scan

Agent cards carry `kernel_deps` and `kernel_skills` arrays (in `metadata` and at top level) listing the kernel skills the agent subscribes to. When kernel skills are renamed or retired, these arrays accumulate stale references that mislead agent initialisation about what capabilities are available.

Known-retired kernel skill IDs:

| Retired ID | Reason |
|---|---|
| `KERNEL-quantum-runtime` | Quantum-computing framing removed in Phase 6 consolidation |
| `KERNEL-qubit-substrate` | Same — Phase 6 quantum removal |

Both appear in the `kernel_deps` array inside `metadata` and the `kernel_skills` array at the agent card top level. Remove them from both locations.

**Pitfall:** These are not self-referential data — they're declaration arrays. Removing a retired entry does NOT require adding a replacement. The remaining skills (e.g. `KERNEL-trinity-33`, `KERNEL-session-inhabit`, `KERNEL-sovereign-recognize`, `KERNEL-verbs-forge-hands`, `KERNEL-reality-skills`, `KERNEL-mcp-zen`, `KERNEL-mcp-builder`) form the current canonical set.

### Phase 2c — AGENTS.md Tool Surface Table Scan

`AGENTS.md` files contain a markdown table listing MCP servers and their "Key Tools". These tables commonly reference deprecated tool names long after the JSON config files have been fixed, because the table is maintained manually.

Search pattern — look for these stale names in markdown tables under `Key Tools` column headers:

```
grep -rn 'session_init\|judge_deliberate\|vault_seal\|mind_reason\|sense_observe' **/AGENTS.md
```

The fixed mapping for AGENTS.md tables:

| Stale (in table) | Canonical |
|---|---|
| `session_init` | `arif_init` |
| `judge_deliberate` | `arif_judge` |
| `vault_seal` | `arif_seal` |
| `mind_reason` | `arif_think` |
| `sense_observe` | `arif_observe` |

**Pitfall:** AGENTS.md tool entries are not qualified — they appear as bare names without the `arif_` prefix. The canonical name uses the full `arif_` prefix. Both old bare names (e.g. `session_init`) and old qualified names (e.g. `arif_session_init`) can appear in the same file; scan for both patterns.

### Phase 3 — Protocol Reference Migration

Search for stale protocol references. The most common migration (as of 2026-07-29):

```
APEXMax → arif_judge
APEX    → arif_judge     (in context of judgment, not APEX scoring)
apexmax → arif_judge
```

Check these files:
- `config/handoff-protocol.yaml` — most common location for APEXMax references
- `AGENTS.md` — may reference APEXMax in routing docs
- `config/config.yaml` — may reference in comments or agent descriptions

For each match, create a mapping:
```yaml
old_reference: APEXMax
new_reference: arif_judge
file: config/handoff-protocol.yaml
context: decision_tree routing, JUDGE_REQUEST, forbidden rules
```

**Pitfall:** Also check field names, not just values. `hermes_action_post_apex` should become `hermes_action_post_judge`. Description text like "Route to APEXMax if 888_HOLD" should become "Route to arif_judge if 888_HOLD".

### Phase 4 — Skills Federation

After consolidated skills are created (multiple redundant skills → one canonical class-level skill), ensure the federation registry knows about them for A2A delegation routing.

For each consolidated Hermes skill, add a federation-aware entry to the skills registry:

```yaml
- id: federated-<short-name>
  name: FEDERATED-<canonical-name>
  version: 1.0.0
  description: One-line description of the consolidated skill
  owner: Hermes (federated via AAA)
  risk_tier: <low|medium|high>
  status: consolidated
  peer_scope: hermes-asi
  delegation_path: A2A → Hermes → execute
  source_path: federated/hermes/<canonical-name>
  package: federated-hermes
  floor_scope:
    - F1       # Always present — AMANAH
    - F<num>   # Per-skill floor scope
```

When placing the entries in the registry:
1. Read the last skill entry to understand the format
2. Use patch with sufficient context to ensure uniqueness
3. Verify the file is valid YAML after the patch

Typical consolidated skills that need federation entries:
| Consolidated Skill | Source Skills Merged | Risk Tier |
|---|---|---|
| autonomous-vps-response | vps-operations, autonomous-response | medium |
| nasi-lemak-tracking | Multiple retail nasi lemak scripts | low |
| flame-free-loop-mesh | Free-loop model engine | low |
| telegram-userbot-telethon | Telegram userbot scripts | medium |
| trading-stack | trading-signal-chart, agentic-trading-companion, mt5-ai-trading-agent | high |

### Phase 5 — Zen Alignment Verification

Verify the agent's identity documents are current and consistent. Check these dimensions:

| Check | What to Verify | Pass/Fail Signal |
|---|---|---|
| **000-999 loop** | AGENTS.md has correct stage table with agent's role per stage | Table present with Init→Observe→...→Seal |
| **F1-F13 enforcement** | Constitutional Laws section lists applicable floors | At least F1, F2, F12, F13 referenced |
| **A2A peers** | Correct peer agents listed with tiers | opencode, hermes-asi, arifOS kernel listed |
| **ART binding** | References correct paths (art.py, not deprecated art_unified) | Path exists, file size ≤500 lines |
| **Stale org references** | No references to deleted/renamed directories | No hermes-* root dirs, no APEX dirs |
| **SOUL.md** | Voice/boundaries current, no stale protocol names | No deprecated tool names, no APEXMax |
| **IDENTITY.md** | Role/authority correct | matches AGENTS.md |
| **Last-updated dates** | Should be recent (within ~1 month of sweep) | Flag as stale if >3 months old |

**Pitfall:** Record all findings — even minor ones like stale last-updated dates. These go into the alignment report as low-severity gaps.

### Phase 6 — Alignment Report

Write a structured JSON report to `forge_work/<date>/<agent>-alignment-report.json`:

```json
{
  "$schema": "arifOS/audit-report/v1",
  "report_id": "<agent>-alignment-sweep-<date>",
  "generated_at": "<ISO8601>",
  "generated_by": "Hermes Agent — <phase description>",
  "phase": "<description>",
  "seal_status": "SEAL-READY after verification",

  "summary": {
    "tools_updated": <count>,
    "tools_added": <count>,
    "stale_references_fixed": <count>,
    "skills_federated": <count>,
    "zen_gaps_found": <count>,
    "zen_gaps_severity": "<low|medium|high>",
    "files_modified": <count>,
    "files_created": <count>,
    "seal_ready": true
  },

  "section_1_tools_update": {
    "status": "COMPLETED",
    "canonical_tool_set": [...],
    "deprecated_to_canonical_mapping": { "old": "new", ... },
    "files_updated": [
      { "file": "<path>", "changes": "<description>" }
    ],
    "legacy_custom_tools_retained": [...]
  },

  "section_2_protocol_migration": {
    "status": "COMPLETED",
    "old_name": "APEXMax",
    "new_name": "arif_judge",
    "references_fixed": <count>,
    "files_updated": [...]
  },

  "section_3_skills_federation": {
    "status": "COMPLETED",
    "skills_registry": "<path>",
    "skills_added": [...]
  },

  "section_4_zen_alignment": {
    "status": "COMPLETED",
    "checks": {
      "000-999_loop_reference": { "status": "PASS|FAIL", "detail": "..." },
      ...
    },
    "gaps_found": [
      { "severity": "LOW", "category": "...", "detail": "...", "recommended_action": "..." }
    ]
  },

  "section_5_files_modified": [
    { "path": "<path>", "change": "<description>" }
  ],

  "verification": {
    "deprecated_names_remaining": 0,
    "stale_references_remaining": 0,
    "skills_federated_count": <count>,
    "seal_ready_verdict": "SEAL-READY",
    "condition": "<summary>"
  }
}
```

The report is the deliverable that gets sealed to VAULT999. It serves as the canonical record of what was found, what was fixed, and what gaps remain.

## Pitfalls

1. **One file at a time.** After editing each config file, verify the tool was applied correctly before moving to the next. Use `patch` with unique context strings.

2. **Legacy custom tools may have no canonical equivalent.** Tools like `arif_gateway_connect`, `arif_ops_measure`, `arif_heart_critique`, `arif_reply_compose`, `arif_evidence_fetch` don't map to the canonical 8. Retain them with annotations — don't delete without understanding their runtime usage.

3. **agent-card.json MCP surface may list tools that don't match the live kernel.** The card is a static document; the live kernel evolves. Always note the last-known-good tool set from the kernel, not from the card.

4. **APEXMax references may be in field names, not just values.** Search for `hermes_action_post_apex`, `apexmax_action`, and similar field names in YAML/JSON configs.

5. **The skills.yaml `- F13` end-of-file is not unique.** The string `- F13` appears on most skill entries. Always match the last skill entry's full block (name + version + floor_scope) to ensure uniqueness.

6. **Skills-index.json may be stale.** The discovery index at `registries/discovery/skills-index.json` may claim "registry stale by 60 skills" — that's a separate concern from the federation registry at `registries/skills.yaml`.

7. **Fleet-wide scope.** Stale tool references rarely affect only one agent card. After a Phase-X consolidation, ALL agent cards under `/root/AAA/agents/` (including `_external/`, `_lanes/`, and all named agent directories) should be swept, not just the one the user initially asked about. The user may only have time to fix a subset — flag the remaining affected cards in the audit report as unaddressed scope.

8. **JSON syntax after edits.** After removing entries from JSON arrays, run `python3 -m json.tool` or a validation script to confirm the result is syntactically valid JSON. Removing the wrong comma can break the file silently, particularly when removing entries from the middle of an array.

9. **Do NOT modify Hermes Agent skills directly** during an OpenClaw sweep. Only update OpenClaw's federation surface (skills registry, config files, agent card). Hermes skills are managed separately.

10. **Last-updated dates in agent docs are easy to miss.** TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md, IDENTITY.md may all show dates from months ago. Flag them as low-severity gaps but don't update them without user direction — they're cosmetic.

11. **The report must reflect reality, not aspirations.** If a gap is purely cosmetic (stale dates, experimental kernel deps), say so. Don't overstate severity. Don't claim SEAL-READY if any blocking issue remains.

## Verification

After all patches are applied, run a final sweep to confirm zero remaining:

```bash
# For each deprecated name pattern — tool references
grep -rn 'arif_session_init\|arif_judge_deliberate\|arif_sense_observe\|arif_kernel_route\|arif_memory_recall\|arif_mind_reason\|arif_act\|arif_vault_seal\b' agent-directory/

# AGENTS.md tool surface table bare names
grep -rn 'session_init\|judge_deliberate\|vault_seal\|mind_reason\|sense_observe' **/AGENTS.md

# Protocol and field-name references
grep -rn 'APEXMax\|apexmax\|APEX verdict\|action_post_apex' agent-directory/

# Retired kernel skills
grep -rn 'KERNEL-quantum-runtime\|KERNEL-qubit-substrate' agent-directory/
```

Confirm tool counts in agent-card.json match the canonical set (8 tools for arifOS kernel MCP surface).

## References

See `references/openclaw-alignment-sweep-2026-07-29.md` for the full worked example — OpenClaw sweep with all 6 phases, 5 files modified, 8 APEXMax references migrated, 6 deprecated tools updated, 5 skills federated.
