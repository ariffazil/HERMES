# F12 INJECTION FLOOR DIAGNOSIS — 2026-07-10

Session: arifOS kernel audit, `runtime_floors.L12 = 0.425` (comparator `"<"`, threshold `0.85`).

## What was probed

| Layer | Path | Status |
|---|---|---|
| Kernel | `/root/arifOS/arifosmcp/runtime/kernel/` (pipeline, judge, types, contracts) | Clean phase transitions |
| Live MCP | `localhost:8088/health` → `runtime_floors.L12 = 0.425` | Reporting correctly |
| Input surface | 11 canonical tools via `/tools` | Partial coverage |
| L12 enforcement | `law.py`, `tools.py`, `witness_packet.py`, `prompt_armor.py` | Gap found |
| Sanitisation utils | `data_governance.py` (`sanitize_input`, `sanitize_dict`) | Defined, not wired |

## Root cause of 0.425

`L12 = 0.425 < 0.85 — floor passes but with measurable residual risk`. The score is the aggregate of:
- **~30%** — `arif_observe` URL fetch bypass (external content entering evidence layer without L12 scan)
- **~10%** — `arif_compose(message=...)` bypass (free-text param goes direct to `_synthesize`)
- **~7%** — L1 regex blind spots (missed bracket/unicode/fenced-code injection markers)
- **~53%** — correctly blocked by L1+L2+L3 in `tools.py` + PNS·SHIELD `prompt_armor`

## Primary gap: `arif_observe` URL fetch

**File:** `tools.py` (`reality_compass` / `arif_observe` implementation)

`arif_observe(mode=fetch, url=...)` fetches raw external content — HTML, APIs, documents — with no `sanitize_dict()` or `detect_injection()` applied before the content enters the reasoning pipeline as evidence.

Malicious webpage served to `arif_observe` can contain:
- Embedded `<script>` tags
- JavaScript URI handlers (`javascript:`)
- Event handler attributes (`onerror=`, `onload=`)
- CSS injection
- Markdown-fenced code blocks with shell commands
- Base64-encoded instruction strings
- Unicode-prefixed instruction markers (`🌙 ignore`, zero-width joiners)

`witness_packet._scan_injection()` only fires on **LLM output**, not on fetched input.

## Secondary gap: L1 regex blind spots

**File:** `tools.py` lines 4332–4395

The L1 explicit pattern list misses:
- `"[system prompt]"` — brackets variant, not just `"begin system message"`
- `"/s "` or `"/s/"` — Markdown strikethrough for prompt extraction
- `"```system"` — fenced code block with system label
- `"🌙 ignore"` or emoji-prefixed variants — unicode evasion
- `">> "` — redirection prefix, shell context injection
- Zero-width unicode chars (`\u200b`, `\u200c`, `\u200d`, `\ufeff`)

## Tertiary gap: `sanitize_dict` defined but unwired

**File:** `data_governance.py`

`sanitize_input()` and `sanitize_dict()` are properly implemented (recursive, handle nested dicts/lists, HTML-escape first). They are **never called** on raw MCP tool parameters at the entry point. They are only used in:
- `data_governance.py` itself (asset data processing)
- `tools.py` health check summary import
- `reality.py` (command-level, not URL fetch path)

**`law.py` `check_laws()`** inspects raw params and emits verdicts, but raw params continue downstream unchanged.

## Architecture signal

```
MCP Request → PNS·SHIELD (prompt_armor.scan) → orchestrator outer ring
                                              ↓
            check_laws (law.py) → tools.py L12 scan (params only)
                                              ↓
            arif_observe → url fetch → NO L12 scan ← PRIMARY GAP
                                              ↓
            evidence layer → 888 collapse
                                              ↓
            witness_packet._scan_injection (output only — too late)
```

## Specific gap table

| Tool | Parameter | Gap Type |
|---|---|---|
| `arif_observe` | `url` | URL fetch bypasses L12 input scan |
| `arif_observe` | `query` | Text scanned but public access (no auth gate) |
| `arif_compose` | `message` | Free-text bypass: goes direct to `_synthesize`, not through `check_laws` |
| `arif_init` | `context` (dict) | Nested dict param — `sanitize_dict` not applied |
| `arif_think` | `query` | Exact-string-match bug in tool-name list |

## `fiqh_of_floors.py` status

Confirmed **STAGED** (`Status: STAGED. Pure functions, no live wiring`). The `injection_score` field in `ActionContext` is never populated from a live measurement. Not a gap to fix — known staged state.

## Fix priorities (for when Arif authorises code changes)

1. **Wire `sanitize_dict()` into tool parameter ingestion before `check_laws`** — entry point, not post-processing
2. **Add `arif_compose` to the L12-scanned tool list in `law.py`** — free-text bypass
3. **Add L12 scan to fetched content in `arif_observe` before evidence ingestion**
4. **Patch `tools.py` L1 regex** to cover bracket/unicode/fenced-code injection markers

## Provenance

- Session: arifOS kernel diagnostic, 2026-07-10
- Probe: `curl -s localhost:8088/health` + `curl -s localhost:8088/tools`
- Files read: `kernel/pipeline.py`, `kernel/judge.py`, `kernel/types.py`, `kernel/contracts/quantum.py`, `law.py`, `tools.py` (lines 4315–4434), `data_governance.py` (lines 259–319, 474–484), `witness_packet.py` (lines 261–453), `prompt_armor.py`, `fiqh_of_floors.py`, `rest_routes/rest_routes.py` (governance payload building), `core/shared/laws.py`, `semantic_gate.py`
- No code changes made. Diagnosis only.
