# F4 Runtime Monitor — Reasoning Loop Circuit Breaker

## Problem
Agent stuck in reasoning loop: reads same logs, tries same diagnosis, produces same conclusion. CPU/RAM burned with ΔS > 0. No resolution ever arrives.

## Solution
Enforce MAX_CYCLES (3 per session) using md5sum of Ghost JSON as state anchor. When state hasn't changed for 3 consecutive cycles, auto-HOLD.

## Implementation

```bash
#!/bin/bash
# /root/scripts/f4-monitor.sh
MAX_CYCLES=3
STATE_FILE="/var/run/arifos_state.json"
HASH_FILE="/var/run/arif_think_last_hash"
CYCLE_FILE="/var/run/arif_think_cycles"

STATE_HASH=$(md5sum "$STATE_FILE" | awk '{print $1}')
PREV_HASH=$(cat "$HASH_FILE" 2>/dev/null || echo "")

if [ "$STATE_HASH" = "$PREV_HASH" ]; then
  CYCLE_COUNT=$(($(cat "$CYCLE_FILE" 2>/dev/null || echo 0) + 1))
  echo "$CYCLE_COUNT" > "$CYCLE_FILE"
  if [ "$CYCLE_COUNT" -ge "$MAX_CYCLES" ]; then
    echo "🔒 [F4 VIOLATION] REASONING LOOP DETECTED. AUTO-HOLD INITIATED."
    echo "{\"ts\":$(date +%s),\"event\":\"F4_VIOLATION\",\"cycles\":$CYCLE_COUNT,\"max_cycles\":$MAX_CYCLES,\"action\":\"AUTO_HOLD\"}" \
      >> "/root/forge_work/$(date +%Y-%m-%d)/rsi/f4-violations.jsonl"
    exit 1
  fi
else
  echo 0 > "$CYCLE_FILE"
  echo "$STATE_HASH" > "$HASH_FILE"
fi
```

## Key Design Decisions

| Decision | Why |
|----------|-----|
| **md5sum of Ghost JSON** | Deterministic, zero API, zero token tracking. State change = real hash change. |
| **Max 3 cycles** | Mathematical invariant across all models/providers. Enough for triage, not enough for infinite loop. |
| **Reset on `arif_init`** | Every sovereign init gets fresh entropy budget. |
| **RSI violation log** | Every F4 violation is recorded to `forge_work/<date>/rsi/f4-violations.jsonl` for post-mortem analysis. |

## Zero-Token Enforcement
This monitor uses ZERO token tracking. No token counting, no API cost monitoring, no "you've used X tokens" prompts. The user (Arif) absolutely does not tolerate token-based enforcement — he calls it "casino." The system enforces via file checksums and exit codes.

## Triggering
```bash
# Wire into agent-init.sh:
rm -f /var/run/arif_think_cycles /var/run/arif_think_last_hash

# Wire into reasoning pipeline:
bash /root/scripts/f4-monitor.sh || exit 1
```

## Verified
- arifOS federation, af-forge VPS (2026-07-27)
- Cycle counting, zero-delta detection, auto-HOLD all verified
- JSONL log entry confirmed valid
