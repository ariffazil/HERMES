# Pitfall: Test Fixtures Must Pass Governance Gates

The #1 bug when building governed stores: **test fixtures are entries too**.

## The Problem

Governed stores reject entries that fail the Gödel lock. But tests often create
minimal fixtures that omit required fields. The entry silently fails the gate,
the store stays empty, and downstream assertions fail with confusing errors
(e.g., "No memories stored" instead of "GÖDEL-3 violation").

## Symptom

```
AssertionError: '[OBS' not found in '# Governed Memory\n\nNo memories stored.\n'
```

The render test creates an OBS entry, calls `add_entry`, then checks the render.
But `add_entry` silently rejected the entry because OBS requires evidence.

## Fix

Always satisfy governance rules in test fixtures:

```python
# OBS needs evidence
entry = create_entry(
    content="test fact",
    truth_class="OBS",
    provenance_source="test",
    provenance_evidence="observed in test output",  # REQUIRED for OBS
)

# Constitutional needs ratified_by (add manually after create_entry)
entry = create_entry(content="test", authority_level="constitutional",
                     provenance_source="test")
entry["authority"]["ratified_by"] = "arif:2026-07-12"  # REQUIRED for constitutional

# INT/SPEC are safe defaults — no extra fields needed
entry = create_entry(content="test", truth_class="INT", provenance_source="test")
```

## Prevention

Always check `add_entry` return value in tests:

```python
ok, msg = add_entry(entry)
self.assertTrue(ok, f"Entry rejected: {msg}")
```
