# Cross-Directory Skill Consolidation

> Pattern for merging overlapping skill libraries into a single canonical source.

## Problem

Multiple skill directories exist with overlapping content:
- `~/.hermes/skills/` — Hermes agent skills
- `/root/AAA/skills/` — AAA canonical library
- `/root/.agents/skills/` — OpenCode agent skills

Each grows independently. Over time, the same skill exists in multiple places with diverged content.

## Detection

```bash
# Extract skill names from each library
find ~/.hermes/skills/ -name "SKILL.md" -not -path "*/.archive*" -exec dirname {} \; | xargs -I{} basename {} | sort > /tmp/hermes_skills.txt
find /root/AAA/skills/ -name "SKILL.md" -exec dirname {} \; | xargs -I{} basename {} | sort > /tmp/aaa_skills.txt
find /root/.agents/skills/ -name "SKILL.md" -exec dirname {} \; | xargs -I{} basename {} | sort > /tmp/agents_skills.txt

# Find overlaps
comm -12 /tmp/aaa_skills.txt /tmp/agents_skills.txt  # shared between AAA and .agents
comm -23 /tmp/agents_skills.txt /tmp/aaa_skills.txt  # unique to .agents
```

## Consolidation Steps

### 1. Identify identical copies (md5sum)
```bash
for skill in $(comm -12 /tmp/aaa_skills.txt /tmp/agents_skills.txt); do
  a=$(md5sum /root/AAA/skills/$skill/SKILL.md 2>/dev/null | cut -d' ' -f1)
  b=$(md5sum /root/.agents/skills/$skill/SKILL.md 2>/dev/null | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then echo "SAME: $skill"; else echo "DIFF: $skill"; fi
done
```

### 2. Symlink unique skills into canonical library
```bash
# Skills that exist only in .agents but not AAA → symlink into AAA
for skill in $(comm -23 /tmp/agents_skills.txt /tmp/aaa_skills.txt); do
  ln -sf "/root/.agents/skills/$skill" "/root/AAA/skills/$skill"
done
```

### 3. Reconcile diverged copies
For skills that exist in both but have different content:
- Determine which is the working copy (used by active agents)
- Backup the canonical version: `mv /root/AAA/skills/$skill /root/AAA/skills/${skill}.aaa-backup`
- Symlink to the working copy: `ln -sf /root/.agents/skills/$skill /root/AAA/skills/$skill`

### 4. Verify
```bash
# Count symlinks in AAA (should match consolidation count)
find /root/AAA/skills/ -maxdepth 1 -type l | wc -l
```

## Result Shape

After consolidation:
- AAA becomes the single canonical library (largest, most complete)
- .agents remains the working copy for OpenCode
- Symlinks from AAA → .agents keep both in sync
- `.aaa-backup` files preserve the original AAA versions

## Proven 2026-07-16

- 81 .agents skills symlinked into AAA (63 unique + 18 reconciled)
- 10 diverged AAA originals backed up as .aaa-backup
- AAA grew from 139 to 220 top-level directories
- Zero breakage — symlinks resolved correctly for all agents

## Pitfalls

- **Don't blindly symlink without checking divergence.** Two skills with the same name may have different content because they evolved independently. Always md5sum first.
- **Don't delete originals.** Always backup as `.aaa-backup` before symlinking. The backup is the rollback path.
- **Hermes skills are independent.** Hermes (~/.hermes/skills/) has its own library with minimal overlap with AAA/.agents. Don't force consolidation where there's no overlap.
- **OpenClaw phantom skills.** Skills listed in openclaw.json may not exist as actual directories. Verify with `ls ~/.openclaw/plugin-skills/` before treating them as real.
