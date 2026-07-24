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
