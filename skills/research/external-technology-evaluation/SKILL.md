---
name: external-technology-evaluation
description: >-
  Evaluate external AI models, research papers, tools, and technologies for
  potential integration into the arifOS federation. Covers the full lifecycle:
  discovery → structured analysis (Observe→Think→Judge) → EUREKA zen proposal →
  SABAR/FORGE/HOLD decision → execution on approval. Distinct from
  ai-model-intelligence-briefing (which is current-awareness briefing) — this is
  integration assessment with execution follow-through.
triggers:
  - "look at this new model"
  - "is this worth having in our system"
  - "what do you think of [paper/model]"
  - "evaluate [technology]"
  - "should we integrate [X]"
  - "yes setup"  # one-word approval after EUREKA proposal
  - "forge"  # execution trigger after approval
  - "forge."  # Arif's canonical execute command
  - "is this worth it"
  - "map all [X] capabilities"
  - "check out [paper/model/tool]"
  - "explain [X] dan contrast dengan architecture kita"  # Mode 3 — architecture comparison
  - "contrast dengan database architecture kita"  # Mode 3
---

# External Technology Evaluation

## When To Use

- Arif shares a link or description of a newly released model, paper, tool, or technology
- He asks whether it's worth integrating into the federation
- He asks you to "map all" capabilities of a system/tool
- **Arif asks for a conceptual/doctrinal contrast** — e.g. "how does X compare to our Y", "what's the difference between loop engineering and reality engineering"
- **Arif asks for an architecture comparison** — e.g. "explain X dan contrast dengan architecture kita", "contrast dengan database architecture kita" (Mode 3)
- The goal is a **decision** (integrate? track? ignore?) + **execution** if approved, OR a **positioning** (how does this relate to arifOS doctrine)

## Modes (three distinct patterns)

This skill covers THREE distinct modes. Identify which one applies before starting:

| Mode | Question | When | Output |
|------|----------|------|--------|
| **1. Integration Evaluation** | "Should we integrate this?" | Arif shares a tool/model/paper and asks if it's worth deploying | FORGE/SABAR/HOLD verdict + execution |
| **2. Doctrinal Contrast** | "How does this concept compare to arifOS reality engineering?" | Comparing a general industry concept (loop eng, harness eng, etc.) against arifOS doctrine | Live-probe-backed table, "So what?" for Arif |
| **3. Architecture Comparison** | "How does this external technology work and how is it different from our stack?" | Arif wants an explainer + contrast against our internal architecture, NO integration decision needed | Tech explainer + multi-dimension contrast table + conclusion |

**Mode 3 — Architecture Comparison** is different from Mode 2: the comparison is against our concrete technical architecture (databases, services, protocols, deployment model), not against abstract doctrine/floors. Use this when Arif says "explain X dan contrast dengan architecture kita." Do NOT run live probes (curl :8088/health) for Mode 3 — instead read the relevant architecture docs (AGENTS.md, LOCALHOST_IS_PASSWORD.md, etc.) for the comparison side.

## Related Skills

- `ai-model-intelligence-briefing` — use for current-awareness briefings (vendor model releases); this skill is for integration evaluation
- `deep-research` — use if deeper multi-source research is needed on the topic

## Workflow

### Phase 0: Live Probe First (Conceptual/Doctrinal Contrasts ONLY)

**CRITICAL: If this is a conceptual/doctrinal contrast (not an integration evaluation), run this phase first — BEFORE any theory.**

Arif will reject a theory-first framing. He wants **live evidence, not philosophy.** Start with live probes:

```bash
# Probe the kernel for real floor values
curl -s http://127.0.0.1:8088/health | jq '.floors_active, .runtime_floors, .vault999_health, .apex_scalars, .thermodynamic'
```

Then gather vault evidence:
```bash
ls /root/.local/share/arifos/vault999/SEAL-*.json 2>/dev/null | wc -l
wc -l /root/.local/share/arifos/vault999/outcomes.jsonl
ls /root/.local/share/arifos/vault999/flow_cooling_*.json 2>/dev/null | wc -l
```

**Key principle: the contrast table MUST carry live values from the probe, not just conceptual descriptions.**

### Phase 1: Observe — Gather Intelligence

Fetch from multiple sources in parallel:

1. **Official source** — project page, GitHub repo, Hugging Face, arXiv paper
2. **Technical details** — architecture, model card, README, benchmarks
3. **Hardware requirements** — watch for GPU/VRAM requirements
4. **License** — MIT, Apache, BSL, CC-NC (NC blocks most federation use)
5. **Release status** — is it released or "coming soon"? Check dates

Use `mcp__hound__mcp_smart_fetch` for content extraction. For papers, fetch the PDF directly from arXiv. Check `nvidia-smi` for local GPU availability.

### Phase 2: Think — Structure the Assessment

Organise findings into these dimensions:

| Dimension | What to Look For |
|-----------|-----------------|
| **Technical excellence** | Benchmarks vs peers, parameter efficiency, architectural novelty |
| **Federation fit** | Does it fill a gap? Complements or competes with existing stack? |
| **Hardware viability** | Can we run it on this VPS? GPU? RAM? Disk? |
| **Novelty vs current stack** | What do we already have that does this? APIs? Skills? |
| **Strategic value** | Is the architecture itself reusable? (e.g. Mage-VAE tokeniser) |
| **Cost** | Open-weight? API-based? Requires paid tier? |

Hardware probe:
```bash
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null
# If empty → no GPU
free -h | head -2
df -h / | tail -1
```

Compare benchmark tables with existing stack capabilities. Be honest about gaps.

### Phase 3: Judge — Decision Framework

Apply floor checks:

| Floor | Check |
|-------|-------|
| **F1 AMANAH** | Reversible? Cloning repo/saving paper is reversible. Deploy is not — flag this. |
| **F7 HUMILITY** | Don't overclaim. If Mage-VL isn't released, say so explicitly. |
| **F10 ONTOLOGY** | Correct classification — AI tool, not sentient. |

Three verdict categories:

| Verdict | Meaning | Follow-up |
|---------|---------|-----------|
| **SABAR** | Worth tracking, not deploying now | Clone repo, save paper, write reference doc. Define trigger conditions. |
| **FORGE** | Deploy now | Integration MCP tool, configure, test, document. |
| **HOLD** | Not worth it at all | Document why, move on. No action beyond brief note. |

### Phase 4: Present — EUREKA Zen Proposal Format

Structure the verdict as:

```
1. 📡 Phase 1: Observe — What [Technology] Actually Is
   - Model family table, key metrics, benchmarks
   - Status of each component

2. 🧠 Phase 2: Think — What Makes It Interesting
   - Structural signals (positive)
   - Counter-signals (negatives)
   - Honest assessment

3. ⚖️ Phase 3: Judge — Worth It or Not?
   - Table: criterion | verdict (or score 1-5)
   - One-line summary: "Jawapan terus: ..."

4. 🔮 Phase 4: Eureka Zen Proposal
   - KATEGORI: SABAR / FORGE / HOLD
   - FLOOR CHECK: F1, F7, F10
   - RECOMMENDATION: one-line
   - Action table: # | Action | Effort | Risk | Why
   - Trigger conditions for escalation

5. 📊 Summary Table
   - Aspect | Score | Note

### Conceptual/Doctrinal Contrast Presentation (alt format for Phase 4)

When the task is to compare an external concept (loop engineering, harness engineering, etc.) against arifOS reality engineering — NOT an integration decision — use this alt format instead of EUREKA Zen:

1. **Live Probe Data First** — curl :8088/health, show floor values, vault counts, seal count
2. **One-Line Canon Statement** — from `/root/AAA/wiki/concepts/CONCEPT_REALITY.md` (the single-source-of-truth canon)
3. **Canonical Contrast Table** — dimension | external concept | arifOS reality engineering. Dimensions include: primitive, unit, question answered, focus, risk, analogy, failure mode, success metric, scale, output
4. **Hierarchy Diagram** — show the containment relationship (e.g. loop eng ⊂ reality eng)
5. **Timeline Foresight** — when did external industry discover this? When did arifOS forge it? Show dates.
6. **"So What?" — Arif-Specific Benefits** — explicitly list what each floor/capability does for Arif that a plain external tool cannot. Use "kau" not "you" where natural. Example:
   - "Plain loop: agent kata 'saya confident' tapi selalu confident even when wrong. arifOS: F7 caps confidence at 0.03-0.05."
   - "Plain loop: takde immutable audit. arifOS: VAULT999 append-only, chattr +a, 83 SEAL receipts."
7. **Live Benchmark Table** — floor | live value | target | plain loop equivalent (usually "none" or "unmonitored")
8. **Honest Corrections** — lift any overclaims from the canon (F2 TRUTH audit). Show what we CAN claim vs what we CANNOT.

**Tone rule:** When Arif pushes back with "So what??", "Hang ada benchmark ka?", or similar — **immediately pivot to live probes.** Stop explaining. Start curling endpoints. The proof is in the kernel, not in the explanation.

### Architecture Comparison Presentation (alt format for Phase 4)

When Mode 3 applies (Arif asks "explain X dan contrast dengan architecture kita") — use this format instead of EUREKA Zen or Doctrinal Contrast:

1. **Explainer** — what the external technology actually is, in plain terms. Core concept (e.g. "LLVM of databases"), key features, architecture diagram in words.

2. **Source Architecture Reference** — read the relevant architecture docs for our side:
   - `/root/AGENTS.md` — federation layout, organs, memory landscape
   - `/root/docs/LOCALHOST_IS_PASSWORD.md` — zero-auth doctrine
   - `/root/docs/AGENTS-wire-3layer.md` — constitutional enforcement
   - Relevant organ READMEs or CLAUDE.md files
   
3. **Multi-Dimension Contrast Table** — use these dimensions (adapt as relevant):

   | Dimension | External Tech | arifOS / Our Stack |
   |-----------|--------------|-------------------|
   | **Core philosophy** | One engine, multiple frontends | Polyglot persistence — right tool for each job |
   | **Engine / data model** | Single VDBE bytecode VM (relational) | 6 engines: Postgres + Redis + Qdrant + FalkorDB + VAULT999 + NATS |
   | **Consistency model** | Single-engine consistency | Multi-engine (ACID for Postgres, eventual for L1/L2, immutable append for L6) |
   | **Security model** | Traditional auth (API keys, managed) | LOCALHOST_IS_PASSWORD — zero passwords, 127.0.0.1 bind, UFW + Cloudflare Tunnel |
   | **Deployment** | Cloud-native, edge/WASM, async | Bare-metal systemd organs, Docker for supporting services, single VPS |
   | **Extension model** | WASM containers inside DB engine | MCP tools across organs via NATS + F1-F13 governance gates |
   | **License** | MIT / open-source | AGPL-3.0 / BSL-1.1 per organ |

4. **Key Axes of Difference** — pick the 2-3 most fundamental differences and explain why they matter. Not all differences are equal; prioritise architectural philosophy differences over implementation details.

5. **Conclusion** — one paragraph: "This is a different solution to a different problem. Turso solves X; we solve Y. Both valid, not competitors."

### Phase 5: Execute on Approval (the "Yes setup" path)

When Arif says any approval signal ("Yes setup", "Ok hang buat", "Go ahead"):

1. **Create directory** — `/root/forge_work/references/<name>/`
2. **Clone repo** — `git clone --depth 1 ...`
3. **Save paper** — `curl -sL -o paper.pdf "https://arxiv.org/pdf/XXXX.XXXXX"`
4. **Write reference document** — structured markdown with:
   - Status, location, license
   - Model family table
   - Key architecture insights
   - Performance benchmarks
   - Hardware requirements
   - Integration paths (if conditions met)
   - Trigger conditions for escalation (SABAR→FORGE)
5. **Report back** — confirm disk usage, key files, location
6. **Build deployment scaffolding (if applicable)** — when the technology runs on GPU and Modal is the deployment target, build a `modal_<name>.py` scaffold with the 5 Modal primitives:

   | Primitive | Modal API | Purpose |
   |-----------|-----------|---------|
   | 1. Image | `modal.Image.micromamba().pip_install()` | Container: Python + deps + flash-attn |
   | 2. Volume | `modal.Volume.from_name(..., create_if_missing=True)` | Persistent model weight cache (~8GB) |
   | 3. Secret | `modal.Secret.from_name(...)` | API keys (HF_TOKEN, etc.) |
   | 4. @app.cls | `@app.cls(gpu="A100-40GB", container_idle_timeout=300, ...)` | GPU class with scale-to-zero |
   | 5. @modal.enter() | `@modal.enter()` → `def load(self)` | Lifecycle: download + warm-up on cold start |
   | 6. @modal.web_endpoint | `@modal.web_endpoint(method="POST", docs=True)` | HTTP API endpoint |

   **Key design decisions:**
   - `container_idle_timeout=300` = F1 AMANAH compliance (5 min idle → scale-to-zero, no burn)
   - `allow_concurrent_inputs=4` = batch efficiency on one GPU
   - HF cache env vars (`HF_HOME=/cache/huggingface`) pointed at Volume for persistent weights
   - Template saved as `templates/modal_inference.py` under this skill
   
   **Output:** scaffold file at `forge_work/references/<name>/<name>_modal.py`. NOT deployed — Arif calls `modal deploy` when ready.

7. **Update the reference doc** with deployment triggers and the scaffold location.

### Tone

- Direct, no fluff
- Arif values: honest assessment > diplomatic language
- Use Malay-English mix naturally when it fits
- Label epistemic tags: OBS (measured), INT (analysis), SPEC (prediction)
- "Jawapan terus" at the start of the verdict
- Summary table with star ratings is Arif-approved format

## Pitfalls

- **Don't skip hardware probe**: `nvidia-smi` may return empty — check explicitly
- **Don't over-recommend closed-source**: Arif prefers open-weight. Flag licensing restrictions clearly.
- **Don't claim "coming soon" as capability**: Mage-VL not released = not evaluated. State this explicitly.
- **Don't propose API-dependent integration without checking existing API keys**: use vault.env.
- **Don't forget the floor check**: Every EUREKA proposal must carry F1/F7/F10 assessments.
- **Don't deploy scaffolding without approval**: Build the Modal scaffold but do NOT run `modal deploy`. Arif calls `modal deploy` when he's ready. The scaffold is the execution-ready plan, not the execution itself.
- **"Apa yang ada guna ja"**: If the current stack already covers the capability, the bar for integration is higher. State the gap explicitly.
- **Don't lead with theory for conceptual contrasts**: When Arif asks "what's the difference between X and our Y" — do NOT start with philosophical framing. Start with `curl :8088/health` and live data. He will push back with "So what??" if you lead with abstractions. The proof is in the kernel, not in paragraphs.
- **For architecture comparisons, read the source docs, don't curl live probes**: Mode 3 compares against technical architecture (AGENTS.md, LOCALHOST_IS_PASSWORD.md) not live floor values. Read the relevant docs instead of curling health endpoints.
- **Don't present a comparison without "So what?"**: After the contrast table, ALWAYS answer what this means for Arif specifically. Use "kau" format. E.g. "Plain loop: agent kata confident tapi selalu salah. arifOS: F7 caps confidence at 0.05."
- **Architecture comparisons need a conclusion, not a verdict**: Mode 3 doesn't produce FORGE/SABAR/HOLD. The conclusion is "different tool for different problem" — state it clearly.
- **References directory stores condensed knowledge**: After a conceptual evaluation, save a reference file so future sessions don't need to re-derive the same analysis.
- **State document PURPOSE in the first sentence, not last**: When Arif shares a research document / paper / report, the very first sentence must answer "what is this FOR?" — i.e. what decision or understanding it serves. If you open with deep analysis instead, Arif will interrupt with "What is this for?" (2026-08-04 session). Structure: (1) one-line purpose, (2) source provenance, (3) then analysis.
- **Verify external paper equations numerically, not just symbolically**: Research PDFs can carry math errors that pass visual inspection. The 2026-08-04 DMF companion paper claimed `⟨X⟩ = P(+1) + P(-1)` for a binary Pauli measurement — which always equals 1.0 (probabilities sum to 1), not the actual expectation. The correct formula is `⟨X⟩ = P(+1) − P(-1)`. Caught only because we ran numbers through `execute_code`. For any paper containing formulas, pick at least one core equation and verify it numerically with known inputs before treating the paper as a reliable reference. This is especially important for tomography / calibration / benchmarking sections where errors silently propagate into implementation.
- **Re-analysis of the same source = patch existing reference, don't duplicate**: When a second session analyzes the same PDF (Gemini Deep Research output is a common case), PATCH the existing reference file with new findings — math errors caught, additional EUREKA candidates, cross-verification with external sources. Don't create a duplicate reference for the same PDF. The reference file is the canonical record that accumulates across sessions.

## References

- `references/mage-evaluation-2026-07-25.md` — Mage-Flow image generation evaluation
- `references/furi-mcp-manager-evaluation-2026-07-26.md` — Furi MCP server manager evaluation (pattern for MCP tool/infra assessments)
- `references/turso-libsql-architecture-2026-07-30.md` — Turso/libSQL "LLVM of databases" architecture (pattern for Mode 3 — Architecture Comparison)
- `references/dmf-epistemology-evaluation-2026-08-04.md` — DMF + Epistemology Tripartition evaluation; 7 EUREKA atoms, 3 Phase 2 gaps in memory_decay
