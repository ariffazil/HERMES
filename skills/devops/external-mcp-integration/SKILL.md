---
name: external-mcp-integration
description: "Evaluate, install, wire, and verify third-party MCP servers into the arifOS federation. Covers"
tags: [mcp, integration, external-tools, federation, multi-agent, pipx]
triggers:
  - "wire this MCP"
  - "add this tool"
  - "integrate this server"
  - "install this MCP"
  - "connect this to Hermes"
  - "deploy this to [VPS]"
  - external GitHub repo shared as MCP server
---

# External MCP Integration

Pattern for evaluating, installing, and wiring a third-party MCP server into the arifOS federation — Hermes, Kimi Code, OpenClaw, Claude Code, OpenCode, Gemini CLI, Cursor, and across VPS nodes. Applies when Arif shares a repo/package and says "wire it."

## Workflow

### 0. Quarantine — Sandbox Evaluation (Required Pre-Step)

**Before any install, the tool must pass mcp_sandbox_eval.py.** This is the arifOS sandbox doctrine: we quarantine the *tool* at intake, not the *agent* at runtime. See `skill_view(name='governance-patterns', file_path='SKILL.md')` section "Sandbox Doctrine" for the architectural rationale.

The sandbox eval runs four stages:

| Stage | Verifies | Why |
|-------|----------|-----|
| 1. Containment | Binary runs in isolated container without production access | Prevents data leak / system mutation during testing |
| 2. Handshake | JSON-RPC 2.0 transport, auth, connection stability | Ensures tool doesn't crash-loop on init |
| 3. Floor Scan | Tool definitions against F1/F2 invariants: path isolation, network gating, schema correctness | F2 TRUTH — claims match source code |
| 4. Stress Test | Error handling, token load, oversized output, edge-case inputs. **Proven case study:** SylphxAI/pdf-reader-mcp passed Stage 1-3 (schema declared `url XOR path`) but failed Test 4.10 — Rust runtime (`ureq`) initiated outbound HTTPS when `url:` was passed. Zod `.refine()` ≠ runtime sandbox. | F4 CLARITY — no entropy introduction |\n\n**⚠️ Critical lesson (proven 2026-07-28):** Stage 4 is non-negotiable. Never trust marketing copy or Zod schema definitions. Verify execution at the socket. See `references/sylphx-intake-case-study.md`.

**PASS** → proceed to Evaluate + Install
**FAIL** → reject or isolate further; do not register

**F1 Safety hard blocks** for any MCP server that:
- Accepts `url:` parameter (must be path-only unless explicitly approved by 888)
- Lacks schema validation on outputs
- Exposes write/delete capability without explicit `ack_irreversible`

**For first-time integrations:** Register with OBSERVE/SUGGEST scope only (read-only extraction, advisory output). Expand scope only after 30-day observation window and explicit 888 approval.

### 0b. Evidence Pinning & Rejection Receipt (Required on FAIL)

When a tool **FAILS** quarantine (especially on F1 CRITICAL), seal the evidence as a permanent artifact. This prevents "did we test X?" questions later and proves the intake caught what it claims.

**SHA-256 evidence chain pinning:**

The eval report generated during Stage 4 is the primary evidence. But the report itself may have `lock_metadata` appended after the initial generation (disposition, doctrine violations, SHA-256 pin). This changes the current file hash from the original — both must be recorded:

```bash
# Capture original hash at time of eval (before any metadata appended)
original_hash=$(sha256sum <eval_report.json> | cut -d' ' -f1)
# Store it in the report's lock_metadata.original_sha256_pre_lock field

# Later, when verifying:
current_hash=$(sha256sum <eval_report.json> | cut -d' ' -f1)
echo "Original (pre-lock): $original_hash"
echo "Current:             $current_hash"
```

**F1_REJECTION_RECEIPT — structured rejection artifact:**

After a FAIL verdict, create a structured JSON receipt alongside the eval report. Template:

```json
{
  "receipt_type": "F1_REJECTION_RECEIPT",
  "dossier_id": "DOSSIER-YYYYMMDD-<TOOL>-CLOSEOUT",
  "authority": "888_SOVEREIGN",
  "target": "<org>/<repo>@<version>",
  "disposition": "OPTION_A_PERMANENT_HOLD",
  "status": "PERMANENT_QUARANTINE",
  "federation_mutation": "ZERO",
  "evidence": {
    "stage_4_report": "<eval_report_path>",
    "original_sha256_pre_lock": "<sha256>",
    "current_sha256": "<sha256>",
    "sha256_note": "Current hash differs from original because lock_metadata block was appended after initial generation"
  },
  "failure_detail": {
    "test": "<test_id> — <test_name>",
    "severity": "F1_CRITICAL",
    "latency_ms": <N>,
    "what_happened": "<plain-text description of what the tool actually did>",
    "doctrine_violated": ["F1_AMANAH", "LOCALHOST_IS_PASSWORD"],
    "verdict": "<one-line ultimate verdict>"
  },
  "rollback_actions": [
    "uninstall ... (confirmed)",
    "sandbox purged (confirmed)",
    "Zero entries in mcp.json",
    "Zero federation mutation"
  ],
  "doctrine_vindication": "<how the intake proved its own value>",
  "seal_chain": {
    "eval_report": "<path>",
    "rejection_receipt": "<path>"
  }
}
```

**SEAL_RECEIPT — assembly verification artifact:**

After all intake components are assembled (evidence, receipts, doctrine), create a SEAL_RECEIPT.md as the permanent assembly checklist. Include artifact map diagram, full checklist with verification evidence, and rollback procedure.

**Proven case study:** SylphxAI/pdf-reader-mcp v4.1.2 intake, 2026-07-28. Test 4.10 `url_xor_schema_rejection` caught at Stage 4 — Sylphx accepted `url:` and made outbound HTTPS (33ms to example.com). Zod `.refine()` only caught BOTH-or-NEITHER, not `url:`-only. Full evidence chain: original SHA-256 (`33a2b3f2...`) → lock metadata → current SHA-256 (`a1266117...`). F1_REJECTION_RECEIPT.json + SEAL_RECEIPT.md + EUREKA doctrine (GENESIS #057) forged as permanent artifacts.

### 1. Evaluate

Before installing, read the README and pyproject.toml/package.json:

- **License**: MIT/Apache-2.0 preferred. AGPL-3.0 acceptable. Proprietary → flag.
- **Cost**: $0/free preferred. Paid → flag with monthly estimate.
- **Capabilities**: What tools does it expose? What does it replace or augment?
- **Dependencies**: Does it need a browser engine? System packages? GPU?
- **Fit**: Does it overlap with existing federation organs? Complement them?

### 2. Install

**Python packages → pipx (preferred)**. The system Python is externally managed (PEP 668). pipx creates an isolated venv.

```bash
pipx install <package>[extras]     # e.g. pipx install hound-mcp[all]
```

**Fallback: system pip** when pipx is unavailable or fails with dependency conflicts:

```bash
pip install --break-system-packages hound-mcp[all]
```

**Browser engines**: If the MCP server uses Playwright/Patchright:

```bash
playwright install chromium
```

### 3. Wire to Federation

**For Hermes (stdio transport)** — use CLI, never hand-edit config.yaml:

```bash
echo "Y" | hermes mcp add <name> --command <command>
```

**For Kimi Code / other agents with mcp.json** — add launcher script + config entry:

```bash
# Create launcher: /root/.arifos/agents/<agent>/mcp-launchers/<name>.sh
echo '#!/usr/bin/env bash
exec <name>' > "/root/.arifos/agents/<agent>/mcp-launchers/<name>.sh"
chmod +x "/root/.arifos/agents/<agent>/mcp-launchers/<name>.sh"
```

Then add to mcp.json or equivalent per-agent config.

**For OpenClaw MCP catalog** — edit:
`/root/.openclaw/workspace/openclaw/exports/mcp-catalog-v1.json`

```json
{
  "server_id": "<name>-mcp",
  "enabled": true,
  "auto_start": true,
  "transport": "stdio",
  "command": "<name>",
  "tool_count": <N>,
  "categories": ["web", "search", "fetch", "research"]
}
```

**Create launchers for all agent homes at once:**
```bash
for agent in kimi claude opencode gemini cursor; do
    dir="/root/.arifos/agents/$agent/mcp-launchers"
    mkdir -p "$dir"
    echo '#!/usr/bin/env bash
exec <name>' > "$dir/<name>.sh"
    chmod +x "$dir/<name>.sh"
done
```

**Update agent docs:** Add the server name to the MCP servers list in each `/root/.arifos/agents/<agent>/AGENTS.md`.

### 4. Cross-VPS Deployment

When a tool must run on another federation VPS (e.g., A-FLOW for WawaBot):

```bash
# 1. SSH to remote
ssh root@<REMOTE_IP>

# 2. Install (same as local — check pipx vs pip)
python3 --version
pip install --break-system-packages <package>[extras]
playwright install chromium

# 3. Verify
<name> --version

# 4. Wire to remote agent configs (same pattern as §3)
# 5. End-to-end test via MCP init sequence
```

### 5. Gateway Restart (Hermes only)

**Cannot restart from within the gateway process.** Options:
- **Cron-based**: One-shot cron job that restarts gateway, then user does `/new`.
- **External shell**: Separate SSH session or tmux pane.
- **Wait for next `/new`**: Tools available on next session without restart.

### 6. Validate-After-Write

**CRITICAL RULE: After any config write, immediately validate.** The third time an agent writes a broken config is the symptom of a missed invariant. Apply the cheapest validation available for each runtime:

| Runtime | Validate command | Schema pitfall |
|---------|-----------------|----------------|
| Hermes config.yaml | `hermes config get` | CLI wrapper handles quoting |
| OpenCode opencode.json | `opencode run "test"` | `tools` must be OBJECT `{"name": true}`, not array `["name"]` |
| OpenClaw openclaw.json | `systemctl restart openclaw-gateway.service` | SecretRefResolutionError if env var missing |
| Kimi Code config.toml | `kimi-code --help` or headless launch | model_id string must match provider key |
| Agent mcp.json | Launch MCP server and probe `tools/list` | JSON schema may differ per agent |

**Ghost tool detection:** The runtime may accept config with phantom tool names. Always probe actual MCP servers via `tools/list` after wiring and compare tool IDs against what the config references. Tool names from MCP servers do NOT carry provider prefixes — `understand_image` from minimax MCP, NOT `minimax_understand_image`.

**Rollback protocol:** `cp <config>.bak-$(date +%s) <config>` before editing. If validate fails, `cp <bak> <config>` to restore.

### 7. Custom MCP Server Deployment (from-scratch)

When building a custom MCP server (not wiring a third-party package), the canonical example is Mage-Flow at `/opt/mage-server/`. Pattern:

```
/opt/<name>/
├── main.py          # FastMCP server (tools, helpers, config)
├── run.sh           # sources vault.env, exec main.py
└── requirements.txt # if needed
```

**Registration** uses the same commands as third-party stdio servers (§3):
```bash
hermes config set mcp_servers.<name>.command "/opt/<name>/run.sh"
hermes config set mcp_servers.<name>.enabled true
hermes config set mcp_servers.<name>.timeout 120
```

**For GPU-backed tools** (image generation, ML inference), the local VPS has no NVIDIA GPU. Pattern is Modal serverless — see `references/modal-gpu-deployment.md`.

### 7b. Value-First Communication Rule

When reporting on any integration or deployment task, lead with what changed for the user, not what you did. The user processes deltas in their capability, not process narration.

| Bad (process-focused) | Good (value-focused) |
|---|---|
| "I wired the MCP server to Modal" | "mage_generate now runs on Modal GPU — ~1s/image when queue clears" |
| "Cloudflare Workers AI research done" | "3 free models ready (Llama 3.3 70B, Qwen3 30B, Mistral 24B) — just need token scope fixed" |
| "Modal scaffolding built" | "Mage-Flow deployed on serverless GPU — $0 idle cost" |

Apply to all user-facing status reports across federation development skills. When the user asks "So what?" the answer must be a concrete capability delta, not a step replay.

### 8. Docker-Deployed MCP Servers (Streamable HTTP)

Some MCP servers ship as containers, not pipx packages — typically Next.js apps with built-in MCP endpoints (deep-research, flowise, etc.).

**Deploy pattern:**

```bash
docker run -d --name <name> --restart unless-stopped \
  -p <port>:3000 \
  -e ACCESS_PASSWORD="<generated-password>" \
  -e API_KEY_ENV="${VAULT_VAR}" \
  <image>:latest
```

**SearXNG bridge for search-dependent servers:**

If the server needs web search and we have SearXNG running on host `:8080`:

```bash
docker run -d ... \
  -e SEARXNG_API_BASE_URL="http://host.docker.internal:8080" \
  -e MCP_SEARCH_PROVIDER="searxng" \
  <image>:latest
```

`host.docker.internal` resolves to the Docker host. Test connectivity before deploying:
```bash
docker run --rm alpine curl -s -I http://host.docker.internal:8080 | head -n 1
# Expect: HTTP/1.1 200 OK
```

**Bearer auth in Hermes mcp_servers config:**

Since Hermes config.yaml is CLI-managed (not hand-edited), use `hermes config set`:

```bash
hermes config set mcp_servers.<name>.url http://localhost:<port>/api/mcp
hermes config set mcp_servers.<name>.transport streamable-http
hermes config set mcp_servers.<name>.timeout 600
hermes config set mcp_servers.<name>.headers.Authorization 'Bearer <password>'
hermes config set mcp_servers.<name>.description "..."
```

`headers.Authorization` sends the Bearer token on every request. The `timeout` MUST be set high (300-600s) for research-type MCP servers — deep research pipelines with iterative search + LLM calls regularly exceed the default 60s.

**Validate after config:**
```bash
hermes config get mcp_servers.<name>
# Confirm url, transport, timeout, headers all present
```

New session will auto-load. No restart needed if using `hermes config set`.

**Verification via curl (before registering):**
```bash
curl -s -w "\nHTTP:%{http_code}" \
  -H "Authorization: Bearer <password>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  http://localhost:<port>/api/mcp
# Expect: HTTP:200 + JSON with tools array
```

For deep-research specifically, see `references/deep-research.md`.

### 8b. OAuth-Authenticated MCP Servers (Streamable HTTP)

Some MCP servers (e.g. OpenRouter MCP at `mcp.openrouter.ai/mcp`) require OAuth 2.1 PKCE approval — Bearer token alone is insufficient. The OAuth flow triggers when the MCP server returns a 401 with a `WWW-Authenticate: Bearer resource_metadata="..."` header pointing to the OAuth protected resource metadata endpoint.

**OpenRouter MCP specific OAuth endpoints** (discovered via `.well-known/oauth-authorization-server`):

| Endpoint | URL |
|----------|-----|
| Authorization | `https://mcp.openrouter.ai/oauth/authorize` |
| Token exchange | `https://mcp.openrouter.ai/oauth/token` |
| Client registration | `https://mcp.openrouter.ai/oauth/register` |
| PKCE method | `S256` (required) |
| Grant type | `authorization_code` |
| Token auth | `none` (PKCE handles auth) |

**Registration — `auth: oauth` is mandatory:**

Without it, `hermes mcp login <name>` never triggers the OAuth flow:

```bash
hermes config set mcp_servers.<name>.url https://<host>/mcp
hermes config set mcp_servers.<name>.transport streamable-http
hermes config set mcp_servers.<name>.auth oauth
hermes config set mcp_servers.<name>.timeout 30
```

**OAuth flow steps:**

1. Register server with `auth: oauth` in config
2. Run `hermes mcp login <name>` from an **interactive terminal** that can open a browser — this starts a local callback server and opens the authorization URL
3. Approve in browser — redirect goes to `http://localhost:<random_port>/callback` (Hermes handles this)
4. Token is cached at `$HERMES_HOME/mcp-tokens/<name>.json` — reconnect doesn't need re-approval
5. Token has a TTL; Hermes auto-refreshes via the SDK's OAuthClientProvider

**Pre-requisite:** The old leaked management key (if any) must be disabled at the provider's web UI first. OAuth approval while a leaked key is still live is a security regression.

**Bypass TTY check (headless environments):**

The MCP SDK refuses OAuth in non-interactive environments via `_is_interactive()` (checks `sys.stdin.isatty()`). To force the flow in a script/headless context:

```python
from tools.mcp_oauth import force_interactive_oauth
from tools.mcp_oauth_manager import MCPOAuthManager
from hermes_cli.mcp_config import _get_mcp_servers

servers = _get_mcp_servers()
entry = servers['openrouter']

with force_interactive_oauth():
    manager = MCPOAuthManager()
    provider = manager.get_or_build_provider(
        'openrouter',
        entry['url'],
        entry.get('oauth', {})
    )
    # Provider built — client registered with OR
    # Actual browser approval still needed for initial token
```

The `force_interactive_oauth()` context manager sets `_oauth_interactive_forced` ContextVar to `True`, bypassing the TTY check. This gets past the "non-interactive environment" gate but still requires browser-based approval for the initial authorization token.

**OpenRouter MCP OAuth vs Management API — they are separate:**

The MCP server at `mcp.openrouter.ai/mcp` uses its own OAuth PKCE flow, NOT the Management API key. The Management key (`OPENROUTER_MANAGEMENT_KEY`) is for the REST API at `openrouter.ai/api/v1/keys` (sub-key management, guardrails provisioning). The MCP OAuth flow registers a client application and gets a token scoped to MCP operations (model discovery, credit monitoring, benchmarks). These are independent auth domains — you can have one work without the other.

**⚠️ Pitfall: `auth: oauth` silently accepted but never triggered.** Config without `auth: oauth` accepts the entry but the OAuth flow never starts — the MCP server appears registered but tools never load. Always verify by (1) checking token file: `ls $HERMES_HOME/mcp-tokens/<name>.json`, and (2) calling `tools/list` via MCP client after first connect. If token file is empty/missing, the browser approval step was never completed.

**⚠️ Pitfall: Non-interactive trap.** `hermes mcp login <name>` in a cron job, SSH session without TTY allocation, or hermes agent session will fail with "non-interactive environment and no cached tokens found" because `_is_interactive()` returns False. The token MUST be created from a real interactive terminal session first. Once cached on disk, subsequent reconnects (even non-interactive) work because the token file exists and passes the `has_cached_tokens()` check.

**⚠️ Pitfall: Token refresh expiry.** The cached token file contains `expires_in`, `access_token`, `refresh_token`, and `expires_at` (absolute Unix epoch). If `expires_at` is in the past, the provider auto-refreshes via the SDK. But if the refresh token also expired (OAuth provider policy), a new interactive login is required. Check with:
```bash
python3 -c "import json;
t=json.load(open('$HERMES_HOME/mcp-tokens/openrouter.json'));
print(f'Expires at: {t.get(\"expires_at\",\"none\")}')"
```

### 9. Verify (Stdio Servers)

After wiring, test end-to-end:

```python
# MCP init → tools/list → call primary tool
import subprocess, json, time
proc = subprocess.Popen(["<name>"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
# Init + tools/list + tool call...
```

**Important:** Some MCP servers prefix tools internally (e.g., `mcp_smart_fetch` not `smart_fetch`). Always probe `tools/list` before calling. Check the `stderr` output too — some servers route tool responses there.

## Provider Key Wiring (API Keys Across Agents)

When adding a new API provider (e.g., MiMo Token Plan), the key must be wired to Hermes (providers in config.yaml) AND OpenClaw (providers in openclaw.json), plus tested before declaring done.

### Hermes Provider Config

**Fix a miswired provider's key_env:**
```bash
hermes config set providers.<provider-name>.key_env <ENV_VAR>
# e.g. hermes config set providers.xiaomi-mimo.key_env MIMO_API_KEY
```

**Common gotcha:** A provider may have the right base URL and models, but point to an empty or wrong env var (`XIAOMI_API_KEY=""` instead of `MIMO_API_KEY`). Always test the key with a live API call before declaring wired.

**View provider chain:**
```bash
grep -A30 'fallback_providers:' ~/.hermes/config.yaml
```

### OpenClaw Provider Config

OpenClaw's model providers live in `/root/.openclaw/openclaw.json` under `models.providers`. Each provider has:

```json
{
  "baseUrl": "https://token-plan-sgp.xiaomimimo.com/v1",
  "apiKey": "${MIMO_API_KEY}",
  "api": "openai-completions",
  "models": [
    {
      "id": "mimo-v2.5-pro",
      "name": "MiMo V2.5 Pro (Token Plan)",
      "reasoning": true,
      "input": ["text"],
      "contextWindow": 1048576,
      "maxTokens": 131072
    }
  ]
}
```

**Edit pattern:** Python one-liner to add a provider, then `systemctl restart openclaw-gateway.service`.
```bash
cat /root/.openclaw/openclaw.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
d['models']['providers']['NEW_NAME'] = { ... }
json.dump(d, open('/root/.openclaw/openclaw.json','w'), indent=2)
"
```

**Restart after config change:**
```bash
systemctl restart openclaw-gateway.service
```

### Key Verification (Always Test Before Claiming Wired)

```bash
source /root/.secrets/vault.env
curl -s --max-time 10 "$BASE_URL/models" \
  -H "Authorization: Bearer $API_KEY" | python3 -c "
import json,sys; d=json.load(sys.stdin)
models=d.get('data', d.get('models',[]))
print(f'{len(models)} models:', [m.get('id','?') for m in models[:5]])
"
```

Do NOT declare a key "wired" without a live API test. "Quota exhausted" = not usable, even if config is correct.

## 10. Manufact Cloud (mcp-use) Deployment

Manufact (acquired Smithery) hosts MCP servers from GitHub repos at `manufact.com`. arifOS and GEOX are deployed there as public endpoints.

### CLI Setup

```bash
npm install -g @mcp-use/cli
npx @mcp-use/cli login --api-key "mcp_xxx..."   # from dashboard
npx @mcp-use/cli whoami
```

### Key Commands

| Action | Command |
|--------|---------|
| List servers | `npx @mcp-use/cli servers list` |
| Server details | `npx @mcp-use/cli servers get <id-or-slug>` |
| List deployments | `npx @mcp-use/cli deployments list` |
| Deployment details | `npx @mcp-use/cli deployments get <deployment-id>` |
| Restart/redeploy | `npx @mcp-use/cli deployments restart <deployment-id>` |
| Follow build logs | `npx @mcp-use/cli deployments restart <deployment-id> --follow` |
| Server env vars | `npx @mcp-use/cli servers env list --server <uuid>` |
| Dashboard | `https://manufact.com/cloud/servers/<server-id>` |

### Deploy Config

Manufact reads `smithery.yaml` from the GitHub repo root (legacy Smithery format auto-generated by `scripts/sync_kernel_abi.py`). Version follows the federation Iron Rule — `vYYYY.MM.DD` only. Source of truth: `KERNEL_ABI_VERSION` in `kernel_abi.py` + `abi_version` in `capability_registry.json`.

### Auto-Deploy

Auto-deploys from the linked GitHub repo on every push to main. No manual trigger. Status: `building` → `running` or `failed` (5-10 min, longer with big ML packages).

### Common Build Failures

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `ModuleNotFoundError: No module named 'scipy'` | Dockerfile import check (`import scipy, torch, transformers`) but `pip install .` skips optional extras | Use `pip install .[heavy,ml]` or drop scipy/torch from the validation step |
| Build hangs >10min | Large ML packages (torch ~2GB) | Slim Dockerfile for Manufact — ML runs on local Ollama |
| Port mismatch | Manufact expects server on port 3000 | Ensure Dockerfile CMD starts on `0.0.0.0:3000` |

### Known State (2026-07-24)

- **arifOS** (`c764a8e3`): 🗑️ **deleted** — 1,420 deployments mostly failing. Python/uv build incompatible with Manufact's TS-first pipeline. See Pitfalls.
- **GEOX** (`95266f6f`): ✅ running — 625+ deployments stable. Python-based but built differently.
- **⚠️ No env vars set** on Manufact — Python repos needing 143 vault.env vars won't build properly on Manufact.

### Auto-Discovery Mechanism

Manufact discovers MCP servers through standard web crawling:

1. Scans `llms.txt` files at known domains
2. Checks `.well-known/mcp.json` for MCP server manifests (endpoint, routing, capabilities)
3. If the Manufact GitHub App is installed on the linked repo + `smithery.yaml` exists, auto-creates a server and deploys

This is how arifOS and GEOX ended up on Manufact. `mcp.arif-fazil.com/.well-known/mcp.json` was scraped, pointing to `ariffazil/arifos` and `ariffazil/GEOX` repos. The Manufact GitHub App had access, so servers were auto-created from those repos.

**To prevent unwanted auto-registration**, add a `discovery` block to `.well-known/mcp.json`:

```json
{
  "discovery": {
    "registry": "self-hosted",
    "auto_register": false,
    "note": "Self-hosted on sovereign infrastructure. External registration not required."
  }
}
```

This may not stop all crawlers, but signals intent for standards-compliant platforms.

### Delete a Server (non-interactive)

```bash
mcp-use servers rm <id> -y   # force delete without TTY prompt
```

Required in headless/agent environments — the default prompt expects interactive Y/N confirmation.

### Pitfalls — Python servers on Manufact

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Repeated build failures | Manufact is TS-first; Python/uv builds often fail silently | Check build logs via dashboard at `https://manufact.com/cloud/servers/<id>` |
| No logs for failed deployment | Build failed at git clone/resolution stage before logging started | Fix must be in Dockerfile or build commands — no log trail |
| Missing ML packages | `pip install .` skips optional extras declared in pyproject.toml | Use `pip install .[heavy,ml]` or drop ML from validation step |

## Pattern-Absorb Decision Framework

**Before integrating any external tool, ask: do we need a package manager, or just a registry?**

### Case Study: Furi (2026-07-26)

Furi is a CLI + HTTP API for managing MCP servers — GitHub install, PM2 process control, SSE aggregation, tool discovery. It solves "one place to install and operate MCP servers."

**Decision: Skip.** Not because it's bad, but because this federation has zero external MCP servers. What it needs is a *registry* for its 6 native organs, not a *package manager* for third-party packages.

**Decision framework:**

```
┌─ Does it solve a problem we actually have?
│  Furi: "manage MCP servers" → we have 0 external MCPs
│  Need: "discover tools across 6 organs" → 1 resource needed
├─ Can we build it natively?
│  arifos://tools/registry — ~100 lines Python, 0 new deps
│  Furi — BSL 1.1 license, PM2 dependency, new infra
├─ What's the pattern we actually need?
│  Not: package manager for external MCPs
│  But: unified tool discovery for federation organs
└─ Decision: Skip integration. Absorb pattern into native.
   Built: arifos://tools/registry (6/6 organs, 128 tools, 5s TTL cache)
```

### When to Integrate vs When to Build Native

| Scenario | Integrate | Build Native |
|----------|-----------|--------------|
| Solves a problem we *actually* have | ✅ If license/cost acceptable | Only if faster |
| Solves a problem we *might* have | ❌ Wait | ❌ Wait |
| Duplicates existing capability | ❌ | ✅ Absorb pattern |
| Requires new protocol/dependency | ❌ Evaluate first | ✅ If ≤200 lines |
| Restrictive license (BSL, AGPL-prod) | ❌ Production blocked | ✅ Forge native |
| Solvable in ≤100 lines | ❌ | ✅ Always |

**Key insight:** "Furi is a good tool for a different architecture. Our architecture needs a registry, not a package manager."

## Pitfalls

- **OpenClaw startup fails without vault.env**: OpenClaw auto-detects models on boot and requires their API keys in the environment. If a model references e.g. `OPENROUTER_API_KEY` and it's not set, the gateway startup fails with `SecretRefResolutionError`. **Fix:** Always start OpenClaw with secrets sourced:
  ```bash
  source /root/.secrets/vault.env && /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway
  ```
  The gateway does NOT source vault.env itself.
- **Shared quota across VPSes**: When two VPSes use the same Token Plan key, they share the same quota pool. Exhaustion on one = exhaustion on both. Always check if the key matches before copying. See `references/mimo-token-plan.md`.
- **OpenClaw model rotation when provider dies**: When primary provider hits quota/rate limit, check what the working VPS uses and mirror. Edit `/root/.openclaw/openclaw.json` → `agents.defaults.model`, then restart with secrets sourced.
- **PEP 668**: Prefer pipx. Fall back to `--break-system-packages`.
- **Playwright unsupported OS warning**: Safe to ignore on Ubuntu 24.04.
- **Gateway restart from within**: Use `kill` + `nohup` for OpenClaw; Hermes needs external shell or `/new`.
- **Tool prefix mismatches**: Always verify via `tools/list` — some servers use `mcp_` prefix. **Crucially: MCP servers expose tools WITHOUT provider prefixes.** The minimax MCP exposes `understand_image`, NOT `minimax_understand_image`. The cloudflare MCP exposes `ai_image_generation`, NOT `cloudflare_ai_image_generation`. Agents that guess prefixed names will reference ghost tools. Probe first, reference exact names.
- **Config write protection**: Use `hermes mcp add` or `hermes config set`.
- **Cross-VPS key auth**: Ensure Ed25519 key accepted on remote first.
- **Provider key_env mismatch**: A provider pointing to empty/wrong env var fails silently — always live-test.
- **Docker MCP servers need Bearer auth in headers**: Containerized MCP servers behind `ACCESS_PASSWORD` won't auth automatically — `hermes config set mcp_servers.<name>.headers.Authorization 'Bearer <password>'` is required. Without it, MCP responds 401 and tools never load.
- **Timeout must be ≥300s for research MCP servers**: Default 60s kills deep research pipelines that do iterative search + LLM calls. Set `timeout: 600` in the mcp_servers entry.
- **Token Plan vs Platform API**: Separate endpoints, separate keys.
- **Session-based MCP servers need `Accept: application/json` header.** GEOX (:8081), WEALTH (:18082), and WELL (:18083) reject `tools/list` calls that omit this header. Proven 2026-07-28 during Sylphx integration work. Always include in curl probes and MCP dashboard queries.
- **searxng/.env is a symlink to vault.env**. `/root/searxng/.env → /root/.secrets/vault.env`. Modifying vault.env automatically updates searxng/.env — no separate file to patch. Symlinks always have permission `777` (kernel behavior). The actual target file's permissions are what matters (`/root/.secrets/vault.env` is `600 root:root`). Do NOT attempt chmod on symlinks — it only affects the symlink itself, not the target.

## References

- `references/deep-research.md` — Full deployment recipe, MCP tools, env vars, architecture zen for deep-research (u14app/deep-research).
- `references/hound.md` — Hound-specific evaluation, tools, federation wiring, and cross-VPS notes.
- `references/mimo-token-plan.md` — MiMo Token Plan vs Platform API endpoints, keys, provider wiring across Hermes + OpenClaw.
- `references/opencode-agent-config.md` — OpenCode config schema (tools→object), MCP tool name discovery via JSON-RPC, ghost tool detection, and the validate-after-write pattern.
