# WEALTH Tool Body Language Gaps

> Source: PETRONAS institutional body language audit, 2026-07-12.
> Maps the 8-channel institutional body language framework against WEALTH MCP tool capabilities.

## Audit Results (Live Run 2026-07-12)

| Tool | Mode | Result | Signal |
|---|---|---|---|
| stress_index | scalar | 0.0 GREEN | SILENT_DEFAULT_RISK: 16 fields absent, treated as zero |
| governance_capacity | scalar | 0.0 capacity, INSUFFICIENT quorum | Board too small, no independence, no committees |
| exploitation_detect | scalar | 0.0 NEUTRAL | No exploitation signals (reads extractive only) |
| collapse_signature | 7-axis | 0.0 MINIMAL | INSUFFICIENT_SIGNAL on all 7 axes + Acemoglu/Calhoun |
| beautiful_mouse | Calhoun Phase C | ERROR | text_too_short (needs 50+ chars in source_text field) |
| capture_scan | capture | ERROR | Bug: detect_capture() unexpected kwarg source_model |
| power_audit | 6-dimension | CRITICAL capture_risk | Pattern: petros_exclusion — NOC outside fiscal oversight |
| cascade_model | linear | 0.0 acceleration | Insufficient data for trajectory |
| capital_wisdom | omni | HOLD, 0.0 confidence | Sub-engine unavailable (ModuleNotFoundError) |

## Channel-to-Tool Mapping

| Channel | Coverage | Tool | Gap |
|---|---|---|---|
| A. Capital Posture | PARTIAL | stress_index | Needs 16 structured fields; returns GREEN when absent |
| B. Institutional Breath | MISSING | cascade_model | No cadence/rhythm measurement |
| C. Personnel Movement | PARTIAL | stress_index workforce fields | Needs data pipeline; can't read from narrative |
| D. Information Posture | MISSING | — | No tool exists |
| E. Governance Posture | BEST | governance_capacity + power_audit | Strongest embedded channel |
| F. Maintenance Behaviour | MISSING | — | No tool exists |
| G. Boundary Behaviour | BLIND SPOT | exploitation_detect | Reads extractive only, not simulative exploitation |
| H. Crisis Reflex | MISSING | — | No tool exists |

## Tool-Behavior-as-Diagnostic Pattern

The most revealing finding: tool failures themselves are institutional body language signals.

| Tool Failure | Institutional Parallel |
|---|---|
| stress_index returns GREEN when 16 fields absent | Institution that gets clean audits because nobody asks hard questions |
| collapse_signature returns INSUFFICIENT_SIGNAL on all axes | Institution that passes compliance because checklist doesn't cover actual risk |
| exploitation_detect returns 0.0 NEUTRAL | "No theft detected" while external actors extract via legal contracts |
| beautiful_mouse errors on text_too_short | Can't be diagnosed because it doesn't publish enough honest text |
| capture_scan errors on parameter mismatch | Audit tool itself is broken |
| capital_wisdom returns HOLD with sub-engine unavailable | Wisdom layer is offline but still gives a verdict |

> The tools ARE the institutional body language. Their failures, blind spots, and default behaviors mirror exactly how institutions hide from scrutiny.

## SILENT_DEFAULT_RISK — The Critical Mechanism

When stress_index receives no data for 16 expected fields, it treats them as zero/false and returns GREEN with 0.0 confidence.

**This is exactly how institutions hide:** by not providing data, they get clean reports. The absence of data is not the absence of stress — it's the absence of transparency.

**Implication for auditors:** A GREEN result with missing fields is not a clean bill of health. It's a transparency failure. Document the missing fields as the primary finding.

## Simulative vs Extractive Exploitation

WEALTH collapse corpus is calibrated for:
- **Extractive patterns:** Enron, PDVSA, Pemex, 1MDB, WorldCom (internal theft, self-dealing, asset stripping)

WEALTH collapse corpus CANNOT see:
- **Simulative patterns:** External actors exploiting institutional weakness through legal/procedural means
  - Counterparty extracting via leverage (Shell MDS renegotiation during weakness)
  - State asserting rights via parallel entity (Sarawak/Petros during federal distraction)
  - Consultancy extracting via dependency creation (Bain during restructuring)
  - Regulatory capture via constitutional exemption (PDA 1974 outside Companies Act)

**Vocabulary gap is structural, not fixable by data injection.** The scanner vocabulary needs expansion to include simulative exploitation patterns.

## Build Priority for 8-Channel Embedding

| Priority | Channel | Implementation |
|---|---|---|
| 1 | B. Institutional Breath | capital_diagnose(mode="cadence_monitor") |
| 2 | D. Information Posture | capital_diagnose(mode="nervous_system") |
| 3 | H. Crisis Reflex | capital_diagnose(mode="crisis_reflex") |
| 4 | G. Boundary Behaviour | Vocabulary expansion for simulative exploitation |
| 5 | F. Maintenance Behaviour | capital_diagnose(mode="maintenance_metabolism") |
| 6 | E. Governance Posture | Exception geometry tracking enhancement |

## Meta-Principle

> The most revealing institutional signal is not what the institution does — it's what the institution's own diagnostic tools cannot see. The blind spots ARE the diagnosis.
