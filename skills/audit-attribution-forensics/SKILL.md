---
name: audit-attribution-forensics
description: When an audit or log says X happened in file Y at line Z, verify the attribution before patching. The audit may be correct about the error and wrong about the source file — cross-unit triggering, multiple bot.py instances, stale .pyc bytecode, and audit-laundering patterns make file-level blame unreliable. Use when an audit names a specific file+line for an error, when a pasted log blames one path but inspection shows another, when multiple gateway units log to the same journal facility, or when past edits to a file seem to have no effect.
category: autonomous-ai-agents
---

# Audit Attribution Forensics

When a sibling agent, OpenClaw bot, or pasted log hands you evidence like `bot.py:51 failed: Request.__init__() got unexpected keyword argument 'data'`, the audit may be:

- Correct (the file you read is the one running and the line is the error)
- Correct about the error, wrong about the file (a different unit logs the same string format)
- Wrong about both (someone constructed a misleading report)

This skill prescribes the 5-step verification before patching.

## The Trap (2026-08-05 SADO-bot case)

The audit said: `/opt/forge-bot/bot.py` has a `data=` kwarg bug.

Inspection of `bot.py` line 13: `from urllib.request import Request, urlopen`. `urllib.request.Request` accepts `data=`. The error string format `Request.__init__() got an unexpected keyword argument 'data'` exists in both `urllib` and `requests` libraries, AND similar wrappers. The audit could be fabricated OR could refer to a different file.

Following this skill: ran 5 checks in parallel → found a sibling `/opt/hermesarifos-bot/bot.py` with DIFFERENT md5. The actual log entry came from a third unit (`hermes-asi-gateway`) invoking `forge_telegram` via A-FORGE's `requests`-based code path. Patching `/opt/forge-bot/bot.py` would have changed nothing.

## The 5-Step Verification Protocol

Run all 5 in parallel — they are independent reads. Total time: ~5 seconds. If any check returns unexpected, do NOT trust the audit's file attribution.

```bash
# 1. Read imports (does the source use urllib or requests?)
head -20 <blamed_file>

# 2. What did systemd actually invoke?
grep ExecStart /etc/systemd/system/<unit>.service

# 3. What is the live PID's working dir?
pid=$(pgrep -f <entrypoint> | head -1)
ls -la /proc/$pid/cwd 2>/dev/null

# 4. Is there stale bytecode?
find /opt/<unit> -name "*.pyc" -newer <blamed_file>
# If a .pyc is newer than .py, the running code may be the .pyc, not your edited .py

# 5. Are there sibling paths with the same name?
find /opt -name "bot.py" -o -name "<entrypoint>.py" 2>/dev/null
```

**Decision rule after step 5:**

| Result | Action |
|---|---|
| imports urllib (or requests), no .pyc drift, single file, no siblings | Audit attribution plausible → patch |
| imports urllib but error uses requests format string | Audit file wrong → find which unit logged the entry, patch THAT unit |
| Multiple sibling paths with different md5s | Audit may refer to wrong sibling → md5 + content diff |
| Newer .pyc than .py | Stale bytecode, not your edits → find . -name __pycache__ -exec rm -rf {} + and restart |
| Live PID cwd != audit's path | Wrong unit, wrong binary → systemctl shows which |

## Common Collision Patterns

### urllib vs requests kwarg signatures

| Library | Function | Accepts data= ? |
|---|---|---|
| urllib.request.Request | __init__(url, data=None, ...) | YES, validated positional |
| urllib.request.urlopen | urlopen(url, data=None, ...) | YES |
| requests.api.post | NOT APPLICABLE — requests has no Request.__init__ | N/A |
| requests.Session.send | send(request, ...) | NO |
| httpx.Client.post | post(url, data=None, json=None, ...) | YES but different semantics |

The error `Request.__init__() got an unexpected keyword argument 'data'` ONLY comes from `urllib.request.Request.__init__` rejecting a second positional or kwarg. The requests library has no Request.__init__ at the API surface — it uses PreparedRequest. So if you see this error and imports show requests, the entry point is via a wrapper module that does have a Request class with stricter signature (e.g. flask.Request, werkzeug.Request, aiohttp.ClientRequest, httpx.Request).

### Multi-bot copy pattern

Several federation units copy the same bot skeleton to different paths (`/opt/forge-bot/`, `/opt/hermesarifos-bot/`, others) with subtly different config wiring. When a single error string appears in journal, it could be from any copy. Confirm with md5sum:

```bash
md5sum /opt/*/bot.py 2>/dev/null
```

Different md5 = different code = different bug surface. The audit may have named the wrong copy.

### Audit laundering

A pasted audit might be derived from a different report (by another agent, by a tool that swallowed stack traces and re-emitted them, by a wrapper that normalized error messages). If the audit reads too clean or too comprehensive vs the journal, suspect laundering — verify the journal itself, not just the audit's interpretation:

```bash
journalctl -u <unit> --since "30 min ago" > /tmp/journal.txt
grep -c "<exact error string>" /tmp/journal.txt
# If 0 hits, the audit's evidence is not in the journal → fabricated or laundered.
```

## When to Use

- Audit names a specific file + line + error
- Code change appears to have no effect (probably wrong file)
- Bot error persists across restarts (probably wrong attribution)
- Multiple gateway units log to same journal facility (`-t` flag aggregates)
- Past edits to a file seem irrelevant (probably the runtime is a different path)

## Integration with sibling skills

- federation-runtime-forensics — covers the audit-content verification side (Section 1) and Telegram flood diagnostics (Section 2). This skill extends Section 1 with file-attribution verification.
- claim-receipt-discipline — every audit claim needs a receipt; this skill teaches you to verify the receipt's path matches reality.
- hermes-telegram-group-setup — covers "bot not replying in group" config side; this skill covers the diagnostic side when allow list is fine but bot still silent.

## Support files

- references/sado-bot-not-replying-2026-08-05.md — full walkthrough of the SADO-bot-not-replying case: allow list OK, journal revealed two distinct errors across two units, source attribution protocol applied, real cause found to be Telegram-side permission (not code).

## Pitfalls

- Don't trust shared-base error formats across libraries. A `Request.__init__() got keyword arg X` could be urllib, requests (rare), werkzeug, aiohttp, or httpx. Read imports before patching.
- Don't patch the wrong sibling. `/opt/forge-bot/bot.py` and `/opt/hermesarifos-bot/bot.py` are different files. md5 first, then decide.
- Don't assume .py is the running code. Stale `__pycache__/*.pyc` files can serve bytecode from previous edits. Clean and restart.
- Don't skip cwd check. A bug at a path you read source from is NOT your bug if the runtime cwd is elsewhere. `ls -la /proc/<pid>/cwd` is the truth.
- Don't trust a journal count. Logs can be laundered through systemd journald forwarding, journal rotation, or service restart. Grep the journal yourself, count, then act.
- Audit claims can be self-fulfilling. An agent reports "X is wrong" → another agent reads the audit → patches X. If the audit is wrong, the patch is wrong. Verify before patching.
