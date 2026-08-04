# FED + Model Capability Audit Protocol

> Session: 2026-08-04 · FED + Hermes-ASI Multimodal Audit
> Use when: auditing whether a model alias actually supports claimed capabilities

## Quick Audit Steps

### 1. FED Health (30 seconds)
```
mcp__fed__fed_health    → status, port, version, tables
mcp__fed__fed_status    → providers, balances, latency, health
```

### 2. LiteLLM Config Check (60 seconds)
```bash
grep -A5 '<alias>' /root/A-FORGE/litellm-config.yaml
```
Look for: model name, api_base, capability flags, timeout, fallback chain.

### 3. Hermes Provider Config (30 seconds)
```bash
grep -A10 '<provider>' ~/.hermes/config.yaml
```
Look for: api URL, capabilities list, model IDs, supports_vision flag.

### 4. Direct API Test (bypasses proxy)
```bash
curl -s -X POST "<endpoint>/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<model>","messages":[{"role":"user","content":"hello"}],"max_tokens":10}'
```

### 5. Multimodal Test (if applicable)
```bash
curl -s -X POST "<endpoint>/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"mimo-v2.5","messages":[{"role":"user","content":[
    {"type":"image_url","image_url":{"url":"https://example.com/img.png"}},
    {"type":"text","text":"describe"}
  ]}],"max_tokens":100}'
```
Check: `image_tokens > 0` in usage response = multimodal works.

### 6. Through-Alias Test
Same as step 4/5 but use the LiteLLM proxy endpoint (`http://127.0.0.1:4000/v1`) and the alias name.

## Known Gotchas

- `mimo-v2.5` ≠ `mimo-v2.5-pro` — base = multimodal, pro = deep thinking text
- LiteLLM `:4000` is NOT the production traffic path — agents call direct
- `supports_vision: true` in Hermes config ≠ multimodal works through proxy
- Capability flags must be declared in litellm-config.yaml for proxy to accept
- MiniMax M3 IS multimodal but config must declare it

## Reference

Full capability matrix: `/root/HERMES/docs/mimo-multimodal-capabilities.md`
Pitfall detail: `references/docs-vs-config-capability-pitfall.md` (provider-routing-zen)
