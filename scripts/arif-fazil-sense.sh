#!/bin/bash
# 🜂 Sense — arif-fazil.com Health Probe
# Passive liveness. Silent on GREEN, reports only RED.
# Deployed as cron job db0aa69e0fdc (every 15 min)
#
# 2026-08-04 fix: NEVER use `curl -w '%{http_code}' || echo 000`.
# When curl writes "200" then exits non-zero (partial/CF/timeout),
# the || branch appends "000" → code becomes "200000" (false RED).
# Same class → "000000" when -w already printed 000.
set -euo pipefail

FAILS=0
DIRTY=0

# http_code only — never concatenate fallback onto curl -w output
http_code() {
  local url="$1"
  shift
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$@" "$url" 2>/dev/null) || true
  # Keep first 3 digits only; empty / garbage → 000
  code=$(printf '%s' "$code" | tr -cd '0-9' | head -c 3)
  if [ "${#code}" -ne 3 ]; then
    code="000"
  fi
  printf '%s' "$code"
}

is_ok() {
  case "$1" in
    200|301|302|307|308) return 0 ;;
    *) return 1 ;;
  esac
}

# Check git repo state (guarded — must never kill the probe)
# Only untracked (??) trip DIRTY — modified tracked files are normal forge churn.
cd /root/arif-fazil.com
DIRTY_COUNT=$(git status --porcelain 2>/dev/null | grep -c '^??' || true)
DIRTY_COUNT=${DIRTY_COUNT:-0}
if [ "$DIRTY_COUNT" -gt 0 ]; then
  DIRTY=1
fi

# web_zen doctor — capture exit WITHOUT dying under set -e
# exit=1 = YELLOW warnings only (caddy hints etc.) — bukan fatal
WEBZEN_EXIT=0
WEBZEN_OUT=$(python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py doctor --timeout 15 2>&1) || WEBZEN_EXIT=$?
if [ "$WEBZEN_EXIT" -eq 1 ]; then WEBZEN_EXIT=0; fi

# Organ subdomains — GET + Accept (HEAD is flaky via CF on some paths)
SUBDOMAIN_FAILS=""
for url in \
  https://arifos.arif-fazil.com/health \
  https://geox.arif-fazil.com/health \
  https://wealth.arif-fazil.com/health \
  https://well.arif-fazil.com/health \
  https://aaa.arif-fazil.com/health \
  https://mcp.arif-fazil.com/; do
  code=$(http_code "$url" -H "Accept: application/json,text/html,*/*")
  if ! is_ok "$code"; then
    SUBDOMAIN_FAILS="$SUBDOMAIN_FAILS\n  $url → HTTP $code"
    FAILS=$((FAILS + 1))
  fi
done

# SPA routes — probe as real browser (Accept: text/html) to match Caddy
# @makcikgpt_nojs handler which 404s requests without Accept: text/html.
ROUTE_FAILS=""
for path in / /writing/ /doctrine/ /earth/ /missions/ /world/makcikgpt/ /000/ /999/ /gas/ /geox/ /canon/ /federation/ /connect/ /verify/ /pulse/ /audit/ /wealth/; do
  code=$(http_code "https://arif-fazil.com${path}" -H "Accept: text/html")
  if ! is_ok "$code"; then
    ROUTE_FAILS="$ROUTE_FAILS\n  https://arif-fazil.com${path} → HTTP $code"
    FAILS=$((FAILS + 1))
  fi
done

# Report
# Only fail if >2 route/subdomain failures (single transient = noise),
# or web_zen hard fail, or untracked files left in the site repo.
if [ "$FAILS" -gt 2 ] || [ "$WEBZEN_EXIT" -gt 1 ] || [ "$DIRTY" -eq 1 ]; then
  echo "🔴 Sense FAILURES:"
  if [ "$WEBZEN_EXIT" -ne 0 ]; then
    echo "  web_zen doctor: exit=$WEBZEN_EXIT"
    echo "$WEBZEN_OUT" | tail -5
  fi
  if [ -n "$SUBDOMAIN_FAILS" ]; then
    echo -e "  Subdomains:$SUBDOMAIN_FAILS"
  fi
  if [ -n "$ROUTE_FAILS" ]; then
    echo -e "  Routes:$ROUTE_FAILS"
  fi
  if [ "$DIRTY" -eq 1 ]; then
    echo "  Repo: $DIRTY_COUNT untracked files (commit or gitignore)"
    git status --porcelain 2>/dev/null | grep '^??' | head -10 || true
  fi
  exit 1
fi

# GREEN — silent
exit 0
