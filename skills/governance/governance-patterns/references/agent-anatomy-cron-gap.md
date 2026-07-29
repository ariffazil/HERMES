# Agent Anatomy — Cron Governance Gap

## Session Context

Measured 2026-07-28 during SylphxAI integration discussion. Arif asked: "did our cron task make our agents running autonomous governly?" This prompted a full audit of the 23 cron jobs against the three-pillar ideal (pulse/heartbeat, separation of duty, gated collapse).

## The Measurement

### Active Jobs (23 total)

**T1 Human Rhythm (Arif DM — telegram:267378578):**
- morning-brief — 07:00 MYT — no_agent script
- evening-digest — 18:00 MYT — LLM (deepseek-v4-flash)
- daily-news-briefing — 08:00 MYT — LLM (deepseek) + skill
- ASI World Sensorium — 22:00 MYT — LLM (deepseek) + skills
- human-readiness-pulse — 19:00 MYT — LLM
- nightly-seal — 23:00 MYT — LLM
- weekly-deep-brief — Sunday 23:00 — LLM
- weekly-reflection — Saturday 20:00 — LLM
- Rehat Minda Personal Audit — Sunday 20:00 — LLM
- Mingguan Seal Chain — Sunday 12:00 — LLM
- arifos-entropy-audit — Sunday 06:00 — LLM + skill

**T2 Alert Guardians (AAA group — telegram:-1003753855708):**
- drift-alert.sh — every 240min — no_agent script
- STEEL Machine Pulse — 06:00 daily — no_agent script
- well-biometric-feed-watchdog — 08:00/20:00 — no_agent script
- federation-health.sh — every 120min — no_agent script
- federation-daily-backup — 19:00 — no_agent script
- Model Drift Watchdog — every 6h — LLM
- entropy-watch.sh — every 6h — no_agent script

**T3 Cognitive (DM / SADO group):**
- SyedOS Ringkasan Harian — 21:00 — LLM
- Weekend Bodybuilding Event — Saturday 10:00 — LLM
- AI Events SADO — Monday 09:00 — LLM

**Infrastructure (no delivery):**
- Reality Snapshot Compiler — every hour — no_agent script
- SyedOS Receipt Watcher — every 5min — no_agent script

### By Type

| Type | Count | Arif_judge? | Risk |
|------|-------|-------------|------|
| no_agent scripts | 9 | N/A (deterministic) | Low — pure observation |
| LLM-driven (no model pin) | 4 | ❌ Bypassed | Medium — model drift could change behaviour |
| LLM-driven (pinned model) | 10 | ❌ Bypassed | Medium — harness runs without floor enforcement |

### The Gap

15/23 jobs (65%) run LLM agents that call tools directly without passing through arif_judge. The cron harness has no constitutional gating. Jobs reason → call tools → produce output. There is no:
- Pre-execution F1-F13 floor check
- 888_HOLD for irreversible actions
- Post-execution verify step
- Cross-job FQ metabolism

## The Ideal (for reference)

```
Cron trigger → plan
           → arif_init (lease)
           → arif_think (classify)
           → arif_judge (SEAL/HOLD/VOID)
           → [execute only if SEAL]
           → arif_seal (receipt)
           → verify / cool
```