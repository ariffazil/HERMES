# Adding Constitutional Gates to arifOS Python Kernel

Pattern for inserting new decision gates into the `arif_kernel_intercept` chain
(`/opt/arifos/arifosmcp/tools/arif_kernel_intercept.py`). Captured from the F8
GENIUS / 17x Rule implementation (2026-07-12).

---

## Kernel Decision Chain (current order)

```
1.  R4/R5 without sovereign token → ESCALATE (F13)
2.  FACT/ESTIMATE without evidence → DENY (F2)
2b. CONFLICT without evidence → ESCALATE (F2)
2c. HYPOTHESIS/CLAIM high-blast without evidence → ESCALATE (F2)
2d. Low confidence + irreversible → SABAR (F8) — 17x RULE
3.  Standard ALLOW
```

Each gate returns early. Once a gate fires, no subsequent gate runs.

---

## Critical Pitfall: Gate Ordering + Default Parameters

When adding a new gate that checks R4/R5 + some condition:

1. **Gate 1 (F13) catches ALL R4/R5 without sovereign token first.** If your
   new gate is placed after gate 1, R4/R5 tests without tokens will never reach
   it — they'll return ESCALATE F13 instead.

2. **Existing tests use default parameter values.** For example, existing R4/R5
   tests don't set `epistemic_state` (defaults to UNKNOWN). If your new gate
   triggers on UNKNOWN, existing tests break.

3. **Sovereign token bypass.** R4/R5 WITH a valid sovereign token passes through
   gate 1 and reaches subsequent gates. Your new gate's R4/R5 tests must include
   `authority_token=sentinel` to actually reach the gate.

### Decision tree for gate placement

```
Want to intercept R4/R5 + condition X?
│
├─ Should it fire BEFORE authority check (gate 1)?
│  → Place before gate 1
│  → Add `and not _verify_sovereign_token(authority_token)` to avoid
│    breaking existing R4/R5 + token tests that expect ALLOW
│  → ⚠️ Existing R4/R5 tests WITHOUT token (default epistemic_state)
│    will now hit your gate instead of F13 ESCALATE
│
└─ Should it fire AFTER authority check?
   → Place after gate 1 (e.g., as gate 2d)
   → R4/R5 without token never reach it (F13 catches them)
   → Tests must pass sovereign token to reach your gate
   → ⚠️ Existing R4/R5 + token tests with default epistemic_state
     may now hit your gate instead of ALLOW
```

### Neither placement is free — pick based on semantics:

- **Before gate 1**: Use when the condition is more fundamental than authority
  (e.g., "you shouldn't act even if authorized because confidence is too low").
  Requires `not _verify_sovereign_token()` guard OR accepting that existing
  no-token R4/R5 tests change behavior.

- **After gate 1**: Use when authority is a prerequisite (e.g., "only check
  confidence after confirming the actor has permission"). Requires sovereign
  tokens in new R4/R5 tests. Existing token-bearing tests may change behavior.

---

## Adding a New Decision Type (e.g., SABAR)

When adding a new `decision` value to `KernelOutput`:

1. **Schema first**: Update the `Literal` in
   `/opt/arifos/arifosmcp/schemas/minimum_kernel.py`:
   ```python
   decision: Literal["ALLOW", "DENY", "ESCALATE", "SIMULATE", "SABAR"]
   ```

2. **LSP stale cache**: Pyright may report type errors even after updating the
   schema. The error is cosmetic — the Literal is already correct. Ignore it.

3. **`_SIGNAL_SEVERITY` in tools.py**: If the new decision maps to a signal
   severity (for monotonicity checks), ensure it's in the dict:
   ```python
   "SABAR": 1,  # severity 1 = held/deferred
   ```

---

## Test Pattern for New Gate (R4/R5 + sovereign token)

```python
@pytest.mark.asyncio
class TestF8_17xRule:
    """F8 GENIUS: Low epistemic confidence + irreversible action → SABAR."""

    async def test_hypothesis_irreversible_sabar(self):
        sentinel = os.environ.get(
            "ARIFOS_SOVEREIGN_KEY",
            "DEV_ONLY_SENTINEL_REPLACE_AT_PROD_BOOT",
        )
        r = await _arif_kernel_intercept(
            actor="test-agent",
            intent="deploy unvalidated model",
            requested_capability="forge_deploy",
            domain="arifOS",
            reversibility_level="R4",
            blast_radius="low",        # avoid gate 2c (high-blast + no evidence)
            epistemic_state="HYPOTHESIS",
            authority_token=sentinel,   # bypass gate 1 (F13)
        )
        assert r["decision"] == "SABAR"
        assert r["constitutional_floor_triggered"] == "F8"
```

**Key test design choices:**
- `authority_token=sentinel` — bypasses F13 so the test reaches gate 2d
- `blast_radius="low"` — avoids triggering gate 2c (HYPOTHESIS + capital/constitution/external-recipient + no evidence → ESCALATE F2)
- For tests that should NOT trigger the new gate (e.g., FACT + R4), omit the
  sovereign token — gate 1 catches them at F13 ESCALATE
- **Sovereignty ≠ epistemic immunity test:** Always add a test with sovereign token + UNKNOWN epistemic state. This proves the gate fires even for the sovereign when confidence is low. Authority grants PERMISSION; epistemic state grants CONFIDENCE. They are orthogonal.
- **Updating existing sovereign tests:** When a new gate intercepts R4/R5 with UNKNOWN epistemic state, existing tests like `test_r5_with_correct_sentinel_allows` will break (they used default `epistemic_state=UNKNOWN`). Fix: add `epistemic_state="FACT"` + `evidence=[...]` to make the test explicitly declare high confidence. The breakage is CORRECT behaviour.

---

## Running Tests

```bash
cd /opt/arifos && python -m pytest tests/runtime/test_kernel_intercept.py -v
```

---

## Files Modified for F8 17x Rule (2026-07-12)

| File | Change |
|------|--------|
| `schemas/minimum_kernel.py` | Added `"SABAR"` to `KernelOutput.decision` Literal |
| `tools/arif_kernel_intercept.py` | Added gate 2d between step 2c and step 3 |
| `runtime/tools.py` | Added `"irreversible_below_0_80"` to `DECISION_THRESHOLDS` |
| `tests/runtime/test_kernel_intercept.py` | Added `TestF8_17xRule` class (6 tests) |
