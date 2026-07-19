# WEALTH MCP Upgrade Pattern

Two-layer recipe for adding a new mode/param to `wealth_stock_analysis` or similar multi-mode tools.

## File Map

| File | Role | Edit? |
|------|------|-------|
| `internal/monolith.py` | Canonical implementation (17k+ lines) | Add handler function + dispatch branch + params |
| `wealth_mcp/server.py` | MCP surface wrapper | Add params + passthrough |
| `wealth_core/optimizers/` | Pure computation engines | Optional — new optimizer modules |

## Step-by-Step: Adding a New Mode

### 1. Add handler function in monolith.py (before `@mcp.tool` decorator)

```python
def _handle_new_mode(account_balance: float, ...) -> dict:
    """Docstring."""
    # computation
    return {"status": "OK", "verdict": "...", "result": {...}}
```

### 2. Add dispatch branch in monolith.py (before the `else:` clause)

```python
elif mode == "new_mode":
    r = _handle_new_mode(account_balance=account_balance, ...)
```

### 3. Add params to monolith.py function signature

```python
async def wealth_stock_analysis(
    # ... existing params ...
    new_param: float = 0.0,  # add after last existing param group
) -> dict:
```

### 4. Update error message in monolith.py

The `else:` clause lists all available modes. Add your new mode to the pipe-delimited string.

### 5. Add params to server.py wrapper

```python
@mcp.tool(name="wealth_stock_analysis")
async def wealth_stock_analysis(
    # ... existing params ...
    new_param: float = 0.0,  # must match monolith
) -> dict:
    from internal.monolith import wealth_stock_analysis as _impl
    return await _impl(
        # ... existing passthrough ...
        new_param=new_param,  # MUST pass through
    )
```

### 6. Restart + test

```bash
systemctl restart wealth
curl -sf http://localhost:18082/health
# Test via MCP tool call
```

## Preload Guard Exemption

If the new mode doesn't need external market data, exempt it from the preload guard in `server.py`:

```python
_mode = (arguments or {}).get("mode", "")
required = [] if _mode == "new_mode" else _REQUIRED_PRELOADS.get(name, [])
```

## Known Pitfalls

- **Sibling subagent overwrites**: Multiple agents editing monolith.py/server.py simultaneously. Verify changes survived after parallel runs.
- **Stale bytecode**: `find . -name "*.pyc" -delete` before restart.
- **Pyright false positives**: Large file confuses static analysis. Ignore for monolith params.
- **Preload guard blocks**: Kelly mode was blocked by `wealth://market/sources` preload until exempted.

## Kelly Mode — Reference Implementation

Kelly criterion was added 2026-07-06 as the first optimizer-driven mode:
- Closed-form math (no Pyomo needed) — `(p*b - q) / b`
- Half-Kelly default (0.5 fraction) for safety
- APEX W organ mapping (Execution — work done by optimal sizing)
- C_dark detection: low win rate, terrible risk/reward, insufficient data
- Trade history auto-estimation when `trade_history` param provided
