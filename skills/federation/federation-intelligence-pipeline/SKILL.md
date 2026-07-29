---
name: federation-intelligence-pipeline
title: Federation Intelligence Pipeline
description: "Process external intelligence (news, reports, analysis) through the governed arifOS pipeline: sense → route → analyze → synthesize → evidence → handoff. Covers WEALTH institutional stress monitoring, forge work receipt filing, and OpenCode handoff envelopes."
category: federation
tags: [intelligence, evidence, pipeline, arifos, handoff, opencode]
triggers:
  - "Process an external intelligence source (news, report, analysis) through the arifOS pipeline"
  - "Route intelligence to a domain organ (WEALTH, GEOX, WELL, A-FORGE)"
  - "Prepare a sealed handoff envelope for downstream actors (OpenCode, operator)"
  - "File forge work receipt from an intelligence processing session"
---

# Federation Intelligence Pipeline

Process external intelligence sources (news articles, institutional reports, market analysis) through the governed arifOS pipeline: sense → route → analyze → synthesize → evidence → handoff.

## Pipeline Sequence

### 1. Session Init (`arif_init`)

```
arif_init(
    mode='init',
    actor_id='hermes-asi',
    intent='<describe the intelligence task>',
    requested_authority='OBSERVE_ONLY',
    verbosity='minimal'
)
```

**Key outputs:** `session_id`, `session_token`, `authority_level`
**Note:** OBSERVE_ONLY authority correctly blocks `arif_seal` and `arif_forge`. Constitutional and expected.

### 2. Source Acquisition

Fetch the intelligence source — prefer the fastest path:

| Source type | Tool | Notes |
|---|---|---|
| News articles | `smart_fetch` (Hound MCP) | Auto http→stealthy escalation |
| PDF documents | `smart_fetch` + auto-extraction | Use `pages=` / `focus=` to save tokens |
| Web pages (dynamic) | `browser_navigate` | For JS-rendered content |
| API/structured | `web_extract` | Only if backend supports it |

### 3. Cross-Reference Search

Search for existing intelligence on the same topic:

```
arif_observe(mode='search', query='<topic keywords>', result_limit=5)
web_search(query='<topic + entity>', limit=5)
```

**Purpose:** Detect whether this is a first signal or a confirmation.

### 4. Organ Routing (`arif_route`)

Route intent to the appropriate domain organ:

| Domain | Organ | Key Tools |
|---|---|---|
| Institutional stress, finance | **WEALTH** | `wealth_institutional_stress_index`, `capital_health` |
| Geology, subsurface | **GEOX** | `geox_basin`, `geox_well_desk`, `geox_claim` |
| Human well-being | **WELL** | `well_assess_homeostasis`, `well_validate_vitality` |
| Execution, forge | **A-FORGE** | `arif_forge` |

```
arif_route(intent='<intent>', organ='WEALTH', session_token='<token>')
```

### 5. Domain Analysis

Call the relevant domain tool with extracted intelligence.

**WEALTH Institutional Stress Index:**
```
wealth_institutional_stress_index(
    org_name='<entity>',
    financial_signals={...},
    governance_signals={...},
    workforce_signals={...},
    legal_signals={...},
    exploitation_signals={...}
)
```

**⚠️ Fallback: Manual stress index when WEALTH is unreachable**

| Dimension | Inputs | Scale |
|---|---|---|
| Financial | Revenue/profit trend, cost-cutting | 0–1 |
| Governance | Board size, resignations, independence | 0–1 |
| Workforce | Rightsizing %, exits, key departures | 0–1 |
| Legal | Litigation, injunctions, regulatory uncertainty | 0–1 |
| External Exploitation | Payment freeze, competing claims, fiscal extraction | 0–1 |

Composite = weighted average. Bands: <0.25 LOW, 0.25–0.45 MOD-LOW, 0.45–0.65 MOD-HIGH, >0.65 HIGH. Re-run via organ tool when server recovers.

### 6. Synthesis (`arif_think`)

Synthesize all evidence with epistemic labels:

```
arif_think(mode='reason', query='''SYNTHESIS: <title>
[OBS] <observation>
[DER-1] <inference>
[SPEC-1] <projection>
VERDICT: <summary>''')
```

**Label conventions:** `[OBS]` — direct observation; `[DER]` — derived inference; `[SPEC]` — speculative projection; `[INT]` — interpretive judgment.

### 7. Evidence Filing (forge work receipt)

When `arif_seal` is blocked (OBSERVE_ONLY), file a forge work receipt:

```
mkdir -p /root/forge_work/$(date +%Y-%m-%d)
```

Write to `forge_work/<YYYY-MM-DD>/<topic>-YYYYMMDD.md` with these sections:

1. **Session Metadata** — Session ID, trace, actor, pipeline date
2. **Source Intelligence** — Raw source URL, title, verified status
3. **Key Data Points** — Extracted metrics in structured table
4. **Contextual Intelligence** — Cross-references to earlier intel
5. **Domain Analysis** — Stress index or domain-specific metrics
6. **Synthesis** — Full OBS/DER/SPEC reasoning output
7. **Pipeline Audit Trail** — Step-by-step with status icons
8. **Handoff Envelope** — Summary, triggers, risks, re-seal note

### 8. Seal Attempt (authority-dependent)

```
arif_seal(mode='seal', payload='<summary>', seal_purpose='<purpose>')
```

**Expected under OBSERVE_ONLY:** HOLD — "Tool 'arif_seal' not in token allowed verbs." Document in receipt. Re-seal requires authenticated SEAL/EXECUTE authority.

## Pitfalls

- **WEALTH unreachable:** May return 3-consecutive-failure errors. Document in audit trail, compute manual estimate with full methodology.
- **arif_seal blocked:** Constitutional — OBSERVE_ONLY correctly blocks irreversible ops. Not a bug.
- **SearXNG is search-only:** `web_extract` depends on backend. Use `smart_fetch` from Hound MCP for URL content.
- **session_token expiry:** SCT TTL is 3600s by default. Long pipelines may need session refresh.
- **Epistemic honesty:** Label ALL uncertainty explicitly. Avoid false precision. Document estimated vs computed values.

## OpenCode Handoff Envelope Format (FI-NNN)

```
## OpenCode Handoff Envelope (FI-NNN)

### Summary for Action
<3-4 sentence summary>

### Recommended Monitoring Triggers
1. <condition>

### Key Risks to Track
- <risk>

### Re-seal Required
<Note if higher authority seal needed>
```

## References

- `references/petronas-fiscal-intel-20260729.md` — First application of this pipeline for Edge Malaysia PETRONAS fiscal intelligence
