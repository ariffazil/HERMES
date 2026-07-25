# FLAME Integration Pattern — MCP Tool Wiring HOWTO

> Forged: 2026-07-25 | Applies to: All OBSERVE-class MCP tools

## When to Wire FLAME Into an MCP Tool

A tool is a FLAME candidate when it:
1. Internally calls an LLM for **non-constitutional** work (summarization, classification, synthesis, pattern matching)
2. Is **OBSERVE-class** — never mutates state, seals, or judges
3. Has **zero sovereignty** — no PII, no governance, no VAULT999

Tools that are **NOT** FLAME candidates:
- Agent cron jobs producing user-facing content (use governed cascade)
- Deterministic engines with zero LLM calls (Paper Trading, hound tools)
- Constitutional boundaries (judge, seal, think, wisdom, WELL)

## Architectural Rules (Arif-ratified 2026-07-25)

Every FLAME integration enforces these 4 rules:

| # | Rule | Implementation | Rationale |
|---|------|---------------|-----------|
| 1 | **Strict timeout (8-10s)** | `timeout_s=8` in HTTP POST — never hang the organ | F1 AMANAH — never let a free model stall a constitutional tool |
| 2 | **Graceful degradation** | Return `ok=False` or empty string on failure — never crash | A hallucinated summary is bad; a crashed organ is worse |
| 3 | **Stateless requests** | Self-contained payload per call — no context history on FLAME | FLAME is a stateless mesh; each call must carry all needed context |
| 4 | **ADVISORY authority** | Every output tagged `authority: "ADVISORY"` in provenance envelope | F2 TRUTH — FLAME output is evidence, never judgment |

## Reference Implementation: `flame_client.py`

Location: `/root/GEOX/src/geox_mcp/tools/flame_client.py`

A standalone HTTP module providing 3 functions:

```python
from geox_mcp.tools.flame_client import flame_summarize, flame_classify, flame_contradiction_analysis

# Summarization / synthesis
result = flame_summarize(text, caller_id="geox")
if result.get("ok"):
    synthesis = result.get("content", "")

# Classification
result = flame_classify(text, categories=["A", "B", "C"], caller_id="geox")
if result.get("ok"):
    label = result.get("content", "")

# Contradiction analysis (GEOX-specific)
result = flame_contradiction_analysis(claim_a, claim_b, caller_id="geox")
if result:
    analysis = result.get("analysis", "")
```

All return dicts with `ok: bool` + `content: str`. Never raise exceptions.

### Internal Architecture

```
flame_summarize(text)
  └─ _flame_post("/summarize", payload, timeout_s=8)
       └─ urllib.request.urlopen(POST :18901/summarize)
            ├─ 200 OK with ok=True   → return parsed JSON
            ├─ HTTP 400+ with ok=True → accept (FLAME bug: sends 400 even when ok)
            ├─ HTTP error             → log warning, return None
            ├─ timeout                → log warning, return None
            └─ connection refused     → log warning, return None
```

Key implementation detail: `_flame_post` treats HTTP 400 as potentially valid because the FLAME API server returns 400 whenever the response dict contains an `"error"` key — even when the value is `""` and `ok=True`. The client must parse the body and check `result.get("ok")` rather than relying on HTTP status code.

## Wiring Pattern: Two Approaches

### Approach A: Replace governed cascade call

When a tool currently calls `arif_think` or another paid LLM path, swap the call to `flame_summarize()`:

**Before (governed cascade):**
```python
from arifosmcp.runtime.tools import _synthesize_async
llm_result = await _synthesize_async(query, reasoning_mode="reason")
synthesis_text = llm_result.get("bounded_answer")
```

**After (FLAME RM0):**
```python
from geox_mcp.tools.flame_client import flame_summarize
result = flame_summarize(query, caller_id="my_tool")
if result.get("ok"):
    synthesis_text = result.get("content", "")
```

### Approach B: Add FLAME as fallback for edge cases

When a tool has deterministic logic that returns UNKNOWN for edge cases, add FLAME as the semantic fallback:

```python
# Step 1: Deterministic classification (fast, always works for common cases)
ctype = rule_based_classify(claim_a, claim_b)
if ctype != UNKNOWN:
    return ctype

# Step 2: FLAME fallback (slower, catches semantic edge cases)
from geox_mcp.tools.flame_client import flame_contradiction_analysis
result = flame_contradiction_analysis(text_a, text_b, caller_id="my_tool")
if result:
    return parse_flame_result(result)

# Step 3: Ultimate fallback
return UNKNOWN
```

## Provenance Envelope Pattern

Every FLAME integration should attach provenance metadata to the output:

```python
artifact["llm_source"] = "FLAME (RM0 free-tier mesh)"
artifact["llm_source_provenance"] = {
    "engine": "FLAME",
    "chain": "RM0-TOOLS-FREELOOP",
    "authority": "ADVISORY",
    "note": "FLAME output is advisory — not constitutional judgment",
}
artifact["llm_confidence"] = 0.7  # FLAME advisory confidence (not calibrated)
```

## Adding to a New Organ Repo

1. Copy `flame_client.py` pattern into the organ's tool directory
2. Wire into specific tools using Approach A or B above
3. Add provenance envelope to outputs
4. Run organ test suite — all existing tests must pass
5. Run `flame --mode probe` to confirm fleet health
6. Update the wiring table in this skill's SKILL.md

## Known Issues

- **FLAME API server returns 400 with valid content**: The `_send()` handler uses `200 if "error" not in result else 400`. Since all responses include `"error": ""`, every response gets 400. The client must handle this. Fix pending: change to `200` unconditionally.
- **Fleet health can change without notice**: Free-tier providers add/remove models, change rate limits. Always `flame --mode probe` before wiring a new pipeline. See `fleet-health-reality-gap` pitfall in SKILL.md.
- **OpenRouter rate-limited**: 20rpm/50rpd shared across all free models. Only use as Tier-3 fallback.
