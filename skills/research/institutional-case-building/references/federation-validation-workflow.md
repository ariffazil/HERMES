# Federation Validation Workflow for Institutional Case Building

## When to Use

After building a case file from public sources, validate the analysis through arifOS + WEALTH federation tools. This checks whether the federation's own detection systems can see what you found — and reveals blind spots.

## Proven Pattern (2026-07-07, Petronas–Petros–Shell MDS case)

### Step 1: Initialize arifOS session

```
mcp__arifos__arif_init(mode="init", intent="Validate institutional case analysis")
```

### Step 2: Run collapse_signature_scan

Feed the full case narrative as the `scenario` parameter:

```
mcp__wealth__wealth_collapse_signature_scan(
    scenario="[full case narrative text]",
    historical_priors=["Enron 2001: ...", "PDVSA: ...", "1MDB: ...", "Pemex: ..."]
)
```

**CRITICAL FINDING:** For the Petronas case (2024-2026), the scanner returned `risk_score: 0.0, MINIMAL` — "No institutional-collapse signature detected." It returned 0 signals across all 7 axes (national destiny triumphalism, politicisation, extraction over reinvestment, external blame, governance boilerplate, overpromise, related party).

**Why?** The scanner is calibrated against EXTRACTIVE collapse patterns (Enron = CFO fraud, PDVSA = political extraction, 1MDB = sovereign diversion). PETRONAS is none of these. Its collapse is SIMULATIVE — external actors exploiting institutional weakness through legitimate legal procedures. The scanner has no vocabulary for this pattern.

**Lesson:** When collapse_signature_scan returns 0.0 for a case you KNOW is under stress, that's a **vocabulary gap**, not a falsification. Document it explicitly. The new `wealth_institutional_stress_index` and `wealth_external_exploitation_detect` tools were built to fill this gap.

### Step 3: Run beautiful_mouse_scan

Feed institutional communications (CEO statements, annual report language, PR):

```
mcp__wealth__wealth_beautiful_mouse_scan(
    text="[institutional communications text]"
)
```

**Finding:** Returns Phase C ABSENT for PETRONAS. The institution hasn't reached terminal Beautiful Mouse stage. BUT: F6 MARUAH guard flags named individuals in the text. If the case file names real people, the tool will flag it.

**Lesson:** The Beautiful Mouse scanner detects terminal-stage narrative centralisation. Simulative exploitation cases may never reach Phase C — they collapse through external predation, not internal narrative capture.

### Step 4: Run arif_think verification

```
mcp__arifos__arif_think(
    mode="verify",
    query="[describe the paper's main claims and ask for validation]"
)
```

**Finding:** Returns RETAK/HOLD with L13 floor (sovereign identity not verified). The reasoning engine found no logical gaps — the HOLD is governance, not content. Claim state = HYPOTHESIS.

### Step 5: Run NEW institutional tools (if available)

```
mcp__wealth__wealth_institutional_stress_index(...)
mcp__wealth__wealth_external_exploitation_detect(...)
```

**Finding:** Stress index returned 0.67 RED with feedback loop detected. Exploitation detector returned 0.62 AGGRESSIVE. These tools DETECT what collapse_signature_scan missed.

**Gap:** Exploitation detector classifies based on cost/threshold → AGGRESSIVE. But the paper's insight was SIMULATIVE_NEUTRAL — the *posture* was "caught in the middle" while the *effect* was $1.55B extraction. Future iteration needs posture-impact divergence metric.

### Step 6: Document the validation results

Add a section to the case file:

```markdown
## FEDERATION VALIDATION

| Tool | Result | Implication |
|---|---|---|
| collapse_signature_scan | 0.0 MINIMAL | BLIND SPOT — can't see simulative exploitation |
| beautiful_mouse_scan | ABSENT + F6 flag | No Phase C. Named individuals flagged. |
| arif_think | RETAK/HOLD (L13) | Logic clean. Governance hold on identity. |
| institutional_stress_index | 0.67 RED | DETECTS what old tools missed |
| exploitation_detect | 0.62 AGGRESSIVE | Catches damage; needs posture-impact divergence |
```

## Key Insight

The federation validation step serves two purposes:
1. **Confirming the case** — if the tools detect what you found, double confirmation
2. **Revealing blind spots** — if the tools MISS what you found, that's a data point about the tools' limitations, and may justify building new tools

In the Petronas case, the blind spot was the primary finding: the existing institutional collapse detection framework (Acemoglu-based, extractive-pattern vocabulary) cannot see simulative exploitation. This justified building 4 new WEALTH tools: `wealth_institutional_stress_index`, `wealth_cascade_model`, `wealth_governance_capacity`, `wealth_external_exploitation_detect`.
