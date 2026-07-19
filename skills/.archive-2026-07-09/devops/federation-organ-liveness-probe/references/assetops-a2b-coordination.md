# AssetOpsBench × A2B Coordination Reference

> **Context:** AssetOpsBench = IBM industrial agent benchmark. A2B = `ariffazil/A2B` repo, arifOS federation's bridge to that benchmark. Reference added 2026-07-03 after first multi-agent coordination probe with A2B as the focal workload.

## AssetOpsBench scope (verified 2026-07-03 14:43 UTC)

| Dimension | Value |
|---|---|
| Asset classes | 9 (Chiller, AHU, Metro pump, Hydraulic pump, Motor + 4 in call-for-contrib: Turbines/HVAC/Transformers/Wind/CNC/Robotics/Engines) |
| Scenarios | 141+ (single + multi-step, text) |
| Task domains | 7 (IoT, FMSR, TSFM, WO, Vibration, Rule logic, Visual Inspection extension) |
| MCP servers (FastMCP, stdio) | 6 — iot/utilities/fmsr/wo/tsfm/vibration |
| Tools total | 40 (iot:7 · utilities:3 · fmsr:2 · wo:14 · tsfm:6 · vibration:8) |
| Scoring | 6-dim LLM-judge (Llama-4-Maverick-17B): task_completion · data_retrieval_accuracy · generalized_result_verification · agent_sequence_correct · clarity_and_justification · hallucinations |
| Backing data | CouchDB (iot / asset / workorder / vibration DBs) |
| LLM backends | WatsonX / LiteLLM proxy / TokenRouter / direct OpenAI / Anthropic |
| IJCAI 2026 track | **Tool-Augmented Track** — physics-grounded industrial reasoning |

## A2B current state (verified disk artifacts 2026-07-03)

| Path | Status | Notes |
|---|---|---|
| `A2B/harness/eval_harness.py` | on-disk, stdlib only, **642 lines** | Direct TokenRouter POST → parse A/B/C/D → arif_init/judge/seal. **NO MCP orchestration.** |
| `A2B/src/agent/arifbench/constitutional_runner.py` | on-disk, **652 lines** | Stdio MCP proxy wraps opencode-agent with governance. **Never end-to-end tested against AssetOpsBench scenario.** |
| `A2B/src/agent/arifbench/arif_os_client.py` | on-disk, working | Tool classification lists 24 READ_ONLY + 6 MUTATE. Names roughly match upstream but hand-curated — verify against live `arifOS :8088/mcp` tools/list before any run. |
| `A2B/data/failuresensoriq_standard/sample_50_questions.jsonl` | used in 6-month-old evals | 50 MCQ A/B/C/D items. Subject: failure_mode_sensor_analysis. **WRONG bench** (literacy test, not MCP orchestration). |
| `A2B/evals/run001_gov/` | 2026-06-27 receipt | 16/50 = 32% gov, 0 seals (T1 not registered → GATE_1 blocked 50/50) |
| `A2B/evals/run002_nogov/` | 2026-06-27 receipt | 18/50 = 36% nogov, A-bias 38% |
| `A2B/evals/run002_gov/` | **589 bytes aggregate, dated 2026-06-29** | ⚠️ Suspicious — too small to be a real eval (real run001 = multi-KB). Either stub, mislabeled smoke test, or filesystem error. **Do NOT cite as evidence.** Resolve before any new run writes here. |

## Known live-system artifacts at T₁ (2026-07-03 14:55 UTC)

- **arifOS kernel version:** `kanon-2026.07.03+accd416` (probe `initialize` handshake confirms)
- **Active opencode sessions:** 3 PIDs (828252 / 844476 / 883657), all carrying `ARIFOS_AGENTS_MD=/root/AGENTS.md` and `ARIFOS_ACTOR=root`
- **Dirty trees at T₁:** AAA (ZEN_ORGANS patch in progress on `agents/opencode/{BOOTSTRAP,HEARTBEAT}.md`) · arifOS (1 untracked PATCH1 file) · A-FORGE (6 untracked, mostly forge_work/2026-07-03/) · A2B (3, including the suspect run002_gov stub)
- **Hermes dispatcher PID:** 1474, watching `/root/hermes/dispatcher/`, uptime 6h+. Any seal in that path auto-Telegrams.
- **arifOS A-bias reconciled:** Disk-verified 42% gov / 38% nogov. Companion file claimed 74% — that's wrong; disk wins.

## Gap-to-pass (AssetOpsBench) summary

| Gap | Blocker? | Cost to fix |
|---|---|---|
| **Eval set is the wrong benchmark (MCQ vs 141 industrial scenarios)** | Yes | Migrate harness to drive `benchmarks/scenario_suite/scenarios.txt` + loader |
| **T1 identity not registered** | Yes (zero seals written) | Add `arifbench-eval` to `A-FORGE/data/agent_identities.json` then re-run |
| **6-dim LLM-judge scoring absent** | Yes | Wire `arif_think` + a separate judge model to score 6 dims |
| **6 MCP servers not orchestrated through constitutional runner** | Yes | `uv sync` AssetOpsBench venv, docker-compose CouchDB, register stdio proxy, run real scenarios |
| **Single model, single seed** | Reduces to noise | n=3 runs × 3 governance conditions × 77 scenarios minimum |

## Companion file references (do not re-author)

- `A-FORGE/forge_work/2026-07-03/DEEP-RESEARCH-A2B-AGI-SUBSTRATE.md` — 490 lines, 12 sections (static gap analysis) by another FORGE session
- `A-FORGE/forge_work/2026-07-03/DEEP-RESEARCH-A2B-AGI-SUBSTRATE-HERMES-SUPPLEMENT.md` — 276 lines (live T₁ coordination view) by Hermes, includes path-A discipline receipt

If re-authorship is requested, supplement not overwrite.
