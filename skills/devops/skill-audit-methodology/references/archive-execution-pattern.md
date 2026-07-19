# Skill Archive Execution Pattern

**Provenance:** EUREKA ZEN operation 2026-07-13 — 29 skills archived, 2 Hermes engine variants enhanced, 1 skill forged, 73 gaps documented.

## When to Use

After running the skill audit (Loop 1-3 of the audit methodology), when acting on the findings:
- Duplicates found → archive the obsolete copy
- Engine variants found → align to native cognitive architecture
- Agent-card referenced skills missing on disk → forge or document as gap

## Step 1: Content Diff Verification

Before archiving any skill, verify it's an exact content duplicate:

```bash
# FORGE-* vs generic pair
diff <(head -5 AAA/skills/FORGE-<name>/SKILL.md) <(head -5 AAA/skills/<name>/SKILL.md)
# If only `name:` field differs → safe to archive (identical content)
```

**Acceptable differences:** Only the `name:` YAML frontmatter field. Everything else identical.

## Step 2: Agent-Card Cross-Reference

Verify the skill being archived is NOT referenced in any agent card:

```python
import json, glob

# Get all skill IDs from agent cards
agent_skills = set()
for f in glob.glob('/root/AAA/agents/**/agent-card.json', recursive=True):
    d = json.load(open(f))
    for s in d.get('skills', []):
        sid = s.get('id', '') if isinstance(s, dict) else str(s)
        agent_skills.add(sid)

# Check if target is referenced
target = '<skill-name>'
if target in agent_skills:
    print(f"⛔ CANNOT ARCHIVE — {target} referenced in agent cards")
else:
    print(f"✅ Safe to archive — {target} not referenced")
```

## Step 3: Move to ARCHIVE-* Prefix

```bash
cd /root/AAA/skills
mv -v <generic-name> ARCHIVE-<generic-name>
```

**Convention:** `ARCHIVE-<original-name>` — the ARCHIVE- prefix at top level preserves visibility while clearly marking as deprecated.

## Step 4: Update SKILL_ALIAS_TABLE

Add tombstone entries for archived skills:

```python
import json

with open('/root/AAA/skills/SKILL_ALIAS_TABLE.json', 'r') as f:
    table = json.load(f)

archived = ['skill-name-1', 'skill-name-2']
canonical_map = {'skill-name-1': 'FORGE-skill-name-1'}

for name in archived:
    canonical = canonical_map.get(name, f'ARCHIVE-{name}')
    new_alias = {
        "v3_name": name,
        "layer": "domain",
        "primary_disk_name": f"ARCHIVE-{name}",
        "primary_path": f"/root/AAA/skills/ARCHIVE-{name}",
        "primary_resolved": f"/root/AAA/skills/{canonical}",
        "primary_home": "aaa",
        "status": "TOMBSTONE",
        "tombstone": True,
        "restored_live": False,
        "superseded_by": canonical
    }
    table['aliases'].append(new_alias)

table['tombstone_count'] = len([a for a in table['aliases'] if a.get('tombstone')])

with open('/root/AAA/skills/SKILL_ALIAS_TABLE.json', 'w') as f:
    json.dump(table, f, indent=2)
```

## Step 5: Triple-Copy Sync

The SKILL_ALIAS_TABLE exists in 3 locations — sync all:

```bash
cp /root/AAA/skills/SKILL_ALIAS_TABLE.json /root/AAA/skills/AGI-skill-unification/SKILL_ALIAS_TABLE.json
cp /root/AAA/skills/SKILL_ALIAS_TABLE.json /root/AAA/skills/skill-unification/SKILL_ALIAS_TABLE.json
```

## Step 6: Engine Variant Alignment Pattern

For skills with engine-specific subdirectories (claude/, hermes/, kimi/, opencode/):

### 6a — Identify Variants
```bash
find /root/AAA/skills/<skill-name>/ -name "SKILL.md"
```

### 6b — Read Canonical + Claude Variant
The Claude variant is typically the most complete (XML-tag structured, detailed YAML frontmatter). Read it to understand the full pattern.

### 6c — Enhance Hermes Variant
Hermes variants should add:
- **RASA tone**: BM casual + English technical mix
- **Creative media routing**: image_generate, TTS, artifact courier hooks
- **Conversational flow**: Direct address to Arif, one-line headline first
- **F9/F10 boundaries**: No consciousness claims, no identity labels

```markdown
## Hermes-Specific Execution

### 1. [Task] → Human Delivery
```
[HEADLINE] — one-line BM
→ Specific steps in English if technical
→ Media routing: [image/audio/document] if applicable
```

### 2. Language Gate
- BM casual with Arif in DM
- English for technical receipts
- Mix when natural

### 3. Invocation
```
Route to canonical: skills/<canonical>/SKILL.md
Hermes adapter: skills/<canonical>/hermes/SKILL.md
```
```

## Step 7: Gap Analysis via Agent-Card Cross-Reference

Find skills referenced in agent cards but missing from disk:

```python
# agent_skills set from Step 2 above
def get_skill_dirs(base):
    import os
    dirs = set()
    for d in os.listdir(base):
        full = os.path.join(base, d)
        if os.path.isdir(full) and not d.startswith(('.', 'ARCHIVE-', 'knowledge', 'substrate')):
            dirs.add(d)
    return dirs

aaa_dirs = get_skill_dirs('/root/AAA/skills')
agents_dirs = get_skill_dirs('/root/.agents/skills')
all_disk = aaa_dirs | agents_dirs

# Per-lane gap analysis
for f in glob.glob('/root/AAA/agents/_lanes/*/agent-card.json'):
    lane = f.split('/')[-2]
    d = json.load(open(f))
    skills = [s.get('id','') if isinstance(s,dict) else str(s) for s in d.get('skills',[])]
    missing = [s for s in skills if s not in all_disk]
    print(f"{lane}: {len(missing)} missing — {', '.join(missing)}")
```

## Step 8: Final Gauge Verification

After all operations, verify state:

```bash
python3 -c "
import os
d = '/root/AAA/skills'
aaa = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d,x))]
live = [x for x in aaa if not x.startswith('.') and not x.startswith('ARCHIVE-')]
arch = [x for x in aaa if x.startswith('ARCHIVE-')]
dot = [x for x in aaa if x.startswith('.archive')]
print(f'Live: {len(live)}')
print(f'ARCHIVE-*: {len(arch)}')
print(f'.archive-*: {len(dot)}')
import json
t = json.load(open(os.path.join(d,'SKILL_ALIAS_TABLE.json')))
print(f'Aliases: {len(t[\"aliases\"])}')
print(f'Tombstones: {sum(1 for a in t[\"aliases\"] if a.get(\"tombstone\"))}')
"
```

## Step 9: Manifest Production

Write a comprehensive manifest covering all phases:
1. Archived skills (from → to mapping)
2. Aligned engine variants (what changed)
3. Forged skills (path, purpose, dependencies)
4. Remaining gaps (for future sessions)
5. State gauge comparison (before/after)
6. Seal proposal reference

---

*DITEMPA BUKAN DIBERI — arifOS Federation*
