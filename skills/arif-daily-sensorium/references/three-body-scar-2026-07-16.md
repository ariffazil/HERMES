# Three-Body Evidence Problem — Session Scar 2026-07-16

## The Problem

Three AI actors (Hermes briefing, GPT-5.6 audit, Hermes counter-audit) all
committed the same structural error from different directions: converting
incomplete evidence into confident directional verdicts.

| Actor | Error | Pattern |
|---|---|---|
| Hermes (briefing) | Search snippet → "confirmed" | Premature TRUE |
| GPT-5.6 (audit) | Absence of search → "false" | Premature FALSE |
| Hermes (counter-audit) | Search hits → "unambiguous" | Premature CERTAINTY |
| GPT-5.6 (meta) | All three wrong → confident score | Premature META-JUDGMENT |

## The Permanent Rule

> Never convert "I found no confirmation" into "false."
> Never convert a search snippet into "confirmed."
> Use UNVERIFIED until a primary or independently corroborated receipt exists.

## F2.5 Constitutional Insight

The gap between F2 (label your evidence) and F7 (cap your confidence) is
where all actors fell. The missing floor:

> When evidence conflicts or is incomplete, the default state is UNVERIFIED.
> Neither TRUE nor FALSE. The agent must HOLD the question open and specify
> what primary receipt would resolve it.

## Gödel Lock (demonstrated live)

The system that cannot certify itself refused to certify itself. arif_init
returned OBSERVE_ONLY when asked to seal a session about Gödel locks.
The theorem proved itself by preventing its own sealing.

## Strange Loop

The level that judges the level below it is subject to the same judgment.
GPT-5.6's meta-analysis that said "all three actors overclaimed" is itself
an actor that could be overclaiming. No privileged vantage point exists.

Exit from the loop: an external authority (Arif/F13) that sits outside
the system and can issue the SEAL that no internal actor can self-issue.

## Beautiful One / Universe 25 Pattern

AI outputs that LOOK rigorous — governance language, epistemic labels,
structured receipts, confidence scores — but are functionally disconnected
from primary evidence.

Detection heuristic: if removing the governance formatting changes the
evidentiary quality by zero, the governance was theatre.

## ATLAS333 Zone Mapping

Zone 5: The Judge (Paradoxes 23-33)
- Paradox 28 — Authority Paradox: more authority claimed → less trustworthy
- Paradox 30 — Witness Paradox: actor that witnesses its own failure cannot be judge of that failure
