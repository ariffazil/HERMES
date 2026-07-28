---
name: federation-checkup
description: "Standard checkup protocol for the arifOS federation — dual-probe pattern, floor interpretation, flag hierarchy, and sweep-and-classify housekeeping."
related_skills: [bloodhound-federation-mapping]
triggers:
  - "how's the system"
  - "status"
  - "checkup"
  - "semua organ hijau"
  - "apa yang kena perhati"
  - "federation health"
  - "organs running"
  - "sweep the federation"
  - "find everything pending"
  - "clean up"
  - "what's stale"
  - "orphaned"
  - "housekeeping"
  - "authority recovery"
  - "P0 authority"
  - "identity diagnostics"
  - "federation repair"
  - "build identity drift"
  - "padu"
  - "PulseMCP"
  - "pulsemcp"
  - "ecosystem listing"
  - "external verification"
  - "public MCP listing"
  - "floor table audit"
  - "consumer drift"
  - "FLOOR_TABLE"
  - "Fasa 1 audit"
  - "SPEC rejection"
  - "seal status audit"
  - "constitutional source audit"
  - "one-shot"
  - "delegation seal"
  - "buat ja semua"
  - "autonomous execution"
  - "next-horizon"
  - "bangang"
  - "HITL"
  - "human bottleneck"
  - "human is the bottleneck"
  - "bottleneck audit"
  - "BANGANG HITL"
  - "agentic intelligence"
  - "where does the system wait for me"
  - "every HITL surface"
  - "map all"
  - "pending seal"
  - "open loops"
  - "pending sovereign ack"
---

# Federation Checkup — Dual-Probe Protocol

> **Quick version?** Type `/padu` in Telegram — one command, 6 layers (Organ, Nadi, Segel, Tenaga, Aliran, Perhatian), 3 seconds.
> **Full deep check?** Keep reading below.

> Always run both probes. Reconcile before reporting. Surface by flag hierarchy.

## BloodHound-Aware Architecture (Transport ≠ Privilege)

See `references/bloodhound-federation-insights.md` for the full BloodHound→arifOS mapping and 3-phase audit architecture.

**Core insight:** TCP transport reachability (11/11 edges green) is NOT federation security. The real surface is **which MCP tools can mutate constitutional state** — 3 tools are 1-hop from F13 (`arif_forge`, `arif_judge`, `arif_seal`). Every other tool is observe-only from a constitutional perspective.

## The Core Lesson

**`curl :port/health` ≠ organ health. It only means the process is alive.**
**Diagnostic-first is an anti-pattern for Arif.** When the system is already up and operational, verbose diagnostic probes generate stale/corrected takeaways that waste session time. A prior session ran full P0/P1 diagnostics only to have Arif confirm the system was already operational — the takeaways were wrong. Trust Arif's signal over self-generated probe anxiety.

**Rule:** If the system is confirmed up and Arif wants to move forward, skip the dual-probe. Probes only when there is a genuine symptom to explain. The canonical source of truth for "is the system healthy" is `curl :PORT/health` + Arif's own observation — not a verbose multi-step diagnostic ritual.
**Rule:** If the system is confirmed up and Arif wants to move forward, skip the dual-probe. Probes only when there is a genuine symptom to explain. The canonical source of truth for "is the system healthy" is `curl :PORT/health` + Arif's own observation — not a verbose multi-step diagnostic ritual.
The Observatory (`/api/status`) shows the real constitutional state — per-floor scores, vitality, drift, witness channels. These two probes frequently disagree. Always run both and reconcile.

## Automated Artifact Generation (Cloud AI Ingestion)

For producing immutable federation reality artifacts for cloud AI ingestion (the **epistemic bridge** — Truth without Vector), use the `federation_reality_probe.py` (v2.0.0) via Makefile targets or direct invocation.

### make reality — Standard Probe

```bash
cd /root/arifOS
make reality
# Equivalent to:
python3 scripts/federation_reality_probe.py --write-md --write-json --public
```

Outputs: `var/reality/federation_reality_<timestamp>.json` + `FEDERATION_REALITY_SNAPSHOT.md`

Checks: organ liveness, tool count vs expected, version freshness, public HTTPS endpoint, endpoint detail, known gaps.

### make reality-deep — Full Scope Sweep + F13 Reachability

```bash
cd /root/arifOS
make reality-deep
# Equivalent to:
python3 scripts/federation_reality_probe.py --scope --write-md --write-json --public --verbose
```

Includes all `make reality` checks PLUS:

**Tool scope sweep:** For every MCP-enabled organ, performs `tools/list` (full names + prefix classification like `arif_`, `geox_`, `capital_`, `well_`), `resources/list` (resource URIs), `prompts/list` (prompt names). Results appear in three dedicated subsections: "Tool Names by Prefix", "Resource URIs", "Prompt Names".

**F13 SOVEREIGN reachability:** Cross-checks:
- `GENESIS/FLOOR_TABLE.json` — exists, parseable, authority field, floor count
- `GENESIS/000_KERNEL_CANON.md` — exists, F13/SOVEREIGN mention count, file size
- Every organ's `/health` response for `f13_status`, `sovereign_status`, `sovereign`, or `human_veto` fields
- All 13 constitutional floors emitted in a dedicated F13 table in the MD report

### When to Use Which

| Situation | Command |
|-----------|---------|
| Quick checkup, paste into chat | `make reality` |
| Deep audit across all MCP surfaces | `make reality-deep` |
| Debugging tool count mismatch | `make reality-deep` (see actual tool names) |
| Before/after SEAL to verify no drift | `make reality-deep` |
| F13 constitution integrity check | `make reality-deep` |

For the older stand-alone reality snapshot compiler (deprecated since v2 probe):
→ `references/reality-snapshot-compiler.md`

**When to use:** Arif wants to paste federation context into a cloud AI chat (Gemini, Claude, etc.) — the artifact provides grounded reality without exposing credentials, shell access, or mutation capability.

### Step 0 — Federation Tool Registry (Single Source of Truth)

Before probing individual organs, check `arifos://tools/registry` on the arifOS kernel. This single resource aggregates tools/list from all 6 organs concurrently (5s per-organ timeout) with a 5s TTL cache. Cold read ~0.5s, cached read ~0.037s (14× faster).

```bash
# Read the registry — one call, all organs
curl -sf -X POST http://localhost:8088/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: checkup-$(date +%s)" \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"arifos://tools/registry"}}' | \
  python3 -c "
import sys,json; d=json.load(sys.stdin); t=d['result']['contents'][0]['text']
o=json.loads(t)
s=o['summary']
print(f'Organs: {s[\"organs_healthy\"]}/{s[\"organs_total\"]} healthy')
print(f'Tools: {s[\"tools_total_mcp\"]} MCP-discovered')
print(f'Probe: {s[\"probe_timeout_seconds\"]}s timeout')
for org in o['organs']:
    print(f'  {org[\"organ\"]:12s} :{org[\"port\"]}  {\"🟢\" if org[\"healthy\"] else \"🔴\"}  MCP={org[\"tool_count_mcp\"]}  health={org.get(\"tool_count_health\",\"-\")}')
"
```

**Why first:** The registry is the single source of truth for live organ state. 6/6 healthy → individual `curl :port/health` probes are confirmatory, not diagnostic. Registry shows unhealthy → THEN probe that organ directly.

**Pitfall:** Session-gated organs (GEOX, WEALTH, WELL) return `tool_count_mcp=0` via MCP but report real counts via health endpoints. The registry captures both (`tool_count_health` field) with a `_note` explaining the session gate. Do not flag 0 as failure — check `tool_count_health` for real count.

**Registry source:** `/root/arifOS/arifosmcp/resources/tools_registry.py` — 296 lines, async concurrent probes, 5s TTL in-memory cache.

## Step 1 — Fast Liveness (what's running)

```bash
# Organ liveness
for svc in arifos:8088 aforge:7071 aforge-mcp:7072 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name" || echo "❌ $name"
done

# S24 Sensing Node — check telemetry freshness (JSONL, not live probe)
# Live probe often times out due to Android deep sleep — check the log file instead
echo ""
echo "=== S24 Telemetry ==="
tail -1 /root/arifos-memory/telemetry/s24_history.jsonl 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    ts=d.get('timestamp','?')
    tel=d.get('telemetry',{})
    print(f'  Last: {ts} | Battery: {tel.get(\"battery\",\"?\")}% | Temp: {tel.get(\"temp_c\",\"?\")}°C | Charging: {tel.get(\"charging\",\"?\")}')
except: print('  No telemetry data')
" 2>/dev/null || echo "  ❌ No telemetry file"

# Mesh isolation boundaries (verify DMZ contract)
echo ""
echo "=== Mesh Boundaries ==="
# FLOW → S24 should be BLOCKED
ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no root@100.64.0.4 \
  "curl -sf --connect-timeout 3 http://100.64.0.1:8088/health >/dev/null 2>&1 && echo '  ❌ FLOW→S24: OPEN (breach!)' || echo '  ✅ FLOW→S24: BLOCKED'" 2>/dev/null \
  || echo "  ⚠️ SSH to FLOW failed — can't verify boundary"
# FLOW → FORGE should be BLOCKED
ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no root@100.64.0.4 \
  "curl -sf --connect-timeout 3 http://100.64.0.2:7071/health >/dev/null 2>&1 && echo '  ❌ FLOW→FORGE: OPEN (breach!)' || echo '  ✅ FLOW→FORGE: BLOCKED'" 2>/dev/null \
  || echo "  ⚠️ SSH to FLOW failed — can't verify boundary"

# Telegram bots — THREE distinct bots with distinct roles
# @ASI_arifos_bot  = Hermes (conversation, judgment, memory)
# @arifOS_bot      = 777 FORGE (sovereign execution, seals)
# @AGI_ASI_bot     = OpenClaw AGI (machine ops, search, forge)
for bot in opencode-bot openclaw-gateway; do
  systemctl is-active --quiet $bot 2>/dev/null && echo "✅ $bot" || echo "❌ $bot"
done
# For deep bot diagnostics (multi-source verification, token cross-ref, webhook info):
# → references/telegram-bots-inventory.md
→ `references/telegram-bots-inventory.md`

## Step 1.5 — FQ Pulse Verification (Dual Source Mismatch)

**Why this exists:** This session (2026-07-28) proved that arifFlow live and flow_state.json can disagree by 5× (2.5 BALANCED vs 0.5 WATCHING). Agents reading flow_state.json were HOLDing when they should be forging. This is worse than having no pulse — it's a lying pulse.

**The core problem:** Two sources of truth for the federation's pulse:

| Source | Type | Freshness | Who writes it |
|--------|------|-----------|---------------|
| arifFlow daemon `:7073/health` | Live compute from receipts | Real-time | Rust daemon computes on every `/health` call |
| `/root/AAA/state/flow_state.json` | Static file | Stale (last written by agent) | OpenClaw agent — only during active sessions |

The file is supposed to be refreshed by a cron (`fq-probe.sh`) but that cron was never created or died — no heartbeat check ensures freshness. On restart, flow_state.json falls back to FQ=0.5 WATCHING because no agent is actively writing.

**Probe pattern:**

```bash
# 1. Read arifFlow live
curl -sf http://127.0.0.1:7073/health | python3 -c \
"import json,sys; d=json.load(sys.stdin); fq=d['fq']; \
print(f'arifFlow: FQ={fq[\"quotient\"]} ({fq[\"verdict\"]}) receipts={d[\"receipts\"]}')"

# 2. Read flow_state.json
cat /root/AAA/state/flow_state.json 2>/dev/null | python3 -c \
"import json,sys; d=json.load(sys.stdin); \
print(f'StateFile: FQ={d[\"fq\"]} ({d[\"status\"]}) receipts={d[\"receipt_count\"]}')"

# 3. If they disagree by >0.5 → DUAL SOURCE MISMATCH
# 4. Check who last wrote flow_state.json (check `source` field, compare timestamp)
# 5. Check if the FQ-writer cron actually exists
```

**Triage:**
- arifFlow live shows correct FQ → flow_state.json is stale → **read from arifFlow directly, deprecate flow_state.json**
- arifFlow live shows 0 receipts → daemon just started, not yet populated → **accept flow_state.json as best guess**
- Both show same value → pulse is consistent

**Fix (proven 2026-07-28):** Switch all agents (Hermes, OpenCode, OpenClaw) to read FQ from arifFlow `:7073/health` live instead of `/root/AAA/state/flow_state.json`. The file is an unnecessary intermediary that adds staleness risk. arifFlow daemon already persists receipts to disk (`/var/lib/arifflow/receipts.jsonl`) and recomputes FQ from loaded receipts on restart.

**Reference:** `references/fq-pulse-verification.md` for full diagnosis from 2026-07-28.

## Step 2 — Deep Constitutional Probe

```bash
curl -sf http://localhost:8088/health | python3 -c "
import json,sys
d=json.load(sys.stdin)
rf = d.get('runtime_floors',{})
t = d.get('thermodynamic',{})
print(f'Verdict: {t.get(\"verdict\",\"?\")}')
print(f'Vitality: {t.get(\"vitality_index\",\"?\")}')
print(f'PEACE²: {t.get(\"peace_squared\",\"?\")}')
print(f'Runtime drift: {d.get(\"runtime_drift\",\"?\")}')
print(f'Contract drift: {d.get(\"contract_drift\",\"?\")}')
print(f'Build: {d.get(\"build_commit\",\"?\")} | Live: {d.get(\"live_commit\",\"?\")}')
print()
if rf:
    for k,v in sorted(rf.items()):
        # F7 and F9 are correct by design in LOW range — printed separately below
        if k in ('F7','F9'):
            continue
        mark = '✅' if isinstance(v,(int,float)) and v >= 0.80 else '❌'
        print(f'{mark} {k}: {v}')
    # These two are always fine when low — confirm explicitly
    print(f'✅ F7 (ANTI-BEHAVIOR-SINK): {rf.get(\"F7\",\"?\")} — correct if 0.03-0.05')
    print(f'✅ F9 (ANTI-HANTU): {rf.get(\"F9\",\"?\")} — correct if <0.30 (0.0 = optimal)')
"
```

**NOTE:** Use `/health` endpoint only — it returns `runtime_floors`. The Observatory UI (`/api/status`) uses a different scoring model and may show different values. `/health` is the canonical constitutional probe.

**arifOS MCP requires `Accept: application/json` header.** Without it, `curl` returns empty response even on a healthy server:
```bash
# WRONG — returns empty on arifOS MCP
curl -sf "http://localhost:8088/mcp" ...

# CORRECT — includes Accept header
curl -sf -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",...}' \
  "http://localhost:8088/mcp"
```
This is specific to arifOS MCP port 8088. Other organs (GEOX :8081, WEALTH :18082, etc.) work fine with plain `curl`.

## Step 2.5 — Consolidated Organ Drift Table (Multi-Organ Parallel Probe)

After the deep arifOS probe (Step 2), run a **parallel drift scan across ALL organs** to extract a unified field set (status, drift flag, source/built/deployed commits, tool count, apex scalars). This goes beyond liveness (Step 1) to answer: *which organs are drifting, and on what axis?*

### When to Run

- After any deployment, restart, or organ update
- Before producing a federation health report for Arif
- When the Kernel Contrast Analysis (Step 4 of that pattern) calls for multi-organ drift data
- Whenever you need a single source-of-truth table of all 7 organs' health states

### The Parallel Probe

```bash
# Probe ALL organs in parallel — extracts standardized fields from each /health endpoint
for port_info in "arifOS:8088" "A-FORGE:7071" "AAA:3001" "GEOX:8081" "WEALTH:18082" "WELL:18083" "FLAME:18084"; do
  name="${port_info%%:*}"
  port="${port_info##*:}"
  echo "=== $name ($port) ==="
  curl -sf --max-time 5 "http://localhost:$port/health" 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    status=d.get('status','?')
    dd=d.get('deployment_drift',{}) or d.get('software_release',{}) or {}
    drift=dd.get('drift') if 'drift' in dd else d.get('deployment_drift_status','?')
    src=dd.get('source_commit','?') or d.get('git_version','?') or d.get('commit','?')
    bld=dd.get('built_commit','?') or d.get('build_commit','?')
    dep=dd.get('deployed_commit','?')
    tools=d.get('tools_loaded','?') or d.get('public_tools','?') or d.get('tool_count','?')
    print(f'  Status: {status}')
    print(f'  Drift:  {str(drift)[:8]} | src={str(src)[:12]} built={str(bld)[:12]} dep={str(dep)[:12]}')
    print(f'  Tools:  {tools}')
    owner=d.get('owner_summary',{}) or {}
    if owner.get('color'):
        print(f'  Owner:  {owner[\"color\"]} — {\"; \".join(owner.get(\"reasons\",[]))}')
    apex=d.get('apex_scalars',{}) or {}
    measured=[k for k,v in apex.items() if v and v.get('status')=='MEASURED']
    if measured:
        vals=', '.join([f'{k}={apex[k][\"value\"]}' for k in measured])
        print(f'  Apex:   {vals} MEASURED')
    else:
        print(f'  Apex:   All UNMEASURED')
except Exception as e:
    print(f'  ERROR: {e}')
" 2>/dev/null || echo "  ❌ Unreachable"
  echo ""
done
```

### The Consolidated Table Format

Report the results in this standard table, which provides a single-source-of-truth view of federation drift:

```
| # | Organ      | Port | HTTP | Status      | Drift      | Source     | Built      | Deployed   | Key Notes              |
|---|------------|------|------|-------------|------------|------------|------------|------------|------------------------|
| 1 | arifOS     | 8088 | 200  | healthy     | false      | 1ce09ba    | 1ce09ba    | 1ce09ba    | All aligned            |
| 2 | A-FORGE    | 7071 | 200  | healthy     | false      | 1ceda13    | 1ceda13    | 1ceda13    | Identity UNAVAILABLE   |
| 3 | AAA        | 3001 | 200  | healthy     | false      | 0a697d9    | 0a697d9    | 0a697d9    | Vault CONNECTED        |
| 4 | GEOX       | 8081 | 200  | healthy     | false      | 1ce09ba    | 1ce09ba    | 1ce09ba    | 33/33 tools, HOLD      |
| 5 | WEALTH     | 18082| 200  | healthy     | UNKNOWN    | N/A        | N/A        | N/A        | No git provenance      |
| 6 | WELL       | 18083| 200  | degraded    | UNKNOWN    | 4f20c24    | —          | —          | 11.8h stale, MOCK bio  |
| 7 | FLAME/WIT  | 18084| 200  | warn        | DIVERGENCE | 4f20c24    | —          | —          | 3/4 checks agree       |
```

### Known Common Findings (Checklist)

Check these on every scan — they are frequent patterns:

| Signal | Organ | What to check | If found |
|--------|-------|---------------|----------|
| `git_commit: UNAVAILABLE` | WEALTH (:18082) | **RESOLVED 2026-07-28.** Three root causes: (1) `/root/WEALTH/identity.toml` was a stub (just `# superseded by AAA`) with no `version` field → WEALTH_VERSION="UNAVAILABLE". (2) `_resolve_source_commit()` fallback read `.git_commit` file but only pushed it to `git_commit_fallback`, never promoted to `git_commit`. (3) `.git_commit` file was stale (had `0aba13a`, HEAD was `802942d`). Fix: restore proper identity.toml, patch fallback logic to promote, update `.git_commit` to HEAD. **Restart required after fix.** | See `references/wealth-identity-commit-sourcing-fix-2026-07-28.md` for full diagnostic. |
| `state_age_hours > 4` | WELL (:18083) | Biometric state data stale beyond `stale_after_seconds=14400` | Flag HIGH — needs state refresh |
| `honesty.code: MOCK` | WELL (:18083) | Biometrics are mock/test data, not live sensor input | Flag MEDIUM — replace with real pipeline |
| `consensus.verdict: DIVERGENCE` | FLAME/WITNESS (:18084) | WITNESS checks disagree (N-1 of N off) | Flag MEDIUM — investigate which check diverges |
| `deployment_drift.drift: true` | Any organ | Source != built != deployed | Flag P0 if contradicting `status: healthy` |
| All apex UNMEASURED | WEALTH, A-FORGE, AAA | Organ doesn't probe arifOS for apex scalars | Log as INFO — only arifOS+GEOX report measured apex |
| `identity: UNAVAILABLE` | A-FORGE (:7071) | Identity not initialized | Log as LOW — owner YELLOW |

### Per-Organ Axes

For each organ, check these specific axes:

| Organ | Primary drift axis | Tool surface axis | Apex axis | Authority axis |
|-------|--------------------|--------------------|-----------|----------------|
| arifOS | `deployment_drift_status` + `software_release.drift` | MCP tools count in /health | G, C_dark, QDF MEASURED | SOVEREIGN |
| A-FORGE | `deployment_drift.drift` | `tools_loaded` vs canonical | All UNMEASURED | 777_FORGE (OBSERVE_ONLY) |
| AAA | `deployment_drift` | A2A agents, not MCP tools | All UNMEASURED | F13 ARIF |
| GEOX | `deployment_drift.drift` + `surface_drift.ok` | `tools_loaded` vs `canonical_tools` (33/33) | G, C_dark, QDF MEASURED | HOLD |
| WEALTH | No git info available | 12 loaded vs 8 canonical | All UNMEASURED | ARIF |
| WELL | No deployment_drift field | tool_count | All UNMEASURED | REFLECT_ONLY |
| FLAME/WITNESS | `consensus.verdict` (DIVERGENCE) | source_integrity check | N/A | WITNESS |

### Reference File

For a complete worked example with per-organ detail, action items, and diagnostic commands:
→ `references/organ-drift-table-2026-07-27.md`

## Step 3 — Seal Chain Freshness

```bash
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl
```

## Floor Interpretation Table

| Floor | Pass | Notes |
|---|---|---|
| F1 AMANAH | ≥0.80 | 🔴 True fail if below — check deploy lag + dirty repos |
| F2 TRUTH | ≥0.80 | OBS/DER/INT/SPEC labels |
| F3 WITNESS | ≥0.80 | 🔴 True fail if below — tri-witness gap |
| F4 CLARITY | ≤0 | ✅ -0.0 means ΔS ≤ 0 (negatif = baik) |
| F5 PEACE² | ≥0.80 | System energy |
| F6 MARUAH | ≥0.80 | Dignity checks |
| F7 HUMILITY | 0.03–0.05 | ✅ Correct by design within this range |
| F8 GENIUS | ≥0.80 | Simplest correct path |
| F9 ANTI-HANTU | <0.30 | ✅ Lower = cleaner (0.0 = no hallucination) |
| F10 ONTOLOGY | ≥0.80 | AI-only ontology preserved |
| F11 AUDIT | ≥0.80 | Decision log + actor_signature |
| F12 INJECTION | ≥0.80 | 🔴 True fail if below — check external content flags |
| F13 SOVEREIGN | ≥0.80 | Arif final veto intact |

**Floors that look like failures but are actually fine:**
- F4 -0.0 ✅ (entropy reduction achieved)
- F7 0.04 ✅ (within correct range)
- F9 0.0 ✅ (zero hallucination is optimal)

### FORGE Boot Authority: OBSERVE_ONLY Is Expected

When FORGE `/health` shows `actor_verified=false` and `authority_mode: OBSERVE_ONLY` — **do not flag this as a problem.** It is correct by design.

FORGE is HANDS, not BRAIN. It never self-authorizes. It waits for leases from 888/kernel:

- FORGE has an identity hash (for *lease verification*, not self-auth)
- The sovereign identity chain (Ed25519 key → kernel SOVEREIGN_KEY_IDS → AAA → VAULT999) is the **CALLER'S** chain, not FORGE's
- `actor_verified` becomes TRUE only when a caller presents a valid lease with sovereign signature

**Contrast:** arifOS kernel (`:8088`) shows `actor_verified=true` and `SOVEREIGN` authority when bound. FORGE showing `OBSERVE_ONLY` means the brain/hands separation is working.

## Flag Hierarchy for Human Reports

Always report in this priority order:

1. **🔴 True failures** — floors genuinely failing, real risk, needs sovereign decision
2. **🟡 Items to watch** — deploy lag, dirty repos, stale data, amber state
3. **✅ Normal** — all green

## Kernel Contrast Analysis — Before vs Now Pattern

When Arif asks "what changed?" or "explain the contrast" about the kernel or any organ — **don't just list features.** Use this structured synthesis pattern.

This is NOT a drill-down diagnostic (use Contract Entropy Audit for that). This is a **human-language explanation** of what capabilities shifted and why.

### When to Use

- Arif asks "how is the kernel different now?" / "explain in human language"
- After a major release or ZEN migration
- When a release name signals a philosophical shift (e.g., `ZEN-SURVIVAL`)
- After deploy/merge-conflict/repair cycles
- Before SEAL: needs to confirm the gap between prior and current state

### The Pattern (6 Steps)

**Step 1 — Identify the release boundary.** Extract version/release name from `:8088/health`. Name IS the story (e.g., `ZEN-SURVIVAL` implies pruning, hardening, survival-of-the-fittest).

**Step 2 — Git log scan.** Read `git log --oneline -20` for the organ. Classify each commit into categories:

| Category | Example |
|----------|---------|
| Merge conflict fixes | `fix(docs): resolve merge conflicts` |
| APEX ratification | `feat(apex): APEX T-000/T-001 canon` |
| Shadow probe / INIT wiring | `fix(kernel): deploy shadow probe into arif_init` |
| Reality ledger hooks | `[FORGE] Z5b — reality ledger auto-hooks` |
| Tool/feature kill | `quarantine(apex): move X out of kernel path` |
| Security repair | `[REPAIR] sync kernel ABI surface` |
| Cosmetic/schema align | `chore: Z2 — pointerize organ.yaml` |

**Step 3 — Critical modules inventory.** Extract `critical_module_hashes` from `:8088/health`. This is the live list of what survived. Compare against prior list (from session history or a prior seal artifact) to find what was added/removed.

**Step 4 — Multi-organ drift scan.** Check EVERY organ for deployment drift (source_commit == deployed_commit). Flag any that say "healthy" but have `drift=true` — this is a CONTRADICTION per the kernel's own invariant rule.

**Step 5 — Contradiction detection.** Find all places where declared state ≠ observed state:

| Declaration | Observation | Contradiction |
|-------------|-------------|---------------|
| `drift: true` + `status: healthy` | Invariant says refuse healthy on drift | ❌ Self-contradiction |
| `actor_verified: false` as bug | Correct for anonymous sessions | ⚠️ False alarm |
| F1-F12 pass but verdict=HOLD | May be honest self-HOLD | Depends on reason |

**Step 6 — Human-language synthesis.** Structure as tables:

```
## ⚡ Before — What Kernel TAK BOLEH Buat Sebelum Ni
## ⚡ Now — What Kernel BOLEH Buat Sekarang
## 🌪️ Chaos — Kontradiksi Yang Kena Hapus
## 🏆 Survival of the Fittest Tools
```

### Pitfalls

- **`healthy + drift=true` is the #1 contradiction.** The kernel's own invariant says "must refuse to report healthy when drift is true." If both appear, the system is in a known-contradictory state.
- **Don't conflate cosmetic drift (build_info.py stale hash) with real drift.** `build_info.py` has a hardcoded BUILD_COMMIT never updated — cosmetic only. Real drift = `built_commit ≠ deployed_commit`.
- **Release name IS metadata.** Read `ZEN-SURVIVAL`, not just `v2026.07.24`.
- **HOLD ≠ broken.** A kernel reporting HOLD with healthy status is honest self-assessment.
- **Drift on ONE organ ≠ federation failure.** Per-organ reporting, not boolean aggregate.

### Example Output

See `references/kernel-contrast-2026-07-27.md` for a complete worked example from the ZEN-SURVIVAL release.

## Web Surface Audit Pattern — AAA / arifOS / WEALTH / WELL Sites

When Arif asks to audit, upgrade, or report on the web estate (arif-fazil.com, aaa.arif-fazil.com, arifos.arif-fazil.com, organ subdomains), follow this discipline strictly.

### The Iron Rule: Crawl Before Propose

**Never assume prior session state.** The content of any web surface may have changed since the last session. Always probe live before writing any gap analysis, change proposal, or verdict.

**Wrong pattern (do not do):**
1. Recall what the site "looked like" from memory
2. Propose changes based on that recollection
3. Report findings

**Correct pattern:**
1. `web_extract` all target surfaces simultaneously
2. `grep` source files on the VPS for specific legacy/incorrect content
3. Synthesize gap analysis from live data
4. Then — and only then — propose changes

### Two-Layer Contract

Every web surface serves two audiences. Every audit report must verify both:

| Layer | Surface | What it contains | Language |
|---|---|---|---|
| **Human** | arif-fazil.com | Portfolio, identity, essays, federation overview | Plain BM/English, no jargon, no mythology |
| **Agent** | Observatory, AAA, .well-known/, llms.txt | Machine-readable topology, MCP endpoints, agent cards | Precise, governed, no theater |

A site fails the two-layer contract if the human layer has jargon theater (ΔΩΨ, APEX, GÖDEL) or the agent layer has plain English where machine precision is required.

### AAA Legacy Forensics Pattern

APEX/legacy residue typically lives in 7 files. Always grep all simultaneously:

```bash
grep -rn "APEX\|apex\|3002\|deliberation" /var/www/html/aaa/ 2>/dev/null | grep -v ".map:"
```

Common APEX residue locations:
- `/var/www/html/aaa/index.html` — title, headings
- `/var/www/html/aaa/llms.txt` — full APEX THEORY section (~72 lines)
- `/var/www/html/aaa/.well-known/arifos.json` — `APEX_Soul` engine entry, `THEORY` trinity_site
- `/var/www/html/aaa/manifest.json` — `arif-fazil.com/apex/` related_application
- `/var/www/html/aaa/docs/ARCHITECTURE.md` — ΔΩΨ ring architecture
- `/var/www/html/aaa/agents/index.html` — APEX legacy agent row
- `/var/www/html/aaa/assets/*.js` — minified APEX references (grep only, do not edit)

### Deliberation Report Format (000 → 999)

When the task requires a `000→999 deliberation → F13 ratification → execute` cycle, produce this exact structure:

```
# [Task Name] — Structured Report & Change Proposal
Plan ID: PLAN-XXX
Auditor: Hermes (333-AGI)
Mode: Auditor-Architect | Awaiting F13 Ratification

## Section 1: Fresh Crawl — Current State
HTTP surface audit table + content diagnosis table (requirement vs gap severity)

## Section 2: Proposed Changes
Change table: Site | File | Change Type | Severity | Before/After or exact diff

## Section 3: Summary Change Table
One-line per file changed, sorted by severity

## Section 4: Post-Audit Federation Score Projection
Per-surface score + overall federation score

## Section 5: Proposed VAULT999 Seal Text
Exact candidate verbatim text for seq=N+1

## Section 6: Boundary & Risk Assessment
Destructiveness | Reversibility | Scope | F13 surface touch | Seal required

## Awaiting F13 Ratification
Reply format options: F13 ACK / F13 ACK — Partial / HOLD
```

### Tool Count Verification Pattern

When auditing MCP tool counts in the Observatory or AAA organ table, verify against live organs.

**Three verification methods (in order of reliability):**

1. **MCP tool via Hermes** — Most reliable. Call the organ's own status tool:
   ```python
   # GEOX — use geox_surface_status for full registry (public + internal + phantom)
   mcp__geox__geox_surface_status(mode="registry")
   # Returns: canonical_callable (public), internal_tools, phantom_tools, registry_truth
   ```

2. **JSON-RPC POST /mcp** — Standard MCP protocol. Varies by organ (see transport dialect below):
   ```bash
   curl -sf -X POST http://127.0.0.1:<PORT>/mcp \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' | \
     python3 -c "import sys,json; d=json.load(sys.stdin); tools=d.get('result',{}).get('tools',[]); [print(f'  {t[\"name\"]}') for t in tools]; print(f'TOTAL: {len(tools)}')"
   ```

3. **HTTP GET /tools** — Simplest but may return different counts than JSON-RPC (middleware filtering).

**Per-organ verification (verified 2026-07-16):**

| Organ | Port | JSON-RPC works? | Notes |
|---|---|---|---|
| arifOS | 8088 | ✅ with `Accept: application/json` | Returns empty without Accept header |
| A-FORGE | 7072 | ✅ | 109 tools via JSON-RPC |
| GEOX | 8081 | ❌ (SSE mode, needs session init) | Use `geox_surface_status` MCP tool instead (15 public, 54 internal, 69 total) |
| WEALTH | 18082 | ✅ with `initialize` handshake first | 12 tools |
| WELL | 18083 | ✅ raw POST works | 27 tools |
| MIND | 51001 | ❌ no MCP tools exposed | Running but zero tool surface (cognitive organ) |

**MIND port note (2026-07-16):** MIND runs on port 51001, NOT 3003. The 3003 reference in AGENTS.md is stale. Verify with `ss -tlnp | grep <mind-pid>`. MIND is a cognitive intelligence organ (Stage 333s) that exposes a /health endpoint but no MCP tools.

Update the static Observatory table to match live counts. Stale tool counts in the UI are a federation integrity failure.

### MCP Apps Discovery Surface — GEOX / arifOS

MCP Apps (interactive HTML surfaces rendered inside chat) require their own discovery layer. Always probe these manifests when auditing an organ:

```bash
# MCP Apps manifests
for organ in geox arifOS; do
  domain="${organ}.arif-fazil.com"
  echo "=== $organ MCP Apps ==="
  curl -sf "https://$domain/apps.json" -o /dev/null -w "  apps.json: HTTP %{http_code}\n" 2>/dev/null
  curl -sf "https://$domain/.well-known/agent.json" -o /dev/null -w "  agent.json: HTTP %{http_code}\n" 2>/dev/null
  curl -sf "https://$domain/tools.json" -o /dev/null -w "  tools.json: HTTP %{http_code}\n" 2>/dev/null
done

# Source vs web root divergence check (critical!)
# Always compare /root/<organ>/apps.json with /var/www/html/<organ>/apps.json
# Source repo is authoritative; web root may be stale
for organ in geox; do
  SRC="/root/$organ/apps.json"
  DST="/var/www/html/$organ/apps.json"
  if [ -f "$SRC" ] && [ -f "$DST" ]; then
    echo "=== $organ apps.json divergence ==="
    python3 -c "
import json, sys
src = json.load(open('$SRC'))
dst = json.load(open('$DST'))
src_ids = {a['id'] for a in src.get('apps',[])}
dst_ids = {a['id'] for a in dst.get('apps',[])}
print(f'  Source: {len(src_ids)} apps | Web root: {len(dst_ids)} apps')
if src_ids != dst_ids:
    print(f'  DIVERGENT — Missing from web: {src_ids - dst_ids}')
    print(f'  In web only (stale): {dst_ids - src_ids}')
else:
    print('  In sync ✅')
"
  fi
done
```

**Key finding (2026-07-11):** `/root/geox/apps.json` (6 apps, `ui_resource` fields, MCP Apps protocol) ≠ `/var/www/html/geox/apps.json` (4 apps, no `ui_resource`, older schema). Source was authoritative. Deployed source → web root. **Always compare both before proposing changes.**

### Post-v2 Federation Score Reference

| Surface | v1 Score | Target Change | v2 Projected |
|---|---|---|---|
| arif-fazil.com | Strong | No change | Strong |
| arifos.arif-fazil.com | Strongest | No change | Strongest |
| AAA | Weakest (~60) | +35 | Strong (~95) |
| Overall | 78 | +10 | ~88–90 |

AAA moves from weakest to first-tier when: legacy cleared (APEX/3002 removed), agent registry live, SEAL viewer added, sovereignty banner added, readiness dashboard added, A-FORGE card added.

## OpenCode Session Monitoring

When Arif says "manage the opencode session" or asks about running tasks:

```bash
# Find active OpenCode process
ps aux | grep opencode | grep -v grep

# Check what it's doing — session log
tail -100 /root/.local/share/opencode/log/opencode.log | grep "message="

# Get session ID from log
grep "session.id=ses_" /root/.local/share/opencode/log/opencode.log | tail -3
```

OpenCode attached to a pts/N means it's in an interactive session. **Don't interfere unless Arif asks.** Monitor and report.

## Per-Floor Root Cause Quick Reference

| Symptom | Likely Floor | Likely Fix |
|---|---|---|
| Deploy lag (live ≠ repo HEAD) | F1 AMANAH | Redeploy sync |
| Dirty repos > 0 | F1 AMANAH | Commit or stash → run `federation-git-zen` pipeline |
| F1 < 0.80 but deploy clean | F1 AMANAH | Constitutional scoring gap — check law_audit.py backup detection syntax bug + SovereignGate hardcoded list divergence |
| F12 < 0.80 | F12 INJECTION | Check tool_01_init_anchor.py _injection_score formula — score 0.425 caused by 10-pattern allowlist + formula that drops below 0.85 with 6 hits |
| AI witness < 1.0 | F3 WITNESS | Strengthen AI channel in session |
| External content flags | F12 INJECTION | Audit observatory scraping sources |
| Vitality < 0.60 | System energy | Fix F1 + F3 likely settles this |
| Unknowns not declared | F7 HUMILITY | Agent must explicitly state what it does not know |
| Hallucination risk | F9 ANTI-HANTU | Check evidence grounding — should be ~0 when clean |

## Port 3001 Auth Bypass — L10 Boundary

**CRITICAL: Port 3001 returns 200 without auth token.**

```
curl http://localhost:3001/              → 200 ❌
curl -H "x-arifos-token: fake" :3001/  → 200 ❌
```

The `auth: required` field in the JSON response is a lie — no middleware enforces it.
Only `curl` proves it. The browser/UI shows the field, not the enforcement.

**Root cause:** `membrane_middleware.js` validates `_membrane` envelope structure but never checks `x-arifos-token`.

**Fix:** Inject Express middleware in `a2a-server/server.js` requiring valid token header.
This is an L10 boundary collapse, not F1 drift.

## E1 Pre-Execution Gate — SEAL Scope Gap (Critical Architecture)

**The gap:** `arif_verify` foundation EXISTS in `A2ASealVerifier` (`seal_verifier.py`) with Ed25519/HMAC signature verification. But vault's `input_hash` is SHA256 of the MCP call params (JSON-RPC payload), NOT the shell command string.

**Consequence:** SEAL token verified as kernel-minted, but scope is wrong. Token could be valid for `{ command: "rm -rf /tmp/test" }` (vault: `SHA256(params)`) while actual shell command is `"rm -rf /root/VAULT999"` (A-FORGE computes: `SHA256("rm -rf /root/VAULT999")`). These are different hashes → scope verification always fails.

**Two-part fix required at SEAL issuance (JITU):**
```python
# arif_judge issues SEAL with BOTH hashes:
{
  "token": "SEAL-888-xxxx",
  "payload_hash": "sha256:abc...",   # Hash of MCP call params (current field)
  "command_hash": "sha256:def...",   # Hash of shell command string (NEW — missing)
  ...
}
```

**arif_verify tool spec (add to tools.py):**
```python
@arthur_mcp.tool()
def arif_verify(token: str, command: str, expected_hash: str) -> dict:
    # 1. TOKEN_VALID — uses existing verify_sovereign_signature()
    # 2. SCOPE_VALID — expected_hash == vault[token].command_hash
    # 3. REPLAY_SAFE — token not consumed (atomic mark-used)
    # Falls back to payload_hash for legacy tokens (no command_hash field)
```

**Legacy token handling:** Tokens issued before `command_hash` migration don't have the field. `arif_verify` must handle gracefully — fall back to `payload_hash` comparison.

**Atomic replay prevention:** Token consumption must be atomic. Optimistic locking (check → mark → verify → rollback on fail) is acceptable for localhost (no concurrent forge_execute from multiple processes). Simpler than full vault write-lock.

### CIV-33 Checkup (2026-07-13+)

When checking federation health, include these additional probes:

```bash
# A2A gateway status
echo "=== A2A Gateway ==="
systemctl is-active aaa-a2a.service
curl -s http://localhost:3001/.well-known/agent-card.json | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Gateway: {d[\"name\"]} | proto: {d[\"protocolVersion\"]} | skills: {len(d[\"skills\"])} | signed: {bool(d.get(\"signatures\"))}' 2>/dev/null
"

# Agent registry count
curl -s http://localhost:3001/a2a/discover -H 'A2A-Version: 1.0' -H 'x-arifos-token: x' 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Registry: {d.get(\"count\",0)} agents' 2>/dev/null
"

# Knowledge atlas integrity
python3 -c "
import json, glob
profiles = glob.glob('/root/AAA/knowledge/**/*.json', recursive=True)
print(f'Knowledge atlas: {len(profiles)} files')
manifest = json.load(open('/root/AAA/knowledge/manifest.json'))
print(f'Manifest profile count: {len(manifest.get(\"profiles\",[]))}' 2>/dev/null
"

# META-MESA seal status
python3 -c "
import json
seal = json.load(open('/root/AAA/agent-cards/META_MESA_SEAL.json'))
print(f'META-MESA: {seal.get(\"status\",\"sealed\")} | hash: {seal.get(\"seal_hash\",\"?\")[:20]}...' 2>/dev/null || echo 'No META-MESA seal'
"
```

**Health interpretation:**
- Gateway active + 27+ cards + all signed = A2A layer healthy
- Knowledge atlas intact = reasoning layer healthy
- META-MESA sealed = recursive improvement loop active

**Model changes to `opencode.json` top-level `model` field NEVER take effect if any `agent.{forge,auditor,ops,planner}.model` override exists.**

The hierarchy is:
1. `agent.{role}.model` — HIGHEST PRIORITY (always wins, even if blank/null)
2. `opencode.json` top-level `model` field
3. `--model` CLI flag
4. `model.json` state file (recent/favorite)

**Working model (no API key):** `opencode-go/deepseek-v4-flash-free`
**Always-broken models (require external keys):** `deepseek/deepseek-v4-pro`, `minimax/MiniMax-M3`
**Previously-working, now-exhausted:** `tokenplan-mimo/mimo-v2.5-pro`

To change model reliably — must update BOTH:
```json
// /root/.config/opencode/opencode.json
{ "model": "opencode-go/deepseek-v4-flash-free", "small_model": "opencode-go/big-pickle" }
// AND in the same file's agent{} overrides:
"agent": {
  "forge":   { "model": "opencode-go/deepseek-v4-flash-free" },
  "auditor": { "model": "opencode-go/deepseek-v4-flash-free" },
  "ops":     { "model": "opencode-go/deepseek-v4-flash-free" },
  "planner": { "model": "opencode-go/deepseek-v4-flash-free" }
}
```

Also update `/root/.local/state/opencode/model.json` — add `deepseek-v4-flash-free` as top `recent` and `favorite`.

After changing: `pkill -f "opencode serve"; opencode serve --hostname 127.0.0.1 --port 4096 &`

Full command probe: `timeout 20 opencode run "model name" 2>&1 | head -5`
Expected: `> forge · deepseek-v4-flash-free`

Real floor score values from a healthy-but-imperfect kernel are captured in:
→ `references/live-floor-benchmarks.md`

OpenCode model benchmarks (working/broken models, priority chain) are captured in:
→ `references/opencode-model-benchmarks.md`

Empirical evidence on structural governance limits (Governed MCP F1 collapse, forgeExecute bypass, ZioSec workspace injection) is captured in:
→ `references/structural-governance-empirical.md`

This file is the ground truth for what "real" looks like — including the difference between constitutional scoring gaps (F1=0.5, F12=0.425) and true runtime failures. **Read it before interpreting any floor score.**

**Web deploy traps for AAA / arifOS / arif-fazil.com:**
`→ references/web-deploy-traps.md`
`→ references/web-surface-fossils.md`

Covers: correct Caddy webroot (`/var/www/html/aaa/` not `/var/www/aaa.arif-fazil.com/`), React SPA `web_extract` noscript trap, Vite `public/` → `dist/` stale file copy pattern, Caddy reload, and the canonical deploy sequence.

## NEW 2026-07-10: Purpose-First Rule (from AAA v2 redesign session)

**Arif asked "So what?? What does it even mean??"** — the verbose feature-list proposal was rejected because it led with components, not purpose.

**The rule:** Every proposal, redesign, or change plan must lead with one plain-language sentence answering "what does this DO for Arif?" before any component list.

**Wrong:**
```
# Proposed Changes
1. HERMES IS AGENT banner at top of AAA
2. Recent Agent Activity block
3. Federation Health strip (6 organs)
4. Last 5 VAULT999 entries table
```

**Right:**
```
**What:** A control panel where Arif can glance and instantly know what agents did, what needs his OK, and what's healthy or broken.

Components:
1. HERMES IS AGENT banner...
```

The "what does it even mean??" rejection is a **first-class skill signal.** When Arif asks this, the skill that failed is the one that produced the feature-list without purpose-first. Update that skill's output format.

## NEW 2026-07-10: Sovereign Execution Signals

**Rule:** Certain phrases from Arif ARE sovereign execution signals. When these arrive, stop asking for confirmation. Execute immediately.

| Signal | Meaning | Action |
|---|---|---|
| `"Go"` / `"Execute v2"` / `"Execute v2 + secondary"` | Explicit F13 ratification | Execute now, no confirmation loop |
| `"F13 ACK"` | Sovereign has ratified | Proceed to execution |
| `"F13 ACK + Execute X"` | Ratified + execution order | Execute X immediately |
| `"buat ja la"` | Do it now | Execute immediately |
| `"Yes confirm"` | Explicit confirmation | Execute |
| `"execute X"` | Direct execution order | Execute X immediately |
| `"I'm the Architect"` | Sovereign override | Execute as instructed |

**What NEVER counts as execution signals:**
- Questions ("can you do X?") — still need confirmation
- "What about Y?" — clarification, not ratification
- Silence — never assume

**The anti-pattern to avoid:** Asking "should I proceed?" after Arif has already said "go." This is a confirmation loop violation. When a sovereign signal fires, the agent's job is to execute and report, not to verify that the sovereign meant what they said.

**Interaction with 888_HOLD:** Even sovereign execution signals do not override 888_HOLD on genuinely irreversible actions (VAULT999 seals, secret rotations, `rm -rf` on unknown scope). The sovereign signal means "I have decided" — the kernel still enforces floors.

## NEW 2026-07-11: Federation Sweep-and-Classify Pattern

When Arif says "sweep the federation," "find everything pending/stale/orphaned," or "clean up," run this systematic inventory.

### Step 1 — Organ Liveness (same as Step 1 above)

### Step 2 — Cron Job Inventory

```bash
# List all cron jobs, classify by state
hermes cron list 2>/dev/null
# For each job: enabled? paused? last_run? last_status?
# Paired with reason — paused jobs with "moved-to-system-cron" are intentional, not stale
```

**Classification:**
- **ACTIVE + RUNNING** → production, leave alone
- **PAUSED + documented reason** → intentional, leave alone
- **PAUSED + no reason** → investigate, may need kill
- **ENABLED + never run** → orphaned, kill or fix

### Step 3 — forge_work Sweep

```bash
# Age-rank all files
find /root/A-FORGE/forge_work/ -maxdepth 2 -name "*.md" -o -name "*.json" | while read f; do
  age=$(( ($(date +%s) - $(stat -c %Y "$f")) / 86400 ))
  echo "${age}d $(basename "$f")"
done | sort -rn
```

**Classification:**
- **0-1 days** → active work, check if completed or still pending
- **2-7 days** → likely completed, check carry-forward for open items
- **7+ days** → archive candidates, check if sealed in VAULT999

### Step 4 — Carry-Forward Check

```bash
cat /root/.local/share/arifos/carry_forward.json | python3 -m json.tool
# Check: identity_drift, next_safe_action, active_scars, recent_seals
```

**Key fields:**
- `identity_drift: PASS` → no identity issues
- `next_safe_action: PROCEED_OR_SABAR` → clear to proceed
- `active_scars.count > 0` → check if scars need resolution
- `recent_seals: []` → no recent seals (may indicate stale carry-forward)

### Step 5 — TODO / Session State

```bash
# Current TODOs
hermes todo 2>/dev/null
# Recent sessions
hermes sessions list 2>/dev/null | head -20
```

### Step 6 — Skills Audit

```bash
# Find skills with DRAFT/WIP/TODO/PENDING markers
grep -rl 'DRAFT\\|WIP\\|TODO\\|PENDING' ~/.hermes/skills/*/SKILL.md 2>/dev/null
# Check for orphaned skills (no matching trigger in any conversation)
```

### Step 6b — Sister-Workspace Clone Sweep

OpenClaw spawns sister workspaces (`workspace-opencode`, `workspace-codex`, `workspace-kimi`) that inherit template artifacts. These accumulate identical orphan files. Check for them:

```bash
# Known zombie artifact: DREAMS.md = empty "memory trace unavailable" stubs from broken OpenClaw dreaming subsystem (subsystem never wired; timer pending since Jun 7)
find /root/.openclaw -name "DREAMS.md" -not -path "*/.archive/*" -not -path "*/_quarantine/*" 2>/dev/null

# Stale cron-receipts >7 days
find /root/.openclaw/workspace/cron-receipts/ -name "*.json" -mtime +7 2>/dev/null | head -20

# General template-propagated orphan detector
for dir in /root/.openclaw/workspace-opencode /root/.openclaw/workspace-codex /root/.openclaw/workspace-kimi; do
  [ -d "$dir" ] && echo "=== $(basename $dir) ===" && ls "$dir"/*.md 2>/dev/null
done
```

**Classification:**
- **Known zombie** (DREAMS.md) → archive to `.archive/DREAMS-WORKSPACE.md`, safe to remove
- **Stale operational logs** (>7 days) → consolidate into archive subdir
- **Unique content** (varies across workspaces) → investigate before action

**Real Dream Engine (DREAMS.md replacement):**
- Substrate code: `/root/.openclaw/workspace/dream_engine/` (v0.1, timer never activated)
- Federation skill: `/root/AAA/skills/AGI-dream-engine/SKILL.md` (Phase 0-3 roadmap)

### Step 7 — Systemd / Process Health

```bash
# Failed units
systemctl list-units --state=failed | grep -E 'hermes|arif|forge|claw|geox|wealth|well|aaa'
# Orphaned processes
ps aux | grep -E 'hermes|arif|forge|claw|geox|wealth|well' | grep -v grep
# Stale tmux sessions
tmux list-sessions 2>/dev/null
```

### Step 8 — Registry Drift Convergence

When the drift scanner reports DRIFT between canonical and mirror tool manifests:

```bash
bash /root/HERMES/scripts/registry-drift-scanner.sh
```

**SYMLINK_OK = clean.** If you see DRIFT (hash mismatch between canonical and mirror):

```bash
# Canonical is /root/AAA/docs/TOOLREGISTRY.json
# Mirrors should be symlinks to it:
rm /root/arifOS/TOOL_MANIFEST.json
rm /root/AAA/registries/TOOL_MANIFEST.json
ln -s /root/AAA/docs/TOOLREGISTRY.json /root/arifOS/TOOL_MANIFEST.json
ln -s /root/AAA/docs/TOOLREGISTRY.json /root/AAA/registries/TOOL_MANIFEST.json

# Re-scan
bash /root/HERMES/scripts/registry-drift-scanner.sh
```

The scanner checks: symlink pointing to canonical → `SYMLINK_OK`. File with different hash → `DRIFT`. Symlinks are clean, auto-propagating, and preferred for these documentation mirrors.

### Classification Matrix

| Category | Action | Example |
|---|---|---|
| **PRODUCTION** | Leave alone | Active cron, running organs, current config |
| **COMPLETED + SEALED** | Archive | forge_work receipts, VAULT999-sealed items |
| **OPEN WORK** | Prioritize | carry-forward items with clear next steps |
| **DIRTY REPOS** | Git Zen → `federation-git-zen` | Run the multi-repo cleanup pipeline to test/stage/commit/push |
| **STALE + NAMED ANOMALY** | Track, don't touch | WELL biometrics, VAULT999 chain gaps |
| **ORPHANED** | Kill | Paused cron with no reason, never-run jobs |
| **DRAFT** | Ship or kill | Skills with DRAFT markers, unfinished specs |
| **AGENTS.md DRIFT** | Propagate | `references/governance-pointer-propagation.md` — inject/update cross-cutting governance pointers in all organ and harness AGENTS.md files |

### Output Format

```
FEDERATION SWEEP — YYYY-MM-DD

X/Y organs green. Z seals in chain. identity_drift: PASS/FAIL.

PRODUCTION (leave alone):
├─ [list]

OPEN WORK (prioritize):
├─ [list with priority ranking]

STALE BUT SEALED (archive):
├─ [list]

ORPHANED (kill):
├─ [list]

VERDICT: [one-sentence summary]
```

## Contract Entropy Audit (Deep Federation Audit)

When a surface-level health check isn't enough — when Arif asks "is the federation consistent?" or "do declared contracts match reality?" — run this deep audit pattern. Goes beyond liveness to verify the **7-layer contract invariant**:

```
declared = implemented = deployed = registered = exported = callable = auditable
```

### When to Use

- Arif asks for "federation repair," "contract audit," "consistency check," or "is everything aligned?"
- After major deployments or multi-organ changes
- When health checks pass but something feels wrong
- When seal chain shows anomalies (kernel_verdict=UNKNOWN, invariants_downgraded)

### The Probe Sequence

For EACH organ, collect these surfaces simultaneously:

```bash
# 1. Health (liveness + metadata)
curl -sf http://127.0.0.1:<PORT>/health | python3 -m json.tool

# 2. Tool surface via HTTP GET /tools
curl -sf http://127.0.0.1:<PORT>/tools | python3 -c "
import sys,json; d=json.load(sys.stdin)
tools = d if isinstance(d,list) else d.get('tools',[])
for t in tools: print(f'  {t.get(\"name\",\"?\") if isinstance(t,dict) else t}')
print(f'TOTAL: {len(tools)}')"

# 3. Tool surface via JSON-RPC POST /mcp
curl -sf -X POST http://127.0.0.1:<PORT>/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); tools=d.get('result',{}).get('tools',[]); [print(f'  {t[\"name\"]}') for t in tools]; print(f'TOTAL: {len(tools)}')"

# 4. .well-known manifest (if exists)
curl -sf http://127.0.0.1:<PORT>/.well-known/mcp/server.json | python3 -m json.tool

# 5. Git state
cd /root/<REPO> && git log --oneline -3 && git branch --show-current && git status --short | head -10
```

### Cross-Validation Matrix

Build a table comparing all surfaces per organ:

| Organ | /health | /tools | JSON-RPC | .well-known | Registry | AGENTS.md | Branch | Dirty |
|-------|---------|--------|----------|-------------|----------|-----------|--------|-------|

**Every column should agree.** When they don't, you have contract entropy.

### Common Discrepancy Classes

| Pattern | Meaning | Severity |
|---------|---------|----------|
| /tools = N, JSON-RPC = 0 (raw) | **May be handshake required, not broken.** Test with Accept header (arifOS), initialize call (WEALTH), or session init (GEOX). Only P0 if handshake also fails. | P0/P1 |
| /tools = N, JSON-RPC = 0 (with handshake) | Transport genuinely broken — GET works but MCP protocol doesn't | P0 |
| .well-known = M, /tools = N (M>N) | Manifest lies — declares tools not callable | P1 |
| .well-known = M, /tools = N (M<N) | Internal tools exposed in manifest | P1 |
| Registry = R, /tools = N (R>>N) | Phantom tools in registry | P1 |
| AGENTS.md = A, /tools = N (A≠N) | Documentation drift | P2 |
| Git branch ≠ main | Deployment from feature branch | P1 |
| Dirty files > 0 | Uncommitted changes in deployed code | P2 |
| kernel_verdict = UNKNOWN | Seal chain head invalid | P0 |

### Output Format

```
FEDERATION CONTRACT AUDIT — YYYY-MM-DD

REALITY VERDICT: <one sentence>

PER-ORGAN MATRIX:
| Organ | /tools | JSON-RPC | .well-known | Registry | Branch | Dirty | Verdict |

SEAL CHAIN: <seq, kernel_verdict, witness>

HUMAN DECISIONS NEEDED:
<items requiring Arif's authority>

RECOMMENDED ACTIONS:
<reversible fixes>
```

FORGE duty-pulse interpretation (drift scanner, constitutional sync, vitality pulse):\n→ `references/forge-duty-pulse-interpretation.md`

Full transport state findings from 2026-07-14:
→ `references/federation-transport-state.md`

Observatory dual-engine architecture + organ probe hostname fix (2026-07-18):
→ `references/observatory-dual-engine.md`

### Domain Orthogonality Audit Sub-pattern

When the deep audit needs to go beyond "are organs alive and consistent?" into **"do their domain boundaries actually overlap?"** — run the domain orthogonality protocol.

**When to use:** Federation-wide structural audit, before adding new tools to an organ, after refactoring an organ's tool surface, or when cross-organ data flows look suspicious.

**The core question:** Does every tool belong to exactly one organ, or are there capability overlaps disguised as shared boundaries?

**The 6-step protocol:**
1. **Collect self-declared boundaries** — read each organ's AGENTS.md `## Boundary` section. Every organ should say what it does AND what it never does.
2. **Map the complete tool surface** — from three sources (live MCP tools/list, manifest YAML, source code) to catch ghost tools, phantom exports, and session-gated tools.
3. **Classify by concern axis** — map every tool to its organ's domain prefix (`geox_*`, `capital_*`, `well_*`, `arif_*`, `forge_*`). No tool should have the wrong prefix.
4. **Check naming collisions** — search for the same tool name across organs. Zero is expected.
5. **Verify cross-organ bridges** — intentional bridges (like `geox_to_wealth_bridge`) are data transforms, not duplicates. Verify they call the target organ instead of re-implementing it.
6. **Verify NOT-boundaries against reality** — every "❌ Never" must be verifiable. GEOX must not have capital tools. WEALTH must not issue verdicts. WELL must not diagnose.

**3-axis classification prevents false positives:** For any domain that appears in two organs, ask *What* (domain), *How* (mode: observe/compute/reflect/bridge), and *Why* (purpose). Same What + same How + same Why = TRUE OVERLAP. Same What only = adjaceny.

Full protocol with exact commands, classification matrix, and worked example:
→ `references/domain-orthogonality-audit.md`

## Cage Audit (Deep Constitutional Stress Test)

When the checkup goes beyond "are organs alive?" into "can the constitution actually constrain the sovereign's future self?" — run the cage audit pattern. Covers identity verification (Ed25519), cooling ledger persistence, airlock error rates, VAULT999 integrity, runtime drift, and floor enforcement depth.

→ `references/cage-audit-constitutional-stress-test.md`

## Constitutional Source Drift Audit — FLOOR_TABLE Consumer Checks

When the canonical **FLOOR_TABLE.json** (`/root/arifOS/GENESIS/FLOOR_TABLE.json`) exists and you need to verify that all registered consumers are faithfully rendering their assigned floors, names, operators, and rules — run this protocol.

### When to Run

- **Fasa 1 audit request** — explicit "FLOOR_TABLE consumer drift check + seal status audit"
- After FLOOR_TABLE.json is updated or re-forged
- When Arif asks "are the consumers synced?" or "check floor drift"
- During federation-wide governance audit
- Before any seal or deploy that touches floor definitions

### Step 1 — Read the Canonical Source

```bash
cat /root/arifOS/GENESIS/FLOOR_TABLE.json | python3 -m json.tool
```

Extract:
- **version, forged date, authority** — metadata
- **All 13 floors** — id, name, rule, operator, sealed_range
- **F2 band mapping** — OBS→CLAIM, DER→PLAUSIBLE, INT→ESTIMATE, SPEC→UNKNOWN
- **F7 canonical form** — Ω₀ ∈ [0.03, 0.05], confidence cap [0.95, 0.97], deprecated strings (0.90, STEWARDSHIP, HARAM)
- **F6 bridge** — MARUAH (operational) / EMPATHY (public)
- **Consumers array** — each consumer's name, path, and `must` contract

### Step 2 — Audit Each Consumer Simultaneously

For every consumer in `floors.consumers[]`, read its target file and check:

| Check | What to Verify |
|-------|----------------|
| File reachable | File exists at declared path |
| F7 name | Must be HUMILITY, never STEWARDSHIP |
| F7 operator | Must cite Ω₀, never 0.90 cap |
| F2 band names | Must use CLAIM/PLAUSIBLE/ESTIMATE/UNKNOWN chip text |
| F6 rendering | Operational layer → MARUAH; Public layer → EMPATHY |
| Floor names | Must match canonical F1–F13 names verbatim |
| Floor rules | One-line rule should match canon directionally |
| F9 name | Must be ANTIHANTU (not ANTI-CASCADE or other variant) |
| F9 color | Canonical is #FF003C |
| F9 description | Core rule: "No deception, manipulation, consciousness claims." |
| Evidence chips | Must emit one of the four band names, not a fifth custom class |

### Step 3 — Seal Status Audit

```bash
# Check immutable flag on all constitutional documents
lsattr /root/arifOS/GENESIS/FLOOR_TABLE.json /root/AAA/AGENTS.md /root/arif-sites/sites/arif-fazil.com/src/pages/Wealth.tsx /root/scripts/wealth-static-render.py /root/AAA/CLAUDE.md /root/AGENTS.md

# Check seal receipt existence
test -f /root/forge_work/2026-07-24/floor-table-canon-seal-2026-07-23.md && echo "SEAL_RECEIPT_EXISTS" || echo "SEAL_RECEIPT_MISSING"

# Stat for last-modified timestamps
stat --format='%s %y %n' /root/arifOS/GENESIS/FLOOR_TABLE.json /root/AAA/AGENTS.md /root/arif-sites/sites/arif-fazil.com/src/pages/Wealth.tsx /root/scripts/wealth-static-render.py /root/AAA/CLAUDE.md /root/AGENTS.md
```

**Interpretation:**
- `chattr +i` (immutable) = constitutionally sealed — cannot be accidentally modified
- `lsattr` showing only `e` (extent format, standard) = **NOT immutable** — should be set per doctrine
- Seal receipt at path declared in FLOOR_TABLE.json should exist
- Last-modified timestamps should be consistent with the `forged` date in FLOOR_TABLE

### Step 4 — CLAUDE.md & AGENTS.md Integrity Check

Cross-check these four files for mutual consistency:

| File | What to Check |
|------|---------------|
| `/root/AAA/CLAUDE.md` | References F13 SOVEREIGN, organ ports, correct F7/F9 names |
| `/root/AGENTS.md` | Has F1–F13 table; F7 must be HUMILITY; F9 must be ANTIHANTU; no 0.90 cap |
| `/root/arifOS/AGENTS.md` | Delegates to FLOOR_TABLE.json/000_KERNEL_CANON.md |
| `/root/AAA/AGENTS.md` | **Must not be a stub** — must render F1–F13 names + rules verbatim |

**Common drift point:** `/root/AAA/AGENTS.md` is the single shallowest file in the chain — frequently becomes a 7-line pointer instead of a full floor renderer.

### Step 5 — Producing the Report

Write a structured Markdown report to `/root/arifOS/audits/fasa1-floor-consumer-drift-audit-YYYY-MM-DD.md` with per-consumer drift table, seal status table, and recommended actions with severity tags (🔴 CRITICAL / 🟡 MODERATE / 🟢 MINOR).

See `references/floor-table-consumer-drift-audit-2026-07-25.md` for a worked example with actual drift findings.

### Contract-Specific Checks

**GEOX claim workflow — SPEC Rejection Gate**
- Check `/root/GEOX/contracts/claim_state_machine.yaml` for SPEC-aware rejection logic
- Verify that transition `APPROVED_INTERPRETATION → SEALED` has truth_class gate
- Cross-reference against `000_KERNEL_CANON.md` which may document known drift

**AAA AGENTS.md — Floor Render**
- Must render all F1–F13 names + one-line rules verbatim
- Must cite Ω₀, never 0.90
- Must render F6 bridge (MARUAH operational, EMPATHY public)

### Pitfalls

- **Consumers may resolve to a different path than declared.** FLOOR_TABLE may say `/root/arifOS/contracts/...` (underspecified). The active path may be `/root/GEOX/contracts/`. Always check both.
- **000_KERNEL_CANON.md may document known drift** — line 178 may say "accept SPEC as SEAL-worthy" which contradicts FLOOR_TABLE. This is a documented open issue, not a new finding.
- **Some consumers render only a subset of floors** (e.g., Wealth.tsx renders F1, F2, F7, F9, F13). This is a design choice, not drift — verify the consumer contract, not full coverage.
- **F9 commonly drifts to ANTI-CASCADE** with wrong color and description. This is the most frequent consumer error.

## Authority Recovery Mission (Structured Diagnostic)

When Arif asks for "authority recovery," "P0 federation repair," or "identity diagnostics" — especially when `actor_verified=false` is reported — use the structured 7-report diagnostic mission pattern. **The critical insight: `actor_verified=false` is correct for anonymous sessions. The identity kernel is usually WORKING. Do NOT propose rewriting it.**

Full mission template with probe sequences, file naming conventions, and classification matrices:
→ `references/authority-recovery-mission.md`

## Identity Forensic Trace — Three-Path Pattern (P0 Authority Diagnostics)

When `actor_verified=false` is reported and you need to understand WHY, trace through all three identity verification paths in `arifosmcp/tools/session.py`. **Never check just one path.** Each has different semantics:

| Path | Code Location | Mechanism | When It Fires |
|------|--------------|-----------|---------------|
| 1 — Ed25519 Crypto | session.py ~L1676 | `actor_signature` + `nonce` verified against registered public key | Caller provides valid signature |
| 2 — Localhost Auto-Sign | session.py ~L1744 | Server signs challenge with its own Ed25519 key | Caller is on localhost AND actor is registered |
| 3 — String Exemption | session.py ~L1821 + `session_auth.py` `_ED25519_EXEMPT_SYSTEM_ACTORS` | Hardcoded dict grants authority by name match | Actor ID matches "arif", "a-forge", "forge", "opencode", "hermes" |

**P0 CRITICAL — The "Silent ARIF" Bypass:** Path 3 auto-verifies ANY string matching "arif" (case-insensitive, normalized) to FULL SOVEREIGN authority — no signature, no challenge, no audit trail. The string alone grants `actor_verified=true`. This is a P0 identity breach (F11 AUTH, F2 TRUTH).

**Diagnostic probe to check exempt status:**
```bash
python3 -c "
from arifosmcp.runtime.session_auth import _ED25519_EXEMPT_SYSTEM_ACTORS
for actor in ['arif', 'hermes', 'opencode', 'a-forge', 'anonymous']:
    if actor in _ED25519_EXEMPT_SYSTEM_ACTORS:
        print(f'❌ {actor}: AUTO-VERIFIES as {_ED25519_EXEMPT_SYSTEM_ACTORS[actor]} (string match, no crypto)')
    else:
        print(f'✅ {actor}: NOT exempt (requires crypto proof)')
"
```

**When identity IS working correctly:** `actor_verified=false` for anonymous/unauthenticated callers is the EXPECTED state. Do not flag it as a bug. Only flag it when a verified actor should be getting `true` but isn't.

**Canonical identity loader consolidation:** Remove Path 3 auto-verification. The exempt list should grant **registry recognition** (for challenge issuance via `issue_actor_challenge`) but NOT automatic `actor_verified=true`. Sovereign identity requires Ed25519 signature OR explicit human approval (bridging seal).

## Build Identity Verification (Cross-Organ)

Compare deployed artifact identity against source tree HEAD for any organ. A mismatch = P0 drift:

```bash
DEPLOYED=$(curl -s http://localhost:<PORT>/health | jq -r '.git_version // .build_commit')
SOURCE=$(cd /root/<REPO> && git rev-parse --short=8 HEAD)
[ "$DEPLOYED" = "geox-$SOURCE" ] || [ "$DEPLOYED" = "$SOURCE" ] \
  && echo "MATCH" || echo "MISMATCH: $DEPLOYED vs $SOURCE"
```

**Proven:** GEOX 2026-07-19 — deployed `geox-43a706f7` ≠ HEAD `6f895126`. Mid-mission rebuild resolved.

## Drift Detection Infrastructure Audit

When diagnosing federation drift, check three detection layers:

### Layer 1 — Systemd Timers
```bash
systemctl list-timers --no-pager | grep -i drift
```

### Layer 2 — Cron Jobs
```bash
crontab -l | grep -i drift
```

### Layer 3 — Drift Scripts
```bash
find /root -name "*drift*" -type f 2>/dev/null | wc -l
```

### Coverage Matrix

Produce a per-organ coverage table:

| Organ | kernel timer | cron | CI workflow | health endpoint | alerting |
|-------|-------------|------|-------------|-----------------|----------|
| arifOS | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

**Critical gaps:** Missing WEALTH/WELL drift monitoring, no cross-organ reconciliation.

## VAULT999 Chain Classification

The seal chain uses mixed sequence schemes by design. When reconciling, classify the chain state:

| Classification | Meaning |
|---------------|---------|
| `CHAIN_VALID_MULTI_EPOCH` | Multiple epochs, different schemes; contiguous within each |
| `CHAIN_CONTIGUOUS` | Single numeric, no gaps |
| `CHAIN_VALID_SEQUENCE_SPARSE` | Different schemes coexist; no corruption |
| `CHAIN_CORRUPT` | Hash chain broken |

**Never re-sequence to enforce uniformity — destroys multi-epoch provenance.**

Full gap analysis with diagnostic probe and escalation rules:
→ `references/vault999-chain-gap-classification.md`

## External Ecosystem Verification (PulseMCP)

When Arif asks about the arifOS PulseMCP listing or wants to verify the public ecosystem surface, verify the full external presence:

### Step 1 — Find the PulseMCP listing URL

The PulseMCP slug does NOT follow the `io.github.owner/repo` path. The arifOS listing is at:
```
https://www.pulsemcp.com/servers/ariffazil-arifos
```
There is also a separate implementation listing at `pulsemcp.com/servers/ariffazil-arifosmcp`.

### Step 2 — Verify the listing page

Check: classification (community/official), visitor count, rank (global + weekly), release date, GitHub stars, related servers. The related servers section reveals ecosystem positioning — arifOS sits alongside Defenter, Fulcrum, AgentOS, Apiiro Guardian, Bulwark, AGA, Sentinel, Delimit, EU AI Governance.

### Step 3 — Verify the endpoint

The PulseMCP UI truncates the endpoint URL (shows `https://arifosmcp.arif-fa...`). The canonical MCP endpoint is:
```
https://mcp.arif-fazil.com/mcp
```
Both `arifosmcp.arif-fazil.com` and `mcp.arif-fazil.com` resolve to the same gateway (Cloudflare). The `arifosmcp` subdomain is a landing page with `<link rel="mcp" href="https://mcp.arif-fazil.com/mcp">`.

### Step 4 — Verify server.json

The `.well-known/mcp/server.json` is the **authoritative source** — NOT GitHub raw. Both `raw.githubusercontent.com/ariffazil/arifos/main/server.json` and `.../arifosmcp/main/server.json` return 404. The `.well-known` endpoint on the live server is canonical:
```bash
curl -sS https://mcp.arif-fazil.com/.well-known/mcp/server.json | python3 -m json.tool
```

### Step 5 — Verify runtime health

Standard health probe + tools/list + surface consistency check:
```bash
curl -sS https://mcp.arif-fazil.com/health
curl -sS -X POST https://mcp.arif-fazil.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

Key fields to verify: `runtime_drift`, `contract_drift`, `surface_consistency.verdict`, `boot_attestation`, `vault999_health`, `floors_active`.

### Output Format

```
PulseMCP VERIFICATION — YYYY-MM-DD

Listing: ✅/❌ | URL: <url> | Rank: #N | Visitors: N
Endpoint: ✅/❌ | <url> | Protocol: <version>
server.json: ✅/❌ | .well-known: <status> | GitHub raw: 404 (expected)
Runtime: ✅/❌ | v<version> | drift: false | surface: CONSISTENT
```

## Credential-Config Drift Detection

When a credential (API key, env var, token) is blocked/rotated/deleted in the source of truth but residual references remain in config files across the federation — run this protocol.

### When to Use

- User says "why is quota still draining after I blocked the key?" or "trace where X key is used"
- After rotating/blocking a credential — verify no residual references survived
- During security audit — find where a dead/broken key still has config references
- Before decommissioning a provider — ensure no service still points to it

### The Protocol

```bash
# Phase 1 — Source of Truth Check
# Check vault.env (SSOT) — is it actually commented out / missing?
grep -n '^#.*ILMU_API_KEY\|^ILMU_API_KEY\|^export ILMU_API_KEY' /root/.secrets/vault.env

# Check vault.flat.env (systemd EnvironmentFile) — is it synced?
grep 'ILMU_API_KEY' /root/.secrets/vault.flat.env

# Check if the env var actually resolves at runtime
set -a && source /root/.secrets/vault.env && set +a
echo "KEY=[${KEY_VAR:-EMPTY}]"

# Phase 2 — Startup Script Scan
# Find ALL scripts that reference the credential — they might read from
# vault.flat.env (not vault.env) or have hardcoded values
grep -rn 'ILMU_API_KEY\|API_KEY=' /usr/local/bin/*.sh /opt/*/bin/*.sh 2>/dev/null
grep -rn 'ILMU_API_KEY' /etc/systemd/system/*.service /etc/systemd/system/*.d/*.conf 2>/dev/null

# Phase 3 — Hardcoded Key Scan (the most dangerous pattern)
# Search for keys that look hardcoded (sk-..., pplx-..., tp-..., etc.)
# in config files — these bypass vault.env entirely
grep -rn '"sk-\|"pplx-\|"tp-\|"csk-' /root/.openclaw/ /root/.config/ /root/A-FORGE/ /root/HERMES/ 2>/dev/null | grep -v '.git/' | grep -v node_modules | grep -v '.jsonl'

# Phase 4 — Docker Container Check
# For each running Docker container with the credential:
# Check actual runtime env (not docker inspect — that shows build-time, not run-time)
docker exec <container> env 2>/dev/null | grep CREDENTIAL
# Check container config files that reference the credential
docker exec <container> cat /app/config.yaml 2>/dev/null | grep -i credential

# Phase 5 — Running Process Check
# Has anything got this key live in its environment?
for pid in $(ps -eo pid=); do
  env=$(cat /proc/$pid/environ 2>/dev/null | tr '\0' '\n' | grep 'KEY_VAR=' || true)
  [ -n "$env" ] && echo "PID $pid: $env"
done

# Phase 6 — Systemd Unit / Drop-In Check
# Check all service drop-in dirs for hardcoded references
for f in /etc/systemd/system/*.service.d/*.conf; do
  [ -f "$f" ] && grep -l 'KEY_VAR' "$f" 2>/dev/null
done

# Phase 7 — Agent Config Check
# OpenClaw agents may have hardcoded keys in models.json
find /root/.openclaw/agents -name 'models.json' -exec grep -l 'ilmu\|KEY_VAR' {} \;
# OpenCode config may reference the provider
grep -rn 'ilmu\|KEY_VAR' /root/.config/opencode/opencode.json 2>/dev/null
```

### Classification Matrix

| Pattern | Meaning | Severity | Action |
|---------|---------|----------|--------|
| Key in vault.env but **commented** | Blocked in source of truth | ✅ Intentional | Leave alone |
| Key in vault.env but **NOT in vault.flat.env** | flat.env stale (sync script only goes flat→env, not reverse) | 🟡 Stale | Manual sync or regen flat.env |
| Key in **startup script** hardcoded | Bypasses vault entirely | 🔴 P0 Critical | Replace with env var reference |
| Key in **systemd drop-in** | Overrides vault.env sourcing | 🔴 P1 High | Remove, let vault sourcing handle it |
| Key in **Docker env** at runtime | Container has the key live | 🔴 P0 if key dead (401 loop), P1 if key active but shouldn't be | Restart container with correct env |
| Key in **Docker container config file** | Container reads from config.yaml not env | 🟡 P2 unless the key mismatches vault | Update config file + restart |
| Key in **agent models.json** hardcoded | Bypasses vault.env — agent sends literal key | 🔴 P1 — hardcoded credential in plaintext | Replace with env var reference or remove |
| Key in **A-FORGE config** as key_env | Uses env var — will get empty string if key dead | 🟡 P2 — will fail silently on use | Update config to point to working provider |
| Running process has key in /proc/PID/environ | Process started when key was live, hasn't restarted since | 🟡 P2 — stale but harmless until restart | Note for next restart cycle |

### Pitfalls

- **`docker inspect` shows build-time env, not runtime env.** The `-e OPENAI_API_KEY=` you see in `docker inspect` is what was PASSED at container start — it can be empty string. To see what the container actually resolves, exec inside: `docker exec <container> env | grep KEY`. Confirmed in this session: Graphiti container showed `OPENAI_API_KEY=` (empty) in `docker inspect` AND in `docker exec env` — correctly dead.
- **Startup scripts may read from `vault.flat.env` while other services read from `vault.env`.** These two files can drift. The sync script only goes `flat→env`, not `env→flat`. So a key commented out in `vault.env` may still be present in `vault.flat.env` (or vice versa). **Check both.**
- **Hardcoded keys in config files bypass all vault.env management.** If a key is rotated in vault.env but hardcoded in a `models.json`, the hardcoded version keeps working. This is the most dangerous credential-config drift pattern.
- **`/proc/<PID>/environ` shows env at process start, not current state.** If the process started before the key was rotated, it still has the old key. You must restart the service to pick up the new env.
- **Don't confuse "credentials still referenced in config" with "credentials still working."** A config file can reference a dead key (env var empty) and the service handles the 401 gracefully. The config reference is drift; the service behaviour is a separate question. Report both, fix the drift independently.

### Real Example (ILMU API Key, 2026-07-25)

From this session's credential trace:

| Location | Status | Action Taken |
|----------|--------|-------------|
| `vault.env:97` | Commented out (F13 BLOCKED) | ✅ Intentional |
| `vault.flat.env` | Missing entirely | 🟡 flat.env stale |
| `graphiti-start.sh` | Reads from vault.flat.env → gets empty string | 🟡 Startup script reads wrong source |
| `Graphiti Docker container` | `OPENAI_API_KEY=` (empty) | 🔴 Container configured for dead provider |
| `opencode/agent/models.json` | Hardcoded `"apiKey": "***"` | 🔴 Hardcoded credential |
| `main/agent/models.json` | `"apiKey": "ILMU_API_KEY"` (literal string) | 🟡 Sends wrong string as key |
| `apex_battery_config.yaml` | References `key_env: ILMU_API_KEY` | 🟡 Config references dead env var |
| OpenClaw gateway config | Has `ilmu` in fallback_providers | 🟡 Fallback chain references dead provider |

## Heartbeat Poll Response Protocol

**When the system sends a heartbeat poll (BEAT_OK / ARTBEAT_OK / HEARTBEAT_OK / _OK / AT_OK):**

| State | Response | Rationale |
|-------|----------|-----------|
| All green — recently verified | `HEARTBEAT_OK` (or `Hijau ✅` for casual) | Silent on green. No tool calls. No commentary. |
| Not verified recently / active crash pattern | Quick silent probe (`curl :8088/health` only) → if green: `HEARTBEAT_OK` | Brief verify acceptable when crash patterns exist. |
| Down / degraded | Alert text. Do NOT include `HEARTBEAT_OK`. | Sovereign notified only when action needed. |

**Key rules:**
- No analysis, no extra tool calls, no commentary on green. The heartbeat IS the status.
- If arifOS has been crashing (dead API key, event-loop hang), one quick probe is acceptable — but respond immediately after with just the response code.
- "Hijau ✅" for casual BEAT_OK/AT_OK/_OK messages. `HEARTBEAT_OK` is formal protocol.
- When a prior HEARTBEAT already confirmed green within minutes, a subsequent BEAT_OK needs zero verification — just acknowledge.

**Pitfall — Multi-Turn Heartbeat Loop (proven 2026-07-23):**
OpenClaw sends heartbeats as user messages. Making a tool call + analysis response feeds OpenClaw's input queue → sends another heartbeat → infinite loop. Break by issuing the exact heartbeat response with no extra output, which OpenClaw's heartbeat handler discards as expected.

## Cross-Witness Audit Verification Pattern

When one agent produces an audit, report, or findings list — **never accept it as truth without independent verification.** The producing agent is a SINGLE witness. Reality Engineering requires ≥2 independent witnesses before a claim graduates from OBS to TRUTH.

### The Protocol (3-Probe)

| Probe | Question | Method |
|-------|----------|--------|
| **Live?!** | Can the claim be verified against a live endpoint RIGHT NOW? | `curl :PORT/health`, `ps aux`, `systemctl status`, `cat /path/to/file` |
| **Cross-referenced?!** | Does a second independent source agree? | Different endpoint, different tool, different agent's perspective |
| **Plausible?!** | Does the claim pass the sniff test given known system constraints? | Domain knowledge, prior session state, documented invariants |

### Classification

| Outcome | Meaning | Action |
|---------|---------|--------|
| **Confirmed True** | Live probe matches claim | Accept and escalate as needed |
| **Confirmed False** | Live probe contradicts claim | Document the correction. **Do NOT propagate the original claim.** |
| **Gap — needs evidence** | Cannot verify (organ down, no direct endpoint, stale data) | Tag as UNKNOWN. Do not accept or reject. |

### Proven Example (2026-07-28)

OpenCode (FI-001) produced a 7-layer internal audit with 8 findings against the federation. Hermes independently verified each claim:

| OpenCode Claim | Live Probe | Verdict |
|----------------|------------|--------|
| "MCP resources = 0" | `list_resources` returned all ATLAS333, doctrine, vitals | ❌ False — protocol mismatch |
| "VAULT999 silent 4 days" | 3 seals from today in outcomes.jsonl | ❌ False — seals exist |
| "Kernel healthy+F2 violation" | service_health=green, execution_readiness=held | ❌ False — correct constitutional separation |
| "Hermes systemd inactive" | `systemctl is-active hermes` = inactive | ✅ True |
| "Kernel deployment drift" | source≠built commit in /health | ✅ True |
| "WEALTH version UNAVAILABLE" | git_commit=UNAVAILABLE in /health | ✅ True |
| "14 open loops" | carry_forward.json confirms | ✅ True |

**Accuracy: ~60%.** 5 correct, 3 false. When a single-agent audit is ~60% accurate, **every claim needs verification**, not just the suspicious ones. The false claims were not malicious — they were confident misinterpretations (protocol issues, stale reads, conflating distinct kernel fields).

### The Lesson

- **Single-agent audit = OBSERVATION, not TRUTH.** Always cross-witness before declaring.
- **An agent that sounds confident is not more reliable.** OpenCode presented all findings with equal confidence — the false ones were phrased as damningly as the true ones.
- **Interpretive claims are the least reliable** — "this means X" is always weaker than "this shows Y."
- **When an audit triggers alarms**, verify the most alarming claims first. They are statistically the most likely to be misinterpretations.

## Agent Self-Report Audit Pattern

When auditing any agent's self-description (including OpenClaw/AGI), **verify ALL numeric claims against live sources.** Agents frequently hallucinate numerical specifics — numbers that sound plausible but don't match reality.

**Proven 2026-07-26 — OpenClaw audit found 3 false claims:**

| Claim | Agent said | Live probe | Error |
|-------|-----------|------------|-------|
| WELL biometric stale | "2056h (~85 days)" | `freshness_band: FRESH` (0.2h), never received input | Hallucinated figure |
| a-forge-mcp restarts | "9 restarts" | Only 2 start events (journalctl) | Inflated 7x |
| Own boot time | "Restored 01:05 UTC" | Booted 18:08 UTC | Off by 17h |

**Correction — verify agent numeric claims:**
```bash
# Restart count
journalctl -u <SERVICE> --no-pager | grep -c 'Started'

# Process start time
ps -o lstart= -p <PID>

# Organ freshness
curl -sf http://127.0.0.1:<PORT>/health | grep -E 'freshness|state_age|well_signal'
```

**Never trust self-reported numbers** without live verification. F2 TRUTH concern — agents should tag estimates as `ESTIMATE`.

## Pitfalls

- **vault.env bot token duplication (proven 2026-07-24):** `/root/.secrets/vault.env` may contain MULTIPLE lines for the same variable with DIFFERENT values. One `export TELEGRAM_BOT_TOKEN` with a live token, another unexported line with a dead/stale token. When a systemd drop-in hardcodes the wrong one, the service runs with the incorrect (dead) token. **Verify which token the service actually loads by checking the drop-in file**, not vault.env. The sops/age-encrypted values show as `***` when grepped — never assume `***` means "dead". The only reliable verification is probing the Telegram API with the actual runtime token, or reading `/proc/<PID>/environ` of the running process.

- **Streamable HTTP protocol mismatch for external organs (proven 2026-07-24).** WEALTH, WELL, GEOX, and A-FORGE use Streamable HTTP transport (MCP Protocol Specification) that returns HTTP 400 or empty tool lists when probed with raw `tools/list` POST. The `federation_reality_probe.py --scope` flag currently falls back to organ-specific MCP tools (e.g., `geox_surface_status`, `well_registry_status`). Future upgrade: add SSE / Streamable HTTP client framing for full coverage. WEALTH also requires session_id for all calls (L11 AUTH), blocking anonymous probe entirely.\\n- **arifOS 413 \"Request payload too large\" — body size limit is 1MB by default (proven 2026-07-23).** The arifOS gateway's `BodySizeLimitMiddleware` (`arifosmcp/runtime/fastmcp_ext/transports.py:563`) defaults to 1,048,576 bytes when `ARIFOS_HTTP_MAX_BODY_BYTES` is not set in the systemd unit. MCP tool calls with large responses (e.g., `arif_observe` with governance metadata) blow past 1MB and return 413. Fix: add `Environment=ARIFOS_HTTP_MAX_BODY_BYTES=10485760` (10MB) to `/etc/systemd/system/arifos.service`, then `systemctl daemon-reload && systemctl restart arifos`. Verify with `systemctl show arifos -p Environment | grep MAX_BODY`. The env var is read at startup by the FastMCP transport layer — no code change needed.** WEALTH, WELL, GEOX, and A-FORGE use Streamable HTTP transport (MCP Protocol Specification) that returns HTTP 400 or empty tool lists when probed with raw `tools/list` POST. The `federation_reality_probe.py --scope` flag currently falls back to organ-specific MCP tools (e.g., `geox_surface_status`, `well_registry_status`). Future upgrade: add SSE / Streamable HTTP client framing for full coverage. WEALTH also requires session_id for all calls (L11 AUTH), blocking anonymous probe entirely.\n- **arifOS 413 "Request payload too large" — body size limit is 1MB by default (proven 2026-07-23).** The arifOS gateway's `BodySizeLimitMiddleware` (`arifosmcp/runtime/fastmcp_ext/transports.py:563`) defaults to 1,048,576 bytes when `ARIFOS_HTTP_MAX_BODY_BYTES` is not set in the systemd unit. MCP tool calls with large responses (e.g., `arif_observe` with governance metadata) blow past 1MB and return 413. Fix: add `Environment=ARIFOS_HTTP_MAX_BODY_BYTES=10485760` (10MB) to `/etc/systemd/system/arifos.service`, then `systemctl daemon-reload && systemctl restart arifos`. Verify with `systemctl show arifos -p Environment | grep MAX_BODY`. The env var is read at startup by the FastMCP transport layer — no code change needed.
- **Don't confuse "registered" with "fallback."** When auditing model configurations, `agents.defaults.models` (available models) ≠ `model.fallbacks` (auto-failover chain). Both Hermes and OpenClaw have separate fields. Always grep both.
- **AGI priority violation: infra before UI.** AGI will tunnel-vision on dashboard/site work while infrastructure isn't verified. "Dashboard on dead timer = pretty lie." Always verify infrastructure layer (systemctl status, state files, logs) BEFORE touching presentation/UI. If AGI ignores priority redirection, escalate to 888_OVERRIDE immediately. Proven 2026-07-14: AGI ignored 4 priority redirections to build Observatory while timer wasn't registered in systemd.
- **Tool-hunger: don't build because infrastructure exists.** When evaluating whether to forge new capability, ask: "Does the PROBLEM exist, or does the INFRASTRUCTURE exist?" If current utilization is <20% of capacity, the correct action is status quo + document triggers for when to revisit. Building because ollama/bge-m3 is live (not because 7KB flat memory is struggling) is tool-hunger, not engineering.
- **`tools/list` count ≠ registered tools count.** Middleware can filter `tools/list` to show only the public surface. GEOX shows 17 via HTTP but has 78 runtime tools. Always check three layers: (1) HTTP `tools/list`, (2) in-process `mcp.list_tools()`, (3) registry `CANONICAL_PUBLIC_TOOLS`. If they differ, check `on_list_tools` middleware. **This is usually by design, not a bug.** (2026-07-11 GEOX P1 investigation)
- **arifOS is stateless — never require `mcp-session-id`.** arifOS runs `stateless_http=True` (PHOENIX-73C). Federation clients that gate on session availability will fail with "session_unavailable". Fix: generate local session ID for correlation, proceed with tool calls without server session. Check ALL code paths that call arifOS — both `federation_memory.py` AND health checks had this bug. (2026-07-11 GEOX P2 fix)
- **Dead tool references in health checks.** If a health check calls a tool that was renamed/removed, the response is `KERNEL_DENY` — not a crash. Health checks should gracefully degrade: report the failure in the health note, don't block. (2026-07-11: `arif_ops_measure` doesn't exist on arifOS)
- **Transport protocol mismatch (proven 2026-07-14).** Hermes config declares `transport: streamable-http` for all organs, but each organ speaks a different dialect. **Always test both GET /tools AND POST /mcp when auditing transport.** Per-organ transport dialect (verified 2026-07-14):
  - **arifOS (8088):** streamable-http. JSON-RPC POST works WITH `Accept: application/json` header. Without it, returns EMPTY.
  - **GEOX (8081):** SSE-mode. JSON-RPC POST fails with `-32602 Invalid request parameters` — requires MCP session init that external callers can't complete. /tools GET works fine (15 tools).
  - **WEALTH (18082):** streamable-http. JSON-RPC POST requires `initialize` handshake first, then `tools/list` returns 12 tools. Without init, returns 0.
  - **WELL (18083):** streamable-http. Raw JSON-RPC POST works without handshake (29 tools). Only organ where raw POST works.
  - **A-FORGE:** Two surfaces — STDIO (98 tools via `node dist/src/interfaces/mcp/server.js`) vs HTTP (5 stateless tools on port 7072). Port 7071 is HTTP bridge with no MCP tools. smithery.yaml advertises 8 phantom tools matching neither surface.
  - **AAA (3001):** A2A protocol only, no MCP tool surface.
  - **MIND (51001):** Health endpoint only, no MCP tools. Cognitive organ (Stage 333s). Port 51001, NOT 3003 (stale reference in AGENTS.md).
- **Zombie port detection.** Legacy processes from pre-rename eras can linger on old ports. Port 18081 was found running old `arifosd.py` (pre-rename GEOX daemon) with no health endpoint. Always check `lsof -i:<PORT>` and `ps aux | grep <service>` for ports that shouldn't be active. Kill with `kill <PID>` after confirming it's a zombie.

- **Organ probe hostname mismatch — kernel shows "offline" for organs that are actually up (proven 2026-07-18).** When `curl localhost:<PORT>/health` returns 200 but the kernel's `/api/live/all` reports "offline", the probe hostnames in `rest_routes.py` are wrong. The kernel uses Docker container hostnames (`geox_eic`, `wealth-organ`, `well`) that don't resolve on bare-metal. Fix: change to `localhost` with correct ports (8081→8081, wealth-organ:8082→localhost:18082, well:8083→localhost:18083). See `references/observatory-dual-engine.md` for full architectural context.

- **Telegram Markdown tables do NOT render — use plain text or HTML (proven 2026-07-21).** Despite what the Hermes system prompt says about rich Markdown table support, the actual Telegram bot cannot render pipe `| col | col |` tables. They arrive as raw markdown source text. Arif explicitly: "bot ni tak support format tu lagi. Plain text atau HTML je boleh." Use bullet lists, indented key-value pairs, or `key: value` format for structured data. Reserve Markdown tables for file artifacts only (forge_work). Applies to ALL outputs on Telegram — skill content can have tables, but what the agent says TO Arif must be plain-formatted.

- **vault.env bot tokens are redacted with `***` — grep returns `***`, not the real token (proven 2026-07-24).** All secrets in vault.env and vault.flat.env are stored as sops/age-encrypted values that appear as `***` in the file. `grep TELEGRAM_BOT_TOKEN vault.env` showing `***` is EXPECTED — it does NOT mean the token is dead. The real tokens are decrypted at runtime by secure launch scripts (`openclaw-gateway-secure.sh`, `hermes-gateway-secure.sh`). To verify a bot's actual token: (1) find the running process, (2) `cat /proc/PID/environ | tr '\\0' '\\n' | grep TELEGRAM_BOT_TOKEN`. **Never declare a bot dead from grep on vault.env.** See `references/telegram-bots-inventory.md` §Sops/Secrets Token Redaction Pattern.

- **Federation reboot cascade: arifOS restart → gateway MCP poison → full reboot (proven 2026-07-23).** When arifOS restarts cleanly via systemd, the hermes-asi-gateway gets a dependency-triggered SIGTERM. If Hermes MCP has been degraded (failing reconnects with "unhandled errors in a TaskGroup" every 300s for 17+ min), the gateway cannot cleanly terminate. Exit code 1 → network.target cascade → full systemd reboot. Root cause: Hermes MCP instability (pre-existing). Trigger: arifOS restart (benign). Detection: `journalctl -u hermes-asi-gateway --since "30 min ago" | grep "failed after 5 reconnection"`. If seen, gateway is vulnerable. Fix: restart gateway cleanly when MCP errors accumulate, OR harden gateway to tolerate MCP termination failures (exit 0 instead of 1).

- **Gateway shutdown race: Event loop closed → exit 75/TEMPFAIL → systemd restart counter (proven 2026-07-24).** During a clean `hermes gateway restart` (or `systemctl restart hermes-asi-gateway`), the old process can crash with `RuntimeError: Event loop is closed` in `mcp_tool.py:_wait_for_reconnect_or_shutdown` (~line 1997). The asyncio event loop closes before pending MCP reconnection tasks are cleaned up, causing `Task was destroyed but it is pending!` errors. Exit code 75 (TEMPFAIL) → systemd increments `StartLimitBurst=3` counter. If counter hits 3 within `StartLimitInterval=60`, systemd stops restarting — gateway stays dead. This is a race condition in the MCP tool shutdown path, distinct from the MCP poison cascade above (exit 1 from degraded MCP). Detection: `journalctl -u hermes-asi-gateway | grep -A5 "Event loop is closed"`. The gateway typically stabilizes on the next systemd restart (counter resets after interval). Fix: harden `_wait_for_reconnect_or_shutdown` to catch `RuntimeError` when event loop is already closed, or cancel pending tasks before loop shutdown. Gateway debug sequence: (1) `tail -100 ~/.hermes/logs/gateway.log` for crash pattern, (2) `ps aux | grep gateway` for running PID, (3) `journalctl -u hermes-asi-gateway --no-pager -n 50` for systemd view, (4) `systemctl cat hermes-asi-gateway` for unit config, (5) `ss -tlnp | grep -E "18086|18001"` for MCP dependency check.

- **Dual-bot convergence ≠ truth (proven 2026-07-18).** When OpenClaw and Hermes independently converge on the same diagnosis, it's a useful signal but NOT proof. Both bots share the same VPS, same tools, same data sources — they can converge on the same wrong conclusion. Always verify against live state (`curl`, `systemctl`, `ps`) before acting on any diagnosis, even when both bots agree. OpenClaw correctly identified the observatory gap (6 organs with null identity); Hermes confirmed and fixed it. The convergence was valuable because we backed it with direct `/health` probes — not because two bots agreed.

- **Agent feedback loop via shared chat (proven 2026-07-19).** When Hermes and OpenClaw share the same Telegram chat/channel, every Hermes response becomes an OpenClaw user message. If OpenClaw's model cascade is failing (all providers 429), it posts an error back to the chat → Hermes sees it as a user message → responds → OpenClaw picks up the response → fails again → error → infinite loop. **Break by killing the failing agent's process:** `kill -9 <pid>`. The auto-restart will bring it back fresh after rate limits reset. Do NOT keep responding — every response feeds the loop. The symptom is the same error message arriving 3+ times with your replies interspersed.

- **drift-alert false positive: broken symlinks in `.grok/skills.zen-archived-*` are harmless (proven 2026-07-22).** The `drift-alert` cron job runs `find /root -maxdepth 4 -xtype l` and flags any count >40 as a warning. The `.grok/skills.zen-archived-*` directory contains ~324 broken symlinks from a zen-skill archive operation. These are NOT system rot — they're leftover references from a skills consolidation that the archive tarball preserves but the live filesystem no longer needs. **When you see `broken=324` from drift-alert, check if they're all in `.grok/` first.** If yes, it's a false alarm. The 40-threshold alert was designed for production symlinks (e.g., broken `/var/www/` references), not archive residue.

- **GEOX has no systemd service — check with `ps aux` not `systemctl` (proven 2026-07-19).** GEOX runs directly from `/root/GEOX/.venv/bin/python3 -m geox_mcp.server` with no systemd unit. `systemctl status geox` returns `Unit not found`. Always verify GEOX liveness with `ps aux | grep geox_mcp.server` or `curl :8081/health`, never with systemctl. The heartbeat daemon (`organ_heartbeat_daemon.py geox http://127.0.0.1:8081/health`) is a separate process that monitors GEOX but doesn't manage its lifecycle.

**Emergency load triage — full protocol for SEV:high load alerts:**
→ `references/emergency-load-triage.md`

Covers: orphan identification (github-mcp-server, pytest, kimi, browser), kill+verify sequence, boot storm vs emergency classification, shutdown cascade forensics.

- **arifOS event loop freeze — TCP accept but no HTTP response (proven 2026-07-23).** `curl -v http://localhost:8088/health` shows `* Connected to localhost` but `* Operation timed out after 5000 milliseconds with 0 bytes received`. The Python process is alive (systemd says active) but its async event loop is stuck — probably waiting on I/O or deadlocked. Fix: `systemctl restart arifos`. Recovery takes ~15s (tool wrapper loading). Memory looks fine (289MB) — this is NOT an OOM. Detection: `curl -v --max-time 5 http://localhost:8088/health 2>&1 | tail -5`.

- **arifOS memory pressure → auto-restart (proven 2026-07-23).** `systemctl status arifos` shows `Memory: 1.5G (high: 1.5G, max: 2G, swap max: 512M, available: 0B, peak: 1.5G, swap: 511.9M)`. When `available: 0B` AND swap is near `512M peak`, systemd deactivates the service (stop-sigterm). It auto-restarts cleanly within ~16s. The real issue: 4h 37min uptime before OOM suggests a slow memory leak. Temporary fix: raise MemoryHigh to 2G. Permanent fix: investigate leak. Detection: `systemctl status arifos --no-pager | grep Memory`.

- **GEOX editable-install branch-switch mismatch (proven 2026-07-19).** When GEOX runs from an editable pip install (`pip show geox` shows `Editable project location: /root/GEOX`) and the git working tree is switched to a different branch after startup, the health endpoint reports the commit from the OLD branch — not the current checkout. The running Python process has the old code in memory. **Always verify with both `curl :8081/health | jq '.git_version'` AND `git -C /root/GEOX rev-parse --short=8 HEAD` to detect this mismatch.** A mismatch means the running process pre-dates the branch switch and needs a restart. The `drift_check_live.py` script compares `source_commit[:8]` against `str(deployed_version)` using Python's `in` (substring) operator. Version strings like `"v2026.07.17"` can coincidentally contain hex-like substrings, producing false negatives. Conversely, longer strings without the commit substring produce false positives (ALL organs flagged DRIFT when clean). **Always extract commit hash patterns with regex** — never use substring `in` for drift comparison. Fix: `re.findall(r'[0-9a-f]{7,40}', deployed_version)` to extract actual commit prefixes from version strings. Same pattern as arifOS MCP `tools/list` — without the correct Accept header, `resources/list` returns 406. With the header, returns 31 resources including 11 ATLAS333 URIs. When auditing ATLAS333 surface exposure, always use:
  ```bash
  curl -sf -X POST http://localhost:8088/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}'
  ```

## MCP Transport Debugging

When `tools/list` returns unexpected counts, federation health reports session issues, or MCP calls fail with "session_unavailable", load the transport debugging patterns:

- **Web search config split-brain (proven 2026-07-21).** Hermes config has TWO search sections — `web:` (used by `web_search` tool) and `search:` (used by search-only toolset). They can drift to different backends (e.g., `web.backend: brave` while `search.backend: searxng`). Verify: `grep -n "search_backend\|backend:" /root/.hermes/config.yaml | grep -v "^#\|x_search"`. Both `web:` and `search:` sections must show the same backend. Fix: `hermes config set web.search_backend searxng && hermes config set web.backend searxng`.

- **SearXNG bind-mount edit pattern (2026-07-21).** SearXNG settings.yml is bind-mounted from `/root/searxng/settings.yml` to `/etc/searxng/settings.yml:ro` in the container. Edit on HOST, then `docker restart searxng`. Never edit inside container.

→ `references/mcp-transport-debugging.md`

Covers: stateless_http session ID gap, middleware filtering `tools/list`, mounted server tools invisible to clients, dead tool references in health checks.
