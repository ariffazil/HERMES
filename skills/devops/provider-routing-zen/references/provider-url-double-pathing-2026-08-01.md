# Provider API URL Double-Pathing — Tool Call Breakage (2026-08-01)

## Symptom

Model outputs raw JSON tool calls as plain text instead of structured `tool_calls`:

```
{
  "name": "web_extract",
  "arguments": {
    "urls": ["https://example.com"]
  }
}
```

This text appears in the chat instead of being intercepted and executed by the agent framework.

## Root Cause

The provider's `api` field includes the **full endpoint path** instead of just the base URL. When Hermes's `openai_chat` transport appends `/chat/completions` to construct the request URL, the path gets doubled or hits a wrong endpoint.

| Provider | `api` value | Format | Works? |
|----------|------------|--------|--------|
| OpenRouter | `https://openrouter.ai/api/v1` | Base URL ✅ | ✅ |
| MuleRouter | `https://api.mulerouter.ai/vendors/openai/v1` | Base URL ✅ | ✅ |
| **OpenCode Go** | `https://opencode.ai/zen/go/v1/chat/completions` | **Full path** ❌ | ❌ |

When transport appends `/chat/completions` to the full-path URL:
- Request goes to: `https://opencode.ai/zen/go/v1/chat/completions/chat/completions`
- Or the API treats it as a non-standard endpoint
- Model responds but `tool_calls` field is missing — content is dumped as text

## Diagnosis

```bash
# Check all provider api URLs — look for ones ending in /chat/completions
grep -n "api:" ~/.hermes/config.yaml | grep -v "^#"
```

Any `api:` value ending in `/chat/completions` is a full-path format — likely to cause double-pathing.

## Fix

Change the `api` field to base URL form:

```yaml
# BEFORE (broken):
  opencode-go:
    api: https://opencode.ai/zen/go/v1/chat/completions

# AFTER (correct):
  opencode-go:
    api: https://opencode.ai/zen/go
```

The transport will append `/chat/completions` automatically.

## Verification

After fixing, test tool calling:
1. Switch to the model on that provider
2. Send a message that triggers a tool call (e.g., "extract content from URL")
3. If the tool executes normally → fixed
4. If raw JSON appears as text → still double-pathed, try stripping `/v1` too

## Pattern for New Providers

When adding a new OpenAI-compatible provider:
1. Check the provider's docs for the **base URL** (not the full endpoint)
2. Use the base URL in `api:` field
3. Test a simple tool call immediately after configuration
4. If tool calls appear as raw text, check URL format before blaming the model
