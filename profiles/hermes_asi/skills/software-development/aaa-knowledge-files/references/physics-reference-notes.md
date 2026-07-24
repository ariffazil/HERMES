# Physics Band: Gold Standard Reference

The physics band at `/root/AAA/knowledge/physics/` is the canonical depth benchmark for AAA knowledge domain files. When creating or enriching another band, use physics as the quality template.

## Depth Benchmarks

| Metric | Physics target | Acceptable minimum |
|--------|---------------|-------------------|
| Description length | 3-4 sentences | 2 sentences |
| Axioms | 5-8 | 5 |
| Reasoning patterns | 4-6 | 4 |
| Boundary conditions | 3-5 | 3 |
| File size | 2,000-2,300 bytes | 1,800+ bytes |
| Named theorems | 80%+ of axioms | 60%+ |

## Current Physics Files (Reference)

| File | Bytes | Domain |
|------|-------|--------|
| `000-foundational-axioms.json` | 1,073 | Epistemology, logic, first principles |
| `100-classical-mechanics.json` | 818 | Newtonian mechanics (small — may need enrichment) |
| `133-thermodynamics.json` | 2,290 | Thermodynamics, statistical mechanics |
| `200-electromagnetism.json` | 2,206 | EM theory, Maxwell's equations |
| `233-quantum-mechanics.json` | 2,259 | Quantum theory |
| `266-particle-physics.json` | 2,042 | Particle physics, standard model |
| `300-relativity.json` | 2,154 | Special and general relativity |
| `333-geophysics.json` | 2,141 | Earth physics |
| `366-astrophysics.json` | 2,081 | Stellar and galactic physics |
| `399-condensed-matter.json` | 2,231 | Solid state, materials |
| `400-nuclear-physics.json` | 2,167 | Nuclear physics |

## Key Axiom Quality Patterns from Physics

Physics axioms demonstrate the expected depth:

- **Named phenomena** ("Wien's displacement law", "Planck's law", "Pauli exclusion principle")
- **Mathematical formulations** ("∇·B = 0, ∇×E = -∂B/∂t" — Maxwell's full equations)
- **Empirical facts with numbers** ("Speed of light c = 299,792,458 m/s is invariant")

When writing axioms for any domain, match this specificity. Avoid:
- ❌ "Functions can be studied" → ✓ "Cauchy integral formula: f(z₀) = (1/2πi)∮ f(z)/(z-z₀) dz"
- ❌ "Continuous things can be analyzed" → ✓ "Brouwer fixed-point theorem: every continuous map f: Dⁿ → Dⁿ has a fixed point"

## Organs Used in Physics

Physics files reference `arifOS` and `GEOX` primarily. The organ assignment reflects real-world usage — geophysics goes to GEOX, nuclear to arifOS. Match organ assignments to actual federation organ responsibilities.
