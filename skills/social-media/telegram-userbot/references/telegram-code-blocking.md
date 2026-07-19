## Telegram Code-Sharing Security (documented 2026-07-11)

Telegram actively monitors for login codes shared in chat. When detected:

1. Telegram sends a warning: "sign in was not allowed, because this code was previously shared by your account"
2. The login attempt is blocked even if the code was entered correctly
3. The device info is logged: "HermesASI, 1.44.0, PC 64bit, Desktop"

**Detection triggers:**
- Sending the login code as a text message in any Telegram chat
- Forwarding the Telegram login code message
- The code appears in the same conversation where the auth was initiated

**What works:**
- Entering code via web browser form (not Telegram)
- Entering code via SSH terminal
- Entering code via any non-Telegram channel

**What doesn't work:**
- Sending code to the bot in the same Telegram chat
- Any channel where Telegram can see the code text

This is a security feature, not a bug. Design auth flows accordingly.
