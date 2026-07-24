# AAA Skill Architecture — Session 2026-07-11

Full architectural work from the skill unification session.

## Problem: 149 skills, no structure

- Mixed naming (UPPER_CASE, kebab-case, emoji prefixes)
- No axis structure (invariant/bridge/contrast)
- 3 paradoxes: bootstrapping, compression boundary, authority gap
- Duplicates across Claude/Codex/Grok/Kimi/OpenCode

## Solution: 3 layers × 3 axes

### Layer 1: 6 Substrate Skills (how agents think)

| Skill | Kernel Verb | Purpose |
|-------|-------------|---------|
| kernel-bind | arif_init, arif_judge | Session governance binding |
| observe-ground | arif_observe | Evidence before narrative |
| route-dispatch | arif_route | Right organ for right intent |
| memory-manage | arif_memory | Memory lifecycle discipline |
| verify-gate | arif_verify, arif_critique | 4-gate verification |
| audit-seal | arif_seal, arif_compose | Decision logging and sealing |

### Layer 2: 3 Knowledge Foundations (what agents know)

| Skill | Covers | Why universal |
|-------|--------|---------------|
| know-physics | mechanics, thermo, QM, info theory | All reality claims are physical |
| know-math | probability, algebra, optimization, logic | All computation is mathematical |
| know-language | semantics, pragmatics, discourse | All human interface is linguistic |

### Layer 3: ~54 Domain Modules (where agents operate)

geo(7), wealth(3), well(2), forge(2), dev(8), ops(12), meta(9), a2a(4), sec(2), research(3), kernel(2)

## Three Paradoxes and Resolutions

### 1. Bootstrapping Paradox

**Problem:** Loader needs skills; skills need loader.
**Resolution:** Firmware, not skill. `kernel-bind` is injected as immutable System Primitive at instantiation. Bootstrap manifest (JSON data, not executable code) lists 9 skills with SHA256 hashes, signed by sovereign Ed25519 key. Kernel primitive `bootstrap-load` verifies signature + hashes before loading any YAML.

### 2. Compression Boundary

**Problem:** Physics doesn't derive stratigraphy. Boundary is lossy.
**Resolution:** Veto, not compression. Universal skills are VETO layers (boundary conditions). Domain skills are GENERATORS (empirical priors). Sequential: domain generates → universal vetoes → sovereign ratifies. Scope tags: {global|regional|local}, evidence tags: {theory|empirical|simulation}.

### 3. Authority Gap

**Problem:** Framework validates syntax, not truth.
**Resolution:** Externalize. Sovereign signs the truth. 3-party quorum (kernel steward + governance council + external attester). Ratification hash: sha256(manifest + sovereign_signature + timestamp). Until signed, skill quarantined.

## Artifacts Produced

| File | Purpose |
|------|---------|
| BOOTSTRAP_MANIFEST.json | Signed manifest (9 skills, hashes, root keys) |
| BOOTSTRAP_LOAD_SPEC.json | 7-step kernel primitive spec |
| CI_VALIDATION_GATES.json | 10 gates + 4 canary tests |
| SKILL_MANIFEST_TEMPLATE.json | Canonical schema for all skills |
| VETO_GENERATOR_CONTRACT.json | Knowledge boundary resolution |
| META_GOVERNANCE.json | Quorum + adversarial + cadence |
| BLINDSPOT_AGENTS.json | 3 meta-governance agents |
| FEDERATED_SKILLS_REGISTRY_V3.yaml | 63 canonical skills |

## Key Commands

```bash
# Re-sign manifest after changes
bash /root/AAA/scripts/sign-manifest.sh

# Check registry
cat /root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml

# Verify manifest signature
python3 -c "
import json, hashlib, base64
from cryptography.hazmat.primitives.serialization import load_ssh_public_key
with open('/root/AAA/skills/BOOTSTRAP_MANIFEST.json') as f:
    m = json.load(f)
with open('/root/.secrets/bootstrap/root-arif-888.pub') as f:
    pk = load_ssh_public_key(f.read())
sig = base64.b64decode(m['signatures'][0]['signature'])
pk.verify(sig, m['content_hash'].encode())
print('✅ Manifest signature valid')
"
```

## Count: 124 → 63 skills (50% reduction)
