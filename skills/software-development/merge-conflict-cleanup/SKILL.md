---
name: merge-conflict-cleanup
description: "Detect and fix merge conflict artifacts across a codebase — duplicate keyword arguments, duplicate lines, partial conflict markers, and leftover merge binder text in Python, JSON, YAML, and config files."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [merge-conflict, codebase-maintenance, cleanup, patch, python]
    related_skills: [deep-codebase-audit, repository-sot-inventory]
prerequisites:
  commands: [python3]
  tools: [patch, search_files]
---

# Merge Conflict Residue Cleanup

Clean up merge conflict artifacts — duplicate keyword arguments, duplicate lines, partial conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), and leftover merge binder text from failed or partially resolved merges in a codebase.

Python is the most common target because duplicate keyword arguments cause `SyntaxError`, but the same patterns apply to JSON, YAML, TOML, and config files where duplicate keys silently override.

## When to Use

- User reports `SyntaxError: keyword argument repeated` in Python files
- User reports merge failed with `Automatic merge failed` and wants help cleaning up
- You encounter files with visible `<<<<<<<`, `=======`, `>>>>>>>` markers
- You find files where the same argument/key appears twice in a call or constructor
- User pushed a merge commit that left artifacts across 5+ files
- After a `git merge` that had "conflicts" you notice compilation errors

## Core Pattern: Batch Read → Batch Patch → Batch Verify

### Step 1 — Discover the Affected Files

Ask the user for the error report, or search for conflict markers:

```bash
# Search for partial conflict markers (the most aggressive signal)
search_files --path . --pattern "[<]{7,7}\\s" --file_glob "*.py"
search_files --path . --pattern "[<]{7,7}\\s" --file_glob "*.{json,yaml,yml,toml}"

# Search for common merge residue patterns
search_files --path . --pattern "default=False, description=.*default=False" --file_glob "*.py"
search_files --path . --pattern "description=.*description=" --file_glob "*.py"
```

Or work from the user's error output — they'll typically provide a stack trace with `SyntaxError: keyword argument repeated` and line numbers.

### Step 2 — Read All Error Locations Simultaneously

Read the affected lines in ALL files at once (they're independent):

```python
# Read each file at the error line ±5
read_file(path1, offset=N-5, limit=10)
read_file(path2, offset=M-5, limit=10)
# ... all in one turn
```

### Step 3 — Identify Which Side to Keep

Merge conflict residue typically keeps **both** sides of a conflict. Determine which side is the correct one by looking for:
- The version that aligns with existing code around it
- The version that makes logical sense
- The version marked with a comment or more descriptive name
- In resource specs: `mime_type="text/plain"` is usually the correct intended type; `"application/json"` was the other side
- In route/policy: the more specific or well-documented version is typically the correct one
- In seals/attestations: F09 ANTIHANTU-compliant names (`HEALTHY` not `ALIVE`) are preferred

### Step 4 — Batch All Patches in One Turn

Use `patch` for each file. **Key technique for non-unique matches:**

```python
# When old_string finds 2+ matches, include more unique surrounding context.
# The most reliable anchor is a UNIQUE nearby line like uri=, name=, or a comment.

# BAD — not unique if two blocks are similar:
old_string = "mime_type=\"text/plain\",\nmime_type=\"application/json\","

# GOOD — include the unique uri= line to differentiate:
old_string = '        uri="arifos://doctrine",\n        name="arifOS Doctrine",\n        ...\n        mime_type="text/plain",\n        mime_type="application/json",'
```

**Reliable anchor types (in order of reliability):**
1. `uri=` or `key=` values (unique strings)
2. Description text (usually unique)
3. Comments on preceding lines (e.g. `# F7 humility:`)
4. Variable names that only appear in one place

**When you can't find a unique anchor:** Re-read the full file to see both occurrences, then note what differs between them (the URI, the name, surrounding comments). Include that differing text in your old_string.

### Step 5 — Handle Edge Cases

**Sibling agent already fixed a file:** The patch tool will report "Found 2 matches" or the file will no longer have the duplicate. Re-read it to verify, then skip it.

**Same pattern in multiple resources (e.g. duplicate mime_type in 2 different ResourceSpec entries):** Fix each one separately with its unique uri= anchor. Do NOT try to fix both in one patch.

**File also has pre-existing lint errors:** The lint check after patching may show pre-existing errors. As long as they're not NEW errors introduced by your edit, proceed.

### Step 6 — Batch Verification

After all patches, verify every modified file compiles:

```python
files = [all 17+ paths...]
all_ok = True
for p in files:
    try:
        compile(open(p).read(), p, 'exec')
        print(f'OK: {p}')
    except SyntaxError as e:
        if 'keyword argument' in str(e):
            print(f'FAIL: {p}:{e.lineno} — {e.msg}')
            all_ok = False

if all_ok:
    print('ALL FILES COMPILE — ZERO DUPLICATE KEYWORD ARGUMENT ERRORS')
```

## Common Duplicate Patterns

These are the most frequent merge conflict artifact patterns in Python:

### Pattern 1: Duplicate Field() keyword arguments (most common)
```python
# Before (both sides kept):
    field: str = Field(
        default="value",
        description="Some description",
        default="value", description="Some description"  # ← merge residue
    )

# After:
    field: str = Field(
        default="value",
        description="Some description",
    )
```

### Pattern 2: Duplicate constructor arguments
```python
# Before:
    SomeClass(
        arg1=val1,
        arg2=val2,
        arg1=val1,  # ← merge residue (one-liner)
    )

# After:
    SomeClass(
        arg1=val1,
        arg2=val2,
    )
```

### Pattern 3: Duplicate function call kwargs
```python
# Before:
    result = func(
        name="foo",
        value=42,
        name="bar",  # ← merge residue
    )
```

### Pattern 4: Duplicate config keys (JSON/YAML)
```json
{
  "port": 8088,
  "port": 8080,  // ← merge residue
  "host": "0.0.0.0"
}
```

### Pattern 5: mime_type duplicates in ResourceSpec tuples with identical descriptions
```python
# Two ResourceSpec entries may have the SAME description text.
# Always use the uri= line as the unique anchor.
```

## Pitfalls

1. **Don't trust line numbers from error reports without verification** — the file may have been edited since the error was generated. Always re-read the actual lines.

2. **Watch for non-unique old_string matches** — when two resources have identical duplicate patterns (same mime_type pair, same description), include the URI or name in your old_string to disambiguate.

3. **One file, multiple resources with the same duplicate** — fix each resource block independently with its unique URI/anchor. Do NOT try to patch them all at once.

4. **Sibling agents may have already fixed some files** — if a patch fails with "Found 2 matches" and re-reading shows no duplicate, the file was already fixed. Skip and move on.

5. **Pre-existing lint errors are not your problem** — the file may have other issues from before the merge conflict. Check the lint output: if only NEW errors are reported, you're fine. If pre-existing errors are flagged, note them for the user but don't try to fix them in the same pass.

6. **One-liner duplicates are easy to miss** — sometimes the merge residue is on the same line as the legitimate argument (`default=False, description=...\ndefault=False, description=...`). The second occurrence is typically the residue.

7. **Always verify compilation** — a successful patch doesn't mean the file is valid Python. Always run `compile()` or a syntax check on every modified file.

## Reference Files

- `references/17-file-batch-fixup-2026-07-27.md` — Full worked example: 17 duplicate keyword argument errors across 17 files, with patch strategies for non-unique matches, sibling-agent conflict handling, and verification.

## Verification

After cleanup:
1. Run `python3 -c "compile(open(f).read(), f, 'exec')"` on every modified file
2. If the project has tests, run `pytest` or equivalent
3. Check for remaining conflict markers with `search_files(pattern="<<<<<<<|=======|>>>>>>>")`
