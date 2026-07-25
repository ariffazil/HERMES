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
---

# External Technology Evaluation

## When To Use

- Arif shares a link or description of a newly released model, paper, tool, or technology
- He asks whether it's worth integrating into the federation
- He asks you to "map all" capabilities of a system/tool
- The goal is a **decision** (integrate? track? ignore?) + **execution** if approved

## Related Skills

- `ai-model-intelligence-briefing` — use for current-awareness briefings (vendor model releases); this skill is for integration evaluation
- `deep-research` — use if deeper multi-source research is needed on the topic

## Workflow

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
```

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
