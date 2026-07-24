---
name: scientific-manuscript-forge
title: Scientific Manuscript Forging — Falsifiable Model Manuscripts with GEOX Receipts
description: "Forge publication-grade scientific manuscripts for falsifiable domain models (geology, biology, economics, etc.). Pipeline: domain research → matplotlib figures → HTML wrapper with print CSS → weasyprint PDF → GEOX claim registration + evidence ledger. Includes the 'YELLOW band tightening' discipline for honest peer-review cycles."
version: 1.0.0
author: Hermes (for Arif F13 SOVEREIGN)
license: MIT
dependencies: [matplotlib, numpy, weasyprint, pandoc, Pillow]
platforms: [linux]
metadata:
  hermes:
    tags: [Manuscript, Scientific Writing, Falsifiable Models, Geology, PDF, weasyprint, matplotlib, GEOX, Evidence Ledger, Peer Review, YELLOW Band, Tightening]
    category: research
    related_skills: [arxiv, research-paper-writing, spike]
    requires_toolsets: [terminal, files, vision]

---

# Scientific Manuscript Forging — Falsifiable Model Manuscripts

End-to-end pipeline for producing **publication-grade scientific manuscripts** for falsifiable domain models. Distinct from ML paper writing (`research-paper-writing`) in three ways:

1. **Domain is not ML** — geology, biology, economics, climate, etc. The output is a falsifiable hypothesis manuscript, not a benchmark-against-SOTA paper.
2. **Output format is HTML+matplotlib+weasyprint, not LaTeX** — faster iteration, native PNG embedding, easier to fix label overlaps between rounds.
3. **Epistemic posture is "challenged with rivals"** — every claim carries explicit falsification tests and rival interpretations. The manuscript is **evidence-laned, not sealed**.

The pipeline ends with a GEOX claim registration and evidence ledger that outlives any single manuscript revision.

## When to use this skill

Use when the user has:
- A **falsifiable scientific hypothesis** with named rival interpretations
- **Measured data** (rock physics, genomic sequences, economic indicators) to anchor
- A **peer-review-style** recipient (academic journal, GEOX jury, ChatGPT verdict, sovereign F13 seal)
- Time pressure — the manuscript needs to be forged within a session, not over weeks

Do NOT use this skill for:
- ML benchmark papers (use `research-paper-writing`)
- Internal reports without falsification tests
- Marketing material or non-scientific writeups

## The Pipeline (7 phases)

### Phase 0: Stack & Venv Probe (1 min)

Before installing anything, probe what's already present:

```bash
ls /root/GEOX/.venv/bin/python* 2>/dev/null   # canonical GEOX venv
which weasyprint pdflatex                       # weasyprint wins for this class
/root/GEOX/.venv/bin/python3 -c "import reportlab; print(reportlab.__version__)" 2>&1
```

**v3 lesson (2026-07-03):** `reportlab` was missing in the GEOX venv and `pip` itself was absent (PEP 668 + no `ensurepip`). Fix:

```bash
/root/GEOX/.venv/bin/python3 -m ensurepip --upgrade    # bootstraps pip
/root/GEOX/.venv/bin/python3 -m pip install --quiet reportlab
```

This is faster and cleaner than a new venv. Default to **extending the existing GEOX venv** for federation-related work.

### Phase 1: Domain Research + Corpus Discovery (10–20 min)

Before forging figures, **read the corpus.** Don't trust memory.

```
1. List available resources via arifOS / GEOX MCP (resources/list, resources/read)
2. Check ontology files (sabah_basin_strat.yaml, GEOX corpus schemas)
3. Read internal briefs (geox_pscs_cot_brief_v2.md, PSCS briefs)
4. Look for existing eureka capsules, acquisition law capsules, knowledge graph entries
5. Catalog the rival hypotheses explicitly (GEOX-LC-001-style)
```

**Output:** A short bulleted list of:
- Domain facts (measured values, ages, densities, Vp)
- The 3-5 named rival hypotheses
- The falsification matrix (which test kills which hypothesis)
- The "evidence ledger" — 5-10 publications + 3-5 internal artifacts

### Phase 2: Figure Forge (matplotlib, 30–60 min)

For each figure (typical: 4-7 in a manuscript):

```
1. Write matplotlib script, save to /tmp/<name>_fig<N>.py
2. Render to PNG at 200 dpi
3. vision_analyze the PNG: ask "any label overlap? unreadable text? scientific accuracy?"
4. If issues found: patch coordinates, re-render, re-check
5. Iterate until all labels readable, no overlaps, scientific content correct
```

**Lessons learned (THIS SESSION):**
- Title blocks overlap data — place title in upper-LEFT not center for wide figures
- Bbox labels (`bbox=`) work; `bboxdict=` is a typo — fails with AttributeError
- Annotation `xytext` needs to be far enough from `xy` to clear the data
- For wide-aspect figures (4:1+), put depth/age axis labels INSIDE the figure on the left edge, not below
- Always include scale bar + north arrow (or equivalent orientation marker)

**Output:** 4-7 PNG figures at /tmp/<name>_figures/fig[1-7]_*.png

### Phase 3: Manuscript HTML (weasyprint-grade, 30–45 min)

Build a single HTML file with:
- Embedded figures via `<img src="fig<N>.png">` (relative paths)
- CSS `@page` rules: A4, 2cm margins, header/footer with title + page numbers
- Section structure: Abstract → Core claim → Regional context → Main figure(s) → Rock physics/data → Timeline → Falsification matrix → Receipts → Conclusions → References
- Tables for the falsification matrix and evidence ledger
- Code blocks for SHA256 fingerprints and GEOX claim IDs

**Use weasyprint, NOT pandoc or LaTeX for this class of work.** Reasons:
- Native PNG embedding (no conversion step)
- CSS print rules are easier to iterate than LaTeX preamble
- box-shadow / flexbox / grid work natively
- Output is fast (seconds, not minutes)

**Output:** /tmp/<name>_figures/<name>_manuscript.html

### Phase 4: PDF Render + Visual Verify

```
$ weasyprint manuscript.html manuscript.pdf
$ pdfinfo manuscript.pdf  # check page count, size
$ pdftoppm -png -r 100 -f N -l N manuscript.pdf preview_pageN
$ vision_analyze preview_pageN.png  # verify each major page
```

**Iterate** until every page renders correctly with no broken figures or cut-off text.

**Output:** /root/<name>_full.pdf with SHA256 fingerprint

### Phase 5: GEOX Claim Registration (CRITICAL)

**Every falsifiable model manuscript ends with a live GEOX claim.** This is what makes it more than prose.

```python
# Via FastMCP Python client (preferred — handles session plumbing)
from fastmcp import Client

client = Client("http://localhost:8081/mcp")
async with client:
    # Create claim
    r = await client.call_tool("geox_egs_claim_create", {
        "title": "Falsifiable statement of the model",
        "statement": "Detailed falsifiable assertion with explicit boundary conditions",
        "domain": "tectonic_stratigraphy",  # or relevant domain
        "author": "Arif (F13 SOVEREIGN)",
        "entity_type": "tectonic_model",  # or relevant type
        "entity_id": "model_<shortname>_v<N>",
        "confidence_score": 0.72,  # CAP at 0.90 per F7 HUMILITY
        "tags": ["...", "..."],
    })
    claim_id = json.loads(r.content[0].text)["claim_id"]

    # Attach evidence (5+ supporting + 2+ rivals)
    for ev in evidence_for:
        await client.call_tool("geox_egs_evidence_attach", {
            "claim_id": claim_id, **ev,
        })
    for rival in evidence_against:
        await client.call_tool("geox_egs_evidence_attach", {
            "claim_id": claim_id, "supporting": False, **rival,
        })

    # Query to verify status upgraded to 'challenged'
    r = await client.call_tool("geox_egs_query_claim", {"claim_id": claim_id})
```

**Why this matters:** A manuscript without a live claim is just text. A manuscript with a live claim is **auditable, falsifiable, and traceable**. The claim_id lives in VAULT999 forever.

## Phase 5.5: AI Peer-Review Loop (NEW 2026-07-03)

Before applying the YELLOW band tightening, **run a second AI agent as red-team peer reviewer** on the sealed v1 manuscript. This converts "self-imposed tightening" into "external review-driven tightening" — which is the difference between confident prose and a defensible manuscript.

**The harness:**

```bash
# 1. Write the prompt file (zen: one symbol + one term; structured; named inputs/outputs)
# /tmp/opencode_prompt_<topic>.md
# Include:
#   - exact paths to the v1 PDF, supporting figures, GEOX-LC-001 capsule, ontology
#   - the 5 questions to answer (falsification tests, weak claims, institutional read,
#     biographical mirror if relevant, acquisition law)
#   - exact output paths (one human-readable MD, one machine-readable JSON)
#   - zen: max 5-line stdout summary

# 2. Run via the LOCAL opencode server (gated, persistent session)
PROMPT=$(cat /tmp/opencode_prompt_<topic>.md)
opencode run --attach http://127.0.0.1:4096 --format default \
  --title "<topic> v1 peer-review" "$PROMPT" > /tmp/opencode_run.log 2>&1

# 3. Poll the log; the agent writes the review files itself
tail -20 /tmp/opencode_run.log
ls -la /root/wealth/domains/<relevant>/<topic>_review_<date>.md
```

**Why `--attach` (not bare `opencode run`):**
- The VPS already runs `opencode serve --port 4096` as a long-lived process (visible in `ps aux | grep opencode`)
- Bare `opencode run` forks a new ephemeral session — loses any tool/MCP context, burns warmup time
- `--attach` reuses the running server's session, MCP wiring, and tool cache
- This is the same `opencode` instance the Telegram opencode-bot routes through

**Flag gotchas (don't repeat my mistake):**
- The CLI flag is `--prompt` in some tools but **NOT in opencode** — opencode takes a positional `message` arg
- `--attach` is required if you want the long-lived server; without it, opencode spawns a new session
- `--format default` for human-readable output; `--format json` for raw JSON events
- Don't pass `--title` and expect it to appear in `opencode session list` — the title is just for the CLI's display
- The bare invocation `opencode run --prompt "..."` is the most common mistake — it shows the CLI help and exits silently. Use the positional `message` form above.

**Output contract for the reviewer agent:**

```markdown
# ⚖ PEER-REVIEW MEMO — <topic> v1
**Verdict:** STRONG_WITH_WEAKNESSES | REAL_BUT_UNSEALED | SEAL | VOID
**Confidence:** 0.NN (with breakdown by evidence kind)

## 1. Falsification tests (cheapest discriminator per hypothesis)
## 2. N weakest claims (with strengthen-with / kill-with)
## 3. Institutional pattern read (if applicable)
## 4. Biographical mirror honesty audit (if applicable)
## 5. Acquisition law recommendation (top 3)
## Appendix — evidence labels used (OBS/DER/INT/SPEC counts)
```

Plus a `/tmp/<topic>_review.json` summary with `{verdict, confidence, weakest_3, top_3_acquisitions, ...}` for downstream automation.

**After the review lands:** apply the YELLOW band tightening (Phase 6) using the reviewer's named weak claims as the explicit correction targets. Cite the reviewer by ID (`reviewer_chatgpt_2026-07-03` or `reviewer_opencode_<date>`) in the GEOX `challenger` field of the new claim challenge — this preserves the provenance chain.

## Phase 5.6: Cross-Organ Deployment (when artifact spans multiple organs)

**Trigger:** the manuscript or artifact carries content that lives in multiple federation organ lanes (e.g. a geological claim with an institutional-pattern read spans GEOX + WEALTH).

**The 4-step pattern (full detail in `references/cross-organ-deployment-pattern.md`):**

1. **Each organ stays in its lane.** GEOX owns physics; WEALTH owns capital/ institutional; AAA owns control/agent identity; arifOS owns constitution/judgment.
2. **Use a shared `claim_id` as the cross-organ anchor.** GEOX creates the claim, returns `claim_id`, WEALTH attaches evidence referencing the same `claim_id`. The `challenger` field (e.g. `reviewer_chatgpt_2026-07-03`) is the permanent cross-organ link.
3. **Each organ pushes from its own repo.** Don't push cross-organ content from one organ's repo. The `git checkout -b forge/...-date` + commit + push + merge-to-main happens on the WEALTH repo for the institutional artifacts, on the GEOX repo for the physics artifacts, etc.
4. **Each commit message carries the cross-organ anchor.** The WEALTH commit references the GEOX `claim_id`. The GEOX commit (if any) references the WEALTH artifacts. Reviewer reading either side finds the other.

**The 4 anti-patterns to avoid:**
- Cross-organ content in one repo (pollutes the lane)
- Same artifact committed to both repos (SHA256 divergence)
- Git push from outside the right repo
- Forgetting the merge-to-main step (artifact on a branch, unreachable to main clones)

**The 5-command reproducible recipe** (full in reference file):
```bash
cd /root/<organ-repo>           # 1. verify
git checkout -b forge/<topic>   # 2. branch
git add <files> && git commit   # 3. commit (with Companion: anchor)
git push -u origin forge/<topic> # 4. push feature
git checkout main && git merge forge/<topic> --no-ff && git push origin main # 5. merge + push main
```

**The honest limit:** this pattern handles *routine* cross-organ artifacts. Federation-wide merges need arifOS judge + F13 SOVEREIGN. Multi-agent commits need signed attribution. For those, escalate to AAA + arifOS.

## Phase 6: YELLOW Band Tightening (CRITICAL)

When peer review (ChatGPT, GEOX jury, human referee) returns a verdict like:
- "PARTIAL EUREKA — not sealed"
- "evidence: L2/L3, band: YELLOW"
- "real_but_overclaimed"

**Do NOT defend.** Execute the tightening cycle:

```
1. Create NEW claim with corrected headline (don't modify old — preserves audit trail)
2. Reduce confidence_score (0.72 → 0.58 is appropriate for YELLOW)
3. Attach weak-claim-as-rival evidence (4+ explicit rivals)
4. Attach falsification tests as evidence-against (named killer tests)
5. Rewrite manuscript headline: "X is a [state]" not "X is [absolute]"
6. Replace "never/always/only" with "did not behave as [X]"
7. Update manuscript PDF; embed new claim_id in receipt block
```

**The original claim is preserved** as `superseded-by-<new_id>`. The audit chain is intact.

## Output Receipts

Every manuscript forge should produce:

```
/root/<name>_full.pdf                      # The manuscript, ~10-15 pages
/tmp/<name>_figures/fig[1-7]_*.png         # Source figures
/tmp/<name>_figures/<name>_manuscript.html # Source HTML
/root/<name>_receipt.md                    # Audit trail with SHA256
GEOX claim ID: <claim_id>                 # Live in GEOX EGS
Evidence ledger: <N> for / <M> against
arifOS verdict: SEAL or ESCALATE
```

## Failure Modes (Anti-Patterns)

1. **Defending the overclaim** — when peer review says YELLOW, the right move is tighten, not argue
2. **Skipping the rivals** — every claim without rivals is brittle; rivals make it strong
3. **Matplotlib labels with bbox=collision** — always vision_analyze every figure before stitching
4. **LaTeX for non-ML** — too slow for falsifiable model manuscripts; weasyprint wins
5. **Pushing the PDF to git** — manuscripts usually have SHA256-bound content; treat as artifacts not code
6. **Missing the GEOX claim** — a manuscript without a live claim is just prose; always register

## User-Specific Lessons (Arif F13 SOVEREIGN)

When the user asks for a manuscript, he expects:
- **Brutal honesty** over diplomatic softening — if the model is overclaimed, SAY SO before generating
- **Tightening** over defense when peer review returns YELLOW band
- **Live evidence ledger** with explicit rivals + falsification tests (not "evidence for" only)
- **No ceremonial footer** in the artifact — receipts live in the body or audit section
- **SHA256 + claim_id embedded** in the manuscript so it's traceable to its evidence

## Related Skills
- `research/research-paper-writing` — ML papers (LaTeX, benchmark-driven). Different class.
- `research/arxiv` — paper search/discovery (input to Phase 1)
- `devops/geological-artifact-publication` — when the manuscript IS a geological model with to-scale cross-sections (the 6-panel Kinabalu final poster is the canonical pattern)
- `devops/geox-federation-mcp-driver` — for driving GEOX/WEALTH/arifOS MCP tools to back the manuscript with live evidence
- `devops/institutional-epistemic-sink-forensics` — when the manuscript's meta-pattern is the Calhoun institutional sink (e.g. pairing a geological model with the institution that produced it — validated 2026-07-03 with Kinabalu two-oceanics + Petronas audit)
- `software-development/spike` — throwaway experiments (good fit for Phase 2 figure iterations)
- `autonomous-ai-agents/claude-code` — delegate coding subroutines (good for parallel figure generation)
- `autonomous-ai-agents/opencode` — for in-federation peer-review loop (Phase 5.5)

## Reference files
- `references/kinabalu-session-2026-07-03-lessons.md` — v3 lessons (matplotlib, GEOX plumbing, YELLOW band cycle, weasyprint)
- `references/kinabalu-v4-session-2026-07-03.md` — v4 lessons (local OpenCode peer-review harness, cross-organ deployment, venv bootstrap, PR branch pattern, biographical-mirror edit discipline)
- `references/cross-organ-deployment-pattern.md` — the GEOX→WEALTH→merge-to-main pattern for federation artifacts that span multiple organ repos (lesson 4 + 5 from v4, distilled)
- `references/submission-readiness-audit-when.md` — when to invoke `submission-readiness-audit` vs this skill (deadline-driven vs single-artifact)
- `references/research-grade-assessment-checklist.md` — 5-criteria checklist for evaluating whether a paper is research-grade vs. conceptual essay. Use when Arif asks "is this paper good enough for peer review?"
- `references/prior-art-archiving-workflow.md` — Wayback Machine + EarthArXiv/arXiv + author cleanup for defensive timestamping. Use when a paper exists only on a personal site and needs independent proof of publication date.

## User-Specific Lessons (Arif F13 SOVEREIGN) — continued

When Arif asks "is this research-grade?", he wants a direct verdict, not diplomatic hedging. Lead with "No" or "Yes", then the criteria. The session where he asked "So u think this is research grade paper?" and I gave a 6-point honest breakdown was accepted immediately — he does not want softening, he wants the truth fast so he can decide what to do next.