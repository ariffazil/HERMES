---
name: active-response-layer
description: "Full implementation of smoketest + state machine + circuit breaker + rollback"
---

# Active Response Layer Implementation

Deployed on af-forge (2026-07-12). Live production system.

## Architecture

```
systemd timer (60s)
    ↓
vps-watchdog.sh
    ↓
t1-smoketest.sh (dependency-free)
    ↓
State machine (IDLE → OBSERVING → HEALTHY/ROLLBACK → DEAD)
    ↓
Circuit breaker (5 rollbacks/hour → 888_HOLD)
    ↓
Rollback (validate .bak → restore → verify)
```

## Files

| File | Purpose |
|---|---|
| `/usr/local/bin/t1-smoketest.sh` | Health probe (shell, no deps) |
| `/usr/local/bin/vps-watchdog.sh` | State machine + circuit breaker |
| `/etc/systemd/system/vps-t1-check.service` | systemd service unit |
| `/etc/systemd/system/vps-t1-check.timer` | systemd timer (60s, BOOT_GRACE=360s) |
| `/var/lib/arifos/vps-health-state.json` | State file (persistent) |
| `/var/lib/arifos/agi_mode` | AGI mode flag (LOCKED/IDLE) |
| `/var/log/arifos/vps-watchdog.log` | Audit log |

## State Machine Logic

```bash
# In vps-watchdog.sh
case "$STATE" in
  IDLE)
    # First run — bootstrap
    smoketest "$SVC"
    RESULT=$?
    if [ "$RESULT" -eq 0 ]; then
      update_state "HEALTHY"
    elif [ "$RESULT" -eq 1 ]; then
      update_state "OBSERVING"
    else
      update_state "CRITICAL"
      trigger_rollback
    fi
    ;;
  OBSERVING)
    # Transient failure — wait and see
    smoketest "$SVC"
    RESULT=$?
    if [ "$RESULT" -eq 0 ]; then
      update_state "HEALTHY"
      reset_retries
    else
      RETRIES=$((RETRIES + 1))
      if [ "$RETRIES" -ge 3 ]; then
        update_state "CRITICAL"
        trigger_rollback
      fi
    fi
    ;;
  HEALTHY)
    # Normal operation
    smoketest "$SVC"
    RESULT=$?
    if [ "$RESULT" -ne 0 ]; then
      update_state "OBSERVING"
      RETRIES=1
    fi
    ;;
  CRITICAL)
    # Rollback triggered
    trigger_rollback
    ;;
esac
```

## Circuit Breaker

```bash
# Check RETRY_BUDGET before rollback
HOUR_ROLLBACKS=$(jq '.services."'"$SVC"'".hour_rollbacks' "$STATE_FILE")
if [ "$HOUR_ROLLBACKS" -ge 5 ]; then
  log "888_HOLD: RETRY_BUDGET exhausted"
  echo "LOCKED" > /var/lib/arifos/agi_mode
  exit 2
fi
```

## Rollback with Validation

```bash
trigger_rollback() {
  # Pre-rollback log snapshot
  journalctl -u "$SVC" --since "10 minutes ago" > "/var/lib/arifos/log-snapshot-$(date +%s).log"
  
  # Validate .bak before restore
  if [[ "$SERVICE_FILE" == *.service ]]; then
    systemd-analyze verify "${SERVICE_FILE}.bak" || { log "888_HOLD: .bak invalid"; echo "LOCKED" > /var/lib/arifos/agi_mode; exit 2; }
  else
    bash -n "${SERVICE_FILE}.bak" || { log "888_HOLD: .bak syntax error"; echo "LOCKED" > /var/lib/arifos/agi_mode; exit 2; }
  fi
  
  # Restore and restart
  cp "${SERVICE_FILE}.bak" "$SERVICE_FILE"
  systemctl daemon-reload
  systemctl restart "$SVC"
  
  # Verify
  sleep 5
  smoketest "$SVC"
  if [ $? -eq 0 ]; then
    log "ROLLBACK SUCCESS"
    update_state "HEALTHY"
    reset_retries
  else
    ROLLBACKS=$((ROLLBACKS + 1))
    if [ "$ROLLBACKS" -ge 3 ]; then
      log "888_HOLD: 3 rollbacks failed"
      echo "LOCKED" > /var/lib/arifos/agi_mode
      exit 2
    fi
  fi
}
```
