# Hermes Skills Library Audit — 2026-07-15

## Library Snapshot

- **Active skills:** 158
- **Archived skills:** 86 (.archive, .archive-2026-07-08, .archive-2026-07-09)
- **Disk usage:** 18 MB total, 3.6 MB archive
- **Location:** `/root/.hermes/skills/`

## Category Distribution

| Category | Count |
|----------|-------|
| devops | 29 |
| creative | 28 |
| research | 24 |
| governance | 20 |
| media | 11 |
| productivity | 10 |
| trading | 5 |
| software-development | 5 |
| social-media | 4 |
| Standalone (root-level) | 17 |
| note-taking, email, geology | 1 each |

## Confirmed Overlap Clusters

### VPS Operations (7 → 2 recommended)

All describe "smoketest, state machine, circuit breaker, rollback, dead-man's switch":

- `vps-operations` — cleanup/health auditing (KEEP as-is)
- `vps-machine-health` — system resource recon, OS cleanup (MERGE into vps-operations)
- `vps-agentic-ops` — smoketest + state machine + circuit breaker
- `vps-autonomous-ops` — autonomous VPS control loops
- `vps-autonomous-response` — autonomous monitoring + response layers
- `agentic-vps-operations` — Tier 1 Active Response
- `autonomous-vps-response` — Tier 1 Active Response pattern

Best-in-cluster for the self-healing pattern: `vps-autonomous-ops` (most comprehensive).

### Music Pipeline (4 → 1 recommended)

- `music-generation` — full pipeline: concept → lyrics → generation (KEEP as umbrella)
- `music-intelligence` — governed generation + somatic scoring (MERGE)
- `heartmula` — Suno-like generation from lyrics + tags (MERGE)
- `songwriting-and-ai-music` — songwriting craft + Suno prompts (MERGE)

### Audio Analysis (3 → 1 recommended)

- `audio-analysis` — Python DSP modules, librosa, MFCC (KEEP as umbrella)
- `audio-feature-analysis` — chroma, motif, spectral (MERGE)
- `songsee` — audio spectrograms/features via CLI (MERGE)

### OCR / Document Extraction (3 → 1 recommended)

- `media/ocr` — image OCR via Tesseract (MERGE)
- `productivity/ocr-and-documents` — PDF/scan text extraction (MERGE)
- `productivity/document-intelligence` — VLM-first document extraction (KEEP as umbrella)

### Image Editing (4 → 2 recommended)

- `image-text-editing` — PIL/Pillow text replacement (MERGE into screenshot-editing)
- `screenshot-editing` — PIL/Pillow image surgery (KEEP, rename to image-editing)
- `screen-replica` — replicate app screen as HTML (MERGE into visual-format-replication)
- `visual-format-replication` — pixel-perfect visual replicas (KEEP)

### Person Profiling (2 → 1 recommended)

- `person-dossier-from-public-sources` — epistemic-tagged dossier (MERGE)
- `person-intelligence-dossier` — verifiable profile + intelligence dossier (KEEP)

### Institutional Forensics (3 → 2 recommended)

- `institutional-case-building` — chronological case files (MERGE into forensic-analysis)
- `institutional-forensic-analysis` — forensic case files on crises (KEEP)
- `legal-case-dossier-from-news` — structured legal dossier from news URLs (KEEP — different input)

## Naming Issues Found

### Directory ↔ Frontmatter Mismatches

| Directory | Frontmatter `name:` | Fix |
|-----------|---------------------|-----|
| `cognitive-level-assertion-protocol` | `akal-cognitive-invariants` | Archive entire skill (SUPERSEDED) |
| `federation-sot-inventory` | `Federation SOT Inventory` | Fix frontmatter name to `federation-sot-inventory` |
| `research/code-analysis-skills` | `code-analysis` | Rename dir to `code-analysis` |

### Stale Superseded Skills

`cognitive-level-assertion-protocol` has `description: "SUPERSEDED by governance/akal-cognitive-invariants"` but is still in the active library. Should be archived.

### Legacy "openclaw" References

10+ active skills still reference "openclaw" in body text:
`xurl`, `hermes-cron-rhythm`, `federation-subsystem-bringup`, `vault999-chain-governance`, `federation-checkup`, `telegram-userbot-telethon`, `federation-identity-propagation-forensics`, `filesystem-entropy-audit`, `arifos-ed25519-sovereign-signing`, `wisdom-scar-session-audit`

## Structural Issues

### Empty Category Directories (10 ghost dirs)

`github`, `mlops`, `smart-home`, `data-science`, `autonomous-ai-agents`, `apple`, `capital`, `dream-engine`, `wellness`

These have zero SKILL.md files. Clean up or repurpose.

### Empty References/Scripts/Templates Dirs (15+)

Many skills have `references/`, `scripts/`, or `templates/` dirs that are completely empty. Either populate or remove.

### Root-Level Skills Without Category (17)

`agent-role-mode-flagging`, `arifos-auto-init`, `arifos-kernel-zen-audit`, `cognitive-commands`, `cognitive-level-assertion-protocol`, `consult-external-llm`, `federated-skill-architecture`, `federation-sot-inventory`, `geological-artifact-rigor`, `hermes-naked-prior-audit`, `institutional-epistemic-sink-forensics`, `meta-cognitive-blindspot-audit`, `meta-mesa-substrate-test`, `seven-zen-organs-enforcement`, `skill-substrate-framework`, `submission-readiness-audit`, `uncertainty-routing-protocol`, `weekly-federation-deep-brief`, `wisdom-scar-session-audit`

Consider categorizing these under existing or new category dirs.

## Cleanup Impact

Consolidating the 7 overlap clusters would remove ~17 skills (158 → ~141), an 11% reduction. The bigger win is trigger-word clarity — fewer near-duplicate skills means the skill loader picks the right one more consistently.
