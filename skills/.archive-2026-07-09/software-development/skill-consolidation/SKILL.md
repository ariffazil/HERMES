---
name: skill-consolidation
description: Use when consolidating multiple narrow skill fragments into a single class-level umbrella skill. Extracts unique knowledge per fragment, produces a §PROVENANCE table, and merges into one cohesive SKILL.md under word limits. Also use when asked to "extract core knowledge from N fragments" or "produce consolidated skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, consolidation, authoring, merge, provenance]
    related_skills: [hermes-agent-skill-authoring, skills-library-dimensional-audit]
---

# Skill Consolidation from Fragments

## Overview

When multiple narrow, overlapping fragments (one-session-one-skill or single-organ-concept skills) exist and should become a single class-level umbrella skill, use this pattern. The goal is to extract what each fragment uniquely knows and merge it into one cohesive deliverable — not to concatenate them.

**Example trigger:** "Extract core knowledge from 5 federation + 10 ZEN fragments and produce two consolidated skills."

## When to Use

- Multiple narrow skills/fragments overlapping the same domain
- User asks to "extract core knowledge from N fragments"
- User asks to "produce consolidated skills" or "merge skills"
- Curator review finds many single-concept skills that should be one umbrella

**Don't use for:** genuinely different domains (keep them separate), a single fragment (nothing to consolidate), or fragments that are already class-level umbrellas.

## The Consolidation Pattern

### Step 1: Read All Source Fragments in Parallel

Load every SKILL.md in scope. Batch independent reads. For 15 fragments, expect 2-3 rounds of parallel reads.

**Completion criterion:** All fragments read and understood.

### Step 2: Extract Unique Contributions Per Fragment

For each fragment, identify the one thing it knows that the others don't. Skip duplicated bodies. Focus on:
- Field-level enforcement rules
- Concrete failure signals
- Exact formats (receipts, JSON schemas, error codes)
- Metrics and measurements
- Pitfalls the other fragments don't mention

**Completion criterion:** A one-line "unique contribution" identified for every fragment. If a fragment brings nothing unique, note it as "absorbed, nothing unique."

### Step 3: Produce a §PROVENANCE Table

```markdown
## §PROVENANCE

| Fragment | Version | Unique Contribution |
|----------|---------|---------------------|
| `fragment-name` | 1.0.0-2026.01.01 | One-line description of what this uniquely contributed |

**Forged:** YYYY-MM-DD | **Consolidation:** <agent/process> | **Predecessors absorbed:** <list or "none">
```

This table goes in the target skill body after the Overview. It serves as a map for future curators — without it, fragments left on disk look like they contain unabsorbed knowledge.

### Step 4: Merge Into One Cohesive SKILL.md

Use the richest fragment as structural base. Inject unique field-level detail from the others. Drop duplicated body content. Preserve concrete formats (receipts, exact commands, error tables) — don't abstract them away.

**Target shape:** class-level, rich SKILL.md with `references/` directory for bulky session-specific detail.

**Completion criterion:** All unique contributions from the §PROVENANCE table are present in the merged file. No duplicated content.

### Step 5: Write the Deliverable

- If the target skill file already exists: `patch` it
- If not: `write_file` from scratch
- Output path depends on context: plans go to `/root/.hermes/plans/`, skills go to the skills tree
- Verify word count — aim for 2,000–4,000 words for a consolidated class-level skill

**Completion criterion:** File written, word count verified, frontmatter valid.

### Step 6: Verify

- [ ] Both target files exist and are non-empty
- [ ] Both under 4,000 words
- [ ] YAML frontmatter valid (starts with `---`, has `name` + `description`)
- [ ] §PROVENANCE table present in each, listing every source fragment
- [ ] No duplicated content within or across files
- [ ] Trigger phrases and floor scopes declared

## Word Budget Rules

- Class-level consolidated skill: **2,000–4,000 words**
- If source material exceeds this: push bulk reference to `references/` files
- If genuinely different domains: split into separate skills, don't force one file

## When NOT to Consolidate

- Fragments cover genuinely different domains (e.g., observability vs naming doctrine) — keep them separate
- The merged skill would exceed 4,000 words without being compressible — split into SKILL.md + `references/` support files
- Only one fragment exists — no consolidation needed
- Fragments are already class-level umbrellas — they're the target shape, not the source material

## Common Pitfalls

1. **Duplicating content across the merge.** The §PROVENANCE table forces the question: what unique thing did each fragment bring? If a fragment brought nothing unique, it's absorbed, not merged.

2. **Losing field-level detail.** Class-level skills can become too abstract. Inject concrete failure signals, receipt formats, and exact commands from the source fragments — don't just summarize.

3. **Omitting the §PROVENANCE table.** Without it, future curators can't trace what was absorbed, and fragments left on disk look like they contain unabsorbed knowledge.

4. **Concatenating instead of consolidating.** A merge is not a concatenation. If two fragments describe the same concept, keep the better version and drop the other. The §PROVENANCE table records the contribution, not the full text.

5. **Writing to the wrong path.** Plans output files go to `/root/.hermes/plans/consolidation-<name>.md`. Skills go to the skills tree. Don't confuse them.

6. **Creating a skill that's too narrow.** If the name only makes sense for today's specific session (e.g., `consolidation-2026-07-08-federation`), it's wrong. Use class-level names (`hermes-prime-federation-map`, `seven-zen-organs-enforcement`).

## Verification Checklist

- [ ] All source fragments read (batch parallel reads)
- [ ] Unique contribution extracted for each fragment
- [ ] §PROVENANCE table present with all fragments, versions, and unique contributions
- [ ] Target file(s) written with valid YAML frontmatter
- [ ] Word count verified (2,000–4,000 per consolidated skill)
- [ ] No duplicated content within or across files
- [ ] Concrete field-level detail preserved (receipts, error tables, exact commands)
- [ ] Footer includes forge date, consolidation agent, and predecessors absorbed
