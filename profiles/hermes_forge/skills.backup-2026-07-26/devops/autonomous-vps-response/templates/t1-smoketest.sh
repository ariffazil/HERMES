#!/bin/bash
# t1-smoketest.sh — Dependency-free VPS Tier-1 smoketest
# Usage: t1-smoketest.sh [service-name] [health-url]
# Exit codes: 0=PASS, 1=FAIL(service dead or url fail), 2=FAIL(watchdog kill detected)
set -euo pipefail

SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"
RET=0

# Step 1: Service is ACTIVE (not just loaded)
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"
  exit 1
fi

# Step 2: Health URL reachable (if provided)
if [ -n "$URL" ]; then
  if ! curl -sf --max-time 5 "$URL" >/dev/null 2>&1; then
    echo "FAIL: $URL unreachable"
    RET=1
  fi
  # Semantic check — not just HTTP 200, but response contains health indicator
  if ! curl -sf --max-time 5 "$URL" 2>/dev/null | grep -qi "healthy\|ok\|ready"; then
    echo "WARN: $URL returned 200 but no health indicator in response"
    RET=1
  fi
fi

# Step 3: No recent watchdog kills in journal
if journalctl -u "$SVC" --since "5 minutes ago" --no-pager -q 2>/dev/null | grep -q "Watchdog timeout"; then
  echo "FAIL: recent watchdog kill detected for $SVC"
  exit 2
fi

echo "PASS: $SVC"
exit $RET
