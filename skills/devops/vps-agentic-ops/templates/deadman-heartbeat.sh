#!/bin/bash
# deadman-heartbeat.sh — Dead-man's switch heartbeat
# Reports VPS vitals. If this stops firing, VPS is down.
# Set up as cron: */30 * * * * /usr/local/bin/deadman-heartbeat.sh

UPTIME=$(uptime -p)
LOAD=$(cat /proc/loadavg | awk '{print $1}')
DISK=$(df / | awk 'NR==2 {print 5}')
RAM=$(free | awk '/Mem:/ {printf("%.0f", $3/$2*100)}')

echo "🫀 heartbeat: up=$UPTIME load=$LOAD disk=$DISK ram=$RAM"
