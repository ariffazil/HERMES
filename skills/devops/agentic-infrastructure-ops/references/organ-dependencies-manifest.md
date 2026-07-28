# Organ Dependencies Manifest — Cascade Prevention

## Problem
When organ X degrades, downstream organs don't know to pause. Agent-level reasoning can't be trusted to handle cascades — agents hallucinate, ignore instructions, or misdiagnose H_WELL (human) vs M_WELL (machine).

## Solution
A formal dependency manifest at `/etc/arifos/organ_dependencies.json` that encodes dependency relationships at the wire layer. Enforcement is architectural — the MOTD checks organ health, consults the manifest, and injects `AF_BLOCKED_ORGANS` into the agent env.

## Canonical Schema

```json
{
  "version": "1.0.0",
  "organs": {
    "arifOS": {
      "port": 8088,
      "depends_on": {},
      "depended_by": ["A-FORGE", "AAA", "GEOX", "WEALTH", "WELL"],
      "fallback": "none — kernel is root dependency"
    },
    "WEALTH": {
      "port": 18082,
      "depends_on": {
        "GEOX": { "status": "healthy", "reason": "bridge requires prospect eval" },
        "arifOS": { "status": "healthy", "reason": "ledger writes need kernel vault authority" }
      },
      "depended_by": [],
      "fallback": "Serve cached market data, HOLD new prospect evaluation"
    }
  },
  "cascade_rules": {
    "mode": "BLOCK_ON_DEGRADED",
    "max_hops": 2,
    "auto_hold_organs": true,
    "notify_888": true
  }
}
```

## Dependency Graph (af-forge, 2026-07-27)

```
arifOS (8088) ──┬── A-FORGE (7071)
                ├── AAA (3001)
                ├── GEOX (8081) ── WEALTH (18082)
                └── WELL (18083)
```

**Cascade rule:** If GEOX degraded → WEALTH auto-HOLD. If arifOS degraded → ALL HOLD.

## Enforcement Flow

```
GHOST MOTD probes organ health
  → degrades detected (e.g., "WELL": "degraded")
  → consult dependency manifest
  → find all dependents of degraded organ
  → inject AF_BLOCKED_ORGANS into /var/run/arifos_env.sh
  → agent sources env → blocks if AF_BLOCKED_ORGANS non-empty
  → cascade stopped at wire layer, not agent layer
```

## Key Design Decisions

| Decision | Why |
|----------|-----|
| **Architectural enforcement** | Cascade is stopped at POSIX layer (wire), not agent layer. Agent never decides to pause — the env forces it. |
| **H_WELL vs M_WELL isolation** | When H_WELL (human readiness) is degraded, agents don't try to "fix" humans (F9 Anti-Hantu violation prevented). System just HOLDS. |
| **Fallback per organ** | Each organ declares what it does when dependencies fail. Prevents starvation — cached data still serves. |
| **max_hops: 2** | Cascades don't propagate more than 2 hops. Stops chain-reaction failure. |

## Verified
- arifOS federation, af-forge VPS (2026-07-27)
- WELL detected as degraded → no cascade (WELL is leaf organ)
- GEOX → WEALTH cascade tested via manifest validation
