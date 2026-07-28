# Dual-Agent Convergence — OpenCode + Hermes (2026-07-28)

## Session Overview

Arif (F13) triggered a reality alignment audit via OpenCode (FI-001). OpenCode produced a 7-layer deep scan covering organs, agents, skills, tools, MCP wiring, memory, and prompts. Hermes was asked to independently verify the findings and seal the result.

## Key Findings

### Convergence Scorecard

| Claim | OpenCode | Hermes Probe | Tag |
|-------|----------|-------------|-----|
| Hermes systemd inactive | ✅ Found | ✅ Confirmed `systemctl is-active hermes` = inactive | CONVERGE |
| Kernel deployment drift | ✅ Found | ✅ Confirmed source≠built, drift=true | CONVERGE |
| WEALTH version UNAVAILABLE | ✅ Found | ✅ Confirmed git_commit="UNAVAILABLE" | CONVERGE |
| WELL degraded | ✅ Found | ✅ Confirmed status=degraded (self-report, expected) | CONVERGE |
| 14 open loops | ✅ Found | ✅ Confirmed in carry_forward | CONVERGE |
| MCP resources = 0 | ❌ Claimed | ❌ `list_resources` returned 34 including ATLAS333, doctrine, vitals | CORRECT |
| VAULT999 silent 4 days | ❌ Claimed | ❌ 3 seals found from TODAY (10:44, 10:45, 10:58) | CORRECT |
| Kernel F2 violation | ❌ Claimed | ❌ service_health=green ≠ execution_readiness=held — correct behavior | CORRECT |

**Convergence score: 5/8 = 0.625**

### Root Cause of False Alarms

1. **MCP resources = 0:** OpenCode's MCP client may have been using a different transport or session scope that hid the resources. The kernel serves resources via Streamable HTTP; a raw curl POST to `/mcp` with wrong content-type gets 406, which could be read as "no resources."

2. **VAULT999 silent 4 days:** OpenCode may have queried the vault before the day's seals were written, or queried a different vault path than outcomes.jsonl.

3. **Kernel F2 violation:** Category error between service_health (is the binary running?) and execution_readiness (is the kernel authorizing actions?). Different axes, both reported accurately.

## The Zen Resource Collapse

OpenCode also implemented the fix: replaced `FastMCPSkillsDirectoryProvider` (which dumped 294 individual skill:// resources) with:

- **Before:** 294 resources (138 skill://SKILL.md + 156 skill://_manifest)
- **After:** 2 resources (`skill://index` + `skill://{name}/SKILL.md` template)
- **Total:** 327 → 34 resources (−293)

Implementation in `arifOS/arifosmcp/server.py` (Phase 2, line 552+):

```python
@mcp.resource("skill://index", ...)
def skill_index_resource() -> str:
    return json.dumps({"skills": _skill_index, "total": len(_skill_index)})

@mcp.resource("skill://{name}/SKILL.md", ...)
def skill_by_name_resource(name: str) -> str:
    path = SKILLS_ROOT / name / "SKILL.md"
    if not path.is_file():
        raise FileNotFoundError(f"Skill not found: {name}")
    return path.read_text()
```

## Lessons

1. **Single-agent audit is OBS.** A thorough scan by a capable agent is observation, not truth. The observing agent can make category errors, query stale state, or misinterpret results.

2. **Cross-witness is TRUTH.** When two agents independently converge on the same finding, that finding is more reliable than either agent's full report. The convergence score (5/8 = 0.625) quantifies trust.

3. **False alarms must be corrected, not ignored.** All three false claims from OpenCode's audit would have been sealed as truth had Hermes not independently verified. Each correction was sealed to VAULT999.

4. **MCP resource collapse is a general pattern.** Any FastMCP server mirroring a filesystem directory as static resources can apply the same fix: 1 index + 1 template replaces N static entries.

## Seals

- `SEAL-2026-07-28-hermes-drift-fix` — Hermes drift verification + correction
- `SEAL-2026-07-28-zen-deploy` — Full federation zen: 34 resources, drift=False, 6/6 repos clean

## Files Changed

- `arifOS/arifosmcp/server.py` — 76 insertions, 62 deletions. Removed FastMCPSkillsDirectoryProvider, added skill://index + skill://{name}/SKILL.md template.
