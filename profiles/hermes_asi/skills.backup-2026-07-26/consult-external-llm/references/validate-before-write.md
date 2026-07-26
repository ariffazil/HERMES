# Validate-Before-Write Pattern

**Seal:** 2026-07-10
**Applies to:** Any migration, file write, or state-commit operation where corruption is possible.

---

## The Problem

When you write data to disk and *then* validate it, a corrupted write leaves the disk in a bad state. The validator says "this is wrong" but the wrong data is already persisted.

**Wrong order:**
```
1. Write data to disk
2. Validate from disk
3. If invalid → try to restore
```
Result: If step 1 succeeds and step 2 fails, disk is corrupted.

## The Fix

Validate **in-memory** before writing. If valid, write. If invalid, restore original.

```
1. Generate/process data in memory
2. Validate in-memory data
3. If invalid → reject, keep original
4. If valid → write to disk
```

**Carry_forward migration example:**
```python
# Generate migrated data
migrated = migrate(raw)

# Validate BEFORE writing
errors = validate_carry_forward(migrated)
if errors:
    raise ValueError(f"Invalid migration: {errors}")

# Only now write
tmp = TARGET.with_suffix(".tmp")
tmp.write_text(json.dumps(migrated, indent=2))
tmp.replace(TARGET)
```

**curl stdin pitfall (Python subprocess):**
```python
# WRONG — -d with stdin can cause JSON parse errors
subprocess.run(["curl", "-X", "POST", url, "-d", "-"], input=payload, ...)

# RIGHT — interpolate into -d argument
subprocess.run(["curl", "-s", "-X", "POST", url, "-d", payload], ...)
```

When using `input=` (stdin) with `curl -d`, the JSON may arrive malformed if the shell intervenes. Pass the payload directly as a string argument instead.

---

## When This Applies

- Data migrations (JSON, YAML, DB schema)
- Writing state snapshots (carry_forward, session-state)
- Config file writes
- Any time you generate data before committing it

## Key Rule

The validator must read from **in-memory**, not from **disk**, to ensure the validated state matches what was written.
