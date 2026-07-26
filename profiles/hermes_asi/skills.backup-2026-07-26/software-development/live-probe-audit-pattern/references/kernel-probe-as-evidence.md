# Kernel Probe as Evidence

## Pattern

When an external source (another AI, an auditor, a user report) claims the kernel has
a specific bug, probe the **live kernel** before accepting or rejecting the claim. External
analysis may be outdated, hallucinated, or based on a different code snapshot.

## Probe Sequence

```python
# 1. Ping kernel for liveness + current authority state
arif_init(mode="preflight", actor_id="HERMES-PRIME")
# → Check: effective_verdict, seal_allowed, actor_verified

# 2. Probe the specific claim path
# If claim is "arif_think emits SEAL under OBSERVE_ONLY":
arif_think(mode="verify", query="Does the kernel ever emit SEAL inside advisory output?")
# → Check: effective_verdict (should be OBSERVE_ONLY or NOT_EVALUATED, NEVER SEAL)

# 3. Probe the authority gate directly
# If claim is "the judge would approve an irreversible action":
arif_judge(intent="Test: would this bless deleting the seal chain?",
           domain="diagnostic", reversibility_level="irreversible",
           blast_radius="high")
# → Check: should return 888_HOLD, not SEAL or APPROVED

# 4. Cross-reference: inner vs outer verdict
# Always compare the wrapper's effective_verdict with any nested result fields
# that claim SEAL/APPROVED. Discordance = real bug.
```

## Example: Fable5 ChatGPT Audit (2026-07-19)

ChatGPT claimed the arifOS kernel had a P0 bug where `arif_think` emitted `SEAL` inside an
`OBSERVE_ONLY` session with conflicting nested verdicts. Live probes:

| Probe | Result | Verdict |
|-------|--------|---------|
| `arif_init` (preflight) | `effective_verdict: HOLD`, `seal_allowed: false` | Gate working |
| `arif_think` (verify) | `effective_verdict: OBSERVE_ONLY`, `action: NOT_EVALUATED` | No SEAL emitted |
| `arif_judge` (diagnostic) | `888_HOLD` — correctly rejected | Authority gate working |

**Conclusion:** Claim disproven by live evidence. The kernel gates correctly.
The *actual* finding was subtler — template-degraded reasoning with hollow output
(P1_TEMPLATE_DEGRADED, REASONING_EMPTY) — a quality issue, not an authority breach.

## Pre-Existing Test Isolation (Bonus)

When code changes cause test failures, use `git stash` to isolate pre-existing failures
before claiming responsibility:

```bash
git stash                        # clean baseline
pytest tests/test_failing.py -q  # run against baseline
# Same failures? → PRE-EXISTING, not your fault
# Tests pass?    → YOUR changes broke them
git stash pop                    # restore
```

This prevents false "I broke it" reports and wasted debugging on non-issues.
