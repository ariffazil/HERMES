# Canonical Model Picker — Fail-Closed Gate Pattern (2026-07-23)

After probing all models and assigning tiers, the results live in one file:
`~/.hermes/model-picker.yaml` — the single source of truth for model routing.

## Why one file

Before: model strings scattered across config.yaml, cron jobs, AGENTS.md, skills.
After: ONE YAML file. All surfaces read from it. No model string hardcoded anywhere else.

## File shape

```yaml
probed_at: "2026-07-23T18:30:00Z"
probe_summary: {zen_total: 57, zen_alive: 19, go_total: 23, go_alive: 20}

tiers:
  bulk:    {use: "cron jobs", provider: opencode-go,  model: deepseek-v4-flash, cost: "flat $10/mo"}
  default: {use: "Telegram",  provider: opencode-zen, model: deepseek-v4-flash, cost: "$0.14/M"}
  heavy:   {use: "codegen",   provider: opencode-zen, model: deepseek-v4-pro,  cost: "$1.74/M", fallback: minimax-m3}
  apex:    {use: "judgment",  provider: opencode-zen, model: grok-4.5,         cost: "$2.00/M", fallback: glm-5.2}

zen_alive:
  deepseek-v4-pro:  {alive: true, http_status: 200, endpoint: chat_completions}
  # ... all probed-alive models with HTTP codes

zen_dead:
  - {model: claude-sonnet-4-6, status: 401, reason: "premium billing required"}
  # ... all dead models with status codes + reasons

go_alive: { ... }
go_dead: [ ... ]
```

## Fail-closed gate — two injection points

The gate is enforced at TWO points in Hermes source. Both import the validator via `importlib` (filesystem path, not package) so they survive Hermes upgrades.

### 1. `switch_model()` in `hermes_cli/model_switch.py`

Right before the final `return ModelSwitchResult(success=True, ...)`, validate that the resolved model is in the alive list:

```python
# --- Picker gate (fail-closed) ---
if target_provider in {"opencode-zen", "opencode-go"}:
    try:
        import importlib.util, os as _os
        _spec = importlib.util.spec_from_file_location(
            "model_picker_gate",
            _os.path.expanduser("~/.hermes/plugins/model_picker_gate.py")
        )
        if _spec and _spec.loader:
            _gate = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_gate)
            if not _gate.is_model_alive(target_provider, new_model):
                return ModelSwitchResult(
                    success=False,
                    error_message=(
                        f"Model '{new_model}' is not in the probed-alive list "
                        f"for {target_provider}. See ~/.hermes/model-picker.yaml"
                    ),
                )
    except Exception:
        pass  # gate unavailable — allow (graceful degrade)
```

### 2. `list_picker_providers()` in `hermes_cli/model_switch.py`

Restrict the picker to tier models only when showing opencode providers:

```python
# Restrict opencode providers to probed-alive tiers from model-picker.yaml
if slug in ("opencode-zen", "opencode-go"):
    try:
        # ... load gate module ...
        tier_models = _gate.get_tier_models()
        tier_ids = [t["model"] for t in tier_models if t["provider"] == slug]
        if tier_ids:
            p = dict(p)
            p["models"] = tier_ids
            p["total_models"] = len(tier_ids)
    except Exception:
        pass
```

## Validator module

`~/.hermes/plugins/model_picker_gate.py` — reads `model-picker.yaml` with filesystem-mtime cache.

Exports:
- `is_model_alive(provider, model)` → bool
- `get_tier_models()` → list of {tier, provider, model, use, cost, fallback}
- `get_alive_models()` → {provider: [model_ids]}
- `get_tier_for_provider_model(provider, model)` → tier name or None

## Weekly re-probe cron

- `cron_id`: c9f94193b521
- Schedule: `0 2 * * 0` (Sunday 02:00 MYT)
- Script: `~/.hermes/scripts/model_reprobe.py` (no_agent=True)
- Deliver: AAA group (-1003753855708)

**Contract:**
- Produces `model-picker.candidate.yaml` + `model-picker.diff.txt`
- NEVER overwrites `model-picker.yaml`
- Fail-closed: probe errors → VOID candidate, canonical untouched
- ≤3 liveness changes → auto-safe, >3 → manual review required
- Tier reassignments: NEVER auto (F13)

## Anti-mahal rule

DEFAULT tier = cheapest adequate model, not most capable.
`deepseek-v4-flash` ($0.14/M) is 12x cheaper than `deepseek-v4-pro` ($1.74/M).
Reserve pro for heavy tier (codegen, audits).
