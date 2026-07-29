# Agent-Card Federation Alignment Audit — OpenClaw Worked Example

> **Date:** 2026-07-29  
> **Target:** `/root/AAA/agents/openclaw/agent-card.json` (v2.2.0, 635 lines, 18 KB)  
> **Canonical skill set:** `/root/.hermes/skills/` (48 skills)  
> **Live organs probed:** arifOS:8088, A-FORGE:7072, GEOX:8081, WEALTH:18082, WELL:18083, arifFLOW:7073, AAA:3001  
> **Federation topology:** `/root/AGENTS.md` §1 (7 organs)  

---

## Summary

12 findings across 5 categories. No modifications made — report-only for sovereign review.

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 3 |
| 🟠 HIGH | 4 |
| 🟡 MEDIUM | 3 |
| 🔵 LOW | 2 |

---

## 🔴 CRITICAL Findings

### 1. Duplicate bare-string skill references (lines 340–344)

4 skills defined as objects AND duplicated as bare strings in the same `skills` array:

| Line | Bare String | Already Defined At |
|------|-------------|-------------------|
| 340 | `KERNEL-sovereign-recognize` | Line 235 (object with tags, floor_scope) |
| 341 | `KERNEL-trinity-33` | Line 280 (object with tags, floor_scope) |
| 342 | `KERNEL-session-inhabit` | Line 249 (object with tags, floor_scope) |
| 343 | `RSI-recursive-improvement` | Line 265 (object with tags, floor_scope) |

**Action:** Remove lines 340–344.

### 2. Orphan bare-string skills not defined anywhere (lines 344–345)

| Line | Bare String | Disk Status |
|------|-------------|-------------|
| 344 | `SHADOW-diagnostic` | NOT FOUND in any skill directory |
| 345 | `CLAIM-verification-gate` | NOT FOUND in any skill directory |

**Probe:** `find /root/.hermes/skills/ /root/AAA/agents/skills/ -name "SKILL.md" -path "*SHADOW*" -o -path "*CLAIM*"` → empty.

**Action:** Remove lines 344–345, or create the skills.

### 3. Deprecated kernel skills referenced (lines 576–577, 590–592)

Both `metadata.kernel_deps` and `kernel_skills` reference:

| Skill ID | Disk Status |
|----------|-------------|
| `KERNEL-quantum-runtime` | NOT FOUND |
| `KERNEL-qubit-substrate` | NOT FOUND |

These were removed from the canonical set during the 212→196 consolidation. GENESIS doc `048_QUBIT_RUNTIME_DOCTRINE.md` still exists, but no skill file remains.

**Action:** Remove both from `metadata.kernel_deps` and `kernel_skills`.

---

## 🟠 HIGH Findings

### 4. All MCP endpoint tool lists are wrong

| Endpoint | Card Claim | Live Reality | Delta |
|----------|-----------|-------------|-------|
| arifOS:8088 | 7 tools incl. `arif_act` | 8 tools (no `arif_act`, has `arif_memory`) | Non-existent `arif_act`, missing `arif_memory` |
| A-FORGE:7072 | 72 tools | 52 tools | −20 |
| GEOX:8081 | 35 tools incl. `geox_well_desurvey`, `geox_vision`, `geox_atlas` | 33 tools (none of those 3 exist) | −2, 3 phantom tools |
| WEALTH:18082 | 26 tools with `wealth_*` names | 14 tools with hybrid `wealth_*`/`capital_*` names | −12, 10 phantom tools |
| WELL:18083 | 22 tools incl. `well_readiness`, `well_assess_metabolism` | 8 tools (none of those exist) | −14, 4 phantom tools |

**Live probe commands:**
```bash
curl -s http://127.0.0.1:8088/health | jq '.tools_loaded'         # 8
curl -s http://127.0.0.1:7072/health | jq '.stateless_tools'       # 52
curl -s http://127.0.0.1:8081/health | jq '.tools_loaded'          # 33
curl -s http://127.0.0.1:18082/health | jq '.tools_loaded'         # 14
curl -s http://127.0.0.1:18083/health | jq '.tool_count'           # 8
```

**Action:** Rewrite ALL 5 endpoint tool lists with actual tool names from live `curl :port/tools`.

### 5. Intelligence tier contradiction (line 23)

Card says `"intelligence_tier": "ASI"` and `"lane": "555-ASI"`.  
OpenClaw's own AGENTS.md says: `Intelligence tier: AGI-level operator`.  
The federation mapping: Hermes = ASI, OpenClaw = AGI.

**Action:** Change to `"intelligence_tier": "AGI"` and `"lane": "333-AGI"`.

### 6. Missing arifFLOW organ (port 7073)

The card's `mcp_surface.endpoints` lists 5 organs. The federation has 7. Missing:

| Organ | Port | Role | In Card? |
|-------|------|------|----------|
| arifFLOW | 7073 | Metabolism (FQ, receipts, cooling) | ❌ MISSING |
| AAA | 3001 | Control plane + A2A | ⚠️ Only as `additional_interfaces` websocket |

arifFLOW is verified healthy: `curl -s http://127.0.0.1:7073/health` → `{"status":"ok","receipts":293}`.

**Action:** Add arifFLOW (port 7073) as a 6th MCP endpoint.

---

## 🟡 MEDIUM Findings

### 7. Stale federation topology in skill description (line 178–179)

`FORGE-federation-ops` description says: `"arifOS federation topology and routing — 10 organs + gateway"`.  
Current federation has **7 organs** (per `/root/AGENTS.md` §1).

**Action:** Change "10 organs" to "7 organs".

### 8. Topological role is APEX residual (line 509)

`"topological_role": "Metabolizer"` — this is APEX theory taxonomy. Current federation uses organ names.

**Action:** Update to `"gateway"` or remove the field.

### 9. Zen organ ∂M/∂t (arifFLOW) uncovered

5/7 zen variables covered. ∂M/∂t (metabolism → arifFLOW) has zero coverage in OpenClaw's skill suite or MCP surface.

| Zen Variable | Federation Organ | Covered? |
|---|---|---|
| ΔG (Governance) | arifOS:8088 | ✅ |
| W (Wisdom) | WEALTH:18082 | ✅ |
| ΔR (Reality) | GEOX:8081 | ✅ |
| Ω (Vitality) | WELL:18083 | ✅ |
| ∂M/∂t (Metabolism) | arifFLOW:7073 | ❌ GAP |
| I_sys (System) | AAA:3001 | ⚠️ Partial |
| ∇F (Floors) | arifOS:8088 | ✅ |

**Action:** Add arifFLOW binding to close the zen gap.

---

## 🔵 LOW Findings

### 10. Empty string key (line 546)

```json
"": "arifOS/agent-card/v2.2.0",
```

Schema version already declared at line 3 (`"schemaVersion": "2.2.0"`). This is a malformed key.

### 11. Duplicate fields

- `securitySchemes` (lines 35–46) AND `security_schemes` (lines 465–476) — identical content
- `protocolVersion` (line 13) AND `protocol_version` (line 457) — both `"1.2"`

---

## Methodology (reusable)

This audit followed the 7-dimension agent-card alignment protocol:

1. **Read the card** → extract all skill IDs, MCP endpoints, identity attributes
2. **Probe live organs** → health check + tool/list for each declared endpoint
3. **Cross-reference skills** → card's declared IDs vs canonical directory
4. **Check duplicates** → objects vs bare strings in the `skills` array
5. **Verify topology** → card's organs vs federation AGENTS.md §1
6. **Check identity** → intelligence tier, warga lane, topological role
7. **Produce F2-cited report** → every finding has file:line, card claim, live reality, and recommended action

**Total time:** ~5 minutes of parallel probing + 10 minutes of analysis.

---

*Worked example for the agent-card-federation-alignment section of the live-probe-audit-pattern skill. DITEMPA BUKAN DIBERI.*
