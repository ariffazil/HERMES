# Path B: Full Vision Bypass — Source Patch (2026-07-29)

**Forged:** 2026-07-29 session  
**Status:** ✅ Live in `gateway/run.py` — requires no additional patches  
**Approach:** Gateway-level model override, NOT agent-level switch_model()

## Problem: Broken Telephone (Path A)

Before this patch, when a text-only primary model (DeepSeek Flash) received an image:

```
User sends IMAGE → vision_analyze(kimi-k3) → [IMAGE TRANSCRIPT] → Flash reads → responds
```

Path A defects:
- **Broken telephone:** qwen3-vl describes → Flash fills gaps from incomplete transcript → hallucination
- **Double latency:** ~4s for vision analysis + Flash processing = ~8s+ total
- **F2 TRUTH violation:** Flash makes confident claims from secondary data it never actually saw
- **Kimi-k3 content=null:** The auxiliary vision model sometimes returned empty analysis → Flash had nothing to work with

## Solution: Path B — Full Bypass

```
User sends IMAGE → _prepare_inbound_message_text()
                  → _img_mode == "text" (Flash is text-only)
                  → instead of _enrich_message_with_vision() (Path A):
                  → defer as pending_native images
                  → set _pending_vision_model_overrides[session]
                  → at run_conversation call site:
                  → swap agent.model → qwen/qwen3-vl-30b-a3b-instruct 
                  → swap agent.provider → openrouter
                  → qwen3-vl processes image natively → responds directly
                  → restore agent.model → deepseek-v4-flash
                  → restore agent.provider → deepseek

User sends TEXT → Flash primary (0ms overhead, no inspector overhead)
```

## Files Patched (Single File: gateway/run.py)

### Patch 1: `_prepare_inbound_message_text` — Image routing block (line ~10508)

**Location:** Inside the GatewayRunner method `async def _prepare_inbound_message_text()`.

**Before:**
```python
if image_paths:
    _img_mode = self._decide_image_input_mode(...)
    if _img_mode == "native":
        # Defer inline
        pending_native[session_key] = list(image_paths)
    else:
        # text mode: vision_analyze prepend
        logger.info("Image routing: text (mode=%s). Pre-analyzing %d image(s) via vision_analyze.",
                    _img_mode, len(image_paths))
        message_text = await self._enrich_message_with_vision(message_text, image_paths)
```

**After:**
```python
if image_paths:
    _img_mode = self._decide_image_input_mode(...)
    if _img_mode == "native":
        # Defer inline (same)
        pending_native[session_key] = list(image_paths)
    else:
        # Path B: text-only model + images → swap to vision-native model
        # Instead of transcribing, defer as native + set model override
        pending_native = getattr(self, "_pending_native_image_paths_by_session", None)
        if pending_native is None:
            pending_native = {}
            self._pending_native_image_paths_by_session = pending_native
        pending_native[session_key] = list(image_paths)
        
        _vision_overrides = getattr(self, "_pending_vision_model_overrides", None)
        if _vision_overrides is None:
            _vision_overrides = {}
            self._pending_vision_model_overrides = _vision_overrides
        _vision_overrides[session_key] = {
            "model": "qwen/qwen3-vl-30b-a3b-instruct",
            "provider": "openrouter",
        }
        logger.info("Image routing: PATH B (text-only primary). %d image(s) deferred — "
                    "model override set to qwen-vl via OpenRouter.", len(image_paths))
```

### Patch 2: `_consume_pending_vision_model_override()` — New method (after line ~10809)

**Location:** Right after `_consume_pending_native_image_paths()`.

```python
def _consume_pending_vision_model_override(self, session_key: str) -> Optional[Dict[str, str]]:
    """Consume-and-clear Path B vision model override for the given session."""
    overrides = getattr(self, "_pending_vision_model_overrides", None)
    if not overrides:
        return None
    return overrides.pop(session_key, None)
```

Same pattern as `_consume_pending_native_image_paths`:
- Reads dict from `self._pending_vision_model_overrides` (None-guarded)
- Pops the session key (one-shot — auto-cleared)
- Returns None if no override exists (no-op on non-image turns)

### Patch 3: `_run_conversation_with_agent` — Model swap + restore (lines ~19077-19144)

**Location:** Inside the `async def _run_conversation_with_agent()` method.

**Before `agent.run_conversation()`:**
```python
_native_imgs = self._consume_pending_native_image_paths(session_key)
if _native_imgs:
    # build native content parts...
```

**After:**
```python
_native_imgs = self._consume_pending_native_image_paths(session_key)
# Path B: consume vision model override
_vision_override = self._consume_pending_vision_model_override(session_key)
_restore_model = None
_restore_provider = None
if _vision_override and _native_imgs and hasattr(agent, "model"):
    _restore_model = agent.model
    _restore_provider = getattr(agent, "provider", None)
    agent.model = _vision_override.get("model", agent.model)
    if "provider" in _vision_override:
        agent.provider = _vision_override["provider"]
    logger.info("Path B: swapped agent model to %s/%s.", agent.provider, agent.model)
```

**After `agent.run_conversation()`:**
```python
result = agent.run_conversation(_api_run_message, **_conversation_kwargs)
# Path B: restore original model/provider after vision-routed turn
if _restore_model is not None:
    agent.model = _restore_model
    if _restore_provider is not None:
        agent.provider = _restore_provider
    logger.debug("Path B: restored agent model to %s/%s.", agent.provider, agent.model)
```

## Flow Diagram

```
TEXT TURN:
  User sends text message
    → _prepare_inbound_message_text() → no images → skip image block
    → _run_conversation_with_agent() → no pending_native → no override
    → Flash processes normally

IMAGE TURN:
  User sends image
    → _prepare_inbound_message_text() → image_paths detected
    → _decide_image_input_mode() returns "text" (Flash is text-only)
    → PATH B: defer images as pending_native + set model override
    → _run_conversation_with_agent()
    → consume pending_native images → build_native_content_parts
    → consume vision model override → swap agent.model to qwen-vl/OpenRouter
    → agent.run_conversation() using qwen-vl (native image handling)
    → qwen3-vl responds directly — ONE API call
    → restore agent.model to Flash/deepseek
    → next turn back on Flash

CONSECUTIVE IMAGE TURNS:
  Turn 1: image → swap → respond → restore
  Turn 2: image again → swap again → respond → restore
  Turn 3: text → no override → normal Flash
```

## Why Gateway (not run_agent.py)

The previous approach (patched in earlier sessions) modified `run_agent.py` and `chat_completion_helpers.py` using `switch_model()`. The gateway-based approach is superior because:

| Dimension | Old approach (agent-level) | Current approach (gateway-level) |
|-----------|---------------------------|----------------------------------|
| **Invasiveness** | Patches core agent runtime | Hooks into existing routing pattern |
| **Model switch mechanism** | `switch_model()` — resets provider, base_url, api_mode | Direct attribute assignment — local scope only |
| **Restore trigger** | Post-API hook in chat_completion_helpers.py | Right after run_conversation returns — same try block |
| **Distributed state** | 2 files (run_agent.py + chat_completion_helpers.py) | 1 file (gateway/run.py) |
| **Pattern re-use** | Custom vision_bypass_active flag | Same pending_native pattern already used for native images |

## Configuration Dependencies

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek

openrouter:
  api_key_env: OPENROUTER_API_KEY  # qwen-vl needs OpenRouter credentials

# The vision auxiliary config provides the model string
# (not used as transcriber anymore — qwen-vl IS the responder)
auxiliary:
  vision:
    model: qwen/qwen3-vl-30b-a3b-instruct
    provider: openrouter
    timeout: 120
```

## Verification

```bash
# Syntax check
python3 -c "import ast; ast.parse(open('/usr/local/lib/hermes-agent/gateway/run.py').read()); print('OK')"

# Send an image in Telegram to test:
# Image only → qwen3-vl responds (check: no [IMAGE TRANSCRIPT] preamble)
# Text after image → Flash responds (check: model reverts correctly)

# Logs to check:
grep "Path B" /var/log/hermes/gateway.log
# Expected: "Image routing: PATH B" on image turns
# Expected: "swapped agent model to openrouter/qwen" before vision response
# Expected: "restored agent model" after vision response
```

## Backup

```bash
cp /usr/local/lib/hermes-agent/gateway/run.py /usr/local/lib/hermes-agent/gateway/run.py.bak
```

Backup exists at `/usr/local/lib/hermes-agent/gateway/run.py.bak` (size ~1MB, 2026-07-29). Revert with:
```bash
cp /usr/local/lib/hermes-agent/gateway/run.py.bak /usr/local/lib/hermes-agent/gateway/run.py
```