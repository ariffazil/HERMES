---
name: external-mcp-integration
description: "Evaluate, install, wire, and verify third-party MCP servers into the arifOS federation. Covers: pipx/pip install, multi-agent wiring (Kimi, OpenClaw, Claude, OpenCode, etc.), cross-VPS deployment, playwright/browser deps, verification."
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

### 7. Verify

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
- **Token Plan vs Platform API**: Separate endpoints, separate keys.

## References

- `references/hound.md` — Hound-specific evaluation, tools, federation wiring, and cross-VPS notes.
- `references/mimo-token-plan.md` — MiMo Token Plan vs Platform API endpoints, keys, provider wiring across Hermes + OpenClaw.
- `references/opencode-agent-config.md` — OpenCode config schema (tools→object), MCP tool name discovery via JSON-RPC, ghost tool detection, and the validate-after-write pattern.
