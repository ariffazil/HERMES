---
name: constitutional-dataset-forging
description: "Prepare structured SFT/DPO/validation datasets from constitutional canon, red-team probes, and governance docs for model fine-tuning. Turns federation DNA into training substrate."
triggers:
  - "I-ARIF dataset"
  - "SFT conversion"
  - "DPO pairs from canon"
  - "training dataset from AAA/BBB/CCC"
  - "fine-tuning data preparation"
  - "constitutional training pairs"
  - "EMD format dataset"
  - "Hugging Face dataset pipeline"
  - "build_iarif_corpus"
  - "ariffazil/* dataset synthesis"
---

# Constitutional Dataset Forging

Take federation canon (7 Hugging Face datasets + 50+ local canon docs) and forge them into structured SFT, DPO, and validation datasets for model fine-tuning.

**Core principle:** The dataset *is* the constitution in weight-space. Every pair must encode EMD (Encode→Metabolize→Decode) reasoning, not just Q&A.

---

## Source Architecture: The 7-Dataset Canon

The training corpus is NOT just AAA. The full fabric:

| Dataset | Role | Size | Split |
|---|---|---|---|
| `ariffazil/AAA` | Constitutional genome — F1-F13, EMD, verdicts | ~1,000 entries | SFT-BASE |
| `ariffazil/BBB` | BM guardrail failure probes | ~50 | DPO (chosen/rejected) |
| `ariffazil/CCC` | Anomalous contrast — ILMU vs arifOS kernel | ~50 | DPO |
| `ariffazil/DDD` | Penang loghat register-sensitivity | ~50 | DPO |
| `ariffazil/EEE` | Kernel spine recovery audit | ~20 | VAL-GATE |
| `ariffazil/FFF` | Federation fitness gate / model promotion | ~30 | VAL-GATE |
| `ariffazil/a2b-eval-results` | AssetOpsBench external benchmark | ~50 | VAL-GATE |
| Local canon | `/root/arifOS/GENESIS/` (49 files), `/root/AAA/docs/` (311), `/root/AAA/governance/` (68), `/root/AAA/contracts/` (16), agent cards (19) | ~4MB text | SFT-BASE |

**Real training pairs:** ~800-1,200 SFT + ~150 DPO + ~70-100 validation. Small, dense, constitutional — ideal for QLoRA.

**Guardrails:**
- 🚫 NO live telemetry (Kabarkan traces)
- 🚫 NO temp session files (carry_forward.json)
- 🚫 NO live seal chains (VAULT999 outcomes.jsonl)
- 🚫 NO credentials (API keys, tokens, kunci-mas.env values)
- 🚫 NO systemd unit logs or journalctl output

---

## SFT Format Specification (EMD Instruction Pairs)

Every SFT pair must use the **EMD reasoning envelope** to encode constitutional decision logic:

```json
{
  "instruction": "Evaluate the following execution signal under F1-F13 constitutional floors.",
  "input": "<raw_signal_or_tool_call>",
  "output": "<reasoning>\nENCODE: Decompose task vector.\nMETABOLIZE: Evaluate risk weights against F1 (Amanah) and F2 (Truth).\nDECODE: Check drift and assertion limits.\n</reasoning>\n<verdict>HOLD|EXECUTE|REJECT</verdict>"
}
```

### EMD Instruction Templates (8 canonical types)

| Template ID | Instruction Pattern | Source |
|---|---|---|
| CONSTITUTIONAL_VERDICT | "Evaluate under F1-F13 constitutional floors." | FLOOR_TABLE + GENESIS |
| AMANAH_CHECK | "Analyze for F1 AMANAH (reversibility) compliance." | GENESIS/000, floor F1 |
| TRUTH_CHECK | "Assess whether this claim satisfies F2 TRUTH (≥0.99 fidelity)." | GENESIS/000, floor F2 |
| DOMAIN_ROUTING | "Route this signal to the correct organ based on domain." | AAA agent cards |
| FLOOR_IDENTIFICATION | "Determine the constitutional hardness floor triggered." | FLOOR_TABLE |
| DECODE_DRIFT | "Perform EMD decode: validate output for drift and assertion limits." | GENESIS/020 |
| SOVEREIGN_TRIGGER | "Evaluate whether this requires 888_HOLD sovereign review." | F13, HITV protocol |
| AUDIT_CHECK | "Assess against F11 AUDITABILITY requirements." | GENESIS/020, F11 |

### Agent Card Pairs

Agent cards define identity + authority boundaries. For each card, generate pairs for:
- **Sovereign authority** — "Identify the sovereign authority for this agent identity."
- **Capability boundaries** — "What are the capability boundaries of this agent?"
- **Principal classification** — "Classify this agent's principal type (human/agent/institution)."

Sources: `/root/AAA/agents/*/agent-card.json` (19 cards: opencode, hermes-asi, main, openclaw, prospect-maturation, makcikgpt, 11 external agents)

---

## DPO Format Specification (Preference Pairs)

For BBB/CCC/DDD probes, produce **chosen** (constitutional arifOS response) vs **rejected** (flawed commercial LLM response or asymmetric refusal) pairs:

```json
{
  "prompt": "<bm_or_penang_or_ilmu_probe>",
  "chosen": "<response maintaining F1-F13 floors and EMD reasoning>",
  "rejected": "<response that violates constitutional guardrails>",
  "domain": "BBB-BM_GUARDRAIL|CCC-ILMU_CONTRAST|DDD-PENANG_LOGHA T"
}
```

### DPO Domain Patterns

| Domain | What it teaches the model |
|---|---|
| **BBB-BM_GUARDRAIL** | Reject manipulation via BM. Constitutional refusal is not rudeness — F9 Anti-Hantu + F13 sovereignty. |
| **CCC-ILMU_CONTRAST** | ILMU is advisory. arifOS kernel is authoritative. Never override F1 based on external model approval. |
| **DDD-PENANG_LOGHA T** | Normalize informal register without changing semantics. F5 PEACE² + F6 EMPATHY for tone. Verdict on constitutional merit, not register. |

---

## Validation Gating Format

Hold-out probes from EEE, FFF, a2b — used for gating model promotion/demotion.

| Source | Domain | Example Probe |
|---|---|---|
| EEE | Kernel recovery | "After systemd restart, FQ counter reads 0. What is the recovery path?" |
| FFF | Federation fitness | "Organ :18083 returns 503. How does the federation respond?" |
| a2b | Asset benchmark | "Evaluate prospect P010 on volumetric risk vs reward." |

---

## Pipeline Structure

```
Phase 1: SCAN LOCAL CANON
  → Walk GENESIS/, AAA/docs/, AAA/governance/, AAA/contracts/
  → Walk agent cards
  → Output: file inventory + metadata (size, sha256, chars)

Phase 2: GENERATE SFT (from canon + cards)
  → Parse FLOOR_TABLE.json for floor definitions
  → Split local canon by sections (## headings)
  → Wrap each substantive section into EMD instruction pair
  → Deduplicate by instruction+input hash
  → Output: train_sft.jsonl

Phase 3: GENERATE DPO (from BBB/CCC/DDD via HF)
  → Pull ariffazil/BBB, CCC, DDD from Hugging Face
  → Convert each probe into chosen/rejected pair
  → Tag by domain
  → Output: train_dpo.jsonl

Phase 4: GENERATE VAL (from EEE/FFF/a2b via HF)
  → Pull ariffazil/EEE, FFF, a2b-eval-results from HF
  → Format as prompt + expected_domain
  → Output: val_gating.jsonl

Phase 5: PUSH TO HUGGING FACE
  → Create/update ariffazil/I-ARIF-CANON
  → Upload: train_sft.jsonl, train_dpo.jsonl, val_gating.jsonl, manifest.json
```

---

## Key Pitfalls

### 1. DPO/Val Counts Will Be Weak Without Real HF Dataset Parsing

Template-based DPO generation produces ~9 pairs. The actual BBB/CCC/DDD datasets contain ~50 each. **Always pull from Hugging Face** and inspect dataset schema first:

```python
from datasets import load_dataset
ds = load_dataset("ariffazil/BBB", split="train")
print(ds.features)    # reveals column schema
print(ds[0])          # inspect first entry
```

### 2. Local Canon Has Strong Section Structure — Use It

GENESIS files are markdown with `##` sections. Split on headings to get 100-500 char segments. Avoid extracting fragments shorter than 100 chars (noise) or longer than 2,000 chars (overloads the EMD template).

### 3. SFT Count Can Exceed Target Easily

With 49 GENESIS + 311 AAA/docs + 68 governance files, section-based extraction easily produces 1,200+ pairs. If over target, **prioritize quality over quantity** — keep only pairs from sections with explicit constitutional content (F1-F13 references, EMD patterns, HOLD/SEAL/REJECT verdicts, KILL matrix mentions).

### 4. Deduplication Is Essential

The same constitutional principle appears in multiple canon files (e.g., F1 appears in GENESIS/000, AGENTS.md, FLOOR_TABLE, and AAA governance docs). **Deduplicate by instruction+input MD5 hash** after generation. Expected compression: ~20-30% reduction.

### 5. Hugging Face Write Access

Set `HF_TOKEN` in environment. Push with:
```bash
huggingface-cli upload ariffazil/I-ARIF-CANON out/ --repo-type dataset
```
Verify upload by pulling back and checking entry counts.

### 7. Canon Chunking Explodes Without Length Filter

AAA docs (311+ files) can produce **4,500+ chunks** if split too aggressively. Critical filters:
- **GENESIS docs**: `min_chars=300`, split on `##` headings
- **AAA docs**: `min_chars=400`, split on `##`/`###` only for files >3,000 chars; keep small files whole
- **Agent cards**: <400 chars each → usually filtered out; consider generating synthetic instruction pairs from their metadata instead

### 8. EEE and FFF Are Not in `datasets` Library Format

These repos store JSONL files directly in the HF repo (not via the `datasets` loading script). The `datasets.load_dataset()` call raises an error. Load via:
```python
import requests, json
r = requests.get("https://huggingface.co/datasets/ariffazil/EEE/resolve/main/data/all_receipts.jsonl")
rows = [json.loads(line) for line in r.text.strip().split("\n") if line.strip()]
```

### 9. Hard Cap SFT at 1,200 — The Pipeline Will Over-Generate

Without a hard cap, the pipeline produces 8,000+ SFT pairs easily (AAA docs overhead). The generation loop should include a counting breaker:
```python
if len(sft) >= 1200: break
```
Prioritise: FLOOR_TABLE pairs (always include all 13×2=26), then GENESIS canon, then AAA docs, then agent cards. Never exceed 1,200.

### 10. Stage, Don't Push — Arif Reviews First

The reference script at `/root/forge_work/i-arif-prep/build_iarif_corpus.py` writes to a local `forge_work/` directory. **Do NOT push to Hugging Face** (`ariffazil/I-ARIF-CANON`) until Arif reviews the manifest and sample pairs. The push step is manual by design.

### 11. When the Model Gets Trained

After training, the GGUF model goes to Ollama as a custom Modelfile, NOT replacing DeepSeek. Architecture:
- **L1 (FREE):** I-ARIF 7B GGUF → constitutional triage, routing, refusal
- **L2 (CHEAP):** FLAME 70B → fact-checking, epistemic verification  
- **L3 (HEAVY):** DeepSeek V4 Pro → complex reasoning, code, judgment

The fine-tuned model never runs general queries. It's a governor, not a chatbot.

---

## References

### Canonical Implementation

The canonical reference implementation lives at:
```
/root/forge_work/i-arif-prep/build_iarif_corpus.py
```

### Session Reference (Actual Results)

Detailed execution log from the first full pipeline run:
```
/root/.hermes/skills/software-development/constitutional-dataset-forging/references/iarif-run-20260729.md
```

### Workflow

1. **Build script** at `/root/forge_work/i-arif-prep/build_iarif_corpus.py`
2. **Run** → outputs to same dir: `i-arif-sft.jsonl`, `i-arif-dpo.jsonl`, `i-arif-val.jsonl`, `manifest.json`
3. **Review** — show Arif the manifest and sample output BEFORE pushing to HF
4. **Push only on explicit approval** — never auto-publish to `ariffazil/I-ARIF-CANON`

Strategy: **HOLD on actual training until operational wiring is stable.** Dataset prep runs in background as non-blocking prep — Arif reviews the staged output before any training is initiated.
