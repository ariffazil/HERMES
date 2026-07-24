---
name: skill-substrate-framework
description: "3-axis skill substrate — invariants, bridges, contrast. 6 substrates + 3 knowledge foundations. Canonical manifest template. Agent loading matrix."
category: devops
version: 3.0.0
triggers:
  - "skill substrate"
  - "skill architecture"
  - "3-axis skill"
  - "skill manifest"
  - "foundational skills"
  - "knowledge foundations"
  - "agent skill loading"
  - "skill universe"
floors: [F2, F4, F7, F8, F11]
---

# Skill Substrate Framework v3

3-layer, 3-axis architecture for universal agent intelligence.
Forged 2026-07-11 from 124-skill audit → 63 canonical (50% reduction).

## When to Use

- Creating new skills (check if substrate already covers it)
- Auditing skill libraries for redundancy or gaps
- Designing agent loading profiles
- Onboarding new agents to the federation
- Checking if a proposed skill is vapor or real

## The Architecture

```
LAYER 1: 6 SUBSTRATES — how agents think (always loaded)
LAYER 2: 3 KNOWLEDGE — what agents know (always loaded)
LAYER 3: N DOMAINS — where agents operate (load on demand)
```

### Layer 1: 6 Substrate Skills

| # | Name | Kernel Verb | Purpose |
|---|------|-------------|---------|
| 1 | `kernel-bind` | `arif_init` + `arif_judge` | Session governance binding + floor awareness |
| 2 | `observe-ground` | `arif_observe` | Evidence before narrative. OBS/DER/INT/SPEC. |
| 3 | `route-dispatch` | `arif_route` | Right organ for right intent. |
| 4 | `memory-manage` | `arif_memory` | Store, recall, promote, compact, forget. |
| 5 | `verify-gate` | `arif_verify` + `arif_critique` | 4 gates: authority + evidence + reversibility + lineage |
| 6 | `audit-seal` | `arif_seal` + `arif_compose` | Log, receipt, seal. ΔS ≤ 0. |

**Anti-drift test:** If a skill can't map to a kernel verb → domain module or vapor.

### Layer 2: 3 Knowledge Foundations

| Name | Covers | Why Universal |
|------|--------|---------------|
| `know-physics` | mechanics, thermo, QM, info theory | All reality claims are physical |
| `know-math` | probability, algebra, optimization, logic | All computation is mathematical |
| `know-language` | semantics, pragmatics, discourse | All human interface is linguistic |

These are not "skills for scientists." They are the SUBSTRATE OF REASONING.

### Layer 3: Domain Modules (12 domains)

`geo-*` `wealth-*` `well-*` `forge-*` `dev-*` `ops-*` `meta-*` `a2a-*` `sec-*` `research-*` `mem-*` `kernel-*`

## 3 Axes per Skill

Every skill — substrate, knowledge, or domain — has 3 axes:

### Axis 1: INVARIANT (what is timeless)

The permanent truth this skill encodes. Survives tool changes, org changes, API deprecations. Not "how to use tool X" but "what law governs this domain."

Invariant fields:
- `authority` — verifiable lease or permission token
- `evidence_schema` — OBS/DER/INT/SPEC typing
- `reversibility` — explicit undo path or safe-hold
- `lineage` — immutable receipt chain (hash + signer)
- `trigger_semantics` — deterministic activation predicate
- `failure_contract` — what to do on partial failure
- `resource_budget` — CPU, time, entropy caps
- `audit_surface` — telemetry and ledger keys

### Axis 2: BRIDGE (what connects)

How this skill relates to other skills, organs, kernel verbs, and knowledge domains. A skill with no bridges is dead weight.

Bridge patterns:
- `synchronous_rpc` — short, authoritative checks
- `event_stream` — monitoring and bias detection
- `ledger_append` — irreversible records
- `runbook_call` — human-mediated escalation
- `knowledge_substrate` — foundational reasoning support

### Axis 3: CONTRAST (what this is NOT)

Boundaries. Where this skill stops and another begins. Prevents overlap creep.

Contrast rules:
- One trigger, one purpose
- No philosophical fluff — no trigger/no outputs = convert to doc
- Granularity: same invariants + bridges + different wording = merge
- Inline vs standalone: tiny decision trees inline; external bridges = skill

## Agent Loading Matrix

ALL agents load: 6 substrates + 3 knowledge = 9 universal.

| Agent | Substrates | Knowledge | Domains |
|-------|-----------|-----------|---------|
| **Hermes** | 6 | 3 | research, meta, geo, wealth, well |
| **Claude Code** | 6 | 3 | dev, forge, ops, meta |
| **OpenClaw** | 4 | 3 | mem, ops, a2a |
| **Codex** | 6 | 3 | dev, forge, ops |
| **Kimi** | 3 | 3 | dev, forge |

New agent? Load 9 universal + pick domain modules. Done.

## Canonical Manifest Template

```yaml
id: {skill-name}
version: {semver}
layer: substrate|knowledge|domain
purpose: {one sentence}
invariants:
  authority: {verifiable token/lease}
  evidence_schema: {OBS/DER/INT/SPEC typing}
  reversibility: {bool}
  lineage: {receipt chain spec}
  trigger_semantics: {boolean predicate}
  failure_contract: {partial failure behavior}
  resource_budget: {cpu, time_ms, entropy}
  audit_surface: {telemetry keys}
bridge_connections:
  kernel_verbs: [list]
  skills: [list]
  knowledge: [list]
  protocol: {rpc|event|ledger|runbook|knowledge}
  inputs: {typed fields}
  outputs: {typed fields}
contrast:
  not: [list of similar skills]
  distinction: {one sentence}
  trigger_conflicts: {when this fires vs others}
covers: {for knowledge skills — domain list}
domain_bridges: {for knowledge — per-domain applications}
replaces: {for substrate — skills absorbed}
```

## Pitfalls

- **Substrate skills don't duplicate kernel verbs.** Skills teach discipline; verbs provide capability. If a skill's content is just "call arif_X", it's a wrapper, not a skill.
- **Knowledge foundations are not domain skills.** `know-physics` is general physical reasoning. `geo-petrophysics` is domain rock physics. The former is substrate; the latter is module.
- **3-axis check catches creep.** No invariant → kill. No bridge → isolate. No contrast → merge.
- **hermes config set serializes lists as JSON strings**, not YAML lists. After using `hermes config set` for list values, verify with grep and fix with python if needed.
- **Gateway can't restart from inside itself.** Use `systemctl restart hermes-asi-gateway.service` or SSH from another terminal.
- **Telegram group IDs change on supergroup migration.** The API returns the new ID as a message. Update `allowed_chats` and `free_response_chats` with the new ID.
- **Merging JSON files loses top-level keys.** When merging `bootstrap_invariants.json` into `bootstrap_manifest.json`, the `_meta` key was missing from the merged file. `kernel_boot.py` crashed on `_meta` check. Always verify ALL required keys exist after a JSON merge — don't assume the merge target has the superset.
- **`python yaml.dump` serializes list-of-dicts as JSON strings.** When `yaml.safe_load` reads a YAML file with list fields, then `yaml.dump` writes it back, lists that were originally YAML format may become `'[\"a\",\"b\"]'` (JSON string). Always verify with `grep` after write. Fix: `yaml.dump(d, f, default_flow_style=False, sort_keys=False)`.
- **SSH signature verification requires specific syntax.** `ssh-keygen -Y verify` needs `-I <identity>` (the key comment) AND the allowed_signers file format (not raw public key). The identity must match the key comment exactly (e.g., `root-arif-888@arifOS`). If verification fails with "incorrect signature", check: (1) hash file content matches exactly what was signed, (2) identity matches key comment, (3) namespace matches (`-n manifest`).
- **Three-agent-surface governance gap.** AAA/skills (coding agents), Hermes skills, and OpenClaw skills are independent ecosystems. The kernel bootstrap only governs AAA. Hermes is governed by SOUL.md/AGENTS.md. OpenClaw by openclaw.json. The governance boundary ≠ skill boundary. Design for this — don't try to unify surfaces that have different runtime constraints.

## AAA Kernel Bootstrap Architecture

The substrate is enforced by **firmware**, not skills. The bootstrap is a kernel primitive, not YAML.

### The Three Fixes (Gödel's Shadow)

1. **Bootstrapping Paradox** → Firmware primitive. The9 invariants are hardcoded in `/root/AAA/kernel/bootstrap_invariants.json`. Loaded BEFORE any skill manifest. Signed by sovereign. Not a skill — data + kernel verb.

2. **Compression Boundary** → Veto vs Generator. Universal skills are VETOES (boundary conditions). Domain skills are GENERATORS (empirical priors). Sequential: domain generates → universal vetoes → if pass → output. `know-physics` doesn't teach `geo-basin` how to model. It rejects `geo-basin` outputs that violate conservation laws.

3. **Authority Gap** → Sovereign signature. Every manifest is inert until Arif signs it. Framework validates structure. Sovereign validates truth. Until signed, skill is quarantined to OBSERVE_ONLY.

### Kernel Artifacts (`/root/AAA/kernel/`)

| Artifact | Type | Purpose |
|----------|------|---------|
| `bootstrap_invariants.json` | FIRMWARE | 9 immutable invariants (BIOS) |
| `bootstrap_manifest.json` | DATA | Signed manifest with9 universal skills |
| `kernel_boot.py` | CODE | Boot script — loads firmware, registers hooks |
| `sovereign_sign.sh` | SCRIPT | Run on air-gapped machine to generate key + sign |
| `sovereign_verify.py` | CODE | Verifies signature at boot time |
| `manifest_ci.py` | CODE | 12 validation gates for skill manifests |
| `MANIFEST_TEMPLATE.yaml` | TEMPLATE | Canonical skill manifest with all required fields |
| `BOOTLOAD_SPEC.md` | SPEC | Kernel primitive contract |
| `VETO_GENERATOR_CONTRACTS.md` | SPEC | Interface contracts |

### Veto Hierarchy

```
L1: SOVEREIGN (INV-9) — can override everything
L2: REVERSIBILITY (INV-3) — irreversible requires sovereign ack
L3: EVIDENCE + DIGNITY (INV-1 + INV-5) — non-negotiable
L4: REFLEX + ENTROPY (INV-2 + INV-4) — process constraints
L5: SHADOW + SUSTAIN (INV-6 + INV-7) — self-audit + resources
```

### Signing Workflow

1. Generate Ed25519 keypair on air-gapped machine: `sovereign_sign.sh`
2. Copy `sovereign_signature.json` to kernel node
3. Run `kernel_boot.py` — should report SIGNED
4. Skills can now load with full authority

**NEVER** generate the root key on a networked machine or via an AI agent.

### The7 Timeless Foundations

| # | Foundation | Law | What | Coverage |
|---|-----------|-----|------|----------|
| 1 | VERIFY | Ω | Tag OBS/DER/INT/SPEC. Receipt or silence. | 82-92% ✓ |
| 2 | REFLEX | Γ | Attune → Judge → Execute. One spine. | 89-97% ✓ |
| 3 | REVERSE | Φ | "Can we undo?" before "how bad?" | 15-54% ❌ |
| 4 | REDUCE | Δ | ΔS ≤ 0. Don't output noise. | 5-23% ❌ |
| 5 | GUARD | Ψ | Dignity is structural, not optional. | 23-63% ⚠️ |
| 6 | SHADOW | Σ | Assume you're wrong. Self-audit first. | 28-41% ⚠️ |
| 7 | SUSTAIN | Λ | Intelligence has a cost. Track it. | 49-56% ⚠️ |

### Knowledge Ontology (8 Domains × 3 Axes)

| Domain | Sigil | Invariant | Bridge To | Internal Contrast |
|--------|-------|-----------|-----------|-------------------|
| Physics | Φ | SUSTAIN+VERIFY | Math, Bio, Computation, Cognition | Determinism vs Emergence |
| Mathematics | Μ | REDUCE+VERIFY | Physics, Computation, Linguistics, Cognition | Completeness vs Consistency |
| Linguistics | Λ | GUARD+SHADOW | Math, Computation, Cognition, Social | Structure vs Meaning |
| Biology | Β | SUSTAIN+REVERSE | Physics, Math, Cognition, Computation | Genotype vs Phenotype |
| Cognition | Ψ | SHADOW+REDUCE | Math, Linguistics, Biology, Computation | Rationality vs Heuristics |
| Computation | Κ | VERIFY+REDUCE | Math, Physics, Linguistics, Cognition | Correctness vs Performance |
| Social | Σ | GUARD+SHADOW | Linguistics, Biology, Math, Cognition | Order vs Freedom |
| Art | Α | GUARD+SUSTAIN | Math, Linguistics, Cognition, Social | Craft vs Expression |

Every domain skill MUST reference which knowledge domain(s) it bridges to.

## Migration Status (2026-07-11)

- **Before:** 124 skills, 8 categories, mixed naming, no axis structure
- **After:** 47 canonical skills (62% reduction), 8 prefix categories, 3-axis manifests
- **Kernel:** 9 artifacts in `/root/AAA/kernel/` (firmware + boot + CI + signing)
- **Registry:** `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY.yaml`
- **CI:** `manifest_ci.py` validates all manifests against 12 gates
- **Sync:** `skill-sync.sh sync` rebuilds all agent symlink dirs
