# Gateway Flood Prevention for Live Location

## The Problem

Telegram's live location feature sends GPS updates every few seconds. Each update triggers `_handle_location_message` in the Telegram adapter, which sends it to the LLM and produces a response. This creates a **spam cascade**:

1. Location pin arrives → agent processes → responds with 📍🫡
2. Next pin arrives while previous response is still being sent
3. Gateway emits "⚡ Interrupting current task" for each new pin
4. Telegram flood control kicks in (429 errors, 10-25s retry delays)
5. Queued responses pile up → more interrupts → more flood control
6. User sees 20+ messages in seconds, including interrupt notices

**Symptoms in gateway.log:**
```
WARNING gateway.run: Interrupt recursion depth 3 reached for session ...
WARNING gateway.platforms.base: [Telegram] Telegram flood control, waiting 14.0s
WARNING gateway.platforms.base: [Telegram] Telegram flood control on send (attempt 1/3)
```

**Chat ID where this was observed:** `-1003815535761` (SADO group)

## The Fix: Rate Limiter in Adapter

**File:** `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py`

Add a class-level rate limiter to `_handle_location_message`. The fix tracks the last processed location timestamp per (chat_id, user_id) and skips updates that arrive within 60 seconds.

### Patch Location

The handler is at approximately line 7565 (varies by version). Find:
```python
async def _handle_location_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming location/venue pin messages."""
    msg = self._effective_update_message(update)
    if not msg:
        return
    if not self._is_user_authorized_from_message(msg):
```

Insert BEFORE the handler (class-level attributes + rate-limit check at top of method):

```python
    _last_location_ts: dict[tuple[int, int], float] = {}
    _LOCATION_RATE_LIMIT_SECS = 60  # ignore live-location updates faster than this

    async def _handle_location_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming location/venue pin messages."""
        msg = self._effective_update_message(update)
        if not msg:
            return
        # Rate-limit: live location sends updates every few seconds; only
        # process at most one per _LOCATION_RATE_LIMIT_SECS per (chat, user).
        chat_id = getattr(getattr(msg, "chat", None), "id", 0)
        user_id = getattr(getattr(msg, "from_user", None), "id", 0)
        import time as _time
        now = _time.monotonic()
        key = (chat_id, user_id)
        last = self._last_location_ts.get(key, 0)
        if now - last < self._LOCATION_RATE_LIMIT_SECS:
            logger.debug(
                "[Telegram] Rate-limiting live location from user %s in chat %s (%.0fs since last)",
                user_id, chat_id, now - last,
            )
            return
        self._last_location_ts[key] = now
        if not self._is_user_authorized_from_message(msg):
```

### Why 60 Seconds

- Live location updates: every 2-5 seconds
- One-off location pins: typically single share, no follow-up
- 60s window: catches live location spam while allowing intentional re-shares
- Single location pin → processed immediately (no prior timestamp)
- Live location → first pin processed, next 60s of updates silently dropped

## Gateway Restart Pitfall

**Cannot restart the gateway from inside the gateway.** The tool blocks it:
```
Blocked: cannot restart or stop the gateway from inside the gateway process.
```

Options:
1. **Separate SSH session:** `hermes gateway restart`
2. **systemctl (if systemd-managed):** `systemctl --user restart hermes-gateway`
3. **From a cron job or script** running outside the gateway process

After patching the adapter, the restart is REQUIRED — Python code changes don't take effect until the process reloads.

## Version Note

This patch is applied to the INSTALLED copy at `/usr/local/lib/hermes-agent/`. It will be **overwritten on `hermes update`**. If the fix works, consider upstreaming it or re-applying after updates.

Check if upstream has fixed this:
```bash
grep -n "rate.*location\|location.*rate\|_last_location" /usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py
```

If the pattern is gone after an update, re-apply the patch.
