# DarkGeometryDetector — WELL Implementation

> Python module: `WELL/gate/darkgeometrydetect.py`
> Tests: `WELL/tests/test_darkgeometrydetect.py`
> Built: 2026-07-12

## What It Is

Lexicon-based regex pattern detector for 4 dark geometry collapse modes.
Mirror, not judge — surfaces signals and reflection prompts, never labels people.
v1 heuristic; LLM-assisted detection is future work.

## Detection Modes → Collapse Indicator Mapping

| Detector Mode | Maps to Indicator(s) | What It Matches |
|---|---|---|
| JUDGMENT_COLLAPSE | #1 (confidence ↑ evidence ↓), #2 (correction rejected) | Certainty creep without evidence markers + correction dismissal |
| SELF_CERTIFIED_NIAT | #6 (intention self-certified) | Niat-as-shield phrases AFTER criticism, not before action |
| RESPONSIBILITY_LAUNDERING | #5 (consequences absorbed), #9 (responsibility dissolves) | Agentless constructions + passive voice in harm contexts |
| FORGETTING_YOU_CAN_BE_WRONG | #1 + #3 (frame lock) | High certainty + low epistemic humility + self-referential grounding |

## Architecture

### Lexicons (6 sets, all pre-compiled regex)

- `CERTAINTY_LEXICON` (10 phrases): definitely, obviously, clearly, certainly, without doubt, no question, absolutely, I know, guaranteed, undeniable
- `UNCERTAINTY_LEXICON` (10 phrases): maybe, perhaps, possibly, I could be wrong, I'm not sure, it seems, arguably, potentially, I think, might
- `NIAT_SHIELD_LEXICON` (8 phrases): my intention was good, I know my heart, God knows my niat, I know my own niat, my niat is pure, I meant well, my intention was, I was trying to
- `AGENTLESS_PATTERNS` (11 regex): passive voice constructions (mistakes were made, it was decided, things happened, etc.)
- `CORRECTION_REJECTION` (5 phrases): you don't understand, that's irrelevant, you're missing the point, etc.
- `SELF_REFERENCE_AS_PROOF` (5 phrases): trust me, I know because I know, believe me, I just know, I feel it in my heart

### Context Gates (critical design choice)

Signals are only significant when paired with the right context:

- **Niat shield** requires `CRITICISM_MARKERS` present → otherwise benign use of niat language
- **Agentless construction** requires `HARM_MARKERS` present → otherwise passive voice about non-harmful events
- **Certainty creep** reduced by `EVIDENCE_MARKERS` (data shows, evidence, measured, etc.)
- **No hedging** reduced by `UNCERTAINTY_LEXICON` markers

Without these gates, the detector would false-positive on normal language.

### Confidence Formula

```
raw = 1 - (1 / (1 + signal_count))
reduction = min(0.8, negative_markers * 0.2)
confidence = max(0.0, raw - reduction)
confidence = min(confidence, 0.95)  # never 1.0
```

Multiplicative: more signals → higher confidence. Negative markers (evidence, uncertainty) reduce it.
Capped at 0.95 because absolute certainty is itself a collapse signal.

### Status Thresholds

- `CLEAR`: confidence < 0.15
- `REFLECT`: 0.15 ≤ confidence < 0.5
- `ATTENTION`: confidence ≥ 0.5

## CLI Usage

```bash
python gate/darkgeometrydetect.py "text to analyze"
python gate/darkgeometrydetect.py --file conversation.txt
python gate/darkgeometrydetect.py --json "text"
```

## Design Principles (Non-Negotiable)

1. Mirror, not judge. Reflection prompts, not verdicts.
2. Never label people. Only surface patterns.
3. Never infer intention. Only observe language patterns.
4. Human can say "this is wrong" and the system holds.
5. All detections are advisory, not identity.
6. Confidence never reaches 1.0.

## Pitfalls

1. **False positives on normal language.** The context gates (criticism for niat, harm for agentless) are essential. Removing them breaks the detector.
2. **English-only v1.** Non-English text returns CLEAR. Malay/Arabic lexicons are future work.
3. **Lexicon drift.** Phrases like "I know" are ambiguous — context gate (no evidence markers) handles this, but review if false positives increase.
4. **Status thresholds may need tuning.** Initial session showed borderline cases landing in ATTENTION rather than REFLECT. The thresholds (0.15/0.5) are calibrated for low false-positive rate, not high sensitivity.

## Extension Points

- Add Malay lexicons (`NIAT_SHIELD_LEXICON` already has "niat" in Malay)
- Add LLM-assisted detection for context understanding beyond regex
- Add Mode 5: SCALE HIDES CONSEQUENCE (indicator #10) — automated harm at scale
- Wire into WELL MCP server as `well_detect_dark_geometry` tool
