---
name: Federation SOT Inventory
version: 1.0.0-2026-07-13
description: Run a comprehensive multi-dimensional State-of-Truth inventory on any arifOS federation organ repo (WELL, arifOS, A-FORGE, AAA, GEOX, WEALTH, profile, etc). Covers git state, documentation integrity, data cross-contamination, language red-flag audit, diagnostic claims vs evidence, live MCP surface vs documented surface, and file-path consistency.
owner: arifOS federation
triggers:
  - user asks for a SOT inventory, repo audit, truth check, or inventory report on a federation organ
  - user asks to verify claims against state for a repo
  - post-consolidation or pre-release verification of a federation organ
  - cross-organ cleanup to detect data from one organ stored in another data directory
no-triggers:
  - health check (use federation-checkup instead)
  - code review (use github-code-review)
  - federation status (use federation-checkup)
authority: REFLECT_ONLY
archived: false
epistemic_scope: |
  Reads git state, files, directory contents, hits running MCP servers over
  HTTP. Does not modify the repo. All findings are advisory.
---

# Federation SOT Inventory Methodology

Run this methodology against any arifOS federation organ repo to produce a structured State-of-Truth report. The report is saved as `SOT-INVENTORY-YYYY-MM-DD.md` in the repo root.

## Required Context

Before starting, establish:
- **Target path:** `/root/<ORGAN>` (e.g., `/root/WELL`, `/root/A-FORGE`)
- **Organ role:** What does this organ do? (REFLECT_ONLY? JUDGE? EXECUTE?)
- **MCP port:** Port the organ runs on (check `/root/CONTEXT.md` or `CONTEXT.md` in the repo)
- **Live MCP endpoint:** `http://127.0.0.1:<PORT>/health` and `http://127.0.0.1:<PORT>/mcp`

## Step-by-Step Protocol

### Phase 1 — Git State

```bash
cd /root/WELL  # adjust per target
git log --oneline -1
git branch -a
git status --short
```

Capture:
- HEAD commit hash + message
- Active branch (compare against what `INVARIANTS.md` or `AGENTS.md` claims is canonical)
- All local and remote branches
- Dirty files list

**Pitfall:** A clean working tree (`git status --short` produces no output) does NOT mean the running server matches the repo HEAD. Always cross-check.

---

### Phase 2 — README & Documentation Integrity

1. Read the full README.md
2. Check for:
   - **Duplicate sections** — same text block appearing in two places (e.g., APEX bridge section)
   - **Redundant SOT-MANIFEST blocks** — more than one frontmatter block
   - **Stale examples** — hardcoded JSON responses with wrong tool counts or port numbers
   - **Cross-referenced files that don't exist** — match every file mentioned in README's architecture diagram / key-files table against actual files on disk
3. Check other root-level `.md` files (CONTEXT.md, BOUNDARY.md, INVARIANTS.md, etc.) for consistency

**Pattern:** README often references `TOOL_SURFACE.md` and `FEDERATION_CONTRACT.md` at the repo root. These frequently end up in `scripts/governance/` instead. Check both locations.

---

### Phase 3 — Data Directory Cross-Contamination

```bash
ls -la /root/<ORGAN>/data/   # or search_files
```

Read every file in `data/`. Look for:
- **Session events from OTHER organs** — e.g., `WEALTH_SESSION_INIT` events in WELL's `data/vault999.jsonl`
- Actor IDs that don't belong to this organ
- Event types prefixed with other organ names

**Pattern:** During consolidation or session-sharing, data from WEALTH, arifOS, or A-FORGE leaks into WELL's data directory (or vice versa). Any file whose event_type or actor_id references a different organ is mis-stored.

---

### Phase 4 — Language Red Flags

Search the entire repo for:

1. **'quantum'** — Federation organs sometimes use this as domain language (meaning "hidden pattern detection", not quantum physics). Flag any usage that isn't clearly within the organ's own documented three-tier diagnostic model. If no misuse, note "domain-correct."

2. **Diagnostic claims** — Search `diagnos*` across all `.md` files. Categorize each hit:
   - `guardrail` — "WELL does NOT diagnose" (clean)
   - `claim` — assertive language like "this indicates X" without evidence tagging
   - Flag any assertive claim not prefixed with CLAIM / PLAUSIBLE / HYPOTHESIS / ESTIMATE / UNKNOWN

3. **Self-certification language** — Patterns like "verified", "certified", "proven", "guaranteed". Cross-reference against the organ's Gödel lock or self-certification guardrails if they exist.

---

### Phase 5 — Live MCP Surface vs Documented Surface

Query the live server:

```bash
# Health endpoint
curl -s http://127.0.0.1:<PORT>/health | python3 -m json.tool

# tools/list
curl -s -X POST http://127.0.0.1:<PORT>/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

Compare against documented tool sets:
- **TOOL_SURFACE.md** (if it exists) — lists canonical set
- **README.md** — may claim a specific count
- **INVARIANTS.md / CONTEXT.md** — may state canonical counts
- **Various GENESIS documents** — may list tools

Compute the delta: `live_tools - documented_tools = undocumented_extras`.

**Key check:** Does the health endpoint return different fields than the server.py code suggests? If so, the running binary is from a different commit than HEAD.

---

### Phase 6 — File Path Consistency

Cross-reference every file path mentioned in README, AGENTS.md, and key docs against actual disk locations:

- `TOOL_SURFACE.md` at root vs `scripts/governance/TOOL_SURFACE.md`
- `FEDERATION_CONTRACT.md` at root vs `scripts/governance/FEDERATION_CONTRACT.md`
- Any `docs/` references that point to non-existent paths
- Scripts referenced in README `build/test/deploy` sections

---

### Phase 7 — Compile Report

Write a structured markdown report at `/root/<ORGAN>/SOT-INVENTORY-YYYY-MM-DD.md` with:

1. **Git state** table (HEAD, branch, dirty files)
2. **README health** — issues found
3. **Data directory** — cross-organ leakage findings
4. **Language audit** — quantum, diagnostic claims, self-certification
5. **MCP surface** — live vs documented delta
6. **Additional quality issues** — numbered table with severity (HIGH/MEDIUM/LOW)
7. **Summary** — "What's Good" checklist + "What Needs Attention" priority list

Each finding should include:
- Exact file path and line numbers
- The actual text or evidence
- Clear verdict (GREEN/clean or RED/problematic)
- Severity rating

---

## Reference Material

- `references/2026-07-13-WELL-SOT-inventory.md` — Full session trace from applying this methodology to the WELL organ. Includes exact commands, discrepancies found, and language audit results.

---

## Pitfalls

- **Clean working tree != running server matches HEAD.** The running `well.service` (systemd) may be built from a different branch or commit than what `git log` shows. Always query the live MCP endpoint and compare its fields against the current `server.py`.
- **Docs claim a static tool count** but the SOMATIC_TOOLS set may have grown or changed. The count in README/TOOL_SURFACE.md is frequently stale.
- **Sets hide duplicates** — Python sets deduplicate silently. `{"a", "b", "a"}` has length 2. Duplicate entries in SOMATIC_TOOLS are a quality signal (sloppy authoring) even though they don't affect runtime.
- **data/ directory may have hidden files** or binary blobs. Use `search_files(target='files', ...)` rather than `ls` to catch everything.
- **Diagnostic language is often nested in guardrails** — count all `diagnos*` hits manually rather than trusting a raw count. A file may say "not a diagnostic authority" 20 times (clean) and "diagnostic pattern detected" once (problematic).
- **Some files referenced in docs are pointer-only** — FEDERATION_CONTRACT.md may be a 5-line bootstrap pointing to `/root/arifOS/FEDERATION_CONTRACT.md`. This is intentional post-consolidation, not an error. Verify the pointer target exists.
