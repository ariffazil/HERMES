---
name: deep-codebase-audit
description: "Multi-dimensional codebase SOT (State of Truth) inventory — parallel git, filesystem, live service, governance framework, and vault inspection with cross-referencing against documentation claims."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, inventory, SOT, codebase, governance, epistemic, repo-inspection]
    related_skills: [codebase-inspection, plan, hermes-prime-federation-map]
prerequisites:
  commands: [git, curl]
---

# Deep Codebase Audit — SOT Inventory

Audit a codebase across multiple dimensions simultaneously, cross-referencing documentation claims against live state. This is NOT LOC counting — it's a structural, epistemic, and governance inventory.

## When to Use

- User asks to "take stock", "inventory", "SOT", "state of truth" for a repo
- User needs to understand the gap between documentation claims and reality
- User suspects structural drift (parallel dirs, stale docs, tool count mismatch)
- User asks about governance framework, vault integrity, or epistemic labeling
- User wants a baseline before making changes

## Core Pattern: Parallel Independent Investigations

Batch ALL independent probes in a single turn — do NOT serialize read-only checks:

```python
# Correct: batch in parallel
terminal(git_log_branch_dirty)
read_file(README, 30_)
terminal(find src/ -type d | head -80)
terminal(find . -name 'core' -type d)
terminal(curl :port/health)
web_extract(:port/health)  # fallback
```

Serialize ONLY when a later call depends on an earlier result (e.g., reading the tool list endpoint to check individual tools).

## Audit Dimensions

### 1. Git State
```bash
git log --oneline -1          # HEAD commit + message
git branch -a                  # local + remote branches
git status --short             # dirty files
git log --oneline -5           # recent history context
```

### 2. README / Documentation SOT-MANIFEST
- Check for `SOT-MANIFEST` block (GEOX-style HTML comment)
- Extract: owner, last_verified, live_commit, public_tools count, internal_tools count
- **Cross-reference:** does README's claimed commit match git HEAD? Does tool count match live service?

### 3. Source Directory Structure
```bash
find src/ -type d | head -80   # tree overview
find src/ -name '*.py' | wc -l # file count
find src/ -type d | wc -l      # dir count
```

### 4. Redundant/Parallel Directory Detection
```bash
# Check for duplicate named directories at different depths
find . -maxdepth 4 -type d -name '<name>' | sort
# For symlink farms: check if they point to same origin
ls -la <path>                  # reveals symlinks
file <path>/*.py               # shows real/resolved paths
```

### 5. Live Service Health Probe
```bash
# HTTP service health
curl -s http://127.0.0.1:<port>/health | python3 -m json.tool

# Tool list / surface
curl -s http://127.0.0.1:<port>/tools | python3 -c "
import sys,json; d=json.load(sys.stdin)
if isinstance(d,dict) and 'tools' in d:
    tools=d['tools']; print(f'Tools: {len(tools)}')
    for t in tools: print(f'  {t[\"name\"]}: {t.get(\"description\",\"\")[:60]}')
elif isinstance(d,list):
    print(f'Tools: {len(d)}')
"

# Service root
curl -s http://127.0.0.1:<port>/ | python3 -m json.tool
```

### 6. Vault / Seal Artifact Inventory
```bash
# Find vault directories
find . -maxdepth 3 -type d -name '*vault*' | sort
# List vault contents
ls -la <vault_dir>
# Check if multiple vaults exist (parallel vaults = split truth)
```

### 7. Governance / Epistemic Framework Mapping
- Search for `epistemic_label`, `truth_class`, `rung`, `governance`, `constitutional` in source
- Identify:
  - Epistemic ladder/rung system
  - Labeling taxonomy (OBS/DER/INT/SPEC or similar)
  - Contradiction resolution rules
  - Gödel wall / sealability constraints
  - Meta-audit layer
- Determine enforcement points (tool wiring, claim creation, runtime events)

### 8. Discrepancy Detection (Critical Step)
Compare claims across these sources for mismatches:
| Source | Example Claim |
|---|---|
| README SOT-MANIFEST | "public_tools: 26" |
| AGENTS.md | "tools/list ≈ 23" |
| Live /health | "public_tools=32" |
| Live /tools | 32 tools |
| registry.py | "CANONICAL = 77" |
| server.py | "_EXPECTED_CANONICAL = 77" |

Report every discrepancy with severity.

## Compilation Report

Write findings to `<repo>/_SOT_INVENTORY.md` with:
1. Git state table
2. README manifest audit (cross-refs)
3. Source structure stats
4. Redundant directory findings (with severity)
5. Live service surface (full tool table)
6. Vault integrity assessment
7. Epistemic framework summary
8. Discrepancy table
9. Overall findings summary with 🟢🟡🔴 severity

## Reference Files

- `references/geox-sot-inventory-2026-07-13.md` — Full worked example: GEOX organ inventory with command chain, discrepancy table, and epistemic framework map. Consult this for concrete patterns when auditing a new codebase.

## Pitfalls

1. **Never trust a single truth source** — cross-reference README vs live service vs registry
2. **Parallel vaults are a red flag** — multiple vault/ directories means split truth authority
3. **Symlink farms may hide stale refs** — check target resolution, especially multi-hop chains
4. **SOT-MANIFEST timestamps may be stale** — the live service /health is more authoritative
5. **Don't conflate "canonical target" with "live count"** — manifest may declare 77 but runtime serves 32
6. **Documentation drift is the norm, not the exception** — any mismatch is a finding worth reporting
7. **Check epistemic labeling quality** — not just that labels exist, but that they're enforced (contradiction ontology, Gödel wall, meta-audit)
8. **Use `web_extract` for health URLs only if `curl` is blocked** — the browser stack is overkill for JSON endpoints
