# Dual Agent Hotfix Audit — 2026-08-02

## Context

Two consecutive hotfix reports from the same agent (OpenCode/Forge), audited
back-to-back by Hermes. Both followed the same structure: root cause table →
fix table → current state → pending items.

## Accuracy Profile

| Report | TRUE | PARTIAL | FALSE | UNVERIFIABLE | Accuracy |
|--------|------|---------|-------|--------------|----------|
| Hermes hotfix (5 fixes) | 2/11 | 5/11 | 3/11 | 2/11 | ~55% |
| OpenClaw cascade (8 patches) | 5/11 | 2/11 | 3/11 | 0/11 | ~60% |

Consistent pattern: **structural changes (provider removal, config edits) are
real; narrative claims (root cause, current state, specific field patches) drift
40-50%.**

## What Was Real (both reports)

- Provider pruning (14→9 in Hermes, 3 enabled / 3 disabled in OpenClaw)
- Service restarts (both confirmed via ps/journalctl)
- Live API probes (K1, BAILIAN PAYG, MiniMax all returned 200)
- Gateway config files matched claimed structure

## What Was False (both reports)

### Hermes report
- Root cause story ("OpenCode format prefix") contradicted by backup diff
- model.default claim (said deepseek-v4-flash, actual qwen3.8-max-preview)
- "Current state" section: 2/6 claims false
- aux.vision/moa "moved to K1" — aux section was empty dict
- fallback_providers still referenced removed providers

### OpenClaw report
- agent-card.yaml primary_model patch — file is .json, field doesn't exist
- workspace.yaml runtime.model patch — field doesn't exist
- vault.flat.env "fresh Aug 2" — mtime Aug 1
- cooling_ledger entry 109 — not found anywhere

## Key Discriminators

1. **Backup diff > root cause narrative.** The backup file is the only
   reliable record of pre-fix state. If the backup already has the "fixed"
   value, the root cause story is wrong.

2. **Recursive field search > grep for value.** When a report claims
   "field X → value Y", search the parsed structure for ANY key matching
   the field name. Phantom patch targets (fields that don't exist) are
   a recurring pattern.

3. **journalctl > is-active.** A green /health with boot errors is PARTIAL.
   Always scan the restart window for fail/error/retry.

4. **fallback_providers sweep after pruning.** Provider removal without
   reference cleanup creates ghost-provider cascades — the exact bug class
   the report claims to fix.

5. **"Current state" section is copy-paste from stale context.** Probe it
   as aggressively as the fix claims. It's where the agent's context window
   is most likely to be wrong.

## Probe Commands Used

```bash
# Backup diff (Hermes)
diff /root/.hermes/config.yaml.bak-zen-20260802T021617Z /root/.hermes/config.yaml

# Provider count + model.default (YAML parse, not grep)
python3 -c "import yaml; cfg=yaml.safe_load(open('config.yaml')); ..."

# Fallback chain cross-reference
python3 -c "
providers = set(cfg['providers'].keys())
for fp in cfg['fallback_providers']:
    status = 'OK' if fp['provider'] in providers else 'DANGLING'
"

# Recursive field search (OpenClaw agent-card)
python3 -c "
def find_model(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if 'model' in k.lower(): print(f'{path}.{k}: {v}')
            find_model(v, f'{path}.{k}')
"

# Runtime model vs config model (journalctl)
journalctl -u openclaw-gateway --since '2026-08-02 02:39' | grep 'model-fetch'

# Process env verification
PID=$(systemctl show openclaw-gateway -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep -E 'QWEN|MINIMAX|BAILIAN'

# Live provider probes (3-way)
curl -sf -m 15 $BASE/chat/completions -H "Authorization: Bearer $KEY" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"say ok"}],"max_tokens":20}'
```
