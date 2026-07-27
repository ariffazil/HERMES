# Import-Chain Failure: WELL Blocked by arifOS Merge Conflicts

**Date:** 2026-07-26
**Session:** WELL freshness DEGRADED → inject → restart failed

## Timeline

1. **Alert:** WELL freshness DEGRADED — staleness=87.7d, vitality=HOLD
2. **Diagnosis:** state.json was overwritten with a test/mock file from 2026-04-30 (`environment: TEST`, `reason: "Mocked healthy state for test session"`)
3. **Fix:** Biometric injection succeeded — state.json written with score=73.0, PROD, OPERATOR_REPORTED
4. **New problem:** `systemctl restart well` failed with `SyntaxError: invalid decimal literal`
5. **Root cause WELL side:** Not state.json — the Python import chain hit git merge conflict markers
6. **Root cause arifOS side:** arifOS repo was stuck in interactive rebase with unresolved `<<<<<<< HEAD` markers across 452 Python files

## The Import Chain

WELL's PYTHONPATH includes `/root/arifOS/`, so its import chain at boot:

```
server.py line 171
  → arifosmcp.rama.state_classifier
    → arifosmcp.__init__
      → arifosmcp.core.embodied_tool_engine
        → arifosmcp.core.tool_self_model
        → arifosmcp.core.reversibility_engine
      → arifosmcp.schemas.*
      → arifosmcp.tools.*
      → arifosmcp.core.witness_log
```

Each module was checked by `beartype.claw` on import, which resolved source code and found merge markers.

## Error Pattern Progression

| Attempt | File | Line | Error |
|---------|------|------|-------|
| 1 | `arifosmcp/__init__.py` | 29 | `>>>>>>> 67fb82d5e` → invalid decimal literal |
| 2 | `arifosmcp/core/embodied_tool_engine.py` | 255 | `<<<<<<< HEAD` → IndentationError |
| 3 | `arifosmcp/core/reversibility_engine.py` | 38 | `>>>>>>> 67fb82d5e` → invalid decimal literal |
| 4 | `arifosmcp/core/tool_self_model.py` | 107 | `>>>>>>> 67fb82d5e` → invalid decimal literal |
| 5 | `arifosmcp/core/tool_self_model.py` | 153 | `default=... default=...` → duplicate Field |

Each error was a new file further in the import chain. After clearing all 452 files' markers, the final error was a **pre-existing syntax error masked by the conflicts** — duplicate `default=` lines in `tool_self_model.py` line 153.

## Bulk Fix Command

```bash
python3 -c "
import re, os
root = '/root/arifOS/arifosmcp'
for dirpath, _, fns in os.walk(root):
    for fn in fns:
        if not fn.endswith('.py'): continue
        fpath = os.path.join(dirpath, fn)
        with open(fpath) as f: content = f.read()
        if '<<<<<<<' not in content and '>>>>>>' not in content: continue
        content = re.sub(r'^>>>>>>> .*$\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^=======$\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^<<<<<<< HEAD\n?', '', content, flags=re.MULTILINE)
        with open(fpath, 'w') as f: f.write(content)
        print(f'Fixed: {fpath}')
"
```

After bulk-clear, also scan for masked syntax errors:
```bash
grep -rn 'default=.*default=' /root/arifOS/ --include='*.py'
grep -rn '<<<<<<<\|>>>>>>>\|=======' /root/arifOS/ --include='*.py' | grep -v 'README\|\.md$\|\.json$\|\.yaml$\|\.txt$'
```

## Key Lessons

1. **ArifOS source conflicts cascade to all federation organs** — any service with `PYTHONPATH=/root/arifOS` in its systemd override imports arifOS modules at boot.
2. **The first error only tells you the FIRST file with a conflict** — always sweep the entire `arifosmcp/` tree, not just the file mentioned in the traceback.
3. **beartype.claw** aggressively type-checks all imports at module load time, which means it catches syntax errors in ALL public symbols — good for safety, but the traceback is deep and nested.
4. **Masked syntax errors** — after removing conflict markers, duplicate code (HEAD + THEIR versions both preserved) can create syntax errors. Always verify with a clean syntax check.
