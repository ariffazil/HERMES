# AAA Agent-Card Discovery Fix — 2026-08-05

Session detail behind the registry section in SKILL.md. The last open horizon after
the gateway identity reconciliation: cards existed on disk but were invisible to discovery.

## Symptom

- `/root/AAA/agents/*/agent-card.json` held 13 warga cards (hermes, hermes-asi, openclaw,
  forge-bot, 777-forge, 333-AGI, 555-ASI, 888-APEX, makcikgpt, agentic-trading-companion, ...)
- `/.well-known/agents.json` had 29 cards but `hermes` & `forge-bot` = `false` in the registry
- `/api/agents` listed only 8 coding-CLI agents (opencode, codex, claude-code, qwen-code...)

## Root cause

`/root/AAA/a2a-server/agent-card-registry.js` `autoLoad()` scanned only 2 roots:
1. `a2a-server/agent-cards/` (legacy, symlinks → CIV-33) — 31 cards
2. `AAA/agent-cards/` (canonical CIV-33) — 12 cards

The warga cards in `/root/AAA/agents/*/` were never scanned. **Registry ready: 37 cards** after fix
(was 29 in discovery).

## Patch (verified live)

Insert after the CIV-33 scan block in `autoLoad()`:

```js
// Tertiary scan: warga agent cards at /root/AAA/agents/*/agent-card.json
const wargaRoot = path.resolve(__dirname, '..', 'agents');
if (fs.existsSync(wargaRoot) && path.resolve(wargaRoot) !== path.resolve(defaultDir) && path.resolve(wargaRoot) !== path.resolve(civ33Root)) {
  console.log(`[agent-card-registry] Scanning warga agent cards: ${wargaRoot}...`);
  const wargaResult = loadDirectoryRecursive(wargaRoot);
  console.log(`[agent-card-registry] Warga scan added/refreshed ${wargaResult.loaded.length} cards`);
  // warn on wargaResult.errors.slice(0,5) ...
}
```

`loadDirectoryRecursive` recurses subdirs and registers any JSON with
`agentId || id || (identity && identity.organId)` — no filename filter needed.

## Endpoint semantics (don't confuse)

| Endpoint | Registry | Shape | Meaning |
|---|---|---|---|
| `:3001/api/agents` | lifecycle (NATS) | `{ok, count, agents:[{agentId, instanceId, state...}]}` | runtime organs/CLI agents, federation bootstrap re-registers them |
| `:3001/.well-known/agents.json` | card registry | `{agents:[{id, name, url, skills...}], total}` | **generated from agent-card-registry.js** — this is the acceptance endpoint |

**JSON gotcha:** well-known uses `agents[].id`, NOT `agentId`. Querying `.agents[].agentId`
returns empty and looks like a failed fix. Use `.agents[].id` or `.total`.

## Cosmetic errors

Scanning `agents/` also grabs non-card JSON: `identity.json` in `_brief/`, `_docs/`,
`_external/`, `_lanes/`, `decisions/` → 27 "no identifiable agent ID" warnings at startup.
Harmless — org identity files, not cards. Check first 5, move on.

## Source ↔ runtime parity

- `aaa-a2a.service` ExecStart = `/usr/bin/node /root/AAA/a2a-server/server.js` → patch to
  source dir is live on restart (no /opt copy involved for THIS unit).
- `/opt/aaa/app/a2a-server/agent-card-registry.js` is a parity copy (Jul 17, stale).
  After patching: `cp` source → /opt copy, `diff -q` to confirm IDENTICAL (deploy doctrine).

## Procedure that worked

1. `cp agent-card-registry.js agent-card-registry.js.bak.$(date +%Y%m%d-%H%M%S)` (F1)
2. patch tertiary scan → `systemctl restart aaa-a2a` (T1, single service)
3. verify: `journalctl -u aaa-a2a | grep -E "Warga|Registry ready"`
4. acceptance: `curl -s :3001/.well-known/agents.json | jq '.total'` → 37
5. parity: cp to /opt + diff -q
6. `git -C /root/AAA commit` (Wajib secret gate passed)

## Commit

`68efca58` on AAA/main: "fix(a2a): scan warga agents/ cards in registry discovery"
(+ `docs/GATEWAY_CONFIG_HOMES.md` canon note in same commit).

*DITEMPA BUKAN DIBERI — sealed 2026-08-05.*
