---
name: corporate-legal-scrub
description: "Remove corporate entity references from git repos to avoid legal exposure. Systematic scrub: nuke dedicated directories, anonymize remaining references across source/tests/docs/contracts, verify zero hits, commit clean. Load when Arif says 'remove [company] references', 'legal scrub', 'clean up corporate mentions', or any task removing employer/client names from repos."
triggers:
  - "remove company references"
  - "legal scrub"
  - "corporate mentions"
  - "anonymize"
  - "PETRONAS"
  - "scrub repo"
  - "clean company names"
  - "dirty repositories"
  - "credential in repo"
  - "P0 audit"
  - "gitleaks finding"
  - "redact credential"
  - "gitignore credential"
args: []
---

# Corporate Legal Scrub

## When to Use

When a git repo contains references to a corporate entity (employer, client, partner) that could create legal exposure if discovered. Common scenario: former employer's name in technical repos built during employment.

## Procedure

### Phase 1: Discovery

```bash
# Count total mentions across repo
grep -ri "<ENTITY>" --include="*.py" --include="*.md" --include="*.json" --include="*.yaml" --include="*.ts" --include="*.js" -l . | wc -l

# Get per-file counts
grep -ri "<ENTITY>" -c . | sort -t: -k2 -rn | head -20

# Find dedicated directories
find . -type d -iname "*<entity>*"
```

### Phase 2: Risk Classification

| Category | Action | Risk |
|----------|--------|------|
| Dedicated directory (e.g., `docs/<entity>/`) | **Nuke entirely** | 🔴 HIGH — concentrated institutional analysis |
| Genesis/doctrine docs | **Anonymize** to generic terms | 🟡 MEDIUM — competitive intelligence |
| Source code comments/strings | **Anonymize** to `NOC-A`, `NOC`, `Malaysian NOC` | 🟡 MEDIUM — proves employment |
| Test data (operator names, fixtures) | **Anonymize** to `NOC_A`, `OPERATOR_A` | 🟢 LOW — but still traceable |
| Schema/contract descriptions | **Anonymize** to generic NOC references | 🟢 LOW |
| Benchmark notes ("not a <entity> well") | **Anonymize** | 🟢 LOW |

### Phase 3: Execution

```bash
# 1. Nuke dedicated directories
rm -rf docs/<entity>/

# 2. Anonymize source files (sed bulk replace)
# Map: entity name → generic term
# - "ENTITY" → "NOC-A" (in formal/technical contexts)
# - "ENTITY_MPM" → "NOC_A_MPM" (in test data)
# - "Entity subsidiary" → "NOC-AI-Partner" (for subsidiaries)
# - "entity_proprietary" → "noc_proprietary" (in code fields)
# - "Entity canonical" → "NOC canonical" (in comments)

# 3. For each file category:
sed -i 's/ENTITY/NOC-A/g; s/ENTITY_MPM/NOC_A_MPM/g' <file>

# 4. Verify zero remaining
grep -ri "<entity>" . | wc -l
# Must be 0
```

### Phase 4: Commit & Push

```bash
git add -A
git commit -m "chore(legal): remove all <ENTITY> references — nuke docs/<entity>/, anonymize source/tests/genesis/contracts

- Deleted docs/<entity>/ (N files: description)
- Anonymized ENTITY → NOC-A / NOC / Malaysian NOC in:
  - list of files modified
- Zero <ENTITY> references remaining in repo"
git push origin <branch>
```

### Phase 5: Archive for Human Memory

If the deleted files contain personal career intelligence worth preserving:

```bash
# Create private local archive (NOT in any git repo)
mkdir -p /root/.private/<entity>-memory
chmod 700 /root/.private/<entity>-memory

# Recover deleted files from git history
for f in $(git diff-tree --no-commit-id --diff-filter=D -r HEAD~1..HEAD --name-only | grep "docs/<entity>/"); do
  git show "HEAD~1:$f" > "/root/.private/<entity>-memory/$(basename $f)"
done

# Lock permissions
chmod 600 /root/.private/<entity>-memory/*

# Create README with file map and purpose
# Add .gitignore to prevent accidental commits
```

## Anonymization Mapping

| Original | Replacement | Context |
|----------|-------------|---------|
| PETRONAS | NOC-A / NOC / Malaysian NOC | Formal references |
| PETRONAS_MPM | NOC_A_MPM | Test operator strings |
| TriCipta | NOC-AI-Partner | Subsidiary/AI arm |
| petronas_proprietary | noc_proprietary | Code field names |
| Petronas field calibration | NOC field calibration | Technical claims |
| "PETRONAS canonical name" | "NOC canonical name" | Comments |

Adapt the mapping to the specific entity being scrubbed.

→ `references/petronas-scrub-mapping.md` — full mapping, file list, and commit receipt from the 2026-07-14 PETRONAS scrub.
→ `references/credential-hygiene-protocol.md` — P0/P1/P2 classification, credential redaction pattern, gitignore protection, and constitutional boundary violation response from the 2026-07-18 18-repo dirty audit.

## Pitfalls

- **Don't forget .bak files.** Old backup files may contain the original text. Search those too.
- **Don't forget GENESIS/ doctrine files.** These often contain competitive intelligence that's highly traceable.
- **Don't forget test fixtures.** Test data with real company names is still discoverable.
- **Check multiple branches.** The scrub commit may be on a feature branch — verify it reaches main.
- **Git history still contains the originals.** The scrub only cleans the working tree. For full removal, `git filter-branch` or BFG Repo-Cleaner is needed — but that's a separate, more destructive operation. The working-tree scrub is the minimum viable legal protection.
- **Subsidiary names are just as traceable.** "TriCipta" is a PETRONAS subsidiary — anonymize subsidiaries too.
- **Check f-string labels in Python.** `sed` replaces dict keys and string literals, but f-string labels like `petronas={result['noc_proprietary']}` have the label OUTSIDE the dict key. After bulk sed, grep for the entity name in print/f-string contexts specifically. **Proven 2026-07-14:** `sed` renamed `petronas_proprietary` → `noc_proprietary` in the dict key but left `petronas=` in the f-string label. Had to do a second pass.

## Provenance

- **Born:** 2026-07-14, PETRONAS scrub from GEOX repo (141 mentions, 16 files nuked, 10 files anonymized, 27 files changed, 1706 deletions).
- **Private archive:** `/root/.private/petronas-memory/` (18 files, owner-only permissions).
