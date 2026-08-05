# When Audit Instinct Misses the Real Bug

The phased-serial-debug skill is for live-service failures. The "kadi bangang" case (2026-08-05) was a perception of agent failure that was actually an edge-layer failure. The audit instinct was to scan `hermes agent` features against upstream. The real bug was at the Telegram gateway.

## Cross-Reference Pattern

When user reports "agent feels broken/stupid/slow":

1. **First question: which layer broke?** — Agent (reasoning) vs Edge (gateway/network) vs Wiring (multiple processes) vs Gate (hooks/audit) vs Memory (provider state).
2. **Diagnostic sequence:** see `hermes-upstream-audit` references/2026-08-05-gateway-vs-agent-decode.md for the 5-step edge-first probe.
3. **Only after layers 1-4 are clean** does the agent itself become the suspect.

## Why This Belongs Here

The phased-serial-debug skill is the canonical diagnostic pattern for live failures. The "kadi bangang" case is a live failure that didn't get diagnosed as a phased-serial-debug case — it got diagnosed as an "audit" (compare to upstream). The audit instinct was wrong. The right instinct was "phased-serial-debug the edge layer first."

## Layer Addition to Phase 2

The skill's existing Phase 2 layer isolation tests (Layer 1-4) covered protocol levels. The 2026-08-05 case exposed that adapter-level faults (DoH discovery, async DNS fallback) live BELOW the protocol tests but ABOVE the application logic. Add adapter-level probes:

```bash
# Adapter-level (befocket for stuck-on-Connecting-style failures)
ss -tnp | grep -E "<pid>|<service>"
strace -f -p <pid> -e trace=network,connect 2>&1 | head -50
cat /etc/gai.conf  # DNS resolution precedence
cat /etc/nsswitch.conf | grep hosts
```

If all of these look correct but the app is still stuck, the bug is in the adapter's async/event loop logic — not in networking per se. That's an upstream fix territory, not a config patch.

## Lesson to Carry Forward

**Edge congestion masquerading as agent failure is the #1 false-positive trap in live-system debugging.** Phased-serial-debug is the right pattern, but the FIRST phase must be "is this even agent failure?" — not "what's the agent-level fix?"

This is a perception problem, not a tooling problem. The fix is diagnostic discipline at session start:

```
User: "agent feels off"
Agent: STOP. Check edge first. Don't assume agent.
```

## The Five-Rule User Constraint (Arif 2026-08-05)

Phased-serial-debug sessions with Arif must also pass the user's 5-rule spec:

1. **Cognitively same level.** Status updates in mixed BM+English, level manusia. No jargon dump.
2. **Beyond language.** High signal truth decode. Real state, not surface recap.
3. **No quiet hours.** Update bila-bila, Arif reads bila ready.
4. **Code → AAA.** When a fix is needed, route to OpenClaw/OpenCode via AAA. Never ask Arif coding specs.
5. **Verify deployed, not documented.** "Hang check semua" — actually run the verification, don't just report.

In phased-serial-debug terms: rule 5 = "verify phase, not just apply phase". The current skill already has this in Phase 4 ("DO NOT claim success unless the user's symptom is gone"). The user rule is the same, restated: don't report "fixed" until symptom is sealed.
