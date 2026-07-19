# Structured Datapack Pattern

**version:** v0.1
**created:** 2026-07-09
**provenance:** PETRONAS fiscal stress analysis session

## When to Use

When building financial, institutional, or economic models from mixed sources (public data + user input + derived computations).

## Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "[Entity] Datapack [year range]",
  "version": "v0.1",
  "created": "YYYY-MM-DD",
  "created_by": "agent name",
  "evidence_layer": "PUBLIC_VERIFIED | MIXED | DERIVED",
  "note": "Human-readable description of what this pack is and isn't.",
  "yearly_data": [
    {
      "year": 2021,
      "fiscal_year": "FY2021",
      "source": "Entity Annual Report 2021 + News Outlet",
      "source_url": "https://...",
      "metric_a": 123.4,
      "metric_b": null,
      "confidence": "L3",
      "notes": "Context about gaps or special circumstances."
    }
  ],
  "computed_trends": {
    "trend_name": "description of how to compute",
    "key_insight": "plain English interpretation"
  },
  "key_observations": [
    "Bullet-point insights that emerge from the data."
  ],
  "source_ledger": [
    {
      "source": "Entity Annual Report 2021",
      "url": "https://...",
      "date": "2022-02",
      "figures": "Revenue X, PAT Y",
      "confidence": "OBS"
    }
  ],
  "next_required_actions": [
    "Specific gaps to fill next."
  ],
  "requires_refresh_after_days": 90
}
```

## Rules

1. **Never mix evidence layers in the same field.** Each metric is either PUBLIC_VERIFIED, USER_SUPPLIED, or DERIVED.
2. **Null for gaps.** Don't guess. Use `null` and explain in notes.
3. **Every year gets a source_url** (or null with explanation).
4. **Confidence tag per year:** OBS (direct from audited report), L3 (reported by reputable outlet), L4 (user-supplied), DER (computed), SPEC (speculative).
5. **Source ledger is mandatory.** Every figure must trace back to a source.
6. **Computed trends section explains the math.** Don't hide calculations in prose.
7. **next_required_actions lists what's missing.** This becomes the checklist for the next iteration.

## Pitfalls

- Don't fill nulls with plausible-looking values. Null is honest; a guess is dangerous.
- Don't claim confidence higher than the weakest source in the chain.
- Don't mix FY22 peak with normal years without flagging the anomaly.
- Don't skip the source_ledger. Without it, the datapack is just numbers.

## Example

See `/root/A-FORGE/forgework/petronas_datapack_2021_2025.json` for a worked example.
