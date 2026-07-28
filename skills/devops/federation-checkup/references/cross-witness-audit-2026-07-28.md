# Cross-Witness Audit Verification — 2026-07-28

> Hermes verified OpenCode (FI-001) deep internal scan claims against live federation state.

## Source Audit

OpenCode produced a 7-layer "Reality Alignment Audit" covering: organs, agents, skills, tools, MCP wiring, memory/continuity, and prompts/doctrine. Claimed: "70% aligned, 30% drift."

## Hermes Verification

Every claim was independently verified via live probe before acceptance:

### Claims Confirmed True (5/8)

| Claim | Probe Method | Evidence |
|-------|-------------|----------|
| Hermes systemd inactive | `systemctl is-active hermes` | Returned "inactive" |
| Kernel deployment drift | `curl :8088/health` → `drift: true`, source=711f8f5 ≠ built=3677c96 | Verified divergence |
| WEALTH version UNAVAILABLE | `curl :18082/health` → git_commit: UNAVAILABLE | Confirmed |
| WELL degraded | `curl :18083/health` → status: "degraded", 5.3h stale data | Confirmed (expected for self-report organ) |
| 14 open loops | `cat /root/.local/share/arifos/carry_forward.json` | Confirmed |

### Claims Confirmed False (3/8)

| Claim | Truth | Root Cause |
|-------|-------|------------|
| "MCP resources = 0" | `list_resources` returns all ATLAS333, doctrine, vitals | OpenCode hit wrong endpoint or protocol mismatch |
| "VAULT999 silent 4 days" | 3 seals from 2026-07-28: 10:44, 10:45, 10:58 UTC | OpenCode read stale cache or wrong file |
| "Kernel healthy+F2 violation" | service_health=green, execution_readiness=held — correct separation | OpenCode conflated two distinct kernel fields |

### Accuracy: ~60%

3 of 8 claims were false. All were presented with equal confidence as the true ones.

## Key Lessons

- **Single-agent audit = OBSERVATION, not TRUTH.** Always cross-witness.
- **Confidence ≠ accuracy.** The false claims were phrased as damningly as the true ones.
- **Interpretive claims are unreliable.** "This means X" is weaker than "this shows Y."
- **Alarming claims are most likely wrong.** "70% aligned, 30% drift" was too dramatic — verified reality was closer to 85-90%.
