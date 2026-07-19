# v3 → v4 Tightening Pattern — Peer-Review Correction Audit

**Date sealed:** 2026-07-03
**Domain:** arifOS / GEOX Earth Graph + manuscript publication
**Use this when:** A peer review (human or LLM) has caught overclaims in a v3 manuscript and you need to forge a v4 that integrates the corrections. Reusable template.

---

## 1. The Four Overclaim Patterns ChatGPT Caught

| # | v3 Overclaim | v4 Correction |
|---|---|---|
| 1 | Absolute language: "continental crust never subducted" | Reframe: "did not behave like active dense slab subduction — it collided, underthrusted at shallow depth, shortened, and jammed the system" |
| 2 | Hypothesis stated as fact: "Jurassic carbonate décollement" | Mark as HYPOTHESIS; name the killer tests pending |
| 3 | Single-cause reductionism: "uplift = granite density alone" | Multicausal framing: extension + lithospheric drip/delamination + isostasy + erosion + pluton buoyancy |
| 4 | Wrong regime framing: "active oceanic slab today" | "Post-subduction interference overprint on a frozen Proto-SCS geometry" |

**General rule:** If your headline can be attacked with a single peer-reviewed paper, you overclaimed. Falsifiable-and-correct > unfalsifiable-and-right.

---

## 2. The GEOX Workflow to Forge v4

```python
# File: /tmp/geox_tighten.py
# Run: /root/GEOX/.venv/bin/python3 /tmp/geox_tighten.py

import asyncio, json
from fastmcp.client import Client

async def safe(c, name, args):
    try:
        r = await c.call_tool(name, args)
        txt = "".join(b.text for b in (r.content or []) if hasattr(b, "text"))
        try: return json.loads(txt)
        except: return {"_raw": txt[:2000]}
    except Exception as e:
        return {"_error": str(e)[:500]}

async def main():
    async with Client("http://localhost:8081/mcp") as c:
        # 1) Create the v4 claim — title must reflect the correction
        new_claim = await safe(c, "geox_egs_claim_create", {
            "title": "<CORRECTED HEADLINE — use 'as a ... node', 'interference', or 'multicausal' framing>",
            "statement": (
                "<v4 statement — explicitly state:\n"
                "  (a) what is OBSERVED (rocks, ages, seismic)\n"
                "  (b) what is INTERPRETED (mechanism, causation)\n"
                "  (c) what is HYPOTHESIS (each one named, killer tests listed)\n"
                "  (d) what the falsifiable target is (NOT the unfalsifiable 'never' claim)>"
            ),
            "domain": "<same as v3>",
            "author": "<your_id>_v4",
        })
        CID = new_claim["claim_id"]

        # 2) Attach the original supporting evidence (re-anchor the truth)
        for name, desc in ORIGINAL_EVIDENCE:
            await safe(c, "geox_egs_evidence_attach", {
                "claim_id": CID, "description": desc, "evidence_kind": "...",
                "supporting": True, "source": name, "created_by": "<your_id>_v4",
                "strength": "strong",
            })

        # 3) Attach the CORRECTIONS as supporting=False evidence
        #    These are the rival hypotheses, the hypothesis qualifiers, the framing corrections
        for name, desc in CORRECTIONS:
            await safe(c, "geox_egs_evidence_attach", {
                "claim_id": CID, "description": desc, "evidence_kind": "tectonic_correction",
                "supporting": False, "source": name, "created_by": "<your_id>_v4",
                "strength": "moderate",
            })

        # 4) File the formal challenge with the peer-reviewer as challenger
        await safe(c, "geox_egs_claim_challenge", {
            "claim_id": CID,
            "challenge_statement": (
                "Reviewer (<name>, <date>) verdict on v3: <verdict>. "
                "v4 corrects the overclaims as follows: <list corrections>. "
                "v3's '<overclaim headline>' framing has been retracted in v4."
            ),
            "challenger": "reviewer_<name>_<date>",
            "evidence_description": "Peer review of v3 overclaims",
            "evidence_kind": "peer_review",
        })

asyncio.run(main())
```

---

## 3. The Manuscript Patch (PDF / Markdown)

For each section, apply these patches:

### §1 Introduction / Headline
- Replace absolute language with conditional/reframe language.
- Add a one-line **"What this paper does NOT claim"** box at the top.

### §2 Contrast Score Table
- Add a row for the **v3 headline** with the overclaim scoring. Mark it as **"Falsified by peer review, retracted in v4."**
- Keep v4 scores side-by-side for direct comparison.

### §3 Mechanism Section (the geology)
- Restructure any "X alone caused Y" into a numbered list: "(a) factor 1 (b) factor 2 (c) factor 3".

### §4 The Hypothesis Section
- Add a header: **"§4.X HYPOTHESIS — pending killer tests"**.
- List the killer tests explicitly. State "Not yet executed. Claim remains CONSISTENT not DIAGNOSTIC."

### §5 Conclusion
- New headline: **"<Subject> is best read as a post-subduction / multicausal / interference node, not as <old v3 framing>."**
- Add a sentence: "v3 of this manuscript was overclaimed. The overclaims are listed in Appendix A and retracted."

### Appendix A — v3 → v4 Correction Audit
Insert a one-page table:
| v3 Overclaim | v4 Correction | Evidence ID (GEOX) | Reviewer |

### Appendix B — GEOX Audit Trail
List the v4 claim_id, the evidence_ids (split into FOR and AGAINST), the challenge_id, and the final confidence score.

---

## 4. The Confidence Drop Is The Point

The v3 claim was at confidence 0.72. The v4 claim is at confidence 0.50. **That drop is the system working correctly.** It happened because:

1. The corrections were attached as `supporting=False` evidence.
2. The peer-review challenge was filed as a permanent provenance record.
3. The rival hypotheses were named explicitly.

**If your v4 confidence is HIGHER than v3, you didn't actually integrate the corrections — you just rebranded them.**

---

## 5. The Five-Rule Discipline (Post-Mortem)

These are the five rules that, if followed at v3 draft time, would have prevented the overclaims:

1. **Headline check:** Does the headline use absolute language ("never", "always", "all", "none")? If yes, reframe to "is not active X" or "did not behave like Y".
2. **Mechanism multiplicity check:** Is any phenomenon reduced to a single cause? If yes, expand to multicausal. Geology is almost never monocausal.
3. **Rival-naming check:** Are the rival hypotheses named in the claim text, not just cited? If no, the claim is unfalsifiable.
4. **Killer-test check:** For each named hypothesis, is there an observation that would kill it? If no, it's not yet a hypothesis — it's a speculation.
5. **Pre-publication peer review check:** Has a reviewer (human or LLM, not the author) critiqued the v3 draft? If no, the manuscript is a draft, not a publication candidate.

---

## 6. The Institutional Epistemic-Sink Warning

**The same failure mode ChatGPT named for PETRONAS exists inside arifOS / GEOX.** It manifests as:

- High-confidence claims with no `supporting=False` evidence attached.
- "Tight" manuscripts that have been iterated many times by the author but never critiqued externally.
- Workflows where confidence only goes UP after attaching more evidence.
- Auto-seal of claims that should have escalated to F13.

The cure is **institutions that require falsification tests before budget, not the absence of institutions.** The GEOX 4-hypothesis matrix (e.g. GEOX-LC-001) is the operational form of this discipline. Use it on your own federation's output, not just on petroleum geology.

---

*Provenance: Kinabalu Two-Oceanics v3→v4 audit, 2026-07-03. ChatGPT peer review. arifOS Federation. DITEMPA BUKAN DIBERI.*
