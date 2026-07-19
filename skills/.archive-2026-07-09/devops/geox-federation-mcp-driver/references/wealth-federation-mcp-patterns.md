---
name: wealth-federation-mcp-patterns
purpose: WEALTH MCP tool surface (:18082, 32 tools) — drive collapse-signature, beautiful-mouse, capture, power, judge_handoff, and the preload gate. Validated 2026-07-03 against the live daemon.
audience: any agent driving WEALTH federation tools for institutional forensics, capital allocation, or epistemic-sink diagnosis.
---

# WEALTH Federation MCP — Patterns That Actually Work

The WEALTH organ runs at `http://127.0.0.1:18082/mcp` (streamable-HTTP, FastMCP). 32 tools exposed. Validated against live daemon 2026-07-03.

## 1. The Two-Layer Preload Gate (CRITICAL)

Several WEALTH tools refuse to execute until specific `wealth://` resources have been read in the current session. The error message names exactly which resources are missing:

```
"wealth://runtime/policy requires these resources to be read in session '_default'
 before calling wealth_compute_emv: ['wealth://reality/context']"
```

**Preload matrix (confirmed 2026-07-03):**

| Tool | Required preloads |
|---|---|
| `wealth_compute_emv` | `wealth://reality/context` |
| `wealth_judge_handoff` | `wealth://handoff/arifos-schema`, `wealth://affordance/contracts` |
| `wealth_vault_write` | `wealth://replay/receipt-schema` |
| `wealth_collapse_signature_scan` | (none observed in practice) |
| `wealth_beautiful_mouse_scan` | (none) |
| `wealth_power_audit` | (none) |

**Important nuance:** Calling `read_resource` via the FastMCP client returns a `'NoneType' object has no attribute 'to_mcp_result'` error for ALL `wealth://` URIs in current daemon. This is **a daemon-side bug, not your problem** — the server tracks preloads internally by session, and the policy gate fires regardless of whether YOUR read succeeded.

**Practical workaround:** Call `wealth_collapse_signature_scan` and `wealth_beautiful_mouse_scan` (the diagnosis tools) **first**. They work without preloads. Only `wealth_judge_handoff` / `wealth_vault_write` need the (currently-broken) preload path. If you MUST do a handoff, log the failure and proceed — the diagnosis tools carry enough evidence on their own.

## 2. The Iron Rule — Schema Discovery via Pydantic Errors

Same pattern as GEOX: **call the tool with empty args and read the Pydantic error.** FastMCP leaks the full schema. Example:

```python
try:
    await c.call_tool("wealth_collapse_signature_scan", {})
except Exception as e:
    # Output: "Missing required argument: scenario"
    # → Required field: scenario (string)
```

Or use `list_tools()` for the full property table:

```python
tools = await c.list_tools()
for t in tools:
    if t.name == "wealth_collapse_signature_scan":
        schema = t.inputSchema  # note camelCase, not input_schema
        # schema["properties"]["scenario"]["type"] == "string"
        # schema["required"] == ["scenario"]
```

## 3. The 32 WEALTH Tools — Confirmed Live Schemas (2026-07-03)

### Tool name → required fields quick reference

| Tool | Required | Optional notable | Returns |
|---|---|---|---|
| `wealth_conservation_check` | (none — but assets+liabilities arrays expected) | `assets[]`, `liabilities[]` | `{net_worth, asset_total, ...}` |
| `wealth_flow_check` | (none — income+expense arrays) | `income[]`, `expenses[]` | `{net_cashflow, is_positive, ...}` |
| `wealth_compute_emv` | `outcomes[]`, `probabilities[]` | — | `{emv, variance, std_dev, outcome_count}` ⚠ needs preload |
| `wealth_runway_check` | `liquid_assets`, `monthly_burn` | `conservative_factor=0.8` | runway_months |
| `wealth_survival_engine` | (mode-driven) | `mode="personal_finance"\|"runway"\|"cashflow"`, `monthly_income`, `monthly_expenses`, `liquid_assets`, `horizon_months=12` | engine envelope with verdict |
| `wealth_capture_scan` | `advice_text` | `source_model=""` | 6-dimension capture_risk envelope |
| `wealth_power_audit` | `scenario` | `actors[]`, `context{}`, `legitimacy_score{}` | structural_coercion_detected + 6 dimensions |
| `wealth_collapse_signature_scan` | `scenario` | `capital_type="financial"`, `historical_priors[]` | 7-axis profile + Acemoglu×Calhoun 2D map + risk_level |
| `wealth_beautiful_mouse_scan` | `text` | `historical_priors[]` | 6 Phase C indicators + phase_c_score + verdict |
| `wealth_omni_wisdom` | (mode-driven) | `mode="synthesize"`, `decision_context{}`, `deal_params{}`, `path_params{}`, `institutional_trust{}`, `memory_query` | wisdom_verdict (HOLD/SEAL) |
| `wealth_judge_handoff` | `tool_name`, `result`, `intent`, `capability` | `blast_radius`, `reversibility_level` | handoff_envelope for arif_judge ⚠ needs preload |
| `wealth_vault_write` | `tx_type`, `amount` | `currency="MYR"`, `description`, `category`, `notes` | vault receipt ⚠ needs preload |
| `wealth_vault_query` | (none) | `query`, `limit`, `asset_id` | vault records |
| `wealth_market_data` | (none) | `mode="fx"`, `base`, `targets`, `commodity`, `indicator`, `country` | market snapshot |
| `wealth_monte_carlo_simulate` / `wealth_monte_carlo` | (probe — same as compute_emv) | — | MC envelope |
| `wealth_compute_npv` / `wealth_compute_irr` / `wealth_compute_evoi` | (probe) | — | capital metrics |
| `wealth_personal_finance` | (probe) | — | personal finance snapshot |
| `wealth_stock_analysis` | (probe) | — | stock envelope |
| `wealth_registry_status` | (none) | `mode="registry"` | registry diagnostic |
| `wealth_system_registry_status` | (none) | — | system registry |
| `wealth_boundary_governance` | (probe) | — | boundary check |
| `wealth_wisdom_evaluate` | (probe) | — | wisdom evaluation |
| `wealth_agent_path` / `wealth_reason_agent` | (probe) | — | agent paths |
| `wealth_forbidden_claims_scan` | (probe — likely takes `text`) | — | scan result |
| `wealth_emv_compute` / `wealth_evoi_compute` / `wealth_fiscal_breakeven` / `wealth_conservation_check` / `wealth_flow_check` / `wealth_confluence_check` / `wealth_asymmetry_check` | (all alias-style, probe) | — | variants of main tools |

⚠ **Confused aliases:** several tools exist as both `wealth_compute_X` and `wealth_X_compute` (e.g. `wealth_compute_emv` AND `wealth_emv_compute`). The `compute_*` variant is canonical; the `_compute` variant is legacy compat. Stick to `compute_*`.

## 4. The Collapse-Signature Forensic Pattern (Wealth's Killer Use Case)

**This is what WEALTH was actually built for** — institutional failure forensics via the 7 collapse signatures + Calhoun Phase C + Acemoglu power. Documented in the `wealth-collapse-signature` skill.

### Workflow

```
1. Read the wealth-collapse-signature SKILL.md (class-level doctrine)
2. GATHER: pull public facts about the institution (latest PAT, headcount, recent events)
3. RUN 4 mandatory checks: conservation, flow, entropy (EMV), survival (runway)
4. SCAN: wealth_collapse_signature_scan(scenario=text, historical_priors=[...])
5. SCAN: wealth_beautiful_mouse_scan(text=narrative, historical_priors=[...])
6. CHECK: wealth_capture_scan(advice_text=your_diagnosis) — verifies your diagnosis is uncaptured
7. CHECK: wealth_power_audit(scenario=power_play, actors=[...]) — power symmetry
8. SYNTHESIZE: wealth_omni_wisdom(decision_context={...}) — multi-domain synthesis
9. HANDOFF: wealth_judge_handoff(tool_name, result, intent, capability) — to arif_judge
10. SEAL: arif_seal(payload, ack_irreversible, actor_signature, nonce)
```

### Real Kinabalu / Petronas audit (2026-07-03) — what WEALTH returned

```
wealth_collapse_signature_scan:
  result.profile: ALL 7 AXES at signal_count=0
  acemoglu_axis.score: 0.5 (INSUFFICIENT_SIGNAL)
  calhoun_axis.score: 0.5 (INSUFFICIENT_SIGNAL)
  risk.score: 0.0 (MINIMAL)
  recommendation: "No institutional-collapse signature detected."

wealth_beautiful_mouse_scan:
  phase_c_score: 0.0
  phase_c_verdict: ABSENT
  narrative_signature: "appears to be in healthy friction"
```

**The honest meta-verdict:** WEALTH's scanner vocabulary is calibrated to **state-level institutional collapse** (Enron, PDVSA, Pemex, 1MDB corpus) and **terminal-stage Phase C narratives** (perfect-performance slogans, zero-failure marketing). It does NOT have vocabulary for:

- **Sub-function epistemic sink** (committee-density, citation-inertia, career-fear patterns)
- **Earlier-stage institutional sink** (signals that haven't crystallized into terminal phrase-pool)

**This is a class-level finding.** The pattern is real but the scanner cannot quantify it. The discipline is to:
1. Document the diagnosis qualitatively (HAMPA cards, PROPA patterns, audit receipts)
2. Name the scanner vocabulary gap as a federation issue
3. **DO NOT promote to SEAL** on sub-function patterns the corpus cannot quantify
4. Wait for richer telemetry (email frequency, task reassignment rate, citation drift) before re-running

### What WEALTH CAN quantify (the discipline)

| Dimension | Tool | Verdict |
|---|---|---|
| Group financial collapse | `wealth_conservation_check`, `wealth_flow_check` | Yes (numbers in, numbers out) |
| Energy transition tail risk | `wealth_compute_emv` (with scenarios) | Yes (probabilities in, EMV out) |
| Personal survival runway | `wealth_runway_check`, `wealth_survival_engine` | Yes |
| Capture of the diagnosis | `wealth_capture_scan` | Yes (6-dimension envelope) |
| Power asymmetry (loose) | `wealth_power_audit` | Partial (misses dossier patterns) |
| Sub-function epistemic sink | `wealth_collapse_signature_scan` | **NO — off-vocabulary** |
| Calhoun Phase C (terminal stage) | `wealth_beautiful_mouse_scan` | Partial (misses earlier-stage sink) |

## 5. The Constitutional Handoff Pattern (WEALTH → arifOS)

```python
# Step 1: Run WEALTH diagnosis tools
collapse_result = await safe(c, "wealth_collapse_signature_scan", {
    "scenario": "Petronas Exploration Geoscience sub-function ...",
    "historical_priors": ["Enron", "PDVSA", "1MDB", "Suriname_beautiful_mouse"],
})

# Step 2: Build the handoff envelope (as a JSON string for the result field)
envelope_result = json.dumps({
    "verdict": "PARTIAL EUREKA",
    "signatures_active": ["governance_sink", "narrative_centralisation", "talent_drain"],
    "signatures_absent": ["financial_sigmoid", "counterparty_contamination"],
    "confidence": 0.58,
    "blast_radius": "personal_career_not_group_collapse",
})

# Step 3: Call judge_handoff (may fail on preload — capture the error)
handoff = await safe(c, "wealth_judge_handoff", {
    "tool_name": "wealth_collapse_signature_scan",
    "result": envelope_result,
    "intent": "Register collapse signature claim against <institution>",
    "capability": "register_collapse_signature_claim",
    "blast_radius": "MEDIUM",
    "reversibility_level": "PARTIAL",
})

# Step 4: Submit to arifOS judge (separate organ, port 8088)
async with arifos_client:
    judge = await safe(arifos_client, "arif_judge", {
        "actor": "Arif (F13 SOVEREIGN)",
        "intent": "Constitutional judgment on institutional epistemic sink diagnosis",
        "requested_capability": "judge_institutional_diagnosis",
        "domain": "capital_governance",
        "reversibility_level": "reversible",  # diagnosis is reversible
        "blast_radius": "personal_career",
        "evidence": [{"type": "wealth_collapse_signature_scan", "result": envelope_result}],
    })
```

The handoff correctly enforces: **WEALTH prepares, arifOS judges, Arif decides.** WEALTH never declares the verdict.

## 6. Calhoun → Institution Translation (class-level doctrine)

The Calhoun Universe 25 ("behavioral sink") pattern translates to institutions as:

| Calhoun Universe 25       | Institutional geology equivalent                  |
|---------------------------|---------------------------------------------------|
| Unlimited food/water      | Budget, data rooms, seismic, reports, consultants |
| High-density enclosure    | Committees, departments, approval chains          |
| Social role breakdown     | Nobody owns first-principles questioning          |
| "Beautiful ones" withdraw | Smart staff become presentation polishers         |
| Reproduction collapse     | No new theories survive internal review           |
| Behavioral sink           | Citation sink / committee sink                    |

**The collapse is not lack of resources. The collapse is role saturation without truth metabolism.** Everyone has a role. Nobody has authority to break the false frame.

## 7. Pitfalls Discovered 2026-07-03

1. **Tool aliases are confusing.** `wealth_compute_emv` AND `wealth_emv_compute` both exist. Use the `compute_*` form. Same for `wealth_runway_check` / `wealth_survival_engine(mode='runway')` — the former is the dedicated tool, the latter is a mode.

2. **The preload gate is currently broken for `wealth://` resources.** Calling `read_resource("wealth://runtime/policy")` returns `'NoneType' object has no attribute 'to_mcp_result'`. The daemon tracks preloads internally and may still apply the gate even though YOUR read failed. **Workaround:** call `wealth_collapse_signature_scan` and `wealth_beautiful_mouse_scan` first (no preload), and only attempt handoffs/writes if you have direct evidence the preload succeeded (e.g. previous session).

3. **Scanner vocabulary is state-level collapse only.** Don't waste cycles trying to make `wealth_collapse_signature_scan` quantify a sub-function epistemic sink. It won't. Document the gap and move on.

4. **`wealth_power_audit` misses "dossier" / "task reassignment" patterns.** It scans for capture dimensions (incentive asymmetry, rent extraction, coercion) — not HR-style power asymmetry. Document the power pattern qualitatively and don't expect the scanner to detect it.

5. **`wealth_judge_handoff` is a *preparation*, not a seal.** It builds the envelope for arifOS. The actual constitutional verdict comes from `arif_judge`. Don't claim "WEALTH sealed the diagnosis" — it doesn't.

6. **`wealth_omni_wisdom` returns HOLD on under-specified context.** It needs `decision_context` with `domain`, `subject`, `evidence_for`, `evidence_against`, `confidence`. Empty context → `synthesis: {summary: "(no decision context provided)"}`, verdict HOLD.

7. **The 9-signal envelope** returned by WEALTH tools includes `witness: {human: false, ai: true, earth: false, is_complete: false, missing: ["human", "earth"]}`. This is honest — the tool doesn't claim human or earth witness; the user (F13) provides the human witness, GEOX provides the earth witness. Document this in any audit receipt.

## 8. Real Receipts From 2026-07-03 Petronas Audit

- `wealth_conservation_check` (assets=RM838.2bn + RM1450bn reserves, liabilities=RM838.2bn) → net_worth=0 (group-level observation), BOOKS BALANCE, NOT a fraud case
- `wealth_flow_check` (PAT trajectory 2020-2024) → PAT normalising post-2022 oil spike, no financial sigmoid at group level
- `wealth_compute_emv` (outcomes=[-200,-50,30,80,150], probs=[0.10,0.20,0.45,0.20,0.05]) → EMV=7.0, variance=7261, tail thickening YES (30% negative scenarios)
- `wealth_collapse_signature_scan` (Petronas Exploration sub-function, priors=[Enron,PDVSA,Pemex,1MDB,Suriname_beautiful_mouse]) → INSUFFICIENT_SIGNAL on all 7 axes (vocabulary gap)
- `wealth_beautiful_mouse_scan` (Petronas Exploration narrative) → Phase C ABSENT (not terminal stage yet)
- `wealth_capture_scan` (the diagnosis itself) → all 6 dimensions LOW (diagnosis is uncaptured, clean)
- `wealth_power_audit` (Laletha dossier scenario) → all 6 dimensions LOW (scanner can't detect dossier pattern)
- `wealth_omni_wisdom` (decision_context=epistemic_sink, confidence=0.58) → HOLD with omega_verdict Ω-WEALTH-00
- `wealth_judge_handoff` → READY for arif_judge (constitutional envelope prepared, F13 path open)

**Honest meta-verdict:** Diagnosis is qualitatively documented (5 Graph patterns + 11 May dossier + 12 Jun reprimand + 50-yr institutional debt), scanners are quantitatively silent on sub-function patterns. Hold at 0.58 confidence, do NOT seal, wait for falsification tests (tomography, KT-7 depth conversion, MYPR outcome).

## 9. Skill Reference

- **Class-level skill:** `wealth-collapse-signature` (at `/root/.agents/skills/wealth-collapse-signature/`) — has the full 4-mandatory-checks + 7-signature-scan + 3-pair-rules doctrine
- **Sibling skills:** `wealth-capital-thermodynamics`, `wealth-law-anthropology`, `wealth-capital-reasoning`
- **Cross-organ:** GEOX `geox_claim_grammar` (every collapse claim must carry evidence_for/against/missing_tests), arifOS `arif_judge` (constitutional verdict on capital decision), WELL `well_assess_homeostasis` (operator readiness before collapse claim)

## 10. Activation

```bash
source /root/GEOX/.venv/bin/activate  # or /root/WEALTH/.venv — fastmcp pre-installed
python3 your_audit.py
```

WEALTH port is `18082`, default transport is streamable-HTTP. Session works the same as GEOX (FastMCP client handles it).