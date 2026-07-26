---
name: flame-free-loop-mesh
description: "Operate the RM0 Free-Loop AI Model Engine — hit-rate-adaptive, graceful-swap inference mesh for tools and system workers. Two-lane architecture with L3 task-routing."
---

# FLAME — Free Loop AI Model Engine

> **DITEMPA BUKAN DIBERI** — Forged 2026-07-20

FLAME is a non-agentic inference mesh — pure RM0 throughput for tools, workers, batch jobs, and pipelines. Zero governance authority. Zero cost.

## Architecture: Two-Lane Design

```
AGENT LANE (governed cascade):
  TokenRouter → MiniMax → MiMo → Groq → Gemini → Cerebras → SEA-LION → Ollama → HOLD
  Constitutional. F1-F13 gated. Judges + seals.

TOOL LANE (FLAME free-loop):
  Groq → SEA-LION → Gemini → Cerebras → Ollama
  Hit-rate adaptive. RM0. Swap-on-fail. No governance.
```

## Fleet (17 models, 8 providers, all RM0)

> **Ground truth:** `flame --mode probe`. Updated 2026-07-25: SambaNova added (1K tok/s, ultra-fast Llama 3.3 70B). Mistral added (Small/8B/Nemo/Codestral — 262K ctx, JSON-native). HuggingFace Inference API added (30K+ models). Ollama dropped (18ms connection refused). OpenRouter relegated Tier-3 fallback (20rpm/50rpd). See `flame_config.json` for the definitive tier list.

| Priority | Provider | Model | Latency | Role |
|----------|----------|-------|---------|------|
| 1 | Groq | qwen/qwen3.6-27b | **~292ms** | Primary extent |
| 2 | **SambaNova** | **Meta-Llama-3.3-70B-Instruct** | **~300ms** | **1K tok/s, deep reasoning** |
| 3 | Groq | llama-3.3-70b-versatile | ~159ms | Deep reasoning |
| 4 | Groq | llama-3.1-8b-instant | ~586ms | Fastest, high-volume |
| 5 | Cerebras | gpt-oss-120b | ~337ms | Fast fallback |
| 6 | Groq | openai/gpt-oss-120b | ~473ms | Deep fallback |
| 7 | Cerebras | gemma-4-31b | ~786ms | Multimodal, vision |
| 8 | Gemini | gemini-flash-lite-latest | ~598ms | 1M context, conciseness |
| 9 | Mistral | **mistral-small-latest** | ~1.2s | **262K ctx, JSON-native** |
| 10 | Mistral | ministral-8b-latest | ~900ms | Efficient general |
| 11 | Mistral | open-mistral-nemo | ~1.5s | Open model fallback |
| 12 | Mistral | codestral-2508 | ~1.8s | Code specialist, 256K ctx |
| 13 | SEA-LION | Qwen-SEA-LION-v4-32B-IT | ~2019ms | BM native |
| 14 | SEA-LION | Llama-SEA-LION-v3-70B-IT | ~1463ms | BM deep |
| 15 | SEA-LION | Gemma-SEA-LION-v4-27B-IT | ~1482ms | BM fast |
| 16 | OpenRouter | :free aggregator | ~1042ms | **Tier-3 fallback** (20rpm/50rpd) |
| 17 | HuggingFace | 30K+ models | varies | **Specialized** (via HF_TOKEN) |

**Dropped:** Ollama qwen2.5-coder:3b — 18ms connection refused. Re-add only after `ollama list` confirms runtime.

## CLI Usage

```bash
# Single prompt
flame "Summarize this log: ..."

# With system prompt
flame --system "You are a classifier." "Classify: ..."

# Modes
flame --mode probe       # Health check all models
flame --mode stats       # Hit-rate table
flame --mode seal        # Integrity seal
flame --mode summarize   # Auto system prompt
flame --mode classify    # Auto system prompt

# Batch
flame --batch prompts.txt

# JSON output
flame --json "What is the capital of Malaysia?"
```

## Key Files

| File | Purpose |
|------|---------|
| `/root/A-FORGE/flame/flame_router.py` | Engine + CLI — `FlameEngine` class, CLI dispatch, `TASK_CLASS_CHAINS` |
| `/root/A-FORGE/flame/flame_api_server.py` | HTTP API server (port 18901) — `/summarize`, `/classify`, `/v1/chat/completions` |
| `/root/A-FORGE/flame/flame_config.json` | Fleet + providers + routing config (versioned) |
| `/root/A-FORGE/flame/flame_control_registry.json` | Tool eligibility registry, 6 control gates |
| `/root/A-FORGE/deploy/systemd/flame.service` | Systemd unit file |
| `/root/A-FORGE/src/tools/flameClient.ts` | TypeScript client for A-FORGE MCP tools (forge_search, forge_diagnose, forge_summarize, forge_draft_plan) |
| `/root/A-FORGE/flame/flame_client.py` | Python CLI client for A-FORGE — `flame_infer`, `flame_extract`, `flame_diagnose`, `flame_summarize`, `flame_draft_plan` |
| `/root/.hermes/scripts/cerebras-watchdog.sh` | Cerebras credit watchdog wrapper — delegates to `flame_cerebras_watchdog.py`. Runs every 30 min via cron `Cerebras Watchdog`. |
| `/etc/systemd/system/flame.service` | Active unit (enabled, running) |
| `/etc/systemd/system/flame.service.d/chain.conf` | Override: `FLAME_CHAIN=RM0-TOOLS-FREELOOP` |
| `/usr/local/bin/flame` | Symlink → flame_router.py |
| `/usr/local/bin/free-llm` | Symlink → flame_router.py |
| `/root/.local/share/flame/flame_state.json` | Hit-rate state |
| `/root/.local/share/flame/flame_hitrate.jsonl` | Event log |
| `/root/.local/share/flame/flame_health.jsonl` | Health probe history |

## Features

- **Hit-rate adaptive routing** — Models sorted by success rate × latency score
- **Graceful swap** — Fail → next tier, no crash, no user impact
- **Health probes** — 1-token sanity check, censorship/refusal/malform detection
- **Dynamic tiering** — Promotes fastest, demotes failures
- **L5 Self-healing (2026-07-25)** — Auto-demote on **3 consecutive fails** (`HitRate.consecutive_fails` ≥ 3). Auto-**remove** on **10 total fails** (`fail + refuse + censor + safety_refuse` ≥ 10). `active=False` → call loop skips model via `continue`. Consecutive counter resets on any success. Removed models stay inactive until re-probed.
- **RM0 enforcement** — Paid models never enter chain
- **Seal** — SHA256 integrity hash of hit-rate state

## Wiring Status Audit (2026-07-25)

> **⚠️ KRITIKAL: 81-surface map adalah aspirational, bukan actual.**
| Coverage ratio | **~18%** (5 dari ~27 FLAME surfaces actually wired) |
> **Always verify actual wiring** — grep for `free-llm`/`FlameEngine` calls, don't trust the table.
> Classification flags (🔥/🚫 dalam dokumen) boleh **salah** — verified example: Paper Trading Morning/Zen flagged 🔥 tapi engine sebenarnya 100% deterministic NO-LLM.

| Metrik | Nilai |
|--------|-------|
| FLAME-PRIME dalam dokumen | 19 |
| CONDITIONAL dalam dokumen | 8 |
| Actually wired | **7** (RAG query.py + WEALTH refresh_briefing.py + GEOX contradiction_scan + GEOX evidence_synthesize + arifOS arif_observe + A-FORGE forge_search + tool cron jobs) |
| Cron guna FLAME | 0/6 (majoriti agent jobs — guna governed cascade intentionally) |
| Hermes tools wired | 0/4 (Hermes MCP tools not deployed as standalone services) |
| A-FORGE tools wired | **1/4** (forge_search via flameClient.ts) |
| GEOX tools wired | **2/5** (contradiction_scan + evidence_synthesize via flame_client) |
| arifOS tools wired | **1/4** (arif_observe search via flame_client) |
| Total calls | ~44 on Groq primary models |

### FLAME Upgrade Priority Sequence (Arif-ratified 2026-07-25)

```
Priority 1 — Flagged but unwired (12 surfaces)
  Action: Wire to FLAME immediately. Ini technical debt paling obvious.
  Scope: MCP tools (geox_*, arif_observe, forge_*, capital_market).
  NOT included: Cron jobs (agent-driven, intentional governed cascade).
  NOT included: Paper Trading (deterministic NO-LLM — see Pitfalls).
  ⚠️ Requires code changes in each organ repo — no blanket deploy.

Priority 2 — Remaining FLAME-PRIME (16 surfaces)
  Action: Push full FLAME integration (19 total − 3 currently wired = 16 pending).
  Scope: Surfaces memang di-design untuk FLAME. Standardize routing di sini.

Priority 3 — CONDITIONAL (8 surfaces)
  Action: Build strict gate logic (if-then ruleset for partial FLAME use).
  Never blanket deploy — clear ruleset required bila FLAME take over vs pass back.

Priority 4 — Boundary Lockdown (54 surfaces)
  Action: Audit + enforce isolation for GOVERNED-ONLY (14) + NO-LLM (40).
  Reason: W_scar protection (F1). Zero boundary bleed — FLAME never parses
  sovereign data.
```

**Routing Insight (from live telemetry):**

| Priority | Provider/Model | Latency | Role |
|----------|---------------|---------|------|
| Primary | **Groq qwen/qwen3.6-27b** | **292ms** | Route majoriti payload ke sini |
| Fallback | Groq llama-*, Cerebras gpt-oss-* | 159-786ms | Standard cascade |
| Tier-3 | OpenRouter :free aggregator | 1042ms | Rate-limited. Phase C fallback only. |
| ❌ Dead | Ollama qwen2.5-coder:3b | 18ms | Connection refused. Drop from active pool. |

### MCP Tool Wiring — Target Table

Each tool needs a `flame_client.py`/`.ts` helper that POSTs to `:18901` with task_class tagging.

| Organ | Tool | Task Class | Status |
|-------|------|-----------|--------|
| arifOS | `arif_observe` (search) | `extract` | ✅ **Wired** (2026-07-25) |
| GEOX | `geox_contradiction_scan` | `classify` | ✅ **Wired** (2026-07-25) |
| GEOX | `geox_evidence` (synthesize) | `summarize` | ✅ **Wired** (2026-07-25) |
| A-FORGE | `forge_search` | `extract` | ✅ **Wired** (2026-07-25) |
| GEOX | `geox_claim` (create) | `extract` | ⏸️ Pending |
| WEALTH | `capital_market` (signal) | `extract` | ⏸️ Pending |
| A-FORGE | `forge_diagnose` | `classify` | ⏸️ Tool doesn't exist as MCP surface |
| A-FORGE | `forge_summarize` | `summarize` | ⏸️ Tool doesn't exist as MCP surface |
| A-FORGE | `forge_plan` | `draft_plan` | ⏸️ F1 risk — advisory only |

### Verification Commands (Audit Reality vs Docs)

```bash
# What actually calls FLAME today
grep -r -l 'free-llm\|FlameEngine\|/usr/local/bin/flame' \
  /root/A-FORGE/dist/ /root/HERMES/ /root/arifOS/ \
  --include='*.{py,ts,js}' 2>/dev/null | grep -v __pycache__ | grep -v forge_work

# Daemon health + fleet
curl -s http://127.0.0.1:18901/health | python3 -m json.tool
free-llm --mode probe && python3 -c "
import json
d = json.load(open('/root/.local/share/flame/flame_state.json'))
for k, v in sorted(d.get('hitrates', {}).items()):
    c = v.get('calls', 0)
    s = v.get('success', 0)
    print(f'  {k:50s} {c:3d} calls, {s:3d} ok')
"

# Hit-rate stats
free-llm --mode stats
```

Full audit data: `references/2026-07-25-wiring-audit.md`

## Wired State (2026-07-25)

| Tier | Status | Detail |
|------|--------|--------|
| **Fleet** | ✅ 11/12 models live, T12 Ollama dropped (connection refused) |
| **Default chain** | ✅ RM0-TOOLS-FREELOOP (was TOKENROUTER-PRIMARY) |
| **Daemon** | ✅ systemd service (was manual) |
| **GEOX flame_client.py** | ✅ New — 8s timeout, graceful degradation, stateless, ADVISORY tagging |
| **geox_contradiction_scan** | ✅ Wired — FLAME fallback when 13-type ontology returns UNKNOWN |
| **geox_evidence (synthesize)** | ✅ Wired — FLAME via `flame_summarize()` replaces `arif_think` governed cascade |
| **arifOS flame_client.py** | ✅ New — lightweight duplicate per F1, fact-only prompt constraint |
| **arif_observe (search)** | ✅ Wired — FLAME synthesis appended to raw search results, raw context fallback |
| **L3 Task-Routing** | ✅ Active — classify/summarize/extract/bm_native chains, task_class tagging in all clients |
| **RAG query.py** | ✅ Already wired (pre-existing) |
| **Tool cron jobs** (5) | ✅ Model Drift Watchdog, IG Story, Trading Report, XAUUSD, Position Monitor → flame/free |
| **Agent cron jobs** (6) | 🔒 REVERTED to governed cascade — intelligence-to-Arif requires quality |

### P4 Boundary Lockdown — Verified 2026-07-25

**GOVERNED-ONLY (14)** — zero-FLAME zone, verified clean:
`arif_judge`, `arif_seal`, `arif_init`, `arif_think`, `capital_wisdom`, `capital_diagnose`, all `well_*` tools (8).

**NO-LLM (40)** — verified: Paper Trading Morning (100% deterministic), federation-daily-backup, STEEL Pulse, well-biometric-feed, Reality Snapshot, Model Picker, all hound tools.

## Integration Map: 81-Surface Classification

Every MCP tool, internal CLI, and cron job in the federation has been classified: **19 FLAME-PRIME**, **8 CONDITIONAL**, **14 GOVERNED-ONLY**, **40 NO-LLM**.

### Classification Framework

| Flag | Meaning | Action |
|------|---------|--------|
| 🔥 FLAME-PRIME | Tool internally calls an LLM for non-constitutional work | Route through FLAME |
| ⚡ CONDITIONAL | LLM for some sub-modes, governed for others | FLAME for non-seal sub-paths only |
| 🏛️ GOVERNED-ONLY | Constitutional hard boundary | NEVER FLAME |
| 🚫 NO-LLM | Pure compute, I/O, no inference path | Not applicable |

### Call Site Governance Categories

| Category | Count | Rule |
|----------|-------|------|
| ALLOWED | 8 | FLAME by default — title gen, skill extract, classify |
| FALLBACK | 6 | Governed primary, FLAME on exhaustion — arif_think non-constitutional, terminal chat |
| FORBIDDEN | 8 | Constitutional hard gate — judge, seal, PII, PETRONAS, sovereign |

### Highest-Impact FLAME-PRIME Candidates

| Surface | Component | Why | Effort |
|---------|-----------|-----|--------|
| arifOS | `arif_observe` (search,fetch) | Result synthesis | Medium |
| GEOX | `geox_contradiction_scan` | Pattern matching | Low |
| GEOX | `geox_evidence` (discover,synthesize) | Evidence synthesis | Low |
| GEOX | `geox_claim` (create) | Claim generation | Low |
| A-FORGE | `forge_search`, `forge_diagnose` | Semantic codebase, root cause | Medium |
| A-FORGE | `forge_summarize`, `forge_plan` | Summarization, planning | Medium |
| WEALTH | `capital_market` (signal) | Market interpretation | Medium |
| Scripts | `mimo-doctor.sh`, `mimo-fallback.sh` | Health routing | Low |

**NOT FLAME-PRIME (corrected classifications):**
- `arif_memory` (remember only) — P0-hardened to NOT use FLAME. Constitutional memory law.
- Hermes MCP tools (`hermes_fact_check`, `hermes_epistemic_check`, etc.) — not deployed as standalone services; they run within Hermes which uses governed cascade.
- `Paper Trading Morning/Zen` — engine is 100% deterministic (yfinance + numpy), zero LLM calls. **Should be NO-LLM, not FLAME-PRIME.** See `references/81-surface-flame-map.md` for the corrected flag.
- Cron agent jobs (`daily-news-briefing`, `evening-digest`, `weekly-reflection`) — produce user-facing content. Intentionally governed cascade. FLAME only suitable for sub-task summarization if a helper function is added.

### NEVER FLAME — Constitutional Hard Boundary

`arif_judge` · `arif_seal` · `arif_init` · `arif_think(reason/atlas/axioms)` · `arif_forge` · `capital_wisdom` · `capital_diagnose` · **all WELL tools** · GEOX claim seal · any tool touching sovereign data

### Full audit map

See `references/81-surface-flame-map.md` — complete 81-entry classification table covering every MCP tool, CLI, script, and cron job in the federation.

## L3 Task-Routing (Arif-ratified 2026-07-25)

> **High-leverage move:** Task routing beats latency routing. Latency is critical, but model-task fit defines intelligence.

FLAME router supports per-task-class chain priority via the `task_class` parameter.
When a request tags its intent, FLAME reorders the model chain to put the best
model for that task first — only falling through to the general pool if all
task-specific models fail.

### Task Class Chains (defined in `flame_router.py:TASK_CLASS_CHAINS`)

Includes Mistral (262K ctx, JSON-native), SambaNova (1K tok/s), and 8 providers.

| Task Class | Primary Model | Rationale | Fallback Chain |
|------------|--------------|-----------|---------------|
| `classify` | **SambaNova Meta-Llama-3.3-70B** (1K tok/s) | Deep reasoning, fast | Groq 70B → Groq 8B → Mistral Small → Gemini |
| `summarize` | Gemini gemini-flash-lite (1M ctx) | Deep context conciseness | Mistral Small → Groq 70B → Groq 8B → qwen3.6 |
| `extract` | Groq qwen/qwen3.6-27b | Code-native, precise | SambaNova 70B → Groq 70B → Mistral Codestral → Cerebras |
| `bm_native` | SEA-LION Qwen-v4-32B | Native BM/Malay | SEA-LION Llama-v3 → Gemma-v4 → Mistral Small |
| `coding` | **Mistral Codestral-2508** (256K ctx) | Code specialist | SambaNova 70B → Groq 70B → Groq 8B → OpenRouter |
| `observe` | Groq llama-3.1-8b-instant | Fastest for search context | Mistral Small → qwen3.6 |
| `draft_plan` | **Groq llama-3.3-70b** | Deep reasoning for planning | Cerebras gemma-4-31b → Groq qwen3.6 → Mistral Small |
| `epistemic` | Groq llama-3.3-70b-versatile | Deep reasoning | SambaNova 70B → Gemini flash |
| `json_mode` | **Mistral mistral-small-latest** | Best-in-class JSON mode | Groq qwen3.6 → Cerebras gemma |
| `gap_fill` | OpenRouter :free aggregator | Provider coverage gap-fill | — |
| `destructive` | (empty) | NEVER FLAME — governed cascade | — |

### How It Works

```
Request with task_class="classify"
  → Router reorders tiers: llama-3.3-70b moves to front
  → If it succeeds → return immediately
  → If it fails → try next in TASK_CLASS_CHAINS
  → If all task-specific fail → fall back to general RM0-TOOLS-FREELOOP pool
```

The fallback is implicit — `TASK_CLASS_CHAINS` only specifies the *preferred*
models. The complete RM0 pool is still available behind them. This ensures
**graceful degradation**: even if the perfect model for the task is down, a
less perfect model still serves the request.

### Caller Integration

Every `flame_client.py` must tag outgoing requests with `task_class`:

```python
# GEOX classify
payload = {"text": text, "task_class": "classify", ...}
# GEOX summarize  
payload = {"text": text, "task_class": "summarize", ...}
# GEOX contradiction
payload = {"text": prompt, "task_class": "extract", ...}
# arifOS search synthesis
payload = {"prompt": prompt, "task_class": "extract", ...}
```

### Moar — A-FORGE + Mistral Integrated

| Organ | Client File | Location | Functions | Task Classes |
|-------|-------------|----------|-----------|-------------|
| GEOX | `flame_client.py` | `geox_mcp/tools/` | `flame_summarize`, `flame_classify`, `flame_contradiction_analysis` | `summarize`, `classify`, `extract` |
| arifOS | `flame_client.py` | `arifosmcp/tools/` | `flame_synthesize_search` | `observe` |
| A-FORGE | `flameClient.ts` | `src/tools/` | `flameSynthesizeSearch` | `extract` |

## Speculative Execution Pattern (Arif-ratified 2026-07-25)

For A-FORGE tools, FLAME uses **Speculative Execution**: FLAME drafts, governed model audits.

```
FLAME (draft) → classify/extract/summarize  →  ADVISORY
Governed Model (audit) → DeepSeek/TokenRouter  →  SEAL-grade verdict
```

Safe because:
- **F1**: Draft never auto-executed (forge_plan requires arif_judge)
- **F2**: FLAME hallucination caught by governed verification
- **Cost**: RM0 draft, paid audit only (90/10 split)

### A-FORGE Task Map

| Tool | task_class | Primary | Rationale |
|------|-----------|---------|-----------|
| `forge_search` | `extract` | Groq Qwen3.6-27b | Code-native parsing |
| `forge_summarize` | `summarize` | Gemini flash-lite | 1M context |
| `forge_diagnose` | `classify` | Groq Llama-3.3-70b | Deep stack trace reasoning |
| `forge_plan` | `draft_plan` | Groq Llama-3.3-70b | F1 ADVISORY only |

### TypeScript Integration

```typescript
import { flameSynthesizeSearch } from "../../tools/flameClient.js";
const synthesis = await flameSynthesizeSearch(query, results, "brave");
```

All functions POST to `:18901/summarize` with `task_type`. Node 22+ built-in fetch.
8s AbortController timeout. Zero external deps.

## Design Principle

L3 routing is **additive** — it doesn't break existing functionality (F1).
Requests without `task_class` fall back to the default latency-based chain.
The task map is a **preference**, not a hard requirement.

## Governance Rule

FLAME touches: advisory, classification, extraction, summarization.
FLAME never touches: judging, sealing, sovereign data, human substrate.
When in doubt → governed cascade. FLAME is for throughput, not truth.

## 🧘 Eureka Zen — 5 Rules (Arif-ratified 2026-07-25)

| # | Rule | Maksud | Implementation |
|---|------|--------|---------------|
| 1 | **"FLAME is reflex, not cerebrum"** | Zero state, zero memory, zero planning. FLAME react → output → forget. | `flame_client.py` stateless — no session/context history. Every request is self-contained. |
| 2 | **"Know thy model, know thy task"** | Route by strength profile, bukan sekadar latency. | `TASK_CLASS_CHAINS` + model profiles in `flame_config.json`. Classify → Llama-3.3-70b. Summarize → Gemini 1M ctx. |
| 3 | **"Let telemetry drive, let human seal"** | FLAME recommend config changes from hit-rate data. You review and seal the change. | **L4 Kabarkan: IMPLEMENTED.** `flame_api_server.py` `_kabarkan_emit()` publishes NATS span on every FLAME call → `kabarkan.ingest.span.flame.*`. Kabarkan worker active, JetStream stream configured. `flame_state.json` tracks hits/misses/latency per model. |
| 4 | **"Dead nodes don't get probe budget"** | If a model is dead (18ms timeout, 403, connection refused), don't waste probe cycles on it. Kill until re-verified. | Ollama dropped. Cerebras auto-removed by watchdog. `active=False` models skipped in call loop. |
| 5 | **"Thin muscle principle"** | FLAME engine stays < 2000 lines. Intelligence lives in config/registry/telemetry, not in code. | `flame_router.py` at ~1761 lines. Task routing in `TASK_CLASS_CHAINS` dict. Fleet in `flame_config.json`. |

## Pitfalls

- **Doc-reality gap — surface classification can be WRONG**: 81-surface map is *aspirational*, not ground truth. Verified cases: "Paper Trading Morning/Zen" flagged 🔥 but 100% deterministic. A-FORGE `forge_diagnose/summarize/plan` listed as MCP tools but **don't exist as MCP surfaces** — they're concept references in the 81-map, not actual tools. **Always verify by grepping actual tool code** before classifying. Run `grep -rn 'openai\\|flame\\|free-llm\\|chat/completions\\|requests\\.post.*:18901' <tool_dir>` — if no matches, it's NO-LLM, not FLAME-PRIME. For A-FORGE specifically: `grep 'server.tool.*forge' src/interfaces/mcp/gatewayTools.ts` to see actual MCP surfaces.\n\n- **FLAME API returns 400 with valid content**: The `_send()` handler uses `200 if \"error\" not in result else 400`. Since all responses include `\"error\": \"\"`, every valid response gets HTTP 400. Client MUST parse body and check `result.get(\"ok\")` rather than relying on status code. Fixed in flame_api_server.py line 432: changed to `self._send(200, result)` unconditionally.\n\n- **`/summarize` and `/classify` endpoints don't support task_class**: They use `_run_flame([\"--mode\", \"summarize\"])` which goes through the CLI, bypassing `engine.call()`. The `/completions` endpoint uses `engine.call(prompt, task_class=...)` and does support task routing. Eventually port `/summarize`/`/classify` to use `engine.call()` directly.\n\n- **Ollama is DEAD (connection refused)**

- **Ollama is DEAD (connection refused)**: 18ms latency with fail status = not running. The qwen2.5-coder:3b model/container is not active on this VPS. Drop from active pool. Only re-add after `docker ps | grep ollama` or `ollama list` confirms runtime.

- **flame.service masked by default**: The unit was symlinked to `/dev/null`. After unmask, must `systemctl enable --now flame.service`. Check `systemctl is-enabled flame.service` after any systemd reinstall.

- **Agent cron jobs are NOT FLAME candidates**: Cron jobs that produce user-facing content (`daily-news-briefing`, `evening-digest`, `weekly-reflection`) use the governed cascade intentionally. Routing them through FLAME's weak free models reduces quality. Only wire FLAME for internal sub-task helpers (e.g., news summarization helper function), not the whole cron job model path.

- **Reasoning-model blind spot (gpt-oss-120b, zai-glm-4.7)**: These models spend `max_tokens` budget on `reasoning_content`, leaving `content=""`. FLAME sees empty content → marks ❌. Both work fine for real prompts. **Fix in flame_router.py `_call_model`**: check `reasoning_content` field — if content is empty but reasoning exists, count as success. Probe `max_tokens` also bumped 5→80.
- **Provider-aware rate-limit cooldown (`probe_all`)**: 500ms between all tiers isn't enough for same-provider bursts. SEA-LION 3 tiers fire consecutively → 401 rate limit. Gemini same pattern → 429. **Fix**: `probe_all` tracks `prev_provider`, sleeps 2s only between same-provider tiers.
- **GPT-OSS-120B (Groq + Cerebras)**: Content safety suppresses short "OK" probes. Works for real prompts. Shadow ref: SHADOW-GPTOSS-001/002.
- **Gemini Flash Lite**: 12s timeout on old probe (max_tokens=5). Fixed with 80 max_tokens. Shadow ref: SHADOW-GEM-002.
- **opencode-go models**: Endpoint issues in FLAME config — excluded from fleet until verified.
- **Sea-LION model names**: Must use HF format (`aisingapore/Qwen-SEA-LION-v4-32B-IT`), not short aliases (`qwen-v4-32b`).

- **L5 auto-demote is silent**: Models demoted after 3 consecutive fails are skipped in the call loop with a `logger.debug` message — no alert. The model stays inactive until re-probed (probe_all auto-reactivates on success). Check `flame_state.json` for `active: false` entries.\n
- **Cerebras credit expires Aug 20 2026**: $5 prepaid. **Watchdog active** — `/root/.hermes/scripts/cerebras-watchdog.sh` runs every 30 min via cron job `Cerebras Watchdog` (no_agent, silent when healthy). Delegates to `flame_cerebras_watchdog.py`. Tests both models (gemma-4-31b + gpt-oss-120b). Auto-demotes on 3x consecutive fail (`--demote` flag). Alerts to Home channel when degraded. Auto-removes from config on 3x consecutive fail.\\n
- **Mistral rate limits unknown**: Not yet load-tested. JSON mode (mistral-small-latest) works for single calls. If 429s appear, add backoff or demote.\n
- **SambaNova not load-tested**: Claims 1K tok/s. Verify actual throughput before routing high-volume classify to it.\n
- **SambaNova not load-tested**: Claims 1K tok/s. Verify actual throughput before routing high-volume classify to it. Key stored in vault.env as `SAMBANOVA_API_KEY` (added 2026-07-25 by sibling agent).\n\n- **Mistral key `5WCWowqnpKpSZWUYOSscefH2w4iLyQq1`**: Personal API key (arifbfazil@gmail.com). Free tier models: mistral-small-latest, open-mistral-nemo, ministral-8b-latest, codestral-2508. All 262K ctx except Nemo (131K). Codestral is code specialist.\n\n- **HuggingFace token** (`HF_TOKEN`): Stored in vault.env, used for 30K+ free inference models. Slow cold-start but infinite model variety. Good for specialized models FLAME can't reach otherwise.

## References

- `references/flame-integration-pattern.md` — Architectural rules + reference implementation for wiring MCP tools to FLAME (`flame_client.py` pattern, 4 enforcement rules, provenance envelope). Read this first before wiring any MCP tool.
- `references/2026-07-25-wiring-audit.md` — Session-specific wiring audit: coverage analysis, what's actually wired vs doc claims, fleet health gaps.
- `references/2026-07-25-l3-task-routing.md` — L3 Task-Routing implementation detail: task class chains, routing verification, integration guide for new task classes.
- `references/81-surface-flame-map.md` — Complete 81-entry classification: every MCP tool, CLI, script, cron job with FLAME eligibility. ⚠️ Aspirational — verify actual wiring with `grep`.
- `references/agent-model-map-alignment.md` — AGENT_MODEL_MAP.json registry update procedure
