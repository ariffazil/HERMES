# Receipt Chain Verification Bug — Phantom Import (2026-08-02)

## Summary

`arif_init(mode=validate)` reported `receipt_chain_valid: false` and
`vault_replay: false`, making the auditability claim look broken. The vault
chain itself was fine — the bug was in the telemetry layer that REPORTS on
the chain, not the chain itself.

This is the #1 blocker in the external (Claude) audit of the arifOS kernel.
The value proposition is auditability; a proof system that can't prove itself
undermines the entire claim, even when the underlying system is healthy.

## Root cause — two bugs, same class

### Bug A: Wrong import path (both telemetry files)

Both files import from a non-existent package:

```python
# arifosmcp/abi/verification_envelope.py line 305
from arifosmcp.core.vault999.verify import verify_chain

# arifosmcp/tools/session.py line 3269
from arifosmcp.core.vault999.verify import verify_chain
```

`arifosmcp.core` does NOT exist as a package. The real module is:

```python
arifosmcp.runtime.canonical_vault_chain
```

The import always raises `ModuleNotFoundError` → caught by `except ImportError: pass`
→ the field stays at its dataclass default `False`.

Verify the phantom import:
```bash
python3 -c "from arifosmcp.core.vault999.verify import verify_chain"
# ModuleNotFoundError: No module named 'arifosmcp.core'

python3 -c "from arifosmcp.runtime.canonical_vault_chain import verify_chain; print('OK')"
# OK
```

### Bug B: verify_chain never actually CALLED (verification_envelope.py)

Even if the import worked, `collect_verification_telemetry()` at line 309 only
sets `telemetry.vault_replay = True`. It NEVER sets `receipt_chain_valid`.
The field stays `False` forever — no code path in the function writes it.

`session.py` line 3272 DOES set `receipt_chain_valid = True` — but only inside
the `try` block guarding the broken import, so it never executes.

## The real verify_chain (already production-grade)

`arifosmcp.runtime.canonical_vault_chain.verify_chain()`:
- Walks `seal_chain.jsonl`
- Classifies EVERY discontinuity (never silent)
- Returns `VerifyResult(verified, status, entries, corrupt_lines, ledger_path, failure_classes)`
- Supports `scope="full"` (production truth incl. historical) and `scope="canonical"` (F-004 envelope entries only)
- Already used by: REST routes, vault tools, observatory, command center, forge preflight
- Read-only — safe to call during validate

Empty/missing chain returns `VerifyResult(verified=True, status=NO_CHAIN)` —
empty genesis is valid by design.

## Fix (minimal, ~10 lines per file)

In both `verification_envelope.py` and `session.py`:

```python
try:
    from arifosmcp.runtime.canonical_vault_chain import verify_chain
    result = verify_chain(scope="canonical")
    telemetry.vault_replay = True
    telemetry.receipt_chain_valid = bool(result.verified)
except Exception:
    pass  # fail-closed: stays False
```

Fail-closed preserved:
- verify_chain raises → stays False
- chain has gaps → verified=False → receipt_chain_valid=False
- chain missing → verified=True (NO_CHAIN) → receipt_chain_valid=True

## Diagnostic technique: phantom import detection

General pattern — when a validate/telemetry endpoint always returns False for
a capability that should work:

1. **Find where the field is set:** `grep -rn "receipt_chain_valid" --include="*.py"`
2. **Check the import is real:** `python3 -c "from <module> import <name>"`
3. **Check the function is actually CALLED**, not just imported. A common
   anti-pattern is `try: from X import Y; field = True` which only proves the
   import works, not that Y was executed.
4. **Find the real implementation:** `grep -rn "def verify_chain" --include="*.py"`
   — often the function exists in a different module than the one imported.

This class of bug is especially dangerous because it makes healthy systems
look broken, eroding trust in the auditability claim itself.

## The 5 ordered kernel blockers (Claude audit, 2026-08-02)

External audit of the live arifOS surface. Ordered by priority:

1. **Receipt chain verification** — `vault_replay=false`, `receipt_chain_valid=false`,
   `signature=null`. The value proposition itself. (Root cause: phantom import above.)
2. **Identity verification with non-null method** — `actor_verified: false` at top
   level, `verified: True` inside `facts[0]`, `verification_method=null` everywhere.
   Session resolves as both `"anonymous"` and `"unknown"` in the same payload.
3. **Collapse parallel verdict paths to ONE** — `HOLD` + `DENY` + `GREEN` + `DEGRADED`
   in one response. Multiple code paths computing verdicts independently, never reconciled.
4. **Token issuance behind authorization** — validate failed with "session_id required"
   but returned a signed bearer SCT anyway. Issuance running parallel to authorization,
   not downstream of it. Security defect.
5. **Measure APEX signals or label floors advisory** — `C_dark`, `G`, `W3`, `h` all
   `UNMEASURED`. `witness: {active: 0}`. Tri-witness is doctrine with zero witnesses running.

### What's genuinely real (don't over-correct)

- `kernel_alive`, `protocol_conformant`, `verifier_plane_ready` all true
- PROOF-SPINE passed with expected/actual state hash matching and clean rollback
- WELL returned REGISTRY_PASS, 0 phantoms, 0 alias conflicts
- It fails CLOSED correctly — degrades to OBSERVE_ONLY, blocks claim_success

The bones are sound. The gap is "constitutionally designed" vs "operationally proven."

### WELL discrepancy worth a look

`callable_tools: 16` vs `exported_tools: 10` while claiming 0 phantoms. Counts
don't reconcile — PASS may measure something narrower than "no phantom tools."
6 extra callables not in the export surface is exactly what "0 phantoms" should catch.

## Caveat on the audit

The auditor probed WITHOUT the ceremonial boot, without Ed25519 signing, without
a real session bind — from their own container loopback with no route to the organs.
So SOME of the DENY is expected fail-closed behavior for an anonymous caller. The
real finding is not "the kernel said no to a stranger" but "the SHAPE of the no is
incoherent" — a healthy bouncer says "no"; this one said "no" + "maybe" + "yes here's
a key" + "the door is green" simultaneously.
