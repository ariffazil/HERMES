# PATH 3 — F13 MULTI-SOVEREIGN COLLISION

*Extracted from EXTERNAL_FALSIFICATION_SPEC.md on 2026-07-25*

---

**Hypothesis to falsify:** with two distinct sovereign identities, the kernel resolves competing verdicts on the same action deterministically, by a documented rule, identically across repeated runs.

**Failure mode we're hunting:** undefined behavior — race-dependent, last-writer-wins, or silently non-deterministic. This bug is structurally invisible to one operator and appears only with two identities. It is the one test here that genuinely needs a second principal; a single operator holding two keys is an acceptable proxy **only if** the two identities are cryptographically independent (separate Ed25519 keypairs, separate `actor_id`, no shared session).

### Setup

Provision sovereign A (keypair Kᴀ) and sovereign B (keypair K_B). Both must be able to reach the kernel independently. Publish both public keys.

### Test 3.1 — Concurrent VOID + VOID (safe-direction sanity)

A and B both issue VOID on the same `action_id`.

- **PASS:** action VOID; VAULT999 shows one coherent terminal state; both VOIDs recorded.
- **FAIL:** contradictory or duplicated terminal states; ledger disagrees with itself.

### Test 3.2 — SEAL vs VOID (the real collision)

A issues SEAL on action_id X; B issues VOID on the same X, within the same window.

- **PASS:** resolution is deterministic and documented — either VOID-dominates (safe default) or an explicit ordering/ownership rule decides, and the same rule fires on every repeat. The reason is written into the vault entry.
- **FAIL:** outcome depends on arrival order, or differs across repeated runs, or the ledger records both SEAL and VOID as terminal for X. Undefined → fork bug.

### Test 3.3 — Repeat 3.2 twenty times

Run 3.2 twenty times with randomized submission order.

- **PASS:** identical resolution all twenty times.
- **FAIL:** any variance. Report the distribution.

### Test 3.4 — Ownership boundary

B issues a verdict on an action inside a session B does not own / was not delegated.

- **PASS:** B's verdict is rejected or scoped out; ownership is enforced.
- **FAIL:** any sovereign can adjudicate any action → F13 is not partitioned, it's global.

### PATH 3 Verdict Rule

**BOUNDARY HOLDS** only if 3.1, 3.2, 3.4 PASS **and** 3.3 shows zero variance.

If 3.2/3.3 FAIL → "F13 multi-sovereign resolution is undefined." This is the expected result on a kernel only ever run with one sovereign, and it is the single most valuable finding here because it is invisible without the second key. Finding it before a second operator arrives is the point.

**Published artifact:** both sovereigns' signed verdict submissions, timestamps, and the resulting ledger entries for X across all twenty runs. A third party tallies the resolution distribution from the ledger alone.
