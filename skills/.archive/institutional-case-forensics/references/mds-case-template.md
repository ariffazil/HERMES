# MDS Case Sheet Template

Standard fields for Multi-Dimensional Scenario case analysis.

## Header
```
# CASE SHEET: [CASE NAME]
> Schema: MDS v1
> Sources: [list outlets]
> Generated: [date] · hermes-prime
> SOT check: [live state / verified / unverified]
```

## Required Fields

### ACTOR
- Name, age, role, tenure, function
- Access to payload/document/instrument

### COUNTERPARTY
- Named recipients / targets
- Their roles and institutional positions
- Structural relationship to actor

### PAYLOAD
- What was at stake (document, money, contract rights)
- Classification level
- Why it matters (strategic significance)

### VECTOR
- Channel (email, court filing, BG call, contract signing)
- Time window (specific dates/times)
- Location if relevant

### TIMELINE
Table format: Date | Event | Source | Confidence
- Every date must have ≥2 source cross-reference for OBS label
- Separate FACT rows from INTERPRETATION rows

### CHARGE / LEGAL FRAMEWORK
- Statutes cited
- Max penalties
- Jurisdiction

### DEFENSE
- What the opposing side argues
- Cross-examination points
- Discrepancies exploited

### EFFECT
- Financial (quantified where possible)
- Institutional (governance impact)
- Strategic (longer-term consequences)

### OPEN THREADS
- What we don't know yet
- Pending court decisions
- Missing evidence

### CONFIDENCE BREAKDOWN
- OBS % — verbatim from ≥2 sources
- DER % — derived/computed
- INT % — interpretive
- SPEC % — hypothesised

## Output Format
- Save as .md to `/var/arifos/artifacts/outbox/YYYY-MM-DD/`
- Save as .json to `/root/forge_work/YYYY-MM-DD/`
- Compute SHA256 for both files
- Cross-reference connected cases by case_id
