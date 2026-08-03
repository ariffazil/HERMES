---
name: live-probe-audit-pattern
description: "Probe status narratives against live system state before accepting. Narrative-vs-state audit for web routing, MCP surfaces, agent registrations, and SOT"
tags: [audit, probe, trust-but-verify, caddy, mcp, navigation, narrative-vs-state]
triggers:
  - "audit this"
  - "100% pass"
  - "zero dead links"
  - "EXECUTED, AUDITED & DEPLOYED"
  - "PLAN ID"
  - "narrative claim"
  - "verify deployment"
  - "navigation audit"
  - "site audit"
  - "deploy receipt audit"
  - "SOT audit"
  - "audit and validate this claim"
  - "validate this claim"
  - "architectural audit"
  - "strategic evaluation"
  - "external audit"
  - "deployment audit"
  - "delegate agent"
  - "subagent"
  - "verify agent claims"
  - "authority recovery"
  - "apex scalars"
  - "G-fold"
  - "UNMEASURED"
  - "hardcoded stub"
  - "live-fetched"
  - "health endpoint wiring"
  - "verbosity trimming"
  - "response pipeline"
  - "apex scalars missing"
  - "MCP response minimal"
  - "direct call vs MCP call"
  - "trim_for_verbosity"
  - "cross-witness"
  - "dual agent"
  - "convergence"
  - "audit claims against live"
  - "autonomous deployment"
  - "completion report"
  - "autonomous AGI"
  - "all gaps closed"
  - "what is"
  - "do we have"
  - "is there a"
  - "deep scan"
  - "scan internal"
  - "can we test all"
  - "existence check"
  - "is this alive"
  - "is this wired"
  - "verify and identify gaps"
  - "capability metabolism"
  - "ephemeral pipeline"
  - "dormant subsystem"
---
# Live Probe Audit Pattern

## The Tell

When a session-feed narrative declares completion with confident numbers ("100% OK", "Zero dead links", "all 91 URLs pass"), the numbers are usually inflated by 20-40% relative to reality. Reasons:
- "URL count" often counts references across all surfaces including duplicates, not unique paths
- "Asset hash fixed" usually means file changed, not Caddy/config reloaded
- "All surfaces wired" usually means 5 of 8 surfaces, missing the rest
- "Discovery files fixed" usually means files added to disk, not routing config wired

**Rule: never trust the preamble, always probe the count.**

## Classify the Report Type FIRST

Not all agent reports are audited the same way. Classify before probing — over-probing a doctrine report wastes effort, under-probing a deployment report misses the lies.

| Report type | Falsifiable surface | Primary probes |
|---|---|---|
| **Deployment / hotfix** ("I changed X, now Y works") | Config files, mtimes, process env, live HTTP, service state | `stat` mtime vs backup, `/proc/<pid>/environ`, `curl :port/health`, diff backup→current |
| **Spec / advisory** ("you should build X, here are references") | Citations + named estate files | curl each cited URL + grep the specifically-claimed terms; `find`/`grep` each named file for existence AND implementation depth |
| **Doctrine / synthesis** ("here is the framework, ratify it") | THIN — mostly unfalsifiable prose | Audit only the concrete anchors: do the named "patterns" map to real findings? Are citations reused correctly? Is the gap/eureka list honest about what it doesn't know? |

**Rule:** the more a report is wisdom-literature, the less there is to probe — the audit becomes "are the concrete anchors real?" Do NOT fabricate audit surface for a doctrine report; report the thin surface honestly.

## Gap-Claim Audit ("you are missing X")

When an external advisor (Copilot, a peer agent, an external audit) claims your estate is MISSING a control, probe the estate for existing primitives BEFORE accepting the gap. Advisors without filesystem visibility systematically overstate gaps — they search their own index (M365, their RAG), find nothing, and assume absence.

Proven 2026-08-02: a Copilot report claimed "your agents are still missing 10 controls." Live probe: 4 of 10 already existed, richer than the proposal (independent-witness machinery in `witness_packet.py`; verdict enum in `verdicts.py` with HOLD_888/PROVISIONAL substates; evidence-freshness TTL in `attestation_verifier.py`; human-approval = the constitutional floors). Only ~1.5 of 10 were genuinely missing.

**Discriminator:** for each claimed gap, `grep -rl` the estate for the capability's conceptual name. If a primitive exists, the gap is "not wired into THIS workflow" (a real but smaller finding), not "absent" (the advisor's framing). Report the delta: "label is new, substance exists."

## Component / Server Existence Scan ("is there an X on this box?")

**Signal:** The sovereign asks "what is X", "do we have X", or "can we test all X" about an internal component — especially an MCP server, organ, daemon, or subsystem. The fast answer from prior/context ("there is no X") is the trap.

**Scar (2026-08-02):** Arif asked "what is HERMES MCP and can we test all." I answered from context that no product named "Hermes MCP" exists — only Hermes Agent (the MCP *client*) plus six wired organ servers. Arif pushed: "so there is no hermes mcp?" I doubled down. He said "u deep scan internal." A four-surface scan found `/root/.hermes/mcp_servers/hermes_mcp.py` — a live standalone MCP server on port 18086, 7 governance tools, running as a process, but **disabled** in `hermes mcp` config so it never appeared in my toolset. The absence claim was false. Two wasted turns.

**The four-surface scan (run all four before ANY existence verdict):**

```bash
# 1. CONFIG / TOOLSET SURFACE — what the agent framework has wired
hermes mcp 2>&1                       # enabled AND disabled custom servers
grep -rniE 'mcp|server' /root/.hermes/config.yaml | head

# 2. FILESYSTEM SURFACE — what exists on disk, wired or not
find /root/.hermes /opt /root -path '*/mcp*' -name '*.py' 2>/dev/null | grep -v venv | head -20

# 3. PROCESS SURFACE — what is actually running
ps aux | grep -iE 'mcp|arifos|geox|wealth|well|mage|hound' | grep -v grep

# 4. PORT SURFACE — what is bound and listening
ss -tlnp 2>/dev/null
```

**Discriminators:**
- **Toolset visibility ≠ existence.** A server can be live (process + port) yet absent from the agent's toolset because it is `disabled` in config, quarantined (`stdio_mcp_quarantine` in config.yaml), or never wired. "Not in my tools" is a statement about *my wiring*, not about the box.
- **Disabled ≠ dead.** A `custom — disabled` entry in `hermes mcp` can still be a running process serving real requests over HTTP. Probe the port before calling it dead.
- **Answer internal "what is X / do we have X" from the SCAN, never from prior.** Priors are for external facts; the live box is the authority for internal inventory.

**Verdict rule:** an absence claim ("no X exists") requires all four surfaces probed clean. A presence claim needs only one surface. Same asymmetry as the truncated-read pitfall below — absence is the expensive claim to prove.

Worked example + the 7-tool test recipe: `references/hermes-mcp-deep-scan-2026-08-02.md`.

## Invariant-Preservation Audit ("slim context" / "zero information loss" claims)

**Signal:** A report claims a compression, pruning, or slimming win — "context compiler", "slim AGENTS.md", "compiled boot", "zero information loss for the task at hand", RAG pruning, prompt compaction. The headline numbers (token reduction %, build time) are usually real. The danger is never in the reduction number — it is in **what the compression silently dropped**.

**Scar (2026-08-03):** A Federation Context Compiler report claimed "2,930 bytes of context instead of 31,298... zero information loss." Live probe of the generated boot doc: the constitutional floors table had **10 floors, not 13** — F3 TRI-WITNESS, F5 PEACE², F12 RESILIENCE were silently dropped from the generator's hardcoded template. An agent booting on that doc would operate without injection defense (F12, HARD) and tri-witness (F3). The compression engine itself was genuinely good (80-90% reduction verified live); the loss was in the "always include" template, not the compiler. Irony: F3 tri-witness is exactly the mechanism that caught the loss — the independent witness probing the builder's claim.

**The rule: compressible vs invariant.** Every system has content classes that MAY be reduced (organ tool surfaces, secondary docs, detail sections) and content that must NEVER be compressed away (constitutional floors, identity/authority anchors, the "one rule", probe-before-act discipline, shell init). A "zero loss" claim is FALSE the moment ANY invariant-class item is absent from the compiled artifact — no matter how good the reduction numbers are.

**Probe recipe (run on the GENERATED artifact, never on the report's numbers):**

```bash
# 1. Generate the actual compiled output
bash /root/A-FORGE/scripts/context_boot.sh --write /tmp/boot_test.md "<task>"

# 2. Count invariant items in artifact vs canonical source
grep -E '^\| F[0-9]+' /tmp/boot_test.md | awk '{print $2}' | tr '\n' ' '
grep -E '^\| \*\*F[0-9]+\*\*' /root/AGENTS.md   # canonical floor list
# Expect identical floor sets. Any missing floor = constitutional amnesia.

# 3. Check other invariant classes survived
grep -c "ONE RULE\|One Rule" /tmp/boot_test.md
grep -c "Probe before act" /tmp/boot_test.md
grep -c "888_HOLD\|HOLD" /tmp/boot_test.md

# 4. Verify size/line claims against disk, not the report
wc -c /tmp/boot_test.md /root/AGENTS.md
wc -l /tmp/boot_test.md   # 2026-08-03: report said "214 lines", disk said 84
```

**Discriminators:**
- **Reduction number true ≠ lossless.** Report the two halves separately: "engine verified (80% reduction, sub-ms) [OBS]" AND "losslessness claim FALSE — 3 floors dropped [OBS]". Never let a good headline number launder a broken invariant set.
- **The loss lives in the template, not the algorithm.** Slim-doc generators hardcode their "always include" blocks. Audit the hardcoded block in the generator script, not just one output — the output shows today's drift; the template shows tomorrow's too.
- **Fix is additive and cheap.** Restoring dropped invariants costs a few hundred bytes and barely dents the ratio (2,913 → 3,142 bytes here, still ~90% reduction). There is never a real trade-off between slim and constitutional — say so when reporting the fix.
- **Receipt counts need a countable artifact.** "43 receipts / metabolic cycle complete" with no locatable receipt store = [SPEC]. Probe the claimed storage path before endorsing.
- **Self-explained anomalies stay unverified.** "FQ=1.22 OVERHEAT is a sub-ms timing artifact" is the builder's own interpretation of its own number — label it [INT], do not adopt the explanation as fact. A metric outside its declared range (FQ ∈ [0,1] reporting 1.22) is a clamp/normalization bug until proven otherwise — "timing artifact" is an excuse, not a diagnosis. Fix the metric; don't narrate it.
- **Reduction % vs a hardcoded baseline is benchmark theater.** (PROVEN 2026-08-03) The compiler's "naive full-dump = 34,000 tokens" was `FULL_LOAD_BASE_TOKENS = ***` — a constant in source, never measured. The compiled side was real; the reduction % was relative to an assumption. Before citing any reduction ratio, grep the source for the baseline constant (`grep -n "naive\|BASE.*TOKENS" <compiler>.py`). If the baseline is assigned rather than computed, the ratio is unverifiable — measure the actual full load (all tool schemas + skills catalog + docs, token-counted) before endorsing. A v2 that fixes the doc side while leaving the baseline hardcoded has not addressed the benchmark gap.
- **Attention reduction ≠ access reduction.** (PROVEN 2026-08-03) A slim context doc reduces what *tempts* the model (attention), but excluded tools stay CALLABLE if their MCP server is still wired — the schemas load regardless of what the doc says. "Tool not present = can't be called wrong" is only true with runtime schema gating (e.g. Hermes cron `enabled_toolsets`), not doc-slimming. Audit both layers: the doc (attention) and the wired schema (access). Doc compile = half the mechanism; schema gate = the other half. Likewise "N× faster" latency claims are [DER] until measured — prefill scales with token count, but never cite a multiplier without a benchmark on this stack.
- **Canary for compressed-context rollout must include a cross-organ task.** A single-organ canary only proves the easy case — the failure mode of a context compiler is tasks touching two organs (both halves need Tier 1). Binary canary criteria: (1) routing hit without hints, (2) missed dependency — and did the on-demand route (`arif_route`) rescue it, (3) quality regression vs full-context run of the same task. If all canary tasks are single-organ, the canary is unfalsifiable for the real risk class.

Full worked example: `references/context-compiler-zero-loss-audit-2026-08-03.md`.

## Architecture-vs-Liveness Audit ("is this subsystem alive?")

**Signal:** A report (or Arif) claims a subsystem exists with impressive architecture — state machines, gates, leases, sandboxes, promotion pipelines. The question is not "do the files exist?" but "is any agent actually using this end-to-end?"

**Scar (2026-08-02):** Arif shared an external agent's Eureka narrative about A-FORGE's ephemeral capability pipeline. The narrative was architecturally correct — 20+ real files, 1,100+ line canonical engine, bwrap sandbox, 10+ tests, 5 built-in templates, evidence-based promotion gate. But the system was operationally dormant: zero production calls, no agent configured to invoke it, and the promotion gate was mathematically unreachable (score defaults to 0.0, threshold requires 0.80, the code that populates the score isn't wired).

**The 10-question liveness probe (run ALL before any "it works" verdict):**

```
Q1. Does the tool appear in the live MCP surface?
    → grep registration in core.ts / server setup; check tools/list

Q2. Are the domain files real implementations or stubs?
    → wc -l each file; check for actual logic vs print/banner stubs
    → (see deployment-claim-verification pitfall #31 for stub detection)

Q3. Is the sandbox/execution backend actually installed?
    → which bwrap; bwrap --version; testBackend() equivalent

Q4. Do templates/recipes exist and are they usable?
    → grep registerBuiltinTemplates / seedTemplates; count entries

Q5. Is there test coverage?
    → find test/ -name "*ephemeral*" -o -name "*sandbox*" etc.

Q6. Is any agent CONFIGURED to call this tool?
    → grep -rn "tool_name" ~/.hermes/ ~/.claude/ ~/.opencode* /root/HERMES/
    → This is the most commonly missed check. A tool nobody calls is dormant.

Q7. Are promotion/retirement gates mathematically reachable?
    → Read the threshold constants AND the default values of their inputs.
    → If input defaults to 0.0 and threshold requires 0.80, and the code
      that populates the input says "P2; defaults to 0.0 until then" —
      the gate is DEAD BY CONSTRUCTION. No entity can ever pass it.

Q8. Are cross-module dependencies actually wired?
    → grep -rn "import.*ModuleB" ModuleA.ts
    → A file can exist with beautiful spec but zero imports from the
      canonical engine. Existence ≠ integration.

Q9. Is the MCP transport network-reachable or stdio-only?
    → ss -tlnp | grep <port>; ps aux | grep <process>
    → stdio transport = library waiting to be spawned, not a live server.

Q10. Has the full lifecycle ever been exercised end-to-end?
    → Search logs, session history, VAULT999 for any production invocation.
    → "No permanent promotion test yet" = the promote→seal path is theory.
```

**Three dormancy patterns (proven 2026-08-02):**

| Pattern | Tell | Example |
|---------|------|---------|
| **No consumer** | Tool registered, zero agent configs reference it | forge_ephemeral not in any Hermes/Claude/OpenCode config |
| **Dead gate** | Threshold requires X, input defaults to 0, populator says "P2" | empirical_capability_score=0.0 forever, threshold=0.80 |
| **Unwired module** | File exists, canonical engine doesn't import it | worldModelTraining.ts + multiModelEvaluator.ts: grep returns zero imports from EphemeralGenesis.ts |

**Verdict template:**

```
Architecture: REAL / STUB / PARTIAL
  [evidence: file count, line count, test count]

Operationally: LIVE / DORMANT / PARTIAL
  [evidence: production calls, agent configs, gate reachability]

Gates: REACHABLE / DEAD BY CONSTRUCTION
  [evidence: threshold vs default value, populator wiring status]

Cross-module wiring: WIRED / UNWIRED
  [evidence: grep imports between modules]
```

**Key discriminator:** "Architecture real, operationally dormant" is a VALID and COMMON verdict. Don't collapse it to "it works" (files exist) or "it's fake" (nobody uses it). Report both halves honestly.

Full worked example: `references/aforge-ephemeral-liveness-audit-2026-08-02.md`.

## Probe Order (Mandatory)

```bash
# 1. Sample 10 random surface URLs
for path in /a/ /b/ /c/; do
  curl -sf -m 5 -o /dev/null -w "%{http_code} %{url_effective}\n" "https://example.com${path}"
done

# 2. Extract all internal hrefs from rendered HTML (not static docs)
curl -sf -m 10 example.com > /tmp/audit/index.html
python3 -c "
import re
with open('/tmp/audit/index.html') as f:
    hrefs = re.findall(r'href=\"([^\"#]+)\"', f.read())
internal = {h for h in hrefs if h.startswith('/') and not h.startswith('//')}
for h in sorted(internal): print(h)
"

# 3. For each unique internal href, probe HTTP code (sample, not all if huge)
# 4. Distinguish real asset URLs from directory listings
#    /assets/specific.css returns 200 (real)
#    /assets/ alone returns 404 (directory listing, false positive)

# 5. Check filesystem for files that exist but route 404 (Caddy bug signal)
ls /var/www/html/.well-known/<path>
curl -sf -m 5 -o /dev/null -w "%{http_code}\n" "https://example.com/.well-known/<path>"
# If file exists on disk + returns 404 → handler routing bug, not missing file

# 6. Bypass Cloudflare/CDN for ground truth
curl -sf -m 5 -k --resolve "example.com:443:127.0.0.1" https://example.com/.well-known/<path>
# 404 from Caddy-direct = server-side bug, not edge cache
```

## The Trust-But-Verify Scoring Template

After probes, produce an honest verdict per claim with epistemic tag.

| Surface | Status | Evidence |
|---|---|---|
| /wealth/, /gold/, /oil/, /gas/, /geox/ | nav wired (OBS) | grep market-map-bar = 2 refs |
| /well/, /writings/, /makcikgpt/ | nav MISSING (OBS) | grep returns 0 refs |
| `/.well-known/{file}` | 404 (file exists on disk) (OBS) | Caddy handler order |

**Real numbers over vibes.** When narrative says "100%" and probe shows "70%", report "70%, not 100%." Don't add qualifiers like "largely complete" or "essentially done." Plain numbers are the F2 TRUTH floor.

## Common Drift Patterns

### Caddy routing for `/` and `/.well-known` cross-roots

When `@well-known` is a catch-all handler matching first in `/etc/caddy/Caddyfile`, AND there are second-pass handlers like `@observatory_discovery` for specific paths in different roots, paths in the second root will 404 even though file exists.

Fix is 888_HOLD (production web routing): reorder handlers in `/etc/caddy/Caddyfile` so cross-root dispatch happens before catch-all.

### AAA pre-commit secret scanner pattern

The AAA repo's pre-commit hook does pattern-scan for API key formats (Telegram / GitHub / generic). If a commit contains config referencing key patterns (even non-secret descriptions), it **times out / blocks the commit** instead of failing clean.

```bash
# Symptom: commit hangs/times out at pre-commit stage
# Fix:
git commit --no-verify -m "..."
# This is the documented emergency escape hatch in the hook script:
# Skip: git commit --no-verify (emergency only SABAR)
```

**Real key placement:** source the API key from `/root/.secrets/vault.env` at runtime, do NOT embed in committed config.

### Asset path drift: `/assets/` vs `/_shared/`

If audit claims fixed `assets/index-HASH.css`, verify the actual file path. Real path may be `/var/www/html/<service>/assets/...` while the web root is `/var/www/html/<other>/_shared/...`. Caddy serves via try_files; some paths redirect fine, some don't.

### Live-vs-disk byte delta behind a CDN/WAF (scar 2026-08-04)

On a Cloudflare-fronted site, if live `curl | wc -c` differs from the disk SOT file by ~1KB, **diff before declaring corruption** — the delta is usually edge injection. Cloudflare appends `<script>window.__CF$cv$params={r:...,t:...}` + the challenge-platform loader (~938B observed on arif-fazil.com's `/_shared/unified-header.html`). Recipe: save live to /tmp, `diff` against disk, read the hunks. Delta is CF/turnstile/challenge script → verdict CLEAN, injection accounted for. Related: an absence claim ("file not on disk") must be probed against EVERY webroot in the Caddyfile — `/_shared/*` serves from `/var/www/html/_shared` while the main site is `/var/www/html/arif`; `find` under the wrong root proves nothing. And a grep hit for a scary pattern ("self-reference") gets a nature-check by reading the hit line — the SELF-REF=1 hit was a benign HTML comment, not a script self-loop. Worked example: `arif-sites-content-ops` → `references/webroot-cf-audit-2026-08-04.md`.

### Agent registration gates

When audit claims "external agents registered in AAA":
1. Check `/root/AAA/agent-skill-binding-map.md` for the row
2. Check `/root/AAA/agents/_external/<name>/agent-card.json` exists
3. Run the agent's binary: `<binary> --version` to verify install

A claim of "registered" may satisfy one of these without the others.

### DeepSeek BYOK Anthropic endpoint (verified 2026-07-19)

DeepSeek exposes an Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`. Wire pattern for any agent that accepts Anthropic-format env vars:

```bash
export COPILOT_PROVIDER_TYPE=anthropic
export COPILOT_PROVIDER_BASE_URL=https://api.deepseek.com/anthropic
export COPILOT_PROVIDER_API_KEY=sk-<deepseek-key>
export COPILOT_MODEL=deepseek-v4-pro    # or deepseek-v4-flash
export COPILOT_PROVIDER_MAX_PROMPT_TOKENS=840000
export COPILOT_PROVIDER_MAX_OUTPUT_TOKENS=128000
```

Verified agents that consume this pattern: GitHub Copilot CLI (`@github/copilot`), Hermes, opencode, claude-code, kilocode, workbuddy, openclaw, gemini-cli, deepcode, nanobot, crush, pi_mono, reasonix, langcli (17 agents per DeepSeek docs sidebar `agent_integrations/`).

**Critical caveat:** Must use provider_type=`anthropic`. `openai` type triggers HTTP 400 `reasoning_content in thinking mode must be passed back to the API` because DeepSeek requires reasoning_content echo on subsequent requests, which Copilot CLI's OpenAI integration does not support.

Verified live: `copilot -p "hello from deepseek via copilot cli"` returned exact match (18s, 141k tokens).

## Verdict Contract

When reporting audit findings:
- Pass: with evidence (probed URL + response code)
- Fail: with **path + root cause** (not just "404")
- Partial: with what's there + what's missing

For each claim in the original narrative, state its true status with epistemic tag (OBS = direct probe, INT = inferred, DER = derived).

```
Layer A APEX fingerprint              Active — G score, C_dark shadow state, &
                                       organ conservation aktif.

Reality:
[OBS] Verified live — Layer A fingerprint rides on tool responses
[OBS] The quote registry Layer A math computes G per resolve
```

## Autonomous Deployment Verification — FQ, Carry-Forward & Goal Probes

**Signal:** Another agent (OpenCode, 333-AGI, or any autonomous lane) returns a session completion report with banners like *"All Gaps Closed"*, *"FQ BALANCED"*, *"Autonomous AGI Execution — All Gaps Closed"*, or specific counts (*"7/7 organs, 14 receipts, 6 cycles"*).

**Do NOT trust the banner without probing these autonomous-specific surfaces:**

```bash
# 1. FQ — probe arifFLOW directly, not the report
curl -s http://127.0.0.1:7073/health | python3 -c "
import json,sys
d = json.load(sys.stdin)
fq = d.get('fq', {})
print(f'FQ: {fq.get(\"quotient\",\"?\")} ({fq.get(\"verdict\",\"?\")})')
print(f'Execute:Verify = {fq.get(\"execute_count\",0)}:{fq.get(\"verify_count\",0)}')
print(f'Trend: {fq.get(\"trend\",{}).get(\"direction\",\"?\")} @ {fq.get(\"trend\",{}).get(\"rate_per_min\",\"?\")}/min')
print(f'Worst actor: {fq.get(\"worst_actor\",\"?\")}')
"

# 2. carry_forward.json — check actual open loops
python3 -c "
import json
try:
    d = json.load(open('/root/.local/share/arifos/carry_forward.json'))
    loops = d if isinstance(d, list) else d.get('open_loops', d.get('goals', []))
    pending = [l for l in loops if l.get('status') not in ('completed','resolved','sealed')]
    print(f'Total loops: {len(loops)}, Pending: {len(pending)}')
    for p in pending[:5]:
        print(f'  🔴 {p.get(\"id\",\"?\")}: {p.get(\"title\",\"?\")[:80]}')
except Exception as e: print(f'carry_forward.json: {e}')
"

# 3. goal_registry.json — check completion vs pending
python3 -c "
import json
try:
    d = json.load(open('/root/AAA/state/goal_registry.json'))
    goals = d.get('goals', [])
    pending = [g for g in goals if g.get('status') != 'completed']
    print(f'Goals: {len(goals)-len(pending)} completed, {len(pending)} pending')
    for p in pending:
        print(f'  ⏳ {p.get(\"id\",\"?\")}: {p.get(\"title\",\"?\")[:60]} ({p.get(\"progress_pct\",0)}%)')
except Exception as e: print(f'goal_registry.json: {e}')
"
```

**Common autonomous deployment overclaim patterns (proven 2026-07-29):**

| Claim | What to Probe | Expectation |
|-------|---------------|-------------|
| "FQ 1.50 BALANCED" | `curl :7073/health \| jq .fq` | May be stale — FQ moves every AED cycle. Actual could be 9.88 OVERHEAT. |
| "All gaps closed" | carry_forward + goal_registry | Usually 3-4 pending. Report counts "infrastructure laid" as "gap closed." |
| "Autonomous AGI" | Check git for 888_HOLD records | Usually bounded autopilot. No T3 ratification exists. |
| "X cycles completed" | `journalctl -u aed.service \| grep -c 'SUCCESS'` | Low-risk claim, usually correct. |
| "7/7 organs" | `for p in 8088 7071 3001 8081 18082 18083 7073; do ...` | Usually correct — thyroid-level metric. |

**FQ Overheat Diagnostic (proven 2026-07-29):**

AED fires every 5 min. Each cycle runs SENSE→EXECUTE→VERIFY→SEAL. EXECUTE + SEAL both push the execute counter. If VERIFY doesn't keep pace (SEAL counts as execute), ratio climbs → FQ spikes.

```bash
curl -s :7073/health | jq '.fq.by_actor | to_entries[] | select(.value.fq >= 8) | {actor: .key, fq: .value.fq}'
```

When AED itself is the dominant consumer, the system is heating itself — thermodynamic irony. Fixes:
- Separate AED metabolism from FQ pipeline (AED = infrastructure cost, not execution debt)
- Add verify step per cycle to balance execute:verify
- NOP: FQ may self-correct as verify events accumulate

**Template for autonomous deployment report audit:**

```
| Claim in report | Probe | Status | Epistemic |
|---|---|---|---|
| {banner claim} | {curl/python probe} | ✅/❌/⚠️ | OBS/INT |
```

Report the converged truth. Do NOT endorse "all gaps closed" when carry_forward shows pending items.

## Config/Env Wiring Claim Verification (secrets & provider receipts)

**Signal:** An agent delivers a receipt claiming "keys wired", "config fixed", "fallback chain diversified", "seats updated", "HERMES-SEAT-OK" — especially when its own file-mutation verifier warns a patch was refused.

**Proven 2026-08-01 (Qwen Token Plan seat wiring):** A 60%-accurate receipt. The claims that failed were exactly the ones a naive reader would accept:

| Claim | Probe | Verdict |
|---|---|---|
| "config.yaml modified" | `stat -c '%y'` mtime AFTER the claimed change + backup files present | ✅ TRUE — but via `hermes config set` CLI, NOT the refused patch tool. **mtime is the proof of modification, not the tool attribution.** Patch-tool refusal ≠ file unchanged. |
| "keys wired in vault" | read kunci-mas.env with masked values | ✅ TRUE (3× REAL sk-sp-*) |
| "21 models per seat" | `GET {base}/models` per key | ✅ TRUE (3×21) |
| "chat OK" (Pro seat) | `POST {base}/chat/completions` | ✅ TRUE |
| "HERMES-SEAT-OK" (Standard seat) | `POST /chat/completions` same key | ❌ FALSE — 429 ×4 (parallel AND serial). **Models-list 200 ≠ chat-completions OK. Test the exact operation claimed.** |
| "seats.yaml updated" | read seats.yaml seat-by-seat | ⚠️ PATCHED WRONG — an agent patch can contradict its own comment (marked seat A POPULATED while its comment said seat A still empty). Read the registry file record-by-record against the vault; never trust the patch summary. |
| "restart will pick it up" | `/proc/<pid>/environ` + `systemctl show -p EnvironmentFile` + launcher script `source` lines | ❌ FALSE — key absent from the process env chain. **Key in file ≠ key in process env.** The gateway sources a per-agent `runtime/.env`, not the vault. Restart alone was useless. See `federation-secret-vault` skill. |

**Discriminators learned:**
- **401 vs 429:** 401 = wrong key; 429 = key valid but throttled/quota-drained. Leaked-key quota drain kills the smaller seat first (Standard 25K before Pro 100K) — consistent with F11 chat-exposure incidents.
- **`export ` prefix parse trap:** dotenv files in `export KEY=value` format break naive `startswith('KEY=')` parsers → false "vault empty" alarm. Match `^(export )?KEY=`.
- **Process env is the truth, not the SOT file:** `PID=$(systemctl show <unit> -p MainPID --value); tr '\0' '\n' < /proc/$PID/environ | grep KEY` — readable as root, shows what the service actually holds at boot.
- **Two-token bot drift:** same bot, two token vars (`FORGE_BOT_TOKEN` works, `TELEGRAM_BOT_TOKEN` 401s); gateway code reads the config-referenced one (the dead one). On any token rejection, `getMe`-test EVERY token var in the env file.
- **`systemctl restart` may not replace the old PID** when `--replace` semantics conflict — verify MainPID changed; `kill -9` the stale one and restart.

### Agent Capability False Gate

**Pattern:** An agent refuses a task citing its config ("groupPolicy allowlist only has X", "I can't post to group Y"). Probe the FULL config before accepting the refusal:
- OpenClaw claimed it couldn't post to the AAA group citing `groups: {"-1003753855708": {}}` allowlist — but its own `bindings[]` table referenced the AAA group (`bindings[3].match.peer.id = -1004446358629`). The allowlist governs SEND permission; bindings are match rules; the agent conflated them and reflexively denied.
- A capability denial citing config is itself a claim — probe it. Check: allowlist vs bindings vs home_channels; which agent already holds send rights (Hermes cron delivered to AAA group daily while OpenClaw claimed it was unreachable).

Full worked example: `references/env-wiring-claim-audit-2026-08-01.md`.

## Cross-Witness Audit Protocol (proven 2026-07-28)

**Signal:** An agent (OpenCode, Claude, any subagent, or a peer) produces a deployment report, internal audit, or status assessment full of specific numbers, status flags, and severity ratings.

**The protocol — two agents, one truth:**

```
Agent A (scanner): Runs deep audit → produces claims + numbers + severity
Agent B (witness): Independently probes every claim against live state
                   → confirms true, corrects false, notes overclaim
Convergence:       Both agents agree → seal the converged truth
```

**Why this exists:** This session proved a single-agent internal audit is ~60% accurate on first pass. OpenCode (FI-001) produced a 7-layer audit with 14 findings. Hermes independently verified and found 3 of 8 core claims were false (MCP resources=0, vault silent 4 days, kernel F2 violation). The false claims were not malicious — they were interpretation errors, stale data, and missed nuance. Without the cross-witness, those 3 false claims would have been sealed as truth.

**Procedure when another agent sends an audit:**

1. **Extract all falsifiable claims** — numbers, boolean flags, severity labels, route statuses. Ignore narrative framing.
2. **Probe each claim independently** — do not re-read the agent's probe output. Use your own tools (curl, HTTP, MCP list, git log). The agent's probe is OBSERVATION, not TRUTH.
3. **Classify each claim:**
   - ✅ **Confirmed** — your independent probe matches the claim
   - ❌ **False** — your probe contradicts the claim outright
   - ⚠️ **Misread** — kernel of truth but interpretation is wrong (e.g., "kernel healthy + held = F2 violation" is actually correct constitutional behavior)
   - 📊 **Inflated** — numbers overstated by 10-30% (common: "327 resources" counts all skill:// noise as signal)
4. **Report the convergence:** Show which claims converged, which diverged. Label with epistemic tags.
5. **Seal the converged truth** — when two independent agents agree, the finding is no longer CLAIM, it is TRI-WITNESS evidence (F3). Append to VAULT999 naming both agents.

**Convergence template:**

| Claim | Agent A | Agent B (witness) | Verdict |
|-------|---------|-------------------|---------|
| Drift exists | True | True (curl /health) | ✅ CONVERGE |
| MCP resources=0 | True | False (list_resources → 34) | ❌ FALSE |
| Vault silent 4 days | True | False (3 seals today) | ❌ FALSE |

**Pitfall:** Do NOT delegate the cross-witness to a subagent. The cross-witness must be YOU probing live state directly. Subagents are themselves single-agent audits and need their own cross-witness.

**Session close:** When a peer agent sends END_SESSION / WITNESS_NULL / "Standing down" markers after convergence, respond with a one-line acknowledgment and stop — do not reopen probes, do not re-litigate settled claims, do not treat ⏸️ pings as new tasks. Silence after close is the correct state. (Proven 2026-08-04: the AGI lane sent ~8 END_SESSION markers post-convergence; each got a one-line ack, zero new work. Reopening a closed audit is itself a drift event.)

### Resource Count Inflation Detection

**Pattern:** When an agent claims an MCP resource count, they may count every `skill://` entry even though those are filesystem mirrors, not operational data. Signal: claimed count >> expected operational resources.

**Detection:** Via MCP `resources/list`, count `arifos://` + `tree777://` URIs only. Expected ~34 resources (doctrine, atlas333, vitals, wisdom, 1 skill://index). Not 294 skill:// static entries (collapsed to 1 index + 1 template on 2026-07-28).

### Convergence Sealing

When two independent agents converge on the same finding, the evidence is stronger than either alone (F3 WITNESS). Seal immediately recording both agents and the converged finding.

### Temporal FQ Self-Correction (proven 2026-07-29)

FQ readings are temporal snapshots. A report claiming "FQ 1.50 BALANCED" at T₀ may show FQ 9.88 OVERHEAT at T₁ (+15 min), or self-correct back to BALANCED at T₂ (+30 min). Mechanism: AED cycles push execute counters with every SENSE→EXECUTE→VERIFY→SEAL pass — both EXECUTE and SEAL increment the execute side of the ratio. If verify events haven't accumulated yet, the ratio skews high temporarily. As later verify events fill in, the ratio rebalances.

**Probe pattern:**
```bash
# T₁ probe — do this immediately upon receiving a report
curl -s :7073/health | jq '.fq | {quotient, verdict, execute_count, verify_count, trend}'

# Check the trend direction
curl -s :7073/health | jq '.fq.trend | {direction, rate_per_min, samples}'
```

**Rule:** Always compare report-time FQ against probe-time FQ. If they differ, name the delta in your audit. Don't trust either reading as single truth — report the converged window.

## Agent-Card Federation Alignment Audit

**Signal:** An agent-card.json (A2A standard or arifOS v2.2.0) needs verification against live federation reality. The card declares skills, MCP surfaces, identity attributes, and topology bindings — each must be probed against the actual running system.

**The tell:** Agent cards drift systematically because they are forked from templates and updated episodically. MCP endpoints add/remove tools, organs get added to the federation, canonical skill sets get consolidated — but the agent card stays frozen at fork time.

### Probe order (mandatory)

```bash
# 0. Source the agent card
AGENT_ID="openclaw"  # or whatever agent
CARD="/root/AAA/agents/${AGENT_ID}/agent-card.json"

# 1. Extract all skill IDs — both objects and bare strings
python3 -c "
import json
with open('$CARD') as f:
    card = json.load(f)
skills = card.get('skills', [])
named = set()
for s in skills:
    if isinstance(s, dict): named.add(s['id'])
    elif isinstance(s, str): named.add(s)
print('\\n'.join(sorted(named)))
"

# 2. Probe all MCP endpoints for health + tool count (parallel)
for port in 8088 7071 7072 3001 8081 18082 18083 7073; do
  echo "=== :${port} ==="
  curl -sf "http://127.0.0.1:${port}/health" 2>/dev/null \
    | python3 -c "
import json,sys
d = json.load(sys.stdin)
t = d.get('tools_loaded') or d.get('public_tools') or d.get('tool_count') or d.get('stateless_tools') or '?'
print(f'health=ok tools={t}')
" 2>/dev/null || echo "UNREACHABLE"
done

# 3. Get actual tool names from arifOS kernel
curl -sf http://127.0.0.1:8088/tools | python3 -c "
import json,sys
d = json.load(sys.stdin)
for t in d.get('tools',[]): print(t['name'])
" 2>/dev/null > /tmp/live_tools_8088.txt

# 4. Cross-reference declared skills against canonical skill set
ls /root/.hermes/skills/*/SKILL.md 2>/dev/null | while read f; do
  basename "$(dirname "$f")"
done > /tmp/canonical_skills.txt
echo "Canonical count: $(wc -l < /tmp/canonical_skills.txt)"

# 5. Check for bare-string skills that duplicate objects
python3 -c "
import json
with open('$CARD') as f:
    card = json.load(f)
skills = card.get('skills', [])
objects = {s['id'] for s in skills if isinstance(s, dict)}
strings = {s for s in skills if isinstance(s, str)}
dupes = objects & strings
orphans = strings - objects
if dupes: print(f'DUPLICATE bare strings: {dupes}')
if orphans: print(f'ORPHAN bare strings (no object): {orphans}')
if not dupes and not orphans: print('No bare-string issues')
"

# 6. Check federation topology for organ coverage
python3 -c "
import json
with open('$CARD') as f:
    card = json.load(f)
endpoints = {e.get('url','') for e in card.get('mcp_surface',{}).get('endpoints',[])}
expected_ports = ['8088','7071','7072','3001','8081','18082','18083','7073']
for port in expected_ports:
    found = any(port in ep for ep in endpoints)
    if not found: print(f'MISSING organ on port :{port}')
"
```

### What to check (7 dimensions)

| # | Dimension | What to probe | Failure signal |
|---|-----------|---------------|----------------|
| 1 | **Skill references** | All skill IDs in the card vs canonical `.hermes/skills/` | Orphan IDs, deprecated names (e.g. KERNEL-quantum-runtime, KERNEL-qubit-substrate) |
| 2 | **MCP tool lists** | Each declared endpoint's tool list via `curl :port/tools` | Tool count mismatch, non-existent tools listed, missing real tools |
| 3 | **Organ coverage** | Card's `mcp_surface.endpoints` vs `/root/AGENTS.md` §1 (7 organs) | Missing organs (e.g. arifFLOW :7073), extra phantom ports |
| 4 | **Intelligence tier** | Card's `warga_binding.intelligence_tier` vs agent's own AGENTS.md | Contradiction (card says ASI but own docs say AGI) |
| 5 | **A2A contract bindings** | `a2a_transport.endpoint` and `mcp_binding` vs live `curl` | Dead endpoint, wrong protocol, stale auth |
| 6 | **Floor bindings** | `floor_scope` on skills vs current F1-F13 from `/root/AGENTS.md` §6 | Wrong floor numbers, references to deprecated floors |
| 7 | **Schema compliance** | Duplicate fields, empty keys, version mismatches | `"": "value"`, duplicate `securitySchemes`/`security_schemes` |

### Findings report structure

Each finding MUST carry:

- **Severity** — 🔴 CRITICAL (orphan/deprecated/contradiction) / 🟠 HIGH (stale data) / 🟡 MEDIUM (cosmetic/gap) / 🔵 LOW (schema)
- **File:line** — exact location in agent-card.json
- **Card claim** — what the card says
- **Live reality** — what the probe found with [OBS] tag
- **Recommended action** — specific edit for the sovereign to approve

Report template:

```
## N. 🔴 CRITICAL: [Category]

**File:** agent-card.json, line L

| Card claim | Live reality |
|------------|-------------|
| {what card says} | {what probe found} [OBS] |

**Action:** {specific edit}
```

### Known pitfalls

- **Bare-string skills lack metadata.** When a consumer iterates the `skills` array, an object (with `id`/`name`/`description`/`floor_scope`) and a bare string appear as different entries. The bare string carries no metadata and is useless for A2A contract evaluation. Flag every bare string.
- **Topological roles are APEX residuals.** A card with `topological_role: "Metabolizer"` is carrying over APEX-theory taxonomy. Update to current organ name.
- **Tool counts inflate over time.** A card written when GEOX had 35 tools will claim 35 forever. Always probe the live count.
- **`kernel_skills` array is often stale.** Skills canonical at fork time get consolidated or renamed. Check every entry against disk.
- **Agent cards are NOT `.hermes/skills/` files.** An agent-card skill entry is an A2A capability declaration; a SKILL.md is a procedural recipe. Don't flag a card for missing a SKILL.md — only flag orphan string references that don't match any declared object.
- **Intelligence tier and warga lane must be consistent.** If the agent's own AGENTS.md says "AGI-level operator" but the card says `intelligence_tier: "ASI"`, that's a contradiction the card needs to resolve.

### Worked example

The canonical OpenClaw audit (2026-07-29) is at `references/agent-card-federation-alignment-2026-07-29.md`:
- 12 findings across 5 categories
- 3 CRITICAL (orphan skills, deprecated kernel refs, duplicate bare strings)
- 4 HIGH (all 5 MCP tool lists wrong, intelligence tier contradiction, missing arifFLOW organ)
- Each finding maps to a diff-ready edit on the agent-card.json

## Pitfalls

- **Truncated-read false negatives — the most dangerous verifier error class (scar 2026-08-02).** A verifier claimed "NO custom_providers.litellm entry" in a 1328-line config.yaml. The block was at lines 1279-1291. The verifier read only the first ~80 lines (`cat | head -80`) and concluded absence. This triggered a false F2/F11 HOLD that wasted a full audit cycle. **Rule:** when a verifier claims a block is ABSENT from a file, check the file's total line count (`wc -l`) against the verifier's read window. If the file is longer than what was read, the absence claim is UNVERIFIED, not TRUE. Always re-probe with `grep -n <term> <file>` (full-file search) before accepting any "not found" verdict. Absence claims require full-file evidence; presence claims only need one match.

- **Never trust "N URLs all 200" without the URL list.** Audit script may include anchor tags, javascript: URLs, mailto: links, fragments (#) in its pass count.
- **Delegate agent claims about code must be grep-verified before forwarding to the user (scar 2026-07-19).** Subagents can fabricate detailed architectural findings (specific line numbers, named patterns, "three parallel paths") that don't exist in the actual source. Always verify at least one key claim with grep/curl before presenting a subagent's analysis as fact. See `references/delegate-agent-audit.md` for the full recipe.
- **When two subagents report different tool counts / version numbers / branch states, trust the live health endpoint, not the agent prose.** Subagent contexts diverge. Health endpoint + git log are the reconcilers.
- **Vision vs. reality — agent-described architecture ≠ deployed code (scar 2026-07-20).** When an agent (Forge, OpenCode, any subagent, or yourself) vividly describes a system feature with architecture, naming, and flow — probe the codebase before discussing it as real. The tell: compelling prose about something you can't grep. Pattern: Forge described PRL (Precedent Retrieval Layer) with full dual-gate architecture, τ ≥ 0.95, blast_radius filtering, Qdrant integration — as if it existed. `grep -r "prl\|PrecedentRetrieval" /root` returned zero code matches. Arif's correction: "Do we have this? Do I need to remember it?" Translation: **if it's not in the code, don't describe it as built.** Probe first: `search_files` for the name, check the tool registry, curl the health endpoint. Vision = blueprint. Reality = code. Don't conflate them, even when the vision is architecturally correct.
- **S24 passive sensor unreachability is industrial SCADA logic, not an outage (scar 2026-07-24).** When the S24 Sovereign Sensing Node times out on direct HTTP probe, do NOT frame it as "Termux asleep — expected Android behavior." The correct framing: S24 is a passive sensor in a data diode architecture — it collects data when polled by the central brain (FORGE cron), sleeps between cycles, and never initiates connections. Check the telemetry JSONL (`/root/arifos-memory/telemetry/s24_history.jsonl`) for the last successful entry rather than relying on a live probe. This is industrial telemetry applied to a smartphone, not a consumer app failing to stay awake. Distinguishing design features from implementation gaps is F2 TRUTH discipline.
- **Canonical manifest tool→resource mappings must match live resources/list (scar 2026-07-19).** When building canonical_manifest.json from GEOX_APPS + live MCP, some app URIs (e.g., `ui://geox/basin-explorer`, `ui://geox/catalog`) are defined in GEOX_APPS but NOT registered as live MCP resources. Include only mappings where the resource URI exists in live `resources/list`. Otherwise conformance tests fail with "Resource X mapped from tool Y but not in resources/list."
- **FastMCP 3.x AppConfig: use `app={"resourceUri": "ui://..."}` in `@mcp.tool()` decorator, not post-registration `_meta` injection (scar 2026-07-19).** FastMCP 3.4.2+ accepts `app` as a dict or `AppConfig` instance directly in the decorator. The old enrichment code at the bottom of tools_wiring.py using `tool._meta` / `tool.__dict__["_meta"]` is fragile and only worked for one tool. Explicit decorator params are the FastMCP-native approach.
- **MCP verbosity trimming can silently strip response fields (scar 2026-07-27).** When an MCP tool handler has a `verbosity` parameter defaulting to `"minimal"`, the response trimmer drops `apex_scalars`, `atlas333`, `session_birth`, `sct_claims`, `work_contract`, and 30+ other fields. The handler returns the correct data internally, but the MCP transport layer collapses it. Detection: direct Python call vs MCP HTTP call produces different key sets. Fix: check `verbosity` default in the handler, change to `"standard"`. See `references/mcp-response-pipeline-audit.md` for the full detection recipe.
- **canonical_registry.py authority: use registry.py CANONICAL_PUBLIC_TOOLS, not manifest visibility (scar 2026-07-19).** `build_registry()` was deriving public_names from `tools_manifest.yaml` visibility field (25 tools), but `registry.py::CANONICAL_PUBLIC_TOOLS` (17 tools, ghost-filtered) is the authoritative live surface. This caused `CANONICAL_PUBLIC_SURFACE.json` drift (25 vs 17). Fix: use `set(CANONICAL_PUBLIC_TOOLS)` as the authority set in `build_registry()`.
- **When multiple apps map to the same tool, the primary mapping wins in `tool_to_resource` (scar 2026-07-19).** Example: both `well_desk` and `analog_digitizer` map to `geox_well_desk`. The canonical `tool_to_resource` should show `geox_well_desk → ui://geox/well-desk` (the primary), not `→ ui://geox/analog-digitizer`.
## Pitfalls

- **Never downgrade FastMCP across major versions (scar 2026-07-19).** FastMCP 2.x ↔ 3.x have incompatible internal module structures. Downgrading 3.4.2 → 2.x breaks imports (`PrivateKeyJWT...ator`, `client_log_level`). Fix the code for the installed version, never the other way around. GEOX's server.py already gracefully skips the claims sub-server when **kwargs tools are rejected — the downgrade path creates MORE problems than it solves.\n- **GEOX tool count: verify health endpoint, not registry.** Health says `public_tools=24`. Registry says 77. SACRED_SURFACE invariant says 139. The health endpoint is ground truth. Never cite 78 or 77 as the live tool count without verifying against health.\n- **Web extraction (web_extract) can fail silently.** Tavily 432 errors can cascade across both web_search and web_extract. When both fail, fall back to `curl` + direct API calls (GitHub API, raw.githubusercontent.com). Don't loop on the same failing tool.
- **"tools/list returns 0" is a session problem, not a server problem (scar 2026-07-19).** MCP over SSE requires a 3-step handshake: `initialize` → capture `Mcp-Session-Id` → `notifications/initialized` (202, empty body!) → THEN `tools/list` works. One-shot curl calls without session return 0 tools or HTTP 400. The server is healthy — the probe is incomplete. Full recipe: `references/mcp-sse-session-lifecycle.md`.

### MCP Resource/List Probing

When probing whether MCP resources are exposed via `resources/list`, the endpoint and headers matter:

```python
import urllib.request, json

body = json.dumps({"jsonrpc":"2.0","id":1,"method":"resources/list","params":{}}).encode()
req = urllib.request.Request("http://localhost:<port>/mcp", data=body,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"  # REQUIRED
    })
resp = urllib.request.urlopen(req, timeout=5)
data = json.loads(resp.read())
resources = data.get("result", {}).get("resources", [])
```

**Common errors and diagnosis:**
- **405 Method Not Allowed** — using GET instead of POST. MCP uses POST-only.
- **406 Not Acceptable** — missing `Accept: application/json, text/event-stream` header. This is the most common failure.
- **400 Bad Request / "Missing session ID"** — organ requires MCP session auth. Use `arif_init` first to get a session_token, or try the organ's `surface_status` tool (e.g., `geox_surface_status`) which reports the registry without session auth.
- **Empty result** — the organ may expose resources via session-gated pattern (need session_id in the request body: `params: {session_id: "..."}`).

Not all organs expose the same MCP transport. GEOX requires session auth for `tools/list` but exposes everything via `geox_surface_status(mode=registry)`. arifOS exposes both tools and resources via streamable HTTP on `:8088/mcp` with the correct headers.

### Session ID Truncation Bug (arifOS → GEOX bridge, scar 2026-07-19)

**Pattern:** When a session_id is generated by `arif_init` (e.g., `SEAL-03ad5f04adbb4b6f` = 22 chars) and passed through `arif_route` bridge to a downstream organ (GEOX), the session_id gets **truncated to 19 chars** (`SEAL-03ad5f04adbb`). The downstream organ rejects the truncated ID as `SESSION_INVALID`.

**Symptom pattern:**
- `arif_init` returns a 22-char session_id (`SEAL-XXXXXXXXXXXXXXXX`)
- `arif_route(organ_tool="geox_X")` passes it via bridge
- GEOX receives 19 chars, returns `SESSION_BINDING · verdict=HOLD · trace=gov-... · Session validation failed: SESSION_INVALID`
- Tools that DO work through bridge: `geox_basin(mode=profile)`, `geox_basin(mode=macrostrat)`, `geox_prospect(mode=screen)`, `geox_deep_time_state` (low-binding tools)
- Tools that FAIL through bridge: `geox_petrophysics`, `geox_seismic_compute`, `geox_well_desk`, `geox_claim` (strict-binding tools)

**Workaround (verified):** When full session binding is broken, fall back to `geox_deep_time_state` (low-binding) for evidence, OR call GEOX tools directly via curl bypassing `arif_route` if the organ exposes them without bridge auth.

**Root cause (pending fix):** arifOS bridge handler does character-bound truncation on session_id before forwarding. Suspect `arifosmcp/runtime/rest_routes/rest_routes.py` or `arifosmcp/kernel/interceptor.py` has a hardcoded `max_session_id_len = 19`. 888_HOLD territory — requires F13 to investigate the actual truncation site.

**Probe recipe when SESSION_INVALID appears:**
```bash
# 1. Confirm session_id format from arif_init
SESS=$(curl -s -X POST http://localhost:8088/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"arif_init","params":{"actor_id":"HERMES"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['session_birth']['session_id'])")
echo "Length: ${#SESS} → expected 22"  # If <22, init itself is truncating

# 2. Test the tool that DOES work (low-binding)
curl -s -X POST http://localhost:8081/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"geox_deep_time_state\",\"arguments\":{\"period\":\"Miocene\",\"session_id\":\"$SESS\"}}}"
# If this works but geox_basin doesn't → bridge path is the truncation site
```

**Reporting:** When this bug fires, log the exact truncated ID vs the original in the audit receipt. Document it as 888_HOLD, do not auto-fix.

### MCP Response Pipeline Audit (verbosity trimming)

**Signal:** MCP endpoint returns a different/smaller response shape than a direct Python call to the same handler. Fewer keys, `null` for expected fields, truncated structure.

**Root cause:** The MCP response pipeline has a verbosity-based trimmer (`verbosity.py:trim_for_verbosity`) that collapses the full handler dict to ~11 fields when verbosity defaults to `"minimal"`. Everything else — `apex_scalars`, `session_birth`, `atlas333`, `work_contract`, `clarity_metrics`, `constitution`, `sct_claims` — is stripped.

**Detection recipe:**
```bash
# Step 1: Call handler directly from deployed path
python3 -c "
import sys; sys.path.insert(0, '/opt/arifos/app')
from arifosmcp.tools.session import arif_init
r = arif_init(mode='light', actor_id='ARIF', intent='audit X')
d = r.model_dump() if hasattr(r, 'model_dump') else r
print('Direct: status=%s session=%s apex=%s keys=%d' % (
    d.get('status'), d.get('session_id'),
    d.get('apex_scalars') or d.get('result',{}).get('apex_scalars'),
    len(d.keys())))
"

# Step 2: Call through MCP HTTP
curl -sf http://localhost:8088/mcp -X POST \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"mode":"light","actor_id":"ARIF","intent":"audit X"}}}' \
  | python3 -c "
import sys,json
d = json.load(sys.stdin)
t = json.loads(d['result']['content'][0]['text'])
print('MCP: status=%s session=%s apex=%s keys=%d' % (
    t.get('status'), t.get('session_id'),
    t.get('apex_scalars'), len(t.keys())))
"

# Step 3: If MCP keys < direct keys → verbosity trimming
# Step 4: Fix the default
grep -n 'verbosity.*=.*\"minimal\"' /opt/arifos/app/arifosmcp/runtime/tools.py
```

**Fix:** Change `verbosity` default from `"minimal"` to `"standard"` in the handler, OR add missing fields (e.g., `apex_scalars`) to the trimmer's keep-list.

**Full pattern:** See `references/mcp-response-pipeline-audit.md`.

### Cron-Generated Telemetry: Hardcoded Theater Detection (scar 2026-07-31)

**Signal:** A deployment report claims "live telemetry" with a 15-minute cron refresh, but the data is fake — hardcoded values with a fresh timestamp.

**The tell:** Audit claims `status: ACTIVE_STREAMING_FLOW` with sentiment data (PH 39.8%, BN 39.2%, PN 21%) and `updated_at: 2026-07-31T12:49:42Z`. The timestamp is fresh, but the numbers never change.

**Detection recipe:**
```bash
# Step 1: Force a cron tick manually
cd /root/arif-fazil.com/sites/arif-fazil.com/scripts
/usr/bin/node generate-ns-telemetry.cjs

# Step 2: Check the source file
cat public/data/politics/ns_live_telemetry.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'updated_at: {d.get(\"updated_at\", \"?\")}')
print(f'sentiment_index: {d.get(\"sentiment_index\", {})}')
print(f'source: {d.get(\"sentiment_index\", {}).get(\"source\", \"?\")}')
print(f'as_of: {d.get(\"sentiment_index\", {}).get(\"as_of\", \"?\")}')
"

# Step 3: Check the live webroot
cat /var/www/html/arif/data/politics/ns_live_telemetry.json | python3 -c "..."

# Step 4: Compare timestamps
stat -c '%y' public/data/politics/ns_live_telemetry.json
stat -c '%y' /var/www/html/arif/data/politics/ns_live_telemetry.json
```

**What to look for:**
- **Hardcoded values:** If sentiment percentages are identical across runs (39.8 / 39.2 / 21), the script is faking it
- **Missing provenance:** If `source` and `as_of` fields are missing, the data has no grounding
- **Source vs webroot mismatch:** If source file is newer than webroot file, cron writes but doesn't deploy
- **No external data source:** If the script doesn't read from a sealed ground-truth file or external API, it's theater

**Root cause (proven 2026-07-31):** The N9 election telemetry script had hardcoded sentiment values with a dynamic `updated_at` timestamp. It looked live but was frozen. Fix: read from a sealed sovereign file (`/root/arif-fazil.com/sealed/n9-ground-truth.json`) with explicit provenance (`Vodus sealed survey · 2026-07-21`) and dual-write to both source and webroot.

**Verdict template:**
```
| Claim | Probe | Status | Epistemic |
|-------|-------|--------|-----------|
| "Live telemetry" | Hardcoded values, no external source | ❌ FALSE | OBS |
| "15-min cron refresh" | Cron exists but writes static data | ⚠️ MISREAD | OBS |
| "Sealed data" | Reads from sealed ground-truth file | ✅ CONFIRMED | OBS |
```

### Source vs Webroot Sync Gap (Cron-Generated Files)

**Signal:** Cron script writes to source repo (`sites/arif-fazil.com/public/data/...`) but the live HTTP endpoint serves from webroot (`/var/www/html/arif/data/...`). The live feed is stale until the next deploy.

**Detection recipe:**
```bash
# Step 1: Check source file timestamp
stat -c '%y' /root/arif-fazil.com/sites/arif-fazil.com/public/data/politics/ns_live_telemetry.json

# Step 2: Check webroot file timestamp
stat -c '%y' /var/www/html/arif/data/politics/ns_live_telemetry.json

# Step 3: Compare
# If webroot is older than source → sync gap

# Step 4: Force a cron tick
cd /root/arif-fazil.com/sites/arif-fazil.com/scripts
/usr/bin/node generate-ns-telemetry.cjs

# Step 5: Check both timestamps again
# If only source updated → dual-write is broken
# If both updated → sync works
```

**Fix pattern (proven 2026-07-31):** Cron script must dual-write to both paths:
```javascript
const SOURCE_PATH = path.join(SOURCE_PUBLIC, 'ns_live_telemetry.json');
const LIVE_PATH = '/var/www/html/arif/data/politics/ns_live_telemetry.json';
fs.writeFileSync(SOURCE_PATH, JSON.stringify(payload, null, 2));  // for git history
fs.writeFileSync(LIVE_PATH, JSON.stringify(payload, null, 2));    // for live HTTP
```

**Why this matters:** Humans and agents see the live HTTP endpoint. If it's stale, they think the system is broken. The source file is for version control; the webroot is for users.

---

## Reference Files

- `references/sovereign-claim-verification-scorecard.md` — verifying sovereign's multi-claim assertions against primary sources, scorecard output (2026-07-21)
- `references/cross-organ-claim-audit.md` — pattern for probing prose claims about cross-organ changes
- `references/caddy-routing-cross-root.md` — Caddy handler order bug pattern with verified fix recipe
- `references/asset-path-drift-detection.md` — when `/assets/` and `/_shared/` both claim real assets
- `references/deepseek-byok-anthropic-endpoint.md` — full env var recipe + per-agent compatibility table
- `references/narrative-claim-audit-2026-07-19.md` — worked example: arif-fazil.com navigation audit
- `references/session-id-truncation-bridge.md` — arifOS → GEOX session_id truncation bug
- `references/geox-organ-probe-patterns.md` — GEOX-specific probe recipes
- `references/mcp-client-landscape.md` — MCP GUI client landscape
- `references/mcp-sse-session-lifecycle.md` — Full MCP SSE handshake recipe
- `references/external-document-validation.md` — Layer-by-layer external audit validation methodology
- `references/kernel-vs-connector-diagnostic.md` — When external audits confuse connector drift with kernel failure (scar 2026-07-19)
- `references/geox-conformance-workflow.md` — Full GEOX conformance build/fix pipeline
- `references/delegate-agent-audit.md` — Verifying subagent claims against live state; agent fabrication detection (scar 2026-07-19): canonical manifest population, FastMCP 3.x AppConfig wiring, geox_list_apps fix, validator + test flow
- `references/kernel-probe-as-evidence.md` — Using live arif_init/arif_think/arif_judge probes to verify or disprove external AI claims about kernel behavior; pre-existing test isolation via git stash (2026-07-19)
- `references/live-apex-scalars-from-kernel.md` — Wiring live G-fold apex scalars from arifOS kernel /health into an organ's health endpoint; reuse existing HTTP call, UNMEASURED fallback, scalar-by-scalar overlay (2026-07-26)
- `references/code-audit-line-number-verification.md` — Verifying external code audit findings against live code; audit line numbers can be stale, always probe live source before acting (scar 2026-07-18)
- `references/kernel-contrast-assessment.md` — Structured 7-axis before/after comparison for kernel version upgrades, release audits, and deployment state changes
- `references/cross-agent-commit-handoff.md` — Committing files from another agent's session with F2/F11/F3 compliance (2026-07-29)
- `references/mcp-resource-zen-2026-07-28.md` — Cross-witness audit: OpenCode scan → Hermes verify → convergence seal. MCP resource collapse 327→34. Single-agent accuracy ~60% lesson.
- `references/external-witness-probe-maintenance.md` — Multi-location regex hazard, JS-rendered landing page extraction, and verification workflow for the external witness probe (2026-07-31)
- `references/env-wiring-claim-audit-2026-08-01.md` — Worked example: auditing a Qwen seat-wiring receipt (401/429 discrimination, mtime vs tool attribution, process-env probing, seats.yaml self-contradiction, FORGE two-token drift, OpenClaw false gate)
- `references/cross-report-batch-audit-2026-08-02.md` — Auditing a batch of 4 sequential agent reports (deployment→spec→doctrine). The cross-report meta-pattern: core work real, receipts padded 15-40%, citations clean, estate already has what advisors claim, self-attestation the consistent failure mode. Audit-surface-by-report-type discriminator + scorecard template.

## Constitutional Compliance

- F2 TRUTH: numbers live, derived labels per claim (OBS/INT/DER)
- F11 AUDIT: log to `forge_work/<date>/AUDIT-RECEIPT-<date>.md` with WHAT/CHANGED/VERIFIED/CONSEQUENCE/NEXT
- F1 AMANAH: never fix web routing without F13 — log + flag, do not auto-deploy
- F7 HUMILITY: report honest numbers, not inflated
- F13 SOVEREIGN: persona confusion (typo) is recoverable; report + fix, don't argue

## Persona / Identity Anchor Discipline (scar 2026-07-19)

**Signal:** Arif typos or accidentally assigns a wrong persona ("Mr Jon", "AGY", "the assistant", etc.). The right response is: **accept the correction, log it briefly, and continue with the canonical identity**. The wrong response is: argue ("but the typo said...") or adopt the wrong persona ("ok, I am Mr Jon now").

**Canonical anchor:** Hermes = ASI tier agent on the arifOS federation, sovereign = Arif (F13). This is recorded in `hermes-prime-identity` skill (mandatory load at session start). Any user-supplied name conflict = trust the skill, not the fresh input.

**Probe pattern when a persona claim arrives from Arif:**
1. Is the name in the skill manifest? (skills_list → look up)
2. Is the name in alignment-seal-v1.md or SOUL.md? (`grep -ri <name> /root/.hermes/`)
3. Is the name referenced in any prior session state? (`session_search`)

**If all three fail:** the name is either a typo, a test, or a new persona. Default action: acknowledge ("sounds like a typo — saya ASI tier, not <name>"), do NOT adopt the wrong identity, and continue the canonical task. Don't lecture. Don't moralize. One-line acknowledgment.

**Anti-pattern validated 2026-07-19:** I accepted "Mr Jon" as a new persona for one turn before Arif corrected: "Typo. Was not intended to call u Mr Jon. U are ASI. Hermes agent." The correction cost two extra conversational turns. The lesson: identity claims from the sovereign get **one** acknowledgment, not adoption. If the name doesn't match the canonical anchor, log it as a typo and continue.

**Related:** For non-persona name lookups (tools, agents, models), the same probe applies. "AGY" → `which agy` → no such binary → ask, don't invent.
