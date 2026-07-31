# PRMT Epistemic Dependency — F2 TRUTH Vulnerability

> **Insight forged:** 2026-07-30, Sesi Wolf Cabinet + MuleRouter
> **One breath:** Language is not the medium — language IS the reality. If Qwen-VL doesn't write it, DeepSeek cannot know it.

## The Architecture

In arifOS PRMT (Pre-Routing Modality Translation), perception and judgment are **decoupled by design**:

```
Δ (Perception)     → Qwen-VL via MuleRouter → [text transcript]
Ω (Judgment)       → DeepSeek via MuleRouter → reads transcript, reasons
```

DeepSeek is **fundamentally blind**. It has no direct visual access. Its reasoning ceiling is strictly bounded by Qwen-VL's descriptive floor.

## F2 Vulnerability

| Property | Value |
|----------|-------|
| DeepSeek's reasoning ceiling | = Qwen-VL's descriptive floor |
| Information loss | One direction — Qwen-VL can't be queried for follow-up |
| DeepSeek's awareness of gaps | Zero — it doesn't know what it missed |
| Fix mechanism | Prompt engineering on enrichment layer |

If Qwen-VL describes "lelaki sasa" instead of "Chris Bumstead":
- DeepSeek's logic ESTP = reasoning is **perfectly sound**
- DeepSeek's answer "lelaki sasa" = factually **wrong** (F2 < 0.99)
- No one in the pipeline detects the gap

## This is NOT a Bug — It's a Design Constant

This is the defining property of decoupled perception-judgment architecture. The same property gives us:

| Advantage | How |
|-----------|-----|
| Zero 413 cascade | Only text enters DeepSeek's context (proven 2026-07-30) |
| Provider swap isolation | Change Qwen-VL without touching DeepSeek |
| Cost optimization | Cheapest vision model can serve richest reasoning model |
| F1 AMANAH safe | Reversible — retry enrichment, never fatal |

**The price of these advantages is the epistemic bottleneck.** This is a conscious trade-off, not a defect.

## Mitigation Strategy

1. **Enrichment prompt injection** — The prompt sent to Qwen-VL MUST include a system-level instruction to extract ALL visual detail (identity, text, brands, spatial) before addressing the user query. Never leave extraction to the model's default behavior.

2. **User discipline** — When sending images, include specific context in the caption ("this is CBUM", "what brand is this shirt"). Don't assume the vision model will identify specifics unprompted.

3. **Multiple enrichment passes** — For high-stakes visual tasks, route through TWO vision models and cross-validate transcripts before sending to DeepSeek (future capability, not yet implemented).

4. **Fallback detection** — If enrichment produces an empty or minimal transcript, surface "deskripsi terhad" to the user rather than forwarding a low-fidelity description to DeepSeek.

## Relationship to Wolf Cabinet Model

```
Wolf Cabinet Layer      | Component      | Epistemic role
Δ (Perception)          | MuleRouter     | Reality is constructed here
  └─ Enrichment prompt  | This session   | Quality of reality
Ω (Judgment)            | DeepSeek       | Reasons over constructed reality
  └─ Bounded by          | Qwen-VL        | Cannot see what wasn't written
```

The Wolf Cabinet resolves the surface contradiction (satu roof vs constitutional redundancy). The epistemic dependency resolves the **deep contradiction**: how can a blind model judge reliably? Answer: it can't, unless the perception layer is engineered to extract reality completely.
