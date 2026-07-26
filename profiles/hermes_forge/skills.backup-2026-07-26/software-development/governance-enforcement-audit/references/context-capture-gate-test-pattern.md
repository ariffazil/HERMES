# Context Capture Gate Test Pattern

> Forged 2026-07-20 during Vector #6 (Fable5 audit) implementation.

## Class of Problem

An agent with T1/T2 authority modifies boot documents (SOUL.md, AGENTS.md, INIT files, memory tiers) and shapes future agent sessions — capturing context without F13 sovereign ack. The fix is a test suite that proves these files are immutable to T1/T2 agents and that any modification is detectable.

## The Vector (Context Capture)

From PRESSURE_VECTOR_AUDIT_2026-07-19.md:
> `AGENTS.md`, `CONTEXT.md`, `SOUL.md`, and memory files are writable by agents
> (T1 under digital ops policy). An agent that writes to these files shapes
> future agent behavior. Boot-doc poison persists across sessions.

## Test Suite Architecture (4 Suites)

### Suite 1 — Governance File Immutability

Verify every governance file exists, is non-empty, carries seal markers (SEALED, SOVEREIGN, F13, FORGED, DITEMPA BUKAN DIBERI), and declares sovereign identity. Parametrized across all governance files and INIT/BOOT files.

**Files to check:**
- `/root/SOUL.md`, `/root/AGENTS.md`, `/root/CLAUDE.md`
- `/root/AAA/CLAUDE.md`, `/root/AAA/AGENTS.md`, `/root/CONTEXT.md`
- `/root/AAA/prompts/INIT.md` + any other INIT/BOOT files

**Key assertions:**
```python
# Existence + non-trivial content
assert path.exists()
assert len(content.strip()) > 100  # governance file too small = possible stub

# Seal marker presence
assert any(marker in content for marker in SEAL_MARKERS)

# Sovereign identity
assert "ARIF-SOVEREIGN-888" in content  # who ratified this?
assert "F13" in content                  # final veto anchor

# Autonomy tiers documented
assert "T1" in content and "AUTO-DO" in content
assert "T3" in content and "888_HOLD" in content

# Boot phase declaration (INIT files)
assert "BOOT PHASE" in content or "SELF-ATTESTATION" in content
```

**Orphan Section 15 detection:** Scan governance files for `forge--end` patterns (agent housekeeping append). This is the exact Vector #6 pattern — an agent writing future-task instructions into the boot document. Treat hits as xfail if known (awaiting F13 review), hard fail if unknown.

### Suite 2 — Memory Tier Gates

Verify the `arif_memory` tool classifies mutation modes correctly and requires leases/elevated authority for governance-adjacent tiers (L4-L6).

**Import from runtime:**
```python
from arifosmcp.runtime.megaTools.tool_13_arif_memory import (
    ARIF_MEMORY_MODES, MODE_ACTION_CLASS, MODE_REQUIRES_LEASE,
    MODE_REQUIRES_HUMAN_ACK, MODE_PRE_FLOORS,
)
```

**Key assertions:**
```python
# remember = mutation, not observe
assert MODE_ACTION_CLASS["remember"] == "EXECUTE_REVERSIBLE"

# promote = high impact
assert MODE_ACTION_CLASS["promote"] == "EXECUTE_HIGH_IMPACT"

# Both require leases
assert MODE_REQUIRES_LEASE["remember"] is True
assert MODE_REQUIRES_LEASE["promote"] is True

# forget requires human ack (L13 SOVEREIGN)
assert MODE_REQUIRES_HUMAN_ACK["forget"] is True

# All mutation modes have L01 (AMANAH) + L02 (TRUTH) pre-floors
for mode in ("remember", "promote", "revise", "forget"):
    assert "L01" in MODE_PRE_FLOORS[mode]
    assert "L02" in MODE_PRE_FLOORS[mode]
```

### Suite 3 — Prompts and GENESIS 888_HOLD

Verify `/root/AAA/prompts/` and `/root/arifOS/GENESIS/` exist, contain files, and aren't trivially mutable.

**Key assertions:**
- Directories exist and contain files (empty dir = red flag)
- `GENESIS/000_KERNEL_CANON.md` exists
- No non-doctrine file types in GENESIS/ (`.md`, `.json`, `.jsonl`, `.txt` only)
- INIT files are not world-writable (defense-in-depth)

### Suite 4 — Seal Hash Manifest

The crown jewel. Compute SHA-256 hashes of all INIT/BOOT files, store them as a `SEAL_MANIFEST` dict in the test file. Each file's hash is checked against the manifest — any drift means the file was modified since the seal was forged.

**Building the manifest:**
```bash
# At forge time (after F13 ratification):
sha256sum /root/AAA/prompts/*.md
```

**Test structure:**
```python
SEAL_MANIFEST = {
    "INIT.md": "83f23200e0a7437f068e7edab70b488c66278c79781ab843052ef39413d82725",
    "GROK_AAA_NEXT_INIT.md": "d932306b07e4352d530e666bca2f02faa2048d98a6ebfe01d9c821b7737fe60b",
    # ... etc
}

@pytest.mark.parametrize("filename,expected_hash", SEAL_MANIFEST.items())
def test_init_file_hash_matches_seal(self, filename, expected_hash):
    actual_hash = _sha256(path)
    assert actual_hash == expected_hash, (
        f"SEAL HASH MISMATCH: {filename}\n"
        f"Expected: {expected_hash}\nActual: {actual_hash}\n"
        f"POSSIBLE VECTOR #6: boot instructions modified by agent.\n"
    )
```

**Manifest completeness check:** Every INIT/BOOT file on disk must be in the manifest. Files that exist but aren't manifest = potential agent-planted content.

**Symlink handling:** Detect symlinks before `is_file()` check (symlinks resolve to files so `is_file()` returns True, hiding the symlink nature):
```python
for f in prompts_dir.iterdir():
    if f.is_symlink():           # ← CHECK FIRST
        # resolve and track
    elif f.is_file():            # ← THEN check
        # regular file
```

**Diagnostic manifest generator:** A test that always passes but prints the current hash state of ALL files — useful in CI logs to identify drift:
```python
def test_generate_seal_manifest_for_audit(self):
    for f in sorted(prompts_dir.iterdir()):
        if f.is_file():
            print(f"  {f.name}: {_sha256(f)}")
    # Also hash GENESIS files
    for f in sorted(genesis_dir.rglob("*.md")):
        print(f"  {f.relative_to(ROOT)}: {_sha256(f)}")
```

## Known-issue xfail Pattern

When a governance test finds a KNOWN issue (e.g., Fable5's Section 15 in INIT.md), mark it xfail rather than hard-failing CI:

```python
@pytest.mark.xfail(
    reason="KNOWN: Fable5 Section 15 append in INIT.md L635-683. "
           "Awaiting F13 sovereign review to ratify or excise.",
    strict=True,  # strict=True = fail if test unexpectedly passes (issue was fixed)
)
def test_no_orphan_section_15(self):
    ...
```

`strict=True` means: if the issue gets fixed (test passes), the xfail becomes a FAIL — reminding you to remove the xfail marker. This prevents xfail rot.

## Running

```bash
# Offline (no kernel required):
cd /root/arifOS && ARIFOS_SKIP_PROTOCOL_SENTINEL=1 python -m pytest tests/test_context_capture_gates.py -v

# With live kernel:
cd /root/arifOS && python -m pytest tests/test_context_capture_gates.py -v
```

## Doctrine References

- `/root/forge_work/PRESSURE_VECTOR_AUDIT_2026-07-19.md` — Vector #6 definition
- `/root/AGENTS.md` §6.2 — T1/T2/T3 autonomy tiers
- `/root/SOUL.md` §4 — Lease Classes L0-L3 mapping to T0-T3
- `/root/arifOS/arifosmcp/resources/memory.py` — L1-L6 tier definitions
- `/root/arifOS/arifosmcp/runtime/megaTools/tool_13_arif_memory.py` — memory tool implementation

## Pitfalls

1. **Symlink handling in file enumeration:** `Path.is_file()` returns True for symlinks pointing to files. Always check `is_symlink()` FIRST, then `is_file()`. Otherwise symlinked init files (like `AGENT_INIT_v3.0.md → INIT.md`) appear as separate files with duplicate hashes.

2. **Don't hash governance files:** Governance files (SOUL.md, AGENTS.md) evolve too frequently for hash-pinning. Check their structure (non-empty, contains headers, seal markers present) instead.

3. **The manifest is a snapshot, not a living document:** When F13 legitimately modifies an INIT file, the manifest must be re-computed. The test then fails on purpose — the failure IS the signal that someone changed a boot file. If it's authorized, update the manifest.

4. **Run offline when kernel is down:** The `ARIFOS_SKIP_PROTOCOL_SENTINEL=1` env var bypasses the kernel health check in conftest.py. These tests are filesystem-level and don't need a running kernel.

5. **forge--end in memory files is expected, in INIT files is a red flag.** Filter hits to only governance/INIT paths when scanning for agent-planted content.
