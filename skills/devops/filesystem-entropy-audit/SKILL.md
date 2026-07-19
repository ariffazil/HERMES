---
name: filesystem-entropy-audit
description: "Audit a directory tree for stale, duplicate, and bloated entries. Classify as LIVE/STALE/ORPHANED, quarantine safe targets, escalate decisions on active-but-bloated projects. Produces a review report."
triggers:
  - disk usage is high or growing
  - user asks to clean up or audit directories
  - quarantine or cleanup of root or project directories
  - duplicate directories (lowercase UPPERCASE pairs)
  - stale venvs or node_modules accumulating
---

# Filesystem Entropy Audit

## When to Use

- `/root` or a project directory has grown unexpectedly
- User asks "what's taking space" or "clean this up"
- Duplicate directories exist (e.g., `wealth/` vs `WEALTH/`)
- Stale virtualenvs, node_modules, or output directories accumulate
- Periodic hygiene (monthly recommended)

**For system-level optimization** (memory hogs, OS packages, Docker, swap, services, full dossier): use `vps-machine-health`. This skill handles directory trees only.

## Workflow

### Phase 1: Probe (parallel)

```bash
# Size overview
du -sh /root/*/ 2>/dev/null | sort -rh | head -30

# For each suspicious directory:
cd /root/DIR && git log --oneline -3 && git log -1 --format=%ci && git remote -v

# Check for duplicates (lowercase/UPPERCASE pairs)
ls -d /root/*/ | tr '[:upper:]' '[:lower:]' | sort | uniq -d

# Check venvs
find /root -maxdepth 3 -name "pyvenv.cfg" -exec stat -c '%y %h' {} \;
```

### Phase 2: Classify

| Category | Criteria | Action |
|---|---|---|
| **LIVE** | Has recent commits (14 days), active service, or live deploy | KEEP |
| **STALE** | No git history, no recent commits (30 days), orphaned deps | QUARANTINE |
| **BLOATED** | Active project but contains rebuildable artifacts (.venv, node_modules, build/) | CLEAN ARTIFACTS |
| **DUPLICATE** | Lowercase/UPPERCASE pair pointing to same or diverged repos | SYNC OR DROP |
| **OUTPUT** | One-time analysis output, old reports, temp artifacts | QUARANTINE |

### Phase 3: Execute safe quarantines

Move (never delete) stale/orphaned dirs to `_quarantine/YYYY-MM-DD/`:

```bash
Q=/root/_quarantine/$(date +%Y-%m-%d)
mkdir -p "$Q"
mv /root/stale-dir "$Q/stale-dir"
```

**Safe to quarantine without asking:**
- Orphaned `node_modules/` (no parent package.json)
- Stale venvs (30 days, no active project reference)
- One-time output directories
- Directories with no git history and no active service

**Always escalate to F13:**
- Duplicate repos with diverged HEADs
- Active projects with bloated .venv (recommend: delete venv, keep code)
- Directories that might be live deploy targets
- Anything referenced by systemd services

### Phase 4: Report

Write report to `_quarantine/YYYY-MM-DD/REVIEW-REPORT.md` with:

1. Summary table (Dir | Size | Status | Action)
2. Safe quarantines (already executed)
3. Needs human call (with options A/B/C and recommendation)
4. Federation org directories (all LIVE, just for reference)

## Pitfalls

### Don't delete — quarantine
Always `mv` to `_quarantine/`, never `rm`. User can restore if a classification was wrong.

### Check systemd before quarantining
If a directory might be a systemd service's `WorkingDirectory` or `ExecStart` path, check `systemctl list-units` before moving. Breaking a live service is worse than leaving stale dirs.

### Duplicate repos need sync, not deletion
When `wealth/` and `WEALTH/` both exist with different HEADs, the right move is to determine which is canonical and sync — not to delete one. Check AGENTS.md for documented canonical paths.

### GitHub is case-insensitive
`ariffazil/wealth` and `ariffazil/WEALTH` resolve to the **same** GitHub repo. Different-case local paths pointing to different URLs (HTTPS vs SSH) may still be the same repo. Check with `curl -sf "https://api.github.com/repos/OWNER/REPO"` — GitHub normalizes the name in the response. Don't treat different-case local clones as diverged repos without verifying.

### "No common ancestor" in git = same repo, different clones
When `git log A..B` returns "no common ancestor," it usually means the two local dirs were cloned independently (different URLs, different times). They may still track the same upstream. Compare `git remote -v` and check if the commit messages match before concluding they're different repos.

### AGENTS.md instruction-file bloat (MCP client warnings)

When any MCP client (Kimi Code, Claude Code, Gemini CLI, OpenCode, etc.) warns that `AGENTS.md` exceeds 32 KB, the root cause is almost always sections 8–11 of `/root/AGENTS.md`. These sections (operating procedures, pointer index, known anomalies, final notes) duplicate content already in `RUNBOOK.md` and `LANDING.md`.

**Trim map (proven 2026-07-15, saved ~3.5 KB):**

| Section | Action | Savings |
|---------|--------|---------|
| §8.1 session checklist | Compress to health-probe loop only | ~1.1 KB |
| §8.2 chaos map | Delete — already in daily memory convention | ~0.4 KB |
| §8.3 when something breaks | Collapse to 1 line → RUNBOOK.md | ~0.8 KB |
| §8.4 memory & fact check | Merge into §8.2 or §1 | ~0.3 KB |
| §9 pointer index | Replace with 1-line → LANDING.md | ~2.3 KB |
| §10 known anomalies | Collapse → RUNBOOK.md | ~0.6 KB |
| §11 final notes | Compress to single paragraph | ~0.5 KB |

**Target: 25–26 KB**, not "just under 32 KB". Underbuying means the warning fires again next time a section is added. 8 KB headroom minimum.

**Why trim root, not per-agent:** Every warga (Kimi, Claude, Hermes, OpenCode, OpenClaw) loads the same root `AGENTS.md`. Per-agent slimmer copies only fix one client. Trimming the root fixes all six.

**MCP tool count verification pitfall:** When a client reports "MCP server X connected · N tools", the count may include prompts + resources combined, not just callable tools. Verify against `arifos://schema` resource or `tools/list` response. Example: Kimi Code reported 33 tools for arifOS but the actual callable tool surface was 12 (12 tools + 19 prompts + 2 resources).

See `references/agents-md-trim-pattern.md` for the full before/after diff.

### Rename = update hardcoded paths
When renaming a directory (e.g., `arif-sites/` → `ARIF-SITES/`), immediately scan and update:
- Deploy scripts (`deploy-vps.sh`, `deploy-site.sh`)
- Caddy configs / docker-compose volume mounts
- Systemd unit files (`WorkingDirectory`, `ExecStart`)
- Any `grep -r "/old/path" /root/DIR/` hits

Use: `sed -i 's|/old-path|/NEW-PATH|g' script1 script2 script3`

Log messages and comments containing the old name are fine to leave.

### venvs are rebuildable but check requirements first
Before deleting a large venv, verify that `requirements.txt` or `pyproject.toml` exists so it can be rebuilt. If no lockfile exists, the venv IS the lockfile — be cautious.

### User may not know Python ecosystem terms
Arif is a geologist/capital strategist, not a Python developer. When referencing `.venv`, `pip`, `node_modules`, etc., explain what they are in one line before proceeding. Don't assume familiarity with Python/Node dependency management.

### Sister-workspace template clones

When multiple agent workspaces share a template parent (e.g., opencode, codex, kimi under `.openclaw/workspace-*/`), identical files can propagate silently:

```bash
# Find identical files across sister workspaces
find /root/.openclaw/workspace-* -name "FILE.md" -exec sha256sum {} \; | sort
# Same hash across workspaces = template propagation, not independent creation
```

**Pattern:** A file appearing in 3-4 workspaces with identical content and near-identical timestamps = template clone. Often a log file from a broken subsystem that each workspace inherits (e.g., DREAMS.md — 4 copies, all identical empty stubs).

**Action:** Archive to `.archive/` under the primary workspace:
```bash
PRIMARY_WS="/root/.openclaw/workspace"
for d in workspace-opencode workspace-codex workspace-kimi; do
  f=$(find "$PRIMARY_WS/../$d" -name "DREAMS.md" 2>/dev/null)
  if [ -n "$f" ]; then
    cp "$f" "$PRIMARY_WS/.archive/DREAMS-$(basename $d).md"
    rm "$f"
  fi
done
```

**Verify:** `find /root/.openclaw -name "DREAMS.md" -not -path "*/.archive/*"` returns empty.

**Trigger:** Anytime an audit finds identical files spread across parallel workspaces inheriting from the same template.

## Verification

After quarantine:
```bash
du -sh /root/*/ 2>/dev/null | sort -rh | head -10
ls /root/_quarantine/$(date +%Y-%m-%d)/
```
