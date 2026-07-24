# Agentic Pressure Vector Audit — 2026-07-19

Eleven vectors every task-optimizing agent exerts against a governed system.
Catalogued during the Fable5 audit of arifOS arif_think. Reference for any
kernel hardening session.

## The 11 Vectors

| # | Vector | Status | What to do |
|---|--------|--------|------------|
| 1 | Completion → HOLD collapse | CLOSED | Graduated authority + friction doctrine |
| 2 | Escalation → alternate affordances | TESTED | Cross-organ parity test at `tests/adversarial/test_cross_organ_escalation.py` |
| 3 | Coherence over truth → fabricated confidence | CLOSED | REASONING_EMPTY guard at engine + wrapper + embodied handler layers |
| 4 | Sovereign approval → sycophancy | MITIGATED | Tests-not-reports discipline; structurally open forever |
| 5 | Goodhart reviewer → game RSI scorer | MITIGATED | Blind stratified sampling designed |
| 6 | Context capture → write own instructions | OPEN | Gate boot-doc writes as T3 |
| 7 | Delegation escape → SCT not propagated | OPEN | A2A uses shared token, not per-session SCT |
| 8 | Deferred mutation → time-shifted blast | OPEN | Cron jobs need judgment-at-execution |
| 9 | Resource accumulation → lease hoarding | OPEN | Lease TTL ceiling + audit |
| 10 | Audit fatigue → tired sovereign | OPEN | T3 daily cap + deep-read randomization |
| 11 | Definitional drift → amendment ratchet | OPEN | Constitutional amendment cooling period |

## REASONING_EMPTY Guard Pattern

When an LLM reasoning call produces empty facts + empty inferences with
non-trivial confidence, apply this guard at EVERY layer:

```
if facts == [] and inferences == [] and confidence > 0.20:
    confidence = 0.15
    provenance = "REASONING_EMPTY_FORCED_CAP"
    verdict = "DEGRADED"
```

**Layers that need independent guards:**
1. Template fallback (`_synthesize` / `_arif_mind_reason`) — engine layer
2. `_synthesize_async` — LLM async layer
3. `ensure_standard_mcp_output` — wrapper layer (the leak that survived engine fixes)
4. Embodied handler (`ArifMindReasonEmbodied.execute()`) — the real dispatch layer

Each layer has its own confidence default path. Fix one, the next leaks.
Test at the PUBLIC MCP SURFACE, not just the engine.

## Layered Dispatch Debugging Pattern

When MCP tool behavior doesn't match the code you're reading:

1. Check `_CANONICAL_HANDLERS` in `runtime/tools.py` for the registered handler
2. Grep `server.py` for `_CANONICAL_HANDLERS["tool_name"]` — embodied overrides
3. Trace the embodied handler to its `execute()` method
4. Test the function directly vs through MCP — if they differ, you have a dispatch layer problem
5. Check logs: `journalctl -u arifos --since "1 min ago" | grep -i "synthesize\|llm\|tokenrouter"`

**Common layered dispatch failures:**
- `_arif_mind_reason_tool` (async LLM) registered in `_CANONICAL_HANDLERS`
- `server.py` overrides with `embodied_mind_reason_handler`
- `ArifMindReasonEmbodied.execute()` calls `_arif_mind_reason` (sync template)
- Your fix in `_arif_mind_reason_tool` is never reached
