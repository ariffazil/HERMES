---
name: knowledge-atlas-authoring
description: "Author passive domain knowledge profiles for the arifOS federation — Geometry B. Domain profiles are NOUNS (axioms, constraints, equations), not VERBS (agents, runtimes, MCP tools). Covers the thermodynamic boundary between agent-cards/ and knowledge/, JSON schema for domain profiles, axiom writing standards (genuine, not placeholder), dependency chain management, epistemic tagging, manifest generation, and schema normalization from parallel subagent output. Load when: Arif says 'create knowledge directory', 'domain atlas', '33 knowledge profiles', 'Geometry B', 'knowledge profiles for physics/math/code', 'atlas authoring', or any task touching /root/AAA/knowledge/."
tags:
  - knowledge
  - atlas
  - geometry-b
  - domain-profile
  - passive-knowledge
  - axioms
  - epistemology
  - 33-civilizational
triggers:
  - "knowledge atlas"
  - "Geometry B"
  - "domain knowledge"
  - "33 profiles"
  - "physics math code bands"
  - "domain-atlas"
  - "knowledge profiles"
  - "passive knowledge"
  - "civilizational agents"
  - "axiom authoring"
  - "knowledge/ directory"
  - "what IS what CAN BE what WILL BE"
  - "thermodynamic boundary knowledge"
  - "schema normalization"
---

# Knowledge Atlas Authoring — Geometry B

> **Thermodynamic invariant:** knowledge/ = NOUNS (data, axioms). agent-cards/ = VERBS (agents, runtimes, signatures).
> **Memory aid:** "Agents are verbs (Compute/Execute). The Atlas is a noun (Data/Axioms)."

## The Geometry B Architecture

The CIV-33 domain agents (000–999 across physics/math/code) are **NOT A2A agents**. Treating them as standalone agents is a thermodynamic error (ΔS > 0) — it confuses the *actor* with the *context*.

| Directory | Count | Composition | Function |
|-----------|-------|-------------|----------|
| agent-cards/ | 21 | 9 Structural + 12 Forge | **The Brain & Hands** (Active routing, execution, judgment) |
| knowledge/ | 33 | 11 Physics + 11 Math + 11 Code | **The Library** (Passive axioms, constraints, context) |

### Why Geometry B is Mathematically Sound

1. **Zero Maintenance Overhead:** 0 new Ed25519 signatures, 0 MCP endpoints, 0 runtime loops.
2. **Dynamic Lensing:** When 333-AGI encounters a subsurface problem, it dynamically loads `knowledge/physics/333-geophysics.json`. It inherits the mathematical axioms and boundary conditions of a geophysicist instantly, without the latency of an agent-to-agent handshake.
3. **Strict Cryptographic Boundary:** `agent-cards/` is your tightly controlled, fully verified routing mesh. `knowledge/` is raw, stateless payload. If a knowledge file is corrupted, the system just loads a different perspective; if an agent card is corrupted, the mesh fails.

### Loading Pattern

```
333-AGI encounters subsurface problem
  → loads knowledge/physics/333-geophysics.json
  → inherits wave equation, Archie's laws, basin axioms
  → loads knowledge/math/500-calculus.json for ODE solvers
  → reasons with full epistemic context
  → no A2A handshake, no agent spawning, no crypto overhead
```

## Directory Layout

```
knowledge/
├── manifest.json          ← Master index + dependency graph (auto-generated)
├── README.md              ← Operational documentation
├── physics/               ← What IS (000-400, 11 profiles)
├── math/                  ← What CAN BE (444-700, 11 profiles)
└── code/                  ← What WILL BE (777-999, 11 profiles)
```

## Canonical Profile Schema

Every domain profile MUST follow this exact schema:

```json
{
  "id": "333",
  "name": "Geophysics",
  "band": "physics",
  "description": "One-paragraph summary of what this domain covers and its role in the federation.",
  "axioms": [
    "First principle or fundamental law in this domain (1-2 sentences, genuine physics/domain content)",
    "..."
  ],
  "key_references": [
    "Author, Title",
    "..."
  ],
  "reasoning_patterns": [
    "How this domain reasons about problems (1-2 sentences)",
    "..."
  ],
  "boundary_conditions": [
    "What this domain does NOT cover",
    "..."
  ],
  "connected_domains": ["000", "100", "300"],
  "epistemic_floor": "OBS — observed. DER — derived. INT — interpreted."
}
```

### Key Fields Explained

- **id**: 3-digit code (000-999). Zero-padded string.
- **band**: `physics`, `math`, or `code`.
- **name**: Human-readable domain name (e.g., "Thermodynamics", not "133").
- **axioms**: Array of genuine first-principles statements. These must be REAL — not placeholder filler. Each axiom should be factually correct for the domain. Examples:
  - Physics: The Second Law, Newton's Laws, Snell's Law, Archie's equations
  - Math: Euler's theorem, Fundamental Theorem of Calculus, Bayes' theorem
  - Code: Amdahl's Law, CAP theorem, Church-Turing thesis
- **connected_domains**: Array of domain IDs this profile depends on. Forms an acyclic dependency graph for load ordering.
- **boundary_conditions**: Honest limits of the domain — what it does NOT cover. Prevents reasoning errors from overreach.
- **epistemic_floor**: Per F2 — label whether the axioms in this domain are OBS (observationally anchored), DER (derived from axioms), or INT (interpreted frameworks).

## Axiom Writing Standards

Each profile must carry genuine axioms that someone in the field would recognise. DO NOT write filler:

```
GOOD (Thermodynamics):
  "The Second Law: entropy of an isolated system never decreases over time"
  "Zeroth Law: transitive thermal equilibrium — if A=C and B=C then A=B"
  "Boltzmann entropy: S = k_B · ln(Ω)"

BAD (Thermodynamics):
  "Thermodynamics studies heat"           ← vacuous, tells nothing
  "Temperature is a fundamental concept"  ← true but useless as axiom
  "Energy can be transformed"             ← too generic, not domain-specific
```

**Rule of thumb:** Each axiom should be something a university student in that field would memorise as foundational. If it wouldn't be on a midterm, it's not an axiom.

### Axiom Anti-Patterns

These are traps that waste context budget and reduce atlas quality:

| Anti-pattern | Example | Why it's wrong |
|---|---|---|
| **Generic statement** | "Math is rigorous" | True but tells nothing domain-specific |
| **Trivial definition** | "A function maps inputs to outputs" | Wouldn't appear in a textbook |
| **Filler axiom** | "Energy can be transformed" | Too generic, not domain-specific |
| **Circular definition** | "Optimization finds optimal solutions" | Defines nothing |
| **Empty citation** | "This is a well-known principle" | Either state the principle or don't

## Dependency Chain

The domains form a directed acyclic dependency graph. Load order matters:

```
PHYSICS:
  000 (Foundational Axioms) → 100 (Classical Mechanics) → 133 (Thermodynamics)
                                                       → 200 (Electromagnetism) → 233 (Quantum Mechanics) → 266 (Particle Physics)
                                                                                → 300 (Relativity)
  133 → 333 (Geophysics)
  300 → 333, 366 (Astrophysics)
  266 → 366, 399 (Condensed Matter) → 400 (Nuclear Physics)

MATH:
  444 (Algebra) → 500 (Calculus) → 533 (Analysis)
                                 → 555 (Topology)
                                 → 566 (Linear Algebra)
  444 → 600 (Probability) → 633 (Statistics)
  444 → 650 (Discrete Math) → 666 (Computation) → 699 (Optimization) → 700 (Numerical Methods)

CODE:
  777 (Systems Programming) → 800 (AI/ML) → 833 (Security)
                                          → 850 (Data) → 888 (Governance)
  777 → 900 (Frontend) → 920 (Backend) → 933 (DevOps) → 950 (Integration) → 977 (Automation) → 999 (Meta-Code)
```

Cross-band dependencies are allowed (e.g., geophysics depends on calculus). Record them in `connected_domains`.

## Manifest Generation

The `knowledge/manifest.json` is the master index. Generate it after creating all profiles:

```python
import json, os, glob

MANIFEST = {
    "manifest_version": "1.0",
    "protocol": "Knowledge Atlas — Geometry B",
    "total_profiles": 0,
    "bands": {
        "physics": {"count": 0, "range": "000–400", "path": "physics/"},
        "math": {"count": 0, "range": "444–700", "path": "math/"},
        "code": {"count": 0, "range": "777–999", "path": "code/"},
    },
    "dependency_chain": {},
    "epistemic_invariant": "Knowledge profiles are OBS/DER/INT. No executable code.",
    "generated_at": None,
}

for fpath in sorted(glob.glob("knowledge/**/*.json", recursive=True)):
    if fpath.endswith("manifest.json"):
        continue
    d = json.load(open(fpath))
    eid = d["id"]
    band = d["band"]
    MANIFEST["dependency_chain"][eid] = {
        "name": d["name"],
        "children": d.get("connected_domains", []),
    }
    MANIFEST["bands"][band]["count"] += 1
    MANIFEST["total_profiles"] += 1
```

## Parallel Subagent Authoring (with Schema Normalization)

When creating 33 profiles across 3 bands, use parallel subagents (1 per band) to maximise throughput. **CRITICAL: enforce a strict schema contract before spawning.**

### Schema Normalization Pitfall

Subagents will drift from the schema if not pinned. In the first pass, 3 parallel subagents produced 3 different schemas:
- Agent A used `{id, name, domain}` (correct)
- Agent B used `{code, label, band}` (mapped code→id, label→name)
- Agent C used `{code, domain, label}` (different mapping)

This creates 3 concurrent-but-incompatible formats. Fix with POST-generation normalization:

```python
FIXES = {"code": "id", "label": "name", "domain": "name"}

for fpath in glob.glob("knowledge/**/*.json", recursive=True):
    if fpath.endswith("manifest.json"):
        continue
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

**Prevention:** When spawning subagents for profile creation, include the EXACT JSON schema in the task prompt (copy-paste the schema block above). Show an example. State: "Every file MUST have `id`, `name`, `band` as strings — NOT `code`, `label`, or `domain`."

### Batch Script for Bulk Creation

If creating profiles from scratch, use this pattern in each subagent's prompt:

```
Create 11 JSON domain profile files under /root/AAA/knowledge/{band}/.
Each file follows this exact schema: [include schema JSON block].
Each axiom must be genuine domain knowledge — not placeholder filler.
Dependency IDs: [list specific IDs for this band].
File naming: {id}-{kebab-name}.json
```

## Pitfalls

- **Write reliability on batch operations.** When writing 5+ files concurrently via `write_file`, some files may silently retain old content. Always VERIFY all files after a batch write — re-read and check for the expected format (e.g., assert `'axioms' in d` to distinguish new from old). Do NOT rely on file size alone. This was validated: 32/33 files written correctly, 1 silently stale.
- **Do NOT create A2A agent cards for domain profiles.** The 33 profiles are passive knowledge, not agents. No Ed25519 keys, no MCP endpoints, no runtime loops, no A2A discovery entries.
- **Do NOT use placeholder axioms.** Vague statements like "this domain studies X" are not axioms. Each axiom must be a genuine first-principles statement that a practitioner would recognise. Real filler kills the atlas' value.
- **Schema drift between parallel subagents is inevitable.** Budget for a normalization pass after parallel creation. Do NOT assume all agents follow the schema perfectly.
- **Dependency graph must be acyclic.** Physics→Math cross-dependencies are fine (geophysics→calculus). But if domain A depends on B and B depends on A, the loading logic loops. Validate before finalising the manifest.
- **Boundary conditions are not optional.** Every profile must state what it does NOT cover. This prevents 333-AGI from applying geophysics axioms to nuclear physics or vice versa.
- **Manifest must be regenerated when profiles change.** The dependency chain and count in manifest.json must reflect the current file set. Stale manifest = stale loading logic.

## Verification Check

After creating the atlas:

```bash
# Check all 33 profiles exist
find knowledge/ -name '*.json' -not -name 'manifest.json' | wc -l
# Should be 33

# Check no schema drift — every profile has id, name, band
python3 -c "
import json, glob
errors = []
for f in glob.glob('knowledge/**/*.json', recursive=True):
    if f.endswith('manifest.json'): continue
    d = json.load(open(f))
    for key in ['id','name','band']:
        if key not in d:
            errors.append(f'{f} missing {key}')
for e in errors: print(f'  ERROR: {e}')
if not errors: print('All 33 profiles schema-valid')
"

# Check dependency graph completeness
python3 -c "
import json
m = json.load(open('knowledge/manifest.json'))
chain = m.get('dependency_chain', {})
orphans = set(chain.keys())
for k, v in chain.items():
    for c in v.get('children', []):
        orphans.discard(c)
orphans -= {'000', '444', '777'}  # root nodes
if orphans:
    print(f'Orphan deps: {orphans}')
else:
    print('Dependency graph valid')
"
```

Always verify after creation. Geometry B is only useful if every profile is loadable.
