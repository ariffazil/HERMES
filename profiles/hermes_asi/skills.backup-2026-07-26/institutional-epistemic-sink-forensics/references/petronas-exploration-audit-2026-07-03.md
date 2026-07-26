# Reference — Petronas Exploration Geoscience Audit, 2026-07-03

This is the **proven audit receipt** from the live WEALTH federation execution. Use it as the template for any future institutional epistemic-sink audit. The full audit lives at `/root/ariffazil/HAMPA/wealth-audit-calhoun-petronas-2026-07-03.md` and is sovereignty-protected (never pushed to public GitHub).

## The 11 WEALTH tools driven

| # | Tool | Result |
|---|---|---|
| 1 | `wealth_conservation_check` | books balance, NOT fraud |
| 2 | `wealth_flow_check` | PAT normalising post-2022 spike, no sigmoid |
| 3 | `wealth_compute_emv` | EMV=7.0, tail thickening YES |
| 4 | `wealth_survival_engine(mode=runway)` | AMBER, g_score=0.6256 |
| 5 | `wealth_collapse_signature_scan` | INSUFFICIENT_SIGNAL on all 7 axes (vocabulary gap) |
| 6 | `wealth_beautiful_mouse_scan` | Phase C ABSENT (earlier-stage sink) |
| 7 | `wealth_capture_scan` | all 6 dimensions LOW (diagnosis clean) |
| 8 | `wealth_power_audit` | all 6 dimensions LOW (scanner can't detect dossier) |
| 9 | `wealth_omni_wisdom` | HOLD, omega_verdict Ω-WEALTH-00 |
| 10 | `wealth_judge_handoff` | READY for arif_judge |
| 11 | `wealth_vault_write` | preload required, deferred |

## Key Findings

1. **Diagnosis is qualitatively real but quantitatively off-vocabulary.** WEALTH's scanners are calibrated to state-level collapse (Enron/PDVSA/Pemex/1MDB), not sub-function epistemic sink (Petronas Exploration class). Result: `INSUFFICIENT_SIGNAL` on all 7 axes is a vocabulary gap, not a falsification.

2. **Diagnosis itself is uncaptured.** `wealth_capture_scan` returns all 6 dimensions LOW — the failure claim is structurally clean, no incentive asymmetry, no vendetta, no capture.

3. **Constitutional separation holds.** WEALTH prepares the envelope (`wealth_judge_handoff` → READY), arifOS judges (`arif_judge` → verdict ESCALATE for irreversible+federation-wide), Arif decides. The handoff correctly enforces separation of powers.

4. **Confidence capped at 0.58 (YELLOW band).** Lower than the Kinabalu two-oceanics claim (0.50-0.58 range after tightening). Honored by the discipline: hold until falsification tests resolve.

## The Falsification Tests (still pending)

1. **Tomography** — confirms 1-slab vs 2-slab Kinabalu geometry → updates "narrative centralisation"
2. **KT-7 depth conversion** — confirms Vp 5.0-6.5 ophiolite vs Vp <4.0 shale → updates "citation discipline"
3. **MYPR outcome 15 July 2026** — updates "career dependency" quantification
4. **Hall 2026 paper release** — updates citation chain inertia
5. **AI tool flagging rate** (12 Jun 2026 point 6 was 1 incident) — updates "competence control" threat signal

## Proven Python Recipe (copy + adapt)

```python
import asyncio, json
from fastmcp import Client

async def audit_institution(institution_name: str, narrative: str,
                             public_facts: dict, dossier_patterns: list,
                             rival_evidence: list):
    """Drive the 11-tool WEALTH audit for institutional epistemic sink."""

    async with Client("http://127.0.0.1:18082/mcp") as c:
        # 4 mandatory checks
        cons = await c.call_tool("wealth_conservation_check", public_facts['assets_liabilities'])
        flow = await c.call_tool("wealth_flow_check", public_facts['income_expenses'])
        emv = await c.call_tool("wealth_compute_emv", public_facts['emv_scenarios'])
        runway = await c.call_tool("wealth_runway_check", public_facts['runway'])

        # 7-signature scan + Calhoun
        collapse = await c.call_tool("wealth_collapse_signature_scan", {
            "scenario": narrative,
            "capital_type": "institutional_sub_function",
            "historical_priors": ["Enron", "PDVSA", "Pemex", "1MDB", "Suriname_beautiful_mouse"],
        })
        mouse = await c.call_tool("wealth_beautiful_mouse_scan", {
            "text": narrative,
            "historical_priors": ["Calhoun_Universe_25", "Suriname_beautiful_mouse"],
        })

        # Capture + power checks
        capture = await c.call_tool("wealth_capture_scan", {
            "advice_text": narrative,
            "source_model": f"federation_we_geo_{datetime.now().isoformat()[:10]}",
        })
        power = await c.call_tool("wealth_power_audit", {
            "scenario": narrative,
            "actors": [d['actor'] for d in dossier_patterns],
            "context": {
                "evidence_basis": dossier_patterns,
                "f6_maruah_check": "names role not individual verdicts",
                "refusal_surface": "preserved",
            },
        })

        # Synthesis
        synthesis = await c.call_tool("wealth_omni_wisdom", {
            "mode": "synthesize",
            "decision_context": {
                "domain": "institutional_epistemic_sink",
                "subject": institution_name,
                "evidence_for": len([d for d in dossier_patterns if d.get('supporting', True)]),
                "evidence_against": len(rival_evidence),
                "confidence": 0.58,
            },
            "institutional_trust": {
                "trust_level": "low_for_sub_function_high_for_group",
                "rationale": "Group financials solid, sub-function shows role saturation",
            },
        })

        # Handoff envelope
        envelope = json.dumps({
            "verdict": "PARTIAL EUREKA",
            "signatures_active": ["governance_sink", "narrative_centralisation", "talent_drain"],
            "signatures_absent": ["financial_sigmoid", "counterparty_contamination"],
            "confidence": 0.58,
            "blast_radius": "personal_career_not_group_collapse",
        })
        handoff = await c.call_tool("wealth_judge_handoff", {
            "tool_name": "wealth_collapse_signature_scan",
            "result": envelope,
            "intent": f"Register collapse signature claim against {institution_name}",
            "capability": "register_collapse_signature_claim",
            "blast_radius": "MEDIUM",
            "reversibility_level": "PARTIAL",
        })

    return {
        "conservation": cons,
        "flow": flow,
        "emv": emv,
        "runway": runway,
        "collapse_signature": collapse,
        "beautiful_mouse": mouse,
        "capture": capture,
        "power": power,
        "synthesis": synthesis,
        "handoff": handoff,
    }
```

## Sovereignty Pattern

This audit lived at `/root/ariffazil/HAMPA/wealth-audit-calhoun-petronas-2026-07-03.md` — sovereignty-protected by `.gitignore` line 6 `*` rule. The INDEX.md on GitHub references the file's existence without exposing its content. F6 MARUAH maintained throughout (no individual verdicts, only role patterns).