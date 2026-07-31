---
name: opencode-config-zen
description: "OpenCode provider, model, agent, and rules configuration — SOT-driven rendering, graceful degradation fallback chains, schema compliance, and drift verification"
tags: [opencode, config, providers, models, agents, sot, rendering, drift-detection]
triggers:
  - "opencode config"
  - "zen opencode"
  - "fix opencode"
  - "align opencode models"
  - "opencode providers"
  - "opencode agents"
  - "opencode rules"
  - "SOT rendering"
  - "opencode drift"
  - "opencode_render.py"
  - "federation-model-sync"
  - "AGENT_MODEL_MAP opencode"
---

# OpenCode Config Zen — SOT-Driven Provider/Model/Agent Alignment

**Pattern:** Read AGENT_MODEL_MAP.json (the canonical SOT), map provider/model IDs to OpenCode provider keys, render a valid `opencode.json`, verify against live runtime.

## Architecture

```
/root/AAA/registries/models/AGENT_MODEL_MAP.json  (SOT — THE source of truth)
  │  symlinked as /root/.config/federation-models.json
  │
  ▼
/root/AAA/src/resolvers/opencode_render.py          (renderer)
  │
  ▼
/root/.config/opencode/opencode.json                (generated config — NEVER hand-edit)
  │
  ▼
opencode debug config                                (schema validation)
opencode models <provider>                           (runtime model list)
```

## Renderer Safety Protocol

The renderer implements a **4-mode safety gate**:

```bash
# Mode 1: DRY-RUN (default) — show diff, no mutation
python3 opencode_render.py

# Mode 2: STAGING — write to separate file for review
python3 opencode_render.py --staging /tmp/opencode.json.staging
diff -u /root/.config/opencode/opencode.json /tmp/opencode.json.staging

# Mode 3: WRITE WITH FORCE — requires --force (F1 AMANAH gate)
python3 opencode_render.py --write --force
# Auto-backup to _backups/opencode-{timestamp}.json + .sha256

# Mode 4: VERIFY — exit 0 if aligned, exit 1 if drifted
python3 opencode_render.py --verify || exit 1
```

**CI standing order:**
```
python3 opencode_render.py --verify || exit 1
# SOT change only:
python3 opencode_render.py
python3 opencode_render.py --write --force
```

## Workflow

### 1. Diagnose

Check current state before making changes:

```bash
# Schema validation
opencode debug config 2>&1 | head -5
# → Error: Unrecognized key → schema violation (remove that key)
# → Error: Invalid config → structural issue

# Agent model resolution
opencode debug config 2>&1 | python3 -c "
import sys, json
import re
raw = sys.stdin.read()
m = re.search(r'\{.*', raw, re.DOTALL)
if m:
    c = json.loads(m.group())
    for n, a in c.get('agent', {}).items():
        print(f'{n}: model={a.get(\"model\",\"(inherit)\")}')
"

# Provider model lists
opencode models deepseek 2>&1    # check primary provider alive
opencode models kimi 2>&1        # check vision provider
```

### 2. Render from SOT

```bash
# Dry-run (see changes without writing)
cd /root/AAA/src/resolvers && python3 opencode_render.py

# Write generated config
cd /root/AAA/src/resolvers && python3 opencode_render.py --write

# Verify drift
cd /root/AAA/src/resolvers && python3 opencode_render.py --verify
```

### 3. Verify Live

After any config change, verify:

```bash
# Config loads without schema errors
cd /root && source /root/.secrets/vault.env && opencode debug config 2>&1 | head -5

# Models resolvable
opencode models deepseek 2>&1 | grep -q 'v4-pro' && echo 'deepseek OK'
opencode models kimi 2>&1 | grep -q 'k3' && echo 'kimi OK'
opencode models opencode-go 2>&1 | grep -q 'kimi-k3' && echo 'opencode-go OK'

# No drift from SOT
cd /root/AAA/src/resolvers && python3 opencode_render.py --verify
```

## Provider → Model Mapping (SOT to OpenCode)

AGENT_MODEL_MAP.json uses its own provider_id and model_key format. The renderer translates these to OpenCode provider section keys and model IDs.

### Provider ID Translation

| SOT provider_id | OpenCode provider key | Notes |
|---|---|---|
| `deepseek` | `deepseek` | Direct match |
| `opencode-go` | `opencode-go` | Direct match |
| `kimi` / `kimi-moonshot` | `kimi` | REST API key (not OAuth) |
| `minimax` | `minimax` | Direct match |
| `ollama` | `ollama` | Local |
| `groq` | `groq` | Free tier |
| `gemini` | `gemini` | Free tier |
| `sea-lion` | `sea-lion` | Direct match |
| `cerebras` | `cerebras` | Direct match |
| `bailian-token-plan` | (no OpenCode equivalent yet) | Maps to kimi for kimi models |
| `glm` | `tokenrouter-arifos` | GLM served via TokenRouter |
| `mimo-platform` | `opencode-go` | MiMo models via Go subscription |
| `openai` / `xai` | `openrouter` | Via OpenRouter |
| `azure-openai` | `azure-openai` | Direct match |

### Model Key Translation

The SOT uses full model_key format like `deepseek/deepseek-v4-pro`. Some SOT model keys don't match OpenCode provider model IDs:

| SOT model_key | OpenCode reference | Reason |
|---|---|---|
| `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` | Kimi API returns `kimi-for-coding`, not `kimi-k2.7-code` |
| `glm/glm-5.2` | `tokenrouter-arifos/z-ai/glm-5.2` | GLM via TokenRouter |
| `mimo/mimo-v2.5-pro` | `opencode-go/mimo-v2.5-pro` | MiMo via Go subscription |
| `sea-lion/Qwen-SEA-LION-v4-32B-IT` | `sea-lion/aisingapore/Qwen-SEA-LION-v4-32B-IT` | Full path needed |
| Everything else | Same as SOT key | Direct match |

## Agent → Model Mapping

### From SOT (forge/auditor/ops/planner/recovery)

The SOT defines these agents with primary_model + fallback_chain. The renderer reads them and sets each OpenCode agent's `model` field.

| OpenCode Agent | SOT Source Agent | Model | 
|---|---|---|
| `forge` | `forge` | deepseek/deepseek-v4-pro |
| `auditor` | `auditor` | deepseek/deepseek-v4-pro |
| `ops` | `ops` | deepseek/deepseek-v4-flash |
| `planner` | `planner` | kimi/kimi-for-coding |
| `recovery` | `recovery` | ollama/qwen2.5-coder:3b |
| `opencode` (default) | `forge` | deepseek/deepseek-v4-pro |

### Special Agents (not in SOT)

These agent configs are maintained independently with hardcoded defaults:

| Agent | Model | Reason |
|---|---|---|
| `image-prompt-architect` | kimi/k3 | Vision capability; permission-gated (bash only) |

## OpenCode Schema Compliance

OpenCode validates config against a strict JSON schema. Unknown top-level keys cause rejection.

### Keys That WILL Be Rejected

- `_model_sot` — previously used as annotation, blocks all config loading
- `_generated` — auto-added by Python json.dump metadata
- Any non-standard key at the top level

**Fix:** Strip these keys before writing. The render script does this automatically.

### Deprecated Fields

- `agent.<name>.tools` — **deprecated** in OpenCode docs. Replace with `permission`.
  - OLD: `"tools": {"bash": true, "understand_image": true}`
  - NEW: `"permission": {"bash": "allow", "*": "deny"}`
  - Permission keys: `read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`, `todowrite`, `webfetch`, `websearch`, `lsp`, `skill`, `question`, `doom_loop`
  - Values: `"allow"` | `"ask"` | `"deny"`

### Agent Mode Values

- `primary` — switched via Tab key
- `subagent` — invoked via @mention or Task tool
- `all` (default) — both

## Graceful Degradation (Provider Fallback Chain)

OpenCode does NOT support model-level fallback lists. Degradation is achieved through:

1. **Primary → provider selection**: Use reliable primary (deepseek), fallback to others
2. **Agent hierarchy**: forge (flagship) → ops (fast) → recovery (local)
3. **provider ordering**: `enabled_providers` list determines load order

Recommended fallback chain:
```
deepseek/deepseek-v4-pro (flagship reasoning, CN, $7.06)
  → opencode-go/deepseek-v4-pro (Go subscription)
    → tokenrouter-arifos/deepseek-v4-pro (routing)
      → groq/llama-3.3-70b-versatile (FREE, US, limited)
        → gemini/gemini-2.5-flash (FREE, 1.5K/d)
          → ollama/qwen2.5-coder:3b (local, always works)
```

## Provider Ordering (Priority)

Providers are ordered by status from the SOT, then deduplicated and filtered:

1. deepseek (ACTIVE, prepaid $7.06) — PRIMARY
2. cerebras ($5 free credit) — TRIAL
3. gemini (FREE, 1.5K req/day) — FREE TIER
4. groq (FREE, 1K-14K req/day) — FREE TIER
5. kimi (REST API alive) — VISION
6. ollama (local, always works) — RECOVERY
7. opencode-go (Go subscription) — BACKUP
8. sea-lion (FREE, SG) — SEA LOCAL
9. openrouter (aggregator) — FALLBACK
10. minimax (RATE_LIMITED) — DEPRECATING
11. azure-openai (retiring Oct 2026) — LEGACY
12. tokenrouter-arifos (routing) — ROUTING

## OpenCode Rules / Instructions

OpenCode loads:

1. **AGENTS.md** — from project root AND `~/.config/opencode/AGENTS.md` (global)
2. **`instructions` field** in opencode.json — explicit file list, supports local paths and remote URLs
3. **CLAUDE.md** — Claude Code compatibility fallback (if no AGENTS.md found)

Instruction files are combined with AGENTS.md at session start. Remote URLs fetched with 5s timeout.

## Prompt Kernel Hooks (instructions field)

OpenCode loads **instruction files** at session start via the `instructions` field in `opencode.json`. These are the **prompt kernels** that define the agent's constitutional personality.

The renderer ALWAYS sets instructions from `render_instructions(sot)` — NEVER conditionally. If you see `if "instructions" not in config or not config["instructions"]:` in a render script, that's a BUG — instructions should be overwritten every cycle, not preserved.

### Kernel File List (12 files)

```
1.  /root/AAA/prompts/INIT.md
2.  /root/AAA/prompts/AAA-ZEN-ALIGNMENT.md
3.  /root/AAA/agents/opencode/AGENTS.md
4.  /root/AAA/agents/opencode/AUTONOMOUS_GOVERNANCE.md
5.  /root/AAA/agents/opencode/TOOLS.md
6.  /root/AAA/agents/opencode/IDENTITY.md
7.  /root/AAA/agents/opencode/BOOTSTRAP.md
8.  /root/AAA/agents/opencode/HEARTBEAT.md
9.  /root/AAA/agents/opencode/WORKFLOW.md
10. /root/AAA/skills/OPENCODE_SKILL_PROFILE.json
11. /root/AAA/registries/opencode_skills_alignment.yaml
12. /root/.config/opencode/rules/arifos-governance.md     ← Governance rules (canonical)
```

### Governance File Split-Brain (How to Resolve)

The renderer emits one governance file path in `instructions[]`. If a SECOND governance file exists elsewhere (e.g., at `~/.opencode/rules/arifos-governance.md`), OpenCode may load a stale copy alongside the canonical one.

**Detection:**
```bash
find /root -path '*.opencode/rules' -type d 2>/dev/null
find /root -not -path '*/forge_work/*' -name '*governance*' 2>/dev/null
```

**Resolution protocol:**
1. Pick ONE canonical path + ONE canonical name. Prefer `~/.config/opencode/rules/arifos-governance.md`
2. Archive duplicates in `~/.config/opencode/rules/_archive/{name}-{timestamp}Z.md`
3. Write `.sha256` alongside each archive entry
4. Remove the non-canonical file
5. Update `render_instructions()` in the renderer to emit the canonical path
6. Re-run `--write --force` + `--verify`

**The renderer's `instructions` field MUST be set unconditionally.** A common bug is:
```python
# ❌ BUG — preserves stale instructions when they have content
if "instructions" not in config or not config["instructions"]:
    config["instructions"] = render_instructions(sot)

# ✅ CORRECT — always overwrites from SOT
config["instructions"] = render_instructions(sot)
```

### Stale Model Reference Audit

After any model change in the SOT, the prompt kernel files can have stale hardcoded model names. The most common stale ref is the PLAN agent's model:

```bash
# Check all 12 kernel files for stale references
grep -rn "kimi-k2.7-code\|kimi/kimi-k2.7" \
  /root/AAA/prompts/ /root/AAA/agents/opencode/ \
  /root/AAA/skills/ /root/AAA/registries/opencode_skills_alignment.yaml \
  /root/.config/opencode/rules/arifos-governance.md 2>/dev/null
```

**Known stale refs found 2026-07-24 (all fixed):**

| File | Line | Old (broken) | New | 
|------|------|-------------|-----|
| `IDENTITY.md` | §Agent Table | `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` |
| `TOOLS.md` | §Model Rotation | `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` |
| `HEARTBEAT.md` | §Agent Cost | `kimi/kimi-k2.7-code` | `kimi/kimi-for-coding` |

**Pattern:** These files contain human-readable agent tables that duplicate model information from the SOT. They drift because they're manual markdown, not generated from SOT. When changing models, ALWAYS:
1. Update the SOT (AGENT_MODEL_MAP.json)
2. Re-run `opencode_render.py --write`
3. Audit the 3 `AAA/agents/opencode/*.md` files for stale model names in tables
4. Re-run `--verify`

## `--verify` as CI Gate

The `--verify` flag compares the generated config against the SOT and reports drift. Use this as a pre-deploy gate:

```bash
# Pre-deploy check
cd /root/AAA/src/resolvers && python3 opencode_render.py --verify
if [ $? -ne 0 ]; then
  echo "OpenCode config drifted from SOT — regenerate first!"
  python3 opencode_render.py --write
fi
```

The verify command checks:
- Agent model assignments match SOT
- Provider ordering follows SOT status
- `small_model` is the lightweight fallback
- No unknown top-level keys
- **Model IDs resolve through MODEL_KEY_TRANSLATION** (NEW: catches typos like `openrouter/auto-betax`)

## Governance Rules File

Location: `~/.config/opencode/rules/arifos-governance.md` (LOADED — canonical)
Archive: `~/.config/opencode/rules/_archive/` (for duplicates)

This file is loaded as the 12th instruction kernel. It contains:
- F1-F13 floor summaries (for agent reference)
- Model hierarchy with fallback chain
- Provider priority order with rationale
- Agent→model mapping table

The renderer emits this path via `render_instructions()`. No other governance file should exist in `.opencode/rules/` — that was the old location and caused split-brain.

**When updating the SOT**, this file should also be checked for model name consistency.

## Xlat Table Verification

The `MODEL_KEY_TRANSLATION` dict is strictly one-directional:

```python
# Only this call pattern exists — never reverse
MODEL_KEY_TRANSLATION.get(sot_key, sot_key)
# Returns OC value if sot_key in dict, otherwise sot_key unchanged
```

Identity mappings (same name in SOT and OC) are normal and harmless:
```python
"deepseek/deepseek-v4-pro" → "deepseek/deepseek-v4-pro"  # passthrough
"kimi/k3"                  → "kimi/k3"                   # passthrough
```

Real translations change the model name or provider prefix:
```python
"kimi/kimi-k2.7-code"       → "kimi/kimi-for-coding"       # Kimi API name mismatch
"glm/glm-5.2"               → "tokenrouter-arifos/z-ai/glm-5.2"  # different provider
"sea-lion/Qwen-SEA-LION-*"  → "sea-lion/aisingapore/Qwen-SEA-LION-*"  # full path
```

## Federation Model Sync Wrapper

A convenience script wraps the renderer:
- `/root/AAA/registries/federation-model-sync.sh`

```bash
bash federation-model-sync.sh            # dry-run
bash federation-model-sync.sh --render   # --write --force equivalent
bash federation-model-sync.sh --verify   # exit 0/1 drift check — now includes model ID validation
bash federation-model-sync.sh --completeness  # NEW (2026-07-24): check all agents have fallbacks
```

The `--verify` mode now includes `validate_model_ids(sot)` which checks every
`model_key` in every agent's `fallback_chain` exists in `MODEL_KEY_TRANSLATION`.
Catches typos like `openrouter/auto-betax` before they go live.

The `--completeness` mode flags agents with zero fallbacks (expected: claude-code,
copilot, grok — single-model agents) and prints total agent/provider/model counts.

## Custom Agents & Providers (Outside SOT)

Not every agent or provider lives in the SOT. Some are purpose-built for specific roles and wired directly. These are preserved across renders — never overwritten by `--write` unless explicitly added to the renderer.

### Dual-Lane Agent Pattern (Text vs. Vision)

When a single role needs two different models depending on modality, split into two agents:

| Agent | Model | When to Use |
|-------|-------|-------------|
| `555-ASI` (text lane) | `deepseek/deepseek-v4-flash` | Memory, drift, telemetry, research — text-only |
| `555-ASI-VISION` (vision lane) | `mulerouter/qwen3-omni-flash` | Image/chart/audio — multimodal constitutional gating |

**Routing logic** (handled by orchestrator):
```
if input contains image/audio → dispatch to 555-ASI-VISION
else → dispatch to 555-ASI (text lane)
```

**Benefits:**
- Vision lane uses a fast, cheap multimodal model only when needed
- Text lane stays on a cheaper text-only model — ~80% of calls hit this lane
- Each lane gets its own permission scope and system prompt
- Async pipeline: vision lane can process while text lane continues on other work

### Custom OpenAI-Compatible Provider with Env API Key

To add a provider not in the SOT (e.g., MuleRouter, a self-hosted proxy, or a new API endpoint):

```json
"mulerouter": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "MuleRouter — Fixed-Price Multimodal Gateway",
  "options": {
    "baseURL": "https://api.mulerouter.ai/vendors/openai/v1",
    "apiKey": "{env:MULEROUTER_API_KEY}"
  },
  "models": {
    "qwen3-omni-flash": {
      "name": "Qwen 3 Omni Flash — multimodal (vision+text+audio)",
      "attachment": true,
      "tool_call": true,
      "reasoning": false,
      "limit": {
        "context": 131072,
        "output": 16384
      },
      "modalities": {
        "input": ["text", "image", "audio"],
        "output": ["text"]
      }
    }
  }
}
```

**Key fields:**
- `"npm": "@ai-sdk/openai-compatible"` — any OpenAI-compatible API
- `"apiKey": "{env:VAR_NAME}"` — reads from env, never hardcoded
- `"attachment": true` — required for multimodal models (image/audio input)
- `"modalities"` — declares input/output types for the model
- `"tool_call": true` — allows structured output / tool calling
- `"reasoning": false` — set false for fast inference; true only for reasoning models

### Adding the Provider to enabled_providers

After adding the provider section, add it to `enabled_providers`:

```json
"enabled_providers": [
  ...
  "mulerouter",
  ...
]
```

### Setting the Route to Direct

When a custom provider doesn't need routing through TokenRouter or OpenRouter, set `"_route": "direct"` on the agent:

```json
"_route": "direct",
"_trinity_role": "Φ Sense — gatekeeper of sensory evidence. Tags, floors, and forwards structured input."
```

### Reference: 555-ASI Sensory Cascade

For a complete worked example, see `references/555-asi-sensory-cascade.md` — the full forge record including the constitutional charter at `/root/.config/opencode/agents/555-ASI.md`.

## Special Agents in Renderer

The renderer preserves `image-prompt-architect` as a special agent not sourced from SOT:

```python
special_agents = {
    "image-prompt-architect": {
        "model": "kimi/k3",
        "permission": {"bash": "allow", "*": "deny"},
    }
}
```

This agent needs:
- `kimi/k3` for vision capability (deepseek v4 doesn't support image input)
- `permission` instead of deprecated `tools` field
- No `tools` field (deprecated by OpenCode docs)

If you add another special agent to the renderer, follow this pattern — keep them in a dict at the top of `generate()`, not scattered through the code.

## Pitfalls

- **🚨 NEVER hand-edit opencode.json after SOT setup**: Always regenerate via `opencode_render.py --write`. Hand-edits create drift that `--verify` catches. The SOT is the only source of truth.
- **Schema validation is strict**: Any unknown top-level key causes `Error: Configuration is invalid`. This includes `_model_sot`, `_generated`, and any other metadata keys. Strip them before writing.
- **`opencode debug config` fails from subdirectories**: OpenCode finds project-local `opencode.json` files by traversing up from cwd. If you're in `/root/AAA/`, it may find `/root/AAA/opencode.json` (an agent card, not the runtime config). Always run from `/root` or the project root.
- **`image-prompt-architect` model gets overwritten**: The renderer preserves this agent's model as `kimi/k3` (vision capability). If you manually edit it, the next render will reset it. Keep the override in `opencode_render.py` under `special_agents`.
- **Provider IDs that don't match**: SOT providers like `bailian-token-plan`, `mimo-platform`, `glm` don't have direct OpenCode equivalents. They get mapped to kimi/tokenrouter/opencode-go providers. The SOT-to-OC mapping in `opencode_render.py` must be kept in sync as providers change.
- **`kimi/kimi-k2.7-code` does NOT exist in the kimi provider**: The Kimi REST API exposes `kimi-for-coding`, not `kimi-k2.7-code`. Always verify: `opencode models kimi`.
- **small_model should be lightweight**: Don't set it to a heavy fallback like MiniMax-M3. Use `ollama/qwen2.5-coder:3b` (local) or another lightweight model.
- **Deprecated `tools` field in agents**: The OpenCode docs explicitly deprecate `tools` in favor of `permission`. Old configs with `tools` still work but will fail on future versions. Migrate them when you touch the config.
- **Backup before first render**: `cp /root/.config/opencode/opencode.json /root/.config/opencode/opencode.json.bak-$(date +%s)`

## Files

- `references/sot-provider-mapping.md` — full SOT provider_id → OpenCode provider key mapping table
- `references/555-asi-sensory-cascade.md` — dual-lane sensory gatekeeper forge (MuleRouter + constitutional charter)
- `scripts/federation-model-sync.sh` — at `/root/AAA/registries/federation-model-sync.sh` (not in skill dir, registered separately)
