# HERMES → AAA Prefix Mapping (2026-07-26)

**Source:** 233 HERMES skills × 167 non-retired AAA skills  
**Method:** Semantic classification by function, not string matching  
**Trigger:** `ARIFOS::AAA_FEDERATED_SKILL_ALIGNMENT::v1`

---

## Classification Summary

| AAA Prefix | Count | Function |
|-----------|-------|----------|
| **AGI-** | 70+ | Cognition, research, creative, media, intelligence |
| **ASI-** | 35+ | Agent governance, architecture, invariants, self-audit |
| **APEX-** | 13 | Verification, audit pipelines, truth gates |
| **FORGE-** | 70+ | Infrastructure, ops, MCP, deployment, tooling |
| **KERNEL-** | 6 | arifOS kernel, organ forging, runtime modules |
| **AUDIT-** | 6 | Knowledge files, SOT inventory, store governance |
| **FLAME-** | 2 | Free-loop model engine |
| **WELL-** | 2 | Human wellness, medical advocacy |
| **WEALTH-** | 14 | Trading, finance, nasi-lemak tracking |
| **HERMES-only** | 6 | Platform-specific (Apple), internal utilities |

---

## Semantic Mapping Rules

### Rule 1: Function Determines Prefix, Not Name

The AAA prefixes correspond to **cognitive/operational layers**, not literal naming:

| Prefix | Function | Triggers |
|--------|----------|----------|
| **AGI-** | Cognition, knowledge, creative, research | `research/`, `creative/`, `media/`, `cognitive-*`, `akal-*`, `arxiv`, `blogwatcher`, any intelligence-gathering |
| **ASI-** | Agent governance, session, architecture | `governance/` (most), `agent-*`, `three-agent-*`, `f13-*`, `somatic-*`, `institutional-*`, `temporal-*` |
| **APEX-** | Verification, truth gates, audit | `apex-*`, `spec-audit`, `deployment-claim-*`, `live-probe-*`, `paper-to-code-*`, `submission-readiness-*` |
| **FORGE-** | Infrastructure, build, deploy, tooling | `devops/` (most), `vps-*`, `mcp-*`, `caddy-*`, `federation-*`, `hermes-*`, `productivity/`, `social-media/` |
| **KERNEL-** | arifOS kernel, floors, modules | `arifos-*`, `ariflow-*` (kernel-adjacent) |
| **AUDIT-** | Inventory, SOT, knowledge governance | `aaa-knowledge-*`, `repository-sot-*`, `federation-sot-*`, `governed-knowledge-*` |
| **FLAME-** | Free-loop model engine | `flame-free-loop*` |
| **WELL-** | Human wellness, health | `hospital-*`, `medical-*` |
| **WEALTH-** | Trading, finance, sales tracking | `trading/`, `business/` (nasi-lemak), `vendor-receipt-*`, `receipt-*` |

### Rule 2: Category Overrides Path When Ambiguous

Some skills sit in `devops/` but operate on governance infrastructure. Classify by domain content, not directory:

```
devops/arifos-ed25519-sovereign-signing → FORGE-ed25519-signing  # infrastructure for signing, not the act of governing
devops/arifos-constitutional-floor-modification → FORGE-constitutional-floor-mod  # infrastructure, not governance theory
devops/a-forge-development → FORGE-a-forge-development  # A-FORGE as devops tooling
```

### Rule 3: Research Starts AGI, Intelli Starts AGI

All research/intelligence/briefing skills → AGI- prefix unless they're about financial trading:

```
research/deep-research → AGI-deep-research           # cognitive intelligence
research/petronas-petros-shell → AGI-petronas-petros-shell  # institutional intelligence  
trading/trading-analysis-xauusd → WEALTH-trading-xauusd  # financial analysis
```

### Rule 4: Creative/Media → AGI-

All creative production, media processing, and content generation → AGI- prefix. These are cognitive tools:

```
creative/ascii-art → AGI-ascii-art
creative/scientific-pdf-generation → AGI-scientific-pdf-generation
media/youtube-content → AGI-youtube-content
```

### Rule 5: Nasi-lemak is WEALTH (not BUSINESS)

All `nasi-lemak-*` and `vendor-receipt-*` and `receipt-*` skills are sales/financial tracking → WEALTH-:

```
business/nasi-lemak-sales → WEALTH-nasi-lemak-sales
trading/nasi-lemak-tracking → WEALTH-nasi-lemak-tracking
receipt-inventory-tracking → WEALTH-receipt-inventory
```

### Rule 6: Productivity/Social Tools → FORGE-

Email, calendar, maps, note-taking, social media posting, Telegram → FORGE- prefix. These are operational infrastructure:

```
productivity/airtable → FORGE-airtable
social-media/xurl → FORGE-xurl-twitter
email/himalaya → FORGE-himalaya-email
```

---

## HERMES-Only Skills (no AAA equivalent)

These 6 skills have no AAA-scope equivalent:

| Skill | Reason |
|-------|--------|
| `apple-notes` | Platform-specific (macOS notes integration) |
| `apple-reminders` | Platform-specific (macOS reminders) |
| `findmy` | Platform-specific (Apple FindMy API) |
| `forge-visual-qa-constitutional` | HERMES-internal governed visual QA contract |
| `imessage` | Platform-specific (Apple iMessage) |
| `manifest-data-repair` | Internal data repair utility |

---

## Key AAA Skills Missing from HERMES (by priority)

### Critical governance/ASI gaps
- `ASI-session-seal` — session sealing protocol
- `ASI-agent-invariants` — agent identity enforcement
- `ASI-fabrication-prevention` — hallucination gate
- `ASI-constitutional-reasoning` — floor reasoning
- `ASI-agentic-governance` — governance core

### FORGE infrastructure gaps
- `FORGE-cicd-docker-deploy` — CI/CD pipeline
- `FORGE-fastapi-api-builder` — API development
- `FORGE-nextjs-mastery`, `FORGE-react-spa-discipline` — frontend
- `FORGE-postgres-schema-design`, `FORGE-redis-qdrant-integration` — data
- `FORGE-secret-hygiene`, `FORGE-incident-triage` — ops

### AGI cognition gaps
- `AGI-claude-xml-structured-reasoning` — structured reasoning
- `AGI-codex-chain-of-thought` — chain-of-thought
- `AGI-emd-encode/decode/metabolize` — EMD protocol
- `AGI-multimodal-bridge`, `AGI-hermes-system-prompt-voice` — core Hermes skills

### KERNEL/RSI
- `KERNEL-trinity-33` — 33 paradoxes
- `RSI-recursive-improvement` — recursive improvement

---

## Full Mapping Table (227 entries)

The full 227-entry mapping table is available in:
- `/root/hermes-aaa-mapping-report.txt` (raw session output, 233 skills)
- Section 1 of this report's parent SKILL.md refers to this file.

### Sample of prefix distribution:

| AAA Prefix | Example Mappings |
|-----------|-----------------|
| AGI- | cognitive-commands, deep-research, arxiv, blogwatcher, ascii-art, p5js, youtube-content, music-intelligence, songwriting-and-ai-music, architecture-diagram, claude-design, image-annotation-labeling, ocr |
| ASI- | three-agent-flow-doctrine, governed-execution-substrate, agent-channel-sovereignty, f13-sovereign-authorization-substrate, temporal-constitution, somatic-intelligence, bloodhound-federation-mapping, institutional-intelligence, wisdom-scar-session-audit |
| APEX- | apex-verification-pipeline, spec-audit, live-probe-audit-pattern, deployment-claim-verification, deep-codebase-audit, paper-to-code-validation, submission-readiness-audit, federation-tri-team-audit, external-artifact-verdict, geox-comparative-testing |
| FORGE- | vps-operations, mcp-conformance-audit, caddy-reverse-proxy, federation-node-onboarding, external-mcp-integration, hermes-cron-rhythm, google-workspace, notion, xurl, telegram-userbot, himalaya, maps, airtable, obsidian |
| KERNEL- | arifos-kernel-zen-audit, arifos-auto-init, arifos-external-council, arifos-organ-forging, arifos-runtime-module-authoring, ariflow-component-forging |
| AUDIT- | aaa-knowledge-files, repository-sot-inventory, federation-sot-inventory, governed-knowledge-stores, external-technology-evaluation, geological-artifact-rigor |
| FLAME- | flame-free-loop, flame-free-loop-mesh |
| WELL- | hospital-patient-advocacy, medical-document-interpretation |
| WEALTH- | daily-trading-signal-briefing, trading-analysis-xauusd, agentic-trading-companion, mt5-ai-trading-agent, nasi-lemak-sales, nasi-lemak-tracking, syedos, vendor-receipt-tracking, receipt-inventory-tracking, receipt-to-analytics |
