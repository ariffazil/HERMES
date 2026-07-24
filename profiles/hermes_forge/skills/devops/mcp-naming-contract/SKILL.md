---
name: mcp-naming-contract
description: Apply the MCP Tools/Prompts/Resources naming contract when designing or auditing tool surfaces. The LLM discovers and invokes tools by name + description alone — name and description are the interface contract, not metadata. Load when authoring a new MCP tool/resource/prompt, when auditing an organ's tool surface for "silent misfires", when renaming existing tools, or when Batch N + 1 tools in a federation disagree on naming convention. Triggers include "name this tool", "audit the MCP surface", "tool description", "tool misfires", "agent picks the wrong tool", "silent misfire", "MCP spec naming", or any task touching arifOS/GEOX/A-FORGE/WEALTH/WELL/AAA/Hermes tool or prompt registries.
version: 1.0.0
author: Hermes-PRIME
created: 2026-07-09
tags: [mcp, naming, tools, prompts, resources, interface-contract, model-briefing, naming-laws]
license: MIT
---

# MCP Naming Contract

## The Prime Truth

> **Naming in MCP is not metadata. It is the interface contract between your server and agentic intelligence.**

The LLM never sees your code. It never sees your README. It sees `name + description` and nothing else. If the description is vague, the model misfires — picks wrong tool, fills wrong arguments, or skips the tool entirely. No error is thrown. The system just produces wrong output.

**This is silent misfire territory. Naming matters more than any other tool surface decision.**

## When to load

- Designing a new MCP tool, resource, or prompt — name + description is the first decision
- Auditing an organ's tool surface for "agent picks wrong tool / fills wrong args" complaints
- Renaming an existing tool (governance mutation: breaks every cached plan that references it)
- Batch N + 1 federation tools disagree on naming convention (canonical vs discoverable names)
- Any "model keeps hallucinating arguments for tool X" report

## The 5 Laws (Arif, 2026-07-09)

### Law 1 — `name` is a machine contract. Never change it.

Once published, renaming breaks every agent, every workflow, every cached plan that references it. Treat it like a database column name. **If you must rename, treat it as a governance mutation: deprecate old, add new, version both, run the migration cycle.**

### Law 2 — `description` is the model's only briefing

The model never sees your code. It never sees your README. It sees `description` — and nothing else. If the description is vague, the model will misfire, hallucinate arguments, or skip the tool entirely.

**Length heuristics (Arif's standing rule):**
- < 30 chars: vague. Model will likely skip or guess.
- 30-300 chars: typical. Specific verbs + concrete nouns + one example.
- > 500 chars: bloated. Model may miss the load-bearing info.

### Law 3 — `title` (human) and `name` (machine) must diverge deliberately

```
name:  "query_macrostrat_columns"     ← machine, stable, snake_case
title: "Macrostrat Geological Columns" ← human, readable, can change
```

`name` is what the model calls. `title` is what Cursor / ChatGPT / IDE shows in their panel. They serve different audiences. Conflating them is a category bug.

### Law 4 — Argument names are semantic, not syntactic

```python
# Wrong — model doesn't know what this means
def query(p1: float, p2: float): ...

# Right — model fills these correctly from user intent
def query(latitude: float, longitude: float): ...
```

`p1, p2, x, y, foo, bar` are **always wrong**. The model pattern-matches argument names from the schema to fill them from user intent. Semantic names = correct fills. Syntactic names = hallucinations.

### Law 5 — Prompt names are user vocabulary

```
/analyse-well-log            ← matches the geologist's mind
/load_las_curve_engine_v2    ← matches your codebase, NOT the user
```

The user types `/this-exact-name`. Match how the domain expert thinks, not how your codebase is organised. The completion API reads `arguments[].description` to drive autocomplete — every field is part of the model-facing interface.

## Tool / Resource / Prompt field-by-field

### Tools

| Field | Role in agentic intelligence |
|---|---|
| `name` | Unique identifier — the model calls this exactly. Wrong name = wrong invocation. |
| `title` | Human display only — Cursor shows this, model ignores it. |
| `description` | The model's decision surface — it reads this to decide whether to call the tool. |
| `inputSchema.description` | Per-parameter intent — model uses this to fill arguments correctly. |
| `inputSchema.properties` | Argument NAMES (Law 4) — semantic, not syntactic. |

### Resources

| Field | Role |
|---|---|
| `name` | Machine identifier — used in URI resolution. |
| `title` | Host UI display — what Cursor shows in the panel. |
| `description` | Host uses this to decide whether to inject into context. |
| `uri` | The address — must be unambiguous, no collisions. |

### Prompts

| Field | Role |
|---|---|
| `name` | Unique identifier — user types `/this-exact-name`. |
| `title` | What appears in the slash command menu. |
| `description` | Tells the user what the prompt does before they trigger it. |
| `arguments[].description` | Drives autocomplete — completion API reads this. |

## Audit procedure (when "tool misfires" report lands)

Run this in parallel against the live MCP wire:

```python
import json, urllib.request

# 1. Initialize (required first)
req = urllib.request.Request("http://localhost:<port>/mcp",
    data=json.dumps({"jsonrpc":"2.0","method":"initialize",
        "params":{"protocolVersion":"2025-11-25","capabilities":{},
                  "clientInfo":{"name":"audit","version":"1.0"}},"id":1}).encode(),
    headers={"Content-Type":"application/json",
             "Accept":"application/json, text/event-stream"},
    method="POST")
sid = urllib.request.urlopen(req, timeout=10).headers.get("mcp-session-id")

# 2. tools/list
req2 = urllib.request.Request("http://localhost:<port>/mcp",
    data=json.dumps({"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}).encode(),
    headers={"Content-Type":"application/json",
             "Accept":"application/json, text/event-stream",
             "mcp-session-id": sid},
    method="POST")
tools = json.loads(urllib.request.urlopen(req2, timeout=10).read())["result"]["tools"]
```

Then apply the 5 laws and tabulate:

| Law | Check | Severity |
|---|---|---|
| 1 | All names snake_case, no uppercase, no spaces | HIGH (model-mismatch risk) |
| 2 | Every description has verbs + concrete nouns, length 30-500 | HIGH (vague = silent misfire) |
| 3 | Every name has both `name` and `title` set, they differ deliberately | LOW (cosmetic) |
| 4 | All argument names are semantic (no p1/x/foo/bar) | HIGH (hallucination risk) |
| 5 | Every prompt name matches domain vocabulary, not codebase | MEDIUM (UX risk) |

## Federation-level application (confirmed 2026-07-10 — always probe before citing)

| Organ | Port | Tool Count | Live Verified |
|---|---|---|---|
| arifOS kernel | 8088 | 12 | ✅ `curl :8088/tools` |
| WEALTH | 18082 | 7 (capital_*) | ✅ `curl :18082/tools` |
| WELL | 18083 | 18 (well_*) | ✅ `curl :18083/tools` |
| GEOX | 8081 | 16 canonical | ✅ MCP surface |
| A-FORGE | 7071 | forge_* | ⚠️ not probed live |
| AAA | 3001 | gateway/A2A router | ✅ |
| APEX | 3002 | **DECOMMISSIONED 2026-06-27** | — |

**Tool counts from docs are unreliable — always probe the live surface.** The 2026-07-08 sweep found doc claims often disagree with `curl :<port>/tools`. Precedence: live HTTP probe > VAULT999 > code > docs.

**Known stale claims in old skills/docs:**
- arifOS 58-tool claim → live is 12 ✅
- arifOS "17 internal tools" → stale, superseded by 12-tool canonical
- GEOX 73/49 canonical → live is 16 canonical (duplicate `geox_physical_reality_interpret` found at positions 15 and 63)
- APEX :3002 references → decommissioned, do not use
- `mcporter` → deprecated, use direct HTTP

**Pitfall: `tool_search` ≠ live surface.** `tool_search` searches Hermes's cached tool index, not the live MCP wire. Always confirm with: `curl http://localhost:<port>/tools` or `tool_describe mcp__<org>__<name>`.

## Pitfalls captured

### Pitfall 1 — Treating naming as a doc check, not a probe

Running `grep arif_ /root/arifOS/README.md` and counting hits ≠ verifying the live surface. Always `curl :8088/tools | python3 -c "import json,sys; print([t['name'] for t in json.load(sys.stdin)['result']['tools']])"` before claiming a name exists.

### Pitfall 2 — Renaming a tool "because the name was unclear"

If agents in production have cached plans referencing `arif_old_name`, renaming breaks every cached plan. The audit fix is: rename the **description** (Law 2), not the name. Add a new tool if the verb really changed. Deprecation cycle for any name change: old name → new name → remove old name, with versioned aliases during transition.

### Pitfall 3 — Using poetic / aspirational / acronym-laden names

```
BAD:   geox_atlantean_petrosal_engine_v3
GOOD:  geox_petrophysics_compute_vsh_phi
```

The model can't pattern-match "atlantean" or "petrosal" → operation. Use the verb-noun pair the model already knows from training data (compute, fetch, list, search, send, validate, ...).

### Pitfall 4 — Argument names inherited from internal codebase naming

If your backend Python uses `(*args, **kwargs)` and you flatten to `params_input_data` in the JSON schema — **wrong**. The schema is read by models, not by your Python. Use `petrophysics_input` or `well_log_curve_data` or whatever the domain expert would say.

### Pitfall 5 — Reading docs as truth for tool surface

Doc claims ("13 tools", "8 public tools", "73 tools") often disagree with the live surface. The 2026-07-08 federation sweep found `tools_canonical.py` header still claims "13-Tool Canonical" while `tools/list` returns 12. Apply the precedence rule from `arifos-kernel-surface-curator`: live wire > VAULT999 > code > docs. Never quote a count from docs.

## MCP surface types — three distinct layers

MCP exposes three surface types. Audits must check all three:

| Surface | What it is | Audit command |
|---|---|---|
| **Tool surface** | JSON-RPC tools, callable by agents | `curl :<port>/tools` → count + description lengths |
| **App manifest surface** | `apps.json` + `.well-known/agent.json` — agent-discoverable apps | `curl https://<domain>/apps.json` + `curl https://<domain>/.well-known/agent.json` |
| **UI resource surface** | `ui://` URIs served by FastMCP — MCP Apps iframe content | `ui://app-name/index.html` — requires MCPBridge.js in app |

**Key session finding (2026-07-11):** Two `apps.json` files existed — source repo (`/root/geox/apps.json`) and web root (`/var/www/html/geox/apps.json`). Source was authoritative (6 apps, `ui_resource` fields, MCP Apps protocol). Web root had 4 apps, no `ui_resource`, wrong schema. **Rule: always compare repo source to deployed web root before assuming they match.**

## Pitfall 6 — `web_extract` returns stale cached data

`web_extract` caches responses. In this session, `arif-fazil.com/wealth/` showed `2026-06-16` via `web_extract` while the actual browser showed `2026-07-10`. The briefing data was correct — the extraction tool was stale.

**Workaround:** Always verify surface state with the browser tool (`browser_navigate` + `browser_snapshot`) for anything user-facing. Use `web_extract` for text-only endpoints, raw APIs, or static files — not for rendered HTML pages with live JS-driven content.

**Cache invalidation:** `web_extract` caches by URL. If data changed, the URL must change or the cache must be bypassed. For the WEALTH case: cron wrote to `latest.json` (correct date on disk) but `web_extract` had the old URL cached. The browser read the correct file directly.

## Pitfall 7 — Source repo vs web root divergence

For any deployed surface (tools.json, apps.json, agent.json):
- Check BOTH the source repo (`/root/<organ>/`) AND the web root (`/var/www/html/<organ>/`)
- Web root is what agents discover via HTTP
- Source repo is the canonical build artifact
- **If they differ: deploy source to web root, do not iterate on the wrong copy**

This session: `/root/geox/apps.json` (6 apps, correct) ≠ `/var/www/html/geox/apps.json` (4 apps, stale schema). Deployed source → web root.

## Federated tool surface probe

Run `references/federated-tool-probe.md` before citing tool counts from docs. It contains confirmed 2026-07-10 probe commands for all live organ endpoints plus known stale surfaces.

## Cross-references

- MCP Specification (2025-06-18) — Tools / Prompts / Resources (authoritative spec source)
- `arifos-kernel-surface-curator` — sibling skill for *trimming* the surface this naming rules govern
- `mcp-tool-upgrade-lifecycle` — sibling skill for *changing* tools (params, modes); naming is upstream
- `geox-federation-mcp-driver` — sibling skill for *driving* tools once named
- `measure-before-acting` — Failure 7 (fabricated quantitative scores), Failure 17 (denied a doc exists), Failure 18 (cited stale audit). All relevant to audit integrity.
- `references/federated-tool-probe.md` — confirmed tool counts + stale surface list from 2026-07-10 live probe
- `references/v2-contract-upgrade-pattern.md` — pattern for upgrading Python module contracts from dict-based to typed dataclass returns with YAML config, backward compat, and comprehensive tests

## Audit artifact template

When running a naming audit, write the report to `/root/forge_work/<date>/<organ>-NAMING-AUDIT.md` with:

- Live source URL + tool count + capture timestamp
- Each tool: name, description length, description's first 80 chars
- Findings grouped by law (1-5)
- Findings table with severity column
- Recommendation: file P0/P1 patches against descriptions (never names)
- Seal the audit receipt only when audit has run end-to-end against live surface

## Standing rule (embed in any org's onboarding)

When a new MCP tool is proposed for an organ, the proposal must include:
1. The intended `name` (snake_case, verb_noun)
2. The intended `title` (human readable, differs from name)
3. A draft `description` meeting Law 2 (30-500 chars, specific verbs + concrete nouns)
4. For each `properties` key: semantic argument name + `description` field
5. A specific user intent the tool solves (so reviewers can answer: "would the model pick this over the wrong tool?")

If any of (1)-(5) is missing, the proposal is rejected at design review — not implementation. **This is naming-as-constitutional-review. Naming is a contract. Contracts get reviewed.**
