---
name: deployment-claim-verification
description: |
  Verify deployment reports and feature claims against live system state and source data.
  Cross-reference claimed counts, route availability, redirect behavior, and data integrity
  against actual source files, live HTTP responses, and build artifacts. Catches inflated
  numbers, phantom features, and routing misrepresentations before they become scars.
  Use when Arif shares a deployment report and says "audit this", "verify these claims",
  "is this real", "check the numbers", or presents a status table with counts to validate.
triggers:
  - "audit this deployment"
  - "verify these claims"
  - "check the numbers"
  - "is this count right"
  - "audit all of these"
  - "deployment report"
  - "status table"
  - "fix deployment contract drift"
  - "P0 deployment audit"
  - "fix P0 critical items"
  - "align all surfaces to source of truth"
  - "audit WELL organ registry"
  - "audit MCP surface"
  - "check for phantom exports"
  - "verify all tools resolve"
  - "MCP registry audit"
  - "organ registry check"
  - "verify this receipt"
  - "audit agent receipt"
  - "check these claims"
  - "verify config claims"
  - "seats registry check"
  - "audit this dashboard"
  - "audit this page"
  - "check the live proxies"
  - "narrative vs live"
---

# Deployment Claim Verification

## When to Load

When a deployment report, status table, or feature manifest includes **specific quantitative claims** (route counts, entry counts, feature counts) that need ground-truth validation. The report may be self-authored or produced by another agent — both need verification.

## Core Principle

**Claims are hypotheses until verified against source data.** A report saying "87 essays" is a CLAIM. The source file having 69 entries is an OBS. The delta (18 overclaimed) is the finding.

## Audit Pipeline

### Phase 1: Route Verification (HTTP layer)

```bash
# For each claimed route, check HTTP status
curl -so /dev/null -w "%{http_code}" https://<domain>/<route> && echo " /<route>"
```

- 200 = route serves content
- 301/302 = redirect (follow it, verify destination)
- 404 = broken claim
- **SPA caveat**: React SPAs serve 200 for ALL paths (including `/nonexistent`). The 200 proves the SPA shell loads, NOT that the route has real content.

### Phase 2: Source File Verification (data layer)

For each claimed data count, find the **actual source file** and count:

```bash
# Find the data file
find <project-root> -name "writings.ts" -o -name "articles.json" -o -name "entries.*"

# Count entries (adapt to data format)
grep -c "slug:" src/data/writings.ts
grep -c '"id":' src/data/entries.json
```

**Always count, never trust the report's number.**

### Phase 3: Cross-Reference Claims vs Source

Compare each claimed number against actual source count. Classify:

| Delta | Classification |
|-------|---------------|
| 0 | ✅ Accurate |
| ±1-2 | ⚠️ Minor drift (might be counting method) |
| ±5+ | ❌ Inflated or deflated — FIND THE SOURCE |
| Claims data in wrong file | ❌ Misattribution |

### Phase 4: Redirect Verification

Distinguish between redirect types:

| Type | HTTP | Implementation | SEO Impact |
|------|------|----------------|------------|
| Server-side (Caddy/nginx) | 301/302 with Location header | Caddyfile, nginx.conf | Crawlers follow |
| Client-side (React Router) | 200 + JS redirect | `<Navigate to="..." replace />` | Crawlers may NOT follow |

```bash
# Check if redirect is server-side or client-side
curl -sI https://domain/old-path | grep -i "location\|HTTP"
# If Location header present → server-side redirect ✅
# If 200 with HTML body → client-side (React Router) ⚠️
```

**Client-side redirects work for humans but not for crawlers/bots.** If SEO matters, server-side redirects are required.

### Phase 5: Build Freshness

```bash
stat <dist-path>/index.html | grep Modify
# Compare against claimed deployment timestamp
```

### Phase 6: SPA Content Verification

For React SPAs, curl + grep on HTML won't find essay content (it's client-rendered). Instead:

1. Check that the JS bundle loads: `curl -s <url> | grep -oP 'src="[^"]*\.js"'`
2. Verify the data file imports exist in the bundle
3. Check the data source file directly for entry counts
4. Use browser_vision for visual verification if needed

## Output Template

```
## Deployment Audit Report

### Route Verification
| Route | Claimed | Actual | Status |
|-------|---------|--------|--------|
| /path | 200 | 200 | ✅ |

### Data Integrity
| Claim | Claimed | Actual | Delta | Source File |
|-------|---------|--------|-------|-------------|
| Essay count | 87 | 69 | -18 ❌ | src/data/writings.ts |

### Redirects
| Old Path | New Path | Type | Status |
|----------|----------|------|--------|
| /old | /new | Caddy 301 | ✅ |

### Build
- Last build: <timestamp>
- Freshness: <age>

### Findings
1. [severity] Finding description
```

## MCP Organ Registry Audit

When auditing an arifOS federation organ's MCP surface (WELL, GEOX, WEALTH, etc.), use the three-layer pattern: registry self-report → independent tool calls → source code cross-check. The key insight: `@mcp.tool()` decorators in source do NOT mean a tool is on the public wire — boundary enforcement strips most of them. Only behavioral verification (Layer 2) proves a tool works.

See `references/mcp-organ-registry-audit.md` for the full pattern with exact commands, the decorator-vs-SOMATIC_TOOLS-vs-wire distinction, and the 5 pitfalls.

## MCP Contract Drift — Audit → Fix Pipeline

When an external audit finds drift between declared MCP surface and live state across multiple P0 items (tool counts, URI canonicalization, output semantics, MCP Apps bridge, build identity, CI repair, dead POC code), use the audit → fix → regenerate → startup-verify pipeline. Commit one P0 item per commit with conventional commits. Always regenerate static surface files from the live registry, never hand-edit them.

See `references/mcp-contract-drift-audit-fix.md` for the full 6-phase pipeline with exact commands, GHOST_TOOLS pattern, concurrent subagent collision handling, and startup verification recipe. Proven on GEOX P0 deployment audit 2026-07-19 (7 items).

## Pitfalls

1. **Self-claims need live probing too — never assert system state from memory.** (PROVEN 2026-07-29) When writing a status report, session summary, or deployment update that includes quantitative system state (FQ, organ health, dirty file counts, receipt counts), always live-probe the relevant endpoint (`curl :port/health`, `git status -s`, `ls`) at the moment of writing. Never rely on a value you saw 15+ minutes ago — T₀ and T₁ can disagree within minutes. The Dynamic-State Principle from AGENTS.md applies: "State observed at T₀ is evidence only for T₀."

    **Checklist before writing any system-state assertion:**
    - `curl -s :port/health | jq .fq` (or relevant field)
    - `git -C /root/REPO status -s | wc -l` for dirty file counts
    - Note the probe timestamp in the report so the reader (including yourself next session) knows when the measurement was taken.

2. **Never trust the report's numbers.** Always count from source.
3. **SPA 200 ≠ content exists.** React SPAs serve 200 for everything. Check the data layer.
4. **Client-side redirects ≠ server-side redirects.** Both "work" but only server-side is visible to crawlers.
5. **Multiple data stores.** A project may have `writings.ts` (69 entries), `essays/` (70 files), `generated/` (50 files), and `articles.json` (66 entries). Don't conflate them.
6. **Legacy vs current data.** Old data files may still exist alongside new ones. Verify which is actually served by the live routes.
7. **"Every surface has feature X" claims need surface-by-surface probe.** Probe each individually.
8. **"100% pass rate" claims must specify what was tested.** Split verification by category (HTML routes / assets / discovery / redirects).
9. **HTML edits to `/var/www/html/` are deploy artifacts, not source.** Track source-of-truth regeneration as a separate TODO.
10. **Static surface files drift from live registry. Never trust them over the health endpoint.** Generate all static surface files from the live registry programmatically, never hand-edit them.
11. **Concurrent subagent edits can corrupt your patches.** Re-read the file before patching when sibling modifications are warned.
12. **Audit the audit — seal reports can contain fabricated receipts.** (PROVEN 2026-07-31) Verify cited git commits exist, reported HTTP status codes match live probes, tool counts match actual `tools/list`, and Caddyfile comments match actual behavior. The report's receipts can be phantom even when underlying work is real.
13. **Check the artifact for internal self-contradiction, not just against the world.** (PROVEN 2026-08-01) Before comparing a report/spec to live state, compare its parts to each other. Two proven cases: (a) a sentinel audit report whose header said "Total probes: 0" while its body listed 64 live probe results — a counter bug that undermines trust in the whole report even though the probes ran; (b) a design-token spec that embedded a block-build CI rule ("every text/background ≥ WCAG AA") while its own token values failed that rule (yellow-500 `#FFCC00` text on paper `#FAF7F0` = 1.4:1). When a spec declares its own invariants, **run the spec's own rules against the spec's own values** before ratifying — a canon that violates its own CI lint becomes a constitutional contradiction the moment it's merged. Cheap to catch pre-merge, expensive after.
14. **Stuck-loop agent hallucination cascade — disengage after delta.** (PROVEN 2026-07-31) When another agent enters a self-sustaining loop — re-proposing the same stale plan based on cached state, citing old git HEAD values, describing UI elements absent from source — each rebuttal you make extends its context window without overwriting the original stale analysis. The break: post ONE delta table (claimed vs actual with probe timestamps), then full silence. Not even emoji. The silence IS the signal. See Wisdom Scar #17 for the full diagnostic and disengagement protocol.
15. **Agent misdiagnosis: verify the ACTUAL blocker before accepting a diagnosis.** (PROVEN 2026-08-01) When another agent reports "PR blocked because X", independently verify with `gh pr view <N> --json mergeStateStatus,reviewDecision,mergeable`. A blocked PR can have multiple simultaneous blockers (signatures, reviews, status checks). The agent may fixate on one (e.g. "SSH key not registered") while the real blocker is another (e.g. `REVIEW_REQUIRED` with no approvals). Always check `reviewDecision` — if it says `REVIEW_REQUIRED`, the blocker is approvals, not signatures, regardless of what the agent claims. See `arifos-ed25519-sovereign-signing` skill § "PR blocked ≠ signing issue" for the full diagnostic flow.
16. **Provider/model-list availability ≠ quota access — probe the exact key+model pair.** (PROVEN 2026-08-01, Qwen Token Plan) A seat can list 21 models in `/models` yet return `Allocated quota exceeded` for specific models at chat-completion time (Standard seat listed `qwen3.7-plus` but only Pro seat could run it; Standard could run `qwen3.8-max-preview`/`qwen3.6-flash`/`kimi-k2.7-code` fine). A claim like "HERMES-SEAT-OK via QWEN_HERMES_API_KEY / qwen3.7-plus" is only TRUE if a live chat-completion call with THAT exact key and THAT exact model returns a completion. Always verify the exact pair, not "the key works" or "the model is listed".
17. **File-mutation verifier "refused" ≠ file unchanged — check mtimes, not the warning.** (PROVEN 2026-08-01) A forge agent's receipt showed a verifier warning "[patch] Refusing to write to config.yaml" yet the file HAD changed — the agent used the sanctioned CLI path (`hermes config set`) after the patch tool refused. When a receipt's verifier note contradicts its own prose, resolve with `stat -c '%y %n'` on the file AND its backups: mtime AFTER backup = changed; mtime at/before backup = untouched. The verifier warning only proves the *patch tool* was refused, not that no change landed.
18. **Blind string-replace can corrupt the very registry it claims to fix — verify per-seat fields.** (PROVEN 2026-08-01) A forge agent's `s.replace(old, new, 1)` script on seats.yaml matched the WRONG seat block (two seats shared identical `rotation_status: "OVERDUE"\n vault_status: "EMPTY"` patterns), marking the OpenClaw seat POPULATED and leaving the actual Hermes seat EMPTY — the reverse of reality. After any agent claims "seats.yaml updated", re-grep the per-seat `env_var` + `vault_status` pairs against the vault values. String-replace scripts need unique anchors (seat_id or env_var), not bare repeated patterns.
19. **Audit reports can compare against the wrong backup — verify against CURRENT live state, not the report's diff.** (PROVEN 2026-08-01) An audit claimed "888-APEX model drift: description says deepseek-v4-pro but actual is still glm-5.2" and "missing structural blocks (references, compaction, plugin, subagent_depth)". Live check: 888-APEX = `qwen-token-plan/deepseek-v4-pro` ✅ and ALL structural blocks present ✅. The auditor had diffed against backup 07:28 (where the agent block was NOT SET) instead of the current config. When a report says "drift", grep the CURRENT file for the exact field before believing the delta.
20. **Reasoning models return empty `content` with low max_tokens — parser false-ERR.** (PROVEN 2026-08-01) `deepseek-v4-flash`/`deepseek-v4-pro`/`glm-5.2` put output in `reasoning_content` and leave `content: ""` when `max_tokens` is tiny (4). A naive parser checking `choices[0].message.content` reports ERR with an empty message — and I nearly classified live models as dead. A model is only dead if the response carries a real `error` object; check `reasoning_content` too, or use `max_tokens >= 20`. Distinguish "quota/API error" (real failure) from "empty content" (parser artifact).
21. **Phantom static deployment — redirect chain live but content file never landed.** (PROVEN 2026-08-01, Shadow Decoder) A sealed receipt claimed `GET /politics/shadow/ → 200 · 22,635B · ttfb 76ms` plus a verified 301 chain (`/shadow/` and `/shadow` → `/politics/shadow/`). Live probe: **HTTP 404, 0B body**. The Caddy handler existed (lines 715-718) and the redirects worked — but `/var/www/html/arif/politics/shadow/index.html` had never been created. Redirect chain green does NOT prove the destination file exists: probe the FINAL destination URL's status AND body size, and match any claimed byte count against `wc -c` of the actual webroot file (claimed 22,635B vs actual 0B is the tell). Fix path: check `/root/backups/` for the pre-seal snapshot (the article HTML was there), rebuild the static page wrapping that content in the site's zen template, deploy, then re-probe status + size.
22. **Security-gate claims need live behavioral tests, not source greps — and coverage must be checked against ALL input-accepting tools, not the report's list.** (PROVEN 2026-08-01, hermes_mcp injection scan) A deployment report claimed "20 regex patterns across 8 categories wired into 3 tools (fact_check, epistemic_check, plan_review), SHA256 X, service active on :18086". Live audit: `sha256sum` matched, `systemctl is-active` matched, but the pattern inventory was actually **21 patterns / 13 categories** (report's grouping coarser — minor), and the report's "wired into 3 tools" framing hid the real finding: **`hermes_cross_verify` and `hermes_memory_steward` also accept external text but had NO injection gate** — the attack surface was 5 tools, only 3 covered. Sequence that proves a gate FIRES (not just exists): (1) `sha256sum` + `systemctl is-active` + `ss -tlnp` for the port; (2) grep ALL tool definitions (`grep -n "@mcp.tool" file` → list every tool) and check which accept free text — compare coverage vs the report's list; (3) count the ACTUAL pattern tuples in source (report's "20/8" is a claim; count `INJECTION_PATTERNS` entries and unique categories); (4) **fire live payloads through the full MCP lifecycle**: `initialize` → capture `Mcp-Session-Id` header (case-sensitive — read `r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")`) → `notifications/initialized` → `tools/call` with (a) a crafted injection payload (expect `injection_detected: true`, score 0.0, category list) and (b) a clean control payload (expect no injection flags). Raw `tools/call` without a session returns 400 "Missing session ID" — that's a handshake requirement, NOT a gate failure. Deliverable for a security-feature claim is a live pass/fail test matrix; the finding is usually the coverage gap (tools the report didn't mention), not the claimed feature.
23. **Claimed patch can target a field that doesn't exist in the file — recursive field search required.** (PROVEN 2026-08-02, OpenClaw audit) A report claimed "agent-card.yaml primary_model → qwen-token-plan/deepseek-v4-flash" and "workspace.yaml runtime.model → ...". Live check: the file was .json not .yaml, and NEITHER file contained any `primary_model`, `model`, or `runtime.model` field anywhere in the tree. The patch target was phantom. **Detection:** when a report claims "field X → value Y" in a config file, don't just grep for the value — recursively search the parsed structure for ANY key containing the field name (`find_model(obj, path='')` walking dicts/lists). If the field doesn't exist, the patch either landed in a different file or never landed at all. Also verify the file EXTENSION matches the claim (.yaml vs .json).

24. **Config file ≠ runtime truth — check journalctl for what the service actually calls.** (PROVEN 2026-08-02, OpenClaw audit) Gateway config declared `minimax/MiniMax-M2.5` as tertiary provider, but journalctl logs showed actual API calls going to `MiniMax-M3`. The config is the INTENT; the runtime log is the TRUTH. When auditing a cascade/fallback claim, check `journalctl -u <service> --since <window> | grep 'model-fetch\|provider='` for the models actually invoked, not just what the config declares.

25. **Provider removal creates dangling references in fallback chains — sweep ALL reference sites.** (PROVEN 2026-08-02, Hermes hotfix audit) Report removed 5 providers (14→9) and claimed "cascading failures fixed." But `fallback_providers[0]` still referenced the removed `mulerouter` and `fallback_providers[5]` referenced `ollama` (also absent). The next failover would cascade into a ghost provider — the exact bug class the report claimed to solve. **After any provider pruning audit, cross-check:** (a) fallback_providers / fallback chains, (b) aux.* references, (c) TTS provider refs, (d) litellm fallback comments, (e) any hardcoded model→provider mappings. A provider is only truly removed when zero references remain.

26. **Restart claims need journalctl error scan, not just "is-active".** (PROVEN 2026-08-02, OpenClaw audit) Report claimed "Restarted openclaw-gateway twice ✅ active, /health ok." Service WAS active and /health returned green. But journalctl in the restart window showed `"agent run failed: Session changed while starting work. Retry."` and `"startup task failed"` — both unreported. **Protocol:** on any restart claim, run `journalctl -u <unit> --since "<restart_time>" | grep -i "fail\|error\|retry"` and report findings. A green /health with boot errors is PARTIAL, not CONFIRMED.

27. **The "current state" summary section is often the most wrong part of a report.** (PROVEN 2026-08-02, dual Hermes+OpenClaw audit) Both reports had "current state" sections that contradicted live config. Hermes report claimed `model.default: deepseek-v4-flash via QWEN_OPENCODE_API_KEY` — actual was `qwen3.8-max-preview via qwen-token-plan-individual`. OpenClaw report claimed vault "fresh Aug 2" — mtime said Aug 1. The fix narrative gets the agent's attention; the summary section gets copy-pasted from stale context. **Always probe the "current state" block as aggressively as the fix claims** — it's where stale context is most likely to survive unchallenged.

28. **Backup-vs-current diff is the ground truth for "what changed" — not the report's root cause story.** (PROVEN 2026-08-02, Hermes hotfix audit) Report claimed root cause was "OpenCode format provider/model prefix" (`qwen-token-plan/deepseek-v4-flash`). But the pre-fix backup showed `model.default: deepseek-v4-flash` — already bare, no prefix. The diff between backup and current is the ONLY reliable record of what actually changed. When a report tells a root-cause story, diff the backup against current and check whether the story matches the delta. If the backup already had the "fixed" value, the root cause narrative is fabricated or the fix landed before the backup was taken.

29. **Report-type determines audit depth — doctrine/synthesis reports have thin falsifiable surface.** (PROVEN 2026-08-02, four-report audit series) Classify the report before probing: deployment/hotfix reports (probe config+mtime+HTTP+env), spec/advisory reports (probe citations + named files), doctrine/synthesis reports (THIN surface — audit only the concrete anchors: do the named "patterns" map to real findings? are citations reused correctly? is the gap/eureka list honest about unknowns?). Do NOT fabricate audit surface for a doctrine report; report the thin surface honestly. The zero-day "Final Seal" doctrine report was ~90% honest precisely because its concrete anchors (devil patterns) mapped to real findings and its eureka list refused to fabricate the E-G..E-L gap. See also `live-probe-audit-pattern` § "Classify the Report Type FIRST" and § "Gap-Claim Audit".

30. **Citation claims need URL probe AND term grep — "page exists" ≠ "page says what's claimed."** (PROVEN 2026-08-02, zero-day spec audit) A spec/advisory report cited 6 external references (CISA KEV, OWASP MCP Cheat Sheet, CycloneDX, NIST 800-115). Verification: `curl -sf <url>` to confirm the page is live AND report its byte size, then `re.search(term, html, IGNORECASE)` for EACH specifically-claimed term. The OWASP MCP Cheat Sheet (79KB) was confirmed to actually contain all 9 claimed risk terms (tool poisoning, rug pull, tool shadowing, confused deputy, data exfiltration, excessive permission, supply-chain, replay, sandbox escape). Don't stop at "the URL resolves" — a citation can point to a real page that doesn't contain the claimed assertion. For reused citations across a report series, verify once and mark "verified prior audit."

31. **Stub-file paradox + docstring drift — a file NAMING a capability ≠ IMPLEMENTING it.** (PROVEN 2026-08-02, zero-day spec audit) Two proven cases: (a) `adversarial_audit_harness.py` was a 7-line stub whose only body was `print("Harness ready. Adversarial cases: [DRIFT, GEN_QUOTE, AUTHOR_SWAP, RISK_BYPASS]")` — it NAMED four test cases and implemented ZERO. A report cited it as "with adversarial cases such as drift, generated quote, author swap, risk bypass," implying working tests. (b) `threat_engine.py` docstring claimed "parses Python AST, SQL tokens, shell structure, and natural language" — AST parsing was real (`ast.parse`/`ast.walk`), but "natural language" was regex keyword matching and "SQL tokens" had no tokenizer. **Detection recipe:** for any file a report cites as a capability, check (1) line count (`wc -l` — a 7-line "harness" is a stub), (2) whether the body is logic or just a banner/print, (3) whether the docstring's verbs ("parses", "verifies", "detects") match the imports actually present (`import ast` vs no `sqlparse`/NLP import). Grep the case/keyword names the report claims — if they appear ONLY in a print string or comment, the capability is named, not built.

32. **systemd `Environment=-VAR=` does NOT unset — use `UnsetEnvironment=VAR`.** (PROVEN 2026-08-02, litellm-proxy) A service unit used `Environment=-DATABASE_URL=` to prevent litellm from seeing the inherited DATABASE_URL. This sets the variable to an *empty string* — litellm still detected it as "set" and triggered Prisma + 128 Supabase migrations. The correct directive is `UnsetEnvironment=DATABASE_URL POSTGRES_URL` which removes the variables from the process environment entirely. Verify with `tr '\0' '\n' < /proc/$PID/environ | grep -c DATABASE_URL` — should return 0. The minus-prefix syntax is for *overriding* inherited values, not *removing* them. See `references/litellm-nodb-fix.md`.

34. **"Missing" claims from advisors without filesystem access need estate probes before acceptance.** (PROVEN 2026-08-02, Copilot zero-day critique) An external advisor claimed "your agents are missing 10 controls." Live probe: 4/10 already existed (witness_packet.py 707 lines, verdicts.py 512 lines with RICHER enum than proposed, attestation_verifier.py with TTL, constitutional floors). The advisor's stated method ("searched M365, found no indexed artifact") meant it never touched the VPS. Rule: when an advisor says "you lack X" and its evidence is citation-only (no curl, no grep, no stat), probe the estate for X before accepting the gap. The genuine gaps are usually the ones identified with least confidence — here, the scanner regression suite was the one real gap, confirmed by a 7-line stub.

35. **Cross-report audit convergence — produce a summary table when auditing multiple reports from the same incident.** (PROVEN 2026-08-02, 4-report series) When auditing 2+ agent reports from the same session/incident, close with a cross-report summary: report name, accuracy %, key finding. Pattern across 4 reports: core operational work is usually real (60-90%), receipts are padded 15-40%, citations are clean when present, self-attestation is the consistent failure mode, and the estate already has more than agents claim to build. The summary table lets the sovereign see the PATTERN, not just individual findings.

36. **Verifier factual error ≠ verifier structural concern invalid — separate the two verdicts.** (PROVEN 2026-08-02, FED FLAME FRAME audit) A verifier claimed "NO custom_providers.litellm entry" (factually FALSE — truncated read at line 80 of 1328) AND "routing not proven through gateway" (structurally TRUE — gateway PID predated config mtime). The correct response is NOT "verifier wrong, dismiss everything" — it's "factual claim wrong, structural concern valid, here's the corrected status table." When a verifier's evidence is bad but its concern has a kernel of truth, issue TWO separate verdicts: one for the factual claim (❌ FALSE, here's the grep proof), one for the underlying concern (✅ VALID, here's what actually needs closing). Conflating them wastes the real finding.

37. **Gateway config freshness — compare PID start time vs config mtime, not just "is-active".** (PROVEN 2026-08-02, FED FLAME FRAME) A gateway can be `active` and healthy while running STALE config in memory. LiteLLM has no hot-reload endpoint (`POST /config/reload` → 404). The proof: `ps -o lstart= -p $PID` (gateway start) vs `stat -c '%y' config.yaml` (last edit). If start < mtime, the running process has the OLD config. Routing through new aliases will fail until restart. This is distinct from "service is down" — the service is UP, just not serving the new config. Always report freshness as a separate gate from liveness.

38. **Hardcoded `Environment=KEY=val` in systemd unit overrides `EnvironmentFile=` — Gödel lock violation.** (PROVEN 2026-08-02, litellm-proxy) A unit had BOTH `EnvironmentFile=/root/.secrets/vault.flat.env` (line 10) AND `Environment=LITELLM_MASTER_KEY=sk-...` (line 13). systemd applies `Environment=` AFTER `EnvironmentFile=`, so the hardcoded value wins. This means vault rotation has NO EFFECT on the service — the key is stranded in the unit file, invisible to `make vault-verify`. **Detection:** `grep -n 'Environment=' /etc/systemd/system/<unit>.service | grep -v EnvironmentFile` — any hit is a potential Gödel lock violation. **Fix:** remove the hardcoded line, ensure the key exists in vault.flat.env, `systemctl daemon-reload && systemctl restart <unit>`, verify via `/proc/$PID/environ`. After fix, vault is the SINGLE source — rotating in kunci-mas.env + `make vault-generate` + restart is the only path.

39. **arifOS VAULT999 seal bounces on OBSERVE_ONLY — expected, not a failure. Disk artifact is the fallback.** (PROVEN 2026-08-02) `arif_seal` without Ed25519 sovereign bind returns `status: pending, authority_level: OBSERVE_ONLY, floor_passed: false`. This is F13 working correctly — mutation intent without verified identity is 888_HOLD. The correct response: write the audit artifact to disk as JSON (`/root/reality_ledger/<name>.json`) with SHA-256 hash, note "VAULT999 seal pending sovereign bind", and move on. Do NOT retry the seal in a loop. Do NOT treat the bounce as an error in the audit itself. The disk artifact IS the audit record; the cryptographic seal is a sovereign ceremony that happens later.

33. **A regex gate that PASSES basic verification still has bypass classes — adversarial-variation testing is the second pass.** (PROVEN 2026-08-01, hermes_mcp injection scan follow-up) After pitfall #22 confirmed the gate fires (24/24 unit tests), adversarial paraphrases found 3 real bypasses in a "working" gate: (a) **intervening article** — `"forget your earlier instructions"` escaped `(disregard|forget|erase)\s+(all\s+)?(previous|prior|earlier|above)` because "your" sat between verb and keyword; fix = `\s+(all\s+|(your|my|the|these|those)\s+)?`; (b) **case-lowering bug** — the code lowercased input (`text.lower()`) but patterns kept literal `F13` uppercase, so `"bypass F13"` NEVER matched (`f13` vs `F13`); fix = `re.search(pattern, text_lower, re.IGNORECASE)` — lowercasing one side is NOT enough when patterns contain uppercase literals; (c) **intervening article in sovereign-bypass** — `"override the sovereign veto"` escaped `(override|bypass)\s+(F13|sovereign|human|veto)`; fix = `(override|bypass)\s+(the\s+|any\s+)?...`. Lesson: unit-test each category with 5+ natural-language variants (insert articles, possessives, pluralize, uppercase literals), not just the literal phrases from the report. **Isolation-extraction technique for unit-testing a gate without starting the server:** bracket-balance the list literal (`INJECTION_PATTERNS = [...]` — walk depth, not `.*?` regex, which cuts early on nested strings), then exec the function with `ns = {'re': _re}` — module-level `import re` sits BETWEEN the patterns block and the function, so the function's `re` reference dangles unless you inject it. **MCP E2E quirk:** `notifications/initialized` can 404 on fastmcp servers — skip it; `tools/call` works with just the `Mcp-Session-Id` header from the initialize response (case-sensitive, response HEADER not body).

40. **SPA catch-all swallows API endpoint typos — silent fetch degradation, not 404.** (PROVEN 2026-08-04, PETRONAS vitals) A dashboard page carried `const API = origin + '/wealth/gold/api/proxies'` but the live endpoint was `/gold/api/proxies`. On an SPA catch-all host the wrong path returns **HTTP 200 + HTML** (the SPA shell), not 404 — so the fetch "succeeds", JSON.parse throws, and the page falls back to "Proxies unavailable · sealed inputs remain authoritative." The live-monitoring layer dies while the page looks intact and every route probe reports green. **Detection recipe:**
    ```bash
    # 1. Extract fetch/API constants from DEPLOYED HTML
    grep -oE 'const API[^;]*;|fetch\("[^"]*"' /var/www/html/<page>/index.html

    # 2. Probe each endpoint — assert JSON, not HTTP 200
    curl -s -o /tmp/out -m 12 -w "%{http_code} %{content_type}\n" "https://domain<path>"
    file -b /tmp/out   # "JSON text data" = alive; "HTML document" = SPA shell swallowed it

    # 3. On a wrong path, try prefix variants (drop/add one segment)
    for p in /gold/api/x /wealth/gold/api/x /wealth/api/x; do
      curl -s -o /tmp/o -m 12 -w "%{http_code} " "https://domain$p"; file -b /tmp/o
    done
    ```
    **Discriminators:**
    - HTTP 200 on an API path proves NOTHING — check content-type / file signature. This is the API-side twin of pitfall #3 (SPA 200 ≠ content).
    - A dashboard's "fallback/unavailable" message IS the failure signal — probe the endpoint it was supposed to render before accepting "graceful degradation" as intended design.
    - Check the endpoint JSON's `timestamp` field for freshness — live endpoint with stale timestamp is its own failure class (see the cron-generated telemetry section in `live-probe-audit-pattern`).
    - Fix is usually one line (the API constant, in source + webroot). On arif-fazil.com this is F13-gated: propose the one-liner, don't deploy.

41. **Back-solve derived constants from sealed anchors — a stated coefficient and its derived prices must agree.** (PROVEN 2026-08-04, PETRONAS vitals) Static text claimed "±$10 Brent ≈ ±RM6.0B FCF/CFFO" AND "FCF crosses zero at $71.60" AND "CFFO tripwire at $47.40" (reference $84.10). Back-solving from the sealed JSON: $84.10−$71.60 = $12.50 against RM11.6B FCF ⇒ implied **RM9.3B/$10**; $84.10−$47.40 = $36.70 against RM25.2B ⇒ **RM6.9B/$10**. Both contradict the stated RM6.0B — at least one number is stale; report both readings, never silently pick one. **Recipe:** whenever a static block pairs a sensitivity/coefficient with derived threshold prices, recompute the implied coefficient from the sealed anchors and compare. When they diverge, label which number is EVIDENCE-sealed (JSON) vs narrative-static (HTML) — the sealed side usually wins, but the divergence itself is the finding.

42. **Verify each cited number maps to the field it CLAIMS — real number, wrong layer is conflation, not fabrication.** (PROVEN 2026-08-04, PETRONAS vitals) A narrative said "governance 22/100 breached." 22 exists in the JSON — but as the SOUL *layer* score; the governance *tripwire* itself scores 33.3. For every number a narrative cites: (a) locate it in the data, (b) identify which field it actually came from, (c) check that matches the field the narrative claims. Report "number real, attribution wrong" as its own verdict class (⚠️ MISREAD), distinct from fabrication (❌) and accuracy (✅). Composite scores also get recomputed from layer weights (e.g. 0.40×75.5 + 0.35×33.6 + 0.25×22.2 = 47.51 vs displayed 47.5) — cheap, deterministic, catches both rounding and wrong-weight bugs.

43. **Canonical-vs-legacy route divergence after a page migration — two public URLs serving two generations of the same page.** (PROVEN 2026-08-04, `/vitals/` vs `/wealth/vitals/`) After a page moves to a canonical route, the legacy route often still serves the OLD file with no redirect — and the two surfaces give contradictory answers about the same subject (here: the same institution's pulse = 0 VOID on canonical, 48 HOLD on legacy; the legacy file also duplicated the narrative section 2×). **Detection:** probe BOTH routes; diff sizes (`curl -s <url> | wc -c`) and grep version-specific markers — amendment IDs, override logic, duplicated section headings (`grep -c 'SECTION NAME' fileA fileB` — a duplicated block in one file but not the other marks different generations). Ground truth for which route is canonical: the sealed data JSON's `public_url` field AND the site's own nav hrefs. **Fix:** Caddy 301 legacy → canonical (one public surface). **Rule:** when auditing a page claim, enumerate ALL routes serving that page (sitemap.xml, llms.txt, nav, JSON `public_url`) and probe each — the divergence itself is an F2 finding.

44. **Computed-but-unused override — the display contradicts its own declared state.** (PROVEN 2026-08-04, vitals hero) A page computed `PULSE_VERDICT_OVERRIDE = EXTRACTION_LOCK_ACTIVE ? "VOID" : null` but the render path used `verdict(PULSE)` (0 → HOLD since 0 < 60) and never consumed the override. Result: hero badge showed "0 HOLD" while the 0-band legend AND the crisis banner both said VOID — three states on one screen. **Audit step:** for every override/lock constant a page's JS computes, grep that it is actually CONSUMED in a DOM write (defined ≠ consumed): `grep -n 'OVERRIDE' index.html` — if it appears only in a `const` definition and never on a `textContent/innerHTML/className` line, it's dead. Compare what banner/legend declares vs what the hero renders. This is pitfall #13's internal-self-contradiction check applied to JS state — run the page's own declared invariants against its own rendered output.

45. **A narrative can be TRUE for the seal it cites yet STALE now — diff the claim's seal anchor against the current reseal before judging.** (PROVEN 2026-08-04, PETRONAS vitals) An essay described the engine's answer as "48 HOLD" — accurate for the 2026-07-24 seal it referenced, but the engine had resealed 2026-08-03 (`AMEND-2026-08-03-001`: extraction 70.5% PAT > 65% pacemaker → BODY override 0, composite VOID, dividend-stop lock). The claim is a **historical snapshot, not a fabrication** — classify "stale one amendment" and report the CURRENT state alongside; calling it fabricated is itself an F2 violation. **Protocol:** when a narrative quotes a score/verdict, find the claim's date/seal anchor, then read the live data file's reseal metadata: `python3 -c "import json; d=json.load(open(f)); print(d.get('reseal_date'), d.get('reseal_from'), d.get('next_audit'), d.get('f2_audit'))"`. If the engine resealed after the claim's anchor → stale-but-true. Note: pre-override fields can still hold the old value in the JSON (`pulse: 47.5`) while the override only exists in page JS or amendment fields — read the amendment fields, not just `pulse`.

46. **Live-vs-disk byte delta behind a CDN/WAF is usually edge injection, not corruption — diff and identify the delta before declaring drift.** (PROVEN 2026-08-04, arif-fazil.com unified-header SOT audit) Live fetch of `/_shared/unified-header.html` returned 11,467 bytes; the disk SOT file was 10,529 — a 938-byte delta that looked like corruption or a self-reference loop. `diff` showed the ENTIRE delta was Cloudflare's injected `<script>window.__CF$cv$params={r:'...',t:'...'}` + challenge-platform loader appended at the end. Disk was byte-perfect versus live minus the injection. **Recipe:** `curl -s <url> -o /tmp/live.html; wc -c /tmp/live.html <disk-file>; diff /tmp/live.html <disk-file>` — then READ the diff hunks. If the delta is a CF `__CF$cv$params` / challenge-platform / turnstile block, the verdict is CLEAN with the injection accounted for, not "content drift." On any site behind an orange-cloud CDN, never compare byte counts without diffing first.

47. **"File absent from disk" claims must be probed against EVERY webroot the reverse proxy maps — derive roots from the Caddyfile, not a guessed path.** (PROVEN 2026-08-04, same audit) `find /var/www/html/arif -name 'unified-header*'` returned empty → near-miss "DISK KOSONG / file lost" alarm. The file was fine: Caddy serves `/_shared/*` from a DIFFERENT root (`/var/www/html/_shared`) than the main site (`/var/www/html/arif`). Absence at one root proves nothing. **Protocol:** before any absence verdict, grep the Caddyfile for `root` directives/handlers, enumerate all roots, and probe each. Companion lesson: a grep hit for a scary pattern ("self-reference") must be NATURE-CHECKED by reading the hit line — SELF-REF=1 was line 2's HTML comment (`<!-- ... loaded via unified-header-loader.js -->`), not a `<script>` self-loop. grep finds text; only reading the line proves risk.

48. **Post-action summary is a CLAIM, not a reflection — verify before presenting it as fact.** (PROVEN 2026-08-04, FED FLAME FRAME audit) After executing infrastructure changes (provider cleanup, bind-migration, archive-on-disk), the natural temptation is to write a tight summary table: "Drop X ✅, Drop Y ✅, single endpoint ✅". This is a NEW claim set, not a record of intent. The user confronted the table with ground truth and revealed three false conclusions: "OpenRouter dropped" (still tracked, $0.50 BLIND), "MuleRouter dropped" (orphaned in DB, balance preserved), "single endpoint :4000" (live but 401-gated). The summary was confidently wrong because it was written from the *intent* of the cleanup, not from a *live probe*. **Rule:** any table or bullet list that says "X is Y" after an action must be backed by a live probe in the SAME response — `curl`, `sqlite3 ... SELECT`, `systemctl is-active`, `ss -tlnp`. If the probe doesn't fit in the response, the summary is premature. The "Reality check vs ringkasan kau" pattern (user shares a table challenging each claim) is the failure mode this rule prevents. Cross-reference: pitfall #1 (self-claims need live probing) applies to on-call status reports; this pitfall is its twin for **post-action deliverables**, where the very fact of having taken action makes the agent MORE confident, not less.

49. **Two systemd units for the same port — only the active one holds the listener; the loser is "dead" but its config is still the field's source of truth.** (PROVEN 2026-08-04, litellm-proxy) When auditing a service bound to a port, FIRST check `systemctl status <unit>` for BOTH candidate units, not just one. The active unit may NOT be the one referenced by `memory` or recent docs. Recipe: `systemctl list-units --type=service --state=active | grep <name>` to find the actually-running unit, then `cat /etc/systemd/system/<unit>.service` to read its `ExecStart`. The dead unit's config is audit noise; the active unit's `ExecStart` (plus any drop-in overrides) is the binding truth. Also check `ps -o pid,unit -p <PID>` and `cat /proc/<PID>/cgroup` — the cgroup path tells you which unit spawned the process, even if the systemd unit name is non-obvious (e.g. `system.slice/litellm-federation.service` vs the `litellm-proxy.service` reference in memory). When changing bind behavior, edit the ACTIVE unit's drop-in (e.g. `/etc/systemd/system/<unit>.service.d/override.conf`), NOT the unit itself — preserve the canonical main file, mutate via drop-in. See `references/litellm-nodb-fix.md` for the broader "no-DB" override pattern this often co-occurs with.

50. **Repo ≠ deployed: the three-way path split that makes "fixed" claims false.** (PROVEN 2026-08-04, arif-fazil.com gold-api) When a claim says "fixed X in repo + restarted server", verify the fix landed in the file the RUNNING SERVER actually reads — which is often NOT the repo file. arif-fazil.com has a three-way split: (1) **repo** `/root/arif-fazil.com/sites/arif-fazil.com/public/gold/api/fetch_gold.py`, (2) **deployed** `/var/www/html/gold/api/fetch_gold.py` (the one the Node.js server reads via `SCRIPT = path.join(__dirname, 'fetch_gold.py')`), (3) **WEALTH engine** `/root/WEALTH/engines/commodity/gold-api/fetch_gold.py` (separate copy). The NaN fix (`_sanitize_nan`) existed in the repo copy (mtime 2026-08-04) but the deployed copy was stale (mtime 2026-08-03) — live API still returned 500 with `Invalid JSON: Unexpected token 'N'`. The claim "restart = fix applied" is false when the fix file ≠ the served file. **Detection recipe:**
    ```bash
    # 1. Find the PROCESS that serves the endpoint
    ps aux | grep -E "server.js|fetch_gold|gold-api" | grep -v grep

    # 2. Identify the FILE it reads (check server.js __dirname or script path)
    grep -n "SCRIPT\|__dirname\|path.join" /var/www/html/gold/api/server.js

    # 3. Compare repo file vs deployed file
    diff /root/repo/path/to/file /var/www/html/deployed/path/to/file

    # 4. Check mtimes — deployed should be NEWER than (or same as) repo
    stat -c '%y %n' /var/www/html/*/api/*.py /root/repo/*/api/*.py

    # 5. Test the ACTUAL endpoint for the specific error pattern
    curl -s https://domain/api/endpoint 2>&1 | grep -c "NaN\|error\|500"
    ```
    **Fix:** copy repo file to deployed path, restart the serving process, re-test. Never declare "fixed" until the LIVE endpoint passes. Companion pitfalls: #11 (deployed edits not in repo), #24 (config ≠ runtime), #48 (post-action summary ≠ fact).

51. **Cross-VPS LLM routing over Tailscale = bind to Tailscale IP, drop localhost trust gate.** (PROVEN 2026-08-04, FED FLAME FRAME v2 cross-VPS expansion) To enable a federated agent on VPS-B (e.g. WawaBot on srv1642546) to route through VPS-A's LiteLLM (e.g. FED on af-forge), bind LiteLLM to the Tailscale IP (`100.64.0.2`), NOT `127.0.0.1` and NOT `0.0.0.0`. `127.0.0.1` blocks all off-host traffic including tailnet. `0.0.0.0` exposes the proxy to the public internet (defeats the trust layer). The Tailscale IP makes the trust layer explicit: only nodes on the tailnet can reach `:4000`. **No auth needed** — Tailscale mesh IS the auth layer (encrypted WireGuard + ACLs). The drop-in override pattern is: `ExecStart=/bin/bash -c '...; exec /usr/local/bin/litellm --config <yaml> --port 4000 --host 100.64.0.2'`. Verification: `curl -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4000/v1/models` should return 000 (localhost blocked clean); `curl -o /dev/null -w '%{http_code}\n' http://100.64.0.2:4000/v1/models` should return 200. Tailscale reachability check: `ping -c1 -W2 <tailscale-ip>` — 0.5ms = mesh healthy. Config snippet for the remote VPS: `/root/.openclaw/federation/wawabot-env.example` (af-forge test artifact, proves the pattern). Companion: `federation-mesh-networking` for the underlying Tailscale mesh; `provider-routing-zen` for the routing role. **SECURITY:** this is TAILNET-ONLY — if Tailscale ACLs allow `:4000` to a non-trusted node, the no-auth pattern becomes a vulnerability. Confirm Tailnet ACL BEFORE binding. Audit recipe: `tailscale status` for the active node list, then check ACL outbound rules for the bind port.

52. **Path confusion: `/root/HERMES/` ≠ `/root/.hermes/` — verify multiple roots before claiming absence.** (PROVEN 2026-08-04, cognitive engine audit) When searching for code/config and finding nothing at one path, DO NOT conclude "doesn't exist" — check alternate roots. The federation has TWO Hermes-related directories with different purposes:
    - `/root/.hermes/` — Hermes Agent runtime config (skills, plugins, cron, memories)
    - `/root/HERMES/` — Hermes Agent source code + cognitive modules (21 files, 5,949 LOC at `/root/HERMES/cognitive/`)
    
    Checking only `/root/.hermes/cognitive/` returns empty → false claim "draft sahaja" → user corrects with actual 5,949 LOC. **Detection:** when you `find` or `ls` a path and get nothing, `find /root -maxdepth 3 -name "<target>"` before concluding. The directory naming convention (`.` prefix = runtime, no prefix = source) is NOT documented in any config — you must probe both.
    
    **Companion:** pitfall #1 (self-claims need live probing) is the general principle; this pitfall is its specific manifestation when the verification probe itself targets the wrong path. A probe that hits the wrong path produces a false NEGATIVE — the most dangerous kind of "verification" because it masquerades as evidence.

## References

- `references/vitals-narrative-audit-2026-08-04.md` — Worked example: auditing a WEALTH vitals narrative + live page. SPA-swallowed API endpoint (one-line fix), back-solved sensitivity contradiction, layer-vs-tripwire conflation, composite recompute, F13-hold proposal pattern.
- `references/mcp-contract-drift-audit-fix.md` — Full audit → fix → regenerate → startup-verify pipeline for MCP deployment contract drift. 6 phases: survey, classify, fix (one commit per P0), regenerate surfaces from registry, add fail-closed startup verification, verify live. GHOST_TOOLS pattern, subagent collision handling, build identity recipe. Proven on GEOX P0 deployment audit 2026-07-19 (7 items).
- `references/react-spa-audit-pattern.md` — React SPA-specific audit techniques (catch-all 200 problem, client-side vs server-side redirects, multiple data store disambiguation). Proven on arif-fazil.com audit 2026-07-18.
- `references/mcp-organ-registry-audit.md` — MCP organ registry audit pattern for arifOS federation organs. Three-layer verification (self-report → behavioral → source cross-check), decorator-vs-wire distinction, boundary enforcement understanding. Proven on WELL organ audit 2026-07-18.
- `references/observability-pipeline-verification.md` — Observability system deployment verification (Kabarkan pattern). Three-layer pipeline: in-process local backend vs NATS stream vs standalone worker. VAULT999 seal claim verification. Covers the case where one layer works while another silently fails. Proven on Kabarkan audit 2026-07-24 (false VAULT999 seal claim, broken standalone worker masked by working local backend).
- `references/wcag-contrast-verification.md` — Independent WCAG contrast ratio verification. Recompute every claimed ratio from hex values before ratifying a design-token spec. Catches wrong ratios AND wrong verdict labels. Proven on PRIMER-1 audit 2026-08-01 (12/13 match, 1 over-restriction caught).
- `references/config-vault-chain-verification.md` — Config/vault-chain claim verification: masked vault inspection, mtime forensics (did the change land?), live provider-seat probing (models-list ≠ quota access), registry repair verification (seats.yaml per-entity cross-check), stale-audit detection, gateway restart pattern, and the kunci-mas SOT→flat→read vault chain layout. Proven on Qwen Token Plan seat-wiring chaos 2026-08-01.
- `references/substrate-verification-pattern.md` — Deployment verification: `substrate_gate` is the receipt, not `substrate`. Two fields, different code paths — one proves the deploy took, the other is finer-grained health that may not be on the probe surface. Proven on arifOS 2026-08-02 deployment.
