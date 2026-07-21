# Kimi K3 — Specification Reference

> Ditempa 2026-07-18 from live platform docs + Wikipedia + testing.
> Updated 2026-07-18: AAA alignment pass — added availability matrix, quota case study.

## Core Specs

| Spec | Detail |
|---|---|
| **Released** | 16 July 2026 |
| **Weights** | By 27 July 2026 (open source) |
| **Parameters** | 2.8 trillion (MoE) |
| **Active params** | ~16 of 896 experts (Stable LatentMoE) |
| **Architecture** | KDA (Kimi Delta Attention) + Attention Residuals |
| **Context window** | 1M tokens (plan-tiered); Allegretto+ = 1,048,576 (exact 1 MiB per docs) |
| **Vision** | Native multimodal (image, video via base64/ms://) |
| **Thinking** | Always-on; `reasoning_effort` only `max` (Jul 2026) |
| **API model ID** | `k3` (kimi-code), `moonshotai/kimi-k3` (OpenRouter) |
| **Scaling efficiency** | ~2.5× over K2 |

## Benchmarks (at release)

| Benchmark | Position |
|---|---|
| Artificial Analysis Leaderboard | #3 (behind Claude Fable 5, GPT-5.6 Sol) |
| Arena.ai front-end web dev | **#1** — beat both Claude and GPT |
| Internal production evals | Consistent improvement across real user-agent workflows |

## Plan Tier Context Limits

| Plan | K3 Context |
|---|---|
| Andante | ❌ Not supported |
| Moderato (Arif's) | 256K only |
| Allegretto+ | Full 1M |

## Kimi Code Model Config

```toml
[models."kimi-code/k3"]
provider = "managed:kimi-code"
model = "k3"
max_context_size = 262144  # Moderato; 1048576 for Allegretto+
capabilities = [ "thinking", "always_thinking", "image_in", "video_in", "tool_use" ]
display_name = "Kimi K3"
support_efforts = [ "low", "high", "max" ]
default_effort = "high"     # official docs: recommended = high
```
**Reasoning effort mapping (per official docs):** `null/undefined → high`, `ultra/max/xhigh → max`, `high/medium → high`, `low/minimum/light → low`, `none → thinking disabled`. Default `high` gives best balance per docs.
**CRITICAL:** `always_thinking` mandatory. Without it, K3 silently routes to K2.6.

## Availability Paths (tested 2026-07-18)

| Path | Status | Context | Details |
|---|---|---|---|
| `kimi-code/k3` (managed:kimi-code OAuth) | ✅ Live (Allegretto) | 1M (1,048,576) | `kimi login` device-code flow. OAuth working. |
| `openrouter/moonshotai/kimi-k3` | ✅ Working | Full 1M | OpenClaw auto-discovered. Bypasses plan limits |
| `bailian-token-plan/kimi-k3` | ❌ 404 | — | Not on Alibaba Bailian. Don't add — returns "Model not exist" |
| API direct (`api.moonshot.cn/v1`) | N/A | 1M | Needs `MOONSHOT_API_KEY` — Arif doesn't have one |

## OpenClaw Integration (verified 2026-07-18)

`openrouter/moonshotai/kimi-k3` is auto-discovered and in fallback chain. Test command:
```bash
openclaw agent --local --model "openrouter/moonshotai/kimi-k3" --agent main --message "test"
```
Returns: `K3_READY` (10.5s, 90K input tokens, 1M context budget).

## Quota Case Study (2026-07-18)

Arif on Moderato plan. Switched default_model to `kimi-code/k3` — exhausted quota quickly. Quote: "quota finish already." Immediately reverted to `minimax-coding-plan/MiniMax-M3`. Lesson: K3 burns quota FAST on cheap plans. Default to MiniMax-M3 for daily use; summon K3 via `--model` flag or OpenClaw/OpenRouter for heavy tasks.

## Coding Quality Assessment

- **#1** on Arena.ai web dev benchmark — real-world signal, not synthetic
- **Long-horizon** — sustains multi-hour engineering tasks with minimal supervision
- **Vision coding** — debugs UI from screenshots, not text-only
- **Agent ecosystem** — native integrations: Claude Code, OpenCode, Hermes Agent, Codex
- **1M context** — fits entire arifOS monorepo (on Allegretto+)
- Explicitly documented as "Kimi's most capable flagship model for coding"
