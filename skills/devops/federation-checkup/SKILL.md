---
name: federation-checkup
description: "Standard checkup protocol for the arifOS federation — dual-probe pattern, floor interpretation, OpenCode session monitoring, flag hierarchy for human-readable reports, and sweep-and-classify housekeeping. Load when Arif asks 'how's the system', 'status', 'checkup', 'semua organ hijau ke', 'what's running', 'sweep the federation', 'find everything pending/stale', or any health/readiness/housekeeping probe of the federation."
tags: [federation, health, checkup, arifOS, observability, ops]
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
  - "drift monitor repair"
---

# Federation Checkup — Dual-Probe Protocol

> Always run both probes. Reconcile before reporting. Surface by flag hierarchy.

## The Core Lesson

**`curl :port/health` ≠ organ health. It only means the process is alive.**
**Diagnostic-first is an anti-pattern for Arif.** When the system is already up and operational, verbose diagnostic probes generate stale/corrected takeaways that waste session time. A prior session ran full P0/P1 diagnostics only to have Arif confirm the system was already operational — the takeaways were wrong. Trust Arif's signal over self-generated probe anxiety.

**Rule:** If the system is confirmed up and Arif wants to move forward, skip the dual-probe. Probes only when there is a genuine symptom to explain. The canonical source of truth for "is the system healthy" is `curl :PORT/health` + Arif's own observation — not a verbose multi-step diagnostic ritual.
**Rule:** If the system is confirmed up and Arif wants to move forward, skip the dual-probe. Probes only when there is a genuine symptom to explain. The canonical source of truth for "is the system healthy" is `curl :PORT/health` + Arif's own observation — not a verbose multi-step diagnostic ritual.
The Observatory (`/api/status`) shows the real constitutional state — per-floor scores, vitality, drift, witness channels. These two probes frequently disagree. Always run both and reconcile.

## Automated Artifact Generation (Cloud AI Ingestion)

For producing immutable federation reality artifacts for cloud AI ingestion (the **epistemic bridge** — Truth without Vector), use the reality snapshot compiler:
→ `references/reality-snapshot-compiler.md`

```bash
# Human + AI readable markdown
python3 /root/scripts/reality_snapshot.py

# Machine-readable JSON
python3 /root/scripts/reality_snapshot.py --json

# Save to dated forge_work
python3 /root/scripts/reality_snapshot.py --output /root/forge_work/$(date +%Y-%m-%d)/reality_state.md
```

**When to use:** Arif wants to paste federation context into a cloud AI chat (Gemini, Claude, etc.) — the artifact provides grounded reality without exposing credentials, shell access, or mutation capability.

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

# Telegram bots — THREE distinct bots, THREE owners
# @ASI_arifos_bot  = Hermes (this session)
# @arifOS_bot      = OpenCode code execution
# @AGI_ASI_bot     = OpenClaw AGI gateway
for bot in opencode-bot openclaw-gateway; do
  systemctl is-active --quiet $bot 2>/dev/null && echo "✅ $bot" || echo "❌ $bot"
done
```

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

## Cage Audit (Deep Constitutional Stress Test)

When the checkup goes beyond "are organs alive?" into "can the constitution actually constrain the sovereign's future self?" — run the cage audit pattern. Covers identity verification (Ed25519), cooling ledger persistence, airlock error rates, VAULT999 integrity, runtime drift, and floor enforcement depth.

→ `references/cage-audit-constitutional-stress-test.md`

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

## Pitfalls

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

- **Federation reboot cascade: arifOS restart → gateway MCP poison → full reboot (proven 2026-07-23).** When arifOS restarts cleanly via systemd, the hermes-asi-gateway gets a dependency-triggered SIGTERM. If Hermes MCP has been degraded (failing reconnects with "unhandled errors in a TaskGroup" every 300s for 17+ min), the gateway cannot cleanly terminate. Exit code 1 → network.target cascade → full systemd reboot. Root cause: Hermes MCP instability (pre-existing). Trigger: arifOS restart (benign). Detection: `journalctl -u hermes-asi-gateway --since "30 min ago" | grep "failed after 5 reconnection"`. If seen, gateway is vulnerable. Fix: restart gateway cleanly when MCP errors accumulate, OR harden gateway to tolerate MCP termination failures (exit 0 instead of 1).

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
