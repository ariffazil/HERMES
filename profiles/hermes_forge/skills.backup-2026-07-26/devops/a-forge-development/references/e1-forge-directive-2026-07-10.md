# E1 PRE-EXECUTION GATE — JITU FORGE DIRECTIVE (2026-07-10)

**Sovereign:** Arif | **Authority:** 888 | **Date:** 2026-07-10
**Phase:** 2 ONLY (A-FORGE Execution Gate)
**Target:** `/root/A-FORGE/src/interfaces/mcp/shell/forgeShell.ts`
**HOLD — do not commit**

---

## What Was Built

### 1. readonlyBypass Leak Closed (was line 314)

```typescript
// REMOVED:
const readonlyBypass = !session_id && isReadonlyShellCommand(command);
```

All commands now go through `classifyShellCommandRisk` — no bypass regardless of
`session_id` presence. This was a F1 AMANAH violation.

### 2. classifyShellCommandRisk — 4-Tier

```typescript
type RiskLevel = "SAFE" | "MUTATION" | "IRREVERSIBLE" | "GODEL_LOCKED";
```

| Tier | Commands | Required |
|------|----------|----------|
| GODEL_LOCKED | `rm -rf /`, `rm -rf /root`, `dd`, `mkfs`, fork bomb, `kill -9 1` | HARD_DENY always |
| IRREVERSIBLE | `git push/merge/reset --hard`, `docker rmi/prune`, `systemctl stop/disable`, `iptables -F`, `userdel`, `groupdel`, `truncate`, `shred` | SEAL envelope + arif_verify |
| MUTATION | `mkdir`, `rm`, `mv`, `cp`, `chmod`, `npm`, `pip`, `ssh`, `rsync`, etc. | session_id (EXECUTE authority) |
| SAFE | `cat`, `ls`, `grep`, `curl` (read-only), etc. | none |

### 3. preExecutionGate Flow

```
command → classifyShellCommandRisk → GODEL_LOCKED? → HARD_DENY (sealed)
                              → IRREVERSIBLE? → no SEAL? → HOLD_IRREVERSIBLE
                                         → arif_verify call → TOKEN_INVALID? → HARD_DENY (sealed)
                                                              → SCOPE_MISMATCH? → HARD_DENY (sealed)
                                                              → !replay_safe? → HARD_DENY
                                                              → SEAL_VALID → proceed
                              → MUTATION? → no session_id? → GATE_HOLD
                                         → session_id → EXECUTE_VALID → proceed
                              → SAFE → proceed
```

### 4. arif_verify Wiring

```typescript
async function callArifVerify(sessionId, command, commandHash) {
  const { callMCP } = await import("../client.js");
  return await callMCP("arifos.arif_verify", {
    token: sessionId,
    command,
    command_hash: commandHash,
  }) as Record<string, unknown>;
}
```

**Status**: `arif_verify` does NOT yet exist in arifOS kernel (Phase 1 in-flight).
Call throws until Phase 1 lands — correct fail-closed behavior.

---

## Build Result

```
cd /root/A-FORGE && npm run build
→ TypeScript compilation: ZERO ERRORS ✅
```

## Git Diff Summary

- `+223` lines: `SealEnvelope`, `SHA256`, `classifyShellCommandRisk`,
  `GatedResult`, `arifSealAudit`, `preExecutionGate`, `callArifVerify`
- `~70` lines: `readonlyBypass` block replaced with `preExecutionGate` call +
  result handling (HARD_DENY, HOLD_IRREVERSIBLE, GATE_HOLD, SEAL_VALID)
- `+1` import: `createHash` from `node:crypto`
- `+1` import: `callMCP` from `../client.js`

---

## Dependency: Phase 1 arifOS

arifOS kernel (`/root/arifOS/arifosmcp/runtime/tools.py`) must provide:

```python
@arthur_mcp.tool()
def arif_verify(token: str, command: str, command_hash: str) -> dict:
    """
    Returns:
        token_valid: bool
        scope_valid: bool
        replay_safe: bool
        sealed_command: str (optional)
        actor_id: str (optional)
        violations: list[str] (optional)
    """
```

With `_VAULT_SEAL_REGISTRY` in-memory dict mapping `SEAL-{hex}` tokens to
their commitment records (command_hash, issued_at, expires_at, used, signature).
