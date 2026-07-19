---
name: skills-library-dimensional-audit
description: Audit and reorganize the Hermes skill library using orthogonal dimensions and cross-cutting paradoxes — not flat alphabetical dumps. Produces a dimensional map with matrix, health checks, and recommendations without changing any skill. Use when Arif asks to "map the skills", "organize the library", "audit the skill set", "show me the skills by dimension/paradox", or any request to restructure or visualize the skill collection.
triggers:
  - "map the skills"
  - "organize the skills"
  - "skill library audit"
  - "skills by dimension"
  - "skills by paradox"
  - "rearrange the skills"
  - "orthogonal map"
---

# Skills Library Dimensional Audit

## When to Load
- Arif asks to map, organize, audit, or visualize the skill library
- Periodic curator reviews (monthly recommended)
- After adding 10+ new skills in a short period
- When skill categories feel stale or overlapping

## The 7 Orthogonal Dimensions

Every skill gets exactly ONE primary dimension. These are orthogonal — no skill spans two primaries.

| Dim | Name | Question | Examples |
|-----|------|----------|----------|
| D1 | OBSERVATION | "How You See?" | research, forensics, data extraction, validation |
| D2 | CREATION | "How You Build?" | design, code gen, media, documents, PDFs |
| D3 | GOVERNANCE | "How You Constrain?" | audit, verification, alignment, floors, scars |
| D4 | EXECUTION | "How You Act?" | deploy, delegate, debug, test, plan |
| D5 | INFRASTRUCTURE | "How You Survive?" | federation, config, CI/CD, liveness, git |
| D6 | INTELLIGENCE | "How You Compute?" | ML, benchmarks, inference, experiment tracking |
| D7 | INTERFACE | "How You Surface?" | email, chat, notes, smart home, social, TTS |

## The 5 Cross-Cutting Paradoxes

These are TENSIONS, not categories. Every skill sits at the intersection of its dimension and at least one paradox.

| # | Paradox | Tension | Governing Floor |
|---|---------|---------|-----------------|
| P1 | OBS ↔ HALL | Seeing more risks inventing more | F2 (TRUTH) + F9 (ANTI-HANTU) |
| P2 | CRE ↔ DES | Every artifact kills an alternative | F4 (CLARITY) + F8 (GENIUS) |
| P3 | GOV ↔ EXE | Too much law = paralysis | F1 (AMANAH) + F13 (SOVEREIGN) |
| P4 | ID ↔ ROLE | Who you are constrains what you do | F10 (ONTOLOGY) + F6 (MARUAH) |
| P5 | KNO ↔ PAR | More context without action = noise | Ψ (VITALITY) |

## Procedure

### Step 1: Enumerate
```
skills_list()  → full list with categories
```
Record total count and category distribution.

### Step 2: Assign Dimensions
For each skill, assign exactly ONE primary dimension based on what the skill DOES (not what category Hermes gave it). Hermes categories are convenience groupings; dimensions are orthogonal.

Rules:
- A skill that "builds X" is D2 CREATION even if X is a governance artifact
- A skill that "audits X" is D3 GOVERNANCE even if X is infrastructure
- A skill that "researches X" is D1 OBSERVATION even if X is for execution
- When unclear: does the skill primarily SEE, BUILD, CONSTRAIN, ACT, SURVIVE, COMPUTE, or SURFACE?

### Step 3: Map Paradox Anchors
For each dimension, identify which paradox(es) its skills sit under. A skill can have a secondary paradox but must have one primary.

### Step 4: Build the Matrix
```
            OBS  CRE  GOV  EXE  INF  INT  IFace
P1 OBS↔HALL ████
P2 CRE↔DES       ████
P3 GOV↔EXE             ████ ████
P4 ID↔ROLE             ████
P5 KNO↔PAR ████             ████
```

### Step 5: Paradox Health Check
For each paradox, assess:
- **HEALTHY** — tension is balanced, floors are working
- **TENSION** — both sides are heavy, risk of one dominating
- **RISK** — one side is overwhelming, action needed

### Step 6: Uncategorized Assignment
Hermes default-category skills often lack clear dimensional homes. Assign each one explicitly with rationale.

### Step 7: Recommendations
Observation-only. No changes during the audit. Recommendations for:
- Consolidation candidates (too many skills in one dimension)
- Paradox imbalance fixes
- Skills that need better trigger coverage
- Skills that overlap and should merge

## Output Format

Produce a single `.md` file with:
1. Header (count, date, scope)
2. The 7 Dimensions (table per dimension with all assigned skills)
3. The 5 Paradoxes (description + tension + floor + affected skills)
4. Orthogonal Matrix (ASCII grid)
5. Category-to-Dimension mapping (showing how Hermes categories map to dimensions)
6. Uncategorized skills with proposed assignments
7. Paradox Health Check table
8. Recommendations (observation only)
9. Constitutional anchor

## Delivery
Send the resulting `.md` file to Arif's Telegram via Bot API:
```bash
curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendDocument" \
  -F chat_id="267378578" \
  -F document="@<path>" \
  -F caption="📐 SKILLS DIMENSIONAL MAP — N skills × 7D × 5P"
```

## Skill Quality Evaluation (2026-07-11)

When auditing skills, don't just count and categorize — **evaluate quality**. Every skill must pass 4 tests: trigger clarity, output spec, operational steps, independence. Skills using physics/science terminology as decoration over classical operations are "cosplay" — extract the insight, discard the metaphor.

See `references/skill-quality-evaluation-2026-07-11.md` for the full evaluation framework, quality classes (OPERATIONAL/FRAMEWORK/REFERENCE/VAPOR), and the 2026-07-11 quantum skills audit results (7 keep, 11 kill out of 18).

## Pitfalls
- **Don't use Hermes categories as dimensions.** Categories like "creative" or "devops" are convenience groupings, not orthogonal axes. A "creative" skill that audits is D3 GOVERNANCE, not D2 CREATION.
- **Don't assign multiple primary dimensions.** Force one. Secondary cross-dimensions are noted but the primary must be singular.
- **Don't change skills during the audit.** The map is observation-only. Recommendations come after.
- **Don't forget the paradoxes.** A dimensional map without paradoxes is just a fancy category list. The paradoxes are what make it orthogonal — they cut ACROSS dimensions.
- **Matrix cells can be empty.** Not every dimension×paradox intersection needs skills. Empty cells are informative too.
- **State at T₀ ≠ state at T₁.** An audit is a snapshot. Between audit and execution (especially across sessions), the live state may have changed — skills may have been pre-archived, duplicates already merged, categories shifted. Never execute audit recommendations blindly. ALWAYS probe live state first with `find` (excluding `.archive*` and `.quarantine*` dirs), verify each target file exists, compare against the audit's assumptions, and adapt the plan before any `mv`/`rm`. This is the Iron Rule applied to skill hygiene: probe at T₁ before irreversible file moves. Pattern validated 2026-07-08: 70 skills archived across Steps 1-4 with zero blast radius. See `references/cleanup-execution-pattern-2026-07-08.md` for the full probe→verify→move→registry→count→receipt pattern and the Step 4 provenance consolidation pattern.
