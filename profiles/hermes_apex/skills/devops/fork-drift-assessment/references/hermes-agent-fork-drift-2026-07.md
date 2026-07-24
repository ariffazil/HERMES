# Hermes Agent Fork Drift — Real-World Example (2026-07-14)

## Context

Arif's Hermes Agent install at `/usr/local/lib/hermes-agent` was assessed against upstream NousResearch/hermes-agent. Two copies existed:

| Copy | Path | Origin | Notes |
|------|------|--------|-------|
| Running install | `/usr/local/lib/hermes-agent` | NousResearch (upstream) + ariffazil-fork remote | 1 local commit (OCR skill) |
| Fork clone | `/root/hermes-agent` | ariffazil/hermes-agent (fork) | Multiple local commits |

Version: v0.18.2 (2026.7.7.2)
Local: 4975d8ca (1 commit)
Upstream: fac85518 (NousResearch/main)
Drift: 450 commits behind

## Categorization results

| Category | Count | Key items |
|----------|-------|-----------|
| Security | 9 | Credential header stripping on cross-host redirects, Azure catalog probe hardening, urllib policy enforcement |
| Fixes | 241 | Cron deadlock (SessionDB hang), gateway shutdown drain, compression lock failures, credential pool boundaries |
| Features | 39 | Smart approvals default, DeepInfra provider, background delegation persistence, per-model token usage tracking |
| Refactors | 10 | — |
| Perf | 5 | — |

## Security patches detail (critical)

```
d83cd6f7c fix(security): secure Azure catalog probes
1f46145e0 fix(security): order sanitizer after installed hooks
92c214603 fix(security): sanitize after installed request hooks
4530a4ca4 fix(security): preserve opener-level header policy
cf34a1e8c fix(security): cover remaining catalog credential paths
27a1042b1 fix(security): preserve installed urllib policies
6e75ba7fa fix(security): enforce one redirect credential policy
a061788d4 security(providers): strip credential headers on cross-host redirects in fetch_models
b9b463f3b feat(security): expose deterministic tool output risk (#61793)
```

The credential header leak on cross-host redirects was the most critical — API keys could be forwarded to redirect targets.

## PR review interpretation

A PR had 3 changes reviewed by @teknium1:

1. **ACP stdout isolation** (builtins.print patch) → UPSTREAM ALREADY SOLVED at session.py:652 via `agent._print_fn = _acp_stderr_print`. Verdict: DROP.
2. **MiniMax image backend** → Project policy requires standalone repo for vendor plugins. Verdict: EXTRACT.
3. **SOPS env support** → No tests, config.py diff stale against current main. Verdict: REWORK against current main + add tests.

The PR was written against a stale base, which is why the config.py hunk was stale.

## Assessment

- Local changes: minimal (1 standalone file addition — OCR skill)
- Conflict risk: low
- Security urgency: HIGH (credential leak vectors)
- Recommendation: upgrade immediately via `hermes update` or `git pull origin main`
