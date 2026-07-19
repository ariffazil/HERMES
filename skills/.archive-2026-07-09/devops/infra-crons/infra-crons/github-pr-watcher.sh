#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  github-pr-watcher — Federation PR monitor (machine task)       ║
# ║  Replaces Hermes cron job 'GitHub PR Watcher' (deepseek/402)    ║
# ║  Pure shell + gh CLI, no LLM. Runs every 4h.                    ║
# ╚══════════════════════════════════════════════════════════════════╝
set -uo pipefail

LOGFILE="/var/log/github-pr-watcher.log"
ALERT_LOG="/root/.openclaw/logs/github-pr-alerts.log"
STATEFILE="/root/.openclaw/state/github-pr.json"
OUTPUTFILE="/root/.hermes/cron/output/github-pr-watcher.md"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

mkdir -p "$(dirname "$LOGFILE")" "$(dirname "$ALERT_LOG")" "$(dirname "$STATEFILE")" "$(dirname "$OUTPUTFILE")"

log "=== github-pr-watcher start ==="

REPOS=(arifOS AAA A-FORGE geox wealth well apex)
TOTAL=0
NEEDS_REVIEW=0
REPORT_ROWS=""

> "$STATEFILE"

for repo in "${REPOS[@]}"; do
    # gh pr list --json number,title,author,createdAt,isDraft --limit 50
    # use --state open, --jq . for safe extraction
    PR_JSON=$(gh pr list --repo "ariffazil/${repo}" --state open --json number,title,author,isDraft,createdAt 2>/dev/null)
    if [ $? -ne 0 ]; then
        alert "FAIL: gh pr list ${repo} failed (auth/repo?)"
        printf '%s=fail\n' "$repo" >> "$STATEFILE"
        continue
    fi

    PR_COUNT=$(printf '%s' "$PR_JSON" | jq 'length' 2>/dev/null || echo "0")
    DRAFT_COUNT=$(printf '%s' "$PR_JSON" | jq '[.[] | select(.isDraft==true)] | length' 2>/dev/null || echo "0")
    READY=$((PR_COUNT - DRAFT_COUNT))

    TOTAL=$((TOTAL + PR_COUNT))
    NEEDS_REVIEW=$((NEEDS_REVIEW + READY))

    printf '%s=ok_open=%s_draft=%s_ready=%s\n' "$repo" "$PR_COUNT" "$DRAFT_COUNT" "$READY" >> "$STATEFILE"

    if [ "$READY" -gt 0 ]; then
        log "OPEN: ${repo} has ${READY} PR(s) awaiting review (${PR_COUNT} total, ${DRAFT_COUNT} draft)"
        # list first 5 ready PR titles (single quotes for jq -r, no escaped backslash needed)
        REPORT_ROWS="${REPORT_ROWS}\n### ${repo} (${READY} ready)\n"
        REPORT_ROWS="${REPORT_ROWS}$(printf '%s' "$PR_JSON" | jq -r '.[] | select(.isDraft==false) | "- #" + (.number|tostring) + " " + .title + " — @" + .author.login' 2>/dev/null | head -5)\n"
    else
        log "CLEAN: ${repo} no PRs awaiting review"
    fi
done

cat > "$OUTPUTFILE" << EOF
# GitHub PR Watcher
Generated: $(date -Iseconds)

| Repo | Open | Draft | Ready (awaiting review) |
|------|------|-------|-------------------------|
$(grep '=ok_open=' "$STATEFILE" | while IFS= read -r line; do
    # state line example: arifOS=ok_open=11_draft=0_ready=11
    # split on '=', index 1=repo, 2='ok', 3=open N, 4=draft M, 5=ready K
    IFS='=' read -r repo _ openraw draftraw readyraw <<< "$line"
    open=$(printf '%s' "$openraw"  | sed 's/_.*//')
    draft=$(printf '%s' "$draftraw" | sed 's/_.*//')
    ready=$(printf '%s' "$readyraw" | sed 's/_.*//')
    printf "| %s | %s | %s | %s |\n" "$repo" "$open" "$draft" "$ready"
done)

**Total:** ${TOTAL} open · **Needs review:** ${NEEDS_REVIEW}
EOF

if [ "$NEEDS_REVIEW" -gt 0 ]; then
    printf '\n## PRs awaiting review:\n%s\n' "$(printf '%b' "$REPORT_ROWS")" >> "$OUTPUTFILE"
fi

log "github-pr-watcher: ${TOTAL} open, ${NEEDS_REVIEW} need review"
log "=== github-pr-watcher done ==="

# Always exit 0 — this is a watcher, not a gate. Alerts already in alert log.
exit 0
