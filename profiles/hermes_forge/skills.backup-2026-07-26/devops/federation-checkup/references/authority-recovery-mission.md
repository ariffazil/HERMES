# Authority Recovery Diagnostic Mission Pattern

> Proven: 2026-07-19 P0 authority recovery — read-only diagnostics with 7 structured reports.

## When to Use

When the kernel reports `actor_verified=false` and the user asks for "authority recovery," "P0 federation repair," or "identity diagnostics." **Do not assume the identity kernel is broken** — `actor_verified=false` is correct for anonymous/OBSERVE_ONLY sessions. The real issues are usually stale connectors, registry drift, or uncommitted changes.

## Mission Structure

Produce 7 report files in `<A-FORGE>/forge_work/<date>/AUTHORITY-RECOVERY/`:

| # | File | Content |
|---|------|---------|
| 00 | `00-baseline.md` | Timestamp, hostname, service statuses, arif_init results, health key fields, git states, dirty file inventory |
| 01 | `01-identity-root-cause.md` | Diagnosis: is kernel working? What's actually broken? Recommended fixes (NOT rewrites) |
| 02 | `02-drift-monitor-repair.md` | Systemd timer check, cron check, drift scripts inventory, coverage matrix, what exists vs what's missing |
| 03 | `03-vault-chain-reconciliation.json` | Chain scan: total records, sequence epochs, gap classification, verdict |
| 04 | `04-geox-build-identity.md` | Build identity comparison (deployed vs HEAD), manifest status, branch verification, fix recipe |
| 05 | `05-final-live-probes.json` | Fresh health probes from all organs, drift findings summary |
| 06 | `unresolved-gaps.md` | Remaining HOLDs, open gaps with severity, resolved-during-mission items, priority-ordered next actions |

## Probe Sequence

### Phase 1 — Parallel Discovery (all at once)
```bash
# arifOS
mcp__arifos__arif_init(mode='light')
mcp__arifos__arif_init(mode='validate')
curl http://localhost:8088/health

# Services
systemctl is-active arifos-api geox-api wealth-api vault999
hostname; date --iso-8601=seconds

# Git states (all repos)
cd /root/arifOS && git log --oneline -3 && git status --porcelain && git branch --show-current
cd /root/GEOX && git log --oneline -3 && git status --porcelain && git branch --show-current
cd /root/A-FORGE && git log --oneline -3 && git status --porcelain && git branch --show-current

# Drift infrastructure
systemctl list-timers | grep -i drift
find /root -name "*drift*" -type f 2>/dev/null | head -30
crontab -l | grep -i drift

# VAULT999
cat /root/VAULT999/seal_chain_head.json
tail -20 /root/.local/share/arifos/vault999/seal_chain.jsonl
wc -l /root/.local/share/arifos/vault999/seal_chain.jsonl

# GEOX
cat /root/GEOX/canonical_manifest.json
cd /root/GEOX && git branch -r | grep "fix/deployment" && git rev-parse HEAD
```

### Phase 2 — Deep Probes (after initial data)
```bash
# GEOX health
curl http://localhost:8081/health
# VAULT999 health
curl http://localhost:8100/health
# Dirty file diffs
git diff <file>
```

### Phase 3 — Final Verification
Re-run key probes to capture any changes that occurred during the mission.

## Build Identity Verification Pattern

Compare the deployed artifact's git version against the source tree HEAD:

```bash
DEPLOYED=$(curl -s http://localhost:<PORT>/health | jq -r '.git_version // .build_commit')
SOURCE=$(cd /root/<REPO> && git rev-parse --short=8 HEAD)

if [ "$DEPLOYED" = "geox-$SOURCE" ] || [ "$DEPLOYED" = "$SOURCE" ]; then
  echo "MATCH"
else
  echo "MISMATCH: deployed=$DEPLOYED source=$SOURCE"
fi
```

A mismatch means the deployed artifact is stale — rebuild and redeploy. This is a P0 finding because the service reports a different identity than the source of truth.

## VAULT999 Chain Classification

The seal chain uses mixed sequence schemes by design. Classify accordingly:

| Classification | Meaning |
|---------------|---------|
| `CHAIN_VALID_MULTI_EPOCH` | Multiple epochs with different sequence schemes; contiguous within each |
| `CHAIN_CONTIGUOUS` | Single numeric sequence, no gaps |
| `CHAIN_VALID_SEQUENCE_SPARSE` | Different schemes coexist; no corruption |
| `CHAIN_CORRUPT` | Hash chain broken, tampering detected |

**Do not** re-sequence the chain to enforce uniformity — this destroys multi-epoch provenance.

## Critical Anti-Patterns

1. **"Identity kernel is broken"** — FALSE when `actor_verified=false` is the correct state for anonymous sessions
2. **"Rewrite VAULT999 history"** — NEVER do this; chain is append-only by design
3. **"Merge to main"** — The authority recovery mission is read-only diagnostics; merging is a separate sovereign decision
4. **"Fix the kernel"** — The kernel is usually fine; the real issues are build pipeline, stale connectors, or uncommitted changes
