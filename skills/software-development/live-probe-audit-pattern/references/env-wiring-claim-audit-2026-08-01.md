# Env/Config Wiring Claim Audit — worked example (2026-08-01)

Full worked example of the "Config/Env Wiring Claim Verification" pattern:
auditing another agent's receipt claiming Qwen Token Plan seats were wired,
config rewritten, and everything verified live.

## The receipt under audit

Agent claimed (paraphrased):
- "Root cause: 3 Qwen seats provisioned but keys never entered vault —
  kunci-mas.env had placeholder literals → 401 InvalidApiKey"
- "config.yaml's qwen-token-plan provider (PRIMARY + 4/5 fallbacks +
  vision + compression + MoA + TTS) all point to QWEN_HERMES_API_KEY"
- "Fallback chain was theater — all on one provider, one key"
- "Fixed: keys wired, config rewritten, verified live (QTP-OK)"
- "Seats.yaml jadi SOT quota"
- Attached file-mutation verifier warning: "config.yaml — [patch] Refusing
  to write to Hermes config file: Agent cannot modify security-sensitive
  configuration."

## Probe sequence (what the witness actually ran)

```bash
# 1. File evidence — mtime + backups prove modification regardless of tool attribution
stat -c '%a %y %n' /root/.secrets/kunci-mas.env /root/.hermes/config.yaml
#   kunci-mas.env  mtime 11:04 (post-wire), config.yaml mtime 11:07 (post-rewrite)
#   → files WERE changed; the patch-tool refusal applied to a different write path
#   (CLI `hermes config set` did the real work). Backup files exist for both.

# 2. Vault contents — MASKED read (never print keys)
#   Watch the export-prefix trap: kunci-mas.env uses `export KEY=value`
#   → naive startswith('KEY=') reports EMPTY for everything
python3 - <<'EOF'
def getkey(name):
    for line in open('/root/.secrets/kunci-mas.env'):
        line = line.rstrip('\n')
        if line.startswith(name+'=') or line.startswith('export '+name+'='):
            return line.split('=',1)[1].strip().strip('"').strip("'")
    return None
EOF

# 3. YAML validity + primary/fallback wiring
python3 -c "import yaml; d=yaml.safe_load(open('/root/.hermes/config.yaml')); print('OK')"
#   _config_version: 33, primary qwen-token-plan/qwen3.7-plus,
#   6 fallbacks diversified, aux/TTS/MoA → qwen-token-plan

# 4. LIVE API verification — models list ≠ chat completion
#   GET  {base}/models            → 21 models (3× keys)  ✅ auth works
#   POST {base}/chat/completions  → Pro seat: OK; Standard seat: 429 ×4  ❌
#   429 = key valid but throttled/quota-drained. 401 would mean wrong key.
#   Receipt claimed "HERMES-SEAT-OK" — could NOT be reproduced. False claim.

# 5. Process env — key in file ≠ key in running process
PID=$(systemctl show hermes-asi-gateway.service -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep -i qwen
#   → QWEN_HERMES_API_KEY NOT in process env. Gateway sourced
#     /root/AAA/agents/hermes-asi/runtime/.env (22 vars, no QWEN) via
#     hermes-gateway-secure.sh + systemd EnvironmentFile=vault.flat.env
#     (had QWEN_API_KEY/QWEN_BAILIAN_KEY, not the new names).
#   → "Restart will pick it up" = FALSE. Restart alone was useless.

# 6. Registry/seat doc — read record-by-record
#   seats.yaml: agent's own patch marked seat_b797 (OpenClaw, key STILL
#   placeholder) as POPULATED while its own comment said "STILL EMPTY";
#   seat_39bf (Hermes Standard, actually wired) left EMPTY.
#   → An agent patch can contradict its own comment. Read the file.
```

## Discriminators learned (durable)

| Signal | Meaning | Action |
|---|---|---|
| 401 | wrong/expired key | re-wire, don't throttle-hunt |
| 429 | key valid but quota/throttle | check seat quota; leaked-key drain kills smaller seat first |
| models-list 200 | auth works | does NOT prove chat/completions works — test the exact op |
| patch refused by verifier | tool-level refusal | file may still be changed via CLI — check mtime |
| key in SOT file | disk truth | NOT process truth — check `/proc/<pid>/environ` |
| seats/registry "POPULATED" | self-report | read the file record-by-record vs vault |
| `systemctl restart` same PID | --replace conflict | kill -9 stale PID, restart, verify MainPID |

## Zen fix applied (structural, not just trigger)

The session's root-cause framing: placeholder keys were the TRIGGER; the
STRUCTURE was multi-file env sprawl — systemd reads a different file than
the generator writes; TWO generators (generate-flat.py + generate-flat.sh)
wrote the same flat; three env pairs with drifting key names; no automated
verify actually running.

Fix:
```bash
cp vault.flat.env vault.flat.env.bak-zen-fix-<ts>          # backup real file
mv generate-flat.py generate-flat.py.disabled-<ts>         # one generator
rm vault.flat.env && ln -s kunci-mas.flat.env vault.flat.env  # symlink, not copy
sed -i 's|EnvironmentFile=.*|EnvironmentFile=/root/.secrets/kunci-mas.flat.env|' /etc/systemd/system/hermes-asi-gateway.service
systemctl daemon-reload && systemctl restart hermes-asi-gateway.service
# verify: readlink -f vault.flat.env + systemctl show -p EnvironmentFile --value
```

## Adjacent: FORGE two-token drift + OpenClaw false gate

- FORGE gateway "Telegram token rejected" since Jul 31. `getMe` showed
  `FORGE_BOT_TOKEN` works while `TELEGRAM_BOT_TOKEN` (the one the gateway
  reads, gateway/config.py:1471) 401s — same bot ID, different secrets.
  Fix: sync config-referenced var to the working value, restart, verify
  MainPID changed (kill -9 stale PID first).
- OpenClaw refused to post a seal to the AAA group citing allowlist
  (`groups: {"-1003753855708": {}}`), but its own bindings referenced the
  AAA group (`bindings[3].match.peer.id = -1004446358629`). Allowlist
  governs SEND; bindings are match rules. Hermes already delivers cron
  output to AAA group daily. Capability denial citing config = claim to
  probe, not a boundary to accept.
