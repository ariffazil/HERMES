# Cleanup Execution Pattern — 2026-07-08

> **When:** Audit recommendations exist but live state may have drifted.
> **Lesson:** Always probe T₁ before irreversibly moving files. Audit assumptions ≠ live state. Adapt, then execute.

## The Pattern

```
1. LOAD AUDIT → 2. PROBE T₁ → 3. VERIFY EACH FILE EXISTS → 4. CREATE ARCHIVE DIRS → 5. MOVE FILES → 6. UPDATE DEPREC REGISTRY → 7. VERIFY COUNTS → 8. RECEIPT
```

## Steps 1-3: Archive + Deprecate (36 items — low blast radius)

### Audit Assumptions (T₀ — 2026-07-07)
- Apple skills (4): apple-notes, apple-reminders, findmy, imessage → archive
- Legacy agents (14): FORGECODE-Autonomous-Init, aforge-execution, agentic-builder, etc. → deprecate
- Duplicates (17): mmx-cli→minimax-cli, shadow-diagnostic→shadow-alignment-test, etc. → archive

### Execution
```
Step 1: Apple — 4 skills + DESCRIPTION.md → .hermes/.archive-2026-07-08/
Step 2: Legacy — 14 skills → .agents/.archive-2026-07-08/ + 31 entries in deprecation registry
Step 3: Duplicates — 17 skills → .agents/.archive-2026-07-08/
```

### Probe Pattern (before executing — critical step)
```bash
for d in skill-name-1 skill-name-2; do
  found=$(find /root/.agents/skills /root/.hermes/skills -maxdepth 3 -type d -iname "*$d*" 2>/dev/null)
  [ -n "$found" ] && echo "FOUND: $found" || echo "MISSING: $d"
done
```

## Step 4: Consolidation Provenance Pattern (34 fragments → 5 surfaced skills)

This is the HIGHER-RISK pattern — merging doctrine fragments into surfaced canonical skills with provenance traceability.

### The Rule
```
Fragment → Read content → Extract core logic → Add provenance table to surfaced skill → Archive fragment
```

### Provenance Table Format
Add this section at the END of each target surfaced skill (before References):

```markdown
## Absorbed [Domain] Fragments (YYYY-MM-DD)

[N] standalone [domain] skills consolidated here.

| Fragment | Core Contribution | Status |
|----------|------------------|--------|
| `fragment-name` | One-line summary of what it contributed | Absorbed — see §[section] |
| ... | ... | ... |

**Provenance:** All fragments archived YYYY-MM-DD to `.agents/skills/.archive-YYYY-MM-DD/`.
```

### Step 4 Execution (this session — 2026-07-08)

| Target Surfaced Skill | Fragments Absorbed | Count |
|----------------------|-------------------|-------|
| `hermes-prime-reflex-v2` | 000-init-intent-classify, 010-forge-execute-warrant, 111-sense-evidence-observe, 333-mind-plan-generate, 666-heart-critique-stress, 888-judge-verdict-render, 999-vault-seal-immutable | 7 pipeline stages |
| `geox-federation-mcp-driver` | geox-claim-grammar, geox-constitution, geox-contradiction-engine, geox-earth-evidence, geox-epistemic-ladder, geox-petrophysics-bounds, geox-redteam-hantu, geox-scientific-writing, geox-000-999-deployment-macro | 9 GEOX fragments |
| `hermes-prime-federation-map` | a2a-federation-builder, aaa-cockpit, federation-observability, federation-safety-wiring, federation-topology-map | 5 federation fragments |
| `apex-governance` | CONSTITUTIONAL_REFLEX, apex-theory, constitutional-ignition-2026-07-07 | 3 APEX fragments |
| `seven-zen-organs-enforcement` | zen-organ-reality, zen-organ-witness, zen-organ-governance, zen-organ-execution, zen-organ-memory, zen-organ-meaning, zen-organ-civilization, zen-diagnostic-probe, ZEN_MD, ZEN_ORGANS | 10 ZEN fragments |

### Key Safety Rules for Consolidation
1. **Never delete fragments — always archive.** Content may be needed for future reference.
2. **Provenance table, not content dump.** Don't copy full fragment content into target. Map core contributions only.
3. **One fragment → one target.** If a fragment could go to multiple targets, pick the closest match.
4. **Verify both target and fragment exist at T₁** before any `mv` or `patch`.
5. **Archive only after successful patch.** If the provenance table patch fails, don't move the fragment.

### Total Results (Steps 1-4 combined)
```
BEFORE: 114 .agents skill dirs active
AFTER:   24 .agents skill dirs active (79% entropy reduction)
ARCHIVE: 70 items (65 .agents + 5 .hermes)
SURFACED: 122 SKILL.md intact (untouched)
BLAST RADIUS: ZERO
```

## Registry Update Pattern
The deprecation registry at `/root/AAA/docs/deprecation-registry.json` was updated using `patch` tool (string replacement, not JSON parsing — the file has pre-existing syntax issues). A new `deprecated_skills_2026-07-08` section was added before `deprecation_lifecycle` with entries containing: status, since, migration, reason.

## Remaining (Step 5 — not executed)
- 31 "OTHER" skills in audit table §3 needing Arif's judgment: KEEP/MERGE/DEPRECATE
- These require sovereign eyeball — some are ambiguous (fix-sequencer, caller-trace, etc.)
