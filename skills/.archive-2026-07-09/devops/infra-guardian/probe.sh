#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  infra-guardian probe — Caddy, SSL, DNS, Cloudflare audit       ║
# ╚══════════════════════════════════════════════════════════════════╝
set -euo pipefail

LOGFILE="/root/.openclaw/logs/infra-guardian.log"
ALERT_LOG="/root/.openclaw/logs/infra-guardian-alerts.log"
mkdir -p "$(dirname "$LOGFILE")"

TS() { date -Iseconds; }
log()  { echo "[$(TS)] $*" >> "$LOGFILE"; }
alert(){ echo "[$(TS)] ALERT: $*" >> "$ALERT_LOG"; echo "[$(TS)] ALERT: $*"; }

DOMAINS="arif-fazil.com openclaw.arif-fazil.com wiki.arif-fazil.com forge.arif-fazil.com geox.arif-fazil.com aaa.arif-fazil.com"
ISSUES=0

log "=== infra-guardian probe start ==="

# ─── 1. Caddy service + config validity ───────────────────────────
if systemctl is-active caddy >/dev/null 2>&1; then
    log "OK: Caddy service active"
else
    alert "CRITICAL: Caddy service not active"
    ISSUES=$((ISSUES + 1))
fi

if caddy validate --config /etc/caddy/Caddyfile >/dev/null 2>&1; then
    log "OK: Caddyfile valid"
else
    alert "CRITICAL: Caddyfile validation failed"
    ISSUES=$((ISSUES + 1))
fi

# ─── 2. SSL cert expiry (Origin CA + Let's Encrypt) ──────────────
for domain in $DOMAINS; do
    expiry=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -n "$expiry" ]; then
        expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null || echo 0)
        days_left=$(( (expiry_epoch - $(date +%s)) / 86400 ))
        if [ "$days_left" -lt 7 ]; then
            alert "CRITICAL: $domain SSL expires in ${days_left}d"
            ISSUES=$((ISSUES + 1))
        elif [ "$days_left" -lt 30 ]; then
            alert "WARNING: $domain SSL expires in ${days_left}d"
            ISSUES=$((ISSUES + 1))
        else
            log "OK: $domain SSL expires in ${days_left}d"
        fi
    else
        log "WARNING: Could not check SSL for $domain"
    fi
done

# ─── 3. DNS resolution parity ─────────────────────────────────────
for domain in $DOMAINS; do
    resolved=$(dig +short "$domain" 2>/dev/null | head -1 || true)
    if [ -n "$resolved" ]; then
        log "OK: $domain resolves to $resolved"
    else
        alert "WARNING: $domain DNS resolution failed"
        ISSUES=$((ISSUES + 1))
    fi
done

# ─── 4. Key origin endpoints reachable ────────────────────────────
for url in "https://arif-fazil.com" "https://openclaw.arif-fazil.com"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
    if [ "$code" = "200" ] || [ "$code" = "301" ] || [ "$code" = "302" ]; then
        log "OK: $url → HTTP $code"
    else
        alert "WARNING: $url → HTTP $code"
        ISSUES=$((ISSUES + 1))
    fi
done

# ─── 5. Cloudflare Origin CA cert files exist ─────────────────────
for cert in /root/.acme.sh/arif-fazil.com_ecc/fullchain.cer /root/.config/caddy/certificates/*.crt; do
    if [ -f "$cert" ]; then
        log "OK: Origin CA cert exists: $cert"
    else
        log "INFO: Origin CA cert not at expected path: $cert"
    fi
done

log "Probe complete. issues=$ISSUES"
