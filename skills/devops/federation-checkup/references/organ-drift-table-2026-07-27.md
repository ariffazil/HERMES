# Organ Drift Table — Worked Example
**Probed:** 2026-07-27T01:00 UTC  
**Method:** `curl -s localhost:{port}/health` for 7 organs in parallel  
**Trigger:** Arif asked to "Audit all 6 organs for drift — produce consolidated state table"

---

## Consolidated Truth Table

| # | Organ | Port | HTTP | Overall Status | Drift Status | Source Commit | Built Commit | Deployed Commit | Notes |
|---|-------|------|------|----------------|--------------|---------------|--------------|-----------------|-------|
| 1 | **arifOS** | 8088 | 200 | **healthy** | **false** (aligned) | `1ce09ba` | `1ce09ba` | `1ce09ba` | Release v2026.07.24-ZEN-SURVIVAL. First probe showed transient drift=true, re-probe confirmed aligned. |
| 2 | **A-FORGE** | 7071 | 200 | **healthy** | **false** | `1ceda13` | `1ceda13` | `1ceda13` | Identity = UNAVAILABLE (owner YELLOW). All apex UNMEASURED. |
| 3 | **AAA** | 3001 | 200 | **healthy** | **false** | `0a697d9` | `0a697d9` | `0a697d9` | Vault CONNECTED. Chain seq=0. |
| 4 | **GEOX** | 8081 | 200 | **healthy** (HOLD) | **false** (aligned) | `1ce09ba` | `1ce09ba` | `1ce09ba` | Surface drift ok=true (33/33 tools). Apex G=0 MEASURED, C_dark=0.4329 MEASURED. |
| 5 | **WEALTH** | 18082 | 200 | **healthy** | **UNKNOWN** | N/A | N/A | N/A | git_commit="UNAVAILABLE", source_sha_available=false. 12 tools loaded vs 8 canonical. |
| 6 | **WELL** | 18083 | 200 | **degraded** | **UNKNOWN** | `4f20c24` | — | — | **11.8h stale state.** MOCK biometrics. WELL_HOLD signal. INSUFFICIENT_DATA. |
| 7 | **FLAME/WITNESS** | 18084 | 200 | **warn** | **DIVERGENCE** (3/4) | `4f20c24` | — | — | 3/4 checks agree, 1 diverges. Source integrity INTACT. |

---

## Per-Organ Detail

### 1. arifOS (:8088)
- **Status:** `healthy`
- **Release:** `v2026.07.24-ZEN-SURVIVAL`
- **Drift verdict:** `aligned` — all three commits match at `1ce09ba`
- **Identity hash:** `632a3b46d0ad...`
- **MCP protocol:** Streamable HTTP (2025-11-25)
- **Apex scalars:** G=0.0 MEASURED, C_dark=0.4329 MEASURED, QDF=0.0 MEASURED
- **Notable:** First probe showed transient drift=true (source=88f5eb7 vs built=1ce09ba) but re-probe confirmed aligned. May be a race condition in health endpoint computation.

### 2. A-FORGE (:7071)
- **Status:** `healthy`, degraded_mode=false
- **Drift verdict:** `false` — source=built=deployed=`1ceda13`
- **Authority ceiling:** `777_FORGE`
- **Identity:** `UNAVAILABLE` (owner YELLOW — identity_missing)
- **SCT mutation gate:** required, enforced, bypass=none, env=production
- **Apex:** All UNMEASURED

### 3. AAA (:3001)
- **Status:** `healthy`
- **Drift verdict:** `false` — source=built=deployed=`0a697d9`
- **Vault:** CONNECTED, chain seq=0
- **Gateway:** AAA, protocol A2A
- **Motto:** "Ditempa Bukan Diberi"
- **Apex:** All UNMEASURED

### 4. GEOX (:8081)
- **Status:** `healthy` with kernel_verdict=HOLD
- **Drift verdict:** `false` (aligned) — source=built=deployed=`1ce09ba`
- **Surface drift:** ok=true — 33/33 canonical tools loaded, 0 drift, 0 gap
- **Identity:** `geox-5da0cdd8`, verified=true
- **Physics manifest hash:** `sha256:c905aef8e16b...`
- **Apex:** G=0.0 MEASURED, C_dark=0.4329 MEASURED, QDF=0.0 MEASURED
- **Owner:** GREEN (identity_verified, public_tools=33, kernel_verdict=HOLD, service_healthy)

### 5. WEALTH (:18082)
- **Status:** `healthy`
- **Drift verdict:** **cannot determine** — git_commit="UNAVAILABLE", source_sha_available=false
- **Tools:** 12 loaded, 12 public, 8 canonical
- **Layers:** wealth_core, wealth_contracts, wealth_mcp, wealth_arifos_bridge, wealth_compat
- **Transport:** streamable-http
- **Apex:** All UNMEASURED
- **Note:** Missing git provenance makes drift assessment impossible from this endpoint alone. This is a persistent instrumentation gap.

### 6. WELL (:18083)
- **Status:** `degraded`
- **Drift verdict:** cannot determine — no deployment_drift field in health response
- **State age:** **11.8 hours stale** (source_timestamp=2026-07-26T13:13:45)
- **Freshness band:** FRESH (service alive) but state_age_hours=11.8 exceeds stale_after_seconds=14400 (4h)
- **Honesty:** `MOCK` — "not live biometrics. Do not treat as body truth."
- **Signal:** `WELL_HOLD`, domain_data_readiness=`INSUFFICIENT_DATA`
- **Metrics:** cognitive.clarity=10, decision_fatigue=3.4
- **Owner:** YELLOW (sovereign_state_unknown, biometric_state_fresh_but_insufficient, canonical_tools=22 expected)
- **Boundary notice:** "Not diagnosis. Not therapy. Reflective readiness only."

### 7. FLAME / WITNESS (:18084)
- **Status:** `warn`
- **Organ:** WITNESS, version 1.2.0
- **Consensus:** `DIVERGENCE` — 3/4 checks agree, severity=WARN
- **Sources:** proc=ok, prometheus=ok, well_machine_state=ok, well_health=ok (all 4 ok individually)
- **Well self-reported:** degraded
- **Source integrity:** INTACT — head_commit=`4f20c24ede91`, 3/3 files intact, no violations
- **Advanced service probes:** verdict=OK

---

## Action Items

| Priority | Issue | Organ | Recommendation |
|----------|-------|-------|---------------|
| **HIGH** | 11.8h stale state | WELL (:18083) | Refresh state.json — biometric state is stale. Verify biometric pipeline. |
| **MEDIUM** | MOCK biometrics | WELL (:18083) | Replace mock data with real sensor/somatic input. Current data flagged as non-live. |
| **MEDIUM** | DIVERGENCE consensus | FLAME/WITNESS (:18084) | Investigate which of the 4 checks diverges. 3/4 agree but 1 off. |
| **LOW** | Missing git provenance | WEALTH (:18082) | No git_commit or source_sha available — instrumentation gap. |
| **LOW** | Identity UNAVAILABLE | A-FORGE (:7071) | Identity missing (owner YELLOW). May need identity initialization. |
| **INFO** | All apex UNMEASURED | WEALTH, A-FORGE, AAA | Only arifOS and GEOX report measured apex scalars. Others show UNMEASURED. |

---

## Diagnostic Commands Used

```bash
# Parallel probe (all 7 organs)
for port_info in "arifOS:8088" "A-FORGE:7071" "AAA:3001" "GEOX:8081" "WEALTH:18082" "WELL:18083" "FLAME:18084"; do
  name="${port_info%%:*}"
  port="${port_info##*:}"
  echo "=== $name ($port) ==="
  curl -sf --max-time 5 "http://localhost:$port/health" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Status: {d.get(\"status\",\"?\")}')
dd=d.get('deployment_drift',{}) or d.get('software_release',{}) or {}
drift=dd.get('drift') if 'drift' in dd else d.get('deployment_drift_status','?')
src=dd.get('source_commit','?') or d.get('git_version','?') or d.get('commit','?')
bld=dd.get('built_commit','?') or d.get('build_commit','?')
dep=dd.get('deployed_commit','?')
print(f'  Drift: {str(drift)[:8]} | src={str(src)[:12]} built={str(bld)[:12]} dep={str(dep)[:12]}')
print(f'  Tools: {d.get(\"tools_loaded\",\"?\") or d.get(\"public_tools\",\"?\") or d.get(\"tool_count\",\"?\")}')
" 2>/dev/null || echo "  ❌ Unreachable"
done

# Full JSON extraction for arifOS deployment drift
curl -s http://localhost:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin); sr=d.get('software_release',{})
print(f'deployment_drift_status={d.get(\"deployment_drift_status\")} drift={sr.get(\"drift\")}')
print(f'source={sr.get(\"source_commit\",\"?\")[:12]} built={sr.get(\"built_commit\",\"?\")[:12]} deployed={sr.get(\"deployed_commit\",\"?\")[:12]}')
"

# GEOX specific: surface drift check
curl -s http://localhost:8081/health | python3 -c "
import json,sys; d=json.load(sys.stdin); sd=d.get('surface_drift',{})
print(f'surface_drift.ok={sd.get(\"ok\")} canonical={sd.get(\"canonical_count\")} live={sd.get(\"live_count\")} gaps={sd.get(\"gap_count\")}')
"

# FLAME/WITNESS consensus detail
curl -s http://localhost:18084/health | python3 -c "
import json,sys; d=json.load(sys.stdin); c=d.get('consensus',{})
print(f'verdict={c.get(\"verdict\")} checks={c.get(\"checks_consensus\")}/{c.get(\"checks_total\")} severity={c.get(\"severity\")}')
print(f'source_integrity={d.get(\"advanced\",{}).get(\"source_integrity\",{}).get(\"verdict\")}')
"
```
