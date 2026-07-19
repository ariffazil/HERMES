# Stale Research Doc Pattern

> **Origin:** 2026-07-19 — GEOX readiness assessment. User sent a detailed research doc claiming "CRITICAL — Service DOWN, FastMCP 3.4.2 crash loop, 5 restart attempts hit systemd limit." Live state at T₁: service HEALTHY, 24 tools, uptime 2+ min. Fix had landed 3 minutes after the doc's observed window.

## The Pattern

A research/audit/status document is sent for review. It cites specific error messages, commit hashes, service states. It reads authoritative. **It was written against a snapshot that is now stale.**

## Detection Signals

- Document says "CRITICAL", "DOWN", "P0", "crash loop" with systemd-level detail
- Document includes specific error messages (e.g., "Functions with **kwargs are not supported")
- Document was written hours/days ago and references time-bound state
- Document proposes fixes for problems that may already be resolved

## Probe Recipe (before acting on any external status doc)

```bash
# 1. Service health — the only truth
curl -sf http://127.0.0.1:<port>/health | jq '{status, identity, uptime}'

# 2. Systemd status — is it actually restart-looping?
systemctl status <unit> --no-pager -l | head -10

# 3. Journal — error messages from the doc still appearing?
journalctl -u <unit> --since "2 hours ago" --no-pager | grep -iE "error|crash|fail" | tail -5

# 4. Git log — did someone already fix it?
git log --oneline -5 && git log --since="<doc-timestamp>" --oneline

# 5. Public surface — external validation
curl -sf -o /dev/null -w "HTTP %{http_code}" https://<domain>/health
```

## The Rule

**Never relay a status doc's CRITICAL/DOWN finding without probing live state first.** The cost of probing: 15 seconds. The cost of relaying stale alarm: lost credibility + wasted attention + the user having to tell you "that was already fixed."

## GEOX Case (2026-07-19)

| What the doc said | Live state at T₁ |
|---|---|
| "CRITICAL — Service DOWN" | `status: healthy`, 24 tools |
| "FastMCP 3.4.2 crash loop" | Fixed by commit `d409cac2` |
| "Start request repeated too quickly" | No restart events in 2+ hours |
| "Fix: pin FastMCP to <3.0" | Wrong fix — actual fix was removing deprecated **kwargs wrappers |

The doc was not wrong — it was **written against a snapshot** that was true when observed. But by the time it reached the agent, reality had moved.
