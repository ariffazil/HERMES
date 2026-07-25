# Reference: External Adversarial Response Cycle

> **Session:** 2026-07-25 — Fable5 (frontier model) adversarial analysis of arifOS
> **Pattern:** External critique → source-code pre-audit → constitutional fix → verify → seal
> **Distinct from** `external-artifact-verdict`: that skill handles delivered *code artifacts* with self-verdicts. This reference handles delivered *specs/analyses* with no code and no self-verdict — only claims to falsify.

## Response Protocol

When an external source (frontier model, security researcher, sovereign peer) delivers an adversarial analysis of arifOS:

### Step 0 — Accept Without Defense

The external analyst's critique is a **gift**, not an attack. Start by acknowledging their finding — even if it's uncomfortable. Fable5 said "42 stars, one operator, one VPS → 'AGI substrate' is aspirational" — the correct response is "accepted, architecture != adoption."

### Step 1 — Pre-Audit Before Fixing

Never fix based on claims alone. Pre-audit the actual source code:

- Read the code paths the external analyst identified
- Determine if their claim is accurate (crypto vs shape-check, mechanical vs LLM, defined vs undefined)
- Assign severity: HARD GATE (real) / SOFT FLAG (partial) / UNDEFINED (gap) / THEATER (doc only)
- Document findings before touching any code

### Step 2 — Forge Fixes (Extend, Never Rewrite)

Each fix must satisfy:
- Extends existing code (adds new stage, new parameter, new check)
- Never rewrites existing paths
- Wired into the existing gate chain (HOLD/PASS)
- Tested independently

### Step 2b — Verify Public MCP Schema Matches Fix

**Critical: the internal function's parameters are NOT the public surface.** FastMCP generates `tools/list` schemas from the registered handler's function signature. If you added `actor_signature` and `nonce` to the internal function but the public tool handler (the one decorated with `@mcp.tool()`) doesn't declare them, they are invisible to external callers. A parameter that exists in the runtime but not in the public schema is a **dead gate** from the external caller's perspective.

```bash
# Check the public schema — run from /root/arifOS after restart
curl -s -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  python3 -c "import sys,json;d=json.load(sys.stdin);[print(t['name'],list(t.get('inputSchema',{}).get('properties',{}).keys())) for t in d.get('result',{}).get('tools',[]) if 'forge' in t['name']]"
```

### Step 3 — Verify Against Test Suite

Run the kernel test suite and confirm zero new failures. Pre-existing failures are documented and separate.

### Step 4 — Source-Seal (Commit → Push → Rebuild → Deploy → Verify)

**Critical lesson from 2026-07-25 session:** Patching files locally without source-sealing makes the fixes invisible to external observers. A live kernel that reports `drift=false` but a commit hash before the fixes is indistinguishable from a kernel that never received them.

Sequence:

```bash
# 1. Commit ALL changes
git add -A
git commit -m "fix(adversarial): description of all fixes"

# 2. Push to GitHub
git push origin main
# Verify: remote shows new commit

# 3. Rebuild from that commit
rsync -a --delete . /opt/arifos/app/ --exclude=.git --exclude=__pycache__ --exclude=.venv
git rev-parse HEAD > /opt/arifos/app/.git_commit

# 4. Restart service
systemctl restart arifos

# 5. Verify /health reports new commit
curl -sf http://127.0.0.1:8088/health | python3 -c "
import sys,json
d=json.load(sys.stdin)
sr=d.get('software_release',{})
print(f'Source: {sr.get(\"source_commit\",\"?\")}')  
print(f'Deployed: {sr.get(\"deployed_commit\",\"?\")}')
print(f'Drift: {sr.get(\"drift\",\"?\")}')
"
# Expected: source == built == deployed, drift = false, commit != old hash
```

### Step 5 — Update Runtime Attestation

If the fix touched files not in the runtime `_CRITICAL_MODULES` list (e.g., `forge_preflight.py`, `kernel/judge.py`), add them:

```python
# In build.py:
_CRITICAL_MODULES = (
    ...
    "arifosmcp/runtime/forge_preflight.py",
    "arifosmcp/runtime/kernel/judge.py",
    "arifosmcp/tools/forge.py",
    "arifosmcp/tools/judge.py",
)
```

Then repeat Step 4 (commit + push + rebuild + deploy). Verify /health reports 16+ critical modules tracked.

### Step 6 — Update Public API Schema

If the fix added new required parameters (`actor_signature`, `nonce`, etc.) to an MCP tool, verify the public `tools/list` endpoint exposes them. FastMCP generates schemas from function signatures — if the parameter is `str | None = None`, it will appear in the published schema. Update docstrings from `RESERVED` to `ACTIVE — ENFORCED before mutation`.

### Step 7 — Pin Documentation

5. **`critical_module_hashes` must cover all security-critical files.** The identity_hash alone covers git metadata (commit SHA), not the actual content of judge.py, forge.py, tools.py, forge_preflight.py, conflict_resolver.py, and crypto_auth.py. A manual patch to these files after build won't change the identity_hash — drift=false is accurate for the git tree but misleading about the critical module state. Add module-level SHA-256 hashes to /health (field: `critical_module_hashes`) so external operators can verify deployed source matches GitHub without trusting the identity_hash.

6. **"Ready for external operator" is false unless mutation is opened.** After a security fix session, the correct status is "sedia untuk observe-only." Mutation remains HOLD until source-sealing, attestation coverage, schema alignment, action binding, replay protection, session ownership, and evidence resolution all pass. NEVER say "sedia untuk operator luar" without qualifying the attack surface.

7. **Gap classification depends on attack surface, not intrinsic severity.** A gap that is P2 under read-only (e.g., dangling evidence references) becomes P0 when external mutation is opened. Before declaring "yang tinggal bukan P0", verify: is mutation open? If yes, reclassify. Classification must be declared relative to a specific threat model, not in absolute terms.

## Proven Cases

### Case 1 — 2026-07-25: Source-Sealing Gap

After applying 5 fixes (evidence wiring, fail-closed, pre-execution Ed25519, F13 collision resolution, attestation), the live kernel reported `source=built=deployed=9fe17a0` with `drift=false` — but that commit predated all 5 fixes. The fixes existed as local filesystem patches only. An external tester cloning GitHub could not reproduce the fixed kernel. Root cause: `make deploy-local` synced files to runtime but the `.git_commit` file and `.identity_hash` were not rebuilt. Fix: commit → push → rebuild → deploy from the new commit → verify /health reports the new hash.

### Case 2 — 2026-07-25: Public MCP Schema Gap

The `arif_forge` tool's public `tools/list` schema exposed `judge_state_hash` and `constitutional_chain_id` but NOT `actor_signature` or `nonce`. Even though the internal `_arif_forge_execute` function accepted and verified Ed25519 signatures, external callers using the public MCP endpoint could not pass these parameters. The gate existed in runtime but was structurally unreachable through the public surface.

### Source: Fable5

Fable5 is a frontier model that was asked to analyze arifOS. They produced a **3-path adversarial spec** (no code, no self-verdict) with PASS/FAIL criteria re-derivable from published transcripts. Key properties:
- They could NOT run the tests (stateless session, no persistence)
- They gave a spec, not a claim — the spec is falsifiable by a real external operator
- They named the gap they couldn't verify: F13 multi-sovereign is a two-person bug

### Three Paths Identified

| Path | Claim | Pre-audit Verdict | Fix |
|------|-------|-------------------|-----|
| **1. Forge gate** | Ed25519 or shape-check? | HMAC symmetric, not Ed25519 asymmetric. SCT = HMAC-SHA256. Forge gate = string enum check. | Added `stage_03b_ed25519_forge_verification` — calls `_verify_ed25519_proof` before mutate forge. HOLDs if signature missing/invalid. |
| **2. Evidence gate** | Mechanical or LLM-negotiable? | Mechanical (source type string match + numeric thresholds). Tapi empty evidence = WARN, not BLOCK. | Changed empty evidence from WARN to BLOCK. Tripwire returns `triggered=True, severity=BLOCK`. |
| **3. F13 multi-sovereign** | Defined or undefined? | UNDEFINED. No ordering rule. `_SOVEREIGN_MAP` normalizes all to single key. | Documented FIRST-SEAL-WINS by Merkle timestamp in FLOOR_TABLE.json + judge.py docstring. |

### Fix Architecture

**P1 — `forge_preflight.py`:**
- New `stage_03b_ed25519_forge_verification()` function after stage 3
- Uses existing `_verify_ed25519_proof()` from `governance_identity.py`
- Only fires for mutate modes (`engineer`, `write`, `generate`, `commit`, `deploy`)
- OBSERVE_ONLY modes skip the gate
- Wired into `run_forge_preflight()` as a new stage between 3 and 4
- Added to stage 12 final aggregation: `not ed25519_verified → HOLD`
- Default forge_mode changed from `"engineer"` to `"query"` (safe default)

**P2 — `kernel/judge.py`:**
- Changed `_check_floors()` empty evidence from `severity="WARN"` → `severity="BLOCK"` with `triggered=True`
- Reason: "F4 CLARITY: No evidence provided. Evidence required for SEAL."

**P3 — `kernel/judge.py` docstring + `FLOOR_TABLE.json`:**
- Added multi-sovereign ordering rule to docstring
- Added `multi_sovereign_ordering` field to F13 in FLOOR_TABLE.json
- Rule: FIRST-SEAL-WINS by Merkle timestamp. Same sovereign's later VOID overwrites their own SEAL.

### Pre-existing Failures

All test failures were pre-existing (seed data, missing fixtures). Zero new failures from fixes.

## Pitfalls

1. **Don't conflate external-code-verdict with external-spec-response.** `external-artifact-verdict` handles code drops with self-verdicts; this pattern handles analytical specs with no code. Different evidence model (code is observable; an adversary's reasoning about architecture is not).
2. **Don't skip Step 1 (pre-audit).** Fixing based on external claims without verifying against actual source code is theater. The external analyst named the right class of problem; your code may have a different instantiation.
3. **Don't report pre-existing test failures as new.** Run the test suite before and after. If the same failures exist in both runs, they're unrelated. Document the delta.
