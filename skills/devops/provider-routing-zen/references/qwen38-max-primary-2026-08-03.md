# Qwen3.8-Max as Hermes Primary — 2026-08-03

State change: Hermes primary moved from `deepseek-v4-pro` to `qwen3.8-max` on
the qwen-token-plan provider (Team Pro seat).

## Facts (verified live 2026-08-03)

| Item | Value |
|---|---|
| Model ID (GA) | `qwen3.8-max` |
| Preview ID (retired) | `qwen3.8-max-preview` — retires ~2026-08-05; config migration done, only `.bak` files retain it |
| Provider | `qwen-token-plan` (key: QWEN_HERMES_API_KEY, Team seat, rotated 2026-08-01, prefix sk-sp-H.IP) |
| Pricing (GA) | $2.0 / $6.0 per 1M in/out, $0.25 cache-hit |
| Context / output | ~984K ctx (config sets 1,048,576) / 131,072 max output |
| Vision | **native base64 (data: URI) verified live** — 6.3s, correct answer. PRMT transcript pipeline now optional |
| Reasoning | always-on (low/high/xhigh), default xhigh; `reasoning_effort: ''` = xhigh, intentional |
| Architecture | 2.4T total, 95B active, MoE |
| Latency (agent.log, real) | 11-19s cached turns (99% cache hit), ~82s heavy reasoning, 37s cold context |
| Open weights | promised week of 2026-08-10 (2.4T + Qwen3.8-27B) — Ψ-survival tier upgrade candidate |

## Live fallback chain (2026-08-03)

```
PRIMARY:  qwen3.8-max        @ qwen-token-plan
  ↓       deepseek-v4-pro    @ opencode-go   (reasoning reserve)
  ↓       MiniMax-M3         @ minimax        (independent provider + compression)
```

## Hard rules that did NOT change

- 666_JUDGE / 999_SEAL = DeepSeek v4-pro ONLY (FFF gate pending for Qwen3.8-Max;
  registry: `identity_verified: false`, `constitutional_roles_forbidden`).
- Sovereign/MY-governance topics (PETRONAS/1MDB/myKad) route DeepSeek direct —
  Qwen carries baked-in guardrails + cross-border data transfer (Singapore region).
- 333/hands, 888/judge constitutional separation unchanged.

## Benchmarks worth knowing (vendor table, GA blog 2026-08-02)

Wins: PaperBench 93.0, OSWorld-Verified 86.1, IFBench 82.8, Terminal Bench 2.1 86.6.
Losses: HLE 43.6, SWE-bench Pro 67.7 vs Fable 5's 80.0. ~40% of the table is
in-house QwenBench — discount accordingly. Only independent test at preview time:
Trilogy AI 80/100 vs Kimi K3 83/100 (single run, single task).

## Operational notes

- ToS Token Plan: interactive use only — agent-as-backend is the accepted gray zone
  on Team seats (not Individual seats; Individual = ToS violation + rolling windows).
- Registry anomaly seen: AGENT_MODEL_MAP.json entry dated 2026-08-05 with
  `probed_by: 333-AGI via GA announcement email` — ingest date ≠ verified date;
  trust live probes over registry dates.
- Probe recipe: `scripts/tokenplan-model-probe.py` in this skill.
