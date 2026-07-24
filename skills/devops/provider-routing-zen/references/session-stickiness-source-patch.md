# Session Stickiness — Hermes Source Patch

> **Applied:** 2026-07-24
> **File:** `/usr/local/lib/hermes-agent/agent/agent_init.py`
> **Lines:** ~952-956 (in `_run_loop` or equivalent agent init block)
> **Pattern:** Every OpenRouter-bound HTTP request carries `x-session-id` header

## The Patch

```python
# Inside the block where OpenRouter headers are built:
if base_url_host_matches(effective_base, "openrouter.ai"):
    from agent.auxiliary_client import build_or_headers
    client_kwargs["default_headers"] = build_or_headers()
    # Session stickiness: pins model+provider for 5min under
    # the same session_id. Cuts classifier round-trip + hits
    # provider prompt cache on follow-up turns. (~30% latency)
    if hasattr(agent, "session_id") and agent.session_id:
        client_kwargs["default_headers"]["x-session-id"] = (
            f"aaa-hermes-{agent.session_id}"
        )
```

## What It Does

- Adds `x-session-id: aaa-hermes-{agent.session_id}` to every outgoing OpenRouter API call
- Only injected when `base_url` matches `openrouter.ai` AND session_id is non-empty
- Pins model + provider for 5 minutes of inactivity per OpenRouter's session stickiness
- Expected: ~30% latency reduction on follow-up turns (skips classifier round-trip + hits prompt cache)

## Verification

After restart, check that outbound requests carry the header via:
- Hermes log with `grep "x-session-id" /root/.hermes/logs/agent.log`
- OpenRouter dashboard request inspector (Activity tab)
- `curl` test with explicit header: `curl -H "x-session-id: aaa-hermes-test" https://openrouter.ai/api/v1/auth/key`

## Reversion

```bash
cd /usr/local/lib/hermes-agent
git checkout -- agent/agent_init.py
```

Or use patch to revert:
```bash
grep -n "x-session-id" agent/agent_init.py
# Then edit to remove the 4 lines
```

## Why Source Patch (Not Config)

Session stickiness requires the runtime to emit `x-session-id` on every HTTP request. Hermes builds the OpenAI SDK client once at agent init time, passing `default_headers`. The session_id is available on the `agent` object at that point. This cannot be achieved through config alone — the header value is dynamic (changes per session) and must be emitted by the runtime.

## After Hermes Updates

When Hermes is updated (via `hermes update` or pip), this patch may be overwritten if `agent/agent_init.py` changes. After every update:
1. Check if the patch is still present: `grep "x-session-id" /usr/local/lib/hermes-agent/agent/agent_init.py`
2. If missing, re-apply from this reference
3. Test: `hermes chat -q "test"` and check log for the header
