# 777-FORGE Bot Group Handling — Code Patterns

> File: `/root/.openclaw/workspace/bots/opencode-bot/bot.py`

## should_respond_in_group (Arif bypass pattern)

When multiple bots share a group (AAA),777-FORGE needs:
- Arif (F13) → always respond, no @mention needed
- Other agents → must @mention @arifOS_bot to get a response

```python
ALLOWED_USER_ID = 267378578  # F13 SOVEREIGN

def should_respond_in_group(update: Update) -> bool:
    """In AAA group: Arif (F13) needs no @mention. Agents must @mention."""
    if update.effective_chat.id != AAA_GROUP_ID:
        return True  # not in AAA group -> respond (DM or other chat)
    # Arif (F13 SOVEREIGN) always gets a response - no @mention needed
    if update.effective_user and update.effective_user.id == ALLOWED_USER_ID:
        return True
    text = update.message.text or ""
    # Other agents/users must @mention this bot to get a response
    return bool(
        re.search(r"@AGI[_-]?ASI[_-]?bot", text, re.IGNORECASE)
        or re.search(r"@arifOS[_-]?bot", text, re.IGNORECASE)
        or "@000" in text  # persona mention
        or text.startswith("/")
    )
```

## Adding New Command Handlers (000-999 alignment)

When adding numbered commands that map to existing handlers:

```python
# In COMMANDS list:
BotCommand("000", "INIT — reset session, fresh identity boot"),
BotCommand("777", "FORGE — build, deploy, code"),

# In handler registrations:
app.add_handler(CommandHandler("000", cmd_init))       # maps to existing handler
app.add_handler(CommandHandler("777", cmd_forge))      # maps to existing handler
# Keep legacy aliases:
app.add_handler(CommandHandler("forge", cmd_forge))
```

## Pitfalls

1. **Syntax error when replacing COMMANDS list.** The Python list must be closed with `]`. If the old block's closing bracket is accidentally removed, you get `SyntaxError: '[' was never closed` at the `] = [` line. Always verify with `py_compile.compile()` before restarting.

2. **ALLOWED_USER_ID vs ARIF_USER_ID.** The bot uses `ALLOWED_USER_ID` (267378578), not `ARIF_USER_ID`. Using the wrong name causes `NameError` at runtime. Check existing constants before referencing.

3. **Emoji in regex patterns.** The persona mention `@000♎️` uses a Unicode emoji. Python source files may have encoding issues with regex escapes. Use `or "@000" in text` (prefix match) instead of exact emoji match for robustness.
