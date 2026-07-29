# ATLAS333 — Organ-Matrix Redundancy Detection

> Methodology for mapping a skill library against 7 zen organs to detect
> redundancy clusters, orphaned skills, and coverage gaps. Proven against
> 212 Hermes skills (2026-07-29).

## The Pattern

Instead of comparing skills pair-by-pair (O(n²)), map every skill to its
**zen organ owner**. Skills with the same organ target and overlapping
description are likely redundant. Skills with no organ are orphans.

### Step 1: Define 7 Organs

| Organ | Port | Domain | Zen Variable |
|-------|------|--------|-------------|
| arifOS kernel | 8088 | Governance, F1-F13, VAULT999 | ΔG |
| A-FORGE | 7071/7072 | Execution, build, deploy | W |
| GEOX | 8081 | Earth intelligence, geoscience | ΔR |
| WEALTH | 18082 | Capital, market, economics | ∂M/∂t |
| WELL | 18083 | Human readiness, dignity | Ω |
| AAA | 3001 | Control plane, A2A, agent cards | I_sys |
| arifFLOW | 7073 | Metabolism, receipts, FQ pulse | ∇F |

### Step 2: Map Each Skill to Its Organ

Use semantic rules (not string-matching):

- If skill deploys/restarts/monitors → A-FORGE (:7071)
- If skill queries governance/floors/judge → arifOS kernel (:8088)
- If skill touches earth/seismic/geology → GEOX (:8081)
- If skill handles money/trading/capital → WEALTH (:18082)
- If skill touches human/vitality/dignity → WELL (:18083)
- If skill manages agent identity/federation/cards → AAA (:3001)
- If skill tracks flow/receipts/metabolism → arifFLOW (:7073)

### Step 3: Find Redundancy Clusters

Within each organ group, look for:

1. **Name-prefix duplicates**: `vps-operations`, `vps-autonomous-ops`,
   `agentic-vps-operations` → same organ (A-FORGE), same domain → merge
2. **Content-length identity**: identical line counts → exact duplicate
3. **Trigger overlap**: same trigger phrases in SKILL.md frontmatter
4. **Description cosine similarity**: `difflib.SequenceMatcher > 0.5`

### Step 4: Score Clusters

| Metric | Formula | Threshold |
|--------|---------|-----------|
| Redundancy count | Skills in same organ + same domain | >2 = merge |
| Entropy contribution | dS = -(count-1) per cluster | Sum all clusters |
| Orphan count | Skills with no organ mapping | 0 = ideal |

### Worked Example: VPS Ops (2026-07-29)

6 skills all mapped to A-FORGE organ:
- `vps-operations` (BASIC ops)
- `vps-autonomous-ops` (overlap with above)
- `vps-autonomous-response` (overlap)
- `vps-agentic-ops` (overlap)
- `agentic-vps-operations` (duplicate name)
- `autonomous-vps-response` (overlap)

**Score**: dS = -5 from this cluster alone. Redundancy index = 83%.
**Fix**: Merge all 6 → 1 canonical skill. Keep `autonomous-vps-response` as
master because it had the richest content + most triggers.

### Worked Example: Nasi Lemak (2026-07-29)

4 skills mapped to WEALTH organ:
- `nasi-lemak-daily-tracking`
- `nasi-lemak-sales`
- `nasi-lemak-sales-tracking`
- `nasi-lemak-tracking`

**Fix**: Merge all 4 → `nasi-lemak-tracking`. Absorbed `vendor-receipt-tracking`
(3 more skills) for total dS = -6 from retail cluster.

### Worked Example: Trading (2026-07-29)

5 skills mapped to WEALTH organ:
- `trading-analysis-xauusd`
- `daily-trading-signal-briefing`
- `trading-intelligence-system`
- `agentic-trading-companion`
- `mt5-ai-trading-agent`

**Fix**: Merge first 4 → 2 (PASSIVE + ACTIVE boundary). Keep mt5 standalone.
dS = -2.

## Redundancy Classification

| Label | Criteria | Action |
|-------|----------|--------|
| **DUPLICATE** | Same organ, same domain, same triggers | Merge into one |
| **SUPERSEDED** | Explicitly marked superseded/stale | Delete, absorb content |
| **OVERLAP** | Same organ, same domain, different trigger set | Keep best, archive rest |
| **ORPHANED** | No organ mapping | Assign organ or delete |
| **PHANTOM** | Referenced in agent cards, doesn't exist on disk | Create or remove reference |

## Output Format

```json
{
  "total_skills": 212,
  "canonical_after_merge": 196,
  "entropy_delta": -16,
  "clusters": [
    {
      "domain": "VPS Ops",
      "skills": ["vps-operations", "vps-autonomous-ops", "..."],
      "count": 6,
      "fix": "merge → 1",
      "dS_contribution": -5
    }
  ],
  "orphans": ["human-sexuality-shadow-framework"],
  "superseded": ["flame-free-loop", "akal-cognitive-invariants"]
}
```

DITEMPA BUKAN DIBERI — 2026-07-29.
