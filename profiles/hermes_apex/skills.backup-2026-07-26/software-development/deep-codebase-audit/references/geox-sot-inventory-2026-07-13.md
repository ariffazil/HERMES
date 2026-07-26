# GEOX SOT Inventory — Reference Example

**Session:** 2026-07-13  
**Repo:** /root/GEOX  
**Organ:** Earth Evidence (arifOS Federation)

## Quick Reference: Command Chain

### Git State
```bash
cd /root/GEOX
git log --oneline -1       # 5bc66284 refactor: align tool manifest with registry truth
git branch -a              # on refactor/apex-entropy-20260712, 7 branches
git status --short         # D FEDERATION_CONTRACT.md.bak.pre-pointer-2026-07-12
```

### Source Stats
```bash
find src/ -name '*.py' | wc -l   # 498
find src/ -type d | wc -l        # 163
```

### Redundant Core Detection
```bash
find . -maxdepth 4 -type d -name 'core' | sort
# Returns: /root/GEOX/core, /root/GEOX/geox/core, /root/GEOX/src/geox_core/core

# /root/GEOX/core/        — 28 symlinks + 2 real files → ../src/geox_core/core/
# /root/GEOX/geox/core/   — 29 symlinks → ../../src/geox_core/core/ (1 has double-hop)
# /root/GEOX/src/geox_core/core/ — 31 real files (canonical origin)
```

### Live Service
```bash
curl -s http://127.0.0.1:8081/health
# {"status":"healthy","public_tools":32,"version":"v2026.07.06-phase3.1-rsi-pipeline","owner_summary":{"color":"GREEN"}}

curl -s http://127.0.0.1:8081/tools | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['tools']))"
# 32
```

### Vault
```bash
find . -maxdepth 3 -type d -name '*vault*'
# /root/GEOX/999_vault/  (single vault, 8 seal artifacts)
```

### Epistemic Search Patterns
```bash
# Find epistemic labeling enforcement points
grep -r 'truth_class\|epistemic_label\|OBS\|DER\|INT\|SPEC' src/ --include='*.py' | grep -v __pycache__ | grep -v '.pyc'
```

## Discrepancies Found

| Source | Claim | Reality | Severity |
|---|---|---|---|
| README SOT-MANIFEST | public_tools=26 | /health says 32 | 🟡 Medium |
| AGENTS.md | "tools/list ≈ 23" | /tools says 32 | 🟡 Medium |
| AGENTS.md | canonical target 77 | not live | 🟡 Low |
| README SOT-MANIFEST | live_commit=4784103d | git HEAD=5bc66284 | 🟡 Low (stale by ~1) |

## Epistemic Framework Structure

- **7-rung ladder:** SIGNAL(1) → MEASUREMENT(2) → DERIVATION(3) → INTERPRETATION(4) → MODEL(5) → JUDGMENT(6) → NARRATIVE(7)
- **4-class surface:** OBS(1-2) / DER(3) / INT(4-5) / SPEC(6-7)
- **Enforcement:** Gödel Wall (claim must be sealable from lower rungs), Iron Law (lower rung wins contradictions), Beautiful One detection (rhetorical confidence > evidentiary density), Meta-audit (CONSTITUTIONAL/DEVIATION/VIOLATION)
- **Key files:** `src/geox_mcp/epistemic/` (7 modules), `src/geox_core/core/epistemic_integrity.py`, `src/geox_core/assumption_lineage.py`
