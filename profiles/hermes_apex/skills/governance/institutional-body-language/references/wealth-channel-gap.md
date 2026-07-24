# WEALTH Tool Capability Gap — Institutional Body Language

## Current State (12 tools, post-fixes July 2026)

### 7 Canonical Tools
- capital_primitive — NPV, IRR, EMV, Monte Carlo, Kelly, Markowitz
- capital_health — Net worth, cash flow, runway, breakeven, fiscal breakeven
- capital_diagnose — Stress index, governance capacity, collapse signature,
  power audit, capture scan, bid surface, entropy
- capital_wisdom — 6-dimension wisdom evaluation (dignity, sovereignty,
  resilience, inequality, ecological, optionality)
- capital_market — Commodity prices, FX, macro indicators
- capital_ledger — VAULT999 capital transactions
- capital_registry — Organ health, tool schema

### 4 Institutional Tools (added July 2026)
- capital_stress_convergence — multi-signal institutional stress
- capital_simulative_scan — external exploitation detection
- capital_vulnerability_window — governance gap detection
- capital_cascade_map — trigger chain amplification

## Tool Behavior as Diagnostic

| Tool Return | What It Means | Institutional Parallel |
|---|---|---|
| GREEN with missing fields | SILENT_DEFAULT_RISK | Clean audit because nobody asked hard questions |
| INSUFFICIENT_SIGNAL | Vocabulary mismatch | Compliance passes because checklist doesn't cover actual risk |
| NEUTRAL on exploitation | Reads extractive only | "No theft detected" while external actors extract through legal contracts |
| All LOW despite evidence | Pattern blindness | Tool can't recognise NOC constitutional position as capture |

## Channel Embedding Status

| Channel | Tool(s) | Status | Gap |
|---|---|---|---|
| A. Capital Posture | stress_index + capital_primitive + capital_health | ⚠️ Needs data feed | Auto-ingestion from financial reports |
| B. Institutional Breath | capital_diagnose(mode="cadence_monitor") | ❌ Missing | Time-series: approval cycles, payment terms, decision backlog |
| C. Personnel Movement | Data integration | ⚠️ Has fields, no pipeline | HR feeds, exit tracking, headcount trends |
| D. Information Posture | capital_diagnose(mode="nervous_system") | ❌ Missing | Bad news velocity, metric stability, report density |
| E. Governance Posture | governance_capacity | ⚠️ Crashes on type | Fix committee members:int vs list + exception geometry |
| F. Maintenance Behaviour | capital_diagnose(mode="maintenance_metabolism") | ❌ Missing | Asset maintenance vs new initiative ratio |
| G. Boundary Behaviour | capture_scan | ✅ Partial | Simulative vocabulary expansion needed |
| H. Crisis Reflex | capital_diagnose(mode="crisis_reflex") | ❌ Missing | Budget cut hierarchy, blame direction, compensation protection |

## Build Priority

1. **B Institutional Breath** — cadence_monitor (highest diagnostic value)
2. **D Information Posture** — nervous_system (measures pain transmission)
3. **H Crisis Reflex** — crisis_reflex (measures protection hierarchy)
4. **G Boundary Behaviour** — simulative vocabulary expansion
5. **F Maintenance Behaviour** — maintenance_metabolism
6. **E Governance Posture** — exception geometry enhancement

## Channel B Spec (cadence_monitor)

**Inputs needed:**
- Approval cycle times (routine vs escalated)
- Payment terms trend (30/60/90 day shift)
- Decision backlog count
- Reporting frequency vs information density
- Emergency reprioritization rate
- Hiring velocity (public data proxy)

**Output:** breath_strain_score (0.0–1.0)
- Healthy: <0.3 (coherent rhythm)
- Strained: 0.3–0.6 (approvals centralising, terms stretching)
- Critical: >0.6 (every decision needs escalation)

**Key design rule:** Don't build a tool that needs data that doesn't exist.
Build a tool that reads what's publicly available and labels what's missing.
Missing signals = UNOBSERVED, not zero. (Lesson from SILENT_DEFAULT_RISK.)

## Known Bugs (pre-existing, pre-July 2026 fixes)

- wealth_governance_capacity: crashes on committee members:int vs list
- capital_entropy veto_holders: expects dict items, rejects string arrays
- power_audit: vocabulary limited to Enron/PDVSA corruption keywords

## Meta-Principle

The most revealing institutional signal is not what the institution does —
it's what the institution's own diagnostic tools cannot see. The blind spots
ARE the diagnosis. When building new channels, always ask: "What pattern
would this channel reveal that the institution would prefer stayed invisible?"
