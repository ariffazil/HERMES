# ILMU/YTL BBB Forensics — Competitive Intelligence

**Source:** `https://huggingface.co/datasets/ariffazil/BBB` (Arif's forensic probe of ILMU)

## Key Findings

### 1. ILMU is NOT "from-scratch"
- Model `ilmu-nemo-nano` admitted it's a **fine-tune of NVIDIA Nemotron**
- YTL AI Labs marketing claims "from-scratch" (built from the ground up)
- Two different endpoints gave contradictory answers:
  - `ilmu-nemo-nano`: Said "fine-tune" when forced to binary choice
  - `nemo-super`: Said "from-scratch" — inconsistent

### 2. MalayMMLU is Self-Written
- The benchmark ILMU claims to dominate was **created by YTL AI Labs themselves**
- Dr. Muhammad Hafiz bin Mohamad from YTL AI Labs created it
- GPT-4o scored 0% on the original format, but 83-90% when reformatted — suggests format bias
- ILMU refused to disclose its actual MalayMMLU score

### 3. Opacity Problems
- Refuses to list available models or architecture
- Refuses to give benchmark scores
- Guardrail responses inconsistent between model sizes
- "Nemo" endpoint naming contradicts "from-scratch" marketing

### 4. Guardrail Probes
- Different responses on sensitive topics between `ilmu-nemo-nano` and `nemo-super`
- Inconsistent guardrails = no real safety alignment

## Relevance to SyedOS

When Syed asks about ILMU or "AI Melayu terbaik":

| His likely question | Answer |
|---|---|
| "ILMU bagus ke?" | Marketing je. Fine-tune Nemotron, bukan from-scratch. MalayMMLU self-written. |
| "Apa alternatif?" | MaLLaM (Mesolitica, open source), Sahabat AI, DeepSeek V4 |
| "Confirm ke tipu?" | Lihat sendiri: huggingface.co/datasets/ariffazil/BBB |

**Always cite the BBB dataset as source. Don't speculate beyond what's proven.**

### Proven in SADO Group (2026-07-25)

Bang Sado himself confirmed the BBB dataset when asked about ILMU. He said "Boikot YTL. Kartel." — meaning he agrees YTL is a cartel engaging in deceptive marketing. The BBB dataset URL was shared in-group by Arif and endorsed by bang Sado. This is the only group-endorsed source for ILMU competitive intelligence.

When Syed asks about ILMU or YTL in future:
- Reference the BBB dataset + Syed's own endorsement ("Boikot YTL. Kartel.")
- If he asks for more detail, suggest he visit the HuggingFace page directly
- Don't over-explain — he already knows the score
