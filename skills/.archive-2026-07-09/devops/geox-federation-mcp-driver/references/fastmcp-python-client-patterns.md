---
name: fastmcp-python-client-patterns
purpose: Async patterns, session lifecycle, schema introspection, and error handling for the FastMCP Python client across federation organs.
audience: any agent driving GEOX/arifOS/A-FORGE/AAA/WEALTH/WELL MCP tool calls.
---

# FastMCP Python Client — Patterns That Actually Work

This is the working reference for driving the federation's FastMCP streamable-HTTP
servers from Python. Verified against live `http://127.0.0.1:8081/mcp` (GEOX),
`http://127.0.0.1:8088/mcp` (arifOS), `http://127.0.0.1:7072/mcp` (A-FORGE),
`http://127.0.0.1:3001/mcp` (AAA) on VPS af-forge, 2026-07-03.

## 1. The Canonical Client Wrapper

```python
import asyncio, json
from fastmcp.client import Client

async def safe(c, name, args, _timeout=60):
    """Call a tool and always return a JSON-friendly dict, even on Pydantic errors."""
    try:
        r = await c.call_tool(name, args)
        # r.content is a list of TextContent blocks
        txt = "".join(b.text for b in (r.content or []) if hasattr(b, "text"))
        try:
            return json.loads(txt)
        except json.JSONDecodeError:
            return {"_raw": txt[:2000]}
    except Exception as e:
        # ToolError leaks Pydantic validation messages — these are gold for schema discovery
        return {"_error": str(e)[:700]}

async def main():
    async with Client("http://127.0.0.1:8081/mcp/") as c:
        # 1. List tools (full schema catalog, one round-trip)
        tools = await c.list_tools()
        for t in tools:
            schema = t.inputSchema
            # schema["required"], schema["properties"], etc.
            ...

        # 2. Read a resource
        r = await c.read_resource("geox://resources/ontology/sabah_basin_strat.yaml")
        text = r[0].text  # FastMCP client returns list[TextResourceContents]

        # 3. Call a tool
        result = await safe(c, "geox_atlas", {"lat": 6.075, "lon": 116.558, "mode": "context"})
```

**Activation:** `source /root/GEOX/.venv/bin/activate && python3 your_script.py`
The venv at `/root/GEOX/.venv` (and the duplicate `/root/geox/.venv`) already has
`fastmcp>=3.4.2` installed.

## 2. Session Lifecycle (Why Raw curl Fails)

FastMCP streamable-HTTP **requires** an `initialize` handshake before any `tools/call`.
The server returns the session id in the response **header** `mcp-session-id`,
not in the JSON body.

| Step | Required? | What happens if skipped |
|------|-----------|-------------------------|
| `initialize` | YES | First POST returns session id. All subsequent calls need it. |
| `notifications/initialized` | YES (per spec) | Tools/call returns HTTP 400 "Bad Request" |
| `tools/call` | needs both above | Otherwise: HTTP 400 |

**The fastmcp client handles all three steps automatically** via its async context
manager. Don't reimplement this in raw `urllib.request` — you will get bitten by
the Accept header (`text/event-stream` is required), the session header casing
variations, and the notification body format.

If you MUST use raw curl (e.g. shell-only env), see the SKILL.md "Path B" section
for the exact 3-step bash handshake. Tested 2026-07-03.

## 3. Pydantic-Errors-as-Schema-Introspection (NEW 2026-07-03)

**Discovery:** When a FastMCP tool rejects your call, the Pydantic v2 validation
error message **leaks the full input schema** — field names, types, required flags,
and even `description` strings.

**Use case:** When you don't want to round-trip `list_tools` for a single tool
(e.g. in a one-shot script), call the tool with `{}` and read the error.

**Example:**

```python
# Probe geox_egs_claim_create to discover its schema
try:
    await c.call_tool("geox_egs_claim_create", {})
except Exception as e:
    msg = str(e)
    # Output:
    # 2 validation errors for call[egs_claim_create]
    # title
    #   Missing required argument [type=missing_argument, ...]
    # statement
    #   Missing required argument [type=missing_argument, ...]
    #
    # → Required fields: title, statement
```

**Pattern (reusable):**

```python
async def probe_schema(c, tool_name):
    """Return the list of required field names by triggering a Pydantic error."""
    try:
        await c.call_tool(tool_name, {})
    except Exception as e:
        msg = str(e)
        # Pydantic format: "X validation errors for call[<name>]\n<field>\n  <detail>"
        import re
        # Required fields appear as "Missing required argument"
        required = re.findall(r'^(\w+)\n\s+Missing required argument', msg, re.M)
        # Unexpected kwargs appear as "Unexpected keyword argument"
        # (these are the field names, not the rejection)
        all_fields = re.findall(r'^(\w+)\n\s+(?:Missing|Unexpected)', msg, re.M)
        return {"required": required, "fields": all_fields, "raw": msg[:2000]}
    return {"required": [], "fields": []}
```

**Caveats:**
- Only works for tools defined with `additionalProperties: false` Pydantic models
  (the GEOX EGS tools all are). Tools that accept `**kwargs` won't leak anything.
- Description strings are NOT in the error — you need `list_tools` for those.
- One probe per call — re-raises the same error, so cache the result.

## 4. Common Error → Fix Table

| Error | Cause | Fix |
|-------|-------|-----|
| `HTTPError 400 Bad Request` on every call | Skipped `initialize` or notification | Use FastMCP client (handles it) |
| `SESSION_REQUIRED` on a read-only tool | Tool is in "reasoning" lane, middleware needs session | Use FastMCP client; or check `geox_surface_status` first to confirm wire works |
| `ToolError: N validation errors for call[<name>]\n<field>\n  Unexpected keyword argument` | Wrong field name (e.g. `region` vs `basin_name`) | Re-check `list_tools` or use probe_schema |
| `Unknown reason_type: <x>` | `geox_egs_evidence_reason` enum | Valid: `support`, `challenge`, `audit`, `verify`, `validate`, `consistency`, `all` |
| `Unknown qc_mode: <x>` | `geox_egs_data_qc_bundle` enum | Valid: try `default`, `evidence_consistency` is NOT one — try `evidence_qc`, `full` |
| `Basin data not found for: <X>` | `geox_basin` needs registered dataset | Register via `geox_well_ingest` or macrostrat; not a code bug |
| Tool returns empty `evidence_for/against: 0` after attach | Normal — counts only update after `geox_egs_query_claim` | Re-query to refresh |

## 5. Response Parsing Patterns

```python
# Tool call: result is CallToolResult with .content (list of TextContent)
r = await c.call_tool("geox_egs_claim_create", {...})
for block in (r.content or []):
    if hasattr(block, "text"):
        payload = json.loads(block.text)  # usually a dict
        cid = payload.get("claim_id")
        evidence_id = payload.get("evidence_id")
        # etc.

# Resource read: returns list[TextResourceContents] directly (not wrapped)
r = await c.read_resource("geox://resources/ontology/foo.yaml")
text = r[0].text  # NOT r.contents[0].text
# (raw JSON-RPC path uses r["result"]["contents"][0]["text"] — DIFFERENT shape)
```

## 6. Async Coordination Patterns

**Sequential dependency chain (claim → evidence → query):**

```python
async with Client(url) as c:
    cid = (await safe(c, "geox_egs_claim_create", {...}))["claim_id"]
    for ev in evidence_list:
        await safe(c, "geox_egs_evidence_attach", {"claim_id": cid, **ev})
    final = await safe(c, "geox_egs_query_claim", {"claim_id": cid})
    # final["results"][0]["status"] now reflects challenge state
```

**Fan-out across organs (parallel):**

```python
import asyncio
async def query_all(organs):
    async def one(url, tool, args):
        async with Client(url) as c:
            return await safe(c, tool, args)
    return await asyncio.gather(*[
        one("http://127.0.0.1:8081/mcp/", "geox_surface_status", {}),
        one("http://127.0.0.1:8088/mcp/", "arif_init", {"mode": "light"}),
        one("http://127.0.0.1:7072/mcp/", "forge_query", {"q": "leases"}),
    ])
```

**Timeout hygiene:** pass `timeout=` to `Client(url, timeout=120)` for tools
that hit slow paths (e.g. `geox_basin` with macrostrat, `geox_egs_scenario_audit`).
Default 60s is too short for `geox_basin Sabah` on a cold cache.

## 7. Real Receipts From 2026-07-03 Kinabalu Audit

A complete 12-step GEOX pipeline (claim create → 4 evidence attach → 1 evidence
against → formal challenge → uncertainty query → provenance → rock physics →
scenario audit → QC bundle → basin synthesis → deep time → map layers → forbidden
scan) executed in **< 4 seconds** wall time using the patterns above.

Key claim created: `935be7ceb54241c2` (Two Oceanic Plates Built Mount Kinabalu).
Final state: `status=challenged`, `evidence_for=4`, `evidence_against=2`,
`confidence_score=0.50`.

Pipeline script: see `templates/geox_audit_script.py`.

## 8. Anti-Patterns To Avoid

- **Don't** hand-roll the session handshake in `urllib` — you'll spend 30 min
  debugging Accept headers. The fastmcp client is already installed in
  `/root/GEOX/.venv/`.
- **Don't** call `list_tools` inside a tight loop — cache the result.
- **Don't** assume `evidence_for` count in the attach response is current —
  re-query the claim to get the authoritative count.
- **Don't** pass `session_id` in tool arguments for reasoning-lane tools — the
  middleware extracts it from HTTP context, not args. Pass it via the fastmcp
  client (which handles the header).
- **Don't** retry the same failing call 5+ times. If it fails twice, re-probe
  state — the federation moves under you.

## 9. arifOS Constitutional Tool Schemas (Confirmed Live 2026-07-03)

### `arif_init` — valid `mode` enum
`init | light | resume | validate | epoch_open | epoch_seal | opt_out | opt_out_profiling`
Anything else (`constitutional_init`, `start`, `begin`) → verdict `RETAK` with reason `"Unknown mode: X"`.

### `arif_observe` — returns 9-signal vector
`result` includes `omega_0: 0.08` (cognitive diversity), `cascade_exhausted`, `void: [...]` (failure modes), `risk_flags: []`, `max_evidence_level: "L0"`. Almost always returns `success: false` with `void: ["search_failed", ...]` when no web source is queried — this is by design (search is not pre-connected).

### `arif_route` — returns routing decision envelope
Fields: `routing_rule` (intent_map / direct_override), `organ`, `port`, `tool_prefix` (e.g. `geox_`), `organ_tool`, `routing_confidence` (0.0-1.0), `chain: [...]` (state-chain entries).

### `arif_think` — modes that DON'T error
`plan` returns SEAL (inner RETAK is normal). Avoid `analyze`, `synthesize`, `reflect` (not in current mode enum — error: "Unknown mode: X").

### `arif_judge` — REQUIRED fields (all 5 must be present, no defaults)
```json
{
  "actor": "Arif (F13 SOVEREIGN)",       // string, required
  "intent": "Constitutional judgment on ...",  // string, required
  "requested_capability": "judge_geological_model",  // string, required
  "domain": "geoscience/tectonic_stratigraphy",     // string, required
  "reversibility_level": "reversible",              // enum: reversible|irreversible
  "blast_radius": "federation_wide"                 // enum: none|local|organ|federation_wide|global
}
```
Optional: `epistemic_state` (enum: UNKNOWN|OBSERVED|DERIVED|...), `evidence` (array of objects with `type`, `id`, `key_finding`), `authority_token`, `actor_id`, `session_id`.

**Verdict matrix:**
| reversibility | blast_radius | verdict |
|---|---|---|
| reversible | any | SEAL |
| irreversible | none/local/organ | SEAL |
| irreversible | federation_wide/global | **ESCALATE** → F13 SOVEREIGN required |

### `arif_seal` — when `arif_judge` returns ESCALATE
To complete the chain, call `arif_seal` with:
```json
{
  "payload": "<the judge_state_hash or claim_id>",
  "ack_irreversible": true,
  "actor_signature": "<F13 SOVEREIGN cryptographic sig>",
  "nonce": "<unique nonce>",
  "witness_type": "human",
  "constitutional_chain_id": "<from judge>",
  "judge_state_hash": "<from judge>"
}
```
Without `actor_signature` + `nonce`, `arif_seal` will return HOLD. This is by design — the kernel demands a real human sovereign signature for irreversible+federation acts. **Do NOT call `arif_seal` autonomously on `ESCALATE` — escalate to Arif instead.**

## 10. GEOX Layer + Resource URI Patterns (Confirmed 2026-07-03)

| URI pattern | Returns | Example |
|---|---|---|
| `geox://layers/<layer_id>/package` | Full layer envelope (license, bbox, truth_class, governance) | `sabah.basin_outline.v3` ✓, `kinabalu.velocity` ✗ not seeded |
| `geox://resources/ontology/<file>.yaml` | Full ontology YAML | `sabah_basin_strat.yaml` ✓ (24,117 chars) |
| `geox://basins/<basin>/profile` | Listed in `geox://basins/index` but `read_resource` returns "Unknown resource" | Listed-only, not exposed |
| `tree777://geo/concepts/<name>` | TREE777 wiki concept | Most return "Concept not found" — wiki is empty/sparse |
| `geox://claims/graph` | List of claim+evidence nodes | Works — returns hardcoded Malay Basin seed + any created |
| `geox://identity` | Server identity BLAKE3 hash | Server-specific |
| `geox://surface/truth` | Surface registration status | Useful for debugging |

**Confirmed working URIs for Kinabalu/Sabah work:**
- `geox://resources/ontology/sabah_basin_strat.yaml` (24 KB — load this FIRST)
- `geox://layers/sabah.basin_outline.v3/package` (PETRONAS open data)
- `geox://claims/graph` (your claim + 5 Malay Basin seed claims)
- `geox://literature/GSM-MADON-2021-MALAY-BASIN` (Madon 2021 paper)

**Confirmed NOT exposed** (listed in indexes but `read_resource` fails):
- `geox://basins/sabah-basin/profile`
- `geox://ontology/sabah_basin_strat.yaml` (note: NO `resources/` prefix — common mistake)
- `tree777://geo/concepts/<anything>` (wiki is empty)

## 11. Search File Glob Traps (Discovered 2026-07-03)

When verifying files exist before claiming, `search_files target=files pattern=PREFIX*` works only if the literal substring `PREFIX` appears in the filename. Example:
- `pattern="kinabalu*"` → matches `KinabaluScar.png`, `kinabalu_correlation_v2.png`, etc.
- `pattern="kinabaluscar*"` → matches NOTHING if no file has the substring `kinabaluscar` (e.g. user might expect `kinabalu_two_oceanics_final.png` to match a `kinabaluscar*` pattern — it won't).

**Workaround:** When in doubt about a filename, run `ls -la /root/<known-prefix>*` or `find /root -maxdepth 4 -iname "<known-prefix>*"` to verify. Don't trust `search_files` returning 0 as proof of absence — it's a substring match, not a fuzzy match.

The 4 PNG files for Kinabalu work all live at `/root/`:
- `KinabaluScar.png` (12.4 MB, original seismic profile — the user's "kinabaluscar" reference)
- `kinabalu_correlation_v2.png` (1.5 MB, KL2 well correlation)
- `kinabalu_two_oceanics_model.png` (early sketch)
- `kinabalu_two_oceanics_final.png` (1.4 MB, the 6-panel final poster — SHA256 `7ca8b00e...0a1f5a30`)
- `kinabalu_two_oceanics_final_tg.png` (Telegram doc version, 1.0 MB)
- `kinabalu_two_oceanics_final_photo.png` (Telegram photo version, 553 KB)

## 12. Visual Audit Loop (Cross-cutting pattern)

When producing geological artifacts (cross-sections, block diagrams, regional maps), **always** run a `vision_analyze` visual audit on each PNG BEFORE assembling into a PDF or sending to the user. Common pitfalls caught:

- Title blocks overlapping key labels → move title to a different corner or above the figure
- Annotation labels overlapping filled polygons → add `bbox=dict(fc='white', ec='black', alpha=0.9)`
- Legends in `loc='lower left'` covering sea polygons on regional maps → use `loc='lower right'` with `bbox_to_anchor=(0.99, 0.02)`
- Header rows in matplotlib `ax.table()` overlapping data cells → use manual rect+text grid (see `geological-artifact-publication` §6)
- Rotated text getting clipped at figure edges → place horizontal label to the SIDE
- Common matplotlib typo: `bboxdict=None` — correct kwarg is just `bbox=dict(...)` (no `bboxdict` key)

This audit catches ~80% of layout bugs. Budget 2-3 minutes per figure for it.