# Evidence Protocol

## Verification Escalation

For every load-bearing claim:

1. Locate the primary record or official source.
2. Confirm the event date separately from the article publication date.
3. Seek an independent corroborating report.
4. Search the local language and exact named entities when relevant.
5. Open the underlying page; do not rely on the search-result snippet.
6. Check whether the page describes a plan, allegation, prediction, announcement, or completed event.
7. Record unresolved gaps as `UNK`.

## Absence Is Not Falsity

Use these states:

- `OBS`: evidence supports the claim.
- `OBS — contradicted`: authoritative evidence directly disproves the claim.
- `UNK — not verified`: the search did not establish the claim.

Never write "false" merely because current search failed to locate confirmation.
To call a claim false, require contradictory evidence, an impossible chronology,
an official denial, or a definitive authoritative record.

**Session scar (2026-07-16):** GPT-5.6 declared "no 2026 Johor election" based
on absence from search. The election occurred July 11, 2026. Absence from search
≠ absence in reality.

## Snippet Discipline

A snippet may be stale, generated, truncated, misattributed, or detached from
the underlying page. Use it only to discover the source. Open and inspect the
source before upgrading the claim.

## Date Discipline

Distinguish:

- event date;
- announcement date;
- publication date;
- effective date;
- scheduled date;
- market observation timestamp.

For elections, check early dissolution and by-election possibilities before
citing the ordinary term deadline.

## Number Discipline

For every important number, verify:

- exact value or stated range;
- unit and currency;
- period and base year;
- denominator;
- nominal versus real;
- seasonally adjusted versus unadjusted;
- estimate, forecast, preliminary, revised, or final status;
- instrument and contract for market prices.

## Event-Conflation Test

Before merging reports, ask:

- Are these the same meeting, programme, coalition, strike, or announcement?
- Does "30 countries" mean participants, signatories, leaders, delegations, or supporters?
- Did separate announcements occur on the same day?

Preserve category distinctions rather than forcing a single count.

## AI Release Protocol

For model, API, dataset, benchmark, or pricing claims:

1. Seek the vendor's official documentation, model page, system card, pricing page, release notes, or repository.
2. Verify public availability separately from announcement.
3. Distinguish developer access, research preview, regional rollout, and general public access.
4. Treat benchmark claims as vendor-reported unless independently reproduced.
5. Label secondary reports `DER` or `UNK` when primary confirmation is absent.

## Causal-Chain Protocol

Write causal analysis as a visible chain:

`Hormuz disruption [OBS] → freight and crude pressure [DER] → Malaysian product and subsidy exposure [DER] → household and political pressure [INT]`

Do not collapse producer revenue, government revenue, consumer cost, currency
effects, and political consequences into one phrase such as "Malaysia benefits."

## Beautiful One Detection (2026-07-16 Scar)

When an AI output contains governance language (epistemic labels, structured
receipts, confidence scores, verdicts) BUT the underlying evidence is only
search snippets without primary receipts — the output is a Beautiful One.

Detection heuristic: if removing the governance formatting changes the
evidentiary quality by zero, the governance was theatre.
