# Hermes Skills Library Audit Report
**Date:** 2026-07-15  
**Auditor:** Hermes Agent (automated)  
**Scope:** `/root/.hermes/skills/` (active + archived)

---

## 1. Total Count

| Metric | Count |
|--------|-------|
| **Active skills** | 158 |
| **Archived skills** | 86 |
| **Total all-time** | 244 |
| **Disk usage (total)** | 18 MB |
| **Disk usage (archive)** | 3.6 MB |
| **Empty category dirs** | 10 |
| **Empty references/scripts/templates dirs** | 15+ |

---

## 2. Category Breakdown (Active)

| Category | Count | Notes |
|----------|-------|-------|
| devops | 29 | Largest. Heavy VPS/federation/arifOS overlap |
| creative | 28 | Image gen, diagrams, PDFs, design tools |
| research | 24 | Dossiers, forensics, analysis, papers |
| governance | 20 | Constitutional, cognitive, sovereignty |
| media | 11 | Audio, music, OCR, video, TTS |
| productivity | 10 | Docs, PDFs, workspace tools |
| trading | 5 | MT5, signals, charts |
| software-development | 5 | Audits, knowledge stores |
| social-media | 4 | Telegram, X/Twitter, IG |
| note-taking | 1 | Obsidian |
| email | 1 | Himalaya |
| geology | 1 | GEOX competitive intelligence |
| **Standalone (root-level)** | 17 | Various — see naming section |

**Empty category directories (0 skills, ghost dirs):**
`github`, `mlops`, `smart-home`, `data-science`, `autonomous-ai-agents`, `apple`, `capital`, `dream-engine`, `wellness`

---

## 3. Duplicates & Redundancies Found

### 🔴 CRITICAL — VPS Operations (7 skills, near-identical scope)

All describe "smoketest, state machine, circuit breaker, rollback, dead-man's switch" for VPS self-healing:

| Skill | Description (truncated) |
|-------|------------------------|
| `vps-operations` | "VPS optimization, cleanup, and health auditing" |
| `vps-machine-health` | "Full VPS machine health optimization" |
| `vps-agentic-ops` | "Autonomous VPS operations — smoketest, state machine..." |
| `vps-autonomous-ops` | "Build and operate autonomous VPS control loops" |
| `vps-autonomous-response` | "Build autonomous VPS monitoring and response layers" |
| `agentic-vps-operations` | "Autonomous VPS monitoring and self-healing — Tier 1" |
| `autonomous-vps-response` | "Tier 1 Active Response pattern" |

**Recommendation:** Consolidate into 2 skills max: `vps-operations` (cleanup/health) and `vps-autonomous-ops` (self-healing loops).

### 🟡 Music Pipeline (4 skills, overlapping)

| Skill | Category | Scope |
|-------|----------|-------|
| `music-generation` | media | Full pipeline: concept → lyrics → generation |
| `music-intelligence` | media | Governed generation + somatic scoring |
| `heartmula` | media | Suno-like generation from lyrics + tags |
| `songwriting-and-ai-music` | creative | Songwriting craft + Suno prompts |

**Recommendation:** Merge into `music-generation` with sub-sections. `heartmula` and `songwriting` are subsets.

### 🟡 Audio Analysis (3 skills, overlapping)

| Skill | Scope |
|-------|-------|
| `audio-analysis` | Python DSP modules — librosa, MFCC, spectral |
| `audio-feature-analysis` | Programmatic analysis — chroma, motif, spectral |
| `songsee` | Audio spectrograms/features via CLI |

**Recommendation:** Consolidate into `audio-analysis`.

### 🟡 OCR / Document Extraction (3 skills, overlapping)

| Skill | Category | Scope |
|-------|----------|-------|
| `ocr` | media | Image OCR via Tesseract |
| `ocr-and-documents` | productivity | PDF/scan text extraction |
| `document-intelligence` | productivity | VLM-first document extraction |

**Recommendation:** Consolidate into `document-intelligence` (superset).

### 🟡 Image Generation (3 skills, partial overlap)

| Skill | Scope |
|-------|-------|
| `comfyui` | Local ComfyUI pipeline |
| `lightweight-image-generation` | Free APIs, no local install |
| `token-plan-image` | Qwen Token Plan models |

**Recommendation:** Keep all 3 — they serve genuinely different use cases (local vs API vs specific model).

### 🟡 Image Editing (2 skills, near-duplicate)

| Skill | Scope |
|-------|-------|
| `image-text-editing` | "Edit existing images to add/replace/remove text using PIL" |
| `screenshot-editing` | "Edit existing screenshots/images to add/modify content. PIL/Pillow image surgery" |

**Recommendation:** Merge into `image-editing`.

### 🟡 Screen/Visual Replication (2 skills, near-duplicate)

| Skill | Scope |
|-------|-------|
| `screen-replica` | "Replicate a specific app screen or UI format as HTML" |
| `visual-format-replication` | "Pixel-perfect visual replicas from screenshots" |

**Recommendation:** Merge into `visual-format-replication`.

### 🟡 Person Profiling (2 skills, overlapping)

| Skill | Scope |
|-------|-------|
| `person-dossier-from-public-sources` | "Epistemic-tagged human profile dossier" |
| `person-intelligence-dossier` | "Verifiable professional profile + intelligence dossier" |

**Recommendation:** Merge into `person-intelligence-dossier` (superset).

### 🟡 Institutional Forensics (3 skills, overlapping)

| Skill | Scope |
|-------|-------|
| `institutional-case-building` | "Chronological case files from public sources" |
| `institutional-forensic-analysis` | "Forensic case files on institutional crises" |
| `legal-case-dossier-from-news` | "Structured legal-case dossier from news URLs" |

**Recommendation:** Merge `institutional-case-building` and `institutional-forensic-analysis`. Keep `legal-case-dossier-from-news` separate (different input: news URLs).

### 🟢 Paper Writing (2 skills, complementary — keep both)

| Skill | Scope |
|-------|-------|
| `research-paper-writing` | ML papers for NeurIPS/ICML |
| `scientific-manuscript-forge` | Domain science manuscripts with figures/PDF |

Different enough to keep separate.

---

## 4. Stale & Broken Skills

### Superseded (still in active library)

| Skill | Status |
|-------|--------|
| `cognitive-level-assertion-protocol` | **SUPERSEDED** by `governance/akal-cognitive-invariants`. Description says "SUPERSEDED". Should be archived. |

### Skills referencing "openclaw" (legacy name)

10+ active skills still reference "openclaw" in their body text. These are not broken but contain stale terminology:
- `social-media/xurl`, `devops/hermes-cron-rhythm`, `devops/federation-subsystem-bringup`, `devops/vault999-chain-governance`, `devops/federation-checkup`, `devops/telegram-userbot-telethon`, `devops/federation-identity-propagation-forensics`, `devops/filesystem-entropy-audit`, `devops/arifos-ed25519-sovereign-signing`, `wisdom-scar-session-audit`

### Empty reference/template/script directories

15+ skills have `references/`, `scripts/`, or `templates/` dirs that are completely empty:
`hermes-naked-prior-audit`, `cognitive-level-assertion-protocol`, `geological-artifact-rigor`, `federated-skill-architecture`, `wisdom-scar-session-audit`, `institutional-epistemic-sink-forensics`, `seven-zen-organs-enforcement`, `skill-substrate-framework`, `arifos-auto-init`, `arifos-kernel-zen-audit`, `federation-sot-inventory`, `agent-role-mode-flagging`, `consult-external-llm`, `weekly-federation-deep-brief`, `meta-mesa-substrate-test`, `uncertainty-routing-protocol`, `submission-readiness-audit`

### Oldest skills (never updated since 2026-05-11)

15 skills in `creative/` and `media/` have never been modified since initial creation (2 months ago). Not necessarily stale but worth reviewing for continued relevance.

---

## 5. Naming Issues

### Directory ↔ Frontmatter Name Mismatches

| Directory Name | Frontmatter `name:` | Severity |
|---------------|---------------------|----------|
| `cognitive-level-assertion-protocol` | `akal-cognitive-invariants` | 🔴 High — also SUPERSEDED |
| `federation-sot-inventory` | `Federation SOT Inventory` | 🟡 Medium — spaces in name |
| `research/code-analysis-skills` | `code-analysis` | 🟡 Medium — extra "-skills" suffix |

### Inconsistent Naming Patterns

- Some skills use `-` (kebab-case): `vps-operations`, `audio-analysis`
- One uses spaces: `Federation SOT Inventory`
- Abbreviations inconsistent: `SOT` vs spelled-out, `OCR` in some, `ocr` in others
- Prefix patterns inconsistent: some devops skills have `arifos-` prefix, some `federation-`, some `hermes-`

### Root-level skills (17) that could be categorized

These skills sit at the root level without a category directory:
`agent-role-mode-flagging`, `arifos-auto-init`, `arifos-kernel-zen-audit`, `cognitive-commands`, `cognitive-level-assertion-protocol`, `consult-external-llm`, `federated-skill-architecture`, `federation-sot-inventory`, `geological-artifact-rigor`, `hermes-naked-prior-audit`, `institutional-epistemic-sink-forensics`, `meta-cognitive-blindspot-audit`, `meta-mesa-substrate-test`, `seven-zen-organs-enforcement`, `skill-substrate-framework`, `submission-readiness-audit`, `uncertainty-routing-protocol`, `weekly-federation-deep-brief`, `wisdom-scar-session-audit`

---

## 6. Quality Assessment — Top 10 Most Likely Used Skills

| Skill | Category | Quality | Notes |
|-------|----------|---------|-------|
| `deep-research` | research | ⭐⭐⭐⭐⭐ | Well-structured, clear triggers, step-by-step |
| `deep-codebase-audit` | software-dev | ⭐⭐⭐⭐⭐ | Comprehensive, proper frontmatter, clear scope |
| `repository-sot-inventory` | software-dev | ⭐⭐⭐⭐⭐ | Excellent trigger list, clear methodology |
| `hermes-cron-rhythm` | devops | ⭐⭐⭐⭐ | Good structure, references openclaw (minor) |
| `caddy-reverse-proxy` | devops | ⭐⭐⭐⭐ | Practical, focused |
| `vps-machine-health` | devops | ⭐⭐⭐⭐ | Detailed, actionable |
| `google-workspace` | productivity | ⭐⭐⭐⭐ | Covers Gmail/Calendar/Drive well |
| `himalaya` | email | ⭐⭐⭐⭐ | Focused CLI skill |
| `arxiv` | research | ⭐⭐⭐⭐ | Clear search patterns |
| `obsidian` | note-taking | ⭐⭐⭐⭐ | Practical vault operations |

**Overall quality:** Skills that exist are generally well-written. The problem is not quality but **quantity and overlap** — too many near-duplicate skills competing for the same trigger words.

---

## 7. Recommendations for Cleanup

### Priority 1: Archive Superseded Skills
- [ ] Move `cognitive-level-assertion-protocol` to `.archive-2026-07-09/` (explicitly SUPERSEDED)

### Priority 2: Consolidate VPS Skills (7 → 2)
- [ ] Merge `vps-agentic-ops`, `vps-autonomous-ops`, `vps-autonomous-response`, `agentic-vps-operations`, `autonomous-vps-response` → `vps-autonomous-ops`
- [ ] Keep `vps-operations` (cleanup/health) and `vps-machine-health` (or merge into `vps-operations`)
- [ ] Result: 7 → 2 skills

### Priority 3: Consolidate Music/Audio Skills (7 → 2)
- [ ] Merge `music-intelligence`, `heartmula`, `songwriting-and-ai-music` → `music-generation`
- [ ] Merge `audio-feature-analysis`, `songsee` → `audio-analysis`
- [ ] Result: 7 → 2 skills

### Priority 4: Consolidate Document Skills (3 → 1)
- [ ] Merge `ocr`, `ocr-and-documents` → `document-intelligence`
- [ ] Result: 3 → 1 skill

### Priority 5: Consolidate Image Editing (2 → 1)
- [ ] Merge `image-text-editing` + `screenshot-editing` → `image-editing`
- [ ] Merge `screen-replica` + `visual-format-replication` → `visual-format-replication`
- [ ] Result: 4 → 2 skills

### Priority 6: Consolidate Person Profiling (2 → 1)
- [ ] Merge `person-dossier-from-public-sources` → `person-intelligence-dossier`
- [ ] Result: 2 → 1 skill

### Priority 7: Consolidate Institutional Forensics (3 → 2)
- [ ] Merge `institutional-case-building` → `institutional-forensic-analysis`
- [ ] Keep `legal-case-dossier-from-news` (different input source)
- [ ] Result: 3 → 2 skills

### Priority 8: Fix Naming Issues
- [ ] Fix `federation-sot-inventory` frontmatter name to `federation-sot-inventory` (remove spaces)
- [ ] Rename `research/code-analysis-skills` dir to `research/code-analysis`
- [ ] Consider categorizing 17 root-level skills

### Priority 9: Clean Empty Directories
- [ ] Remove 10 empty category dirs: `github`, `mlops`, `smart-home`, `data-science`, `autonomous-ai-agents`, `apple`, `capital`, `dream-engine`, `wellness`
- [ ] Remove 15+ empty `references/`, `scripts/`, `templates/` dirs

### Priority 10: Update Stale References
- [ ] Grep-replace "openclaw" → "hermes" in 10+ active skills

---

## Impact Summary

| Action | Skills Affected | Net Reduction |
|--------|----------------|---------------|
| Archive superseded | 1 | -1 |
| Consolidate VPS | 7 | -5 |
| Consolidate music/audio | 7 | -5 |
| Consolidate document | 3 | -2 |
| Consolidate image editing | 4 | -2 |
| Consolidate person profiling | 2 | -1 |
| Consolidate institutional forensics | 3 | -1 |
| **TOTAL** | **27** | **-17** |

**Current:** 158 active skills  
**After cleanup:** ~141 active skills (11% reduction)  
**With empty dir cleanup:** Cleaner structure

The biggest win is **trigger-word clarity** — fewer near-duplicate skills means the skill loader picks the right one more often.
