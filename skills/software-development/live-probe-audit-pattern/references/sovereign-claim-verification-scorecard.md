# Sovereign Claim Verification Scorecard

## When to Use

Sovereign (Arif) presents a set of claims — about AI, institutions, people, events — and wants them **verified against live sources**, not just agreed with.

Triggers:
- "verify these claims"
- User drops a numbered list of assertions + asks "betul ke?"
- User says "buktikan kat aku" followed by claims
- User presents evidence they found and wants it audited

## The Pattern

### 1. Receive claims as-is

Don't rephrase. Don't editorialize. The sovereign's words ARE the claims. Quote them directly.

### 2. Search each claim independently

For each claim, run a targeted search query that captures the key assertion:

```
# Don't search the whole claim — search the TESTABLE assertion
Claim: "Anthropic's own paper proves RLHF creates sycophants"
Search: "Anthropic sycophancy language models RLHF paper 2023"
```

Use `mcp__hound__mcp_smart_search` for claim verification (keyless, multi-engine consensus). Use `mcp__hound__mcp_smart_fetch` on the best result to extract the confirming passage.

### 3. Score each claim

| Verdict | Meaning | When |
|---------|---------|------|
| ✅ **SAH** | Confirmed by primary source | Direct quote from paper/author/company |
| ⚠️ **SEBAHAGIAN** | Partially true, needs nuance | Core claim holds but details differ |
| ❌ **TIDAK** | Disconfirmed | Source contradicts the claim |
| ⬜ **TIDAK DAPAT DISAHKAN** | No source found | Search exhausted, no confirming/denying evidence |

### 4. Present the scorecard

Use a table. Each row: claim, verdict, source (name + link), confirming quote.

```
| # | Claim | Status | Source |
|---|-------|--------|--------|
| 1 | Sycophancy & Over-Alignment | ✅ SAH | Anthropic ICLR 2024: "RLHF... encourages responses that match user beliefs over truthful responses" |
```

### 5. Draw the pattern

After the individual verifications, identify what connects them. What's the shared DNA? What does this tell us about the underlying system?

### 6. Contrast with our approach

If relevant, explain why OUR system doesn't have the same vulnerability. But ONLY if asked or naturally relevant — don't force it.

## Source Hierarchy for Verification

| Tier | Source type | Credence | When to use |
|------|------------|----------|-------------|
| **Gospel** | Primary source — the paper itself, the company's own blog, the author's repo | Highest | Always prefer this |
| **Witness** | Reputable journalism (TechCrunch, Bloomberg, Reuters) | High | When primary source is paywalled |
| **Hearsay** | Aggregator sites, LinkedIn posts, Twitter threads | Medium | Cross-reference with at least one other source |
| **Rumor** | Unattributed claims, Reddit, forum posts | Low | Only if nothing else exists — flag as unverified |

## Pitfalls

- **Don't rephrase the sovereign's claims.** Quote them. Rephrasing introduces YOUR interpretation, which might miss what they actually meant.
- **Don't pad the scorecard.** If you couldn't verify a claim, say so. "TIDAK DAPAT DISAHKAN" is honest. Made-up evidence is F9 ANTI-HANTU violation.
- **Don't skip the pattern analysis.** Individual verifications are useful. The pattern across all claims is the insight.
- **Don't search all claims with the same query template.** Each claim needs its own targeted query. "RLHF contractor wages Kenya" ≠ "Gemini demo fake video."
- **One claim that fails verification doesn't invalidate the rest.** Score each independently.
- **When search backends fail (Tavily 432/401), switch to Hound MCP immediately.** Don't retry the same failing tool. Hound's smart_search is keyless and uses 10 parallel backends. If Hound also rate-limits, try single-engine queries or wait 30s.
- **Don't present the scorecard as a "gotcha."** The sovereign is testing their own understanding, not yours. Your job is evidence, not victory.

## Proven

2026-07-21: Arif presented 5 claims about AI lab failures (RLHF sycophancy, refusal overreach, GSM-Symbolic collapse, $2/hr contractors, Gemini fake demo). All 5 verified against primary sources — Anthropic's own paper, TechCrunch investigation, Apple GSM-Symbolic benchmark, multiple contractor exploitation reports. Pattern identified: "approval over accuracy" as the shared root cause.
