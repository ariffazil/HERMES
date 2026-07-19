# WEALTH New Domain + New Tools Pattern

Adding an entirely new domain (e.g., `institutional/`, `optimization/`) with pure engines and new MCP tools. Distinct from the "add mode to existing tool" pattern in `wealth-mcp-upgrade-pattern.md`.

## File Map

| File | Role | Create/Edit? |
|------|------|-------------|
| `wealth_core/<domain>/__init__.py` | Module init, exports engine functions | CREATE |
| `wealth_core/<domain>/<engine>.py` | Pure computation (no I/O, no MCP) | CREATE |
| `wealth_mcp/tools/<domain>.py` | Standalone MCP tool registration | CREATE (optional) |
| `wealth_mcp/server.py` | MCP surface — inline registration + public names | EDIT |
| `tests/test_<domain>.py` | Tests with real-case fixtures | CREATE |

## Step-by-Step

### 1. Create pure engines in `wealth_core/<domain>/`

Each engine is a pure function: inputs in → dict out. No MCP, no I/O, no side effects.

```python
# wealth_core/<domain>/__init__.py
from .engine_a import compute_a
from .engine_b import compute_b
__all__ = ["compute_a", "compute_b"]
```

**Rules:**
- All outputs `0-1` clamped where applicable
- F7 HUMILITY: confidence cap 0.90 — `min(0.90, signal_richness)`
- F9 ANTI-HANTU: declare unknowns, no hallucinated defaults
- Deterministic: no random without seed
- Return `confidence` + `confidence_note` in every result

### 2. Create MCP tool registration (inline in server.py)

Follow the existing pattern — `_register_<domain>_tools(mcp)` function:

```python
def _register_institutional_tools(mcp: FastMCP) -> None:
    """Docstring with tool list."""
    from wealth_core.<domain> import compute_a, compute_b

    @mcp.tool(
        name="wealth_<tool_name>",
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True,
            "apex_primitive": "ΔG Governance",
        },
    )
    async def wealth_<tool_name>(param: str, ...) -> dict:
        """Docstring becomes MCP tool description."""
        result = compute_a(param=param, ...)
        return wrap_result(
            tool_name="wealth_<tool_name>",
            domain="<domain>",
            result=result,
            epistemic_tag=EpistemicTag.DERIVED,  # or INTERPRETED
            evidence_quality=EvidenceQuality.MODERATE,
            source_attribution=["source_a_OBS", "source_b_DER"],
        )
```

### 3. Register in server.py — 4 edits required

**Edit 1: Import** (top of file, after existing core imports):
```python
from wealth_core.<domain> import compute_a, compute_b
```

**Edit 2: Call registration** (in `create_mcp_server()`, after existing `_register_*` calls):
```python
_register_<domain>_tools(mcp)
```

**Edit 3: Add to public names** (in `WealthSurfaceFilterMiddleware.on_list_tools`):
```python
public_names = {
    ...
    "wealth_<new_tool_1>",
    "wealth_<new_tool_2>",
}
```

**Edit 4: Update `_infer_domain()`** (if new domain name):
```python
if any(k in t for k in ("<domain_keyword>",)):
    return "<domain>"
```

### 4. Write tests

```python
# tests/test_<domain>.py
import pytest
from wealth_core.<domain>.engine_a import compute_a

# Fixture: real-world case data
REAL_CASE_INPUT = { ... }

class TestEngineA:
    def test_real_case(self):
        result = compute_a(**REAL_CASE_INPUT)
        assert 0.0 <= result["score"] <= 1.0
        assert result["confidence"] <= 0.90

    def test_empty_inputs(self):
        result = compute_a(empty=True)
        # Should not crash

    def test_maximum_stress(self):
        result = compute_a(**MAXIMUM_INPUT)
        assert result["risk_level"] == "CRITICAL"

    def test_deterministic(self):
        r1 = compute_a(**REAL_CASE_INPUT)
        r2 = compute_a(**REAL_CASE_INPUT)
        assert r1 == r2

class TestIntegration:
    def test_full_pipeline(self):
        # Tool 1 output feeds Tool 2 input
        a = compute_a(**INPUT)
        b = compute_b(stress=a["score"])
        assert b["gap"] > 0
```

### 5. Optional: standalone registration file

Create `wealth_mcp/tools/<domain>.py` with `register_<domain>_tools(mcp)` for standalone use outside the server. This is optional — server.py inline is the primary path.

## Epistemic Tagging Rules

| Signal Source | Tag | Example |
|--------------|-----|---------|
| Financial data (filing, price) | OBSERVED | profit_change_pct |
| Governance data (board filings) | OBSERVED | board_size, resignations |
| Computed from observed data | DERIVED | stress_index, capacity_score |
| Pattern from temporal data | INTERPRETED | cascade_type, trajectory |
| Behavioral pattern matching | DERIVED | exploitation_score |
| Hypothesis without evidence | SPECULATED | (rare, flag explicitly) |

## Cascade Detection Pitfall

**Pitfall:** Constant deltas (e.g., 0.15 every period) produce zero second-derivative → classified as LINEAR, not SPIRAL.

**Fix:** Test timelines must have *accelerating* deltas — the gap between periods must INCREASE:
```
# WRONG: constant delta → LINEAR
[0.20, 0.35, 0.50, 0.65, 0.80]  # deltas: 0.15, 0.15, 0.15, 0.15

# RIGHT: accelerating delta → SPIRAL
[0.20, 0.35, 0.55, 0.75, 0.92]  # deltas: 0.15, 0.20, 0.20, 0.17
                                  # 2nd deltas: +0.05, 0, -0.03
                                  # LAST 2nd delta must be > 0.01
```

The cascade detector checks `deltas[-1] - deltas[-2] > 0.01` — only the LAST second-derivative matters.

## Exploitation Classification Ordering

**Pitfall:** SIMULATIVE_NEUTRAL is a superset of AGGRESSIVE conditions. If checked first, AGGRESSIVE never triggers.

```python
# WRONG: SIMULATIVE_NEUTRAL catches everything first
if avg_rationality > 0.3 and high_rationality >= 2:
    return "SIMULATIVE_NEUTRAL"
if avg_rationality > 0.6:
    return "AGGRESSIVE"  # dead code

# RIGHT: check most specific first
if avg_rationality > 0.6 or (high_rationality >= 3 and indicators >= 5):
    return "AGGRESSIVE"
if avg_rationality > 0.3 and high_rationality >= 2:
    return "SIMULATIVE_NEUTRAL"
```

## Pre-existing Issue: `wealth_core.optimizers` Missing

`wealth_mcp/server.py` imports `wealth_core.optimizers` which may not exist on all branches. This is NOT caused by new domain additions. Workaround: test MCP registration in isolation:

```python
from fastmcp import FastMCP
mcp = FastMCP('test')
from wealth_mcp.tools.<domain> import register_<domain>_tools
register_<domain>_tools(mcp)
tools = asyncio.run(mcp.list_tools())  # Verify registration
```
