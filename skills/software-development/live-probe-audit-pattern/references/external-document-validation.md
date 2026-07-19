# External Strategic Document Validation

> Born from: GEOX vs Petrel comparison audit + GEOX deployment audit (2026-07-19)
> Distinct from: narrative-claim-audit (inflated deploy receipts). This handles full strategic/architectural analysis documents.

## Signal

Arif pastes a complete document from another agent/session/LLM containing strategic analysis, scoring tables, capability comparisons, valuations, or architectural assessments. Key markers:
- Multi-section structured document (not a deploy receipt)
- Contains numeric scores, dollar valuations, or capability grades
- May have comparison tables against competitors
- Often authored by another LLM agent (Gemini, GPT, etc.)
- Arif asks "audit and validate this claim" or "test all claims"

## Methodology: Layer-by-Layer Cross-Reference

### Layer 1 — Ground truth probe
Before reading the document fully, probe the subject's live state:
```bash
# For GEOX-style MCP organ:
systemctl is-active <service>
curl -s http://localhost:<port>/health | python3 -m json.tool
# For web surfaces:
curl -sLI <url> | head -20
```

### Layer 2 — Section-by-section tagging
For each section of the document, tag claims:
- **OBS** — directly verified by live probe (e.g., "service is healthy" → curl health)
- **INT** — plausible from architecture but no live proof (e.g., "falsification engine has 7 filters")
- **DER** — derived from observed state + documented design
- **ESTIMATE** — subjective (scores, valuations) — note as such
- **VOID** — contradicted by live evidence (e.g., "version v2026.07.19" when health says v2026.07.17)

### Layer 3 — Scoring inflation detection
When the document contains numeric scores (e.g., "8.5/10 for uncertainty handling"):
1. Ask: has this capability ever been benchmarked against a real decision?
2. If no → the score is aspirational. Downgrade by 1.5–2 points.
3. If the architecture exists but the implementation is partial → cap at 5.5–6.5
4. If the implementation is deployed but untested → cap at 6.0–7.0

### Layer 4 — Valuation skepticism
When the document contains dollar valuations:
1. Is there a paying customer? → if no, the valuation is INT, not CLAIM
2. Are there comparable transactions? → if no, the valuation is ESTIMATE
3. Is there demonstrated avoided loss? → if no, the valuation is SPECULATION
4. Tag accordingly: `$800K–$2.5M [ESTIMATE — no transaction evidence]`

### Layer 5 — Strategic thesis check
Does the document's core strategic argument hold regardless of scoring inflation?
- Often: the thesis is correct even when the numbers are aspirational
- Distinguish: "the direction is right" from "the magnitude is right"
- Example: "GEOX should not compete with Petrel" → correct thesis. "GEOX scores 6.9 vs Petrel 6.8" → invalid composite scoring.

## Audit Receipt Structure

```markdown
# [Document Title] — Claim Audit
> AUDITOR: HERMES-PRIME-AAA · DATE: YYYY-MM-DD

## §0 · METHODOLOGY (OBS/DER/INT/ESTIMATE/VOID tags)
## §1 · GROUND TRUTH — Live state vs claimed state
## §2 · CLAIM-BY-CLAIM AUDIT (per section)
## §3 · KEY GAPS — What the document misses
## §4 · OVERALL VERDICT (honesty / accuracy / strategic clarity / completeness)
## §5 · CORRECTED VIEW — What the document SHOULD say
```

## Common Drift Patterns in External Documents

### Pattern A: Composite scoring without weights
"Overall Score: 6.9/10" combining incomparable categories (software cost + governance philosophy + interpretation depth). Invalid composite. Flag as VOID unless weights and methodology are stated.

### Pattern B: Architecture-as-capability
"Strong falsification (7-filter kill matrix)" when only 3/7 filters are tested. Architecture ≠ implementation. Downgrade.

### Pattern C: Valuation without transaction evidence
"$800K–$2.5M current value" with no customers, no comparables, no revenue. Tag as ESTIMATE not CLAIM.

### Pattern D: Version inflation
"v2026.07.19" when health says v2026.07.17. Tool-count inflation. Underlying: generated during session but never actually deployed/restarted.

### Pattern E: Missing the live constraint
Document describes a capability as available but ignores session-gating, tool-count limits, or crash states that block it in practice. Probe the live surface before accepting.

## Pitfalls

- Don't dismiss the entire document because the scores are inflated. The strategic thesis is often correct.
- Don't accept "Strong" claims without live execution proof. If it's documented but never benchmarked, it's PLANNED not STRONG.
- Don't debate the author. Produce the audit, state the corrections, move on.
- If Arif pasted the document without comment, he wants validation, not agreement. Challenge with evidence.
