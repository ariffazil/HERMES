#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  session-memory-consolidation — Hourly essence extraction   ║
# ║  Script-only. No LLM. Extracts session summaries to file.    ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/var/log/session-memory-consolidation.log"
RECENT_FILE="/root/.hermes/memories/arif-recent.md"
SESSION_OUTPUT="/root/.hermes/cron/output/"
MAX_LINES=200

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$RECENT_FILE")"

log "=== session-memory-consolidation start ==="

# Find most recent session output files
recent_files=$(find "$SESSION_OUTPUT" -name "*.md" -newer /tmp/last-consolidation 2>/dev/null | head -5)

if [ -z "$recent_files" ]; then
    log "No new session files since last run"
    touch /tmp/last-consolidation
    exit 0
fi

consolidated=0
for f in $recent_files; do
    fname=$(basename "$f")
    # Extract date, topic from filename
    if [[ "$fname" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        date_part="${BASH_REMATCH[1]}"
        # One-line summary: date | (topic derived from filename) | status
        entry="${date_part} | session | $(date -r "$f" +%H:%M) | output file: $fname"
        echo "$entry" >> "$RECENT_FILE"
        consolidated=$((consolidated + 1))
    fi
done

log "Consolidated $consolidated session files to $RECENT_FILE"

# Prune if too long
line_count=$(wc -l < "$RECENT_FILE" 2>/dev/null || echo "0")
if [ "$line_count" -gt "$MAX_LINES" ]; then
    tail -n $((MAX_LINES / 2)) "$RECENT_FILE" > /tmp/arif-recent-pruned.md
    mv /tmp/arif-recent-pruned.md "$RECENT_FILE"
    log "Pruned to $((MAX_LINES / 2)) lines"
fi

touch /tmp/last-consolidation
log "=== session-memory-consolidation done ==="
