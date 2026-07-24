# arifOS Kernel SOT Inventory — Worked Example (2026-07-12)

This reference captures the session that produced the `repository-sot-inventory` methodology. It serves as a concrete example of every phase in the workflow.

## Repository Under Audit

```
Path:       /root/arifOS
Live port:  8088 (health endpoint)
Domain:     https://arifos.arif-fazil.com
Type:       Constitutional AI governance kernel (MCP server + federation hub)
Owner:      Arif bin Fazil
```

## Phase 1: Parallel Probe Commands Used

```bash
# Git
cd /root/arifOS
git log --oneline -5
git branch -a
git status --short
git diff --stat HEAD

# GENESIS listing
ls -la GENESIS/

# Docs listing
find docs/ -type f | sort
find docs/ -type f | wc -l

# Live service
curl -s http://127.0.0.1:8088/health

# Key docs
read_file README.md
read_file identity.toml
read_file docs/AUTHORITY_MODEL.md
read_file docs/CONSTITUTION.md  # (redirect, note this!)
```

## Phase 2: Search Patterns Used

```bash
# Pattern: VAULT999 references
search_files --path /root/arifOS --pattern VAULT999 --limit 30 --output_mode files_only

# Pattern: Constitutional floors + identity/authority
search_files --path /root/arifOS --pattern "constitutional.*floor|F13|F12|sovereign.*veto|identity.*contract|authority.*model" --limit 30 --output_mode files_only

# Pattern: Identity files 
search_files --path /root/arifOS --pattern identity --file_glob "*identity*" --limit 20 --output_mode files_only

# Numbering conflicts in GENESIS/
ls GENESIS/ | grep -E "^0(06|07|40)"

# Case-insensitive duplicates in .arifos/
ls .arifos/ | sort -f | uniq -di
# Found: REALITY_LAWS.md vs REAlITY_LAWS.md

# Archived count
find docs/archive/pre-genesis-2026-06-06 -type f | wc -l
# Result: 74

# Total .md count (non-git)
find . -name "*.md" -not -path "./.git/*" | wc -l
# Result: 1,419
```

## Phase 3: Key Cross-References Made

| Claim | Verification | Result |
|---|---|---|
| README: 12 canonical tools | Health: tools_loaded=8 | MISMATCH — 8 public + 16 internal hidden + 58 registry total |
| README: owner_summary=GREEN | Health: owner_summary=YELLOW | MISMATCH — runtime drift detected |
| README: live_commit=2fc0089 | Health: live_commit=182266c, build=1403cac | MISMATCH — 3 different commits across surfaces |
| README: runtime_drift=false | Health: runtime_drift=true | MISMATCH — container vs branch divergence |
| docs/CONSTITUTION.md exists | Contains only redirect | Redirect: points to static/arifos/theory/000/000_CONSTITUTION.md |

## Phase 4: Report Structure Used

The final SOT report had 10 sections:
1. Git State (table)
2. GENESIS/ Directory (table + numbering anomalies flagged)
3. docs/ Structure (subdirectory counts)
4. README Metadata (table)
5. Live MCP Surface State (tool count semantics table)
6. Constitutional Doctrine Files (table)
7. VAULT999 References (30 files, key refs listed)
8. Identity/Authority Contracts (file list)
9. Duplicate/Superseded Documents (severity-graded table)
10. Summary Statistics (table) + Key Findings (5 items)

## Notable Finding Categories Found

### Tool Count Semantics (4 different surfaces)
- Public MCP facade: 8 tools (exposed via `forge_next_8` mode)
- Internal superset: 24 tools (8 public + 16 hidden internal)
- Registry: 58 callables
- Total declared: 48 (8 public + 40 diagnostic)
- README declared: 12 (does not match any live count)

### File-system-only Detections
- `REALITY_LAWS.md` vs `REAlITY_LAWS.md` — differing only in capital 'A'
- 3 numbering conflicts in GENESIS/ (006, 007, 040 each have 2 files)
- 74-file bulk archive from pre-consolidation epoch
- 1 redirect-only doc (CONSTITUTION.md)

### Live-vs-Doc Mismatches
- Runtime drift = TRUE (build ≠ live HEAD)
- Owner summary = GREEN vs YELLOW

## Lessons for Future SOT Inventories

1. **Tool count is never a single number.** Always report it from multiple vantage points with explicit semantics for each.
2. **Check the health endpoint even if it seems up.** The health response IS the source of truth for live state, not the README.
3. **Case-insensitive filename dupes are invisible to most search tools.** Use `sort -f | uniq -di` specifically.
4. **Archive directories suppress the real doc count.** Always report live vs archived separately.
5. **Redirect-only docs are not empty — they tell you where the real content lives.** Report them as redirect layers.
6. **GENESIS numbering conflicts signal incomplete consolidation.** Two files with the same number means a rename/merge never completed.
7. **Cross-referencing README vs health catches the most actionable drift.** Every SOT should treat this as the primary reconciliation.
