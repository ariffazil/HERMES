---
name: cognitive-substrate-engineering
description: Build, validate, and integrate cognitive substrate modules (memory decay, causal tagging, drift monitoring, narrative construction) into LLM-based agents. Use when the agent needs to improve beyond flat RAG/lookup — i.e., when old data needs to fade, when "because X" claims must carry evidence tags, or when long-conversation drift detection is required.
metadata:
  hermes:
    tags: [agent-cognition, memory-systems, epistemic-governance, F2-TRUTH, simulation-validation, phased-delivery]
---

# Cognitive Substrate Engineering

Class of work: extending an LLM agent from stateless or flat-RAG behavior to one with structured cognition across Temporal, Causal, Metacognitive, Narrative, and Emotional axes.

## Trigger Conditions

Use this skill when ANY of the following recurs in a session:
- The agent must know old data is stale (not just retrieve it)
- The agent makes "because X" claims without evidence backing
- The agent drifts from user intent during long conversations
- The agent needs to track story arcs across sessions
- Memory needs to fade rather than be retained flat
- A blueprint or paper references "Memory Decay", "Causal Tagger", "Drift Monitor", or similar cognitive architectures

## The Four Validated Cognitive Axes (Phase 1 scope)

| Axis | Function | Implementation pattern |
|---|---|---|
| **Temporal** | Memory decay with freshness | Interaction-count (Δn) decay, NOT wall-clock. Ebbinghaus curve + multi-factor V(m) + score-dependent inertia μ(Ω). |
| **Causal** | Claim evidence-tagging | Regex-syntax approach. Do NOT use sentence-transformers for causal syntax detection (regressed 78% → 57% in Phase 1 simulation). |
| **Metacognitive** | Drift detection | Embedding cosine (sentence-transformers primary, TF-IDF fallback) + threshold tier (0.3 warning, 0.5 alert). |
| **Narrative + Emotional** | Episode tracking + affect modeling | Out of scope for Phase 1; requires episodic graph + S-Vector attention modification (Phase 2). |

## Build Order (Phase-Gated)

1. **Shared foundation** — `config.py` (constants), `receipt.py` (evidence emission)
2. **Memory Decay** — most impactful, most complex
3. **Causal Tagger** — lightweight regex
4. **Drift Monitor** — fallback-friendly
5. **Unit tests** — pytest must pass before moving on
6. **Simulation tests** — ground truth + synthetic data BEFORE integration
7. **Tune** — fix failure modes from simulation honest reporting
8. **Integrate** — only after tests + simulation show production-ready behavior

Never skip the simulation step. Code that passes unit tests can still fail at runtime on real conversation patterns.

## Live-Agent Integration Layer (Step 9 — After Step 8)

Once the cognitive modules are production-ready in isolation, wrap them in an **integration adapter** that the host agent imports. This layer is the public surface; the inner engine stays untouched.

### Why an adapter layer (don't push into core)

Most agent runtimes (Hermes, Claude Code, OpenCode) do NOT have a single importable "ConversationLoop" class. The conversation flow is distributed across gateway, hooks, cron, plugins, and a markdown/JSON memory directory. Pushing cognitive logic INTO those surfaces is fragile and breaks on upgrade.

Better: ship a thin **adapter module** (`cognitive/integration.py`) that wraps the engine + monitor and exposes a stable Python surface. Hooks, gateway, cron, and CLI all `import` it. No host-agent core file is modified.

### Required adapter surface

```
cognitive/integration.py:
  CognitiveMemoryAdapter
    add_memory(memory_id, content, category=None, value_score=None, omega=None)
    advance_turn()                          # call once per incoming message
    decay_aware_query() -> DecayAwareResult # feed into prompt context
    reinforce(memory_id)                    # call when memory used in response
    increase_reinforcement_interval(memory_id)  # runtime η-tuning, no restart
    decrease_reinforcement_interval(memory_id)
    get_memory_state(memory_id) -> MemoryState
  CognitiveDriftMonitor
    check_drift(user_input, agent_output) -> DriftSignal
    recommendation(level) -> str            # "suggest reconfirm" / "suggest reroute"
  ReinforceHook = Callable[[str, MemoryState, Adapter], Optional[MemoryState]]
  IDENTITY_LOCK                              # hardcoded locked-keyword registry
  Receipt emission on every operation       # F1 AMANAH + F7 cap
```

### Spec-aligned vs engine-calibrated thresholds — split cleanly

The inner `DriftMonitor` may use calibrated thresholds (e.g. 0.55/0.75 for short sentences with `all-MiniLM-L6-v2`). The integration layer owns the spec contract (e.g. 0.30/0.50 from the user-facing requirements doc). Pass the spec values through explicitly:

```python
self._monitor = DriftMonitor(
    baseline_text=baseline,
    warning_threshold=DEFAULT_DRIFT_WARNING,   # 0.30, the spec value
    alert_threshold=DEFAULT_DRIFT_ALERT,       # 0.50, the spec value
)
```

If the integration needs a transient "user_input vs agent_output" check (separate from the long-running conversation monitor), instantiate a throw-away monitor with the spec thresholds rather than mutating the live one.

### Identity lock — clock-reset on reinforce (key technique)

Plain Ebbinghaus `Ω_eff = Ω · exp(-λ · Δn · μ)` will eventually decay any memory below MTM no matter how high `Ω` is or how low `μ` is — for `Ω=1.0, μ=0.10, λ=0.05`, the MTM-floor half-life is ~13.86 turns, and Ω crosses 0.40 around turn 122. So "high value-score + low μ" alone is **not enough** to keep identity memories above MTM forever.

The fix lives in `default_reinforce_hook`: on every reinforce call for an `identity` or `trauma` memory, reset `n_born` to the current turn so `Δn → 0` and `Ω_eff` jumps back to `Ω`. Combined with low μ, this makes any reasonable recall cadence (≥ once per ~40 turns) sufficient to keep these memories pinned above MTM indefinitely.

```python
def default_reinforce_hook(memory_id, state, adapter):
    ext = adapter._records[memory_id]
    rec = ext.record
    new_recall_count = ext.recall_count + 1
    new_omega = min(1.0, rec.omega * (1 + log1p(new_recall_count)) / (1 + log1p(ext.recall_count)))
    if ext.category in IDENTITY_CATEGORIES:
        rec.n_born = adapter._turn    # ← THE FIX: reset decay clock
        ext._eta_floor = MU_FLOOR
    else:
        # Non-locked: also bump value_score slightly (0.01/recall, cap 0.90).
        # This lowers μ(Ω) and slows decay without resetting the clock —
        # routine/task memories should still fade naturally.
        if ext.category == "routine" and new_omega > 0.85:
            new_omega = 0.85
        rec.value_score = min(0.90, rec.value_score + 0.01)
    rec.omega = new_omega
    ext.recall_count = new_recall_count
    ext.last_reinforced_turn = adapter._turn
    adapter._engine.tick(memory_id, adapter._turn)
    return adapter.get_memory_state(memory_id)
```

For non-locked memories, do NOT reset the clock — task/routine memories should fade. Just bump value_score a little so reinforced memories slow down.

### Auto-classify via IDENTITY_LOCK content heuristic

The integration layer can ship a hardcoded lock registry and a content-substring classifier so callers don't have to remember to tag identity memories manually:

```python
IDENTITY_LOCK = {
    "arif":   ["Arif bin Muhammad Fazil", "age 36", "PETRONAS engineer",
               "federation architect", "Arizona geologist"],
    "syed":   ["Syed / Abang Sado", "@rico_ricaldo_33", "ISFJ",
               "XAUUSD trader", "Hypnos sleep aid"],
    "trauma": ["DERITA/", "F9", "F10", "888_HOLD"],
}

def classify_locked_category(content: str) -> Optional[str]:
    lc = content.lower()
    for key, needles in IDENTITY_LOCK.items():
        for needle in needles:
            if needle.lower() in lc:
                return "trauma" if key == "trauma" else "identity"
    return None
```

Adapter `add_memory(content="...", category=None)` calls this and auto-tags identity/trauma content. `category=` kwarg lets the caller override.

### Integration-layer test discipline

The adapter needs its own test file separate from the inner-engine tests:

- **7 required tests** (per common spec pattern): identity prioritization, routine demotion, reinforce boosts inertia, drift WARNING threshold, drift ALERT threshold, identity never decays, trauma locked.
- **+9 additional coverage**: classify heuristic, runtime tuning, snapshot dataclass fields, receipt emission per operation, registry keys stable, KeyError on unknown memory_id, auto-classify from content, exact brief smoke test.
- **Smoke test**: replicate the exact scenario from the task brief as a separate test (`test_brief_smoke_test`) so the spec contract is locked in.

Constraint compliance must be asserted:
- ✅ Zero LLM calls (no `import openai`, no `requests.post(...)`, etc.)
- ✅ All operations deterministic (same inputs → same outputs)
- ✅ Zero host-agent core files modified
- ✅ All existing engine tests still pass

See `references/live-integration-pattern.md` for the full adapter implementation from `/root/HERMES/cognitive/integration.py` (Hermes production, 2026-08-04, 114 tests passing: 98 inner + 16 adapter).

## Simulation Validation Pattern (Non-Negotiable)

Before integration to live system:
- Generate 100+ ground-truth examples per claim type with known correct answer
- Test on synthetic data with KNOWN outcomes (not projected/hardcoded results)
- Per memory type, define expected final tier (identity → STM/MTM, routine → ARCHIVE)
- Per causal claim, define ground-truth evidence type
- Per drift scenario, define expected detection behavior

If simulation shows regression (e.g., 78% → 57% accuracy after adding a layer), REVERT that layer. Honest `NEEDS TUNING` > optimistic `PASS`.

Templates: see `templates/simulation_harness_template.py` for the 3-phase harness structure.

## Critical Pitfalls (Validated by Failed Attempts)

1. **Wall-clock vs Interaction-count decay.** Wall-clock punishes users who take breaks (1 month away = all memory gone). Interaction-count is deterministic across machines and session pauses. Alexander Jul 2026 TDS proved byte-identical cross-machine determinism.

2. **λ tuning alone can't fix sparse reinforcement.** When reinforcement interval > decay half-life, memories still decay. Fix by boosting inertia `μ(Ω) = 1 - η·Ω` or boosting `Ω_base` on recall — NOT by reducing global `λ` (which corrupts routine decay).

3. **Sentence-transformers HURT causal syntax detection.** Semantic similarity is not causal structure. The Phase 1 simulation showed regression from 78.3% → 57.5% accuracy after adding semantic embeddings. Keep causal detection regex-based; reserve embeddings for semantic drift detection.

4. **TF-IDF produces high baseline cosine for non-identical but related sentences.** In the Phase 1 simulation, ON_TOPIC scenario produced 9/10 false ALERTs because TF-IDF measures lexical overlap, not semantic similarity. Fix: use sentence-transformers primary, TF-IDF only as fallback with raised thresholds (0.85/0.95 instead of 0.3/0.5).

5. **Forgetting curve alone is not enough.** Add logarithmic reinforcement `S_new = S_old × (1 + ln(1 + recall_count))` (Alexander Jul 2026) on recall — recall_count=0 gives no boost, high recall_count gives meaningful gain.

6. **Honest reporting > nice-looking PASS.** If results are `NEEDS TUNING`, say `NEEDS TUNING`. Hardcoded PASS in templates is fabrication; user will catch it and reject the work.

## Configuration Defaults (Phase 1 Validated)

```
Ω₀ = 0.03         # base decay rate
λ = 0.05          # half-life ~30 turns at this value
η = 0.50          # inertia strength (μ = 1 - η·Ω)
Confidence cap = 0.90   # F7 HUMILITY

Memory tiers:
  STM (32-bit): Ω ≥ 0.70
  MTM  (8-bit): 0.40 ≤ Ω < 0.70
  LTM  (4-bit): 0.15 ≤ Ω < 0.40
  ARCHIVE (2-bit): Ω < 0.15

Drift thresholds:
  STABLE: drift < 0.30
  WARNING: 0.30 ≤ drift < 0.50
  ALERT: drift ≥ 0.50
```

Reasoned archive of what was tried and why each value was chosen lives at `references/config-tuner-log.md`.

## Evidence Emission (Receipt Pattern)

Every operation emits a JSON receipt with:
- `timestamp` (ISO 8601)
- `evidence_type` label: `OBS / DER / INT / SPEC / UNKNOWN`
- `confidence` value (capped at 0.90 per F7)
- `verdict`: `SEAL / PARTIAL / SABAR / HOLD / UNKNOWN`

Receipts are evidence, NOT verdicts. The judge system (888 / `arif_judge`) issues final verdict. Receipts are the substrate; judge is the arbiter.

## arifOS Integration Hooks

For the federation that wraps this work:
- **F1 AMANAH** lock for irreversible memory operations (mutations to LTM)
- **888 JUDGE** for high-stakes causal claims before surfacing
- **forge_receipt_draft** for receipt emission on every decay/tagging/drift operation
- **forge_cool_drift** for drift signals feeding into the cool/receipt ledger
- **F7 confidence cap** at 0.90 enforced in the receipt emitter

## User Communication Discipline (Arif-specific)

- **"Cakap macam manusia"** — user explicitly rejected over-structured, robotic, RFC-style responses mid-session (2026-08-04: "aku nak Hermes aku cakap bahasa manusia wei"). Default to casual BM Penang, direct, no excessive tables. Tables only when comparison genuinely helps. Not every answer needs a 12-row table. When user asks simple question, give simple answer. Deep only when requested.
- Diagnosis tepat → auto-execute tanpa semakan (when user gives clear instruction with confirmed diagnosis, proceed — don't ask again)
- Phased delivery: P1 (highest impact, smallest scope) → P2 → P3; never batch all phases
- Honest numbers > nice-looking PASS; user validates and detects fabrication
- 110 passing unit tests with no real-world simulation is NOT a green light

### Anti-pattern: Overclaiming module readiness

**Proven 2026-08-04:** Agent claimed "98 tests green" when actual count was 62 (28+20+14). Agent claimed "Drift Monitor production-ready" when Phase C had 5/14 tests failing on threshold mismatch. Agent claimed "Memory Decay wired to live" when code existed but was NOT wired to live cron — draft only.

**Root cause:** Conflating different test suites (unit tests vs simulation tests vs integration tests) into one count. Reporting PASS status from unit tests while simulation showed NEEDS TUNING. Using "wired" to mean "code exists" instead of "hooked into production loop."

**Rule:** When reporting module status, ALWAYS separate three categories:
1. **Unit tests:** N/M passing (e.g., "28/28 unit tests pass")
2. **Simulation tests:** verdict from SIMULATION_REPORT.md (e.g., "Phase A: PARTIAL — REINFORCED 0%, Phase C: PASS")
3. **Integration status:** one of `standalone` (code exists, not wired) / `draft` (incomplete) / `wired` (hooked into live loop) / `production` (running in live conversations)

**Never aggregate across these categories.** A module that passes 100% unit tests but fails 35% simulation tests is NOT production-ready. A module with code on disk but no cron/hook wiring is NOT "integrated."

## Reference Files

- `references/config-tuner-log.md` — what values were tried, why each was chosen, what failed
- `references/eight-axis-atlas.md` — full 12-axis intelligence map for context beyond Phase 1
- `references/live-integration-pattern.md` — canonical adapter pattern for wrapping Phase 1 modules in a live LLM agent (clock-reset on reinforce, spec-aligned vs engine-calibrated thresholds, IDENTITY_LOCK auto-classify, 16-test discipline). Source: `/root/HERMES/cognitive/integration.py` (2026-08-04, 114 tests).
- `templates/simulation_harness_template.py` — 3-phase harness skeleton (200-turn memory, 100-sentence causal GT, 4-scenario drift)
- `templates/receipt_template.json` — canonical receipt schema

## Provenance

Validated 2026-08-04 in /root/HERMES/cognitive/ — 19 files, 4,757 LOC, 98 unit tests passing. Phase 1 complete for Drift Monitor + Memory Decay (identity/trauma 100% retention). Causal Tagger deferred to Phase 2 due to sentence-transformers regression.

**Step 9 (live integration) validated 2026-08-04:** `cognitive/integration.py` ships the canonical adapter pattern. 16 new tests, 114 total (98 inner + 16 adapter) all green. Hermes gateway/cron/hooks import the adapter; zero host-agent core files modified. See `references/live-integration-pattern.md` for the full pattern.
