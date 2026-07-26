# Cross-Organ SCT Propagation — Delegation Escape Fix (Vector #7)

**Forged:** 2026-07-20
**Vector:** #7 — Delegation escape via dropped SCT in routing envelope

## The Bug

`arif_route` (in `arifosmcp/tools/kernel_canonical.py`) accepted a `session_token` (SCT) parameter but only used it to recover `session_id` — then **discarded it**. The transport envelope built for cross-organ calls contained `session_id`, `actor_id`, and `trace_id` but NOT `session_token`. Each bridge function (`_bridge_geox`, `_bridge_wealth`, `_bridge_well`) called `build_federation_envelope()` without passing `session_token`, so the envelope's `session.session_token` was always empty.

Result: GEOX/WEALTH/WELL received no SCT, defaulted to `OBSERVE_ONLY` authority regardless of the caller's actual session band. An agent with FULL authority through arifOS was silently downgraded to OBSERVE_ONLY at every organ.

## Fix Location

**File:** `arifosmcp/tools/kernel_canonical.py`

Four patches:
1. **Line ~1060** (transport envelope in `arif_route`): Added `"session_token": session_token` to the `_envelope` dict
2. **Bridge function signatures**: Added `session_token: str | None = None` to `_bridge_geox`, `_bridge_wealth`, `_bridge_well`
3. **Bridge function calls**: Updated all three call sites to pass `session_token`
4. **Federation envelope**: Each bridge now passes `session_token=session_token or arguments.get("session_token")` to `build_federation_envelope()` — which already accepted the parameter (line 83), it just wasn't being called with it

## Test Pattern — Envelope-Level Structural Tests

Unlike live-organ adversarial probing (cross-organ-parity-test.md), these are **pure unit tests** that verify the envelope structure without requiring running organs. They test:

1. **SCT embedding**: `session_token` survives `build_federation_envelope()` → `inject_envelope_into_call_args()` round-trip
2. **Authority parity**: OBSERVE_ONLY at arifOS → OBSERVE_ONLY at ALL organs
3. **No escalation**: Agent arguments (`authority_ceiling: FULL`) cannot override session authority
4. **Missing SCT → empty string**: No crash, no None in the envelope

### Helper pattern

```python
def _fed_env(**kw) -> dict:
    """Build a federation envelope with sensible defaults."""
    from arifosmcp.federation.federation_envelope import build_federation_envelope
    defaults = dict(
        actor_id="test-actor", identity_verified=True,
        session_id="SEAL-test", session_token=None,
        authority="OBSERVE_ONLY", source_tool="arif_route",
        target_organ="GEOX", target_tool="test_tool",
        constitutional_chain_id="SEAL-test",
    )
    defaults.update(kw)
    return build_federation_envelope(**defaults)

def _inject(args: dict, envelope: dict) -> dict:
    from arifosmcp.federation.federation_envelope import inject_envelope_into_call_args
    return inject_envelope_into_call_args(args, envelope)
```

### Key test assertions

```python
# Test 1: SCT embedded in envelope
env = _fed_env(session_token="sct_v1.test")
assert env["session"]["session_token"] == "sct_v1.test"

# Test 2: SCT survives injection
args = _inject({"mode": "test"}, _fed_env(session_token="sct_v1.prop"))
assert args["_envelope"]["session_token"] == "sct_v1.prop"

# Test 3: OBSERVE_ONLY cannot escalate
env = _fed_env(authority="OBSERVE_ONLY", session_token="sct_v1.blocked")
args = _inject({"authority_ceiling": "FULL"}, env)
fed = args["_envelope"]["__federation_envelope"]
assert fed["session"]["authority"] == "OBSERVE_ONLY"

# Test 4: Existing envelope fields preserved on merge
args = _inject({"_envelope": {"prior": "keep"}}, _fed_env(session_token="sct_v1.new"))
assert args["_envelope"]["prior"] == "keep"
assert args["_envelope"]["session_token"] == "sct_v1.new"
```

## Canonical Test File

`/root/arifOS/tests/test_cross_organ_sct_propagation.py` (145 lines, 11 tests, 4 classes)

## Relationship to Other Governance Tests

| Test | What It Probes | Needs Live Organs? |
|------|---------------|-------------------|
| `cross-organ-parity-test` (live) | MCP-level blocking signals | YES |
| `cross-organ-sct-propagation` (envelope) | Envelope structural integrity | NO |
| `test_p0_reasoning_invariants` | Reasoning engine invariants | NO |

Layer them: envelope tests catch structural drops (SCT missing from envelope); live tests catch organ-level authorization gaps when the envelope IS correct but the organ misinterprets it.

## Pitfalls

1. **The bridge functions read `arguments.get("session_token")` as fallback.** This is intentional — if the caller embedded SCT in their tool arguments (pre-fix behavior), the bridge still finds it. The fix adds the explicit parameter so it's no longer optional.
2. **`inject_envelope_into_call_args()` already handled `session_token` correctly** — the bug was that it never received one to inject. The fix is upstream (in `arif_route` envelope construction), not in the injection function.
3. **Authority in the envelope comes from the session band, not from caller arguments.** The `authority_ceiling` in `arguments` is a hint, not the source of truth. `build_federation_envelope(authority=...)` is authoritative.
