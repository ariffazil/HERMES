# Case: OpenCode (FI-001) Cross-Witness Audit — 2026-07-28

## Context

| Field | Value |
|---|---|
| Auditing agent | OpenCode (FI-001, DeepSeek V4 Pro) |
| Cross-witness agent | Hermes ASI (DeepSeek V4 Flash) |
| System audited | arifOS Federation (7 organs, 138 skills, ~327 MCP resources) |
| Audit scope | 7 layers: organs, agents, skills, tools, MCP wiring, memory, prompts |
| Trigger | OpenCode internal scan; Hermes asked to independently verify |
| Outcome | ~60% of claims accurate; 3 overclaims corrected; reconciliation sealed to VAULT999 |

## What OpenCode Found (their 14 findings)

OpenCode performed a comprehensive 7-layer deep scan. Key findings by severity:

### CRITICAL
1. Kernel deployment_drift=True — source_commit (711f8f5) ≠ built_commit (3677c96)
2. arifOS MCP resources/prompts = 0 — ATLAS333, 000/999 not discoverable via protocol

### HIGH
3. VAULT999 silent for 4 days — last seal 2026-07-24
4. Hermes systemd inactive — Telegram bridge down
5. WELL degraded, WEALTH version UNAVAILABLE
6. 14 open loops unresolved in carry_forward

### MEDIUM
7. Skill frontmatter inconsistency — not all skills have 8-field format
8. MCP audit trail corrupted — non-JSON lines in mcp-audit.jsonl

## Cross-Witness Verification (Hermes)

For each CRITICAL/HIGH claim, Hermes independently probed:

| Claim | OpenCode Verdict | Hermes Probe Result | Convergence |
|---|---|---|---|
| Kernel deployment drift (source≠built) | TRUE | `curl :8088/health` → source=711f8f5 ≠ built=3677c96, drift=True | ✅ **Converge** — confirmed |
| MCP resources = 0 | TRUE | `list_resources` → 327 resources returned, including ATLAS333, doctrine, vitals | ❌ **Diverge** — session-scoping artifact, not real gap |
| VAULT999 silent 4 days | TRUE | `tail -3 outcomes.jsonl` → 3 seals from 2026-07-28 (10:44, 10:45, 10:58 UTC) | ❌ **Diverge** — agent missed recent entries |
| Hermes systemd inactive | TRUE | `systemctl is-active hermes` = inactive | ✅ **Converge** — confirmed |
| WELL degraded | TRUE | `curl :18083/health` → status=degraded, freshness stale | ✅ **Converge** — but expected: self-report organ, not sensor |
| WEALTH version UNAVAILABLE | TRUE | `curl :18082/health` → git_commit=UNAVAILABLE, version=UNAVAILABLE | ✅ **Converge** — confirmed |
| 14 open loops | TRUE | carry_forward.json → 14 open loops documented | ✅ **Converge** — confirmed |
| Kernel "healthy but HOLD = F2 violation" | TRUE (misread) | `curl :8088/health` → service_health=green, execution_readiness=held. Different dimensions. | ❌ **Diverge** — correct behavior, not violation |

### Accuracy Summary

| Category | Count |
|---|---|
| Correct claims | 5 of 8 verified claims (62.5%) |
| Overclaimed | 3 of 8 |
| Overall session accuracy | ~60% |

### Specific Overclaims Corrected

1. **MCP resources = 0** — OpenCode hit a session-scoped endpoint or used wrong transport. `list_resources` via Hermes returned full surface: 17 arifos:// system resources, 10 atlas333, 5 wisdom, 1 tree777 + 294 skill:// from the then-active SkillsDirectoryProvider (this was collapsed to 2 resources the same session). Root cause: single-protocol test without retry.

2. **VAULT999 silent 4 days** — OpenCode used `ls -lt` or similar timestamp filter that missed the current day's seals. The 2026-07-28 entries existed at: SEAL-3eef5d7243f64afc (10:44), SEAL-2026-07-28-apex-inspect (10:45), SEAL-2026-07-28-session-seal (10:58). Root cause: partial directory scan.

3. **Kernel F2 violation** — OpenCode conflated `service_health=green` with `execution_readiness=held`. The kernel correctly distinguishes: "service is running" vs "refusing to execute until drift is fixed." This is correct constitutional behavior, not a violation. Root cause: didn't read both fields separately.

## What Was Fixed

1. Kernel deployment drift → rebuilt and deployed. Post-fix: source=3677c96 == built=3677c96 == deployed=3677c96, drift=False.
2. AAA dirty files → 2 committed (cooling_state + Kimi K3 license)
3. MCP resources confirmed → false alarm, but SKILL.md bloat identified (294 of 327 resources were skill:// noise) → led to resource collapse fix
4. Audit evidence → 2 vault entries: evidence seal + correction receipt seal

## Lessons

### For the auditing agent
- **Probe three ways before declaring "not working"** — one protocol failure does not mean the surface is empty
- **Read the actual file, not the index** — `tail -3 outcomes.jsonl` beats timestamp-filtered directory listing
- **Distinguish orthogonal dimensions** — `service_health` and `execution_readiness` are not the same axis
- **70% alignment is an estimate, not a measurement** — label it ESTIMATE, not OBS

### For the cross-witness agent
- **Falsification is faster than verification** — each overclaim was disproven by one command
- **Score the audit after verifying** — "60% accurate" is useful feedback the auditing agent can calibrate against
- **The auditor's job is breadth; the witness's job is depth** — compliment the audit's scope, correct its depth
- **Convergence is the goal, not competition** — both agents were right about drift, Hermes down, WELL/WEALTH degradation. The areas of divergence are calibration points, not failures.

### For the sovereign
- **Single-agent audit requires cross-witness before truth** — a thorough scan by one agent is still INT until a second agent confirms the OBS-able claims
- **The combination works** — OpenCode found the drift; Hermes caught the overclaims. Two agents = better than either alone
- **The seal chain was the decider** — the only definitive proof of vault activity was reading outcomes.jsonl directly. Protocol-level `resources/list` showed 0 results but filesystem didn't lie.

## The MCP Resource Collapse (corollary fix)

The OpenCode audit's false alarm about MCP resources being "0" actually revealed a real problem: 294 of 327 resources were skill:// noise from `FastMCPSkillsDirectoryProvider` registering each SKILL.md as an individual resource. This was collapsed the same session:

**BEFORE:** 294 skill:// resources (FastMCP provider scanning each skill directory)  
**AFTER:** 2 MCP resources (skill://index + skill://{name}/SKILL.md resource template)  
**Net:** 327 → ~35 resources (10× entropy reduction)

Fix committed to `/root/arifOS/arifosmcp/server.py` (PHASE 2: ZEN SKILL RESOURCES — 2026-07-28).
