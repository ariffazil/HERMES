---
name: repository-sot-inventory
description: "Establish multi-surface ground truth for any repository or live system. Probe git state, filesystem structure, live HTTP endpoints, pattern search across docs, cross-reference claims vs reality, detect duplicates/superseded documents, and produce a structured SOT report. For codebases, monorepos, kernel repos, or any system where you need to know what IS true right now."
triggers:
  - user asks 'build a SOT', 'SOT inventory', 'state of truth', 'what is the state of the repo'
  - user asks 'audit the repository', 'full inventory', 'map the codebase', 'inspect everything'
  - user asks 'what's going on with repo X', 'tell me the state of X', 'document everything in X'
  - starting work on a repo you've never touched or haven't touched recently
  - user asks to compare doc claims vs live system state
  - detecting duplicates, renames, superseded documents, or numbering conflicts in a doc corpus
  - before a significant refactor, migration, or cleanup to establish baseline truth
  - user asks to contrast/compare two agents, instruments, or forge tools across their full registry/config/card surface
  - user asks to find gaps or asymmetries between instruments in a multi-registry governance system
---

# Repository SOT Inventory — Multi-Surface Ground Truth

## Core Principle

A repository has **multiple truth surfaces** — git history, filesystem, docs directory, live services, configuration files. Any one surface can be stale, misleading, or diverged. The SOT inventory cross-references ALL surfaces to establish what IS actually true.

**The invariant:** Report what surfaces **actually say**, not what they should say. If README claims 12 tools but the health endpoint serves 8, that IS the truth — a divergence, not a bug to paper over.

## Workflow

### Phase 1: Parallel Probe (all independent surfaces at once)

Batch these — they don't depend on each other:

```bash
# 1. Git state
git log --oneline -5
git branch -a
git status --short
git diff --stat HEAD   # dirty file details

# 2. Filesystem structure
find GENESIS/ -type f -o -type d | sort   # or equivalent key dir
find docs/ -type f | sort                  # full doc tree
du -sh */                                  # size overview per key dir

# 3. Live service state (if applicable)
curl -s http://127.0.0.1:<port>/health
curl -s http://127.0.0.1:<port>/tools    # MCP surface

# 4. Key docs
read_file README.md
read_file AGENTS.md (or equivalent entry doc)
read_file identity.toml / identity config
```

### Phase 2: Pattern Search

Search for the key patterns that define this repo's domain:

```bash
# Organizational patterns
search_files --path . --pattern "VAULT999|VAULT|seal|ledger"
search_files --path . --pattern "constitutional|floor|F\d\d|F13|sovereign"
search_files --path . --pattern "identity|authority|contract|charter"

# Duplicate detection
# Numbering conflicts
ls GENESIS/ | grep -E "^0(06|07|40)" -- check for same-number files
# Filename duplicates (case-insensitive)
ls .arifos/ | sort -f | uniq -di
# Archived duplicates (bulk archived ahead of consolidation)
find docs/archive/ -type f | wc -l

# Cross-reference README claims vs live health
grep -i "tools_exposed" README.md
grep "tools_loaded" health.json
```

### Phase 3: Cross-Reference

Compare claims across surfaces:

| Claim Source | Verification Surface | What to Check |
|---|---|---|
| README.md | Live health endpoint | Tool counts, version, status |
| AGENTS.md | Actual directory structure | Paths, port numbers, services |
| GENESIS canon | Static constitution files | Numbering consistency |
| identity.toml | Live health identity_hash | Hash match |
| published_url | curl probe | Site actually up? |

### Phase 4: Structured Report

Write a section-by-section SOT report covering:

1. **Git State** — HEAD commit, branch, all local branches, dirty files table (added/modified/deleted/untracked), net diff stats
2. **Key Directories** — GENESIS/ listing with sizes, docs/ tree with file counts per subdir, total .md count
3. **README Metadata** — release version, declared tool counts, live commit, owner summary
4. **Live Service State** — health check (status, version, tool counts at every surface level), floors active, VAULT999 health, runtime drift
5. **Constitutional / Domain Documents** — core files by category with sizes and status
6. **Identity / Authority Contracts** — config files for identity, authority model, security
7. **VAULT / Ledger References** — pattern search results with file list
8. **Duplicate / Superseded Detection** — numbering conflicts, case-insensitive duplicates, archived copies, redirect-only files, README-vs-health mismatches
9. **Summary Statistics Table** — counts for all dimensions
10. **Key Findings** — the 3-5 most important divergences or structural issues

## Reporting Style

- **Tables for structured data** (git state, tool counts, floor enforcement, file counts)
- **Emoji markers** for severity (⚠️ = numbering conflict, ❌ = mismatch, 🔴 = runtime drift)
- **Section numbers** (1–10) for scannability
- **Bottom-line findings** — the 3-5 things that matter most, not a firehose

### Phase 5: Agent Cards & Registry Files (Governance Repos)

For repos with agent registrations (AAA, arifOS, federation), inspect:

**Agent cards** — found in `agents/` directories and `a2a-server/agent-cards/`:
- Read `agentId`, `version`, `schemaVersion`
- Check `capabilities` (streaming, push, spawn agents)
- Count `skills[]` — note domains, floor_scope, kernel bindings
- Read `mcp_surface` — endpoints consumed, tool counts, key lanes
- Check `apexMasterSeal` — cognitive ring, thermodynamic role, jituGate
- Note status fields — ACTIVE, RETIRED, ARCHIVED, with reassignment targets

**Registry files:**
- `agent-card-registry.js` — examine the dynamic loader: auto-scan directory, `normaliseCard()` pattern, query methods
- `explorer_federation_registry.json` — dependency graph showing ordered handoff (e.g. GEOX→WEALTH→WELL→A-FORGE)
- `organ-affinity-index.json` — organ-to-domain tag mapping with branch counts
- `a2a-port-map.json` — port-to-role-status map; check for DEGRADED status or empty ports

**Registry docs:**
- `AGENT_REGISTRY.md` — read the full file; may contain SCAR entries documenting category errors (organs mislabeled as agents), registry drift (doc vs machine registry disagreements), and pending splits
- `ROOT_AGENT_CONFIG.yaml` — root config for warga, peers, forge instruments

**Public registries:**
- `public/a2a/agents.json` — the published HEXAGON + instrument cards
- `public/a2a/status.json` — A2A discovery status

**Cross-reference:** Agent card versions vs registry versions vs what docs claim. Discrepancies are findings.

### Phase 6: Federation Topology Extraction

Extract from port maps and gateway configs:

```json
"ports": {
  "A": { "port": 3001, "role": "AAA_A2A_GATEWAY", "status": "LIVE", "organId": "aaa" },
  "K": { "port": 8088, "role": "KERNEL_arifOS", "status": "LIVE", "organId": "arifos" },
  "L": { "port": 18083, "role": "WELL", "status": "DEGRADED", "organId": "well" },
  "F": { "port": 8700, "role": "AFORGE_A2A", "status": "REGISTERED", "live_mcp": 7072 }
}
```

Build a table: organ → port → role → status. Note:
- Organs on LIVE vs DEGRADED vs optional status
- A2A port vs live MCP port (may differ, e.g. A-FORGE A2A=8700, MCP=7072)
- Dependency chains from `explorer_federation_registry.json`
- Route rules from `federation_gateway.js`

### Phase 7: Hardcoded State Detection

Search for literal status strings that should come from live probes, not hardcoded code:

```bash
# In display code
search_files(pattern='"GREEN"', file_glob='*.{tsx,ts,js}', path=path)
search_files(pattern="'GREEN'", file_glob='*.{tsx,ts,js}', path=path)
search_files(pattern='"SEAL"', file_glob='*.{tsx,ts,js}', path=path)
search_files(pattern="'SEAL'", file_glob='*.{tsx,ts,js}', path=path)

# In JSON schemas and configs
search_files(pattern='"GREEN"', file_glob='*.json', path=path)
```

**Categorize findings into 4 buckets:**

| Bucket | Example | Verdict |
|--------|---------|---------|
| **TYPE definition** | `type AutonomyBand = 'GREEN' \| 'YELLOW' \| 'RED'` | Acceptable — proper type safety |
| **DEFAULT value** | `"default": "GREEN"` in schema | **Flag** — optimistic default masks probe failures |
| **HARDCODED status** | `status: healthy ? 'GREEN' : 'RED'` without unknown/loading state | Acceptable if live-probed; flag if static |
| **EXAMPLE file** | `"autonomy_band": "GREEN"` in example JSON | Acceptable — just an example |

**High-severity patterns to flag:**
- `const overallVerdict = probe.allHealthy ? 'GREEN' : 'YELLOW'` — falls back to YELLOW, never RED
- `const band = task?.autonomy_band \|\| 'GREEN'` — nullish coalesce defaults to GREEN
- `drift_state: 'GREEN'` hardcoded in server response regardless of actual drift
- Schema `"default": "GREEN"` on `autonomy_band` — first render is GREEN even when no probe ran

### Phase 8: Schema Default Auditing

In JSON schemas, search for `"default"` on status/health/verdict fields:

```json
"autonomy_band": {
  "enum": ["GREEN", "YELLOW", "ORANGE", "RED", "BLACK"],
  "default": "GREEN"  /* Optimistic default — flag this */
}
```

This means the state is GREEN even when no probe has ever run. For live safety-critical displays, `"default"` should be `"UNKNOWN"` or the field should be required with no default.

### Phase 9: Public Surface Audit

Check well-known endpoints for repos that serve a web surface:
- `public/.well-known/agent.json` — A2A discovery card
- `public/.well-known/a2a-routing-policy.json`
- `public/status.json` — check for stale timestamps/build hashes vs git HEAD
- `public/a2a/status.json` — A2A-specific status
- `public/sitemap.xml`, `public/robots.txt`, `public/CNAME`, `public/_redirects`
- `public/llms.txt`, `public/llms.json` — LLM consumption surface

### Phase 10: Key State Files (Federation/Governance Repos)

For AAA or federation repos, inspect:
- `a2a-server/agent-state/wire_state_lineage.json` — verdict→A2A wire mapping (SEAL→COMPLETED, HOLD→INPUT_REQUIRED, VOID→REJECTED, ghost task blockers)
- `a2a-server/agent-state/arif_desired_behaviors.json` — F1-F13 positive behavior map
- `a2a-server/agent-state/haram_enforcement.json` — forbidden behaviors with verdicts and enforcement rules
- `a2a-server/seal_chain.js` — chain writer (version, enriched envelope format, backward compat)
- `schemas/cockpit-model.schema.json` — cockpit UI model
- `agents/_docs/AGENT_REGISTRY.md` — canonical registry with SCAR entries

### SOT Report Template

When producing a structured report, use this template:

```
## 1. Git State
- HEAD commit, branch, dirty files (with git diff for deletions)

## 2. Package Identity
- name, version, license, tech stack, key deps

## 3. Federation Topology
- organ → port → role → status table
- dependency graph, route rules

## 4. Agent Cards & Registry Files
- Warga lane cards
- External/forge instrument cards
- Registry files and versions
- Retired/subsumed agents and reassignments
- Registry drift (doc vs machine registry)

## 5. Cockpit/UI Display Code
- Entry points, sub-panels, support modules

## 6. Hardcoded State Findings
- By file with line numbers, categorized (type/default/hardcoded/example)

## 7. Key State Files
- Wire state mapping, desired behaviors, enforcement maps

## 8. Notable Observations
- Retired agents, DEGRADED organs, stale timestamps
- Schema-level optimism risks
- Doc-vs-filesystem discrepancies
- Absence of expected patterns
```

## Pitfalls

### Tool count is not a single number
A repo can report different tool counts from different vantage points:
- Public MCP facade (`tools/list`)
- Internal registry superset
- Total declared (public + diagnostic)
- What README claims
Cross-reference ALL and explain each count's semantics.

### Runtime drift is the most common finding
Build commit ≠ live commit is normal on active branches. Document it as a finding, not a bug. It becomes actionable only when it persists across deployment cycles.

### Archive directories = intentional duplication
`docs/archive/pre-genesis-*/` with 74+ files is a consolidation move, not rot. Flag the count but note it as intentional.

### Numbering conflicts are structural, not cosmetic
When two GENESIS documents share a number (006, 007, 040), it signals either a rename collision (one supersedes the other) or parallel creation. Both need human resolution — flag both and list their sizes/dates.

### Redirect-only documents
Returned by `search_files` but contain only a redirect path. They're not duplicates, but they ARE potential confusion sources if an agent reads them expecting content. Flag them.

### README badges and config files may not match live state
Badge CI URLs, version numbers, and tool-count labels are often manually maintained and diverge from reality. Always verify against live probes, not doc claims.

### Case-insensitive filename duplicates
Linux filesystems are case-sensitive, so `REALITY_LAWS.md` and `REAlITY_LAWS.md` are different files. These are almost always accidental duplicates. Compare their content hashes to confirm.

### Phase 11: Cross-Registry Instrument Comparison

When comparing **two forge instruments** (or agents) across a federated governance system with multiple registries (e.g., AAA toolbench), do NOT read one registry at a time. Read ALL registries in parallel, then cross-reference each instrument in every surface. The goal is a dimension-by-dimension gap analysis showing which instrument is more complete on each axis.

**The registries form a federated truth graph — each surface may report different facts about the same instrument:**

| Registry | What It Tells You | Common Drift |
|---|---|---|
| `forge_instruments.yaml` | Canonical FI entry: binary, model, subagents, MCPs, version | Often stale vs agent card |
| `ROOT_AGENT_CONFIG.yaml` | Runtime routing: port bindings, citizenship, live config path, autonomy | Model mismatch vs FI entry |
| `AAA_AGENTS_REGISTRY.json` | Who's registered as warga | Instruments may be missing entirely |
| `agents.yaml` | A2A peer rules, allowed servers/tools, hook contracts | May reference indirect bindings only |
| Primary `agent-card.json` | Full capabilities, skills, MCP endpoints, authority boundary | Model often differs from FI entry |
| A2A forge card (`fi-00N-*.json`) | A2A-registered view: services, kernel deps, Ed25519 signatures | Version often older than primary card |
| Harness card | CLI-level card: model rotation per subagent | If exists, is most runtime-accurate |
| Runtime config (`config.toml` / `opencode.json`) | Live model, hooks, MCP launchers, skill dirs, thinking mode | **The ground truth** — always read this |
| MCP config (`mcp.json`) | Live MCP server definitions, transport (HTTP vs stdio), launchers | May differ from FI/ROOT surface lists |
| Skill index (`SKILL_INDEX.md`) | Stage→skill map, contrast/reflector skills, session lifecycle | Some instruments have this; others don't |

**Workflow:**

1. **Discover all surfaces** — search for the instrument name across filenames in config homes (`/root/.config/`, `/root/.arifos/`, `/root/.kimi*/`, `/root/.opencode*/`) and registry dirs (`/root/AAA/registries/`, `/root/AAA/agents/`, `/root/AAA/a2a-server/`)
2. **Batch-read all registries** — `forge_instruments.yaml`, `ROOT_AGENT_CONFIG.yaml`, `AAA_AGENTS_REGISTRY.json`, `agents.yaml` in one parallel call
3. **Batch-read all agent cards** — at least 3 locations per instrument: primary (`agents/<name>/agent-card.json`), A2A forge (`a2a-server/agent-cards/forge/fi-00N-*.json`), A2A harness (`a2a-server/agent-cards/harnesses/*.json`), and external (`agents/_external/<name>/agent-card.json`)
4. **Read live runtime configs** — the actual config file (TOML/JSON) and MCP config
5. **Read skill index** — if an instrument has one, map the contrast/reflector skills by role and tier
6. **Cross-reference systematically** — build a table with one row per dimension, one column per instrument, and a "Gap" column

**Minimum dimensions to cover (11):**
1. `forge_instruments.yaml` — entry completeness (line count, detail depth, A-R-I-F chain)
2. `ROOT_AGENT_CONFIG.yaml` — citizenship, MCP count, autonomy block, verification scripts
3. `AAA_AGENTS_REGISTRY.json` — presence or absence
4. `agents.yaml` — direct entry or indirect binding
5. Agent cards — count, versions, skills, capabilities
6. MCP surface — active count, transport (HTTP/stdio), disabled/quarantined, strategy
7. Model setup — primary, context window, vision, thinking mode, fallback chain, per-subagent rotation
8. Subagent policies — max parallel, registered count, isolation, model-per-role
9. Contrast/reflector skills — count, tiers covered (AGI/ASI/APEX), session rituals (INIT/HANDOVER)
10. Config paths — binary, config home, format (JSON/TOML), legacy paths, systemd services, hooks
11. Directory structure — AAA agent dir, external vs internal, skill index, CIV-33

**Pitfalls specific to cross-registry comparison:**
- **Model mismatch is the #1 finding.** FI entry may say `deepseek-v4-pro` while agent card says `mimo-v2.5-pro` and runtime config says something else. The runtime config is ground truth; the FI entry is aspirational.
- **Agent cards exist in 3+ locations** — `agents/<name>/`, `a2a-server/agent-cards/forge/`, `a2a-server/agent-cards/harnesses/`, `agents/_external/<name>/`. They may differ in version, model, and skills. Read ALL of them.
- **Missing from registry is a finding.** If FI-001 is absent from `AAA_AGENTS_REGISTRY.json` while FI-008 is present, that's a critical gap — call it out explicitly.
- **MCP counts are reported differently across surfaces.** FI entry may claim 15, ROOT_CONFIG may say 25, runtime config has 9 active. Explain each count's semantics (declared vs active vs total-with-disabled).
- **A-FORGE transport (HTTP vs stdio) is a design choice** — note it. Stdio is more reliable for single-session tools; HTTP allows concurrent access but has SDK limitations.
- **Skills listed in agent cards often overlap with kernel_deps.** The same skill IDs appear in both `skills[]` and `kernel_deps[]`. Kernel_deps are the required spine; skills are the full set. Both lists are canonical.
- **Contrast skill counts are not comparable across instruments with different chain architectures.** OpenCode has 12 (4 roles × 3 tiers) because it has an A-R-I-F chain. Kimi Code has 7 because it uses a simpler coordinator/worker pattern. The gap is architectural, not negligent.

- **FI number directory mismatch.** During CIV-33 reorganization, harness directories may retain old FI numbers (e.g., `fi-003-kimi-code` for an instrument now registered as FI-008). The directory name is NOT authoritative — always check `forge_instruments.yaml` for the canonical FI assignment. The `skills.json` in the harness dir may also carry the old FI number.

- **Agent card versions diverge systematically by location.** `harnesses/fi-00N-*/agent-card.json` tends to be the oldest. `agents/<name>/agent-card.json` is canonical. `a2a-server/agent-cards/harnesses/` may carry an intermediate version. `agents/_external/<name>/agent-card.json` may have a different model entirely. Expect model names to differ between harness cards (which reflect runtime reality) and external cards (which reflect the tool's native identity).

- **Only one instrument will have the full A2A registry entry.** In the current federation, Claude Code is the only forge instrument with a full governed-agent entry in `agents.yaml`. OpenCode routes through `777-forge` (spawn witness); Kimi Code has no A2A entry. This is by design — A2A entries require a running gateway process, not just a registered tool.

- **Systemd services, Telegram bots, and toolbench registries are not equally distributed.** As of 2026-07-18, OpenCode is the only forge instrument with systemd services, a Telegram bot, and a toolbench registry. This is intentional (OpenCode is the primary execution harness) but means health checks that assume all instruments have services will fail.

- **CIV-33 directories may not exist under agent-cards/.** CIV-33 orchestration placed domain profiles under `domain-atlas/`, not `agent-cards/`. The CIV-333 directory nesting scheme (identity/functions/extensions/harnesses/organs/pillars) exists at the agent-cards level, but there are no CIV-33-named subdirectories. Search for CIV-33 content under `domain-atlas/` instead.

See also: `references/fi-001-002-008-three-way-2026-07-18.md` for a complete three-way comparison with all specific gap findings.

## Verification

After producing a SOT report, verify:
- Every claimed tool count references a specific vantage point (public/internal/total)
- Every file count from `find` is real (not a stale search_files cache)
- Live health check was actually executed (not guessed)
- Duplicates were checked by file-system listing, not search_files-only (search_files may miss case-insensitive dupes)
- Key findings are ordered by impact, not by section number

## Related Skills

- `filesystem-entropy-audit` — for stale/duplicate/bloated directory cleanup (narrower: files only, no live services)
- `federation-checkup` — for cross-organ federation health (broader: multiple organs, shallower per-repo depth)
- `federation-sot-inventory` — single-organ inventory (git, docs, cross-contamination, language audit, MCP surface vs docs)
- `codebase-inspection` — for LOC/language statistics (different axis: code metrics vs truth establishment)
