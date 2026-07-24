# v2 Contract Upgrade Pattern — Federation Organ Tools

> Pattern for upgrading a Python module from dict-based returns to typed
> dataclass contracts while preserving backward compatibility. Used in the
> WELL dark geometry detector v1→v2 upgrade (2026-07-12).

## When to use

- An organ tool returns raw dicts and needs typed output contracts
- The detection/computation logic is sound but the interface is untyped
- Backward compatibility is required (existing MCP tools call the module)
- Config is hardcoded and needs externalization

## The pattern (7 steps)

### 1. Define typed contracts (keep engine, upgrade interface)

```python
from dataclasses import dataclass, field
from enum import Enum

class ModeName(str, Enum):
    MODE_A = "MODE_A"
    MODE_B = "MODE_B"

@dataclass
class Signal:
    type: str
    pattern: str
    evidence: str
    line: int = 0

@dataclass
class ModeResult:
    mode: ModeName
    signals: list[Signal]
    confidence: float
    status: str
    questions: list[str]
    counterevidence: list[str]           # NEW: what argues against this
    alternative_explanations: list[str]  # NEW: benign interpretations

@dataclass
class AnalysisOutput:
    detected_modes: list[ModeResult]
    dominant_mode: ModeName | None
    overall_status: str
    prohibited_conclusions: list[str]    # always populated
    authority_effect: str = "NONE"       # never automatic
    epistemic_status: str = "INSUFFICIENT_EVIDENCE"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict. Handle enums manually."""
        def _serialize(obj):
            if isinstance(obj, Enum): return obj.value
            if isinstance(obj, list): return [_serialize(i) for i in obj]
            if isinstance(obj, dict): return {k: _serialize(v) for k, v in obj.items()}
            if hasattr(obj, '__dataclass_fields__'):
                return {k: _serialize(v) for k, v in asdict(obj).items()}
            return obj
        return _serialize(self)
```

### 2. Update detect_* methods to return typed results

```python
def detect_mode_a(self, text: str) -> ModeResult:  # was dict
    signals = _find_signals(text, _PATS, "signal_type")
    conf = _confidence_from_signals(signals, len(signals))
    status = _status_from_confidence(conf)
    return ModeResult(
        mode=ModeName.MODE_A,
        signals=signals,
        confidence=round(conf, 3),
        status=status,
        questions=PROMPTS if status != "CLEAR" else [],
        counterevidence=COUNTEREVIDENCE[ModeName.MODE_A],
        alternative_explanations=ALTERNATIVES[ModeName.MODE_A],
    )
```

### 3. Add counterevidence and alternatives per mode

```python
COUNTEREVIDENCE = {
    ModeName.MODE_A: [
        "Speaker may have domain expertise",
        "Urgent situation may justify direct language",
    ],
}

ALTERNATIVES = {
    ModeName.MODE_A: [
        "Cultural communication style",
        "Second-language patterns",
        "Executive communication preference",
    ],
}
```

### 4. Add prohibited conclusions (always populated)

```python
PROHIBITED_CONCLUSIONS = [
    "hidden_niat",
    "evil_identity",
    "permanent_trait",
    "psychiatric_diagnosis",
]
```

### 5. Preserve backward compatibility

```python
def analyze_with_context(self, text, context=None) -> dict[str, Any]:
    """Backward-compatible wrapper — returns dict."""
    result = self.analyze(text, context)
    return result.to_dict()  # to_dict(), not asdict()
```

### 6. Externalize config to YAML with graceful fallback

```python
def _load_yaml_config(filename: str) -> dict | None:
    config_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception:
        return None

def _load_lexicon(key: str, fallback: list[str]) -> list[str]:
    config = _load_yaml_config("rules.yaml")
    if config and "lexicons" in config and key in config["lexicons"]:
        return config["lexicons"][key]
    return fallback  # hardcoded defaults always work
```

### 7. Write comprehensive tests (pytest style)

Test categories:
- **Mode positive/negative**: each mode with triggering and non-triggering text
- **Benign counterexamples**: code review, legal prose, executive directives, L2 speakers, trauma
- **State not trait**: output never contains permanent identity labels
- **No hidden intent**: prohibited conclusions always present, no intent declarations
- **Output contract**: all required fields present, enum values valid, authority_effect = "NONE"
- **Backward compat**: `analyze_with_context` returns dict, aliases work
- **Edge cases**: empty input, whitespace, single word

## Pitfalls

1. **Don't use `asdict()` for the top-level return** — enum fields serialize as
   enum objects, not strings. Write a custom `to_dict()` that handles enums.

2. **Don't break the CLI** — update `pretty_print()` to handle the new field
   names (`detected_modes` not `mode_results`). Update `main()` to call
   `result.to_dict()` before passing to `pretty_print()`.

3. **YAML fallback must be seamless** — if YAML file is missing, hardcoded
   defaults must produce identical behavior. Test with and without YAML.

4. **Backward-compatible method signatures** — `analyze_with_context()` must
   still accept `dict[str, Any] | None` as context and return `dict[str, Any]`.

5. **Counterevidence/alternatives per mode, not global** — each mode gets its
   own counterevidence and alternative explanations. Don't use a single global list.

## Files produced in WELL example

| File | Purpose |
|------|---------|
| `gate/darkgeometrydetect.py` | v2 detector with typed contracts |
| `gate/dark_geometry_rules.yaml` | Lexicons, patterns, thresholds |
| `gate/dark_geometry_reflections.yaml` | Reflection prompts per mode |
| `gate/adapters/well_adapter.py` | Domain-specific event adapter |
| `tests/test_darkgeometrydetect.py` | 29 pytest tests |

## Cross-references

- `mcp-tool-upgrade-lifecycle` (archived) — sibling skill for changing tools
- `mcp-naming-contract` — naming is upstream of contract structure
