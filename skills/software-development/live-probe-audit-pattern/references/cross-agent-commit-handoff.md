# Cross-Agent Commit Handoff

**Proven:** 2026-07-29 (Hermes committing files from opencode/333-AGI session)

## Context

In a multi-agent federation, Agent A (opencode, 333-AGI FI-001) forges and deploys infrastructure. Agent B (Hermes) verifies and commits. The commit must carry F2 evidence for every file, F11 audit attribution, and F3 witness of the originating agent.

## The Handoff Pattern

```
Agent A (forges):  Created duties/ara_breakage_detect.py, precommit-gate.sh
                   → already committed (6379a652)
                   Modified duties/aed.py, sctIngress.ts
                   → waiting for commit

Agent B (verifies): 1. git status --short → identify dirty files
                    2. Read each changed/untracked file (F2 evidence)
                    3. Verify file exists and content matches intended change
                    4. Commit with path:line evidence per changed file
```

## Commit Message Template (Conventional)

```
feat: {scope} — {summary line}

Forged by {agent} ({session_ref}).
Audited by {agent} ({session_id}).

Changes:
• {path} — {what changed}
  (path:{absolute_path}:{line_range})
  {additional F2 evidence}
• {path} — {what changed}
  (path:{absolute_path}:{line_range})
  {constitutional compliance notes, e.g. F1-gated, F13-respected}

F2 evidence: verified file content at paths listed above.
F11 audit: this commit seals the deployment receipt.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## F2 Evidence Checklist (per file)

Before committing another agent's output:

- [ ] File exists and is readable
- [ ] Line count matches expectations
- [ ] Content is syntactically valid (no obvious corruption)
- [ ] If code: imports resolve, no immediate errors visible
- [ ] If config/minifest: JSON/YAML syntax valid
- [ ] If executable: shebang present and correct
- [ ] F1/F13 gates present where applicable (e.g., "critical organs excluded")
- [ ] No hardcoded secrets, no vault.env references in committed config
- [ ] Governance claim in the file (e.g., "F1 AMANAH: revert is reversible")

## Attribution Rules

- **Originating agent**: credited in the commit body with session ID
- **Auditing agent**: credited after verifying
- **Model attribution**: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` per arifOS convention
- Do NOT co-author yourself as the forger — the forger is the originating agent

## Pitfalls

- **Already-committed files**: Check `git log --oneline <file>` before adding. The other agent may have already committed. `git status --short` won't show files where index == HEAD.
- **Deleted files**: Use `git add -A <dir>/` to capture deletions, not just `git add <file>`. Deletions require the `-A` flag to stage.
- **Untracked files not staging**: If `git add <file>` produces no output and `git status` doesn't show the file as staged, check `.gitignore` and `git ls-files` to see if it's already in the index from a prior commit.
- **Surface gate hooks**: arifOS repos may have a pre-commit SURFACE-GATE that probes live MCP. Verify it passes before force-pushing. Surface gate fail = commit blocked, not bypass.
- **Multi-file commits**: Group related changes (all AED work) in one commit. Split unrelated changes (AED + sctIngress is related as "autonomous infrastructure").

## Proven Example

```bash
git commit -m "feat: forge autonomous execution infrastructure — AED, ARA, precommit, SCT fix

Forged by opencode (333-AGI, FI-001) session SEAL-bb1502e31d3d4960.
Audited by kimi-code (FI-008).

Changes:
• duties/aed.py — AED v1: SENSE→EXECUTE→VERIFY→INGEST→SEAL loop + notify_telegram()
  (path:/root/A-FORGE/duties/aed.py:1-721)
• duties/ara_breakage_detect.py — Post-deploy degradation detector with auto-revert
  for non-critical organs (path:/root/A-FORGE/duties/ara_breakage_detect.py:1-214)
  F1-gated (git revert), F13-respected (critical organs excluded)
• duties/precommit-gate.sh — T1 push guardian (<10s): work-tree, lint, secrets, drift
  (path:/root/A-FORGE/duties/precommit-gate.sh:1-96)
• src/infrastructure/governance/sctIngress.ts:280 — SCT actor case mismatch fix
• forge_mcp_ui/* — cleanup of legacy MCP UI files (deprecated)
• AED timer active, 5-min cycles, 7/7 organs verified

F2 evidence: verified file content at paths listed above.
F11 audit: this commit seals the deployment receipt.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```
