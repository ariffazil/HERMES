# Datapack Gap Filling — Method for Systematic Knowledge Completion

> **Purpose:** After an initial research deliverable, identify specific knowledge gaps and fill them with targeted searches. Prevents "I know 80% but the 20% I'm missing changes the conclusion."

---

## When to Use

- After completing a financial deep-dive, identify what data you COULDN'T find
- When management narrative omits specific metrics (subsidiary PAT, capex breakdown, fiscal dependency)
- When user asks "what are you missing?" or "fill the gaps"
- When a prediction has high uncertainty that could be reduced with specific data

## Method

1. **List gaps explicitly.** After initial deliverable, create a gap list:
   - What numbers are estimated, not observed?
   - What narratives lack supporting data?
   - What subsidiary/segment data is undisclosed?
   - What external dependencies (court rulings, policy changes) are unquantified?

2. **Prioritize by impact.** Which gaps, if filled, would change the conclusion?
   - HIGH: Changes the headline number by >10%
   - MEDIUM: Changes segment breakdown or risk assessment
   - LOW: Adds context but doesn't change conclusion

3. **Targeted search per gap.** Each gap gets a specific search query:
   - Don't search broadly — search for the exact missing number
   - Use multiple angles: official reports, Reuters, analyst notes, government statements
   - Tag each finding OBS/DER/INT/SPEC

4. **Reconcile with existing model.** New data may confirm, modify, or invalidate the original estimate. Update the model and note the delta.

5. **Deliver as structured JSON.** Gap ID → question → answer → sources → epistemic class.

## Output Format

```json
{
  "gap_id": {
    "question": "What is X?",
    "status": "ANSWERED / CONFIRMED NEVER DISCLOSED / PARTIALLY ANSWERED",
    "answer": {
      "key_metric": "value",
      "context": "explanation",
      "sources": ["url1", "url2"],
      "epistemic_class": "OBS / INT / DER / SPEC"
    }
  }
}
```

## Proven Example

2026-07-13: PETRONAS datapack gaps — 4 gaps filled:
1. Dividend cut reason (RM 320k → RM 200k): NONE given by management. OBS from Malaysiakini.
2. Gentari standalone PAT: CONFIRMED NEVER DISCLOSED. Inferred ~RM -1.0 to -1.25bn/year from Corp & Others.
3. Fiscal dependency: PM says "5-6%" on dividend alone. Total contribution = 19.7% of federal revenue. OBS from Finance Ministry.
4. Petros-Sarawak court status: Federal Court allows leave for constitutional reference, no ruling date. OBS from NST, Borneo Post.

Each gap changed the analysis: dividend cut = responsible shareholder; Gentari = hidden drag; fiscal = misleading framing; Petros = unresolved binary risk.

## Pitfalls

- **Don't stop at "not found."** If a number is genuinely undisclosed, that's a finding. "Never disclosed" is an answer.
- **Don't mix estimated and observed.** If you infer a number from a proxy, label it INT, not OBS.
- **Don't fill gaps with assumptions.** If you can't find the number, say so. An unfilled gap is better than a fabricated one.
