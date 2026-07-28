# AKAL API Reference — Wiring Hooks

## Import Pattern

```python
from arifosmcp.core.akal import (
    score_friction, should_escalate, required_pipeline,  # I1
    emit_shadow, validate_shadow, ShadowTrace, SHADOW_REQUIRED_FIELDS,  # I2
    tag_novelty, enforce_novelty, NoveltyChunk, ChunkType, NOVELTY_THRESHOLD,  # I3
    dual_evaluate, DualVerdict, VerifyResult, JudgeResult, L5A_FIELDS, L5B_FIELDS,  # I4
    blast_class, cooling_requirement, BlastClass, LatencyRequirement,  # I5
    FrictionLevel, FrictionResult,
)
from arifosmcp.core.akal_wiring import (
    akal_pre_think,      # 333_MIND entry
    akal_post_critique,  # 555_HEART exit
    akal_pre_forge,      # 777_FORGE entry
    akal_pre_judge,      # 888_JUDGE entry
    akal_pre_seal,       # 999_VAULT entry
)
```

## I1 — Friction Scoring (333_MIND)

```python
result = score_friction(
    query="...",
    blast_radius="low"|"medium"|"high"|"irreversible",
    has_prior_receipts=True,
    cross_organ=False,
    context_complexity=0.0,
)
# result.score: float [0,1]
# result.level: FrictionLevel.LOW|MEDIUM|HIGH|CRITICAL
# result.escalation_required: bool
# result.required_depth: "fast"|"standard"|"deep"|"full_ascent"
# result.signals: dict[str, float]

escalate = should_escalate(result)  # bool
pipeline = required_pipeline(result)  # list[str] e.g. ["L1","L2","L3","L4","L5a","L5b"]
```

## I2 — Shadow Observer (555_HEART)

```python
trace = emit_shadow(
    assumptions=["System is stable"],
    missing_data=["No rollback plan"],
    shortcuts=["Skipped staging"],
    likely_biases=["Confirmation bias"],
    tribal_frames=["Corporate framing"],
    confidence=0.7,
)
# trace.valid: bool
# trace.violations: list[str]
# trace.is_empty(): bool — True if all fields empty (schema violation)

validated = validate_shadow(trace)  # same trace, violations populated
```

Required fields: assumptions, missing_data, shortcuts, likely_biases, tribal_frames.
Generic answers ("none", "n/a", "no assumptions") are flagged as violations.

## I3 — Novelty Detection (777_FORGE)

```python
chunks = [
    NoveltyChunk("According to the spec...", ChunkType.DERIVED),
    NoveltyChunk("A new framework that maps...", ChunkType.SYNTHESIZED),
]
result = tag_novelty(chunks)
# result.verdict: "PASS"|"INSUFFICIENT"|"REGURGITATION"
# result.synthesized_ratio: float [0,1]
# result.novelty_pass: bool

action = enforce_novelty(result)
# "PROCEED" | "SECOND_PASS" | "HOLD"
```

Thresholds: NOVELTY_THRESHOLD=0.20 (≥20% SYNTHESIZED), REGURGITATION_CEILING=0.90 (>90% DERIVED = HOLD).

## I4 — Dual Evaluation (888_JUDGE)

```python
dual = dual_evaluate(
    coherence=0.9,
    evidence_validity=0.8,
    logic_consistency=0.85,
    reasoning_chain=["step1", "step2"],
    blast_radius="irreversible",
    harm_assessment="No direct harm",
    dignity_impact="Neutral",
    long_term_consequences="Permanent",
    value_alignment="Aligned with F1-F13",
    floors_checked=["F1", "F2", "F6", "F13"],
)
# dual.verify.pass_l5a: bool — agent verification
# dual.judge.sovereign_required: bool — True for HIGH/IRREVERSIBLE
# dual.dual_pass: bool — True only if both pass
```

L5a thresholds: coherence<0.7 → fail, evidence_validity<0.6 → fail, logic_consistency<0.7 → fail.

## I5 — Latency Enforcement (999_VAULT)

```python
bc = blast_class("irreversible")  # BlastClass enum
req = cooling_requirement(bc)     # LatencyRequirement
# req.min_passes: int (IRREVERSIBLE=3)
# req.requires_branching: bool (IRREVERSIBLE=True)
# req.requires_cooling: bool (IRREVERSIBLE=True)
# req.cooling_seconds: float (IRREVERSIBLE=300)
# req.requires_second_look: bool (IRREVERSIBLE=True)
```

## Wiring Hooks (akal_wiring.py)

```python
# I1 — at entry of arif_think
r = akal_pre_think(query, blast_radius="low")
# r["friction"], r["must_escalate"], r["pipeline"], r["cognitive_level"]

# I2 — after arif_critique
r = akal_post_critique(assumptions=[], missing_data=[], shortcuts=[], likely_biases=[], tribal_frames=[])
# r["trace"], r["valid"], r["violations"]

# I3 — before arif_forge(mode=generate)
chunks = [NoveltyChunk("...", ChunkType.SYNTHESIZED)]
r = akal_pre_forge(chunks)
# r["novelty"], r["action"], r["can_forge"]

# I4 — before arif_judge
r = akal_pre_judge(coherence=0.9, evidence_validity=0.8, logic_consistency=0.85, reasoning_chain=[], blast_radius="irreversible")
# r["dual"], r["can_verdict"], r["requires_sovereign"]

# I5 — before arif_seal
r = akal_pre_seal("irreversible")
# r["blast_class"], r["cooling_required"], r["cooling_seconds"], r["requires_branching"], r["requires_second_look"], r["can_seal_immediately"]
```

## Constants

```python
NOVELTY_THRESHOLD = 0.20       # ≥20% SYNTHESIZED required
REGURGITATION_CEILING = 0.90   # >90% DERIVED = HOLD
FRICTION_ESCALATION = 0.60     # ≥this → deep pipeline
FRICTION_CRITICAL = 0.80       # ≥this → full ascent + sovereign
SHADOW_REQUIRED_FIELDS = ["assumptions", "missing_data", "shortcuts", "likely_biases", "tribal_frames"]
L5A_FIELDS = ["coherence", "evidence_validity", "logic_consistency", "reasoning_chain"]
L5B_FIELDS = ["harm_assessment", "dignity_impact", "long_term_consequences", "value_alignment"]
```
