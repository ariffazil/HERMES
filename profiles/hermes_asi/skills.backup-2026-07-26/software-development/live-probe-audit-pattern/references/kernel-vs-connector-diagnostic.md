# Kernel-vs-Connector Diagnostic Pattern

**When an external audit claims "identity system is broken" or "authority chain is failing":**

1. Probe the kernel directly first — not through connectors, not through ChatGPT bridge.
2. `curl /health` → check `runtime_drift`, `contract_drift`, `runtime_matches_build`
3. `arif_init(mode="light")` → check `actor_verified`, `authority_mode`
4. Compare source git SHA vs deployed SHA from health endpoint.

**Decision matrix:**

| Kernel Signal | Meaning |
|---|---|
| `actor_verified=false` for anonymous | CORRECT — not a failure |
| `runtime_drift=false`, source=deployed | CORRECT — identity chain intact |
| `arif_init(validate)` rejects without session | CORRECT — validate needs prior session |
| Stale connector verb (e.g., `arif_session_init`) | CONNECTOR issue, not kernel |
| Session ID truncated in bridge | KERNEL BRIDGE bug, not identity system |
| `IDENTITY_NOT_VERIFIED` banner | CORRECT for anonymous callers |

**The pattern:** External audits often conflate connector/schema drift with kernel identity failure. The kernel enforces identity correctly; the connector just advertises stale verbs. Fix the connector, not the kernel.

**Scar from 2026-07-19:** An external audit claimed arifOS identity was broken and required P0 recovery. Live probes showed the kernel was healthy — `actor_verified=false` is correct behavior for anonymous callers, and the `IDENTITY_NOT_VERIFIED` banner is a feature, not a bug. The real issues were ChatGPT connector stale verbs and GEOX session ID truncation in the kernel bridge. Six hours of diagnostic work confirmed: constitutional core healthy, connector layer needs patching.
