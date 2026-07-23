# FORGE Duty-Pulse Interpretation

## Three Duty Types

FORGE fires three autonomous duties via cron. Each produces a report. Interpret them fast.

### 1. Drift Scanner (daily 02:00 MYT)

**What it checks:** arifOS runtime vs source commit, unknown public ports, memory usage, identity drift.

**False-positive patterns:**
- `arifOS DRIFT: src=349d5fb runtime=349d5fb92` → same commit, different hash length. Compare first 7 chars: `[0:7]`.
- `UNKNOWN_PUBLIC_PORTS` → list of 50+ ports. These are third-party deps (postgres:5432, redis:6379, nats:4222, etcd:2379) + ephemeral sockets. Not real drift. Only flag NEW ports that weren't there the day before.
- `IDENTITY_DRIFT: DRIFT` → check `carry_forward.json` first. Often a stale flag from a deployment canary HOLD, not real drift. Look at `last_seal.verdict` — if SEAL, the drift flag is stale.
- Ports 3457/3458 → gold trading API sockets. Known, ignore.
- New ports like 6277/6274 → consensus/RPC ports. Investigate once, then classify as known.

**Real drift signals (act on these):**
- arifOS runtime ≠ source AND commits are genuinely different (not hash-truncation)
- MEMORY_USAGE > 95%
- New unknown ports in unfamiliar ranges when no deployment occurred

**Diagnosis pattern:**
1. `cat /root/.local/share/arifos/carry_forward.json` → check last_seal
2. `git -C /root/arifOS log --oneline <runtime>..<source>` → count real commits ahead
3. `free -h` → confirm memory pressure
4. One-line verdict + offer to fix

### 2. Constitutional Sync (daily 07:00 MYT)

**What it checks:** Skills, agents, seal chain integrity, floor compliance.

**False-positive patterns:**
- 13 "agents" without IDENTITY.md → these are organizational folders (_archive, _brief, _docs, agent-zero, etc.), not real agents. The scanner treats every directory under agents/ as an agent. Ignore these unless count changes.
- Missing `floor_scope` and `owner` declarations on skills → institutional. Bulk-imported skills from OpenClaw-Hermes migration never carried this metadata. ~17-29 skills affected, stable across runs.
- Compliance score drops from 80%→68% when skill count grows 50→120 → denominator effect from bulk import, not regression.
- `seq=None` or `seq=2` after `seq=9900+` → sequence wrap is normal. Multi-epoch seal chain.

**Real signals:**
- Compliance drops with no skill-count growth
- New agent stubs appearing (means new agent dirs were created)
- Floor compliance matrix changes (F13 owner binding dropping significantly)
- Seal chain seq jumping backward by hundreds → counter reset, investigate

### 3. Vitality Pulse (daily 15:00 MYT)

**What it checks:** Organ health, VPS score, entropy, contradictions, tools, VAULT999 entries.

**False-positive patterns:**
- `VPS: UNKNOWN` — correct behavior. Human dimension requires biometric injection. Don't fabricate scores.
- `1 contradiction(s) detected` → single duplicate skill name between Hermes and OpenClaw skill stores. Always `wealth-capital-thermodynamics` or similar. Known, ignore.
- `Entropy: 0/6` → entropy probes not getting data, not "zero entropy." Yellow flag is informational.
- `6 contradictions` → 6 duplicate skill names after bulk migration. Not real contradictions.

**Real signals:**
- Entropy climbing day-over-day (0→2→4→6)
- New contradictions appearing (different names, not just stale duplicates)
- VAULT999 growth rate changes (normal is ~5-13/day, spike >50 = bulk seal operation)
- Governance: UNCERTAIN → investigate why
- Machine: STRAINED → check memory/CPU

### Output Template

For all three duty types, respond in ≤3 lines + one-line verdict:
```
[Signal summary] — [real/false-positive diagnosis]. [Action if needed].
```

Never verbose. Never recap the full report. The human got the same notification.
