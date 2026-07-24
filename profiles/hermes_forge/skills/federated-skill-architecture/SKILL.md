---
id: federated-skill-architecture
name: federated-skill-architecture
version: 1.0.0
description: >
  Design, validate, and manage skills across a multi-agent federation.
  3-layer architecture (substrate/knowledge/domain), 3-axis manifests
  (invariant/bridge/contrast), veto-generator separation, bootstrap
  signing, CI validation gates, and naming conventions.
owner: F13 SOVEREIGN
status: active
trigger_phrases:
  - "skill architecture"
  - "skill registry"
  - "skill naming"
  - "skill manifest"
  - "bootstrap manifest"
  - "veto generator"
  - "substrate skills"
  - "knowledge foundation"
  - "toolbench alignment"
  - "agent card audit"
  - "zen the toolbench"
  - "agent card fix"
  - "A2A wiring"
---

# Federated Skill Architecture

> **Purpose:** Class-level pattern for designing, validating, and managing skills across a multi-agent federation. Not tied to any specific agent — applies to any governed multi-agent system.

## The 3-Layer Architecture

```
Layer 1: SUBSTRATE (how agents think) — always loaded, agent-agnostic
Layer 2: KNOWLEDGE (what agents know) — always loaded, veto layer
Layer 3: DOMAIN (where agents operate) — load on demand, per-agent
```

Every agent loads Layer 1 + 2. Layer 3 is per-role.

## The 3-Axis Manifest

Every skill must declare three axes:

| Axis | Question | Test |
|---|---|---|
| **Invariant** | What's timeless? | Survives tool/org changes? |
| **Bridge** | What connects? | Linked to kernel verbs + other skills? |
| **Contrast** | What is this NOT? | Clear boundaries with neighbors? |

**Anti-drift rule:** If a skill has no invariant → kill. No bridge → isolate. No contrast → merge.

## Canonical Skill Manifest Template

Required fields for every skill:

```yaml
id: lowercase-kebab
name: Human Name
version: semver
layer: substrate | knowledge | domain
purpose: One sentence.
invariants:
  authority: What grants permission
  evidence_schema: How evidence is typed (OBS/DER/INT/SPEC)
  reversibility: true/false
  lineage: How provenance tracked
  trigger_semantics: Boolean predicate for activation
  failure_contract: What happens on partial failure
  resource_budget: {cpu, time_ms, entropy}
  audit_surface: [what gets logged]
bridge_connections:
  kernel_verbs: [arif_* verbs used]
  skills: [connected skills]
  knowledge: [knowledge foundations]
  protocol: synchronous_rpc | event_stream | ledger_append | knowledge_substrate
  inputs: {typed fields}
  outputs: {typed fields}
contrast:
  not: [skills this is NOT]
  distinction: How to tell from neighbors
  trigger_conflicts: When this should NOT fire
```

## Veto-Generator Separation

**Critical pattern for knowledge boundaries:**

- **Domain skills = GENERATOR** — produce hypotheses from empirical data. Authority: ADVISORY.
- **Universal skills = VETO** — enforce boundary conditions. Authority: BINDING. Can kill any claim that violates physical/mathematical law.
- **Sovereign = TRUTH** — ratifies axioms the framework cannot verify.

Rule: Domain generates, universal vetoes. Never invert.

Scope tags for domain claims: `{global|regular|local}` + evidence type: `{theory|empirical|simulation}`.

## Bootstrap Manifest (Firmware, Not Skill)

The loader is NOT a skill. It's a signed data artifact consumed by a kernel primitive.

```json
{
  "manifest_version": "1.0.0",
  "universal_skills": [
    {"name": "skill-name", "layer": "substrate", "hash": "sha256:..."}
  ],
  "signatures": [{"key_id": "...", "signature": "..."}],
  "content_hash": "sha256:..."
}
```

**Key insight:** Breaking the circularity — the loader is DATA + kernel primitive, not a skill. Like BIOS vs OS.

## Naming Convention: `{domain}-{verb}`

All lowercase kebab-case. Max 3 words. Domain prefix mandatory.

Domains: `kernel`, `geo`, `wealth`, `well`, `forge`, `a2a`, `meta`, `mem`, `sec`, `ops`, `dev`, `research`

No "skill", "intelligence", "engineering", "doctrine" in names.

## CI Validation Gates

10 gates for production skill systems:

1. **manifest_schema** — validate against schema
2. **skill_hash_integrity** — recompute hashes, compare to manifest
3. **three_axis_completeness** — invariant/bridge/contrast all present
4. **dependency_acyclicity** — no circular dependencies
5. **veto_generator_separation** — substrates don't generate, domains don't veto
6. **adversarial_contradiction** — inject contradictions, verify veto catches
7. **bootstrap_self_host** — deterministic self-host test
8. **signature_present** — at least 1 valid signature
9. **skill_count_bounds** — flag if growing beyond threshold
10. **entropy_budget** — verify entropy non-increasing across boot phases

## The EUREKA-ZEN Workflow: Federation-Wide Skill Lifecycle

When a federation-wide skill audit and alignment is needed, follow this 5-phase lifecycle:

### Phase 1 — Deep Scan & Chaos Purge
1. Map ALL skill surfaces (`AAA/skills/`, `.agents/skills/`, Hermes library)
2. Identify duplicates: FORGE-*/generic pairs, ASI-*/generic pairs, same-content-different-name
3. Check agent-card references — if the archived skill is NOT in any agent card, safe to archive
4. Archive by renaming to `ARCHIVE-<name>` — never `rm -rf`
5. Update `SKILL_ALIAS_TABLE.json` with tombstone entries pointing to canonical
6. Sync to all 3 copies (root, AGI-skill-unification, skill-unification)

### Phase 2 — Architectural Alignment (Bijaksana)
Refactor skills to the cognitive engine that will execute them:
- **Claude Code**: XML-tag structuring, extended context recall patterns
- **Codex**: Chain-of-thought, strict step-by-step deduction, precise API schema adherence
- **Hermes (Nous)**: Conversational voice (BM+English), creative media routing, SOUL.md obedience
- Engine variants live under `skills/<name>/claude/` or `skills/<name>/hermes/`

### Phase 3 — Forge Gaps (Eureka)
1. Cross-reference agent-card skill IDs against skills on disk
2. Missing skills = architectural gaps — forge new SKILL.md files
3. Prioritize: lane-critical (role bindings), cross-agent (handoff protocols), intelligence (memory tiers)
4. Each forged skill must conform to the 3-axis manifest format

### Phase 4 — KERNEL Substrate Injection
Every agent card must inherit arifOS baseline physics. Inject via tiered script:
- **Universal (all)**: KERNEL-reality-skills, KERNEL-sovereign-recognize, KERNEL-session-inhabit, RSI-recursive-improvement
- **Lane add**: KERNEL-trinity-33, KERNEL-mcp-zen
- **Forge add**: KERNEL-verbs-forge-hands, KERNEL-mcp-builder
- **Intel add**: KERNEL-quantum-runtime, KERNEL-qubit-substrate

### Phase 5 — Seal
1. Verify SKILL_ALIAS_TABLE synced across all copies (hash match)
2. Verify federation health (all 6 organs green)
3. Write seal payload to VAULT999 seal chain
4. Verdict: SEAL (if kernel-verified) or HOLD (needs F13 upgrade)

### Pitfalls
- **Same-content skills with different names** — FORGE-* vs generic. Only `name:` field differs. Choose FORGE-* as canonical (V3 design).
- **Agent cards reference skills that don't exist** — 73 gaps found in one audit. Document and forge in priority order.
- **SKILL_ALIAS_TABLE has 3 copies** — background forges may update root but not copies. Always verify hash match.

## Three Gödelian Paradoxes (and Mitigations)

| Paradox | Mitigation |
|---|---|
| **Bootstrapping** — loader needs skills, skills need loader | Firmware primitive + signed manifest (data, not code) |
| **Compression** — universal ≠ derivable from domain | Veto pattern: universal constrains, domain generates |
| **Authority** — framework validates structure, not truth | External ratification: sovereign signs the truth |

These are REAL LIMITS, not bugs. Design for them, don't pretend they don't exist.

## Pitfalls

1. **Philosophical skills** — if a skill has no trigger, no outputs, no protocol, convert to a doc. "Quantum" metaphors without operational content are vapor.
2. **Naming chaos** — mixed `UPPER_CASE`, `kebab-case`, emoji prefixes. Pick one convention and enforce.
3. **Duplicate skills** — same invariants + different names = merge. Check before creating.
4. **Skills that duplicate kernel verbs** — the kernel provides capability; skills teach discipline. If a skill just wraps `arif_init`, it's redundant.
5. **Bootstrap key != kernel identity** — the manifest signing key and the kernel's sovereign identity are separate concerns. Don't conflate them.
6. **Skipping the 3-axis check** — every skill must have invariant/bridge/contrast. No exceptions.
7. **Treating substrate as domain** — substrate skills are TIMELESS. If it references a specific tool version or API, it's domain.
8. **Agent cards rot silently** — model fields, MCP counts, skill lists in agent cards go stale within weeks. The card says `claude-sonnet-4` but the binary uses `deepseek-v4-pro`. Audit cards against live config at least monthly. Check: model, binary path, MCP servers, skills list, FI slot, **A2A endpoint**, **MCP binding**. Pattern: read agent card → read live config → diff → update card. See `references/agent-card-alignment.md` for full 3-phase protocol including contradiction detection (harness vs forge vs registry), orphan archival, and registry sync.

## Agent Loading Matrix

| Agent | Substrates | Knowledge | Domains |
|---|---|---|---|
| Full (Hermes) | 6 | 3 | research, meta, geo, wealth, well |
| Coder (Claude) | 6 | 3 | dev, forge, ops, meta |
| Metabolizer (OpenClaw) | 4 | 3 | mem, ops, a2a |
| Executor (Codex) | 6 | 3 | dev, forge, ops |
| Minimal (Kimi) | 6 | 3 | dev, forge, ops, meta, a2a |

## Key Files

| Artifact | Purpose |
|---|---|
| `BOOTSTRAP_MANIFEST.json` | Signed manifest with 9 skills, hashes, keys |
| `BOOTSTRAP_LOAD_SPEC.json` | 7-step kernel primitive spec |
| `CI_VALIDATION_GATES.json` | 10 gates + 4 canary tests |
| `SKILL_MANIFEST_TEMPLATE.json` | Canonical schema |
| `VETO_GENERATOR_CONTRACT.json` | Knowledge boundary resolution |
| `META_GOVERNANCE.json` | Quorum + adversarial + cadence |
| `BLINDSPOT_AGENTS.json` | 3 agents for system self-monitoring |
| `TOOLBENCH_3WAY_CONTRAST.md` | 3-agent full spec comparison (kimi, opencode, claude) — `/root/AAA/docs/TOOLBENCH_3WAY_CONTRAST.md` |

## References

- `/root/AAA/skills/` — canonical skill directory
- `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` — 63 canonical skills
- `/root/AAA/scripts/sign-manifest.sh` — signing script
- `/root/.secrets/bootstrap/` — root keypair
- `references/skills-vs-agents.md` — When to use A2A delegation vs loading a skill
- `references/salam-aaa-init-pattern.md` — Platform-agnostic agent bootstrap (SALAM ceremony, thin-wrappers, universal init)
- `references/mcp-server-wiring-pattern.md` — Federation-wide MCP server deployment (5-step pattern from Hound deployment)
- `references/session-artifact-inventory.md` — Session artifact inventory
- `references/agent-card-alignment.md` — Agent card vs live config alignment

---

*Forged: 2026-07-11 from AAA skill substrate session.*
*DITEMPA BUKAN DIBERI*
