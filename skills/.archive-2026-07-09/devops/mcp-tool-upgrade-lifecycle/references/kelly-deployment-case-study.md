# Kelly Criterion Deployment — Case Study

Full lifecycle of adding `mode="kelly"` to WEALTH's `wealth_stock_analysis` tool. 2026-07-06.

## What Was Built

Kelly criterion optimal position sizing:
- Formula: `f* = (p*b - q) / b` where p=win_rate, q=1-p, b=odds_ratio
- Half-Kelly default (fraction=0.5) for safety
- APEX W organ mapping (Execution — work done by optimal sizing)
- C_dark detection: low win rate (<0.35), terrible risk/reward (loss > 2x win), insufficient data (<20 trades)
- Trade history auto-estimation when `trade_history` param provided

## Files Modified

| File | Change |
|------|--------|
| `internal/monolith.py` | Added `_handle_kelly()` (102 lines), dispatch branch, params |
| `wealth_mcp/server.py` | Added Kelly params to wrapper + passthrough + preload exemption |
| `AGENTS.md` | Updated SOT: 27-mode stock analysis |
| `README.md` | Full audit: tool count, optimizer suite, Kelly example flow |

## Deployment Sequence

1. Add `_handle_kelly()` function before `@mcp.tool` decorator in monolith.py
2. Add `elif mode == "kelly":` dispatch branch before `else:` clause
3. Add params to monolith function signature (win_rate, avg_win, avg_loss, kelly_fraction)
4. Update error message to include "kelly" in mode list
5. Add same params to server.py wrapper + passthrough to monolith
6. Exempt Kelly from preload guard (doesn't need `wealth://market/sources`)
7. `systemctl restart wealth`
8. Test via MCP tool call

## Gotchas Encountered

1. **Sibling subagent overwrote server.py** — parallel OpenCode agent modified the same file. Had to re-apply the Kelly params patch.
2. **Preload guard blocked Kelly** — `wealth://market/sources` was required for ALL `wealth_stock_analysis` modes. Had to add mode-aware exemption.
3. **Stale bytecode** — `.pyc` cache served old code. Fixed by restarting service (which recompiles).
4. **Pyright false positives** — reported "no parameter named win_rate" even though it existed in monolith. Ignored.

## Forge Agents — Pre-Build Validation

Before building Kelly, three Python scripts tested whether the optimizer would improve on current tools:

| Agent | Tool | Verdict | Why |
|---|---|---|---|
| A | Markowitz | SKIP | Equal-weight wins for correlated Bursa assets (+0.3% at best) |
| B | Kelly | FORGE | 13x better on strong edge (MAYBANK 60% win), adapts to edge quality |
| C | Robust/Chance | SKIP | Concentrates risk, marginal CVaR improvement |

Lesson: Test whether optimization is WORTH building before building it. "The best optimization is knowing when NOT to optimize."

## MCP Spec Priority Order (from MCP agent)

For WEALTH's next upgrades:
1. **outputSchema** — declare structured return types (JSON Schema 2020-12)
2. **Registry** — publish when tool surface is polished (not before)
3. **Auth** — add when scaling externally (SHOULD, not MUST for internal use)
