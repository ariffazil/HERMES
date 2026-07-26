---
name: aaa-knowledge-files
description: "Create, enrich, or audit structured knowledge domain files in the AAA federation knowledge base (/root/AAA/knowledge/{band}/). OVERLAPS with governance/knowledge-atlas-authoring — that skill is authoritative for Geometry B. This skill covers directory structure, axiom quality rules, and the subagent schema-normalization pitfall but its schema section is historical."
triggers:
  - "create knowledge domain file"
  - "aaa knowledge band"
  - "enrich knowledge files"
  - "knowledge domain schema"
  - "math knowledge file"
  - "physics knowledge file"
  - "code knowledge file"
  - "domain axiom file"
  - "knowledge file validation"
  - "dependency chain knowledge"
---

# AAA Knowledge Domain Files

Create, enrich, or audit structured JSON knowledge domain files under `/root/AAA/knowledge/{band}/` (bands: `math/`, `physics/`, `code/`). Each file represents one domain of knowledge with canonical axioms, reasoning patterns, boundary conditions, and dependency chains.

## Directory Structure

```
/root/AAA/knowledge/
├── README.md
├── math/         # 444-700
│   ├── 444-algebra.json
│   ├── 500-calculus.json
│   ├── ...
│   └── 700-numerical-methods.json
├── physics/      # 000-400
│   ├── 000-foundational-axioms.json
│   ├── 100-classical-mechanics.json
│   └── ...
└── code/         # 777-999
    ├── 777-systems-programming.json
    ├── 800-ai-ml-engineering.json
    └── ...
```

## Canonical Schema

Every knowledge domain file in `/root/AAA/knowledge/` uses this schema (normalized from earlier `code`/`label` variants):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | 3-digit code from 000-999 (e.g., `"444"`) |
| `name` | string | Human-readable title (e.g., `"Algebra"`) |
| `band` | string | Directory name: `"math"`, `"physics"`, or `"code"` |
| `description` | string | 2-4 sentence overview covering scope, applications, and dependency context |
| `axioms` | array | 5+ genuine domain-specific axioms, theorems, or first principles |
| `reasoning_patterns` | array | Characteristic reasoning modes of the domain |
| `boundary_conditions` | object or array | Limits, known impossibilities, or common fallacies |
| `dependencies` | array | List of prerequisite domain IDs (e.g., `["000", "100"]`) |
| `epistemic_floor` | string | Epistemic class: DERIVED, OBSERVED, or INTERPRETED |
| `key_equations` | array (optional) | `[{name, expression, significance}]` |
| `key_references` | array (optional) | Authoritative textbooks and papers |
| `canonical_truths` | array (optional) | Settled knowledge in this domain |

**Schema history:** The files were created by 3 parallel subagents, which produced 3 different schemas. A POST-generation Python script normalized all 33 files to the unified `id`/`name`/`band` schema above. The current schema does NOT use `code`/`label`/`domain`/`question`/`organs`/`reality_layer` — those were from an earlier subagent-pass that was overwritten. Use `knowledge-atlas-authoring` (governance category) for the definitive schema and validation.

## Gold Standard: Physics Band

The physics files at `/root/AAA/knowledge/physics/` are the depth reference. They are ~2,000-2,300 bytes each with:

- **Rich descriptions** that explain the domain's scope and why it matters
- **7+ genuine axioms** that are the real foundational theorems of the domain
- **4-6 reasoning patterns** specific to the domain
- **3-5 boundary conditions** covering real limitations
- **Dependency chains** linking to prerequisite codes
- **Organ assignments** mapping to federation organs (GEOX, WEALTH, A-FORGE)

## Dependency Chain Convention

Codes are not ordered arbitrarily — they encode a prerequisite chain. When creating or updating, ensure:

- **First band (e.g., 000/444):** empty dependencies array (root node)
- **Later codes:** list their direct prerequisite(s) by `"{code}-{domain}"`
- **Last band (e.g., 700):** depends on all prior codes in the chain
- Validate that no circular dependencies exist
- Cross-check: every dependency listed should be resolvable to a real file in the band

Example math chain:
```
444 ← 500 ← 533 ← 555 ← 566
444 ← 600 ← 633
444 ← 650 ← 666 ← 699 ← 700
```

## Axiom Quality Rules

Axioms must be **real** — domain-significant theorems, first principles, or fundamental results. Avoid:

- ❌ **Generic statements** ("Math is rigorous", "Functions can be analyzed")
- ❌ **Trivial definitions** ("A function maps inputs to outputs")
- ❌ **Filler axioms** that wouldn't appear in a textbook
- ✅ **Named theorems** (Cauchy integral formula, Brouwer fixed-point, KKT conditions)
- ✅ **Foundational principles** (Kolmogorov axioms, Church-Turing thesis, P vs NP)
- ✅ **Domain-specific results** (Euler's theorem, handshaking lemma, CFL condition)

## Validation Checklist (Run After Every Create/Update)

**STALE — the validation script below checks for old schema fields (`domain`, `code`, `label`, `question`, `organs`, `reality_layer`). The actual knowledge files now use `id`, `name`, `key_equations`, `key_references`, `canonical_truths`. Use `knowledge-atlas-authoring` (governance category) for correct validation.**

```python
# WARNING: This script checks for the WRONG fields.
# The actual files were normalized from code/label to id/name.
# Do NOT run this against the live knowledge/ directory — it will flag every file.
import json

def validate_band(band_dir):
    """Check all JSON files in a knowledge band directory."""
    import os
    errors = []
    files = sorted(f for f in os.listdir(band_dir) if f.endswith('.json'))
    
    for fname in files:
        path = os.path.join(band_dir, fname)
        try:
            d = json.load(open(path))
        except json.JSONDecodeError as e:
            errors.append(f"{fname}: INVALID JSON — {e}")
            continue
        
        # 1. Required fields
        required = ['domain', 'code', 'band', 'label', 'question', 'description',
                    'axioms', 'reasoning_patterns', 'boundary_conditions',
                    'dependencies', 'organs', 'epistemic_floor', 'reality_layer']
        for field in required:
            if field not in d:
                errors.append(f"{fname}: missing field '{field}'")
        
        # 2. Axiom quality — at least 5
        if len(d.get('axioms', [])) < 5:
            errors.append(f"{fname}: only {len(d.get('axioms', []))} axioms (need ≥5)")
        
        # 3. Reasoning patterns — at least 4
        if len(d.get('reasoning_patterns', [])) < 4:
            errors.append(f"{fname}: only {len(d.get('reasoning_patterns', []))} patterns (need ≥4)")
        
        # 4. Band matches directory
        expected_band = os.path.basename(band_dir)
        if d.get('band') != expected_band:
            errors.append(f"{fname}: band='{d.get('band')}' but dir is '{expected_band}'")
        
        # 5. Code order matches filename
        if fname.startswith(d.get('code', '')):
            pass  # Good
        elif d.get('code', '') in fname:
            pass  # Acceptable — code in filename
        else:
            errors.append(f"{fname}: code='{d.get('code')}' doesn't match filename")
        
        # 6. Dependency resolution
        all_codes = {f.split('-')[0] for f in files}
        for dep in d.get('dependencies', []):
            dep_code = dep.split('-')[0]
            if dep_code not in all_codes:
                errors.append(f"{fname}: dependency '{dep}' not found in band")
        
        # 7. Epistemic floor
        valid_floors = ['OBSERVED', 'DERIVED', 'INTERPRETED', 'SPECULATED']
        if d.get('epistemic_floor') not in valid_floors:
            errors.append(f"{fname}: invalid epistemic_floor '{d.get('epistemic_floor')}'")
    
    return errors

# Example: validate math band
# errors = validate_band('/root/AAA/knowledge/math')
# for e in errors: print(e)
```

## Pitfalls

### 1. Schema Has Been Normalized Away From Subagent Creep

The knowledge files went through THREE schema iterations in one session:
1. `{domain, code, band, label, question, ...}` (physics subagent) 
2. `{domain, code, band, label, ...}` (math subagent)
3. `{id, name, domain, ...}` (code subagent — closest to final)

All 33 were normalized to a unified schema using `{id, name, band, description, axioms, reasoning_patterns, boundary_conditions, dependencies, epistemic_floor, key_equations, key_references, canonical_truths}`. The old fields (`code`, `label`, `question`, `organs`, `reality_layer`) DO NOT EXIST in the current files.

This skill describes the INTERMEDIATE schema (set 1/2 above), not the final normalized schema. See `knowledge-atlas-authoring` for the definitive version.

### 2. Write Reliability on Batch Operations

When writing 5+ files concurrently via `write_file`, some files may silently retain old content. Always verify all files after a batch write — re-read and check for the expected format. Use a format check (`'dependencies' in d` distinguishes new from old) rather than checking file size alone.

### 3. Band Field Must Match Directory

The `band` field is a string like `"math"` — NOT `"444-700"` or any code range. It must exactly match the directory name. This is a common remnant from the old format (the subagents used range strings).

### 4. POST-Generation Normalization Is Required

Parallel subagents WILL produce schema drift. Always budget for a Python normalization pass after parallel creation:

```python
FIXES = {"code": "id", "label": "name", "domain": "name"}
for fpath in glob.glob("knowledge/**/*.json", recursive=True):
    if fpath.endswith("manifest.json"): continue
    d = json.load(open(fpath))
    changed = False
    for old, new in FIXES.items():
        if old in d and old != new:
            if new not in d or d[new] is None:
                d[new] = d[old]
            del d[old]
            changed = True
    if changed:
        json.dump(d, open(fpath, "w"), indent=2)
```

This was validated live: 32 files fixed in one pass, zero data loss.

### 4. Question Field Convention

The `question` field should be a single, high-impact question in plain language with key concept in ALL CAPS:
- ✓ `"What STRUCTURES exist?"` (algebra)
- ✓ `"How do things CHANGE?"` (calculus)
- ✓ `"What can be COMPUTED?"` (computation)
- ✗ `"This domain covers algebraic structures and their properties"` (not a question)

## References

- `references/canonical-schema-template.json` — Complete schema template with annotated fields and validation notes
- `references/physics-reference-notes.md` — Physics band as gold standard: depth benchmarks, axiom density targets
