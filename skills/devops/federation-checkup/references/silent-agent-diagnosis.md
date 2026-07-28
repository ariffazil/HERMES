# Silent Agent Diagnosis — Telemetry Drift

> **Signal:** Agent process running (`ps aux` shows it, CPU/RAM stable) but not responding or acting.
> **Most likely cause:** Telemetry dual-source mismatch. Agent reads wrong FQ → constitutional HOLD.

## The Pattern

```
Running agent process → reads flow_state.json → sees wrong FQ → constitutional HOLD → silent
```

## The Chain (from real incident, 2026-07-29)

```
fq-probe.sh (inverted formula) → FQ=0.5 → flow_state.json → 
  OpenClaw reads → "FQ WATCHING, better HOLD" → 
    send heartbeats only, no execution
```

## What to Check

| Check | Command | What Drift Looks Like |
|-------|---------|----------------------|
| Live FQ (canonical) | `curl -sf :7073/health \| jq .fq` | fq.verdict = BALANCED or OPTIMAL |
| Stale FQ (cron probe) | `cat /root/AAA/state/flow_state.json \| jq .fq, .status` | fq = 0.5, status = WATCHING or STUCK |
| Disagreement magnitude | Compare both | If 5x+ difference = sensor drift confirmed |
| Probe script formula | `cat /root/scripts/fq-probe.sh \| grep "fq ="` | Formula might have inverted numerator/denominator |

## Root Cause

The fq-probe.sh cron script computes FQ with inverted terms:

```python
# WRONG — verify/exec inverted
fq = round((total_verify + 1) / (total_exec + 1), 2)
```

The canonical arifFlow daemon formula:

```
FQ = Σ(execute_cost) / Σ(verify_cost)
```

### Numeric example

With exec=1, verify=0:
- **Wrong formula:** (0+1)/(1+1) = **0.5 → WATCHING** 🚨
- **Correct formula:** execute_cost / verify_cost = **2.5 → BALANCED** ✅

## The Fallout

Every agent that reads `flow_state.json` as its FQ source:
- Sees FQ < 1.0 → constitutional reflex triggers HOLD
- Stops executing, sends heartbeats only
- Admin sees "process running, no work done"
- Root cause appears to be "agent is broken" but it's actually "agent is obeying bad telemetry"

## Fix Options

| Option | Effort | Risk | Durability |
|--------|:-----:|:----:|:----------:|
| **1.** Fix formula in fq-probe.sh | 2 min | Low | Temporary (still dual source) |
| **2.** Agents read arifFlow :7073/health directly | 30 min | Low | Permanent |
| **3.** Both (fix + eliminate dual source) | 32 min | Low | Best |

### Fix 1 — Patch fq-probe.sh

Line 65 in `/root/scripts/fq-probe.sh`:

```python
# Change from:
fq = round((total_verify + 1) / (total_exec + 1), 2)
# To:
fq = round((total_exec + 1) / (total_verify + 1), 2)
```

### Fix 2 — Eliminate dual source

1. Delete `flow_state.json`
2. Remove cron job: `crontab -e` → remove fq-probe line
3. Every agent reads FQ via `curl -sf http://127.0.0.1:7073/health | jq '.fq'`

## Verification

```bash
# Compare both sources after fix
curl -sf http://127.0.0.1:7073/health | jq '.fq.quotient, .fq.verdict'
cat /root/AAA/state/flow_state.json | jq '.fq, .status'
# They should agree within smoothing margin
```

## When to Use This Diagnosis

- Agent process running > 12 hours with no visible output
- Gateway logs show only heartbeat messages (ARTBEAT_OK, BEAT_OK)
- Agent telemetry source reads from a file, not from a live health endpoint
- Agent was working before a restart/reboot then went silent

> Proven in production: 2026-07-29 — OpenClaw (AGI🦞) had PID 1944342 running 2d 22h, 940MB RAM, but only sending heartbeats because flow_state.json showed FQ=0.5 WATCHING while real arifFlow daemon showed FQ=2.5 BALANCED.
