# GEOX Version Format → Identity Guard Pitfall

**Discovered:** 2026-07-19, GEOX P0 deployment audit

## The Pitfall

`is_geox()` at `src/geox_mcp/server.py:378` checks:
```python
return GEOX_VERSION.startswith("v2026.") and ...
```

Changing `GEOX_VERSION` from `"v2026.07.17"` (semantic) to a raw git SHA like `"f186227a"` would **silently break identity verification** — `is_geox()` returns `False`, every health check shows `identity.verified: false`, nothing warns you.

## Why It's a Trap

A deployment audit task saying "fix version to match git SHA" looks like a mechanical fix. But the version string feeds into an identity guard that depends on the semantic format. The `build_identity` commit (`f186227a`) had **intentionally restored** semantic versioning for this reason, reverting an earlier raw-SHA version.

## The Health Endpoint Already Has All Three

| Field | Value | Use Case |
|-------|-------|----------|
| `version` | `"v2026.07.17"` | Semantic version — human-readable, starts-with guard |
| `git_version` | `"geox-f186227a"` | Git SHA — deployment drift detection |
| `build_identity` | `sha256(version\|epoch\|sha\|tool_count)` | Combined identity hash |

All three were already present before the task brief was written. No change needed.

## Probe Recipe

Before changing any version/identity string:

```bash
# 1. Find every reference to the current value
grep -n "$OLD_VALUE" "$TARGET_FILE"

# 2. Check for string-format guards nearby
grep -rn 'startswith\|== "v\|match' "$TARGET_FILE"

# 3. Check recent commits for intentional reverts
git log --oneline -5 -- "$TARGET_FILE"

# 4. Check if HEAD already has the fix
git show HEAD:path/to/file | grep "expected_fix_pattern"
```

If ANY downstream guard depends on the current format, the change is NOT cosmetic. Report the constraint and stop.
