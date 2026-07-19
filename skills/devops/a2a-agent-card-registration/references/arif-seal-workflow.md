# arif_seal Workflow — Sovereign Seal via MCP

## The 888_HOLD Problem

When calling `arif_seal` directly via curl to the MCP endpoint (`POST :8088/mcp`), the tool returns 888_HOLD even with a valid SOVEREIGN session token. This happens because:

1. The MCP tool schema declares `additionalProperties: false`
2. `ack_irreversible` is documented in `_meta.arifos_manifest.inputs` but NOT in `inputSchema.properties`
3. The kernel enforces F13 — seal requires explicit sovereign approval

**888_HOLD is CORRECT behavior.** The constitution is working. Do not work around it.

## Correct Seal Path

### Via MCP Tool Interface (from sovereign agent session)

1. Establish SOVEREIGN session:
```python
import base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Get nonce from arif_init call
nonce = "<challenge_nonce>"
with open("/root/.secrets/aaa-identity/keys/arif_private.pem", "rb") as f:
    key = load_pem_private_key(f.read(), password=None)
msg = f"arif:{nonce}".encode()
sig_b64 = base64.b64encode(key.sign(msg)).decode()

# Call arif_init with actor_id=arif + nonce + actor_signature
# Returns SOVEREIGN session with seal_allowed=true
```

2. The MCP tool interface (from Hermes) handles session propagation automatically. The seal call goes through `mcp__arifos__arif_seal` which passes the session context.

### Via Kernel (bypassing MCP)

If the user is Arif and has direct terminal access, the seal works through the kernel's internal flow. The MCP transport is secondary.

## Key Observations

- `additionalProperties: false` on the MCP input schema means only declared params are accepted
- `ack_irreversible` should be added to `inputSchema.properties` in the arifOS kernel if direct API sealing is needed
- 888_HOLD is NOT a bug — it's F13 enforcement
- The session token from arif_init carries the SOVEREIGN authority; the MCP tool should respect it
