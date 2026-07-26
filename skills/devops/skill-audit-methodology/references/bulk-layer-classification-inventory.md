# Bulk Layer Classification & Cross-Repo Skill Inventory

**Proven against:** 233 SKILL.md files in `/root/HERMES/skills/` vs 167 in `/root/AAA/skills/`
**Date:** 2026-07-26
**Method:** Python YAML frontmatter extraction + content-based layer classification + cross-repo comparison + semantic AAA prefix mapping

---

## Use Case

You need to:
- Classify every skill in a large library into **substrate / knowledge / domain** layers (per AAA canonical taxonomy)
- Produce both machine-readable JSON and human-readable markdown inventory
- Compare a HERMES-scope inventory against the AAA canonical inventory
- Detect symlinks, layer mismatches, and skills unique to one scope
- **Map skills from one naming convention (flat names) to the AAA prefix taxonomy** (AGI-/ASI-/APEX-/FORGE-/KERNEL-/AUDIT-/FLAME-/WELL-/WEALTH-)

---

## Step-by-Step Protocol

### Phase 1 — Discover All SKILL.md Files

```bash
# Find every SKILL.md, excluding archives
find /path/to/skills/ -name "SKILL.md" ! -path "*/.archive*" ! -path "*/.curator*" | sort
```

### Phase 2 — Extract YAML Frontmatter

Parse SKILL.md files to extract structured data. The canonical frontmatter regex:

```python
import re, yaml

def extract_frontmatter(filepath):
    with open(filepath) as f:
        content = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {"error": "No frontmatter"}
    data = yaml.safe_load(m.group(1)) or {}
    data["_file"] = filepath
    return data
```

Collect these fields per skill:
| Field | Source | Purpose |
|-------|--------|---------|
| `id` | frontmatter `id:` or dirname | Unique identifier |
| `name` | frontmatter `name:` | Display name |
| `purpose` / `description` | frontmatter | What the skill does |
| `tags` | frontmatter `tags:` | Governance / domain tags |
| `triggers` | frontmatter `triggers:` | When to load |
| `_path` | computed | Relative path from skills root |
| `_category` | parent dir (if any) | e.g., devops, governance, creative |

### Phase 3 — Layer Classification

Classify every skill into one of three layers based on content analysis:

#### Substrate (foundational infrastructure)
Skills about governance, kernel, binding, dispatch, verification, crypto identity, floors, execution engines, observability, routing.

**Keywords to look for** (in description, tags, triggers, path, category):
`governance`, `constitutional`, `substrate`, `kernel`, `binding`, `observe`, `route`, `dispatch`,
`verify`, `gate`, `memory`, `floor`, `f13`, `sovereign`, `apex`, `seal`, `audit`,
`enforcement`, `execution engine`, `Gödel`, `ed25519`, `identity propagation`

Also scan for:
- Devops skills that operate on arifOS internals (floor modification, interceptor patching, identity propagation, provider routing, vault chain governance)
- Empty/null category skills about kernel audit, substrate test, meta-mesa, wisdom-scar
- Any skill whose path contains "substrate"

#### Knowledge (reference & retrieval)
Skills providing domain knowledge, research infrastructure, reference material, or structured information retrieval.

**Keywords:**
`knowledge`, `know-`, `atlas`, `research`, `arxiv`, `deep-research`, `wiki`, `blog`,
`polymarket`, `llm-wiki`, `summarize`, `code-analysis`

Also scan for:
- Categories: email, note-taking, research
- Skills whose primary purpose is information retrieval rather than action

#### Domain (everything else)
Skills that produce domain-specific outputs or operate within a bounded context.

Categories that are always domain:
`creative`, `devops` (most), `trading`, `media`, `social-media`, `business`, `legal`,
`geology`, `productivity`, `software-development`

**Heuristic cascade** (proven working order):
```python
def classify_layer(skill_data):
    all_text = f"{name} {description} {category} {tags} {triggers} {path}".lower()
    
    # Step 1: Governance skills that are substrate-level (floors, crypto, execution engines)
    if governance_keywords_match and substrate_keywords_match:
        return 'substrate'
    
    # Step 2: Explicit substrate designation in path
    if 'substrate' in path:
        return 'substrate'
    
    # Step 3: Domain-specific checks (trading, creative, devops ops, etc.)
    if domain_keywords_match:
        return 'domain'
    
    # Step 4: Knowledge checks
    if knowledge_keywords_match:
        return 'knowledge'
    
    # Step 5: Substrate fallback
    if any(k in all_text for k in substrate_keywords):
        return 'substrate'
    
    # Step 6: Default by category
    cat_to_layer = {
        'governance': 'domain', 'research': 'knowledge', 'note-taking': 'knowledge',
        None: 'domain',  # uncategorized defaults to domain
    }
    return cat_to_layer.get(category, 'domain')
```

### Phase 4 — Cross-Repo Comparison

When comparing two skill catalogs (e.g., HERMES skills vs AAA skills):

```python
# 1. Scan both directories independently
hermes = scan_directory("/root/HERMES/skills/")
aaa    = scan_directory("/root/AAA/skills/")

# 2. Build a map by skill path
hermes_by_path = {s['_path']: s for s in hermes}
aaa_by_name = {Path(s['_path']).name: s for s in aaa}

# 3. Detect symlinks from AAA → HERMES
for link_name in os.listdir(aaa_dir):
    target = os.readlink(os.path.join(aaa_dir, link_name))
    if target.startswith("/root/HERMES"):
        print(f"SYMLINK: {link_name} → {target}")

# 4. Detect layer mismatches
for h_path, h_item in hermes_by_path.items():
    skill_name = Path(h_path).name
    if skill_name in aaa_by_name:
        aaa_layer = aaa_by_name[skill_name].get('aaa_layer', 'unknown')
        if aaa_layer != h_item['layer']:
            print(f"MISMATCH: {skill_name} → HERMES:{h_item['layer']} vs AAA:{aaa_layer}")

# 5. Find AAA-only skills (not in HERMES)
aaa_only = set(aaa_by_name.keys()) - {Path(p).name for p in hermes_by_path}
```

### Phase 5 — Semantic AAA Prefix Mapping

When mapping HERMES flat names to the AAA prefix taxonomy (AGI-/ASI-/APEX-/FORGE-/KERNEL-/AUDIT-/FLAME-/WELL-/WEALTH-), use function-based rules:

```python
def map_to_aaa_prefix(skill_data):
    """Map a HERMES skill to its AAA prefix based on function."""
    path = skill_data.get('_path', '')
    name = skill_data.get('name', '')
    category = skill_data.get('_category', '')
    tags = skill_data.get('tags', [])
    all_text = f"{path} {name} {category} {' '.join(tags)}".lower()
    
    # Rule: FLAME → flame-free-loop skills
    if 'flame-free-loop' in all_text:
        return 'FLAME'
    
    # Rule: KERNEL → arifOS kernel skills
    if any(k in path for k in ['arifos-kernel', 'arifos-auto-init', 'arifos-external-council',
                                'arifos-organ-forging', 'arifos-runtime-module', 'ariflow-component']):
        return 'KERNEL'
    
    # Rule: WELL → human wellness  
    if any(k in path for k in ['hospital-patient', 'medical-document']):
        return 'WELL'
    
    # Rule: WEALTH → trading/finance/sales
    if any(k in path for k in ['trading/', 'business/', 'receipt-', 'vendor-receipt']):
        return 'WEALTH'
    if any(k in name for k in ['nasi-lemak', 'trading', 'signal-briefing', 'xauusd']):
        return 'WEALTH'
    
    # Rule: AUDIT → SOT/inventory/knowledge governance
    if any(k in name for k in ['sot-inventory', 'aaa-knowledge', 'governed-knowledge',
                                'external-technology-evaluation', 'geological-artifact']):
        return 'AUDIT'
    
    # Rule: APEX → verification/truth gates
    if any(k in name for k in ['apex-', 'spec-audit', 'deployment-claim', 'live-probe',
                                'paper-to-code', 'submission-readiness', 'deep-codebase-audit',
                                'external-artifact', 'geox-comparative', 'site-deployment',
                                'parallel-forge-history', 'runtime-truth', 'federation-tri-team']):
        return 'APEX'
    
    # Rule: ASI → agent governance
    if any(k in path for k in ['governance/']) and not any(k in path for k in ['geox', 'forge-visual',
                                'explore-before', 'evidence-before', 'knowledge-atlas', 'eureka',
                                'akal', 'atlas333', 'negative-space', 'j-collapse', 'sovereign-conversation',
                                'human-envelope', 'uncertainty', 'external-wisdom', 'ai-cognitive',
                                'seven-zen']):
        return 'ASI'
    if any(k in name for k in ['agent-', 'three-agent', 'f13-', 'governed-', 'somatic-',
                                'institutional-', 'temporal-', 'bloodhound', 'meta-mesa',
                                'meta-cognitive', 'hermes-naked', 'skill-substrate',
                                'wisdom-scar', 'sovereign-sexuality', 'apa-sovereign',
                                'human-sovereignty', 'external-analysis', 'governance-']):
        return 'ASI'
    
    # Rule: AGI → cognition/research/creative/media
    if any(k in path for k in ['research/', 'creative/', 'media/']):
        return 'AGI'
    if any(k in name for k in ['cognitive-', 'deep-research', 'consult-external', 'akal-',
                                'arxiv', 'blogwatcher', 'polymarket', 'llm-wiki',
                                'summarize', 'code-analysis', 'text-forensics',
                                'explore-before', 'evidence-before', 'knowledge-atlas',
                                'eureka', 'negative-space', 'j-collapse', 'sovereign-conversation',
                                'human-envelope', 'uncertainty', 'atlas333', 'seven-zen',
                                'ai-cognitive', 'human-intelligence', 'person-dossier',
                                'person-intelligence', 'legal-case', 'petronas', 'whatsapp',
                                'institutional-forensic', 'institutional-case', 'witness-companion',
                                'vendor-partner', 'human-voice', 'humanizer', 'songwriting',
                                'ai-model-intelligence']):
        return 'AGI'
    
    # Default: FORGE (infrastructure)
    return 'FORGE'
```

### Phase 6 — Output Production

Generate two complementary outputs:

**Machine-readable (JSON):**
```json
{
  "report_metadata": { "source_dir": "...", "total_skills": 233 },
  "layer_summary": { "substrate": 43, "knowledge": 12, "domain": 178 },
  "aaa_prefix_summary": { "AGI": 70, "ASI": 35, "APEX": 13, "FORGE": 70, "KERNEL": 6, "AUDIT": 6, "FLAME": 2, "WELL": 2, "WEALTH": 14 },
  "category_summary": { "devops": 54, "governance": 37, "creative": 29, ... }
}
```

**Human-readable (markdown):**
- Summary table with layer counts
- Full substrate listing with governance tags
- Knowledge listing with AAA symlink annotations
- AAA prefix mapping (3 lists: mapped, HERMES-only, AAA-missing)
- Domain listing by category

## Pitfalls

- **Category directories have no SKILL.md themselves** — e.g., `/root/HERMES/skills/creative/` has no SKILL.md, but its subdirectories like `/creative/ascii-art/SKILL.md` do. Always use `find` recursion, not `ls`.
- **`yaml.safe_load()` handles `null` gracefully** — empty frontmatter blocks return `None`, not failure. Guard with `or {}`.
- **AAA skills dir has a flat mix:** symlinks (pointing to HERMES), substrate/knowledge taxonomy dirs, AND flat prefixed skills (AGI-*, ASI-*, APEX-*, FORGE-*, AUDIT-*). The prefixed skills are AAA-only — they come from OpenCode/Kimi Code scopes, not from HERMES.
- **Description field may be `purpose` or `description`** — check both keys in the YAML. The frontmatter is inconsistent across skills.
- **Tags/triggers may be a string (not a list)** — always normalize: `tags if isinstance(tags, list) else [tags] if tags else []`.
- **Symlinks from AAA to HERMES are directional** — they exist in AAA pointing TO HERMES, not the reverse. Don't double-count.
- **AAA-only skills lack a canonical layer** — they don't live under substrate/knowledge/domain subdirs, so they have no AAA-layer tag. Classify them using the same heuristic as HERMES skills.
- **Semantic prefix mapping is NOT string matching.** A skill sitting in `devops/` about arifOS governance infrastructure gets FORGE- (it's infra ops), not ASI- (which would be governance theory). Always classify by function, not by directory name.
- **Nasi-lemak is WEALTH, not BUSINESS.** Despite living under `business/` or `trading/` categories, all sales tracking receipts are financial → WEALTH-.
- **Apple/platform-ecosystem skills have no AAA equivalent.** `apple-notes`, `apple-reminders`, `findmy`, `imessage` are HERMES-only.
- **Hardcoded port references or agent counts** in README files are often stale. Never trust documentation claims without live endpoint verification.

## Related Reference

→ `references/hermes-aaa-prefix-mapping-2026-07-26.md` — Complete 227-entry mapping table with priority-ranked gap analysis.
