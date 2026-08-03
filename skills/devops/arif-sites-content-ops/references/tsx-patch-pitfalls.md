# JSX/TSX Editing Pitfalls for arif-fazil.com

## patch tool silently fails on JSX/TSX blocks

**Problem:** The Hermes `patch` tool reports `success: true` for replace-mode patches on
`.tsx` files but changes may NOT persist to disk — especially with large blocks of JSX
containing template literals (`${}`), arrow functions, or 50+ line replacements. The file
appears modified in the diff output but actually reverts to original content.

**Evidence:** This session (2026-08-03): 8+ patches on `ElectionCartographyMap.tsx` all
reported success, but `read_file` and `tsc` showed the original stale content. Had to
`git checkout` to restore and redo all edits.

**Symptoms:**
- `patch` returns `success: true` with a clean-looking unified diff
- Running `read_file` or `tsc -b` afterward shows the OLD content
- TypeScript `tsc` errors reference interface properties you know you already added
- Multiple successive patches on same file all report success but none take effect

## Reliable approaches (in order of preference)

### 1. execute_code + hermes_tools.patch() (for targeted edits)

```python
from hermes_tools import patch
result = patch(
    "/root/arif-fazil.com/sites/arif-fazil.com/src/components/Foo.tsx",
    old_string="exact old code block...",
    new_string="exact new code block..."
)
print(result['success'])  # Actually verifiable
```

Batch multiple patches in a single `execute_code` call. This is the most reliable approach
for targeted JSX edits.

### 2. write_file (for whole-file rewrites)

When changes are comprehensive (interface + data + logic + JSX all changing), just rewrite
the entire file with `write_file`. Verify afterward with `terminal(head -n 5 path)`.

### 3. terminal + git checkout (for recovery)

If patches corrupted the file structure:
```bash
cd /root/arif-fazil.com/sites/arif-fazil.com && git checkout -- path/to/file.tsx
```

## DO NOT

- Chain 4+ standalone `patch` calls on the same `.tsx` file — batch them in `execute_code`
- Trust `patch` diff output as proof of change — always verify with `read_file` or `terminal`
- Use `patch` for multi-section restructures (hero → map section swap) — use `write_file` instead

## Build & verify pattern

After any `.tsx` edit:
```bash
cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build 2>&1 | tail -10
```

Check for `tsc` errors — they're the fastest signal that edits didn't persist.
If no errors, deploy:
```bash
rsync -avz --delete /root/arif-fazil.com/sites/arif-fazil.com/dist/ /var/www/html/arif/
```

Then verify key routes:
```bash
curl -s -o /dev/null -w "%{http_code}" https://arif-fazil.com/politics/ns-election
```
