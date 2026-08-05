# 2026-08-05 — Gateway-vs-Agent Decode Session

When Arif said "Hermes agent aku macam kadi bangang lepas tukar gateway", the audit instinct was to scan features. The actual decode was at the edge layer.

## What Triggered the Audit

Recent GIT activity (3 commits in <3 hours, 2026-08-05 subuh-pagi):
- `7d01561` feat(hermes): remove all config blocks — full toolsets, no quarantine, no allowlist
- `6b64c4b` fix: un-ignore mcp_servers/ — source code for A2A listener, agent MCP, real bridge
- `48f3bef` chore(hermes): archive corrupted config backups, add new skills

Phased-serial-debug transcript earlier that day documented **partial IPv6 hang fix** (gai.conf + force_ipv4 worked; env-var dead code reverted). Gateway was still cycling restart, just slower.

## What the Audit Found (NOT what's "missing")

The bug was not "missing feature". The bug was **edge congestion mistaken for agent slowness**:

| Symptom Arif observed | Actual root cause | Evidence |
|---|---|---|
| Bot not replying reliably | Hermes-asi-gateway.service restart-cycling (22s → 1-2min slower but not settled) | PID 1359579 started 13:44, `@ASI_arifos_bot` reply latency uncertain |
| Feels like agent is "kadi bangang" | Two gateway processes running simultaneously: `openclaw-gateway` (PID 1085689) + `hermes-asi-gateway`. Token overlap potential. | `ps -eo pid,ppid,uid,etime,stat,pcpu,pmem,comm` |
| Constitutional guard hook silent | Hook deployed 2026-08-03, ledger last entry 2026-08-05T01:34, now 13:52. 12h silence = gateway restart needed, hooks don't auto-reattach. | `tail -1 /root/AAA/ledger/constitutional_guard.jsonl` |
| Memory.md 98% full | Char limit 4000, can't write new rules. Voice — the "saya tak boleh save" feedback. | `hermes memory status` + memory tool error |

## The Decode Pattern: "Kadi Bangang" Reflex

When Arif (or any user) reports an agent feels dull/slow/forgetful, the reflex is to blame the agent. The actual probe sequence is:

1. **What's the edge state?** — gateway/service uptime, last reconnect, pending update backlog
2. **What's the gate state?** — hook fire-silence = gateway restart missed
3. **What's the wiring state?** — multiple processes claiming same token?
4. **What's the memory state?** — Honcho tier active or local fallback?
5. **Only then** — what's the agent reasoning state?

If 1-4 are clean, the agent is the problem. If any of 1-4 are broken, the agent is functioning in degraded mode — fixing the agent won't help.

## Lesson: Diagnostic Sequence Before Code Patch

When audit-mode encounters "Hermes feels off":

```bash
# 1. Edge state
systemctl status hermes-asi-gateway.service --no-pager | grep -E "Active|MainPID|Memory"
journalctl -u hermes-asi-gateway.service --since "1 hour ago" --no-pager | grep -E "Started|Stopped|failed" | wc -l

# 2. Gate state
ls -la /root/AAA/ledger/constitutional_guard.jsonl && tail -1 /root/AAA/ledger/constitutional_guard.jsonl
echo "Now:" && date -u

# 3. Wiring state
ps -eo pid,ppid,uid,etime,stat,pcpu,pmem,comm | grep -E "gateway|hermes_mcp|hermes_a2a|hermes_real_bridge" | grep -v grep

# 4. Memory state
hermes memory status 2>&1 | grep "Provider:"

# 5. Agent state - only if 1-4 OK
last receipt in VAULT999, last session transcript coherence
```

## Output Style Applied

Per Arif's 5 rules spec, this decode was delivered as:
- Mixed BM Penang + English tech (no jargon dump)
- Plain text bullet, no tables unless structural
- "Hang check" framing — verified what's deployed, not what's documented
- No coding questions back to Arif — code path → OpenClaw/OpenCode via AAA
- "Lapor-jika-seal" — partial findings only, not "everything is fine"

The user-specced rules **are the audit output format**, not just style preferences.
