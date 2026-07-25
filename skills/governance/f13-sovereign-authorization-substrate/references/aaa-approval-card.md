# AAA Approval Card Schema

Returned as part of the `ESCALATE` + `F13_REQUIRED` response for UI rendering.
**Must not expose private keys, raw signatures, or reusable bearer tokens.**
Raw nonce and hashes may appear only in expandable audit details.

> **Deployment status:** `build_approval_card()` helper exists in `crypto_auth.py` (line 601)
> but is NOT yet wired into the judge `ESCALATE` response path. This is a Phase 2 target.

## Card Shape

```json
{
  "approval_card": {
    "title": "Production authorization required",
    "action_summary": "<human-readable action description>",
    "reason": "<why this action is needed — 1-2 sentences>",
    "affected_systems": ["<system-name>"],
    "environment": "staging | production | sovereign",
    "reversibility": "R4 | R5",
    "blast_radius": "LOW | MEDIUM | HIGH | SOVEREIGN",
    "rollback_available": true,
    "rollback_summary": "<plain-language rollback procedure — what happens if we need to undo>",
    "requested_by": "<agent or organ name>",
    "expires_at": "<ISO-8601>",
    "actions": ["APPROVE", "REJECT", "INSPECT"]
  }
}
```

## Render Rules

- **DO NOT** expose: private keys, raw PEM, raw signature bytes, reusable bearer tokens
- **DO NOT** expose: full nonce in primary card (may appear in expandable audit detail)
- **DO NOT** expose: full candidate_hash in primary card (may appear in expandable audit detail)
- **DO** expose: human-readable action_summary, reason, rollback_summary
- **DO** expose: expiry as ISO-8601 (not as epoch/relative seconds)

## Integration Points

| Layer | Where | Details |
|---|---|---|
| Judge | `_arif_judge_deliberate()` | Generates approval_card on `F13_REQUIRED` |
| AAA Cockpit | `AAA/src/components/ApprovalCard.tsx` | Renders the card + APPEND/REJECT/INSPECT buttons |
| A2A Agent Card | `agent-card.json` | Declares `capabilities.f13_approval`. |
| Telegram Gateway | `HERMES` | Forwards approval_card as formatted message + inline buttons |

## Progressive Strength

| Action Class | Auth Method | UI Complexity |
|---|---|---|
| R4 (irreversible, non-constitutional) | Passkey / biometric PIN | One-tap approve |
| R5 (sovereign, constitutional change) | Hardware key / cold wallet | Multi-step, cooldown |
| R3 (costly reversible) | Confirm dialog | Soft confirmation only |
