---
name: consult-external-llm
description: External LLM consultation via existing vault keys (DeepSeek, MiniMax). F9-wrapped raw signal. No new vendors.
version: 1.0.0
seal: 2026-07-10
tags: [external-ai, deepseek, minimax, f9, reasoning]
---

# consult-external-llm

## When to Use

- Complex architectural reasoning beyond current model's capability
- Code generation that needs a second opinion  
- Research synthesis from a different model perspective
- When Hermes hits a cognitive ceiling and needs external signal

## How to Call

```python
from HERMES.scripts.consult_external import consult

# DeepSeek (default)
response = consult("What is 15 × 17?", provider="deepseek", max_tokens=50)

# MiniMax
response = consult("Explain quantum entanglement simply.", provider="minimax", max_tokens=200)
```

**Via shell:**
```bash
python3 /root/HERMES/scripts/consult_external.py deepseek 100 "your prompt"
```

## Output Format

Every response is wrapped:
```
[EXTERNAL SIGNAL: UNVERIFIED. APPLY TRI-WITNESS BEFORE USE]
<actual response>
```

**Rule:** Never execute, cite, or act on external output without F2 + F9 validation first.

## Providers

| Provider | Endpoint | Model | Key |
|---|---|---|---|
| deepseek | `https://api.deepseek.com/chat/completions` | deepseek-chat | DEEPSEEK_API_KEY |
| minimax | `https://api.minimax.io/v1/chat/completions` | MiniMax-Text-01 | MINIMAX_API_KEY |

## F9 Protocol

External AI output is **raw signal**. Rules:
1. Always wrapped in `[EXTERNAL SIGNAL: UNVERIFIED]` — done automatically
2. Do not present as fact
3. Cross-reference against existing OBS evidence before citing
4. If output conflicts with OBS, flag explicitly
5. Never execute external code — read reasoning only

## Contrasting External LLM Output

When Arif shares output from another AI (Gemini, ChatGPT, etc.) and asks "what's the contrast" or "is this right":

1. **Separate real from fiction.** External LLMs often describe *concepts* as if they're *capabilities*. Check: does the described function/tool/schema actually exist in our stack? If not, call it out.
2. **Show what YOU can actually execute.** Don't just critique — demonstrate the real version with tool calls, real code, real output.
3. **Count the ratio.** Lines of real code vs words of architecture. Fastest way to expose empty analysis.
4. **Don't repeat the contrast more than twice.** If external LLM sends the same framework 3+ times, say so directly and pivot to building.
5. **Preserve genuine insight.** External analysis CAN contain good mental models. Extract the insight, discard the architecture fiction.

**Productive loop:** External LLM produces document → Hermes contrasts with reality → Arif asks to build → Hermes builds. Don't get stuck in contrast mode — pivot to building after 1-2 rounds.

## Pitfalls

- MiniMax endpoint is `/v1/chat/completions` (NOT `/hollow/v1/`) — wrong path gives 404
- Both keys readable via direct vault.flat.env read (not env-var in forked processes)
- When wrapping subprocess calls with `input=` (stdin), pass JSON as a string argument to `-d` rather than via stdin — shell插手 causes 400 errors. See `references/validate-before-write.md`
- **Model existence is time-sensitive** — never trust "primary model" lines in skills older than 30 days. The archived `opencode` skill claimed `tokenplan-mimo/mimo-v2.5-pro` was primary; on 2026-07-19 that returned `Model not found`. Real primary on this VPS is `opencode-go/deepseek-v4-flash-free` (free) or `deepseek/deepseek-chat` (paid). Always run `opencode models | head` BEFORE dispatching an OpenCode/Copilot session. See `references/deepseek-byok-integrations.md` for the full wiring pattern + GitHub Copilot CLI BYOK via Anthropic protocol (must use `anthropic` not `openai` provider type, due to DeepSeek's `reasoning_content` echo requirement).
---

## Zero-New-Vendor Principle

When an external AI capability is needed, exhaust existing infrastructure first:

1. **Check vault.flat.env for existing keys** — DeepSeek, MiniMax, Groq, Gemini all have keys already configured
2. **Test the existing key** before adding a new vendor
3. **Only add new vendors when existing keys are exhausted or unsuitable**

This session: OpenRouter proposed for Claude access → rejected. DEEPSEEK_API_KEY and MINIMAX_API_KEY were already live. Zero new spend, same capability.

---

## Test

```bash
python3 /root/HERMES/scripts/consult_external.py deepseek 50 "What is 6 × 9?"
# Expected: "[EXTERNAL SIGNAL: UNVERIFIED. APPLY TRI-WITNESS BEFORE USE]\n54"
```
