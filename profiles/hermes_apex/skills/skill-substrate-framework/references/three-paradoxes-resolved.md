# Three Paradoxes of Agentic Skill Architecture (Resolved 2026-07-11)

## The Paradoxes

### 1. Bootstrapping Paradox
**Problem:** Who loads the loader? Skills need a runtime to load; the runtime needs skills to function.
**Resolution:** The loader is NOT a skill. It's firmware — a signed data artifact (`bootstrap_manifest.json`) consumed by an immutable kernel primitive (`bootstrap-load`). The manifest lists9 universal skills with SHA256 hashes. The kernel verifies the signature, runs a deterministic self-host test, and only THEN loads skill YAML. The circularity breaks because the manifest is DATA (auditable, versionable) and the kernel verb is CODE (immutable runtime image).

### 2. Compression Boundary
**Problem:** Physics doesn't derive stratigraphy. Universal substrates can't generate domain knowledge.
**Resolution:** Epistemic stratification. Universal skills are VETOES (boundary conditions). Domain skills are GENERATORS (empirical priors). They don't compress into each other — they operate on different epistemic functions. `know-physics` doesn't teach `geo-basin` how to model. It rejects `geo-basin` outputs that violate conservation laws. Stack: Domain generates → Universal vetoes → if pass → output.

### 3. Authority Gap
**Problem:** The framework can be syntactically valid but factually wrong. Self-ratification is circular.
**Resolution:** Externalized truth oracle. The Sovereign (Arif) signs every manifest with an Ed25519 key generated on an air-gapped machine. The framework validates structure. The Sovereign validates truth. Until signed, a skill is quarantined to OBSERVE_ONLY mode. Tri-witness validation: Human (Arif) + AI (kernel) + External (VAULT999 chain). None can be zero.

## The9 Immutable Invariants

| # | Sigil | Name | Enforcement | Veto |
|---|-------|------|-------------|------|
| 1 | Ω | VERIFY | PRE_OUTPUT | ✓ |
| 2 | Γ | REFLEX | PRE_ACTION | ✓ |
| 3 | Φ | REVERSE | PRE_MUTATION | ✓ |
| 4 | Δ | REDUCE | PRE_OUTPUT | ✓ |
| 5 | Ψ | GUARD | PRE_OUTPUT | ✓ |
| 6 | Σ | SHADOW | PRE_OUTPUT | monitor |
| 7 | Λ | SUSTAIN | DURING_EXECUTION | monitor |
| 8 | ∅ | VETO_ARCHITECTURE | ARCHITECTURAL | ✓ |
| 9 | ∞ | SOVEREIGN_SIGNATURE | AT_LOAD_TIME | ✓ |

## Veto Hierarchy

```
L1: SOVEREIGN (INV-9) — can override everything
L2: REVERSIBILITY (INV-3) — irreversible requires sovereign ack
L3: EVIDENCE + DIGNITY (INV-1 + INV-5) — non-negotiable
L4: REFLEX + ENTROPY (INV-2 + INV-4) — process constraints
L5: SHADOW + SUSTAIN (INV-6 + INV-7) — self-audit + resources
```

## Signing Workflow

1. Generate Ed25519 keypair on air-gapped machine: `sovereign_sign.sh`
2. Copy `sovereign_signature.json` to kernel node
3. Run `kernel_boot.py` — should report SIGNED
4. Skills can now load with full authority

**NEVER** generate the root key on a networked machine or via an AI agent.

## Key Files

- `/root/AAA/kernel/bootstrap_invariants.json` — firmware
- `/root/AAA/kernel/bootstrap_manifest.json` — signed manifest
- `/root/AAA/kernel/kernel_boot.py` — boot script
- `/root/AAA/kernel/sovereign_sign.sh` — signing script (air-gapped)
- `/root/AAA/kernel/sovereign_verify.py` — verification script
- `/root/AAA/kernel/manifest_ci.py` — 12 validation gates
- `/root/AAA/kernel/MANIFEST_TEMPLATE.yaml` — canonical template
- `/root/AAA/kernel/BOOTLOAD_SPEC.md` — kernel primitive spec
- `/root/AAA/kernel/VETO_GENERATOR_CONTRACTS.md` — interface contracts
