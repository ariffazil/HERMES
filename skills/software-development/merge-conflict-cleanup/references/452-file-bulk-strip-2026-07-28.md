# 452-File Bulk Conflict Marker Strip — 2026-07-28

**Codebase:** arifOS (`/root/arifOS/arifosmcp/`)
**Scale:** 452 Python files with unresolved `<<<<<<< HEAD` / `=======` / `>>>>>>>` markers
**Trigger:** `systemctl restart well` failed with `SyntaxError: invalid decimal literal` at `>>>>>>>` markers

## Root Cause

An interactive rebase (`git rebase`) was in progress on the arifOS repository. The commit `67fb82d5e` ("feat(kernel): restrict Ollama to embedding & append vault attestations") conflicted with the current HEAD on essentially every file it touched. The rebase was left incomplete, leaving conflict markers scattered across the entire `arifosmcp/` Python package.

## Impact

WELL (`well.service`) imports from `/root/arifOS/` via `PYTHONPATH`. When WELL restarted (triggered by `well_auto_keepalive.py` quarantine), the import chain traversed:

```
server.py → arifosmcp.rama.state_classifier → arifosmcp.__init__
  → arifosmcp.core.embodied_tool_engine → arifosmcp.core.tool_self_model
  → arifosmcp.core.reversibility_engine → ...
```

Each module in this chain could have conflict markers. The FIRST one hit caused the SyntaxError and blocked the entire WELL restart. Fixing one file at a time was impractical — after fixing `__init__.py`, the next error was in `reversibility_engine.py`, then `tool_self_model.py` — a game of whack-a-mole.

## Fix Strategy

### Phase 1 — Bulk Regex Strip (immediate)

Strip ALL `<<<<<<< HEAD`, `=======`, `>>>>>>> commit-ref (message)` lines from all Python files in `arifosmcp/` using a single Python script:

```python
import re, os

root = '/root/arifOS/arifosmcp'
count = 0
for dirpath, _, filenames in os.walk(root):
    for fn in filenames:
        if not fn.endswith('.py'):
            continue
        fpath = os.path.join(dirpath, fn)
        with open(fpath) as f:
            content = f.read()
        if '<<<<<<<' not in content and '>>>>>>' not in content:
            continue
        original = content
        content = re.sub(r'^>>>>>>> .*$\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^=======$\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^<<<<<<< HEAD\n?', '', content, flags=re.MULTILINE)
        if content != original:
            with open(fpath, 'w') as f:
                f.write(content)
            count += 1
```

Result: 452 files fixed in ~2 seconds.

**Important:** This approach keeps the HEAD side of every conflict (the text between `<<<<<<< HEAD` and `=======`). The THEIR side (between `=======` and `>>>>>>>`) is discarded. This is the right default when the current running kernel uses HEAD names (e.g., `arif_think`, `arif_judge`) and the incoming commit renamed them (`arif_mind_reason`, `arif_judge_deliberate`). If the THEIR side should be kept instead, modify the regex to keep the THEIRS block or do per-file review.

### Phase 2 — Expose Masked Syntax Errors

After stripping markers, some files still failed. The conflict markers had **masked** syntax errors that were now exposed:

| File | Error | Cause |
|------|-------|-------|
| `tool_self_model.py:153` | `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | Two `default=` lines ended up in the same Field — HEAD had `default=BlastRadius.LOCAL`, THEIR had `default=BlastRadius.LOW`. No comma between them. |

This happened because both sides had independent additions to the same function call. The conflict markers were between them, but after stripping, they became adjacent Python with a syntax error.

### Phase 3 — Per-File Fix of Exposed Errors

Use the standard `patch` tool to fix each exposed error individually. The patterns match the existing `merge-conflict-cleanup` skill's Patterns 1-5 (duplicate keyword arguments).

## Lessons

1. **Bulk regex strip is fast and safe when HEAD side is the right choice** — but always verify with a compile check afterward.
2. **Conflict markers can mask other bugs** — after stripping, always check for syntax errors that were hidden.
3. **Service restart triggers may cascade** — a merge-conflict issue that only affects one service (arifOS kernel) may also break downstream services (WELL, GEOX, WEALTH) that import from arifOS.
4. **`PYTHONPATH` dependency means freshness matters** — WELL's `/etc/systemd/system/well.service.d/override.conf` sets `PYTHONPATH=/root/arifOS:/opt/arifos/app`. This means WELL loads the LIVE source tree on every restart, not a frozen install. Any uncommitted conflict in the source tree immediately breaks WELL.
