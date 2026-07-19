# Kinabalu Two-Oceanics Session — Concrete Lessons (2026-07-03)

This is a session-specific reference documenting the pitfalls hit and fixes applied during the Kinabalu manuscript forge. Future agents on similar falsifiable-model tasks should **read this first** to avoid repeating the same mistakes.

## 1. Matplotlib label-overlap pitfalls

### 1.1 Title placement on wide-aspect figures
**Problem:** Title placed at center-top overlaps data labels on figures with aspect ratio >3:1.
**Fix:** Place title in upper-LEFT corner (x=45, y=7.5 for 400-unit-wide figure), not center.
**Code pattern:**
```python
ax.text(45, 7.5, 'TITLE', ha='left', fontsize=13, weight='bold',
        bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='black', alpha=0.95))
```

### 1.2 Annotation `xytext` distance from `xy`
**Problem:** Annotation labels placed too close to data points get covered by data labels.
**Fix:** Always place `xytext` at least 30-50 units away from `xy` for 400-unit-wide figures, or use `arrowprops` to draw a clear connector.

### 1.3 Decompression / kinematics labels crossing other features
**Problem:** "Decompression melt rises" label placed over Dangerous Grounds box.
**Fix:** Move to opposite side of figure (x=145 vs x=200) or use white-on-color boxed annotation that's clearly visible.

### 1.4 Vertical text rotation issues
**Problem:** `rotation=90` on text caused overlap with horizontal axis labels.
**Fix:** Don't rotate. Place horizontally to the right of vertical lines instead.

### 1.5 `bboxdict` typo (silent fail)
**Problem:** Wrote `bboxdict=None` instead of removing the parameter. Got `AttributeError: 'Text' object has no property 'bboxdict'`.
**Fix:** Just delete the parameter. Don't try to pass `None` to override.

## 2. PNG file path gotchas

### 2.1 Glob pattern typos
**Problem:** Initial `search_files` for `kinabaluscar*` returned 0 hits because there's no such file. Actual files are `KinabaluScar.png`, `kinabalu_two_oceanics_final.png`, etc.
**Fix:** Use case-insensitive patterns. Check actual filenames with `ls -la` first.

### 2.2 Aspect ratio for full manuscript pages
**Problem:** Cross-section PNG was 3971×964 px (4.1:1 aspect). On A4 portrait page, weasyprint would scale it to fit width, making it visually short.
**Fix:** Either: (a) use a `class="wide-figure"` CSS that breaks onto a separate landscape page, or (b) crop/extend the figure to a more balanced aspect. For this manuscript, fit-to-width was acceptable.

## 3. GEOX MCP session plumbing

### 3.1 FastMCP HTTP session initiation
**Pattern:** Direct curl with `MCP-Protocol-Version` header and `mcp-session-id` from initialize response works for read-only tools (`geox_atlas`, `geox_deep_time_state`) but **fails for reasoning-lane tools** (`geox_map_layers_list` returns SESSION_REQUIRED).

**Fix:** Use the FastMCP Python client (`from fastmcp import Client`), which handles session/actor plumbing correctly:
```python
client = Client("http://localhost:8081/mcp")
async with client:
    r = await client.call_tool("geox_egs_claim_create", {...})
```

### 3.2 Lane enforcement in middleware
**Discovery:** Reasoning-lane tools (most GEOX compute/visualize tools) require session_id in the **HTTP request context**, not in the body. Pydantic strict validation strips unknown body args before middleware reads them.

**Workaround:** Use FastMCP client (which sets the HTTP session header) — don't try to bypass with raw curl + session header for reasoning-lane tools.

### 3.3 Claim challenge pattern
**Discovery:** Old claims in earlier sessions become invisible to new sessions (session-scoped state). To "supersede" a claim:
1. Create a NEW claim with corrected headline
2. Attach evidence to the NEW claim
3. Add `supersedes-<old_id>` tag to the new claim for audit trail
4. Don't try to modify the old claim (it's locked in its session)

### 3.4 evidence_attach error response
**Pattern:** When claim_id is from a different session, `evidence_attach` returns `{'success': False, 'error': "Claim '<id>' not found", 'errorCode': 'GEOX_404_DATA', 'recoverable': True}`. **Don't retry** — the claim truly isn't visible. Create new claim instead.

## 4. weasyprint PDF pipeline

### 4.1 Python module not installed
**Problem:** `pip install weasyprint` blocked by PEP 668 (externally-managed-environment).
**Fix:** Use system-installed `weasyprint` binary at `/usr/local/bin/weasyprint`, which is already installed on the VPS. Don't try to pip install.

### 4.2 Image embedding
**Pattern:** WeasyPrint needs absolute paths OR a `base_url` for relative image paths.
```python
HTML(filename=html_path, base_url='/tmp/kinabalu_pdf_figures/').write_pdf(out_pdf)
# OR
weasyprint /tmp/kinabalu_pdf_figures/manuscript.html /root/output.pdf
```

### 4.3 Unknown CSS property warnings
**Observation:** `box-shadow: 2px 2px 8px rgba(0,0,0,0.1)` triggers "unknown property" warning but doesn't break the PDF.
**Fix:** Either accept the warning or replace with `border: 1px solid #ccc` for similar visual effect.

## 5. YELLOW band tightening pattern (most important)

When peer review returns:
```json
{
  "eureka_status": "REAL_BUT_UNSEALED",
  "scientific_value": "HIGH",
  "current_form": "OVERCLAIMED",
  "best_claim": "...",
  "weak_claims": ["..."],
  "publication_status": "DRAFT_AFTER_MAJOR_TIGHTENING"
}
```

**Execute:**

### 5.1 New claim with corrected headline
Create a new claim, NOT modify the old one. The old claim preserves audit trail. The new claim has:
- confidence_score **reduced** (0.72 → 0.58 for YELLOW band)
- Tags include `supersedes-<old_claim_id>` and `chatgpt-red-team-tightened`
- Statement explicitly addresses each weak_claim

### 5.2 Attach weak claims as rivals
For each weak claim from peer review, attach an `evidence_kind=rival_hypothesis_correction` entry:
- `supporting: False` (it's a rival)
- `source: "ChatGPT red-team review (2026-07-03) — based on [specific paper]"`
- `strength: moderate_rival` or `strong_rival`
- Description paraphrases the peer reviewer's concern

### 5.3 Attach falsification tests
For each named falsification test, attach as `evidence_kind=falsification_test` with `supporting: False` (it's a test, not a fact) and `strength: decisive`.

### 5.4 Rewrite manuscript
Replace absolute language ("never subducted", "is the mechanism") with hedged language ("did not behave as normal oceanic slab subduction", "is one factor among several"). Update manuscript PDF, embed new claim_id in receipt block.

### 5.5 Verdict expectation
After tightening: claim status will be `challenged` with high evidence-for count AND high evidence-against count. Confidence below 0.65. **This is the correct YELLOW band posture** — not SEAL, not VOID.

## 6. Reality-prism meta-pattern

When the manuscript exposes institutional patterns (Calhoun-like epistemic sink, committee disease, citation inertia), and the user has private life folders documenting those patterns (HAMPA cards, PROPA structural reality, LIFE decisions):

**Tie the manuscript to the personal pattern via a meta-eureka note**, not via gossip. Update HAMPA cards with "meta-pattern link" footnotes. Update INDEX.md to reflect new structure. Write the meta-pattern as a separate file (e.g. `eureka-institutional-epistemic-sink.md`) that ties multiple cards together.

**Never push these to GitHub.** The user has explicitly forbidden it. Verify with `git status -sb` after edits — files should appear as untracked or modified but never committed.

## 7. Concrete artifacts from this session

For reproducibility / future reference:

| Artifact | Path | SHA256 |
|---|---|---|
| Source PNG (poster) | /root/kinabalu_two_oceanics_final.png | 7ca8b00e...0a1f5a30 |
| Tightened PDF | /root/kinabalu_two_oceanics_full.pdf | (regenerated; check after each YELLOW cycle) |
| Manuscript HTML | /tmp/kinabalu_pdf_figures/kinabalu_two_oceanics_manuscript.html | n/a |
| Original GEOX claim (now superseded) | e12b21e3f0574267 | (session-locked) |
| Tightened GEOX claim (live) | 9cf5ec26c45f40ed | (session-locked) |
| Meta-eureka note (private) | /root/ariffazil/HAMPA/eureka-institutional-epistemic-sink.md | (private, never push) |