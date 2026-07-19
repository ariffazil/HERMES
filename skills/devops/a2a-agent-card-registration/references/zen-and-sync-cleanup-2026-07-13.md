# Zen-and-Sync Cleanup — 2026-07-13

## Context
Arif asked to "zen and sync" all agent cards after the Geometry B reorganization (agent-cards/ subdirectory structure vs root-level flat files). Discovered 21 stale root duplicates, two conflicting FI numbering schemes, and a dual-scan-path issue.

## Root Cause
The gateway's `agent-card-registry.js` scans **two paths** recursively:
1. `a2a-server/agent-cards/` (primary)
2. `AAA/agent-cards/` (secondary, CIV-33 canonical)

Both load ALL `.json` files. After reorganizing cards into subdirectories, the old root-level `.json` files remained, causing duplicate registrations.

## Cards Cleaned
**21 root-level duplicates removed:**
- identity/: 333-AGI, 555-ASI, 888-APEX
- functions/: OpenClaw, A-ARCHIVE, A-AUDIT
- extensions/: Hermes-ASI, 777-forge, MakcikGPT
- harnesses/: All 11 CLI tools (opencode through qwen-code)
- Legacy: main.json (arifOS_bot), agy.json (old FI-009)

**Stale secondary scan entries removed:**
- `_retired/` directory (arifOS_bot, prospect-maturation)
- `harnesses/fi-012-antigravity` (duplicate FI number)
- `harnesses/fi-009-agy` (Agy mapped to wrong FI-009, conflict with FI-004)

## Gateway Restart Pitfall
Standard `systemctl restart aaa-a2a.service` fails silently if a stale node process holds port 3001 (EADDRINUSE). Fix:
```bash
lsof -ti:3001 | xargs -r kill -9 2>/dev/null
systemctl restart aaa-a2a.service
```

## Result
- 41 agents, all proto=1.2, all Ed25519 signed
- All organized in correct subdirectories per CIV-333
- Canonical sources in `agents/<name>/agent-card.json`
- Gateway copies in `a2a-server/agent-cards/<subdir>/`
