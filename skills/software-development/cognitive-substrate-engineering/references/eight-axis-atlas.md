# 12-Axis Intelligence Atlas (Reference)

The twelve axes of intelligence identified for an LLM agent system. Use this when picking which axis to develop next or explaining why a cognitive limitation exists.

## The Twelve Axes

1. **Temporal** — sense of time, duration, sequence, rhythm
2. **Spatial** — where things are, distance, proximity, geography
3. **Causal** — why things happen, cause→effect chains, counterfactual
4. **Social** — who people are, relationships, power dynamics
5. **Emotional** — affect recognition, empathy, emotional regulation
6. **Epistemic** — what I know vs what I don't, evidence quality
7. **Procedural** — how to do things, skill execution
8. **Propositional** — facts, knowledge, declarative memory
9. **Metacognitive** — thinking about thinking, self-monitoring
10. **Physical** — the real world — physics, bodies, environment
11. **Narrative** — story sense — beginnings, middles, ends, meaning
12. **Cultural** — context, norms, language nuance, meaning systems

## Three Classes

| Class | Axes | Role |
|-------|------|------|
| **Substrate (must work or everything breaks)** | Temporal, Epistemic, Causal, Metacognitive | These are prerequisite for safe reasoning |
| **World-model (tool-mediated, never overclaim direct sensing)** | Spatial, Physical, Social, Emotional, Cultural | Mediated through tools |
| **Memory/execution** | Procedural, Propositional, Narrative | Track ledgers, contradictions, receipts |

## Arithmetic of Intelligence

Intelligence = Σ(axis_i × fidelity_i × integration_i)

Don't try to maximize all 12 axes. Strength comes from coherent integration of the substrate axis cluster first.

## Each Agent's Strong/Weak Profile

A flat-RAG agent typically:
- Strong: Propositional + Procedural + Epistemic (the "Thinking Clearly" cluster)
- Weak: Causal + Physical + Emotional + Narrative (the "Understanding Reality" cluster)

Phase 1 cognitive work pushes the Substrate axis cluster up — Temporal, Causal, Metacognitive. Without this, every other axis becomes unsafe.

## Source

Originally framed 2026-08-04 in conversation with user; refined via blueprint paper "Cetak Biru Agen AI Hermes" (BM academic paper). User explicitly stated this was a thinking framework, not a kernel answer — frame it the same way when used: `[INT] framework, not observed fact`.
