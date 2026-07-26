#!/bin/bash
# t1-smoketest.sh — Dependency-free VPS Tier-1 smoketest
# Usage: t1-smoketest.sh [service] [health-url]
# Exit codes: 0=PASS, 1=DEGRADED, 2=CRITICAL
# Customize: change defaults below for your service

set -euo pipefail

SVC="${1:-1mcp.service}"
URL="${2:-http://127.0.0.1:3050/health}"

FAIL=0

# Step 1: Service is ACTIVE
if ! systemctl is-active "$SVC" >/dev/null 2>&1; then
  echo "FAIL: $SVC not active"
  exit 1
fi

# Step 2: Health URL reachable + content validation
if [ -n "$URL" ]; then
  RESPONSE=$(curl -sf --max-time 5 "$URL" 2>/dev/null || echo "FAIL")
  if echo "$RESPONSE" | grep -q "FAIL"; then
    echo "FAIL: $URL unreachable"
    ((FAIL++)) || true
  fi
  # Content validation — check for expected string
  if ! echo "$RESPONSE" | grep -qE '"status"|"healthy"|"ok"'; then
    echo "WARN: $URL unexpected response"
    ((FAIL++)) || true
  fi
fi

# Step 3: VPS vitals
RAM_PCT=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')
DISK_PCT=$(df / | awk 'NR==2 {gsub(/%/,""); print $5}')

[ "$RAM_PCT" -gt 85 ] && echo "WARN: RAM ${RAM_PCT}%" && ((FAIL++)) || true
[ "$DISK_PCT" -gt 90 ] && echo "WARN: Disk ${DISK_PCT}%" && ((FAIL++)) || true

# Exit codes
[ "$FAIL" -eq 0 ] && exit 0
[ "$FAIL" -le 2 ] && exit 1
exit 2
