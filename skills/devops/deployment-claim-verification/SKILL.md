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

## References

- `references/mcp-contract-drift-audit-fix.md` — Full audit → fix → regenerate → startup-verify pipeline for MCP deployment contract drift. 6 phases: survey, classify, fix (one commit per P0), regenerate surfaces from registry, add fail-closed startup verification, verify live. GHOST_TOOLS pattern, subagent collision handling, build identity recipe. Proven on GEOX P0 deployment audit 2026-07-19 (7 items).
- `references/react-spa-audit-pattern.md` — React SPA-specific audit techniques (catch-all 200 problem, client-side vs server-side redirects, multiple data store disambiguation). Proven on arif-fazil.com audit 2026-07-18.
- `references/mcp-organ-registry-audit.md` — MCP organ registry audit pattern for arifOS federation organs. Three-layer verification (self-report → behavioral → source cross-check), decorator-vs-wire distinction, boundary enforcement understanding. Proven on WELL organ audit 2026-07-18.
- `references/observability-pipeline-verification.md` — Observability system deployment verification (Kabarkan pattern). Three-layer pipeline: in-process local backend vs NATS stream vs standalone worker. VAULT999 seal claim verification. Covers the case where one layer works while another silently fails. Proven on Kabarkan audit 2026-07-24 (false VAULT999 seal claim, broken standalone worker masked by working local backend).
- `references/wcag-contrast-verification.md` — Independent WCAG contrast ratio verification. Recompute every claimed ratio from hex values before ratifying a design-token spec. Catches wrong ratios AND wrong verdict labels. Proven on PRIMER-1 audit 2026-08-01 (12/13 match, 1 over-restriction caught).
- `references/config-vault-chain-verification.md` — Config/vault-chain claim verification: masked vault inspection, mtime forensics (did the change land?), live provider-seat probing (models-list ≠ quota access), registry repair verification (seats.yaml per-entity cross-check), stale-audit detection, gateway restart pattern, and the kunci-mas SOT→flat→read vault chain layout. Proven on Qwen Token Plan seat-wiring chaos 2026-08-01.
