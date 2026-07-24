# Per-Repo Git Push Quirks — Empirical Reference

> Last verified: 2026-07-19

## Push Results Matrix

| Repo | Push Method | Result | Notes |
|------|------------|--------|-------|
| arifOS | `git push origin main` | ✅ succeeds | **On `security/p0-boundary-federation-2026-07-19`: pre-commit `[SURFACE-GATE]` hook fires.** On `main`: standard push, no special hooks. See §SURFACE-GATE Pre-Commit Hook below. |
| AAA | `git push origin main` | ✅ succeeds | Pre-commit: Wajib Secret Gate (detect-secrets, can timeout at 30s). Pre-push: governance gate (non-blocking) |
| A-FORGE | `git push origin main` | ✅ succeeds | Standard push |
| ARIF-SITES | `git push origin main` | ⚠️ may block | Gitleaks pre-commit blocks on rootkey.json (use `--no-verify`). GitHub push protection blocks on Mapbox token in geox-app/index.html history (use git-filter-repo or allow via GitHub UI). See `references/github-push-protection-secrets.md`. |
| A2B | `git push origin main` | ✅ succeeds | Standard push |
| AssetOpsBench | `git push origin main` | ❌ 403 Forbidden | IBM-owned repo. ariffazil has no write access. Commit locally only. |
| WEALTH | `git push origin main` | ✅ succeeds (new commits) | Protected branch. Force-push rejected. Always use fresh commits. |
| GEOX | `git push origin <branch>` | ✅ succeeds | Check branch first. Often on feature branches. |
| WELL | `git push origin main` | ✅ succeeds (with REPO=) | Pre-push hook rejects without `REPO=` trailer in commit body. |

## SURFACE-GATE Pre-Commit Hook (arifOS MCP organ)

**Trigger:** Any `git commit` on the branch `security/p0-boundary-federation-2026-07-19`
in the `/root/arifOS` repo (or any branch that touches `arifosmcp/`'s MCP surface).

**What it does:** Probes the **live MCP tool surface** against the declared `surface-map`
(e.g. `arifosmcp/constitutional_map.CANONICAL_TOOLS`). If the live MCP server exposes
`N` tools and the surface-map declares `N` tools and they match by name, the commit is
allowed. If they drift, the commit is blocked.

**Output observed (2026-07-19, commit `72e9c6ac8`):**
```
[SURFACE-GATE] Running surface-map drift check...
[SURFACE-GATE] 🔴 STRICT MODE (FORGE_SURFACE_GATE_STRICT=1)
🔍 Probing live MCP surface...
   Live MCP tools: 8
     - arif_init
     - arif_observe
     - arif_think
     - arif_route
     - arif_memory
     - arif_judge
     - arif_forge
     - arif_seal
   /health exposed: 8
   /health total declared: 48

✅ SURFACE PINNED — Live tools match surface-map declarations.
[SURFACE-GATE] ✅ Surface pinned — commit allowed.
```

**Why this matters:** Editing the MCP-tool surface (renaming tools, adding modes, deleting
verbs) without updating the `surface-map` declaration will pass code review and tests,
then silently break at runtime when the federation cron probes the live organ. The
SURFACE-GATE catches this BEFORE the commit lands.

**Strict mode env var:** `FORGE_SURFACE_GATE_STRICT=1` — fail-closed. Default is
advisory. If strict mode is on (current state), commit is blocked on drift.

**When the hook fires as expected:** pre-commit, takes ~2-5 seconds, no agent action needed.
**When the hook blocks the commit:** investigate why the live MCP does not match the
declared surface-map. DO NOT `--no-verify` past this — fix the drift.

## Running arifOS Pytest Offline (2026-07-19)

`tests/conftest.py` exits hard if it cannot reach the arifOS MCP server at
`http://127.0.0.1:8088/mcp` (timeout = refused). To run pytest without the live
kernel:

```bash
PYTHONPATH=src ARIFOS_SKIP_PROTOCOL_SENTINEL=1 python3 -m pytest tests/<file.py> -q --tb=short
```

The `ARIFOS_SKIP_PROTOCOL_SENTINEL=1` env var tells `conftest.py:_check_protocol_sentinel()`
that this is a controlled offline run and to skip the protocol version check.

This is required for any agent running tests in a CI-like environment where the :8088
MCP server is not running. It is NOT a real skip in production — pre-commit / CI / live
sessions should always have the kernel up.

## Scope Discipline for Fork Commits on Dirty Working Trees

When executing a bounded fork on `arifOS` whose user-supplied spec lists specific files
(`DO EXACTLY THIS, NOTHING MORE`), the working tree may already contain pre-existing
untracked modifications from a previous session/agent. Stage ONLY the scope files —
never `git add .` or `git add -A`:

```bash
# Check what is dirty vs what is your fork
git status --short

# Stage only the fork scoped files
git add arifosmcp/data/quote_registry_v2.json \
        arifosmcp/runtime/philosophy_registry.py

# Verify what is staged before committing
git diff --cached --stat
git status --short   # lowercase = unstaged (pre-existing), uppercase = staged
```

Then commit. The pre-existing files remain unstaged for whoever owns them to commit
later. This keeps fork commits atomic and easy to revert.

If your fork touches a `philosophy_registry.py` Layer B function (e.g. `inject_philosophy`),
verify the chain still closes by re-deriving from the resolver → injector boundary:
`wisdom_quote_resolve()` returns a `ResolveResult` with `deploy_warrant`;
`inject_philosophy()` must check it and return `{}` if False. Do not trust current
in-VM behavior — re-probe via `tests/test_forge_quote_invariance.py` and the related
Layer A/B/C/D test files.

## Gitleaks False Positive Details

**File:** `sites/arif-fazil.com/public/999/rootkey.json`
**Line:** `"public_key_multibase": "z9AafFEn8WYCaE1ooiAud5gVLFapgkyyCvj34HSFgxoBK"`
**Rule:** `generic-api-key`
**Entropy:** 4.89
**Verdict:** FALSE POSITIVE — this is a public key (multibase-encoded), not a secret.
**Fix:** `git commit --no-verify` and document in commit message.

## WELL REPO= Trailer Format

The pre-push hook extracts the remote repo name from the push URL:
```
git@github.com:ariffazil/WELL.git → "WELL"
```

The trailer must match (case-insensitive, strips `ariffazil/` prefix):
```
REPO=WELL        ✅
REPO=well        ✅
REPO=ariffazil/WELL  ✅
REPO=WEALTH      ❌ (mismatch)
```

## Protected Branch Recovery (WEALTH)

If you accidentally amend a pushed commit on WEALTH:

```bash
# 1. Undo the amend
git reset --soft HEAD~1

# 2. Make a fresh commit
git commit -m "chore(zen): git hygiene — ..."

# 3. If remote is ahead (because you previously pushed the amended version):
git fetch origin main
git merge origin/main --no-edit
# Resolve conflicts with: git checkout --ours <file> && git add <file>
git commit --no-edit

# 4. Push
git push origin main
```

## Test Baselines (Pre-Existing Failures)

These are KNOWN and expected. Do not flag as regressions:

| Repo | Pre-Existing Failures | Total Pass | Notes |
|------|----------------------|------------|-------|
| arifOS | ~18-20 collection errors | 263+ pass | Import/dependency issues in test collection; ledger/archive-path files missing from `.archive-pre-zen-2026-07-12/` paths. Verified 2026-07-19 by stash-and-retest on commit `72e9c6ac8`: same failures reproduce without the patch applied, so they are pre-existing, not regressions. |
| WEALTH | 12 collection errors | N/A | pip install may fail on some deps |
| WELL | 6 test failures | 188 pass | Registry status, canonical tools, unknown telemetry |
| A-FORGE | 0 | 8/8 | Clean |
| AAA | 0 | build+test | Clean |
