# WELL SOT Inventory — Worked Example (2026-07-13)

This is a detailed session trace showing the federation-sot-inventory methodology applied to `/root/WELL`. Use it as a pattern reference for future SOT inventories on other federation organs.

## Context

| Property | Value |
|----------|-------|
| Target | `/root/WELL` |
| Organ role | REFLECT_ONLY — Human Readiness Mirror |
| MCP port | 18083 |
| Active branch | `zen-migration-2026-07-11` |
| HEAD | `765cf92` |

## Key Discrepancies Found

### 1. Tool Count Mismatch (HIGH)
- **Documented:** 22 tools (21 canonical + 1 deprecated)
- **Live:** 29 tools exposed via MCP tools/list
- **Root cause:** SOMATIC_TOOLS set grew with ZEN extensions but TOOL_SURFACE.md, CONTEXT.md, INVARIANTS.md were not updated

### 2. Running Server != Repo HEAD (HIGH)
- Health endpoint returned fields (`status`, `final_authority`, `tool_count`) not present in `server.py` at HEAD `765cf92`
- The running `well.service` was built from a different commit or branch

### 3. Cross-Organ Data Leakage (MEDIUM)
- `data/vault999.jsonl` contained 5 `WEALTH_SESSION_INIT` events from the WEALTH organ
- These had `actor_id: "wealth-agent"` and `intent: "economic-analysis"` — clearly WEALTH territory

### 4. Duplicate APEX Bridge Section (MEDIUM)
- 7-line block at README.md lines 54-63 and 103-109 — identical text

### 5. Mislocated Files (LOW)
- `TOOL_SURFACE.md` referenced at repo root but at `scripts/governance/TOOL_SURFACE.md`
- `FEDERATION_CONTRACT.md` referenced at repo root but at `scripts/governance/FEDERATION_CONTRACT.md`

## Commands Used

```bash
# Git state
cd /root/WELL && git log --oneline -1 && echo "---BRANCH---" && git branch -a && echo "---STATUS---" && git status --short

# Health endpoint
curl -s http://127.0.0.1:18083/health | python3 -m json.tool

# MCP tools/list
curl -s -X POST http://127.0.0.1:18083/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Count unique SOMATIC_TOOLS entries
grep -c '"well_' /root/WELL/server.py | head -1
```

## Language Audit Summary

| Pattern | Matches | Verdict |
|---------|---------|---------|
| 'quantum' | 15 | ✅ Domain-correct (3-tier diagnostic model) |
| 'diagnos*' | 191 | ✅ All in guardrail context ("does NOT diagnose") |
| 'self-certif*' | 0 | ✅ Clean |

## Output Report

The full inventory was written to `/root/WELL/SOT-INVENTORY-2026-07-13.md`.
