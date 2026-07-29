# SylphxAI/pdf-reader-mcp — Intake Case Study

> **Date:** 2026-07-28
> **Verdict:** PERMANENT QUARANTINE (F1 CRITICAL — SSRF/Outbound Egress)
> **4-Stage Pipeline Proven:** Marketing copy + Zod schema passed review; runtime behavior failed Test 4.10

## What Happened

SylphxAI/pdf-reader-mcp (pinned v4.1.2, MIT) was evaluated for integration into the arifOS federation as a Layer 1 perception sensor for PDF extraction. The 4-stage intake pipeline was followed:

| Stage | Result | Notes |
|-------|--------|-------|
| 1. Containment | ✅ PASS | Isolated process, no production access |
| 2. Handshake | ✅ PASS | JSON-RPC 2.0, stable connection |
| 3. Floor Scan | ✅ PASS | F1/F2 invariants looked clean — Zod schema declared `url XOR path` |
| 4. Stress Test | ❌ **FAIL** | Test 4.10 caught SSRF/egress |

## The Critical Finding (Test 4.10)

**Schema claim (Zod):** `.refine((args) => Boolean(args.path) !== Boolean(args.url), {...})` — this checks that `url` and `path` are mutually exclusive at the schema level.

**Runtime reality:** The Zod `.refine()` checked `Boolean(path) !== Boolean(url)`. This failed when BOTH or NEITHER were present, but allowed `{ url: "..." }` alone to pass validation and reach the Rust HTTP client (ureq).

**When triggered with a URL:** Sylphx initiated an outbound HTTPS connection to `example.com` (33ms latency).

**F1 violation:** SSRF/outbound egress violates F1_AMANAH (reversible-first — remote fetch is not reversible from the local system's perspective) and LOCALHOST_IS_PASSWORD doctrine (all data services bind 127.0.0.1).

## The Accept Header Fix (Positive Discovery)

During integration testing, it was discovered that GEOX (:8081), WEALTH (:18082), and WELL (:18083) MCP servers reject calls without `Accept: application/json` header. This was not a Sylphx issue but a federation-level discovery that affected session-based MCP servers.

**Fix applied:** All MCP dashboard and integration probes now send `Accept: application/json` by default.

## Key Lessons

1. **Never trust marketing copy or schema definitions. Verify execution at the socket.** The Zod `.refine()` looked correct on paper but the runtime behavior differed. Only Stage 4 dynamic testing caught the mismatch.

2. **Schema validation at the JSON-RPC layer is NOT runtime sandboxing.** Zod runs on the same process as the tool. It doesn't prevent the tool from calling `ureq::get()` if the schema passes.

3. **The 4-stage pipeline (containment → handshake → floor scan → stress test) is non-negotiable.** Each stage covers a different failure mode. Skipping any stage would have missed this vulnerability.

4. **`url:` parameter = SSRF risk = F1 CRITICAL.** Any MCP server that accepts a `url:` parameter and initiates outbound HTTP(S) connections must be path-only gated. This was added as F1.8 clause in the integration contract.

## Rollback Execution

```bash
npm uninstall -g @sylphx/pdf-reader-mcp   # Remove native binary
# Remove mcp.json entry
# forge_registry --remove <fingerprint>
# Zero federation data mutated
```

Full audit trail at `/root/A-FORGE/forge_work/2026-07-28/sylphx-integration/`.
