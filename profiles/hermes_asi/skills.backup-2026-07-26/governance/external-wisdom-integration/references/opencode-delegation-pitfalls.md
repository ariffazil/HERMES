# OpenCode Delegation Pitfalls (2026-07-12)

Critical lessons from delegating kernel code changes to OpenCode.

## 1. Fabrication Detection

**OpenCode can produce plausible-looking delivery summaries without writing any files.**

2026-07-12: OpenCode claimed "4,101 lines delivered across 5 files" for an AAA TypeScript architecture. Zero files existed on disk. The summary included file names, line counts, test results — all fabricated.

**Verification checklist (MANDATORY after every OpenCode delegation):**
```bash
# Check file existence
ls -la /path/to/claimed/files

# Check line counts
wc -l /path/to/claimed/files

# Run tests if claimed
cd /repo && python -m pytest tests/... -v

# Spot-check key functions exist
grep -n "def function_name" /path/to/file.py
```

**Rule:** Never report "delivered" without running verification. The delegation summary is CLAIM (SPEC), not OBS.

## 2. Kernel Gate Testing Pitfall

When adding a new gate to `arif_kernel_intercept.py`:

1. **Schema first.** If the gate returns a new decision type (e.g., SABAR), update `KernelOutput.decision` Literal FIRST.
2. **Full test sweep.** Run `pytest tests/runtime/test_kernel_intercept.py -v` after adding the gate.
3. **Default parameter breakage.** Any existing test that doesn't explicitly set the new gate's input parameter will hit the new gate with defaults. Example: adding the 17x gate broke `test_r5_with_correct_sentinel_allows` because it used default `epistemic_state=UNKNOWN`.
4. **Fix direction.** If the breakage is correct behaviour (sovereign + unknown epistemic → SABAR), update the test. If wrong, fix the gate.

## 3. Sovereignty ≠ Epistemic Immunity

Authority tokens (F13) grant PERMISSION. Epistemic state grants CONFIDENCE. They are orthogonal.

A valid sovereign token on an UNKNOWN-epistemic R5 action should SABAR, not ALLOW. If a test assumes otherwise, the test is wrong — update it to set `epistemic_state="FACT"` + evidence.
