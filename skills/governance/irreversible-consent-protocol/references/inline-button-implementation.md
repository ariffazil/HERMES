# Inline Button Implementation — `ic:` Callback Prefix

> The `ic:` (irreversible consent) callback prefix is how the Telegram inline consent button resolves back to the agent session. Implemented in `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py`.

## Three Gateway Modifications

### 1. State dict in `__init__` (line ~655)

```python
self._irreversible_consent_state: Dict[str, dict] = {}
```

Keyed by `ic_id` (integer counter, same pattern as `_approval_state`). Each entry:
```python
{
    "session_key": str,    # Gateway session key (for resolve_gateway_approval)
    "receipt_id": str,     # Unique receipt ID for forge_work
    "description": str,    # Human-readable action description
}
```

### 2. `send_irreversible_consent()` method (line ~4648)

Sends inline keyboard with two buttons:
- **✅ Confirm IRREVERSIBLE** → `ic:confirm:{ic_id}`
- **❌ Cancel** → `ic:cancel:{ic_id}`

Stores state in `_irreversible_consent_state`. Reuses existing `_send_message_with_thread_fallback` for topic support.

### 3. Callback handler in `_handle_callback_query` (line ~5598)

Triggered by `data.startswith("ic:")`:

| Choice | Behaviour |
|---|---|
| `confirm` | Writes consent receipt to `forge_work/<date>/consent-{receipt_id}.json`. Calls `resolve_gateway_approval(session_key, "once")` to unblock agent thread. |
| `cancel` | Writes denial receipt to `forge_work/<date>/consent-denied-{receipt_id}.json`. Calls `resolve_gateway_approval(session_key, "deny")`. |

Both paths:
1. Verify user authorization via `_is_callback_user_authorized()`
2. Pop state from `_irreversible_consent_state` (prevents double-click)
3. Write structured JSON receipt with `user_id`, `user_name`, `description`, `timestamp`, `source: "telegram_inline_button"`
4. Edit the inline message to show decision + user identity, remove buttons
5. Resolve via `resolve_gateway_approval` (same mechanism as `ea:` exec approval)

## Consent Receipt Format

Written to `forge_work/<date>/consent-{receipt_id}.json`:

```json
{
  "type": "IRREVERSIBLE_CONSENT",
  "consent_id": "IRREV-20260729-125952-62b3c752",
  "ts": "2026-07-29T12:59:52.700852+00:00",
  "user_id": "267378578",
  "user_name": "Arif",
  "description": "Delete file /tmp/test.txt",
  "choice": "confirm",
  "source": "telegram_inline_button"
}
```

## Agent Flow (LLM side)

The agent does NOT call `send_irreversible_consent()` directly. Instead:

### Phase 1 (current — no agent-side interceptor)
The agent triggers the gateway approval mechanism (same as dangerous commands), which calls `_approval_notify_sync`. The approval callback already supports `send_exec_approval`; the `ic:` buttons provide an alternative UX path for irreversible actions.

### Phase 2 (future — pre_tool_call hook interceptor)
Wire the `pre_tool_call` hook to detect `ack_irreversible=true` on MCP tools and replace the normal tool execution flow with an irreversible consent prompt. The hook would:
1. Intercept the tool call
2. Call `register_gateway_notify` to create a blocking entry
3. Call `send_irreversible_consent` to show inline buttons
4. Block until user confirms or denies
5. On confirm: proceed with tool call + `arif_seal` receipt
6. On deny: abort cleanly

## Fallback: Text-Based Consent

If the gateway patch is not applied, use text confirmation:
- Send clear IRREVERSIBLE warning message
- Ask user to type: `confirm` or `ya, saya sahkan`
- Accept: `sah`, `confirm`, `ya`, `ok`, `yes` (case-insensitive, BM + EN)
- Reject: anything else or timeout > 60s
- Seal receipt via `/root/.hermes/scripts/irreversible_receipt.py`

---

*Forged: 2026-07-29 from multi-user consent architecture session.*
*DITEMPA BUKAN DIBERI*
