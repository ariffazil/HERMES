# Config / Vault-Chain Claim Verification (2026-08-01)

Proven on the Qwen Token Plan seat-wiring chaos: Arif pasted a forge agent's receipt
("Siap. Chaos mapped, fixed, verified — semua live"), and live probing found the
receipt's central claim false, its seats.yaml patch corrupted, and its audit stale.
This file is the reusable recipe for verifying claims about config files, vault env
files, and provider seats.

## 1. Masked vault inspection (never print full secrets)

```bash
awk -F= '/QWEN/{v=$2; gsub(/[ \r]/,"",v); print $1" | len="length(v)" | head="substr(v,1,14)}' /root/.secrets/kunci-mas.env
```

- `len=114`-ish + `head=sk-sp-*` → real key wired
- `len≈17` + `head="PASTE_*"` or `${VAR}` indirection → placeholder still present
- KEY: a receipt claiming "all seats live" is falsified by ONE placeholder line.

## 2. mtime forensics — did the change actually land?

```bash
stat -c '%y %n' /root/.secrets/kunci-mas.env /root/.hermes/config.yaml
ls -la --time-style=long-iso /root/.secrets/ /root/.hermes/ | grep -E 'bak|config|kunci'
```

- File mtime AFTER its backup's timestamp → file WAS modified (regardless of any
  file-mutation-verifier warning; the agent may have used `hermes config set`).
- File mtime == backup mtime → untouched; receipt's prose about the file is suspect.
- Backup naming pattern `*.bak-zen-*`, `*.bak-<UTC-stamp>` lets you pair file ↔ backup.

## 3. Live provider-seat probing (Qwen Token Plan pattern)

```bash
set -a; . /root/.secrets/kunci-mas.env; set +a
API=https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
# models list is a WEAK signal — identical across seats (21/21)
curl -s -m 25 "$API/models" -H "Authorization: Bearer $QWEN_HERMES_API_KEY" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d.get("data",[])))'
# chat completion is the STRONG signal — the only thing that proves quota access
curl -s -m 40 "$API/chat/completions" -H "Authorization: Bearer $QWEN_HERMES_API_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"balas satu perkataan sahaja: OK"}],"max_tokens":8}'
```

Findings that falsified the receipt (2026-08-01):
- Standard seat (sk-sp-D.IPRH, QWEN_HERMES_API_KEY): `/models` = 21, but
  `qwen3.7-plus`/`qwen3.7-max`/`qwen3.6-plus` → `Allocated quota exceeded` (DEAD).
  Works: `qwen3.8-max-preview`, `qwen3.6-flash`, `kimi-k2.7-code`.
- Pro seat (sk-sp-H.DIEXP, QWEN_OPENCODE_API_KEY): `qwen3.7-plus` OK.
- Parser trap: `deepseek-v4-flash`/`deepseek-v4-pro`/`glm-5.2` with `max_tokens:4`
  return `content:""` + `reasoning_content` filled + `finish_reason:"length"` →
  naive parser prints ERR with empty message. Use `max_tokens>=20` or check
  `reasoning_content`. A model is dead only when a real `error` object returns.

## 4. Registry repair verification (seats.yaml pattern)

After an agent claims "seats.yaml updated" (or any registry), re-grep per-entity:

```bash
grep -E 'seat_id|env_var|vault_status|rotation_status' /root/AAA/federation/seats.yaml
```

Cross-check EACH seat's `env_var` against the vault value:
- `QWEN_OPENCODE_API_KEY` ↔ seat_fbdaf17967 (Pro) — must be sk-sp-H.*
- `QWEN_HERMES_API_KEY` ↔ seat_39bf2828 (Standard) — must be sk-sp-D.*
- `QWEN_OPENCLAW_API_KEY` ↔ seat_b797ca6b — was left placeholder → "all live" claim FALSE

PITFALL (proven): a `str.replace(old,new,1)` script matched the WRONG seat block
because two seats shared identical `rotation_status:"OVERDUE"\n vault_status:"EMPTY"`
patterns → OpenClaw seat marked POPULATED, real Hermes seat left EMPTY (reversed
reality). Always anchor replacements on unique ids (`seat_id`/`env_var`), never on
repeated structural patterns.

## 5. Stale audit reports — verify CURRENT, not the diff

An audit that claims "model drift" or "missing blocks" may be diffing against the
WRONG backup. 2026-08-01 case: audit claimed 888-APEX still glm-5.2 + missing
references/compaction/plugin/subagent_depth; live opencode.json showed
`qwen-token-plan/deepseek-v4-pro` and ALL blocks present. The auditor diffed backup
07:28 (agent NOT SET then). Rule: grep the CURRENT file for the exact field before
believing any "drift" claim. Audit-vs-backup is a hypothesis, live state is the OBS.

## 6. Gateway restart pattern (token valid, daemon claims rejected)

When a long-running gateway (13h+) reports "token rejected" but direct
`curl api.telegram.org/bot<TOKEN>/getMe` returns ok:True → the daemon holds a stale
state. Restart the unit, then verify BOTH:
```bash
sudo systemctl restart forge-gateway && sleep 5
systemctl is-active forge-gateway
journalctl -u forge-gateway --since "15 sec ago" --no-pager | grep -i 'rejected\|error'
curl -s "https://api.telegram.org/bot${FORGE_BOT_TOKEN}/sendMessage" -d "chat_id=<id>" -d "text=probe"
```

## Vault chain layout (SOT → flat → read)

```
kunci-mas.env (SOT, mode 600)  ← Arif edits here
   ├─ generate-flat.sh → kunci-mas.flat.env   (ONE generator; .py twin removed)
   ├─ vault.flat.env   → symlink → kunci-mas.flat.env
   └─ systemd units    → EnvironmentFile=kunci-mas.flat.env
```

Old failure mode: systemd read `vault.flat.env` (stale generation, 212 keys) while
generator wrote `kunci-mas.flat.env` (263 keys) → two files, two generations, drift
invisible. Single-SOT→single-flat→single-read, plus `verify-vault.py` 0-drift check.
Generator bug (pre-existing): double-escaped `\$` → `\\$` in ARIFOS_SOVEREIGN_BASIC;
fixed by decode-bash-escape + strip inline comment + atomic write (verify before move).
