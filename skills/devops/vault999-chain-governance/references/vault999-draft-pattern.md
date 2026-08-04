# VAULT999 Write Gate — Draft Pattern

**Source session:** 2026-08-04 FED + Hermes-ASI Multimodal Audit
**Problem:** `forge_vault` MCP tool returns `URLElicitationRequiredError` when user not present — vault write requires explicit F13 confirmation.

## Pattern: Draft-Then-Seal

When user is not available for interactive confirmation:

1. Write audit receipt to `/root/VAULT999/drafts/<AUDIT-NAME>.md` (human-readable markdown)
2. Include all findings, evidence references, deploy status, and holds
3. Mark as "Draft pending F13 vault write authorization"
4. When user returns, present draft and ask for seal confirmation

## Why This Works

- VAULT999 is append-only and irreversible — requires human acknowledgment
- forge_vault tool enforces this via URLElicitationRequiredError
- Draft files are safe (not sealed, not in chain) but preserve the audit trail
- User can review draft before authorizing seal

## Files

| Path | Purpose |
|---|---|
| `/root/VAULT999/drafts/` | Draft audit receipts (pending seal) |
| `/root/VAULT999/outcomes.jsonl` | Sealed receipts (append-only, irreversible) |
| `/root/VAULT999/vault999.jsonl` | Legacy sealed receipts |

## Session Receipt (2026-08-04)

Attempted `forge_vault` write for FED multimodal audit — blocked by URLElicitationRequiredError. Wrote draft to `/root/VAULT999/drafts/AUDIT-FED-MULTIMODAL-2026-08-04.md` instead. User did not return to authorize seal in same session.
