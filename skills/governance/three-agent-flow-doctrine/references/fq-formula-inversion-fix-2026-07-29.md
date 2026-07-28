# FQ Formula Inversion Fix — 2026-07-29

## Timeline

| Time | Event |
|------|-------|
| 2026-07-28T16:30Z | flow_state.json last written by v2 fq-probe.sh — FQ=0.5 WATCHING |
| 2026-07-29T~16:45Z | Hermes probes system: flow_state.json shows 0.5, arifFlow daemon shows 2.5 |
| 2026-07-29T~16:46Z | Root cause found — fq-probe.sh has inverted formula |
| 2026-07-29T~16:47Z | fq-probe.sh rewritten to v3 — mirrors daemon directly |
| 2026-07-29T~16:48Z | Verified: flow_state.json now matches daemon at FQ=2.5 BALANCED |

## Root Cause

fq-probe.sh (v2) computed FQ using:
```python
fq = round((total_verify + 1) / (total_exec + 1), 2)
```

This is **inverted** — FQ should be `execute / verify`, not `verify / execute`.

**Why it happened:** The original author thought FQ = verification density = verify/execute. But the canonical arifFlow formula is `Σ(exec_cost) / Σ(verify_cost)` — how much execution relative to verification. Higher = more flow. Lower = stuck in self-monitoring.

**Formula comparison:**

| Exec | Verify | v2 (WRONG) | Daemon (CORRECT) |
|:----:|:------:|:----------:|:----------------:|
| 1 | 0 | 0.5 WATCHING | 2.5 BALANCED |
| 3 | 7 | 2.0 BALANCED | (daemon uses costs) |
| 10 | 11 | 1.09 BALANCED | (daemon uses costs) |

The gap widens at low-verify states. With 1 exec + 0 verify (daemon reset state), v2 reports WATCHING — causing agents to HOLD when they should be executing.

## Chain Reaction

```
fq-probe.sh v2 (inverted formula)
  → flow_state.json: FQ=0.5 WATCHING
    → OpenClaw reads: "sistem WATCHING"
      → OpenClaw self-HOLDs (constitutional reflex: FQ<1.0 → reduce execute)
        → OpenClaw goes silent, only sends heartbeats
          → flow_state.json stops being updated by OpenClaw
            → cron takes over, perpetuates stale FQ=0.5
```

The inverted formula created a **self-reinforcing silence loop**: agents believed the system was weak, so they stopped acting, so the system appeared even weaker.

## The Fix: v3 Mirror Architecture

Instead of computing FQ at all, v3 **mirrors the daemon directly**:

```python
# v3 — no recompute
fq = float(health["fq"]["quotient"])
verdict = health["fq"]["verdict"]
execute_count = int(health["fq"]["execute_count"])
verify_count = int(health["fq"]["verify_count"])
```

Benefits:
1. Single formula — daemon is canonical source
2. No divergence between state file and daemon
3. Cost-weighted sliding window preserved (can't replicate with simple counters)
4. Removes entire class of formula bugs

## Lesson

**Never have two independent FQ computations.** The daemon's cost-weighted sliding window is mathematically richer than any count-based approximation. External probes should mirror, not recompute. If a probe must recompute (e.g., daemon down), it must document its formula explicitly and label the output as ESTIMATE.
