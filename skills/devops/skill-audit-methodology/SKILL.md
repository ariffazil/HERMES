---
name: skill-audit-methodology
description: "Audit skill libraries for redundancy, quality, naming alignment, and foundational coverage. Three-loop zen distillation: extract → cross-reference → distill."
version: 1.0.0
triggers:
  - "audit skills"
  - "skill redundancy"
  - "skill quality"
  - "skill naming"
  - "zen skills"
  - "skill library health"
  - "federated skills"
  - "skill consolidation"
  - "archive skills"
  - "skill duplicates"
  - "engine variants"
  - "hermes variant"
  - "skill gap analysis"
  - "agent card skills missing"
  - "eureka zen"
floors: [F2, F4, F7, F11]
---

# Skill Audit Methodology

Repeatable process for auditing any skill library — single agent or federated multi-agent.

## After the Audit: Acting on Findings

The audit identifies what to archive, what to align, and what's missing.
For the actual **execution** of:
- **Archiving duplicates** (move → ARCHIVE-* prefix, update alias table, agent-card cross-ref)
- **Aligning engine variants** (enhance hermes/claude/codex variants with native guidance)
- **Forging gaps** (agent-card referenced skills missing from disk)
- **Verifying state** (gauge, health check, manifest)

→ See `references/archive-execution-pattern.md` for the step-by-step execution protocol.

For **cross-directory consolidation** (merging .agents into AAA via symlinks):
→ See `references/cross-directory-consolidation.md`

For **boot-wiring** (making knowledge modules auto-load at init via governed.json):
→ See `references/boot-wiring-pattern.md`

## When to Use

- Skill library has grown organically and needs consolidation
- After a unification/migration to verify it actually worked
- Before pruning — extract wisdom before deleting
- When naming is inconsistent across agents/surfaces
- Periodic health check (quarterly recommended)

## The Three-Loop Zen Process

### Loop 1: QUANTITATIVE MEASURE

Audit every skill on hard metrics:

**Prefix-duplicate detection (scored 2026-07-13):**
Before deep content analysis, check for name-prefix duplicates:
```python
# A common federation anti-pattern: FORGE-x + x, ASI-x + x, ARCHIVE-x + x
# where content is identical except the `name:` frontmatter field.
# Detection: compare line counts + first 20 lines of SKILL.md per pair.
pairs = [(f"FORGE-{name}", name) for name in all_names if f"FORGE-{name}" in all_names]
for forge, generic in pairs:
    forge_lines = count_lines(f"/skills/{forge}/SKILL.md")
    generic_lines = count_lines(f"/skills/{generic}/SKILL.md")
    if forge_lines == generic_lines:
        diff = diff_first_20_lines(forge, generic)
        if diff == "name:" only:
            mark_duplicate(forge, generic)  # generic is superseded
```
The FORGE-/ASI- prefix variants are canonical (they have engine subdirs, agent-card references). The un-prefixed generics are superseded. See `references/archive-execution-pattern.md` for the archive workflow.

```
For each skill:
  - exists on disk? (bool)
  - file_size (bytes)
  - line_count, word_count
  - has_triggers? ("when to use" / "use when" / "trigger")
  - has_pitfalls? ("pitfall" / "gotcha" / "watch out")
  - has_verification? ("verify" / "test" / "check")
  - has_references/templates/scripts? (linked files)
  - description_length
  - content_hash (md5, for exact duplicates)

Quality score (0-100):
  +20  file exists
  +20  substance (min 2000 chars for full score)
  +10  has triggers
  +10  has pitfalls
  +10  has verification
  +10  has linked files
  +10  description quality (len/10)
  +10  word count > 200
```

Tiers: EXCELLENT (80-100), GOOD (60-79), THIN (40-59), SKELETON (0-39).

### Loop 2: SEMANTIC OVERLAP DETECTION

Two levels of similarity:

**Description-level** (fast, cheap):
```python
SequenceMatcher(None, desc1, desc2).ratio() > 0.5
```

**Content-level** (deep, expensive):
```python
# Combined score: 60% sequence match + 40% Jaccard keyword overlap
seq = SequenceMatcher(None, content1[:3000], content2[:3000]).ratio()
jac = len(kw1 & kw2) / len(kw1 | kw2)
combined = seq * 0.6 + jac * 0.4
# > 0.25 = non-trivial overlap
```

Also check:
- **Exact duplicates**: same content hash → run `references/canonical-determination-pattern.md` to determine which copy is canonical and which is a rogue bulk-copy
- **Cross-references**: skills that cite other skills by name
- **Contradictions**: skills that say "deprecated" / "superseded"

### Loop 3: ZEN DISTILLATION

Extract irreducible wisdom from the corpus:

1. **Recurring principles**: bold claims appearing in 3+ skills
2. **Meta-patterns**: concepts present across all skills (e.g., evidence-before-action %)
3. **Floor usage heatmap**: which constitutional floors are referenced most/least
4. **Unique insights per skill**: terms/concepts in this skill but NOT in others of same category
5. **Best-in-cluster**: for each redundancy cluster, which skill has the most unique knowledge + triggers

Output: ranked list of eureka insights + distilled laws.

## Multi-Agent Federation Audit

When auditing across multiple agent surfaces (e.g., AAA, Hermes, OpenClaw):

1. Load skills from each surface independently
2. Extract concepts per surface (floors, patterns, operations)
3. Find UNIVERSAL concepts (present in all surfaces)
4. Find SURFACE-SPECIFIC concepts (unique to one)
5. Identify COVERAGE GAPS (universal concepts missing from surfaces)
6. Map to foundational invariants (VERIFY, REFLEX, REVERSE, REDUCE, GUARD, SHADOW, SUSTAIN)

See: `references/agent-foundations.md` for the7 timeless foundations.

## Naming Convention

Align prefixes to the7 zen laws:

| Prefix | Law | Domain |
|--------|-----|--------|
| `gov-` | Γ REFLEX | Governance, floors, authority |
| `eng-` | Δ ENTROPY | Engineering, build, ops |
| `geo-` | Ω VERIFY | Earth, capital, verification |
| `mem-` | Λ METABOLISM | Vault, dream, continuity |
| `met-` | Σ SHADOW | Meta-audit, skills, drift |
| `con-` | Ψ DIGNITY | Consciousness, boundary |
| `ops-` | Φ IRREVERSIBLE | Operations, bootstrap |
| `ker-` | ∞ KERNEL | Trinity, quantum, eureka |

Format: `prefix-verb-noun`, ≤25 chars, filesystem-safe, no collisions.

## Pruning Checklist

Before deleting skills:
- [ ] Extract unique insights (Loop 1 unique terms)
- [ ] Check cross-references (will deleting break other skills?)
- [ ] Verify symlink integrity (broken symlinks = agent confusion)
- [ ] Remove rogue copies (directories that aren't symlinks to canonical; see `references/canonical-determination-pattern.md` for timestamp-cluster detection and bulk-copy identification)
- [ ] Remove orphan canonicals (in registry, linked by nobody)
- [ ] Remove stubs (<30 char descriptions, <50 words)

## Knowledge Ontology Coverage Audit

After the3-loop process, map skills against the8 knowledge domains:

| Domain | Sigil | Keywords |
|--------|-------|----------|
| Physics | Φ | physics, entropy, thermodynamic, energy, conservation, quantum |
| Mathematics | Μ | math, theorem, proof, algebra, calculus, probability, bayesian |
| Linguistics | Λ | language, grammar, syntax, semantics, nlp, prompt, meaning |
| Biology | Β | biology, evolution, organism, neuroscience, genome, metabolism |
| Cognition | Ψ | cognition, bias, heuristic, attention, memory, consciousness |
| Computation | Κ | algorithm, complexity, compiler, software, api, protocol, docker |
| Social | Σ | governance, institution, power, law, policy, sovereignty, dignity |
| Art | Α | art, aesthetic, beauty, design, creative, music, literature |

For each surface (agent), count skills that contain domain keywords. Result:
```
Domain          AAA     Hermes  OpenClaw  Status
Physics         69%     72%     36%       🟡 OpenClaw weak
Mathematics     58%     63%     10%       ❌ OpenClaw critical
Biology         10%     35%     10%       ❌ AAA & OpenClaw critical
```

Gaps <25% in any surface → need dedicated skill.

### Bridge Skill Identification

A **bridge skill** spans 3+ knowledge domains. These are the strongest assets — they connect knowledge.

```python
for sid, content in skills.items():
    domain_hits = [d for d, kw in domain_keywords.items() if any(k in content for k in kw)]
    if len(domain_hits) >= 3:
        # This is a bridge skill
        print(f"{sid} → {', '.join(domain_hits)}")
```

Bridge skills are the nexus points of the knowledge graph. Protect them during pruning.

### Agent-Card Cross-Reference Gap Analysis (scored 2026-07-13)

Skills referenced in agent cards MUST exist on disk. Run this check after any archive/forge operation:

```python
# Phase 1: Collect all skill IDs from all agent-card.json files
agent_skills = set()
for card_path in glob('**/agent-card.json', recursive=True):
    card = json.load(open(card_path))
    for s in card.get('skills', []):
        sid = s.get('id', '') if isinstance(s, dict) else str(s)
        agent_skills.add(sid)

# Phase 2: Collect all skills on disk
disk_skills = set(os.listdir('/root/AAA/skills/'))  # + .agents/skills/

# Phase 3: Find gaps
missing = agent_skills - disk_skills  # skills referenced but NOT on disk → forge targets
unreferenced = disk_skills - agent_skills  # skills on disk but NOT referenced → archive candidates

print(f"Agent-referenced: {len(agent_skills)}")
print(f"Disk-available: {len(disk_skills)}")
print(f"GAP (need to forge): {len(missing)}")
print(f"ORPHANED (archive candidates): {len(unreferenced)}")
```

**Critical check:** If a lane agent card (e.g., 333-AGI, 555-ASI, 888-APEX) references a skill that doesn't exist, the lane cannot function. These are HIGH-priority forge targets.

**Substrate check:** `KERNEL-*` and `RSI-*` skills must be present in EVERY agent card. Use batch injection:
```python
# Tiered kernel binding
UNIVERSAL = [KERNEL-reality-skills, KERNEL-sovereign-recognize, KERNEL-session-inhabit, RSI-recursive-improvement]
LANE = [KERNEL-trinity-33, KERNEL-mcp-zen]
FORGE = [KERNEL-verbs-forge-hands, KERNEL-mcp-builder]
INTEL = [KERNEL-quantum-runtime, KERNEL-qubit-substrate]
# External CODING/FI agents → UNIVERSAL only
# Lanes + Warga → UNIVERSAL + LANE + tier-specific
```

See `references/archive-execution-pattern.md` for the full archive workflow.

### Kill/Keep/Merge/Doc Classification

After audit, classify every skill:

| Action | Criteria | Count Target |
|--------|----------|-------------|
| KEEP | Has triggers + substance + unique value | ~40-50% |
| MERGE | Overlaps with another, combine content | ~20-25% |
| DOC | No trigger, no bridge → becomes documentation | ~5-10% |
| KILL | Empty stub, superseded, or phantom | ~20-30% |

## 3-Axis Skill Architecture (structural invariant for all skills)

Every skill must declare three orthogonal dimensions:

| Axis | Question | Test |
|------|----------|------|
| **Invariant** | What's timeless? | Survives tool/org/API changes? |
| **Bridge** | What connects? | Linked to kernel verbs + other skills + knowledge? |
| **Contrast** | What is this NOT? | Clear boundaries with neighbor skills? |

**Anti-drift rule:** No invariant → kill. No bridge → isolate. No contrast → merge.

### Veto-Generator Contract (knowledge boundary)

Universal knowledge skills (know-physics, know-math, know-language) are **veto layers** — enforce boundary conditions, never generate hypotheses. Domain skills (geo-*, wealth-*) are **generators** — produce hypotheses, must pass veto before irreversible action. Stack: Domain generates → Universal vetoes → Sovereign ratifies.

### Bootstrap Manifest Pattern (bootstrapping paradox)

The loader cannot be a skill (circular). It's a **signed data artifact** consumed by immutable kernel primitive `bootstrap-load`. Manifest lists 9 universal skills with SHA256 hashes, signed by sovereign Ed25519 key. Kernel verifies signature + hashes + self-host test before loading any YAML. Artifacts: `BOOTSTRAP_MANIFEST.json`, `BOOTSTRAP_LOAD_SPEC.json`, `CI_VALIDATION_GATES.json`, `SKILL_MANIFEST_TEMPLATE.json` in `/root/AAA/skills/`.

### Blindspot Agents (meta-governance)

Three agents operate on the skill system itself:
- **superposition-manager** — holds competing hypotheses, prevents premature collapse
- **flow-diagnostics** — monitors live skill behavior, flags prune/evolve
- **lineage-attester** — verifies seal chain integrity, zero tolerance for breaks

Full details: `references/aaa-skill-architecture-2026-07-11.md`

## Pitfalls

- **Unification ≠ deduplication.** Merging directories doesn't remove redundancy. Run content-level similarity AFTER structural unification.
- **GEOX/geology skills look redundant but aren't.** Petrophysics ≠ basin modeling ≠ seismic. Different geological disciplines. Check domain knowledge before merging.
- **Broken symlinks are silent failures.** Agents load nothing and don't error. Always check `os.path.islink()` + `os.path.exists()`.
- **Rogue copies survive sync scripts.** The sync script may ADD symlinks NEXT to existing directories without removing the originals. Use `--purge-rogues` or manual cleanup.
- **Background coordinator may forge skills during the audit.** During federated operations, a 333-AGI or other coordinator agent may autonomously forge new skills (e.g., AGI-claude-xml-structured-reasoning, FORGE-data-compression) while the audit is in progress. After any long-running operation, re-scan for new directories: `find /root/AAA/skills/ -maxdepth 1 -mmin -60 -type d | sort`. These new skills need entries in SKILL_ALIAS_TABLE with status=FORGED. **Detection tip:** bulk-copied rogues share an identical `stat -c '%Y'` timestamp across all copies — a single bulk operation produces a timestamp cluster. Run timestamp comparison across suspected duplicate pairs to distinguish original (older, individual timestamp) from rogue (batch timestamp). See `references/canonical-determination-pattern.md`.
- **Gateway can't restart itself.** `hermes gateway restart` from inside the gateway = circular dependency. Use `systemctl restart hermes-asi-gateway.service` directly. SIGHUP to the gateway PID may trigger config reload without full restart.
- **Telegram group IDs change on supergroup migration.** The API returns the new ID as a message. Update `allowed_chats` and `free_response_chats` with the new ID. The old ID becomes invalid.
- **`hermes config set` serializes lists as JSON strings**, not YAML lists. After setting list values, grep the config to verify format. If serialized as `'["a","b"]'` instead of YAML list, fix with: `python3 -c "import yaml,json; d=yaml.safe_load(open('config.yaml')); d['telegram']['allowed_chats']=json.loads(d['telegram']['allowed_chats']); yaml.dump(d,open('config.yaml','w'),default_flow_style=False)"`
- **`bot_token_env` must match actual env var name.** Default is `TELEGRAM_BOT_TOKEN` but the actual var may be different (e.g., `ASI_ARIFOS_BOT_TOKEN`). Check `~/.hermes/.env` for the real var name and set `telegram.bot_token_env` accordingly. `hermes send` will fail silently if this is wrong.
- **`hermes send` needs the token in env.** If `bot_token_env` points to a var that isn't exported, `hermes send` fails with "You must pass the token you received from BotFather." Either fix `bot_token_env` or export the correct var before calling.
- **YAML frontmatter check must test line 1, not head -5.** When checking for valid YAML frontmatter, `head -5 | grep "^---"` can produce false positives if `---` appears as a markdown separator later. Always check `head -1` equals exactly `---`. The correct check: `first_line=$(head -1 "$f"); if [ "$first_line" != "---" ]; then echo "BAD_YAML"; fi`. Skills with non-YAML first lines (e.g., starting with `#` heading) still work but lose structured metadata parsing.
- **"OpenClaw" legacy references are common after rebranding.** When a product/org gets renamed, grep for the old name across all SKILL.md files. Skills referencing the old name aren't broken but contain stale terminology that confuses new agents. Batch find-replace or flag for manual update.

## Hermes Library Audit Reference

→ See `references/hermes-library-audit-2026-07-15.md` for a concrete audit of the Hermes skills library (158 active skills, 7 overlap clusters, naming issues, structural findings). Use as a template for future library audits.
