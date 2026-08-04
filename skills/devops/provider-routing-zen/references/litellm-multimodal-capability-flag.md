# LiteLLM 1.90 Multimodal Capability Flag — The Hidden Reject Gate

> **Proven 2026-08-04** during FED + Hermes-ASI Multimodal Audit.
> **Symptom:** `litellm.NotFoundError: No endpoints found that support image input. Received Model Group=<alias>`. Backend never sees the request.
> **Cost:** Hours of debugging that go nowhere if you don't know this exists.

## The Trap

LiteLLM does NOT look at the live model API to decide if a model supports image/audio/video input. It inspects a **declarative capability flag** in its own config before forwarding. If the flag is missing or false, the whole model group is rejected — fallback chains abort. The request never leaves the box.

```yaml
# WRONG — config says nothing → proxy rejects multimodal input
- model_name: hermes-asi
  litellm_params:
    model: openai/mimo-v2.5-pro
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
    api_key: os.environ/MIMO_API_KEY
```

```yaml
# RIGHT — declare the capability, even if the backend always returns 200 for multimodal
- model_name: hermes-asi
  litellm_params:
    model: openai/mimo-v2.5
    api_base: https://token-plan-sgp.xiaomimimo.com/v1
    api_key: os.environ/MIMO_API_KEY
  model_info:
    supports_image_input: true
```

## The Diagnostic Chain (2 minutes)

1. **Identify the error verbatim**:
   ```
   litellm.NotFoundError: OpenAIException -
   No endpoints found that support image input.
   Received Model Group=<alias>
   Available Model Group Fallbacks=None
   ```
2. **Confirm the underlying API DOES support multimodal** — call the vendor docs page for the model name. For example: `https://mimo.mi.com/docs/.../image-understanding` says `mimo-v2.5` supports image input; `mimo-v2.5-pro` is the deep-thinking variant and may not.
3. **Open `litellm-config.yaml`** for the file bound to the failing model_name.
4. **For every entry in that model group**, add:
   ```yaml
   model_info:
     supports_image_input: true   # or false for text-only models
   ```
5. **`systemctl restart litellm-federation`** (or equivalent service on your org).

## Apply To Each Group Member

Don't add the flag to one entry and think the chain is fixed. LiteLLM rejects the **group** if ANY entry lacks the flag for a capability the request needs. Add the flag to EVERY entry in the chain — backends, fallbacks, shadow models — even if only one is actually invoked.

```yaml
model_list:
  # PRIMARY
  - model_name: hermes-asi
    litellm_params: { model: openai/mimo-v2.5, ... }
    model_info: { supports_image_input: true }
  # FALLBACK 1
  - model_name: hermes-asi
    litellm_params: { model: openai/mimo-v2.5-pro, ... }
    model_info: { supports_image_input: true }   # even though -pro may not support it
  # FALLBACK 2
  - model_name: hermes-asi
    litellm_params: { model: openai/MiniMax-M3, ... }
    model_info: { supports_image_input: true }
```

## Capability Flags Reference (LiteLLM 1.90)

| Capability | Flag | Notes |
|---|---|---|
| Image input | `supports_image_input: true` | Required for `image_url` content parts |
| Audio input | `supports_audio_input: true` | Required for `input_audio` content parts |
| Video input | `supports_vision: true` | LiteLLM uses vision flag for video frames |
| Function calling | `supports_function_calling: true` | Required for `tools=[...]` with multiple backends |
| Reasoning | `supports_reasoning: true` | Surfaces `reasoning_content` field |
| Structured output | `supports_response_schema: true` | Required for `response_format={type: json_schema}` |

## Verified Test (Kimi K3 2026-08-04)

```python
import openai
client = openai.OpenAI(
    api_key="<MASTER_KEY>",
    base_url="http://127.0.0.1:4000/v1"
)

# BEFORE FIX — fails with NotFoundError
# AFTER FIX — returns image_tokens: 1024
resp = client.chat.completions.create(
    model="hermes-asi",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example-files.cnbj1.mi-fds.com/example-files/image/image_example.png"}},
            {"type": "text", "text": "describe this"},
        ],
    }],
    max_tokens=256,
)
print(resp.choices[0].message.content)
print(f"image_tokens: {resp.usage.prompt_tokens_details.image_tokens}")
```

## Pitfalls

1. **`mimo-v2.5-pro` ≠ `mimo-v2.5`.** The `-pro` suffix = deep-thinking variant which Xiaomi documents as **text-only**. Do not assume inheritance from the base model. Read the docs.
2. **`supports_vision: true` ≠ `supports_image_input: true`.** LiteLLM's API has split these between versions. Use `supports_image_input: true` for chat completions image_url ingestion. `supports_vision` is for video frame extraction (STAC-style).
3. **`Available Model Group Fallbacks=None` is a hint, not an answer.** Means LiteLLM knows about the group but has no group-fallback policy registered. The issue is the capability flag, not the fallback chain.
4. **DB-less config means no audit trail.** LiteLLM 1.90 with `DATABASE_URL` unset rejects `master_key` auth with "No connected db." This is accepted in arifOS LiteLLM 1.90.2 setup (master key disabled) — only health probes and route metadata flow through. Completions go direct.
5. **The flag is per-entry, not per-group.** If you have a 3-deep chain and only add the flag to entry 1, the proxy still aborts because entries 2 and 3 haven't declared capability. Add to all.
6. **`drop_params: true` does NOT save you here.** LiteLLM's `drop_params` strips unknown keys from the request before forwarding; it does NOT auto-add missing capability metadata to the model entry. Separate flags.

## Probe Pattern (use before claiming a model supports multimodal)

```bash
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<alias>",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "https://<test-image-url>"}},
        {"type": "text", "text": "describe"}
      ]
    }],
    "max_tokens": 32
  }' | jq .
```

Acceptable responses:
- `usage.prompt_tokens_details.image_tokens > 0` → model accepted image
- HTTP 400 + `BadRequestError` from upstream → backend API rejects → fix vendor

Unacceptable responses (the trap):
- HTTP 400 + `NotFoundError: No endpoints found that support image input` → capability flag missing in YOUR config
- `Available Model Group Fallbacks=None` → no fallback registered for the group → audit litellm-config.yaml

## Related Reading

- Xiaomi MiMo multimodal docs: <https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/>
- LiteLLM proxy model_info reference: <https://docs.litellm.ai/docs/proxy/configs#model_info-fields>
- `references/federation-topology-and-fallbacks.md` (this skill) for group-level chain design
- `references/archived-provider-reconciliation.md` (this skill) for stranded-balance pattern
