# Forge Fault Fix Flow

> Compact diagnostic + repair protocol for A-FORGE failures. Merges systematic debugging (4-phase) with forge-specific architecture: ArifJudge, Pre-Execution Gate, GodelLock, arifSeal, WM instrumentation.

## Phase 0: T₁ Probe (30s)

```bash
# Federation pulse
for svc in arifos:8088 aforge:7071 aforge-mcp:7072 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done

# Forge-specific
curl -s http://127.0.0.1:7072/health | python3 -m json.tool
journalctl -u a-forge-mcp --since "5 min ago" --no-pager | grep -iE "error|fail|deny"

# Orphan processes (stale subagent sessions)
ps aux | grep -E "github-mcp-server|kimi|opencode" | grep -v grep
```

Rule: >1 `github-mcp-server` process → stale subagent sessions. Kill orphans first.

## Phase 1: Root Cause (5-15 min)

1. **Read full error** — especially `_epistemic` block and `constitutional_floor` field
2. **Reproduce** with tight loop — one `curl` to `:7072/mcp` or direct `node -e "..."`
3. **Check git diff** — `git diff HEAD~1`, `git log --oneline -5`
4. **Trace data flow** through gates: ArifJudge → Pre-Execution Gate → GodelLock → execute → ArifSeal

## Forge-Specific Fault Map

| Symptom | Most Likely Root | Check |
|---------|-----------------|-------|
| `POLICY_GATE: L1_AUTHORITY` | No session_id, or session expired | `arif_init()` not called, or session timed out |
| `HARD_DENY` / `GODEL_LOCKED` | Self-modifying command on protected path | Check `godelLock.ts` path scoping |
| `AUTHORITY_REJECTED` | arifOS session invalid | `curl :8088/api/observatory/v1/ready` |
| `auth failed` / `403` | TokenRouter key missing or expired | `source /root/.secrets/vault.env` |
| `Cannot find module` | Build stale, `dist/` mismatch | `npm run build` |
| `Block-scoped variable used before declaration` | Sibling subagent conflict | Re-read file, fix merged variable ordering |
| `ENOENT: ... world-model` | WM log directory missing | `mkdir -p /root/.local/share/arifos/world-model` |
| `tools/list` count ≠ expected | Fingerprint drift or tool not registered | Check `core.ts` registration call, restart service |

## The Rule of Three

| Attempts | Action |
|----------|--------|
| 1–2 failures | Return to Phase 1, re-analyze |
| **3+ failures** | **STOP. Question architecture.** The pattern itself is wrong. |

## Phase 4: Fix + Verify

```bash
cd /root/A-FORGE && npm run build           # zero errors required
systemctl restart a-forge-mcp && sleep 3
curl -s http://127.0.0.1:7072/health | python3 -m json.tool
# Re-run the tight loop from Phase 1b — must go GREEN
npm test 2>&1 | tail -20                     # no regressions
```

## Common Quick Fixes

| Problem | Fastest Fix |
|---------|------------|
| Build fails after patching | Re-read file first (sibling subagent conflict), verify imports exist on disk |
| MCP tool not appearing | Check `registerXxxTools(server)` call in `core.ts`, rebuild, restart |
| arifOS kernel unreachable | `systemctl status arifos`, check `:8088/api/observatory/v1/ready` |
| WM directory missing | `mkdir -p /root/.local/share/arifos/world-model` |
| TokenRouter auth error | `source /root/.secrets/vault.env` |
| Stale orphan processes | `pkill -f github-mcp-server` then restart affected service |

## Key Architecture Touch Points

- **`src/interfaces/mcp/shell/forgeShell.ts`** — canonical governed shell (PRIMAL SHELL)
- **`src/interfaces/mcp/shell/arifJudge.ts`** — DENY/GATE/ALLOW classification (does NOT adjudicate)
- **`src/interfaces/mcp/shell/arifSeal.ts`** — SHA-256 hash-chain ledger
- **`src/interfaces/mcp/shell/godelLock.ts`** — path-scoping locks, NEVER bypass
- **`src/domain/governance/worldModel.ts`** — WM types, hashes, surprise scoring (canonical)
- **`src/interfaces/mcp/wmQueryTools.ts`** — forge_wm_stats, forge_wm_gaps, forge_wm_quality
