# Canonical Determination Pattern — Identical-Content Duplicates

## When to Use

When two skill directories have identical SKILL.md content (differing only in `name:` field) and you need to determine which variant is canonical and which is a rogue copy.

## The Pattern

### Step 1: Quick Content Diff

```bash
diff -q /path/to/FORGE-X/SKILL.md /path/to/x/SKILL.md
```

If only `name:` differs, proceed. If body content differs, you have a genuine divergence — apply semantic overlap detection instead.

### Step 2: Timestamp Comparison

```bash
stat -c '%Y' "/path/to/dupe1/SKILL.md"
stat -c '%Y' "/path/to/dupe2/SKILL.md"
```

- If one timestamp is shared across MANY directories (same second), it was created by a **bulk-copy operation** — that's the rogue set.
- The older, individually-timestamped variant is the original.

### Step 3: Git Provenance (when in a repo)

```bash
git log --oneline --format="%h %ai %an %s" -- skills/FORGE-X/SKILL.md skills/x/SKILL.md
```

- If the bulk-copy commit message mentions a migration, reorg, or zen refresh, that confirms the copy was mechanical.
- Check whether the bulk commit existed before or after the original's last touch.

### Step 4: Sub-File Structure Check (multi-file skills)

```bash
diff -rq /path/to/FORGE-X/ /path/to/x/ --exclude=SKILL.md
```

- If sub-files (references, templates, scripts) are identical, the duplication extends beyond the top-level SKILL.md.
- No output = full structural identity.

### Step 5: ID Field Parity

Read the `id:` field in the YAML frontmatter (if present):

- If both copies share the same `id:` but only `name:` differs, they are **the same skill registered under two directory names**.
- The generic-name entry (no prefix) is the original registration; the prefixed copy is a rogue duplicate.

### Step 6: Follow the Timestamp Chain

When one timestamp value (e.g. `1783879625` = 2026-07-12) appears uniformly across ALL FORGE-* copies and nowhere in the generic-name copies:

```
FORGE-code-wiki:     1783879625
FORGE-docker:        1783879625
FORGE-federation:    1783879625
FORGE-github:        1783879625
...
generic/code-wiki:   1782179870
generic/docker:      1783159796
generic/federation:  1782462855
```

→ Conclusive: the batch timestamp cluster is the rogue set.

## Canonical Verdict

The **generic-name (unprefixed) variant is canonical** when:

1. It is older (individual timestamp predates the bulk copy)
2. The FORGE-/ASI-prefixed variant shares a timestamp with other bulk-copied skills (proving mechanical duplication)
3. Content is byte-identical except for the `name:` field
4. Sub-file structure is identical
5. The `id:` field matches between both copies

The bulk-copied variant should be **removed as a rogue copy** — the generic variant already exists and carries the same content.

## Real-World Calibration

Applied to /root/AAA/skills/ on 2026-07-13:

| Result | Count | Finding |
|--------|-------|---------|
| Pure dupes | 28 pairs | FORGE-* and ASI-* names bulk-copied in a single commit |
| Byte-identical pair | 1 | constitutional-reasoning / ASI-constitutional-reasoning |
| Genuine divergence | 0 | No pair had differing body content |

This pattern was validated on a VPS filesystem (Linux ext4) in mid-2026. Timestamp granularity is seconds; on sub-second copy operations, actual file content diff is the deciding factor.
