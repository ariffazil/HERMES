# Archived Provider Reconciliation — The Stranded-Balance Pattern

> **Proven 2026-08-04** during FED + Hermes-ASI Multimodal Audit.
> **Symptom:** `notes: "ARCHIVED <date>: not in litellm-config.yaml, orphaned from old MuleRouter routing"` on `mcp__fed__fed_status` rows. Balance stays in `token_bank.db` indefinitely.
> **Cost:** Real money un-reconciled. mulerouter $49.93 + tokenrouter $59.94 + openrouter $0.50 = ~$109.37 dormant as of 2026-08-04.

## The Failure Mode

A provider gets removed from `litellm-config.yaml` (rewire, retirement, or Migration under Hood event) but its row in `token_bank.db` survives the deletion. The provider is no longer routed, but the balance is still tracked. Federal status queries show it as ARCHIVED; downstream agents have no way to spend it. Net result: money in the system that can't move.

```sql
-- See it in /root/.local/share/arifos/token_bank.db
SELECT provider_name, balance_usd, track_type, notes
FROM providers
WHERE notes LIKE 'ARCHIVED%';
```

```json
{
  "provider_name": "mulerouter",
  "balance_usd": 49.925,
  "track_type": "B",
  "confidence_score": 0.99,
  "notes": "ARCHIVED 2026-08-04: not in litellm-config.yaml, orphaned from old MuleRouter routing. Manual top-up 2026-07-30."
}
```

## The Three Paths

| # | Path | When | Cost | Risk |
|---|---|---|---|---|
| 1 | **Withdraw + tombstone** | Cash recoverable to active wallet | Audit-clean | Reconciliation effort (manual) |
| 2 | **Revive** | Provider still routable + useful | Free | Re-creating the orphan class |
| 3 | **Tombstone only** | Cash not recoverable, audit-clean needed | Free | Balance frozen in legacy record |

### Path 1 — Withdraw + Tombstone

```bash
# 1. Withdraw from provider console (manual, arif proves identity)
# 2. Update token_bank.db with tombstone receipt
sqlite3 /root/.local/share/arifos/token_bank.db <<EOF
UPDATE providers
SET balance_usd = 0.0,
    notes = 'ARCHIVED 2026-08-04: withdrawn 2026-XX-XX, tombstone F11',
    confidence_score = 0.0
WHERE provider_name = '<name>';
EOF

# 3. Log to VAULT999 for F11 audit
echo "{\"ts\":\"$(date -Iseconds)\",\"action\":\"TOMBSTONE\",\"provider\":\"<name>\",\"actor\":\"hermes-prime\",\"reason\":\"withdrawn_reconciled\"}" >> /root/VAULT999/federation_epistemology.db  # or seal_law.py
```

### Path 2 — Revive

```bash
# 1. Verify provider is healthy
curl -s -H "Authorization: Bearer $PROVIDER_KEY" https://api.<vendor>/v1/models | head

# 2. Add back to litellm-config.yaml model_list
# 3. Restart litellm-federation
sudo systemctl restart litellm-federation
```

### Path 3 — Tombstone Only

```bash
sqlite3 /root/.local/share/arifos/token_bank.db <<EOF
UPDATE providers
SET notes = 'ARCHIVED 2026-08-04: not recoverable, tombstone F11',
    confidence_score = 0.0
WHERE provider_name = '<name>' AND balance_usd > 0;
EOF

# Audit receipt (F11 hard requirement)
mcp__aforge__forge_vault \
  --name "TOMBSTONE-<provider>-$(date +%Y%m%d)" \
  --reason "ARCHIVED_TOMBSTONE" \
  --tier "audit.session"
```

## Decision Heuristic

Run this thought experiment before choosing:

- **Is the provider API still alive?** → If NO, Path 3 (tombstone only)
- **Is the balance confirmed recoverable through provider dashboard?** → If YES, Path 1 (withdraw + tombstone)
- **Do we actually use this vendor's models anywhere?** → If YES, Path 2 (revive); if NO, Path 3

For **BLIND providers** (openrouter-style: API returns usage but no credit balance), Path 3 is the only honest option. The balance field is a Track-B estimate built from inferred data; the cash position is unknowable.

## Pitfalls

1. **Don't drop the DB row.** LiteLLM 1.90 audit trail needs the historical record. UPDATE the `notes` field instead of DELETE.
2. **Don't blanket-zero `balance_usd`.** If you do, you lose the audit value. Set to zero only with a verified withdrawal receipt; otherwise mark unverified with `confidence_score=0` and keep the balance visible.
3. **The DB comment field is the audit log.** Every reconciliation step must end with an `UPDATE providers SET notes = '...'` entry. F11 will not accept silent mutations.
4. **Mirroring orphaned config still triggers federation drifts.** Even after tombstone, keep `mcp__fed__fed_status` queries on ARCHIVED rows — they let Arif track pending cash-out actions in the morning brief.
5. **Hashed vault receipt vs live db mutation.** Two-channel: db UPDATE is the operational truth; `forge_vault` write is the constitutional receipt. Do both.
6. **`mulerouter` and `tokenrouter` were archived 2026-08-04 by a config sweep.** The sweep wasn't audited against balance impact. This is a "what to do better next time" — always include balance audit in any config deletion sweep. Add a CI step: `before deleting provider entry, check providers.balance_usd != 0`.

## Pre-Archive Hardening (recommended CI step)

In your config-sweep pipeline, add:

```python
def pre_delete_provider(config_path: Path, provider_name: str, db_path: Path):
    """Gate provider removal against stranded-balance pattern."""
    current = sqlite3.connect(db_path).execute(
        "SELECT balance_usd, notes FROM providers WHERE provider_name = ?",
        (provider_name,),
    ).fetchone()
    if current and current[0] > 0.0:
        raise ProviderArchiveError(
            f"Cannot archive {provider_name}: balance ${current[0]:.2f} stranded. "
            f"Run reconcile-archived-providers skill first."
        )
```

## Cross-Skill Links

- `references/litellm-multimodal-capability-flag.md` — another config-drift trap in the same YAML file
- `audit-seal` — F1-F11 sealed events for provider reconciliation
- `vault999-chain-governance` — append-only seal pattern for F11 audit
