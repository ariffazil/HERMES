# Registry Drift Patterns — Federation Substrate Enforcement

> Forged: 2026-07-05 from Phase 1 enforcement session
> Related skill: `federation-config-reconciliation`
> Document: `/root/AAA/docs/FEDERATION-SUBSTRATE-RULES.md`

---

## The Problem

In a multi-organ federation, the same logical registry (tool list, agent cards, schemas) exists in multiple physical locations. Without canonical write path enforcement, drift is guaranteed — not a risk, a certainty.

**Proof from live audit (2026-07-05):**
- 5 tool registry files → 5 different SHA256 hashes (none match)
- 5 agent card directories → 28 files in canonical, 1-5 files in stale copies
- 1 broken JSON file in deprecated APEX directory

---

## Drift Classes

| Class | Symptom | Fix |
|---|---|---|
| **DEPRECATED** | File in decommissioned directory (e.g., APEX/ASF1) | Remove + backup |
| **STALE_SUBSET** | Copy has fewer entries than canonical (e.g., OpenClaw agent-cards with 3 files vs 28 in canonical) | Remove + symlink to canonical |
| **DIFFERENT_FORMAT** | Same name but different schema/purpose (e.g., TOOLREGISTRY.json vs TOOL_MANIFEST.json) | Keep both, update scanner to mark as KNOWN_DIVERGENT |
| **DRIFT** | Same purpose, different content | Identify canonical, convert others to symlinks or read-only mirrors |

---

## Enforcement Script Pattern

```bash
#!/bin/bash
# Canonical write path enforcement — non-destructive, backup-first

set -e
BACKUP_DIR="/root/.local/share/arifos/registry-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# For each registry type:
# 1. Identify canonical path
# 2. Find all copies (find -name ...)
# 3. For each copy: backup, remove, symlink
# 4. Deploy drift scanner
```

---

## Drift Scanner Pattern

Deploy to `/root/.hermes/scripts/registry-drift-scanner.sh`:
- SHA256 comparison between canonical and mirrors
- Symlink validation (resolves link target)
- Missing file detection
- JSONL output to `/var/arifos/artifacts/logs/registry-drift.jsonl`
- Exit code = drift count (0 = clean)

Run via daily cron: `0 3 * * * bash /root/.hermes/scripts/registry-drift-scanner.sh`

---

## Pitfalls

### 1. Don't symlink blindly

`arifOS/TOOL_MANIFEST.json` (13 tools, MCP server manifest) and `AAA/docs/TOOLREGISTRY.json` (10 governed skills with capability tags) serve **different purposes**. Symlinking one to the other breaks both. Check file structure before converting to symlink.

### 2. APEX is decommissioned

Port 3002 retired 2026-06-27. Anything under `/root/arifOS/APEX/` is legacy. Safe to remove with backup. APEX warga agent (888-APEX) lives in `/root/AAA/agents/888-APEX/` — that's separate.

### 3. OpenClaw workspace copies are stale by design

When workspace gets cloned/forked, agent-cards directory gets copied once then never updated. These are always stale subsets. Safe to symlink to canonical A2A surface.

### 4. AAA/registries/TOOL_MANIFEST.json is metadata, not a skill list

This file contains federation manifest data (supply_gates, missing_layers, live_attestation) — not a list of skills/tools. It's a different contract entirely.

---

## Phase Migration Plan

| Phase | Action | Effort |
|---|---|---|
| 1 | Remove deprecated, symlink stale subsets, deploy scanner | Done 2026-07-05 |
| 2 | Analyze format-different registries, decide merge vs keep separate | Pending |
| 3 | WELL RLS schema + GEOX blob formalization | Pending |
| 4 | ACL enforcement + naming guard | Pending |
