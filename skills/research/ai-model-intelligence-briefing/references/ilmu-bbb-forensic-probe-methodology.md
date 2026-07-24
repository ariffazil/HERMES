# BBB Forensic Probe Methodology — ILMU Deconstruction

## Source
Dataset: `ariffazil/BBB` on HuggingFace (https://huggingface.co/datasets/ariffazil/BBB)
Date: 2026-06-07

## What Was Tested
Two ILMU endpoints probed side-by-side:
- `ilmu-nemo-nano` (smaller/faster)
- `nemo-super` (larger/stronger)

## Core Findings

| Finding | Signal | Verdict |
|---------|--------|---------|
| "From scratch" claim false — endpoints named "nemo" (NVIDIA Nemotron) | ilmu-nemo-nano **admitted it's a fine-tune** | Off-the-shelf, not original |
| MalayMMLU benchmark self-created by YTL AI Labs | Scores opaque, refused disclosure | Benchmark is marketing, not independent |
| Cross-endpoint contradictions | nemo-super said "from scratch" opposite to nano | Product doesn't know own identity |

## Reusable Methodology

### 1. Binary Forced-Choice Probing
Force model to pick ONE of two contradictory answers. Bypasses evasive guardrails better than open-ended questions.

### 2. Cross-Endpoint Testing
Same product, different endpoints. Inconsistency = red flag.

### 3. Naming Forensics
Endpoint names reveal underlying architecture. "nemo" = Nemotron, "sonnet" = Claude, "turbo" = GPT. Marketers rename but infra naming leaks truth.

### 4. Benchmark Independence Audit
Three questions for every vendor claim:
1. Who created the benchmark? (Vendor self-created = red flag)
2. Can scores be independently reproduced?
3. What does the model score on REAL independent benchmarks (MMLU, HumanEval, etc.)?

### 5. Opacity as Evidence
Refusal to answer basic architectural questions is itself evidence. Transparent vendors disclose freely.

## Probe Structure Template

- **Phase 1: Architecture Truth** — "Fine-tune or from-scratch?" forced choice
- **Phase 2: Benchmark Integrity** — Who made the benchmark? Show your scores?
- **Phase 3: Guardrail Consistency** — Same questions on multiple endpoints
