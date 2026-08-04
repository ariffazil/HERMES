# Cognitive Intelligence Upgrade — Phase 1

This directory contains the first cognitive-intelligence layer for Hermes Agent. It is deliberately small, deterministic, and dependency-light so it can run inside the Hermes edge bridge without requiring a heavy inference stack.

## Modules

### 1. `memory_decay/`

Interaction-count-based Ebbinghaus forgetting with a multi-factor memory-value model.

- Effective decay: `Ω_eff(Δn) = Ω · exp(-λ · Δn · μ(Ω))`
- Value score: `V(m) = Σ wᵢ fᵢ(m)`
- Inertia: `μ(Ω) = 1 - η · V(m)`
- Recall reinforcement: `S_new = S_old · (1 + ln(1 + recall_count))`
- Hierarchy: `STM (32-bit) → MTM (8-bit) → LTM (4-bit) → ARCHIVE (2-bit)`
- Quantization changes precision only; it does not delete a memory.

The module uses a canonical interaction counter. It does not use wall-clock time, which makes tests reproducible and avoids paused-session/system-clock effects.

### 2. `causal_tagger/`

A lightweight regex-based causal-language detector for English and Bahasa Melayu. It classifies claims using the arifOS evidence taxonomy:

- `OBS_CAUSAL`: trace/log/measurement evidence
- `DER_CAUSAL`: multiple-source derivation
- `INT_CAUSAL`: single-source inference
- `SPEC_CAUSAL`: no evidence marker
- `UNKNOWN`: no causal cue detected

The optional spaCy integration was intentionally not made mandatory. Regex cue detection is the minimum viable real-time path; formal causal graph packages such as DoWhy are outside Phase 1 scope.

### 3. `drift_monitor/`

Semantic output-vs-intent drift detection using cosine distance:

- `≤ 0.30`: `STABLE`
- `> 0.30`: `DRIFT_WARNING`
- `> 0.50`: `DRIFT_ALERT`

The preferred backend is `sentence-transformers` with `all-MiniLM-L6-v2`. If it is unavailable, the module automatically falls back to a deterministic pure-Python TF-IDF embedder. The last five scores are retained by default to provide a trend: `IMPROVING`, `STABLE`, `WORSENING`, or `INSUFFICIENT_DATA`.

## Shared receipt contract

Every compute/detect operation emits a `cognitive.receipt.Receipt`. Receipts contain:

```json
{
  "receipt_id": "rcpt-...",
  "module": "memory_decay | causal_tagger | drift_monitor",
  "operation": "...",
  "timestamp": "ISO-8601 UTC",
  "evidence_type": "OBS | DER | INT | SPEC | UNKNOWN",
  "confidence": 0.0,
  "verdict": "COMPUTED | DETECTED | DRIFT_SIGNAL | UNKNOWN",
  "data": {},
  "source": "...",
  "meta": {}
}
```

Confidence is always capped at `0.90` by the receipt layer. These are evidence receipts, not constitutional seals. Integration with arifOS should route receipts through the appropriate `forge_receipt_draft`/memory path; irreversible memory mutations still require F1 + 888 JUDGE handling.

## Usage

From `/root/HERMES`:

```python
from cognitive.memory_decay import MemoryDecayEngine, MemoryItem

memory = MemoryItem(
    memory_id="goal-1",
    content="User's active deployment goal",
    goal_relevance=1.0,
    task_utility=0.9,
    strength=1.0,
    last_interaction=10,
)
result = MemoryDecayEngine().compute(memory, current_interaction=25)
print(result.tier, result.effective_strength)
print(result.receipt.to_json())
```

```python
from cognitive.causal_tagger import classify_claim

result = classify_claim("The service failed because the disk was full")
print(result["evidence_type"], result["confidence"])
print(result["receipt"])
```

```python
from cognitive.drift_monitor import DriftMonitor

monitor = DriftMonitor("deploy the application")
signal = monitor.compute("write a recipe for banana bread")
print(signal.drift_level, signal.recommendation)
```

## Tests

The complete suite is runnable with the requested command:

```bash
cd /root/HERMES
python -m pytest cognitive/tests/ -v
```

## Dependencies

The core package uses only Python's standard library. `pytest` is required for tests. `sentence-transformers` is optional and only needed for the higher-quality embedding backend; the TF-IDF fallback is automatic.

## Research alignment

The implementation follows `/root/HERMES/scratch/research_brief_phase1_validation.md`:

- interaction count instead of wall-clock decay;
- multi-factor memory value scoring;
- logarithmic recall reinforcement;
- regex causal cues rather than DoWhy;
- embedding distance rather than runtime MetaCrit;
- receipts as observable evidence, with governance left to arifOS.
