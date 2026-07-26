---
name: mcp-conformance-audit
description: Full MCP server conformance audit — Streamable HTTP lifecycle, ghost tool classification, AppConfig wiring, vertical slice proof, and test suite generation. Use when auditing any MCP server for protocol compliance, tool→app UI mapping correctness, or registry drift.
---

# MCP Conformance Audit

Complete end-to-end conformance verification for MCP servers. Covers HTTP transport lifecycle, tool surface truth, AppConfig UI mappings, resource registration, and vertical slice proof.

## When to use

- Auditing an MCP server for protocol compliance
- Verifying tool→app→resource URI chains (SEP-1865 MCP Apps)
- Classifying ghost/recovered tools against a canonical registry
- Wiring FastMCP `AppConfig` for tool UI mappings
- Building a conformance test suite against a live MCP endpoint

## Phase structure

### GATE 0: Remote continuity
- Confirm branch and commit exist on remote
- Write `artifacts/conformance/remote-branch-proof.json`

### P0.1: HTTP lifecycle diagnostic
Write a Python test script (using only `urllib`) that performs the full MCP handshake:
```
initialize → notifications/initialized → tools/list → resources/list → prompts/list
```
Key details to capture:
- HTTP status codes per step
- `Content-Type` and body mode (JSON vs SSE)
- `mcp-session-id` header (case-sensitive: lowercase `mcp-session-id` in FastMCP)
- protocolVersion, serverInfo, capabilities from initialize response
- Tool count, resource count, prompt count
- SSE transport rejection (406 Not Acceptable for JSON-only servers)

**Critical pitfall**: FastMCP uses lowercase `mcp-session-id` header, not `Mcp-Session-Id`. Your test headers must match. Use `{k.lower(): v for k, v in resp.headers.items()}` for case-safe comparison.

Save output to `artifacts/conformance/initialize-capture.json`.

### P0.2: Ghost tool classification
Compare live `tools/list` against canonical registry. For each tool in the registry but NOT live:
- **PUBLIC_CANONICAL**: Declared public, needs wiring
- **INTERNAL_CALLABLE**: Internal dispatch, never expose publicly
- **COMPATIBILITY_ALIAS**: Mode alias for consolidated tool (e.g. `geox_well_tie` → `geox_seismic_compute mode=well_tie`)
- **CROSS_ORGAN_ROUTE**: Bridges to another organ (e.g. WEALTH) — do NOT expose as public
- **DEAD_OR_DUPLICATE**: Genuinely defunct

**Rule**: Do NOT blindly `@mcp.tool()` all phantom tools. Classify first. Cross-organ tools must remain internal.

Save output to `artifacts/conformance/ghost-tool-classification.json`.

### P0.3: AppConfig wiring
Wire `app={"resourceUri": "ui://..."}` to `@mcp.tool()` decorators for tools with UI apps. The canonical manifest (`canonical_manifest.json`) is the single source of truth for mappings.

Verify via live `tools/list` that `_meta.ui.resourceUri` appears for linked tools.

Create `artifacts/conformance/tool-app-resource-matrix.json` mapping every tool→app→resource URI.

### P0.4: Fix `list_apps` to derive from manifest
The `list_apps` MCP tool MUST derive from `canonical_manifest.json`, not a hardcoded dict. Output format:
```json
{
  "standard": "SEP-1865",
  "count": N,
  "apps": [{"id", "title", "resourceUri", "mimeType", "linkedTools", "status"}]
}
```
Include fallback to the hardcoded source for backward compatibility.

### P0.5: Vertical slice proof
Pick one tool→app chain and prove every link:
1. Tool in `tools/list` ✓
2. `_meta.ui.resourceUri` in tool definition ✓
3. URI in `resources/list` ✓
4. `resources/read` returns HTML ✓
5. MIME type is `text/html;profile=mcp-app` ✓

Write `artifacts/conformance/vertical-slice-report.md` with a chain diagram and SEP-1865 checklist.

### P0.6: Conformance test suite
Create 5 test files under `tests/mcp_conformance/`:
1. `test_initialize_streamable_http.py` — HTTP handshake, protocol version, capabilities, SSE rejection
2. `test_lifecycle.py` — Full init→notifications→tools→resources→prompts
3. `test_appconfig_links.py` — `_meta.ui.resourceUri` for linked tools
4. `test_list_apps.py` — SEP-1865 output validation
5. `test_one_app_vertical_slice.py` — End-to-end tool→app→resource chain

Tests use only `urllib` + `json` (no dependencies) and work against any MCP server at `http://localhost:PORT/mcp`.

## External holds
Record service build drift (running server version ≠ working tree version), federation geometry gaps, and transitional URI mappings in `artifacts/conformance/external-holds.json`.

## Commit discipline
- One commit per phase (or logical group)
- Push to the conformance branch, never merge to main without review
- Final verdict: PASS | CONDITIONAL_PASS | HOLD | FAIL
