# Mage Evaluation — 2026-07-25

**Technology:** Microsoft Mage (Mage-Flow + Mage-VL + Mage-VAE)
**Verdict:** ⭐️⭐️⭐️ — SABAR (track, don't deploy)
**Location:** `/root/forge_work/references/mage/` (303MB)
**Full reference:** `_notes/MAGE-REFERENCE.md`

## Key Learnings

### Architecture Worth Remembering

**Mage-VAE** is the most novel component — a lightweight latent tokeniser using one-step diffusion encode/decode with anchor-latent KL regularisation. Matches FLUX.2-VAE quality with ~12× fewer encode MACs and ~22× fewer decode MACs. Could inform future GEOX domain-specific latent spaces.

**NR-MMDiT** (4B Native-Resolution MMDiT) — rectified flow matching, native-resolution packing (FlashAttention var-len + per-sample 2D RoPE), packaged CFG inference. Stack-level CUDA kernel fusion achieved MFU 14% → 29%.

### Performance

- **Mage-Flow RL**: GenEval 0.90 — #1 open-source (beats FLUX.2 32B, Qwen-Image 20B)
- **Mage-Flow-Turbo**: 4-step, 0.59s/image at 1024² on A100, ~18GB VRAM
- **Mage-Flow-Edit**: ImgEdit 3.34/5 — second only to GPT-Image-1 closed (3.40)

### Why SABAR

1. No GPU on this VPS (nvidia-smi returned empty, 31GB RAM only)
2. Mage-VL (vision-language understanding) not yet released — the half that would actually complement our stack
3. Existing API-based generation (lightweight-image-generation, minimax-cli) already covers the use case

### Trigger Conditions for FORGE

- Mage-VL releases code + weights → reassess as local VL for GEOX/WELL
- GPU acquired (≥18GB VRAM) → deploy Mage-Flow-Turbo as MCP tool
- GEOX needs domain visual gen → fine-tune on geological imagery

### Quick Reference

```bash
# Paper
/root/forge_work/references/mage/mage-flow-paper.pdf  # 43MB, 59pp
# Repo
/root/forge_work/references/mage/  # git clone --depth 1
# Reference note
/root/forge_work/references/mage/_notes/MAGE-REFERENCE.md
```
