---
name: federation-config-reconciliation
description: Reconcile split-brain truth sources in a multi-organ federation — when arifOS capability_map, Hermes config.yaml providers block, MCP server registry, and runtime env all claim to be the canonical source for "what's configured". Load when Arif reports "Hermes says 1 provider, arifOS says 28", when a tool call fails with unknown provider, or when fixing audit findings about API key / model / organ coverage.
tags: [federation, reconciliation, capability-map, providers, split-brain, drift]
triggers:
  - "providers don't match"
  - "capability map drift"
  - "split brain"
  - "reconcile configs"
  - "tool not registered"
  - "which source of truth"
  - "arifOS sees X, Hermes sees Y"
---

# Federation Config Reconciliation

## The Problem

In a sovereign federation (arifOS kernel + N organ MCPs + Hermes gateway), configuration truth lives in **multiple surfaces simultaneously**:

| Surface | Lives at | Owns |
|---------|----------|------|
| arifOS capability_map | `/health` endpoint payload, `arifosmcp/runtime/capability_map.py` | Server identity, providers, storage, ops, substrates |
| Hermes config.yaml `providers:` | `~/.hermes/config.yaml` | CLI `/model` picker, model fallback chain |
| Hermes config.yaml `mcp_servers:` | `~/.hermes/config.yaml` | MCP server URLs, transport, tool count |
| Runtime env vars | `~/.hermes/.env` | API keys (the secrets themselves) |
| Tool registry | arifOS `tool_registry.json` (live wire surface count) | Canonical tool list |

When these drift, symptoms appear:
- Hermes `/model` picker shows a model that arifOS `arif_route` rejects
- `arif_route` routes to an organ whose port is dead
- API key in `.env` but provider not in `providers:` block → can't pick from CLI
- Tool count differs across `hermes status`, `arifOS /health`, and runtime ps

## When to Load This Skill

- **Audit reports surface provider/key count anomalies** ("1/17 keys configured", "arifOS capability_map shows 28 providers")
- **Tool call fails with "unknown provider"** or "no route to organ"
- **Reconciliation needed between arifOS capability_map and Hermes providers block**
- **Adding a new model/provider/organ** — which surface to update first?

## The Reconciliation Workflow (proven 2026-07-04 pattern)

### Phase 1 — Inventory all surfaces

```bash
# Surface 1: arifOS capability_map (via /health)
curl -sf -m 5 http://localhost:8088/health | jq '.capability_map.providers'
# Returns: {anthropic: configured, deepseek: configured, sea_lion: configured,
#           minimax: configured, brave: configured, jina: configured, ...}

# Surface 2: Hermes providers block
python3 -c "import yaml; c=yaml.safe_load(open('/root/.hermes/config.yaml')); print(list(c.get('providers',{}).keys()))"

# Surface 3: Hermes mcp_servers block
python3 -c "import yaml; c=yaml.safe_load(open('/root/.hermes/config.yaml')); print(list(c.get('mcp_servers',{}).keys()))"

# Surface 4: env keys
grep -E "^[A-Z_]+_API_KEY|^[A-Z_]+_TOKEN" /root/.hermes/.env 2>/dev/null | cut -d= -f1

# Surface 5: live process / port map
ss -tln 2>/dev/null | grep -E ":(8088|7072|8081|18082|18083|18789|3001|18086)\s" | awk '{print $4}'
```

### Phase 2 — Diff and classify

Build a table:

| Provider/Organ | arifOS map | Hermes providers | Hermes mcp_servers | env key | Live port | Drift? |
|----------------|-----------|------------------|---------------------|---------|-----------|--------|
| GEOX | ✅ | (n/a — not in providers) | ✅ :8081 | (n/a) | ✅ | aligned |
| OpenAI | ❌ | ✅ | (n/a) | ✅ | (n/a) | Hermes-only |
| arifOS | ✅ | (n/a) | ✅ :8088 | (n/a) | ✅ | aligned |
| Hermes MCP | ❌ | (n/a) | ❌ (until wired) | (n/a) | ✅ :18086 | orphan |

**Drift classes:**
- **Hermes-only**: configured in Hermes but arifOS capability_map doesn't know → arif_route won't route to it
- **arifOS-only**: in capability_map but Hermes config doesn't reference it → can't pick from `/model`
- **Orphan port**: listening but no config entry on either side → zombie
- **Dead reference**: in config but port dead → routing fails

### Phase 3 — Pick the canonical source

For each drift class, decide:
- **Provider truth:** `arifOS capability_map` is canonical for organ routing. Hermes `providers:` is canonical for CLI picker visibility
- **API key truth:** env vars (`.env`) are canonical for secrets
- **MCP server truth:** `mcp_servers:` block in config.yaml (or arifOS-managed for organ MCPs)
- **Tool count truth:** live `arifOS /health` `tools_loaded` field

### Phase 4 — Write the reconciliation

```bash
# If a new provider needs to appear in Hermes picker:
python3 << 'PY'
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg.setdefault('providers', {})['new-provider-name'] = {
    'name': 'Human-Readable Name',
    'api': 'https://api.example.com/v1',
    'key_env': 'PROVIDER_API_KEY',
    'transport': 'openai_chat',
    'models': [{'id': 'model-id', 'name': 'Model Display Name'}],
}
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
PY

# If an MCP server needs to be wired:
cfg.setdefault('mcp_servers', {})['server-name'] = {
    'url': 'http://127.0.0.1:<port>/mcp',
    'transport': 'streamable-http',
    'description': 'What this server provides',
}
```

### Phase 5 — Verify with live probes

```bash
# Verify the new provider appears in CLI picker
hermes model  # should list new model

# Verify the new MCP server connects
curl -sf -m 5 http://127.0.0.1:<port>/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 500

# Verify arifOS knows about it (if it's an organ)
curl -sf -m 5 http://localhost:8088/health | jq '.capability_map.providers'
```

## Critical Pitfalls (proven 2026-07-04)

### 1. arifOS capability_map != Hermes providers list

On a multi-provider install, arifOS may have 28 providers configured in its capability_map (because the server-side capability surface includes org-wide defaults), while Hermes config only lists 4 explicit providers (because Hermes explicitly overrides/picks a subset for its user-facing `/model` menu). Both can be correct for their purpose. **The reconciliation question is not "which is right" but "does arif_route route to organs that Hermes can pick"**.

**Probe:** `curl :8088/health | jq '.capability_map.providers'` vs `python3 -c "import yaml; list(yaml.safe_load(open('/root/.hermes/config.yaml'))['providers'])"`. If arifOS has X but Hermes doesn't list X for `/model`, that's expected — X is server-side capability, not user picker option.

### 2. Bot token in env != bot token wired in config

Hermes has `telegram.bot_token_env: ASI_ARIFOS_BOT_TOKEN` in config.yaml. But the actual token value lives in `/root/.hermes/.env` as `ASI_ARIFOS_BOT_TOKEN=<prefix>...`. **The env var name is the bridge; the env file is the secret store.** Don't paste the token value into config.yaml — that creates a credential leak in version control.

**Probe:** `grep "ASI_ARIFOS_BOT_TOKEN" /root/.hermes/.env 2>/dev/null | head` to confirm env var is set; never read the value itself.

### 3. stdio MCP orphans stay in `mcp_servers.json` even after disabled

If you add a server to `agent.disabled_toolsets` to quarantine, the entry in `mcp_servers.json` (if present) may still spawn a zombie process if the gateway reads from there too. **Always probe `ps aux` after quarantine** to confirm the subprocess actually died:

```bash
ps aux | grep -i "<stdio-mcp-name>" | grep -v grep | wc -l
```

If still > 0, the server is being spawned from a different config source (Claude config dir, mcp.json, etc.). Check those too.

### 4. OpenCode plugin hardcodes base_url

`opencode-go` provider in Hermes config has `base_url: https://opencode.ai/zen/go/v1` hardcoded. If you change `key_env`, the URL stays fixed. Don't try to override URL via provider config — the plugin ignores it. To redirect, change the actual plugin source or use a different provider key.

### 5. Nous Portal login creates a new provider entry automatically

When you run `hermes portal`, on success Hermes auto-creates a `nous-portal` provider entry pointing at `https://portal.nousresearch.com/api/v1`. **You don't need to manually add it.** If you pre-added a stub like the one in this session, that's fine — it just gets overwritten with the live config on first login.

### 6. Case-fix overrides: what looks like drift may be deliberate

When systemd `WorkingDirectory` or `ExecStart` points to a path that disagrees with AGENTS.md (e.g., systemd uses `/root/GEOX` but AGENTS.md says `/root/geox` is canonical), **do not immediately flag as critical drift.** Check for override conf files that document the discrepancy:

```bash
ls /etc/systemd/system/<service>.service.d/
grep -l "case\|capital\|workdir" /etc/systemd/system/<service>.service.d/*.conf
```

Real example (2026-07-20): `geox-mcp.service` points to `/root/GEOX` (uppercase) but AGENTS.md says `/root/geox` (lowercase) is canonical. The override `path-geox-casefix.conf` (dated 2026-07-12) explicitly documents: *"live tree is /root/GEOX (case). /root/geox path absent → restart would fail."* This is a deliberate workaround, not drift. Both paths had independent git repos — uppercase was operational, lowercase aspirational.

**Rule:** Before re-pointing any systemd path based on AGENTS.md claims, check: (1) override files for documentation explaining the choice, (2) whether both paths exist with independent git repos, (3) `git log --oneline -3` in both to identify the live working tree. Only flag as drift if NONE of these explain the discrepancy. The AGENTS.md declaration may be aspirational; the systemd config is operational.

### 7. TokenRouter model name diverge by component — not necessarily drift

When each component in the chain uses a different default model (`deepseek-v4-pro` in Hermes primary, `gemini-3.5-flash` in arifOS LLM client via env override, `MiniMax-M3` in fallback), this is usually by design — not a consensus failure. Check for env var overrides before flagging:

```bash
# arifOS LLM client default vs actual
grep 'TOKENROUTER_MODEL' /root/.secrets/tokenrouter.env
grep 'DEFAULT_MODEL\|cfg\[.model.\]' /root/arifOS/arifosmcp/runtime/llm_client.py | head -5
```

The env var in `/root/.secrets/tokenrouter.env` overrides the code default. What looks like drift (code says `MiniMax-M3`, reality uses `gemini-3.5-flash`) is correct env-var-based configuration. Only flag divergence when comparing ALL surfaces — code defaults, env overrides, and config.yaml blocks — and none agree.

## Standard Reconciliation Receipt

When reporting reconciliation work to Arif, deliver a compact diff table:

| Surface | Before | After | Drifts Closed |
|--------|--------|-------|---------------|
| Hermes `providers:` | 4 entries | 5 (added `nous-portal` stub) | 0 (stub, login creates real) |
| Hermes `mcp_servers:` | 6 servers | 7 (added `hermes` :18086) | 1 (hermes MCP now wired) |
| arifOS `capability_map.providers` | 28 | 28 | 0 (unchanged) |
| Live port map | 6 | 7 | 1 (hermes now listening via 18086) |

Then one sentence on next action ("after `hermes portal` login, provider count moves to 5 live").

## Cross-References

- `references/registry-drift-patterns.md` — Drift classes, enforcement script patterns, pitfalls (forged 2026-07-05)
- `references/multi-organ-version-drift-scan.md` — Cross-organ version freshness, systemd path audit, and TokenRouter model consensus scan pattern (forged 2026-07-20)
- `/root/AAA/docs/FEDERATION-SUBSTRATE-RULES.md` — Federation Substrate Partitioning Rules (canonical write paths, naming contract, ACL, enforcement)
- `measure-before-acting/SKILL.md` — Failures 6, 10. Read this skill first; never propose reconciliation without measuring both sides first
- `federation-organ-liveness-probe/SKILL.md` — Pitfalls 23-25. Stdio MCP quarantine + gateway restart patterns
- `hermes-provider-setup/SKILL.md` — How to add a single provider to the picker
- `mcp-server-building/SKILL.md` — How to build and wire a new MCP server
- `/root/AGENTS.md` §11 — Federation organs, must-never-become compass

## Provenance

Forged 2026-07-04 from live session. Triggered by audit report showing "Only 1/17 API keys configured" while arifOS capability_map showed 28 providers configured. The reconciliation surfaced three actionable gaps (Hermes MCP wiring, Nous Portal login, stdio MCP quarantine) — all closed in the same session without kernel rebuild.