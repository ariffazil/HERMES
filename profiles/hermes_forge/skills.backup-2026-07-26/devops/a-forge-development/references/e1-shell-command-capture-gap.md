# E1 Shell Command Capture Gap — 2026-07-10

## Status: OPEN (needs JITU patch)

## The Problem

A-FORGE's `preExecutionGate()` calls:
```
callMCP("arifos.arif_verify", { token, command, command_hash })
```

Where:
- `token` = SEAL token from JITU approval (session_id)
- `command` = exact shell command string (e.g. `"git push --force origin main"`)
- `command_hash` = SHA256(command)

The arifOS kernel's `verify_seal()` (in `vault_registry.py`) correctly:
1. Looks up token in `_VAULT_SEAL_REGISTRY`
2. Compares SHA256(command) against stored `command_hash`
3. Burns token and writes SEAL_VERIFIED entry

**BUT**: The SEAL was issued without ever capturing `shell_command`.

## Where SEALs Are Issued

`arif_judge` (via `_arif_judge_deliberate_tool` in `tools.py`) issues SEALs when `verdict == "SEAL"`. It calls `arif_vault_seal` but **does not pass a `shell_command` parameter**.

The SEAL token format in `vault_registry.issue_seal()` requires:
```python
entry = {
    "shell_command": shell_command,  # ← currently always ""
    "command_hash": _compute_sha256_hex(shell_command),  # ← always SHA256("")
    ...
}
```

This means every SEAL is bound to `SHA256("")` — not to the actual command.

## The Fix (Option A — Full Option A)

### 1. Patch `arif_judge` to accept `shell_command`

In `tools.py` (`_arif_judge_deliberate_tool`):
```python
async def _arif_judge_deliberate_tool(
    ...
    shell_command: str = "",   # ADD THIS
    ...
):
```

When verdict == "SEAL" and shell_command is non-empty:
```python
from arifosmcp.runtime.vault_registry import issue_seal
...
if seal_output.get("verdict") == "SEAL" and shell_command:
    seal_output["sealed_command"] = shell_command
    seal_output["command_hash"] = issue_seal(
        shell_command=shell_command,
        actor_id=actor_id or "ARIF",
    )
```

### 2. A-FORGE passes shell_command at JITU time

In `forgeShell.ts` when calling `arif_judge`:
```typescript
const judgeResult = await callMCP("arifos.arif_judge_deliberate", {
  candidate: `IRREVERSIBLE: ${command}`,
  shell_command: command,  // ADD THIS — exact command string
  session_id,
  ...
});
```

### 3. Token format (already correct in vault_registry.py)

`issue_seal()` stores `shell_command` and `command_hash` correctly. Only the JITU call chain is missing.

## Verification

After fix, a SEAL entry should read:
```json
{
  "entry_type": "SEAL_ISSUED",
  "token": "SEAL-45d4b93165ca4670",
  "shell_command": "git push --force origin main",
  "command_hash": "sha256:d20c97f7d0825f2f93cb4052cd7e62799a2f731d5cecc35b5e6e21910362d940",
  ...
}
```

## References

- `vault_registry.py` — `issue_seal()` + `verify_seal()` (correct implementation)
- `tools.py` lines 19643-19681 — `_arif_verify_tool` (correct, calls `verify_seal`)
- `tools.py` line 15669+ — `_arif_judge_deliberate_tool` (missing `shell_command` param)
- `forgeShell.ts` — `preExecutionGate()` + `callArifVerify()` (correct, ready for wired kernel)
