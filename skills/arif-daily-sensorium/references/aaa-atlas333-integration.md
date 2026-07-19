# AAA · Atlas333 · VAULT999 Integration

## When to activate

This layer activates when the briefing encounters **genuine epistemic tension** — not every section, only when:
- two credible sources contradict on a load-bearing claim;
- the briefing's central thesis depends on an UNK;
- a causal chain crosses multiple organ boundaries;
- the same pattern was observed in a previous session.

Do not force Atlas333 activation on routine briefings. It is for contradiction, not decoration.

## Atlas333 paradox mapping

When tension is detected, identify which paradox axis is activated. Use `arifos://atlas333/paradox/list` (if available) or reference these:

| ID | Paradox | Organ | When it fires |
|---|---|---|---|
| 5 | epistemic hunger vs. discipline | memory | Wanting to produce signal before evidence supports it |
| 10 | humility vs. paralysis | memory | UNK on the dominant story — can't release, can't hold forever |
| 12 | confidence vs. competence | mind | Presenting analysis with authority beyond evidence quality |
| 13 | epistemic vs. pragmatic certainty | mind | Need a decision but evidence is uncertain |
| 18 | false negative vs. false positive | mind | "Not found" treated as "false" OR snippet treated as "confirmed" |
| 19 | metacognition vs. meta-uncertainty | mind | Audit of audit — more self-reference without more evidence |
| 26 | comprehensiveness vs. decidability | judge | Comprehensive briefing that can't be acted on |
| 33 | expertise vs. authoritarianism | judge | Technical confidence overriding sovereign judgment |

Map 1-3 paradoxes per tension. Do not map all 33.

## EUREKA capture

When a contradiction resolves into genuine new structure (not just "we don't know"), compose an EUREKA777 entry:

```
id: eureka-<uuid12>
session_id: sensorium-<date>
contradiction_class: 1-8 (see below)
ladder_state: TENSION → CONTRADICTION → COMPRESSION_FAILURE → EUREKA
commitment_a: "first position"
commitment_b: "second position"
why_old_frame_failed: "why existing frame can't absorb this"
new_structure: "the insight"
paradox_axis_ids: [list from above]
affected_stage: 555 (judge)
```

Contradiction classes:
1. factual — two sources disagree on what happened
2. temporal — event date vs announcement date vs effective date
3. causal — A→B chain disputed
4. scope — "30 countries" means what exactly?
5. method — how to verify is itself disputed
6. authority — who gets to declare this true?
7. frame — the category itself is wrong
8. godel — the system can't certify its own claim

Store at `/root/.local/share/arifos/atlas333/eureka/sensorium-<date>.json` if writable. Otherwise log in briefing output.

## VAULT999 seal path

When a briefing is released (RELEASE or RELEASE_WITH_HOLDS) and contains a structural insight worth preserving:

1. Compose a seal payload with: session_id, evidence_layer, verdict, material_unknowns, key claims with labels
2. Offer to Arif: "Seal this briefing to VAULT999?"
3. If Arif confirms → route through arif_seal with ack_irreversible=true
4. If Arif declines → no seal, no pressure

**Gödel Lock rule:** The sensorium cannot self-seal. The briefing agent is the author, not the witness. Only the sovereign (F13) or a tri-witness (H+M+E ≥ 0.70) can seal.

## Beautiful Mouse detection

Before releasing, check for **epistemic theatre**:
- Are governance labels (OBS/DER/INT) attached to claims that weren't actually verified?
- Does the briefing LOOK more rigorous than the evidence supports?
- Is the form (structure, tables, labels) doing work that the substance (sources, receipts) should be doing?
- Would removing all the labels reveal weak evidence dressed in strong formatting?

If yes → downgrade to HOLD or RELEASE_WITH_HOLDS and name the theatre.

## Universe 25 warning

If the briefing is the Nth consecutive briefing on the same topic with no new primary evidence, flag:
> "Same evidence pool as [previous date]. Recycled signal risk."

The sovereign needs ground truth, not increasingly polished versions of the same web search results.

## AAA governance integration

When arifOS MCP tools are available:
- `arif_observe` (111) — use for structured web search with evidence labeling
- `arif_think` (333) — use for structured reasoning when causal chains are complex
- `arif_judge` (888) — use ONLY when Arif explicitly requests governance clearance
- `capital_market` — use for live price data (gold, oil, FX)
- `capital_health` — use for fiscal/economic analysis

When not available, continue with public evidence. Never block on missing tools.
