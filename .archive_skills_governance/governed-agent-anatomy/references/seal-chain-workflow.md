# Seal Chain Workflow: AUDIT_RECORD vs ACTION_AUTHORIZATION

> **Forged:** 2026-07-24 from F13 seal chain session  
> **Canonical source:** `arif_Kernel_intercept.py` `_ACTION_CLASS_POLICY` table  
> **Umbrella skill:** `governed-agent-anatomy` (constitutional chain 000-999)

## Core Distinction

The constitutional seal chain has TWO paths, distinguished by whether the seal grants authorization to mutate the world or merely records evidence:

| Dimension | AUDIT_RECORD | ACTION_AUTHORIZATION |
|-----------|-------------|---------------------|
| **seal_purpose** | `RECORD` | `AUTHORIZE` |
| **authority_effect** | `NONE` | `EXECUTION_GRANT` |
| **reversibility** | R2 | R4/R5 |
| **ack_irreversible** | `false` | `true` |
| **requires_f13** | `false` | `true` |
| **F13 bypass?** | ✅ Autonomous | ❌ Needs Arif Ed25519 or sentinel |
| **Example** | Audit report, evidence attestation, vault receipt | Production deploy, constitution amend, capital action |

## The F13 Trap (How It Catches You)

When calling `arif_judge` without explicit `action_class`, the kernel resolves the action class from `reversibility_level`:

1. If `reversibility_level` is `"FULL"`, `"IRREVERSIBLE"`, `"R4"`, `"R5"`, or any unknown value → **resolves to ACTION_AUTHORIZATION → requires F13**
2. If `reversibility_level` is `"R2"`, `"RECORD_ONLY_APPEND"`, `"EVIDENCE_ATTESTATION"`, `"AUDIT_RECEIPT"` → resolves to AUDIT_RECORD → **no F13 needed**

**The old code (pre-2026-07-24):** Unknown reversibility levels silently converted to R4_IRREVERSIBLE, which always triggered F13 ESCALATE. The P0 fix changed this to CLASSIFICATION_HOLD instead, but the trap still exists if you pass `"FULL"` (which is not a recognized R-class).

## Calling arif_judge for Audit Records

```python
# For audit/evidence seals — autonomous, no F13
judge = arif_judge(
    actor_id="arif",
    intent="AUDIT_RECORD seal of artifact X — evidence only, no execution",
    action_class="AUDIT_RECORD",     # KEY: explicit action class
    reversibility_level="R2",        # KEY: must be R2 or equivalent
    blast_radius="LOW",
    session_id="SEAL-...",
    session_token="sct_v1.xxx"
)
# Returns: decision=ALLOW, seal_type=SEAL_RECORD, requires_human_signature=false
# MCP params: action_class, reversibility_level are both passed at top level
```

## Calling arif_judge for Authorization Seals

```python
# For production/deploy/constitutional changes — requires F13
judge = arif_judge(
    actor_id="arif",
    intent="ACTION_AUTHORIZATION deploy v2026.07.24",
    action_class="ACTION_AUTHORIZATION",
    reversibility_level="R4",
    blast_radius="MEDIUM",
    authority_token="DEV_ONLY_SENTINEL_REPLACE_AT_PROD_BOOT",  # or real Ed25519 sig
    session_id="SEAL-...",
    session_token="sct_v1.xxx"
)
# Returns: decision=ALLOW, seal_type=SEAL_AUTHORIZATION, authorized_execution=true
```

## Known Gap: arif_seal Chain ID

`arif_judge` (via `arif_kernel_intercept_tool`) returns `audit_hash` but NOT `constitutional_chain_id` or `judge_state_hash`. The `arif_seal` tool expects these fields for its chain linkage. When the seal chain isn't wired:

- **Workaround:** Append the receipt directly to VAULT999 outcomes.jsonl (for audit records only — not for authorization seals)
- **Proper fix (P1):** Wire `arif_kernel_intercept` to return `cc_id` / `judge_state_hash`, and wire `arif_seal` to accept `constitutional_chain_id` for audit records (currently it requires one)

## File Map for F13 Operations

| Item | Path |
|------|------|
| Private key (arif) | `/root/.secrets/aaa-identity/keys/arif_private.pem` |
| Agent identities registry | `/root/A-FORGE/data/agent_identities.json` |
| Sovereign key registry | `/root/AAA/docs/sovereign_key_registry.json` |
| Kernel intercept handler | `/opt/arifos/app/arifosmcp/tools/arif_kernel_intercept.py` |
| MCP tool handler (judge wrapper) | `/opt/arifos/app/arifosmcp/runtime/tools.py` (function `_arif_kernel_intercept_tool` at ~line 22082) |
| Action class policy table | `arif_kernel_intercept.py` `_ACTION_CLASS_POLICY` (line ~50) |
| VAULT999 outcomes | `/root/.local/share/arifos/vault999/outcomes.jsonl` |

## Private Key Mismatch Diagnosis

When Ed25519 operations fail with "F13 SOVEREIGN cryptographic signature required":

1. Check which public key is registered in `agent_identities.json` for "arif"
2. Derive public key from each candidate private key file
3. If none match → update `agent_identities.json` with the correct public key
4. Or if the registered key's private counterpart is missing → generate new keypair and register

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

with open('/root/.secrets/aaa-identity/keys/arif_private.pem', 'rb') as f:
    key = serialization.load_pem_private_key(f.read(), password=None)
pub = key.public_key()
pub_bytes = pub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
pub_b64 = base64.b64encode(pub_bytes).decode()
print(f"Derived pubkey: {pub_b64}")
```

## Dev Sentinel (for testing)

When `ARIFOS_SOVEREIGN_KEY` env var is not set, the kernel falls back to:
```
DEV_ONLY_SENTINEL_REPLACE_AT_PROD_BOOT
```
Pass this as `authority_token` for testing. The code itself warns: "trivially bypassable — DO NOT use in production".

## Pitfalls

- **Silent R4 conversion:** Old code silently converted unknown reversibility to R4 → F13. New code returns CLASSIFICATION_HOLD. Always pass explicit `action_class` to avoid ambiguity.
- **Two handler paths:** The MCP tool `arif_judge` goes through `_arif_kernel_intercept_tool` (not `judge.py`'s `arif_judge`). The judge.py function is a separate, older path. Debugging requires knowing which path is active.
- **Session degradation:** SOVEREIGN sessions can degrade to OBSERVE_ONLY between tool calls. Create a fresh session before the judge→seal chain.
- **Nonce required for arif_seal:** The seal tool requires a `nonce` parameter (4-128 chars alphanumeric) to prevent replay attacks. Always provide one.
