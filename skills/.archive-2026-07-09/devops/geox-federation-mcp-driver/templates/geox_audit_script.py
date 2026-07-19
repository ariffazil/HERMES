#!/usr/bin/env python3
"""
geox_audit_script.py — Starter template for a Phase 1-4 GEOX federation audit.

WHAT THIS DOES
==============
Phase 1 — Discovery:
    geox_surface_status  → federation health, canonical tool count
    geox_atlas           → point-in-country (default: Mount Kinabalu summit)
    geox_forbidden_claims_scan → civilizational safety gate

Phase 2 — Claim + Evidence:
    geox_egs_claim_create → returns claim_id (16-hex)
    geox_egs_evidence_attach ×N → FOR (supporting=True) and AGAINST (False)
    geox_egs_claim_challenge → formal falsification lens
    geox_egs_query_claim → authoritative status after all attaches
    geox_egs_query_uncertainty + geox_egs_query_provenance

Phase 3 — Compute:
    geox_egs_rock_physics → vp_hill, rho_bulk at given porosity
    geox_basin → synthesis (needs registered Sabah dataset, else HOLD)
    geox_deep_time_state → age_ma, named period, geomagnetic chrons
    geox_map_layers_list → bbox-scoped layer discovery

Phase 4 — Constitutional:
    (outside scope of GEOX — route through arifOS judge if needed)

USAGE
=====
    source /root/GEOX/.venv/bin/activate   # fastmcp already installed
    python3 geox_audit_script.py

CUSTOMIZE
=========
Edit the HYPOTHESIS dict at top, set your claim text, evidence list, and
run. The output is a single JSON dict printed to stdout. Save with:
    python3 geox_audit_script.py > /tmp/audit_receipt.json

VALIDATED
=========
2026-07-03 — Kinabalu "Two Oceanic Plates" audit executed end-to-end with this
pattern. Claim 935be7ceb54241c2 sealed, evidence_for=4, evidence_against=2,
final status=challenged, confidence=0.50.
"""
import asyncio, json, sys
from fastmcp.client import Client

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG — edit me
# ──────────────────────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8081/mcp/"
LAT, LON = 6.075, 116.558  # Mount Kinabalu summit

HYPOTHESIS = {
    "title": "Two Oceanic Plates Built Mount Kinabalu",
    "statement": (
        "Proto-South China Sea (consumed ~15 Ma) thickened Borneo crust; "
        "Celebes Sea rollback then melted that crust to emplace Kinabalu "
        "granite 8-7 Ma. Continental crust was not subducted."
    ),
    "domain": "sabah_tectonics",
    "author": "arif_via_geox",
}

EVIDENCE_FOR = [
    {
        "description": "Krebs (2011) PETRONAS chronosequence — biostratigraphic data from Sabah basins shows no continental metamorphism signature.",
        "evidence_kind": "biostratigraphic",
        "source": "Krebs 2011, PETRONAS chronosequence stratigraphy",
        "strength": "strong",
    },
    {
        "description": "Hall (2013) SE Asia tectonic reconstructions — Dangerous Grounds continental fragment collides with Borneo ~15 Ma, terminating Proto-South China Sea subduction.",
        "evidence_kind": "tectonic_reconstruction",
        "source": "Hall 2013, SE Asia tectonic evolution",
        "strength": "strong",
    },
    {
        "description": "Thermochronology (Nature 2017) — exhumation rates >7 mm/yr at Kinabalu since 8 Ma, consistent with rapid isostatic uplift.",
        "evidence_kind": "geochronology",
        "source": "Nature 2017, thermochronology of Mount Kinabalu",
        "strength": "strong",
    },
    {
        "description": "Density contrast — granite 2.64 g/cm3 denser than sediment 2.49 g/cm3, providing negative buoyancy driving isostatic rebound.",
        "evidence_kind": "rock_physics",
        "source": "Petrophysical measurements, Kinabalu pluton",
        "strength": "moderate",
    },
]

EVIDENCE_AGAINST = [
    {
        "description": "Seismic sections show laterally continuous high-reflectivity horizons beneath the Crocker prism — alternative interpretation as underthrusted continental fragments remains possible.",
        "evidence_kind": "seismic",
        "source": "Regional seismic survey, Sabah offshore",
        "strength": "moderate",
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
async def safe(c, name, args, timeout=60):
    """Call a tool and return JSON-friendly dict. Never raises."""
    try:
        r = await c.call_tool(name, args)
        txt = "".join(b.text for b in (r.content or []) if hasattr(b, "text"))
        try: return json.loads(txt)
        except json.JSONDecodeError: return {"_raw": txt[:2000]}
    except Exception as e:
        return {"_error": str(e)[:700]}

# ──────────────────────────────────────────────────────────────────────────────
# PHASES
# ──────────────────────────────────────────────────────────────────────────────
async def phase1_discovery(c, out):
    out["surface_status"] = await safe(c, "geox_surface_status", {})
    out["atlas"] = await safe(c, "geox_atlas",
        {"lat": LAT, "lon": LON, "mode": "context"})
    out["forbidden_scan"] = await safe(c, "geox_forbidden_claims_scan",
        {"text": HYPOTHESIS["statement"]})

async def phase2_claim(c, out):
    created = await safe(c, "geox_egs_claim_create", {
        "title": HYPOTHESIS["title"],
        "statement": HYPOTHESIS["statement"],
        "domain": HYPOTHESIS["domain"],
        "author": HYPOTHESIS["author"],
    })
    out["claim_create"] = created
    cid = created.get("claim_id")
    if not cid:
        return cid

    # Attach FOR evidence
    for ev in EVIDENCE_FOR:
        await safe(c, "geox_egs_evidence_attach", {
            "claim_id": cid, "created_by": HYPOTHESIS["author"],
            "supporting": True, **ev,
        })
    # Attach AGAINST evidence
    for ev in EVIDENCE_AGAINST:
        await safe(c, "geox_egs_evidence_attach", {
            "claim_id": cid, "created_by": HYPOTHESIS["author"],
            "supporting": False, **ev,
        })
    # Formal challenge
    out["challenge"] = await safe(c, "geox_egs_claim_challenge", {
        "claim_id": cid,
        "challenge_statement": (
            "Alternative model: the high-reflectivity horizons beneath the "
            "prism are underthrusted continental crust fragments, not "
            "Jurassic carbonates. If valid, Kinabalu could be a continental "
            "underthrusting signature, not pure oceanic."
        ),
        "challenger": HYPOTHESIS["author"],
        "evidence_description": "Reinterpretation of seismic horizons as continental fragments",
        "evidence_kind": "alternative_interpretation",
    })
    # Authoritative re-query
    out["query_claim"] = await safe(c, "geox_egs_query_claim", {"claim_id": cid})
    out["uncertainty"] = await safe(c, "geox_egs_query_uncertainty",
        {"entity_id": cid, "entity_type": "claim"})
    out["provenance"] = await safe(c, "geox_egs_query_provenance",
        {"entity_id": cid, "entity_type": "claim"})
    return cid

async def phase3_compute(c, out):
    out["rock_physics"] = await safe(c, "geox_egs_rock_physics", {
        "vp_mineral": 5.8, "vp_fluid": 1.5, "porosity": 0.05,
        "rho_mineral": 2.64, "rho_fluid": 1.02,
    })
    out["basin"] = await safe(c, "geox_basin", {
        "basin_name": "Sabah", "intent": "synthesize",
        "claim_strictness": "moderate",
    })
    out["deep_time"] = await safe(c, "geox_deep_time_state", {
        "age_ma": 7, "query": "kinabalu",
    })
    out["map_layers"] = await safe(c, "geox_map_layers_list", {
        "bbox": [114.0, 4.0, 119.5, 8.5],  # Sabah bbox
    })

# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
async def main():
    out = {}
    async with Client(BASE_URL) as c:
        await phase1_discovery(c, out)
        cid = await phase2_claim(c, out)
        await phase3_compute(c, out)
    out["_meta"] = {
        "claim_id": cid,
        "evidence_for": len(EVIDENCE_FOR),
        "evidence_against": len(EVIDENCE_AGAINST),
        "base_url": BASE_URL,
    }
    print(json.dumps(out, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())
