# Live-Agent Integration Pattern — Production Reference

**Source:** `/root/HERMES/cognitive/integration.py` (2026-08-04)
**Status:** ✅ Production — 114 tests passing (98 inner engine + 16 adapter)
**Coverage:** CognitiveMemoryAdapter + CognitiveDriftMonitor + ReinforceHook + IDENTITY_LOCK

This file is the canonical pattern for wrapping the Phase 1 cognitive modules
(memory_decay + drift_monitor) for use inside a live LLM agent. The adapter
is additive — the inner engine is not modified.

---

## Why an adapter layer (decision rationale)

Hermes Agent has no single importable "ConversationLoop" class. The
conversation flow is distributed across:

| Surface | Path | Role |
|---|---|---|
| Telegram gateway loop | `/root/HERMES/gateway/` | Telegram inbound/outbound |
| Hooks | `/root/HERMES/hooks/constitutional-guard/` | Pre/post message gates |
| Cron jobs | `/root/HERMES/cron/` | Scheduled tasks |
| Plugins | `/root/HERMES/plugins/` | Model picker, seal queue |
| Memory store | `/root/HERMES/memories/` (markdown + JSON) | Persistent identity/user facts |
| CLI | `/root/HERMES/scripts/governed_memory.py` | Memory CRUD via shell |

Pushing cognitive logic INTO those surfaces is fragile (breaks on upgrade,
duplicates logic across surfaces). Instead, ship a thin adapter that all
surfaces `import`. No host-agent core file is modified.

---

## Public surface (what the adapter exposes)

```python
from cognitive.integration import (
    # Constants
    IDENTITY_LOCK,             # arif / syed / aliff / trauma → needles
    IDENTITY_CATEGORIES,       # frozenset({"identity", "trauma"})
    CATEGORY_DEFAULT_WEIGHTS,  # per-category 7-factor seeds
    DEFAULT_DRIFT_WARNING,     # 0.30 — spec-aligned
    DEFAULT_DRIFT_ALERT,       # 0.50 — spec-aligned
    # Adapters
    CognitiveMemoryAdapter,    # wraps MemoryDecayEngine
    CognitiveDriftMonitor,     # wraps DriftMonitor
    # Hooks
    ReinforceHook,             # type alias
    default_reinforce_hook,    # built-in
    # Snapshots
    MemoryState, DecayAwareResult,
    # Helpers
    classify_locked_category,  # content → "identity"/"trauma"/None
    # Re-exports
    DriftSignal, Receipt,
)
```

### CognitiveMemoryAdapter API

| Method | When called | What it does |
|---|---|---|
| `add_memory(memory_id, content, category=None, value_score=None, omega=None)` | Once at memory creation | Auto-classifies via `classify_locked_category` if `category=None`. Seeds value-score from `CATEGORY_DEFAULT_WEIGHTS`. Returns initial `MemoryState`. |
| `advance_turn()` | Once per incoming message (Telegram, cron, CLI, etc.) | Bumps `_turn` by 1, ticks every stored memory, emits one receipt summarising tier transitions. |
| `decay_aware_query()` | Before prompt-context build | Returns `DecayAwareResult` with `by_category`, `by_tier`, `demoted`, `promoted`. Caller feeds into context. |
| `reinforce(memory_id)` | When memory used in outgoing response | Fires `ReinforceHook`. Default hook resets clock for identity/trauma, bumps value-score for others. |
| `increase_reinforcement_interval(memory_id)` | Runtime η-tuning | Raises `value_score` by 0.05 (capped at 1.0). Effect: lower μ(Ω) → slower decay. |
| `decrease_reinforcement_interval(memory_id)` | Runtime η-tuning | Lowers `value_score` by 0.05 (floor 0.0). Effect: higher μ(Ω) → faster decay. |
| `get_memory_state(memory_id)` | Introspection | Returns full `MemoryState` snapshot (omega, value_score, mu, omega_eff, tier, recall_count, last_reinforced_turn, is_locked). |

### CognitiveDriftMonitor API

```python
mon = CognitiveDriftMonitor("deploy the application to production")
# (warning_threshold=0.30, alert_threshold=0.50 by default)

signal = mon.check_drift(user_input="...", agent_output="...")
# signal.drift_distance — cosine(user_input, agent_output) in [0, 2]
# signal.level — STABLE / DRIFT_WARNING / DRIFT_ALERT
# signal.recommendation — spec-aligned text

print(mon.recommendation(signal.level))
# STABLE        → "Conversation on track."
# DRIFT_WARNING → "Drift WARNING — suggest reconfirmation of intent."
# DRIFT_ALERT   → "Drift ALERT — suggest reroute to baseline."
```

### ReinforceHook contract

```python
ReinforceHook = Callable[[str, MemoryState, CognitiveMemoryAdapter], Optional[MemoryState]]
```

The hook receives the current state, can mutate the underlying record, and
returns the new state (or `None` to leave state untouched). Built-in
`default_reinforce_hook` is deterministic — same inputs → bit-identical
outputs. NO LLM calls.

---

## Identity lock — the clock-reset technique

### The problem (validated by Phase 1 simulation)

For the canonical decay model `Ω_eff = Ω · exp(-λ · Δn · μ)` with
`Ω=1.0, μ=0.10, λ=0.05`:

- Half-life at MTM-floor (Ω_eff=0.5): ~13.86 turns
- Ω_eff crosses 0.40 (MTM threshold): ~122 turns
- Ω_eff crosses 0.15 (LTM threshold): ~316 turns

So "high value-score + low μ" alone is **not enough** to keep identity
memories above MTM forever. They will always eventually decay unless the
decay clock itself is reset on reinforcement.

### The fix

In `default_reinforce_hook`, when the memory is in `IDENTITY_CATEGORIES`
(`identity` or `trauma`), reset `n_born` to the current turn:

```python
if ext.category in IDENTITY_CATEGORIES:
    rec.n_born = adapter._turn    # ← reset decay clock
    ext._eta_floor = MU_FLOOR
```

This makes `Δn → 0` immediately after each recall, so
`Ω_eff → Ω · exp(0) = Ω = 1.0`. Combined with low μ (slow decay between
recalls), any cadence ≥ once per ~40 turns keeps these memories pinned
above MTM indefinitely.

### Non-locked memories (task, routine)

Do NOT reset the clock — task/routine memories should fade naturally.
Instead, bump `value_score` by 0.01 per recall (capped at 0.90). This
lowers μ(Ω) and slows decay without resetting the clock, so reinforced
memories decay slower than unreinforced ones but still reach ARCHIVE
eventually.

### Why category matters

| Category | Clock reset on reinforce? | Value-score bump? | Max omega? |
|---|---|---|---|
| `identity` | YES | NO | 1.0 |
| `trauma` | YES | NO | 1.0 |
| `task` | NO | +0.01 (cap 0.90) | 1.0 |
| `routine` | NO | +0.01 (cap 0.90) | 0.85 (capped to allow fast decay) |

The category-seeded `eta_floor` (in `CognitiveMemoryAdapter._CATEGORY_ETA_FLOOR`)
controls the per-record inertia floor: `identity=0.10, trauma=0.05,
task=MU_FLOOR (0.10), routine=0.30`. Lower floor → lower μ → slower decay.

---

## Spec-aligned vs engine-calibrated thresholds

The inner `DriftMonitor` uses calibrated thresholds (0.55/0.75) tuned for
short sentences with `all-MiniLM-L6-v2`. The integration layer uses the
spec's 0.30/0.50 — these are separate contracts and both must be honoured:

```python
# Integration-layer default (spec contract)
DEFAULT_DRIFT_WARNING = 0.30
DEFAULT_DRIFT_ALERT = 0.50

# Inner-engine calibration (Phase 1 simulation finding)
# (lives in cognitive.drift_monitor.monitor as WARNING_THRESHOLD/ALERT_THRESHOLD)
```

When constructing the wrapped monitor, pass the spec values explicitly:

```python
self._monitor = DriftMonitor(
    baseline_text=baseline,
    warning_threshold=DEFAULT_DRIFT_WARNING,   # 0.30, not the engine's 0.55
    alert_threshold=DEFAULT_DRIFT_ALERT,       # 0.50, not the engine's 0.75
)
```

For transient "user_input vs agent_output" checks (separate from the
long-running conversation monitor), instantiate a throw-away monitor with
the spec thresholds rather than mutating the live one — that way the
live monitor's calibration history is preserved.

---

## Auto-classify via IDENTITY_LOCK content heuristic

The hardcoded registry:

```python
IDENTITY_LOCK = {
    "arif":   ["Arif bin Muhammad Fazil", "age 36", "PETRONAS engineer",
               "federation architect", "Arizona geologist"],
    "syed":   ["Syed / Abang Sado", "@rico_ricaldo_33", "ISFJ",
               "XAUUSD trader", "Hypnos sleep aid"],
    "aliff":  ["Muhammad Aliff Al Husna", "PETRONAS KLCC",
               "Arizona geologist", "Lenggeng NS"],
    "trauma": ["DERITA/", "F9", "F10", "888_HOLD"],
}
```

Matching is case-insensitive substring search across the union of all
needles. The classifier picks the FIRST lock key whose needles hit, so
put more specific keys (e.g. "trauma") earlier if order matters.

`add_memory(content="...", category=None)` calls this and auto-tags
identity/trauma content. `category=` kwarg lets the caller override
(e.g. caller can force `category="task"` even if content mentions Arif).

---

## Test structure (16 tests in `test_integration.py`)

### The 7 required tests (per common spec)

1. `test_decay_aware_query_prioritizes_identity` — identity ranked above routine after 30 turns
2. `test_decay_aware_query_demotes_routine` — routine demoted to LTM/ARCHIVE after 50 turns
3. `test_reinforce_hook_boosts_inertia` — reinforced omega_eff > unreinforced omega_eff
4. `test_drift_monitor_warning_threshold` — drift > 0.30 produces DRIFT_WARNING
5. `test_drift_monitor_alert_threshold` — drift > 0.50 produces DRIFT_ALERT
6. `test_identity_memory_never_decays` — identity stays STM/MTM after 100 turns (recall every 5)
7. `test_trauma_memory_locked` — trauma auto-classified, stays STM/MTM, value_score > 0.50

### The 9 additional coverage tests

8. `test_classify_locked_category` — heuristic covers all 4 keys, returns None for non-locked
9. `test_increase_decrease_reinforcement_interval` — runtime tuning works
10. `test_get_memory_state` — snapshot dataclass fields populated
11. `test_adapter_creates_receipts` — every operation emits a receipt, IDs unique
12. `test_drift_monitor_creates_receipts` — drift receipts emitted
13. `test_identity_lock_registry_keys` — locks the 4-key registry shape
14. `test_unknown_memory_raises_keyerror` — error contract on reinforce/get_state
15. `test_auto_classify_from_content` — auto-detect identity/trauma, default to "task"
16. `test_brief_smoke_test` — exact reproduction of the task-brief smoke test

### Smoke test pattern (locked-in via `test_brief_smoke_test`)

```python
adapter = CognitiveMemoryAdapter()
adapter.add_memory("arif_age", "Arif is 36", category="identity")
adapter.add_memory("weather", "Sunny today", category="routine")
for turn in range(50):
    adapter.advance_turn()
    adapter.reinforce("arif_age")  # recalled each turn
results = adapter.decay_aware_query()
assert "arif_age" in [m.memory_id for m in results.by_category["identity"]]
assert "weather"  in [m.memory_id for m in results.by_category["routine"]]
```

Expected output (from `/root/HERMES/cognitive/INTEGRATION_REPORT.md`):

```
Categories: ['identity', 'routine']
arif_age present in identity? True
weather present in routine? True
arif_age: tier=STM, omega_eff=1.0000, locked=True   (clock-reset on last reinforce)
weather:  tier=LTM, omega_eff=0.1071, locked=False  (demoted as expected)
```

---

## How to wire from a host-agent surface

### Telegram gateway (Python)

```python
# In /root/HERMES/gateway/telegram_loop.py (or similar)
from cognitive.integration import CognitiveMemoryAdapter, CognitiveDriftMonitor

adapter = CognitiveMemoryAdapter()
drift_monitor = CognitiveDriftMonitor("user's stated goal at session start")

async def on_message(user_input: str, agent_output: str):
    adapter.advance_turn()
    # ... build prompt context from adapter.decay_aware_query() ...
    signal = drift_monitor.check_drift(user_input, agent_output)
    if signal.level == "DRIFT_ALERT":
        log.warning(drift_monitor.recommendation(signal.level))
        # suggest reroute
    elif signal.level == "DRIFT_WARNING":
        log.info(drift_monitor.recommendation(signal.level))
        # suggest reconfirm
    # ... generate and send response ...
    # After response: adapter.reinforce(memory_id) for any memory the
    # response cited.
```

### Cron / scheduled audit

```python
# In /root/HERMES/cron/audit_conversation_quality.py
from cognitive.integration import CognitiveDriftMonitor
mon = CognitiveDriftMonitor("expected baseline intent")
for turn in conversation_log:
    signal = mon.check_drift(turn.user_input, turn.agent_output)
    # Append to quality report, emit receipt to forge_cool_drift if ALERT.
```

### CLI (no Python loop)

```bash
# One-shot decay report — no need to import the adapter in bash.
# Just invoke a small Python wrapper script that uses the adapter.
python -c "
from cognitive.integration import CognitiveMemoryAdapter
a = CognitiveMemoryAdapter()
a.add_memory('x', 'Arif PETRONAS')
for _ in range(20):
    a.advance_turn()
    a.reinforce('x')
print(a.get_memory_state('x'))
"
```

---

## Constraint compliance checklist

When shipping a new integration layer (or auditing an existing one):

- [ ] Zero LLM calls in the adapter module (grep for `openai`, `anthropic`, `requests.post`, etc.)
- [ ] All operations deterministic — same inputs → bit-identical outputs
- [ ] Zero host-agent core files modified (the adapter is purely additive)
- [ ] All existing inner-engine tests still pass
- [ ] All new adapter tests pass
- [ ] Receipts emitted for every operation (F1 AMANAH + F7 confidence cap)
- [ ] IDENTITY_LOCK is hardcoded (no runtime config, no DB lookup)
- [ ] Spec-aligned thresholds passed through explicitly (don't silently inherit engine defaults)

---

## Phase 2 candidates

1. **Causal Tagger integration** — extend `ReinforceHook` to consume
   causal tags and bias value-scoring.
2. **Narrative/Emotion axes** — add `narrative` and `emotion` to
   `CATEGORY_DEFAULT_WEIGHTS` and `IDENTITY_LOCK`.
3. **MCP resource exposure** — expose adapter state via
   `cognitive://memory/state` MCP resource so gateway/cockpit can read
   tier counts without invoking the engine directly.
4. **Honcho dialectic memory interop** — when `/root/HERMES/.honcho/`
   is wired, route identity/trauma memories to Honcho's permanent store
   and treat the cognitive adapter as a tier-1 cache.