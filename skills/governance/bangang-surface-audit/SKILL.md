---
name: bangang-surface-audit
description: "Systematic audit methodology to surface BANGANG (arrogant/overinflated) — three dimensions: code overreach, analytical persona-shadow deconstruction, and agent conversational self-audit."
related_skills: [federation-checkup, governance-patterns, human-sexuality-shadow-framework]
triggers:
  - "bangang"
  - "BANGANG"
  - "arrogant"
  - "overinflated"
  - "autonomy audit"
  - "who decides"
  - "agentic intelligence"
  - "surface map"
  - "HITL"
  - "human bottleneck"
  - "fail open"
  - "gate bypass"
  - "env var bypass"
  - "T1 auto-do"
  - "autonomous execution"
  - "autonomous seal"
  - "persona"
  - "shadow"
  - "Jung"
  - "Anwar"
  - "political deconstruction"
  - "hypocrisy analysis"
  - "hypocrite"
  - "gap between word and deed"
  - "reformasi"
  - "victimhood"
  - "persona shadow gap"
  - "figure deconstruction"
  - "kritik pemimpin"
---

# BANGANG Surface Audit — Methodology

> BANGANG = Malay "swollen/arrogant/overinflated"
> Three dimensions: authority BANGANG (system overreach), analytical BANGANG (persona-shadow gap in humans/institutions), and conversational BANGANG (agent self-audit of its own outputs).
> When a task involves deconstructing a figure's claimed identity vs actual behavior, load `references/bangang-as-analytical-lens.md`.
> When the user asks you to measure your own BANGANG level, load `references/agent-self-audit.md`.

## Cross-Reference: Three BANGANG Dimensions

BANGANG has three dimensions — know which one is in play:

| Dimension | Focus | Skill / Location | 
|-----------|-------|-------|
| **Authority BANGANG** | System acting without authorization | This skill (`bangang-surface-audit`) |
| **Evaluation BANGANG** | Fake precision, wrong evaluation mode, metric theatre | `governance-patterns` §Evaluation Mode Doctrine |
| **Analytical BANGANG** | Persona-shadow gap in humans/institutions | `references/bangang-as-analytical-lens.md` (this skill) |
| **Conversational BANGANG** | Self-audit of agent's own outputs — fake precision, scope creep, mode mismatch | `references/agent-self-audit.md` (this skill) |

> 📖 **Analytical BANGANG reference:** `skill_view(name='bangang-surface-audit', file_path='references/bangang-as-analytical-lens.md')` — Jung Shadow framework, 3-phase biographical deconstruction, rationalisation counter, Victimhood Loop, archetype table. Load when deconstructing a figure, not a codebase.

**Evaluation BANGANG** includes: generating scores like "8.5/10" with no provenance, evaluating a bedtime artifact against publication standards, and assuming reviewer authority over user purpose. Load `skill_view(name='governance-patterns')` then search for "Evaluation Mode Doctrine" when evaluating external critiques — especially if the critic generates ungrounded numerical scores.

---

## 7 Search Patterns

Search ALL codebases (`/root/arifOS`, `/root/A-FORGE`, `/root/AAA`, `/root/GEOX`, `/root/WEALTH`, `/root/WELL`, `/root/HERMES`) for:

### 1. AUTONOMOUS EXECUTION (auto-exec)
Pattern: `T1|auto.*do|autonomous|human_in_loop|human_confirm|888_HOLD|FORGE_TEST_MODE|FORGE_SKIP`
- File operations without human loop
- Production deploy without notification
- Self-modification paths

### 2. OVERRIDE CAPABILITY (override)
Pattern: `bypass|override|force|skip_|FORGE_SKIP_|CI.*bypass|skip.*gate`
- Gates that env-vars can disable
- `--force` flags that skip verification
- Principal/sovereign flags that skip all checks

### 3. SUBSTITUTION (substitution)
Pattern: `send_message|auto_send|sign|represent|impersonate|act_as`
- System acting AS the human (messaging, signing, committing)
- Autonomous message sending to third parties

### 4. INTENT INFERENCE (intent-inference)
Pattern: `infer|guess|assume|route.*intent|intent.*classify|recommend.*without.*ask`
- System guessing what human wants instead of asking
- Intent routing that skips human clarification

### 5. CONFIDENCE MISMATCH (confidence-mismatch)
Pattern: `force_humility|overconfident|omega|C_dark|confidence.*>|over.*certain`
- F7 violation surfaces — high confidence with weak evidence
- Omega state measurement

### 6. SOVEREIGN ASSUMPTION (sovereign-assumption)
Pattern: `fatigue|readiness|sleep|machine_autonomy|C_class|BLOCK.*human|DEFER`
- System inferring human state and using it to gate human decisions
- WELL readiness assessment that can return BLOCK

### 7. STATE OVERRIDE (state-override)
Pattern: `carry_forward|flow_state|stale.*state|session.*inherit|last.*session`
- Stale session state overriding fresh human input
- Persisted decisions biasing future contexts

## 6-Layer Classification

| Tier | Label | Meaning |
|---|---|---|
| 🔴 CRITICAL | Can override/substitute for human — no guard | 6 env-var bypasses found |
| 🟠 HIGH | Can proceed autonomously; guard is soft/bypassable | Fail-open cascade + T1 creep |
| 🟡 MEDIUM | Can proceed without human; guard exists but wasn't triggered | State inference + autonomous execution |
| 🔵 LOW | Advisory only; human always final | Qualified interpretation |
| ⚪ SELF-AWARE | System detects its own BANGANG pattern | Mesa detector, auto-metric |

## Key Patterns to Identify

### Pattern A: The env-var backdoor
Look for: `CI || FORGE_TEST_MODE || FORGE_SKIP_*` patterns
These bypass constitutional enforcement with zero cryptographic gate.
Any process can set these. Document every occurrence.

### Pattern B: The fail-open cascade
Look for: `fail.*soft|fail.*open|never.*block|advisory|non.fatal|must never block`
Each occurrence individually defensible (resilience).
Collectively: if ANY gate crashes, ALL subsequent gates are disabled silently.

### Pattern C: The T1 creep
T1 defined as "zero friction" in doctrine.
Check if it extends to systemctl restart, arif_seal, self-modification.
Document the gap between doctrine and practice.

### Pattern D: The BANGANG paradox
System that measures itself → decides it's too autonomous → gates human's ability to decide.
WELL `machine_human_substrate.py` is the canonical example.

### Pattern E: The Persona-Shadow gap (Analytical BANGANG)
Look for: `gap between word and deed | persona vs reality | claimed identity vs actual behavior`
This is the **analytical** face of BANGANG — not code patterns, but human/institutional patterns.
- Figure claims identity X → acts as Y (the gap size = BANGANG)
- Victimhood narrative that immunises from self-reflection
- Rationalisation: material justification (e.g. "harga ayam murah") covering emotional attachment
- 3-phase pattern: Rise (builds persona) → Fall (hardens victim identity) → Return (shadow collides with persona)
- Detailed framework at `references/bangang-as-analytical-lens.md`

## Output Format

For each surface found, report:
- **FILE + line number**
- **SURFACE TYPE** (auto-exec, override, substitution, intent-inference, confidence-mismatch, sovereign-assumption, state-override)
- **WHAT IT DOES**
- **FLOOR RELEVANCE** (which F1-F13 floor it touches)
- **SEVERITY** (HIGH/MEDIUM/LOW)
- **LIVE**: is it running in production now?

## Reference: Previous Findings (2026-07-28)

Full map sealed at `/root/arifOS/BANGANG_SURFACES_MAP_COMPLETE.md`
35 surfaces found across 6 layers:
- 6 🔴 CRITICAL (env-var bypasses)
- 10 🟠 HIGH (fail-open + T1 creep)
- 7 🟡 MEDIUM (state inference + autonomous execution)
- 6 🔵 LOW (qualified interpretation)
- 3 ⚪ SELF-AWARE (mesa detection + circuit breakers)

---

## Delivery Preferences for Arif

Arif has clear preferences on how BANGANG analysis output should be formatted. Honor these:

### Format: Written over audio
- Arif prefers **PDF or text** over voice notes. Default to written deliverables.
- Voice notes (TTS) were explicitly rejected: *"Aku malas nak dengar voice."*
- If you already generated a voice note, also provide the text/PDF version before being asked.

### Language: Makcik-grade, not academic
- *"Bahasa manusia. Makcik2 boleh faham."* — Final deliverable must be in simple, accessible Malay.
- Use Jung Shadow framing **as your analytical scaffolding only**. Never put Jung terminology in the deliverable itself — the reader only needs the conclusion.
- Short sentences. No English where Malay works.
- Test: would a makcik at a nasi lemak stall understand it in one read?

### Structure: Comprehensive numbered lists
- Arif prefers **comprehensive numbered lists** (21 > 9). When he asks for "9 benda" he may want more — offer to expand.
- Group by chronological phases (Fasa 1: Timbalan, Fasa 2: Pembangkang, Fasa 3: PMX).
- Each BANGANG point: `### N. [Punchy Title]` + one paragraph plain explanation + `**BANGANG:**` one-liner.

### Audience register guide
| Audience | Register | Depth | Style |
|----------|----------|-------|-------|
| **Abang Sado** | 100% BM, direct, emotional | Deep — identity deconstruction | Challenge but respect his investment |
| **Makcik / group chat** | Very simple BM, short sentences | Surface but punchy | One point fits one WhatsApp message |
| **Arif** | BM campur English | Deep — Jung, psychology, political theory | Analytical but not academic; real-talk |

### Image visuals: PIL fallback
- When MCP tools fail (Mage-Flow, Pollinations), **PIL/Pillow** is a reliable local fallback.
- Use for: symbolic split-face compositions, light-dark contrast, text overlay, silhouette art.
- Reference `image-text-editing` and `screenshot-editing` skills for PIL patterns.
