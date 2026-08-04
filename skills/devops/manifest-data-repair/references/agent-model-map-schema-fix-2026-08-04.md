# AGENT_MODEL_MAP.json Schema Fix — 2026-08-04

## Context

The AAA pre-commit hook blocked a commit on `/root/AAA/registries/models/AGENT_MODEL_MAP.json`. The hook detected bare strings in arrays that expect objects.

## Root Cause

Automated cascade updates added bare strings (e.g., `"deepseek/deepseek-v4-pro"`) to fallback chain arrays that expect objects with `{model, provider, priority, cost, note}` schema. This happened because the update tool appended model identifiers without wrapping them in the expected object format.

## Affected Entries

8 bare strings across 8 agent fallback chains:

| Agent Index | Fallback Chain Index | Bare String |
|---|---|---|
| agents[0] | fallback_chain[4] | `"deepseek/deepseek-v4-pro"` |
| agents[1] | fallback_chain[4] | `"deepseek/deepseek-v4-pro"` |
| agents[2] | fallback_chain[4] | `"deepseek/deepseek-v4-pro"` |
| agents[3] | fallback_chain[5] | `"qwen-token-plan/deepseek-v4-flash"` |
| agents[4] | fallback_chain[8] | `"kimi-k3"` |
| agents[9] | fallback_chain[7] | `"kimi-k3"` |
| agents[10] | fallback_chain[4] | `"deepseek/deepseek-v4-pro"` |
| agents[13] | fallback_chain[3] | `"kimi-k3"` |

## Fix Applied

Converted each bare string to an object with:
- `model`: the bare string value
- `priority`: 99 (low priority, auto-fixed)
- `cost`: "unknown"
- `note`: "auto-fixed from bare string"

## Validation

After fix:
- JSON validated: `python3 -c "import json; json.load(open('...'))"`
- Pre-commit hook passed: `git commit` succeeded
- Commit: `6563395a` on AAA main branch

## Prevention

When automated tools modify the AGENT_MODEL_MAP.json:
1. Always validate JSON schema after modification
2. Check that arrays containing objects don't receive bare strings
3. Run `python3 -c "import json; json.load(open('...'))"` before staging
4. The pre-commit hook will catch this, but it's better to validate earlier

## Class-Level Pattern

This is a general pattern for any structured JSON manifest where automated tools modify arrays. The detection and repair scripts in the parent skill (`manifest-data-repair`) can be reused for any similar schema violation.
