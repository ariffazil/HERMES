# OpenCode Agent Config Schema Reference

## Tools Must Be Object, Not Array

OpenCode's `agent.<name>.tools` field expects an **object** mapping tool names to booleans:

```json
// ✅ CORRECT
"tools": {
    "understand_image": true,
    "ai_image_generation": true
}

// ❌ WRONG — schema validation will fail
"tools": [
    "cloudflare_ai_image_generation",
    "minimax_understand_image"
]
```

The remediation agent's template wrote tools as an array. Always inspect the schema before writing.

## MCP Tool Name Discovery

MCP servers expose tools via JSON-RPC `tools/list` WITHOUT provider prefixes:

```python
import subprocess, json, time

def probe_mcp_tools(command_args):
    """Probe an MCP server's tools via JSON-RPC init sequence."""
    proc = subprocess.Popen(
        command_args,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True
    )
    # Must initialize first (MCP protocol requirement)
    init = {'jsonrpc':'2.0','id':1,'method':'initialize',
            'params':{'protocolVersion':'2024-11-05','capabilities':{},
                      'clientInfo':{'name':'probe','version':'1.0'}}}
    proc.stdin.write(json.dumps(init) + '\n')
    proc.stdin.flush()
    time.sleep(1)

    # Then list tools
    tl = {'jsonrpc':'2.0','id':2,'method':'tools/list'}
    proc.stdin.write(json.dumps(tl) + '\n')
    proc.stdin.flush()
    time.sleep(2)

    out, err = proc.communicate(timeout=10)
    for line in out.split('\n'):
        if not line.strip(): continue
        try:
            d = json.loads(line)
            if 'result' in d and 'tools' in d['result']:
                return [t['name'] for t in d['result']['tools']]
        except: pass
    return []

# Example — what tools does minimax MCP expose?
tools = probe_mcp_tools(['uvx', 'minimax-coding-plan-mcp', '-y'])
# Returns: ["web_search", "understand_image"]  — NOT minimax_web_search, NOT minimax_understand_image

# Example — what tools does cloudflare MCP expose?
tools = probe_mcp_tools(['/root/.npm-global/bin/mcp-server-cloudflare', 'run'])
# Returns ai_image_generation, ai_inference, r2_list_objects, etc. — NOT cloudflare_ai_image_generation
```

**Key insight:** The tool name in OpenCode's `agent.<name>.tools` is discovered via MCP `tools/list`. It is NOT constructed by prepending the MCP server name. Probe first. Reference exact names.

## Ghost Tool Classification

A ghost tool = referenced in config but absent from the MCP server's `tools/list`. Causes:
- Agent prompt claims capability that doesn't exist (F9 ANTI-HANTU violation)
- Agent may attempt tool calls that silently fail
- Session spends tokens on hallucinated capability

**Remedy:** After any config edit that references MCP tools, probe the actual MCP server's `tools/list` and diff against config references. Remove or correct any mismatches.

## F13 Ruling Context (2026-07-23)

The image-prompt-architect agent was wired under F13 ruling to route through MiniMax multimodal. The remediation agent:
1. Used prefixed tool names (`cloudflare_ai_image_generation`, `minimax_understand_image`) without probing
2. Added a Cloudflare image generation tool that was never ratified in the F13 ruling — scope creep
3. Claimed tools were "verified active" in the agent prompt without running any verification

**Meta pattern:** Same failure as kimi-code writing `redacted display text` into vault.env, and Hermes assuming `6/6 = all models`. All three = agent writes config without a validate-after-write step.

## Model Alignment & Graceful Degradation

When realigning OpenCode agent models after a provider key dies or is exhausted:

### 1. Verify Which Providers Are Actually Alive

Do NOT trust config presence — test the API directly:

```bash
source /root/.secrets/vault.env
curl -s --max-time 10 https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" | python3 -c \
  "import json,sys;d=json.load(sys.stdin);[print(m['id']) for m in d.get('data',[])]"
```

For each provider in `enabled_providers`, confirm the key isn't empty AND the endpoint responds. A key that exists but is quota-exhausted is as dead as a missing key — OpenCode won't error, it'll just time out.

### 2. Identify Broken Model References

**Run `opencode debug config`** after every agent model edit — it shows the resolved config and catches schema errors immediately.

**Common model reference pitfalls:**

| Pitfall | Example | Fix |
|---------|---------|-----|
| Model ID doesn't match any model in the referenced provider | `kimi/kimi-k2.7-code` but `kimi` provider has `kimi-for-coding` | Use the exact model ID from the provider's model list: `kimi/kimi-for-coding` or switch to a provider where the ID exists |
| Provider prefix doesn't match any `enabled_providers` entry | `some-provider/deepseek-v4-pro` but `some-provider` not in `enabled_providers` | Add provider or use a listed one |
| Model name in agent prompt contradicts `model` field | Prompt says "Model: Kimi K3 via kimi/k3" but model field is `deepseek/deepseek-v4-pro` | Update prompt text to match actual model — agents read their own prompt as self-identity |
| Custom key (`_model_sot`, `_note`, etc.) breaks schema validation | `_model_sot: "source: ..."` causes `Unrecognized key` error | Remove unrecognized keys — OpenCode validates strictly against its JSON schema |

**Validation** — verify resolved models after every edit:

```bash
source /root/.secrets/vault.env && opencode debug config 2>&1 | python3 -c "
import sys, json
raw = sys.stdin.read()
import re
m = re.search(r'\{.*', raw, re.DOTALL)
if m:
    c = json.loads(m.group())
    for name, a in c.get('agent',{}).items():
        print(f'{name}: model={a.get(\"model\",\"(inherits)\")}')
"
```

### 3. Build the Fallback Chain

OpenCode does NOT support model-level fallback lists (one `model` field per agent). Graceful degradation is achieved through **agent-level fallback**:

```
Tier 1 (flagship reasoning) → forge, auditor, planner → deepseek-v4-pro
Tier 2 (fast lane)          → ops                      → deepseek-v4-flash
Tier 3 (vision-capable)     → image-prompt-architect   → kimi/k3
Tier 4 (local last resort)  → recovery                 → ollama/qwen2.5-coder:3b
```

**When deepseek fails:** Try the same model via a different provider that has it — `opencode-go/deepseek-v4-pro` (Go subscription) or `tokenrouter-arifos/deepseek-v4-pro` (TokenRouter routing). Both providers list overlapping model catalogs.

**Provider redundancy catalog** (verified 2026-07-24):

| Model | Via deepseek | Via opencode-go | Via tokenrouter | Via openrouter |
|-------|:---:|:---:|:---:|:---:|
| deepseek-v4-pro | ✅ primary | ✅ backup | ✅ backup | ❌ |
| deepseek-v4-flash | ✅ primary | ✅ backup | ✅ backup | ❌ |
| kimi-k3 | ❌ | ✅ | ✅ | ✅ |
| MiniMax-M3 | ❌ | ❌ | ✅ | ❌ |

### 4. Update Agent Prompts to Match Actual Model

Every OpenCode agent reads its own `prompt` field as system prompt. If the prompt says "Model: Kimi K3" but the `model` field says `deepseek-v4-pro`, the agent will contradict itself:

```diff
- Model: Kimi K3 via kimi/k3 (1M ctx, thinking+tools)
+ Model: DeepSeek V4 Pro (1M ctx, reasoning+tools)
```

**Search for all stale mentions:**

```bash
grep -n 'Kimi K3\|kimi/k3' /root/.config/opencode/opencode.json
```

Every match in an agent `prompt` field is a stale self-identity claim. Fix all in one pass.

### 5. Include Fallback Instructions in Agent Prompts

For agents that may need it (e.g., image-prompt-architect with a vision model that could go down), add a fallback hint:

```
MODEL: kimi/k3 (KIMI_API_KEY via REST API) — handles vision+reasoning.
FALLBACK: opencode-go/kimi-k3 (Go subscription) or deepseek/deepseek-v4-pro (text-only).
```

### 6. Test After Every Change

```bash
source /root/.secrets/vault.env
opencode models deepseek    # Verify deepseek models still listable
opencode models kimi        # Verify kimi models still listable
opencode debug config       # Verify no schema errors + all agents resolved
```
