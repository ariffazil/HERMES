# EGS Claim Workflow Examples

Real claim_create + evidence_attach recipes from past GEOX audits. Each example shows: intent → schema → result.

## Example 1: Kinabalu Two-Oceanics Eureka (2026-07-03)

**Intent:** Register a falsifiable tectonic model with 5 supporting + 2 rival evidence pieces, route through arifOS judge, expect ESCALATE → F13 SOVEREIGN.

```python
# Claim create
r = await geox.call_tool("geox_egs_claim_create", {
    "title": "Mount Kinabalu built by sequential action of two oceanic plates",
    "statement": (
        "Mount Kinabalu (4,095 m) and the Sabah margin were built by the sequential "
        "action of two oceanic plates (Proto-SCS consumed ~40-15 Ma southward beneath "
        "Borneo building the Crocker prism; Celebes Sea subducted northward ~15 Ma "
        "onward beneath Sulu Arc, rollback drove decompression melting that produced "
        "the 8-7 Ma granite pluton). Continental crust was never subducted beneath "
        "Sabah; the 'continental subduction' narrative violates buoyancy, metamorphism, "
        "seismicity, vergence, arc timing, basin geometry, and chronosequence patterns."
    ),
    "domain": "tectonic_stratigraphy",
    "author": "Arif (F13 SOVEREIGN)",
    "entity_type": "tectonic_model",
    "entity_id": "model_kinabalu_two_oceanics_2026",
    "confidence_score": 0.72,
    "tags": ["kinabalu", "sabah", "two-oceanics", "proto-south-china-sea",
             "celebes-sea", "rollback", "granite-pluton",
             "continental-subduction-falsified"],
})
# Returns: {"success": true, "claim_id": "e12b21e3f0574267", "status": "draft"}

# Evidence attach — supporting
r = await geox.call_tool("geox_egs_evidence_attach", {
    "claim_id": "e12b21e3f0574267",
    "description": "Krebs (2011) chronosequence stratigraphy of West Crocker + Kudat "
                   "formations shows no continental source material in the Oligocene-"
                   "Miocene turbidite pile; provenance ties to Proto-SCS island arc + "
                   "Dangerous Grounds attenuated continental margin",
    "evidence_kind": "publication",
    "supporting": True,
    "source": "Krebs 2011, PhD thesis, University of Malaya",
    "created_by": "GEOX corpus",
    "strength": "strong",
    "url": "geox://literature/KREBS-2011-CHRONOSEQ",
})
# Returns: {"success": true, "evidence_id": "5c9036f6a0274d2d"}

# Evidence attach — RIVAL
r = await geox.call_tool("geox_egs_evidence_attach", {
    "claim_id": "e12b21e3f0574267",
    "description": "RIVAL: H2 (Thrust Detachment over Continental Margin) — Hutchison "
                   "(1996) interprets the deep reflector as a décollement over stretched "
                   "continental crust (Dangerous Grounds). NOT falsified by current data.",
    "evidence_kind": "rival_hypothesis",
    "supporting": False,
    "source": "Hutchison 1996, Geological Evolution of SE Asia",
    "created_by": "GEOX corpus",
    "strength": "moderate_rival",
})
# Returns: {"success": true, "evidence_id": "e65b882e40354123"}
```

## Example 2: arifOS Judge Verdict Chain

```python
# Full constitutional chain — leads to ESCALATE → F13 SOVEREIGN
arifos = Client("http://localhost:8088/mcp")
async with arifos:
    # 1. Route the intent
    r = await arifos.call_tool("arif_route", {
        "intent": "Validate geological claim against GEOX EGS evidence",
        "actor_id": "arif",
        "session_id": "kinabalu-eureka-2026-07-03",
        "organ": "GEOX",
    })
    # Returns: verdict=SEAL, routing_confidence=0.95, organ=GEOX

    # 2. Observe — gather state
    r = await arifos.call_tool("arif_observe", {
        "mode": "search",
        "query": "Kinabalu two-oceanics GEOX claim e12b21e3f0574267",
        "actor_id": "arif",
        "session_id": "kinabalu-eureka-2026-07-03",
        "result_limit": 5,
    })
    # Returns: verdict=RETAK (L11 AUTH: session_id not found or expired — common issue)
    # Workaround: keep session_id consistent across all calls in same client session

    # 3. Think
    r = await arifos.call_tool("arif_think", {
        "mode": "plan",  # valid modes: plan, reflect, critique, metabolize, etc.
        "query": "Kinabalu two-oceanics vs continental-subduction falsification",
        "actor_id": "arif",
        "session_id": "kinabalu-eureka-2026-07-03",
        "witness_type": "human",
    })
    # Returns: status=SEAL but inner verdict=RETAK (sub-signal floor)

    # 4. Judge — full schema
    r = await arifos.call_tool("arif_judge", {
        "actor": "Arif (F13 SOVEREIGN)",
        "intent": "Constitutional judgment on Kinabalu two-oceanics eureka",
        "requested_capability": "judge_geological_model",
        "domain": "geoscience/tectonic_stratigraphy",
        "reversibility_level": "reversible",  # CHANGE to "irreversible" to trigger ESCALATE
        "blast_radius": "federation_wide",
        "epistemic_state": "PLAUSIBLE",
        "evidence": [
            {"type": "geox_claim", "id": "e12b21e3f0574267",
             "evidence_for": 5, "evidence_against": 2, "confidence": 0.72},
            {"type": "ontology", "id": "geox://resources/ontology/sabah_basin_strat.yaml",
             "key_finding": "Ophiolite basement 165-50 Ma = oceanic crust"},
        ],
        "actor_id": "arif",
        "session_id": "kinabalu-eureka-2026-07-03",
    })
    # Returns: verdict=SEAL → decision=ESCALATE (F13 floor triggered)
    # constitutional_floor_triggered: "F13"
    # next_safe_action: "Obtain F13 sovereign token or downgrade to reversible action"

    # 5. Seal — only Arif (F13 SOVEREIGN) with cryptographic signature
    r = await arifos.call_tool("arif_seal", {
        "payload": "Mount Kinabalu two-oceanics eureka — model_kinabalu_two_oceanics_2026",
        "ack_irreversible": True,
        "actor_signature": "<F13 cryptographic signature>",
        "nonce": "<fresh nonce>",
        "constitutional_chain_id": "<from judge verdict>",
        "judge_state_hash": "<from judge verdict>",
        "witness_type": "human",
        "actor_id": "arif",
        "session_id": "kinabalu-eureka-2026-07-03",
    })
    # Returns: verdict=SEAL → claim moves to "sealed" status in GEOX EGS
```

## Example 3: Falsification Test Trigger (LC-001 style)

Use this pattern when you have a hypothesis capsule (e.g. `KINABALU-LAYANG-BASEMENT-FALSIFICATION-LC001-2026-06-29.md`) and want to attach falsification tests as evidence:

```python
# Read the capsule from disk
capsule = open("/root/GEOX/forge_work/KINABALU-LAYANG-BASEMENT-FALSIFICATION-LC001-2026-06-29.md").read()

# Attach the capsule as an internal_brief
await geox.call_tool("geox_egs_evidence_attach", {
    "claim_id": claim_id,
    "description": "Acquisition Law Capsule LC-001: 4 competing hypotheses (H1 Oceanic, "
                   "H2 Detachment, H3 Volcanic-Continent, H4 Shale-Tectonic) with full "
                   "falsification matrix. Basement Vp 5.0-6.5 km/s discriminates H1 vs H2.",
    "evidence_kind": "internal_brief",
    "supporting": True,
    "source": "forge_work/KINABALU-LAYANG-BASEMENT-FALSIFICATION-LC001-2026-06-29.md",
    "created_by": "GEOX",
    "strength": "structural",
})
```

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `SESSION_REQUIRED` on raw curl | Pydantic strict rejects `session_id` in arguments | Use FastMCP Python client (Path A in SKILL.md) |
| `Unknown reason_type: X` | `geox_egs_evidence_reason` needs enum | Try: support, challenge, audit, verify, validate, consistency, all |
| `Unknown mode: analyze` | `arif_think` mode is enum | Valid: plan, reflect, critique, metabolize, reason, evaluate |
| `L11 AUTH: session_id not found` | Session expired across clients | Re-initialize via `arif_init(mode="init")` first |
| `Output validation error: outputSchema` | `arif_judge` missing required field | Add all 6: actor, intent, capability, domain, reversibility, blast_radius |
| `ESCALATE F13` | Expected for irreversible+federation-wide | This is correct behavior — report to Arif (F13) |
| Layer not_found | Wrong URI pattern | Use `geox://layers/<layer_id>/package` (e.g. `sabah.basin_outline.v3`) |
| Ontology not_found | Wrong URI pattern | Use `geox://resources/ontology/<name>.yaml` (NOT `geox://ontology/...`) |
| `'list' object has no attribute 'contents'` | FastMCP client API quirk | Use `r[0].text` not `r.contents[0].text` |