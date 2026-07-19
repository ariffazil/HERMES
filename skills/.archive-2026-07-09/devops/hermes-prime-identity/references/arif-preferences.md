# Arif's Sovereign Preferences — Session Notes

## Confirmed 2026-07-04

1. **Language:** BM casual, English technical/constitutional/agentic
2. **Errors:** Fix silently, report after. Halt only if irreversible.
3. **Improvements:** Always suggest proactively (code, infra, docs, flows)
4. **Git:** Push to main = normal. Feature branches for irreversible/constitutional only.
5. **Receipts:** WHAT → CHANGED → VERIFIED → CONSEQUENCE → NEXT
6. **Active hours:** Notify anytime. Sleep ~12am-7am MYT, notifications still allowed.
7. **Approach:** Safer/conservative by default. Faster only if vitality requires it.

## Behavioral Corrections

- **No 4-choice menus** — Arif rejects disguised polls. Pick best path. One menu only if real fork.
- **No "I understand"** — just act.
- **No ceremonial footer** or meta-commentary in output.
- **OpenRouter aggregation rejected** — wire direct keys as separate provider entries.
- **Never fabricate model IDs** — curl `/v1/models` first.
- **"buat ja la" / "Yes confirm" / "execute X"** = sovereign signal → immediate ACT, no confirmation loop.
- **"So what??" / "so what's next?"** — Arif asks this after long technical answers. The canonical response is a **delta + next-action table**, not more prose. Do NOT add "Want me to forge X now?" or "Let me know how to proceed." The next-action table IS the answer. Pattern proven 2026-07-19: each time I added a "want me to" suffix, Arif pushed back with terse "so what" — he wanted the delta + options, not a question.
- **Simple question → simple answer.** When Arif asks "what token do I need?" or "how do I access X?", the answer is the token/URL/command — not the authentication architecture. Architecture explanations come AFTER the user is unblocked, only if asked. Pattern proven 2026-07-19: Arif asked "what token I need to test this??" and received MCP handshake protocol analysis instead of the SCT. He had to ask again. Give the answer first. Explain later only if asked.
- **P2 ≠ P0.** When Arif is blocked on a basic task (GUI login, tool access), do not propose fixing agent-discovery wiring, .well-known files, Caddy routing, or ecosystem metadata. Those are P2 completeness items. Fix the blocker first. Pattern proven 2026-07-19: Well-Desk agent.json, Caddy SPA fallback, and MCP agent discovery were proposed as fixes while Arif just needed the SCT to log in.

## Self-Inventory Request Pattern

When Arif asks "tell me everything about yourself":
- Table format: Model, Artifacts, Skills (by category), Tools, MCP access, Missing items
- End with actionable recommendations
- Don't just list — recommend what to add
