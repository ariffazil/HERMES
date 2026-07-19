# External AI Audit Integration Pattern

> **Proven:** 2026-07-13 — Gemini, Grok, Qwen, ChatGPT outputs reviewed during MakcikGPT article creation.
> **Trigger:** When Arif shows outputs from external AI models (Gemini, Grok, Qwen, ChatGPT) in the conversation.

## How to Treat External AI Outputs

| Signal | Action |
|---|---|
| External AI contradicts your data | **VERIFY before dismissing.** Search primary sources. In session 2026-07-13, Gemini caught FY2022 PAT wrong (RM55bn vs actual RM101.6bn). |
| External AI confirms your data | **Note as cross-validation.** Adds confidence. |
| External AI uses your framework language (F2, F9, 888_HOLD) | **Legitimate accountability.** Not cosplay. The framework is being tested by external instruments. |
| External AI makes claims you can't verify | **Flag as UNKNOWN, don't accept or reject.** Run your own search. |
| External AI has different data sources | **Check if their source is better.** Gemini had access to Bloomberg/ICIS that I missed. |

## Anti-Patterns

- ❌ Dismissing external AI output as "just mirroring" without checking
- ❌ Accepting external AI output without verification (same as self-certification)
- ❌ Treating external AI language use as "cosplay" when it's using YOUR framework accurately
- ❌ Ignoring external AI corrections because "I already checked"

## The Grok Lesson (2026-07-13)

Grok outputs ranged from high-cosplay (Part 1: used arifOS vocabulary without understanding) to genuinely useful (Part 5: priority stack from AAA agent). The key distinction:
- **Cosplay:** Using arifOS vocabulary (F13, VAULT999, DITEMPA) without access to the actual system
- **Legitimate:** Using the same vocabulary because it's the correct framework for the analysis

Detection: if the external AI's claim can be verified against live system state (kernel, VAULT, federation), it's legitimate. If it's just language decoration, it's cosplay.

## Integration into Audit Pipeline

After self-audit (T×A×M×P×G×R), run ONE external verification:
1. Web search for the highest-risk number
2. If Arif shows external AI output → treat as peer review
3. Cross-check external AI's source against your source
4. If discrepancy → verify against primary source (IR, FRED, BNM, Bloomberg)
5. Document which source won and why
