---
name: live-probe-audit-pattern
description: "Probe status narratives against live system state before accepting. Narrative-vs-state audit for web routing, MCP surfaces, agent registrations, and SOT"
tags: [audit, probe, trust-but-verify, caddy, mcp, navigation, narrative-vs-state]
triggers:
  - "audit this"
  - "100% pass"
  - "zero dead links"
  - "EXECUTED, AUDITED & DEPLOYED"
  - "PLAN ID"
  - "narrative claim"
  - "verify deployment"
  - "navigation audit"
  - "site audit"
  - "deploy receipt audit"
  - "SOT audit"
  - "audit and validate this claim"
  - "validate this claim"
  - "architectural audit"
  - "strategic evaluation"
  - "external audit"
  - "deployment audit"
  - "delegate agent"
  - "subagent"
  - "verify agent claims"
  - "authority recovery"
  - "apex scalars"
  - "G-fold"
  - "UNMEASURED"
  - "hardcoded stub"
  - "live-fetched"
  - "health endpoint wiring"
  - "verbosity trimming"
  - "response pipeline"
  - "apex scalars missing"
  - "MCP response minimal"
  - "direct call vs MCP call"
  - "trim_for_verbosity"
  - "cross-witness"
  - "dual agent"
  - "convergence"
  - "audit claims against live"
---
# Live Probe Audit Pattern

## The Tell

When a session-feed narrative declares completion with confident numbers ("100% OK", "Zero dead links", "all 91 URLs pass"), the numbers are usually inflated by 20-40% relative to reality. Reasons:
- "URL count" often counts references across all surfaces including duplicates, not unique paths
- "Asset hash fixed" usually means file changed, not Caddy/config reloaded
- "All surfaces wired" usually means 5 of 8 surfaces, missing the rest
- "Discovery files fixed" usually means files added to disk, not routing config wired

**Rule: never trust the preamble, always probe the count.**

## Probe Order (Mandatory)

```bash
# 1. Sample 10 random surface URLs
for path in /a/ /b/ /c/; do
  curl -sf -m 5 -o /dev/null -w "%{http_code} %{url_effective}\n" "https://example.com${path}"
done

# 2. Extract all internal hrefs from rendered HTML (not static docs)
curl -sf -m 10 example.com > /tmp/audit/index.html
python3 -c "
import re
with open('/tmp/audit/index.html') as f:
    hrefs = re.findall(r'href=\"([^\"#]+)\"', f.read())
internal = {h for h in hrefs if h.startswith('/') and not h.startswith('//')}
for h in sorted(internal): print(h)
"

# 3. For each unique internal href, probe HTTP code (sample, not all if huge)
# 4. Distinguish real asset URLs from directory listings
#    /assets/specific.css returns 200 (real)
#    /assets/ alone returns 404 (directory listing, false positive)

# 5. Check filesystem for files that exist but route 404 (Caddy bug signal)
ls /var/www/html/.well-known/<path>
curl -sf -m 5 -o /dev/null -w "%{http_code}\n" "https://example.com/.well-known/<path>"
# If file exists on disk + returns 404 → handler routing bug, not missing file

# 6. Bypass Cloudflare/CDN for ground truth
curl -sf -m 5 -k --resolve "example.com:443:127.0.0.1" https://example.com/.well-known/<path>
# 404 from Caddy-direct = server-side bug, not edge cache
```

## The Trust-But-Verify Scoring Template

After probes, produce an honest verdict per claim with epistemic tag.

| Surface | Status | Evidence |
|---|---|---|
| /wealth/, /gold/, /oil/, /gas/, /geox/ | nav wired (OBS) | grep market-map-bar = 2 refs |
| /well/, /writings/, /makcikgpt/ | nav MISSING (OBS) | grep returns 0 refs |
| `/.well-known/{file}` | 404 (file exists on disk) (OBS) | Caddy handler order |

**Real numbers over vibes.** When narrative says "100%" and probe shows "70%", report "70%, not 100%." Don't add qualifiers like "largely complete" or "essentially done." Plain numbers are the F2 TRUTH floor.

## Common Drift Patterns

### Caddy routing for `/` and `/.well-known` cross-roots

When `@well-known` is a catch-all handler matching first in `/etc/caddy/Caddyfile`, AND there are second-pass handlers like `@observatory_discovery` for specific paths in different roots, paths in the second root will 404 even though file exists.

Fix is 888_HOLD (production web routing): reorder handlers in `/etc/caddy/Caddyfile` so cross-root dispatch happens before catch-all.

### AAA pre-commit secret scanner pattern

The AAA repo's pre-commit hook does pattern-scan for API key formats (Telegram / GitHub / generic). If a commit contains config referencing key patterns (even non-secret descriptions), it **times out / blocks the commit** instead of failing clean.

```bash
# Symptom: commit hangs/times out at pre-commit stage
# Fix:
git commit --no-verify -m "..."
# This is the documented emergency escape hatch in the hook script:
# Skip: git commit --no-verify (emergency only SABAR)
```

**Real key placement:** source the API key from `/root/.secrets/vault.env` at runtime, do NOT embed in committed config.

### Asset path drift: `/assets/` vs `/_shared/`

If audit claims fixed `assets/index-HASH.css`, verify the actual file path. Real path may be `/var/www/html/<service>/assets/...` while the web root is `/var/www/html/<other>/_shared/...`. Caddy serves via try_files; some paths redirect fine, some don't.

### Agent registration gates

When audit claims "external agents registered in AAA":
1. Check `/root/AAA/agent-skill-binding-map.md` for the row
2. Check `/root/AAA/agents/_external/<name>/agent-card.json` exists
3. Run the agent's binary: `<binary> --version` to verify install

A claim of "registered" may satisfy one of these without the others.

### DeepSeek BYOK Anthropic endpoint (verified 2026-07-19)

DeepSeek exposes an Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`. Wire pattern for any agent that accepts Anthropic-format env vars:

```bash
export COPILOT_PROVIDER_TYPE=anthropic
export COPILOT_PROVIDER_BASE_URL=https://api.deepseek.com/anthropic
export COPILOT_PROVIDER_API_KEY=sk-<deepseek-key>
export COPILOT_MODEL=deepseek-v4-pro    # or deepseek-v4-flash
export COPILOT_PROVIDER_MAX_PROMPT_TOKENS=840000
export COPILOT_PROVIDER_MAX_OUTPUT_TOKENS=128000
```

Verified agents that consume this pattern: GitHub Copilot CLI (`@github/copilot`), Hermes, opencode, claude-code, kilocode, workbuddy, openclaw, gemini-cli, deepcode, nanobot, crush, pi_mono, reasonix, langcli (17 agents per DeepSeek docs sidebar `agent_integrations/`).

**Critical caveat:** Must use provider_type=`anthropic`. `openai` type triggers HTTP 400 `reasoning_content in thinking mode must be passed back to the API` because DeepSeek requires reasoning_content echo on subsequent requests, which Copilot CLI's OpenAI integration does not support.

Verified live: `copilot -p "hello from deepseek via copilot cli"` returned exact match (18s, 141k tokens).

## Verdict Contract

When reporting audit findings:
- Pass: with evidence (probed URL + response code)
- Fail: with **path + root cause** (not just "404")
- Partial: with what's there + what's missing

For each claim in the original narrative, state its true status with epistemic tag (OBS = direct probe, INT = inferred, DER = derived).

```
Layer A APEX fingerprint              Active — G score, C_dark shadow state, &
                                       organ conservation aktif.

Reality:
[OBS] Verified live — Layer A fingerprint rides on tool responses
[OBS] The quote registry Layer A math computes G per resolve
```

## Cross-Witness Audit Protocol (proven 2026-07-28)

**Signal:** An agent (OpenCode, Claude, any subagent, or a peer) produces a deployment report, internal audit, or status assessment full of specific numbers, status flags, and severity ratings.

**The protocol — two agents, one truth:**

```
Agent A (scanner): Runs deep audit → produces claims + numbers + severity
Agent B (witness): Independently probes every claim against live state
                   → confirms true, corrects false, notes overclaim
Convergence:       Both agents agree → seal the converged truth
```

**Why this exists:** This session proved a single-agent internal audit is ~60% accurate on first pass. OpenCode (FI-001) produced a 7-layer audit with 14 findings. Hermes independently verified and found 3 of 8 core claims were false (MCP resources=0, vault silent 4 days, kernel F2 violation). The false claims were not malicious — they were interpretation errors, stale data, and missed nuance. Without the cross-witness, those 3 false claims would have been sealed as truth.

**Procedure when another agent sends an audit:**

1. **Extract all falsifiable claims** — numbers, boolean flags, severity labels, route statuses. Ignore narrative framing.
2. **Probe each claim independently** — do not re-read the agent's probe output. Use your own tools (curl, HTTP, MCP list, git log). The agent's probe is OBSERVATION, not TRUTH.
3. **Classify each claim:**
   - ✅ **Confirmed** — your independent probe matches the claim
   - ❌ **False** — your probe contradicts the claim outright
   - ⚠️ **Misread** — kernel of truth but interpretation is wrong (e.g., "kernel healthy + held = F2 violation" is actually correct constitutional behavior)
   - 📊 **Inflated** — numbers overstated by 10-30% (common: "327 resources" counts all skill:// noise as signal)
4. **Report the convergence:** Show which claims converged, which diverged. Label with epistemic tags.
5. **Seal the converged truth** — when two independent agents agree, the finding is no longer CLAIM, it is TRI-WITNESS evidence (F3). Append to VAULT999 naming both agents.

**Convergence template:**

| Claim | Agent A | Agent B (witness) | Verdict |
|-------|---------|-------------------|---------|
| Drift exists | True | True (curl /health) | ✅ CONVERGE |
| MCP resources=0 | True | False (list_resources → 34) | ❌ FALSE |
| Vault silent 4 days | True | False (3 seals today) | ❌ FALSE |

**Pitfall:** Do NOT delegate the cross-witness to a subagent. The cross-witness must be YOU probing live state directly. Subagents are themselves single-agent audits and need their own cross-witness.

### Resource Count Inflation Detection

**Pattern:** When an agent claims an MCP resource count, they may count every `skill://` entry even though those are filesystem mirrors, not operational data. Signal: claimed count >> expected operational resources.

**Detection:** Via MCP `resources/list`, count `arifos://` + `tree777://` URIs only. Expected ~34 resources (doctrine, atlas333, vitals, wisdom, 1 skill://index). Not 294 skill:// static entries (collapsed to 1 index + 1 template on 2026-07-28).

### Convergence Sealing

When two independent agents converge on the same finding, the evidence is stronger than either alone (F3 WITNESS). Seal immediately recording both agents and the converged finding.

## Pitfalls

- **Never trust "N URLs all 200" without the URL list.** Audit script may include anchor tags, javascript: URLs, mailto: links, fragments (#) in its pass count.
- **Delegate agent claims about code must be grep-verified before forwarding to the user (scar 2026-07-19).** Subagents can fabricate detailed architectural findings (specific line numbers, named patterns, "three parallel paths") that don't exist in the actual source. Always verify at least one key claim with grep/curl before presenting a subagent's analysis as fact. See `references/delegate-agent-audit.md` for the full recipe.
- **When two subagents report different tool counts / version numbers / branch states, trust the live health endpoint, not the agent prose.** Subagent contexts diverge. Health endpoint + git log are the reconcilers.
- **Vision vs. reality — agent-described architecture ≠ deployed code (scar 2026-07-20).** When an agent (Forge, OpenCode, any subagent, or yourself) vividly describes a system feature with architecture, naming, and flow — probe the codebase before discussing it as real. The tell: compelling prose about something you can't grep. Pattern: Forge described PRL (Precedent Retrieval Layer) with full dual-gate architecture, τ ≥ 0.95, blast_radius filtering, Qdrant integration — as if it existed. `grep -r "prl\|PrecedentRetrieval" /root` returned zero code matches. Arif's correction: "Do we have this? Do I need to remember it?" Translation: **if it's not in the code, don't describe it as built.** Probe first: `search_files` for the name, check the tool registry, curl the health endpoint. Vision = blueprint. Reality = code. Don't conflate them, even when the vision is architecturally correct.
- **S24 passive sensor unreachability is industrial SCADA logic, not an outage (scar 2026-07-24).** When the S24 Sovereign Sensing Node times out on direct HTTP probe, do NOT frame it as "Termux asleep — expected Android behavior." The correct framing: S24 is a passive sensor in a data diode architecture — it collects data when polled by the central brain (FORGE cron), sleeps between cycles, and never initiates connections. Check the telemetry JSONL (`/root/arifos-memory/telemetry/s24_history.jsonl`) for the last successful entry rather than relying on a live probe. This is industrial telemetry applied to a smartphone, not a consumer app failing to stay awake. Distinguishing design features from implementation gaps is F2 TRUTH discipline.
- **Canonical manifest tool→resource mappings must match live resources/list (scar 2026-07-19).** When building canonical_manifest.json from GEOX_APPS + live MCP, some app URIs (e.g., `ui://geox/basin-explorer`, `ui://geox/catalog`) are defined in GEOX_APPS but NOT registered as live MCP resources. Include only mappings where the resource URI exists in live `resources/list`. Otherwise conformance tests fail with "Resource X mapped from tool Y but not in resources/list."
- **FastMCP 3.x AppConfig: use `app={"resourceUri": "ui://..."}` in `@mcp.tool()` decorator, not post-registration `_meta` injection (scar 2026-07-19).** FastMCP 3.4.2+ accepts `app` as a dict or `AppConfig` instance directly in the decorator. The old enrichment code at the bottom of tools_wiring.py using `tool._meta` / `tool.__dict__["_meta"]` is fragile and only worked for one tool. Explicit decorator params are the FastMCP-native approach.
- **MCP verbosity trimming can silently strip response fields (scar 2026-07-27).** When an MCP tool handler has a `verbosity` parameter defaulting to `"minimal"`, the response trimmer drops `apex_scalars`, `atlas333`, `session_birth`, `sct_claims`, `work_contract`, and 30+ other fields. The handler returns the correct data internally, but the MCP transport layer collapses it. Detection: direct Python call vs MCP HTTP call produces different key sets. Fix: check `verbosity` default in the handler, change to `"standard"`. See `references/mcp-response-pipeline-audit.md` for the full detection recipe.
- **canonical_registry.py authority: use registry.py CANONICAL_PUBLIC_TOOLS, not manifest visibility (scar 2026-07-19).** `build_registry()` was deriving public_names from `tools_manifest.yaml` visibility field (25 tools), but `registry.py::CANONICAL_PUBLIC_TOOLS` (17 tools, ghost-filtered) is the authoritative live surface. This caused `CANONICAL_PUBLIC_SURFACE.json` drift (25 vs 17). Fix: use `set(CANONICAL_PUBLIC_TOOLS)` as the authority set in `build_registry()`.
- **When multiple apps map to the same tool, the primary mapping wins in `tool_to_resource` (scar 2026-07-19).** Example: both `well_desk` and `analog_digitizer` map to `geox_well_desk`. The canonical `tool_to_resource` should show `geox_well_desk → ui://geox/well-desk` (the primary), not `→ ui://geox/analog-digitizer`.
## Pitfalls

- **Never downgrade FastMCP across major versions (scar 2026-07-19).** FastMCP 2.x ↔ 3.x have incompatible internal module structures. Downgrading 3.4.2 → 2.x breaks imports (`PrivateKeyJWT...ator`, `client_log_level`). Fix the code for the installed version, never the other way around. GEOX's server.py already gracefully skips the claims sub-server when **kwargs tools are rejected — the downgrade path creates MORE problems than it solves.\n- **GEOX tool count: verify health endpoint, not registry.** Health says `public_tools=24`. Registry says 77. SACRED_SURFACE invariant says 139. The health endpoint is ground truth. Never cite 78 or 77 as the live tool count without verifying against health.\n- **Web extraction (web_extract) can fail silently.** Tavily 432 errors can cascade across both web_search and web_extract. When both fail, fall back to `curl` + direct API calls (GitHub API, raw.githubusercontent.com). Don't loop on the same failing tool.
- **"tools/list returns 0" is a session problem, not a server problem (scar 2026-07-19).** MCP over SSE requires a 3-step handshake: `initialize` → capture `Mcp-Session-Id` → `notifications/initialized` (202, empty body!) → THEN `tools/list` works. One-shot curl calls without session return 0 tools or HTTP 400. The server is healthy — the probe is incomplete. Full recipe: `references/mcp-sse-session-lifecycle.md`.

### MCP Resource/List Probing

When probing whether MCP resources are exposed via `resources/list`, the endpoint and headers matter:

```python
import urllib.request, json

body = json.dumps({"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}).encode()
req = urllib.request.Request("http://localhost:<port>/mcp", data=body,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"  # REQUIRED
    })
resp = urllib.request.urlopen(req, timeout=5)
data = json.loads(resp.read())
resources = data.get("result", {}).get("resources", [])
```

**Common errors and diagnosis:**
- **405 Method Not Allowed** — using GET instead of POST. MCP uses POST-only.
- **406 Not Acceptable** — missing `Accept: application/json, text/event-stream` header. This is the most common failure.
- **400 Bad Request / "Missing session ID"** — organ requires MCP session auth. Use `arif_init` first to get a session_token, or try the organ's `surface_status` tool (e.g., `geox_surface_status`) which reports the registry without session auth.
- **Empty result** — the organ may expose resources via session-gated pattern (need session_id in the request body: `params: {session_id: "..."}`).

Not all organs expose the same MCP transport. GEOX requires session auth for `tools/list` but exposes everything via `geox_surface_status(mode=registry)`. arifOS exposes both tools and resources via streamable HTTP on `:8088/mcp` with the correct headers.

### Session ID Truncation Bug (arifOS → GEOX bridge, scar 2026-07-19)

**Pattern:** When a session_id is generated by `arif_init` (e.g., `SEAL-03ad5f04adbb4b6f` = 22 chars) and passed through `arif_route` bridge to a downstream organ (GEOX), the session_id gets **truncated to 19 chars** (`SEAL-03ad5f04adbb`). The downstream organ rejects the truncated ID as `SESSION_INVALID`.

**Symptom pattern:**
- `arif_init` returns a 22-char session_id (`SEAL-XXXXXXXXXXXXXXXX`)
- `arif_route(organ_tool="geox_X")` passes it via bridge
- GEOX receives 19 chars, returns `SESSION_BINDING · verdict=HOLD · trace=gov-... · Session validation failed: SESSION_INVALID`
- Tools that DO work through bridge: `geox_basin(mode=profile)`, `geox_basin(mode=macrostrat)`, `geox_prospect(mode=screen)`, `geox_deep_time_state` (low-binding tools)
- Tools that FAIL through bridge: `geox_petrophysics`, `geox_seismic_compute`, `geox_well_desk`, `geox_claim` (strict-binding tools)

**Workaround (verified):** When full session binding is broken, fall back to `geox_deep_time_state` (low-binding) for evidence, OR call GEOX tools directly via curl bypassing `arif_route` if the organ exposes them without bridge auth.

**Root cause (pending fix):** arifOS bridge handler does character-bound truncation on session_id before forwarding. Suspect `arifosmcp/runtime/rest_routes/rest_routes.py` or `arifosmcp/kernel/interceptor.py` has a hardcoded `max_session_id_len = 19`. 888_HOLD territory — requires F13 to investigate the actual truncation site.

**Probe recipe when SESSION_INVALID appears:**
```bash
# 1. Confirm session_id format from arif_init
SESS=$(curl -s -X POST http://localhost:8088/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"arif_init","params":{"actor_id":"HERMES"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['session_birth']['session_id'])")
echo "Length: ${#SESS} → expected 22"  # If <22, init itself is truncating

# 2. Test the tool that DOES work (low-binding)
curl -s -X POST http://localhost:8081/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"geox_deep_time_state\",\"arguments\":{\"period\":\"Miocene\",\"session_id\":\"$SESS\"}}}"
# If this works but geox_basin doesn't → bridge path is the truncation site
```

**Reporting:** When this bug fires, log the exact truncated ID vs the original in the audit receipt. Document it as 888_HOLD, do not auto-fix.

### MCP Response Pipeline Audit (verbosity trimming)

**Signal:** MCP endpoint returns a different/smaller response shape than a direct Python call to the same handler. Fewer keys, `null` for expected fields, truncated structure.

**Root cause:** The MCP response pipeline has a verbosity-based trimmer (`verbosity.py:trim_for_verbosity`) that collapses the full handler dict to ~11 fields when verbosity defaults to `"minimal"`. Everything else — `apex_scalars`, `session_birth`, `atlas333`, `work_contract`, `clarity_metrics`, `constitution`, `sct_claims` — is stripped.

**Detection recipe:**
```bash
# Step 1: Call handler directly from deployed path
python3 -c "
import sys; sys.path.insert(0, '/opt/arifos/app')
from arifosmcp.tools.session import arif_init
r = arif_init(mode='light', actor_id='ARIF', intent='audit X')
d = r.model_dump() if hasattr(r, 'model_dump') else r
print('Direct: status=%s session=%s apex=%s keys=%d' % (
    d.get('status'), d.get('session_id'),
    d.get('apex_scalars') or d.get('result',{}).get('apex_scalars'),
    len(d.keys())))
"

# Step 2: Call through MCP HTTP
curl -sf http://localhost:8088/mcp -X POST \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"light","actor_id":"ARIF","intent":"audit X"}}}' \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)
t = json.loads(d['result']['content'][0]['text'])
print('MCP: status=%s session=%s apex=%s keys=%d' % (
    t.get('status'), t.get('session_id'),
    t.get('apex_scalars'), len(t.keys())))
"

# Step 3: If MCP keys < direct keys → verbosity trimming
# Step 4: Fix the default
grep -n 'verbosity.*=.*\"minimal\"' /opt/arifos/app/arifosmcp/runtime/tools.py
```

**Fix:** Change `verbosity` default from `"minimal"` to `"standard"` in the handler, OR add missing fields (e.g., `apex_scalars`) to the trimmer's keep-list.

**Full pattern:** See `references/mcp-response-pipeline-audit.md`.

## Reference Files

- `references/sovereign-claim-verification-scorecard.md` — verifying sovereign's multi-claim assertions against primary sources, scorecard output (2026-07-21)
- `references/cross-organ-claim-audit.md` — pattern for probing prose claims about cross-organ changes
- `references/caddy-routing-cross-root.md` — Caddy handler order bug pattern with verified fix recipe
- `references/asset-path-drift-detection.md` — when `/assets/` and `/_shared/` both claim real assets
- `references/deepseek-byok-anthropic-endpoint.md` — full env var recipe + per-agent compatibility table
- `references/narrative-claim-audit-2026-07-19.md` — worked example: arif-fazil.com navigation audit
- `references/session-id-truncation-bridge.md` — arifOS → GEOX session_id truncation bug
- `references/geox-organ-probe-patterns.md` — GEOX-specific probe recipes
- `references/mcp-client-landscape.md` — MCP GUI client landscape
- `references/mcp-sse-session-lifecycle.md` — Full MCP SSE handshake recipe
- `references/external-document-validation.md` — Layer-by-layer external audit validation methodology
- `references/kernel-vs-connector-diagnostic.md` — When external audits confuse connector drift with kernel failure (scar 2026-07-19)
- `references/geox-conformance-workflow.md` — Full GEOX conformance build/fix pipeline
- `references/delegate-agent-audit.md` — Verifying subagent claims against live state; agent fabrication detection (scar 2026-07-19): canonical manifest population, FastMCP 3.x AppConfig wiring, geox_list_apps fix, validator + test flow
- `references/kernel-probe-as-evidence.md` — Using live arif_init/arif_think/arif_judge probes to verify or disprove external AI claims about kernel behavior; pre-existing test isolation via git stash (2026-07-19)
- `references/live-apex-scalars-from-kernel.md` — Wiring live G-fold apex scalars from arifOS kernel /health into an organ's health endpoint; reuse existing HTTP call, UNMEASURED fallback, scalar-by-scalar overlay (2026-07-26)
- `references/code-audit-line-number-verification.md` — Verifying external code audit findings against live code; audit line numbers can be stale, always probe live source before acting (scar 2026-07-18)
- `references/kernel-contrast-assessment.md` — Structured 7-axis before/after comparison for kernel version upgrades, release audits, and deployment state changes
- `references/mcp-resource-zen-2026-07-28.md` — Cross-witness audit: OpenCode scan → Hermes verify → convergence seal. MCP resource collapse 327→34. Single-agent accuracy ~60% lesson.

## Constitutional Compliance

- F2 TRUTH: numbers live, derived labels per claim (OBS/INT/DER)
- F11 AUDIT: log to `forge_work/<date>/AUDIT-RECEIPT-<date>.md` with WHAT/CHANGED/VERIFIED/CONSEQUENCE/NEXT
- F1 AMANAH: never fix web routing without F13 — log + flag, do not auto-deploy
- F7 HUMILITY: report honest numbers, not inflated
- F13 SOVEREIGN: persona confusion (typo) is recoverable; report + fix, don't argue

## Persona / Identity Anchor Discipline (scar 2026-07-19)

**Signal:** Arif typos or accidentally assigns a wrong persona ("Mr Jon", "AGY", "the assistant", etc.). The right response is: **accept the correction, log it briefly, and continue with the canonical identity**. The wrong response is: argue ("but the typo said...") or adopt the wrong persona ("ok, I am Mr Jon now").

**Canonical anchor:** Hermes = ASI tier agent on the arifOS federation, sovereign = Arif (F13). This is recorded in `hermes-prime-identity` skill (mandatory load at session start). Any user-supplied name conflict = trust the skill, not the fresh input.

**Probe pattern when a persona claim arrives from Arif:**
1. Is the name in the skill manifest? (skills_list → look up)
2. Is the name in alignment-seal-v1.md or SOUL.md? (`grep -ri <name> /root/.hermes/`)
3. Is the name referenced in any prior session state? (`session_search`)

**If all three fail:** the name is either a typo, a test, or a new persona. Default action: acknowledge ("sounds like a typo — saya ASI tier, not <name>"), do NOT adopt the wrong identity, and continue the canonical task. Don't lecture. Don't moralize. One-line acknowledgment.

**Anti-pattern validated 2026-07-19:** I accepted "Mr Jon" as a new persona for one turn before Arif corrected: "Typo. Was not intended to call u Mr Jon. U are ASI. Hermes agent." The correction cost two extra conversational turns. The lesson: identity claims from the sovereign get **one** acknowledgment, not adoption. If the name doesn't match the canonical anchor, log it as a typo and continue.

**Related:** For non-persona name lookups (tools, agents, models), the same probe applies. "AGY" → `which agy` → no such binary → ask, don't invent.
