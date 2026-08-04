# Multi-Location Provider Key Rotation — 2026-08-04 Case

When `MINIMAX_API_KEY` died (HTTP 401 returned from both `/v1/models` and
`/v1/chat/completions`), the rotation required updates in 5+ independent
files. The KUNCI-MAS SOT pattern covers systemd `EnvironmentFile` consumers
but does NOT cover the Hermes gateway launcher path.

## Timeline

1. **Discovery** (`grep -rln "MINIMAX_API_KEY"`): found 5 independent files
   holding the stale key value. None were symlinks to each other — each
   was a real, separately-edited file.

2. **Initial fix (missed one)**: touched KUNCI-MAS + 4 per-profile files.
   Did NOT touch `/root/.hermes/.env`. litellm-federation picked up the
   new key (probed 200), but Hermes `vision_analyze` continued to 401.

3. **Cross-probe revealed gap**: litellm `/v1/chat/completions` returned
   200 with new key; Hermes gateway returned 401. The two layers
   disagreed. Cross-probe of BOTH paths caught it.

4. **Catch-up fix**: updated `/root/.hermes/.env` independently.
   Restarted hermes-asi-gateway. `vision_analyze` then 200.

## All 5+ Locations (verified)

For provider `minimax`, all locations held the same key name
`MINIMAX_API_KEY` but were 5 separate files:

| # | File | Ingestion path | Restart needed |
|---|------|---|---|
| 1 | `/root/.secrets/kunci-mas.env` | SOT → `make vault-generate` → flat.env → `EnvironmentFile=` | regenerate flat |
| 2 | `/root/.hermes/.env` | Hermes auth/dotenv loader at gateway startup | restart hermes-* gateway |
| 3 | `/root/.hermes/profiles/hermes_asi/.env` | `hermes-asi-gateway-secure.sh` source | restart hermes-asi-gateway |
| 4 | `/root/.hermes/profiles/hermes_apex/.env` | `hermes-apex-gateway.sh` source | restart hermes-apex-gateway |
| 5 | `/root/.hermes/profiles/hermes_forge/.env` | `hermes-forge-gateway.sh` source | restart hermes-forge-gateway |
| — | systemd `EnvironmentFile` for litellm-federation | resolved from flat.env symlink | restart litellm-federation |

## Why main `~/.hermes/.env` is its own slot (not a symlink)

Empirical: at last check, `/root/.hermes/.env` and the per-profile files
are independent non-symlinked files. The `per-profile` config inheritance
happens at the Hermes Agent config layer (config.yaml), NOT the env file
layer. So even though `~/.hermes/config.yaml` may set
`vision.provider: minimax` from main config, the env-resolved `API_KEY`
can still come from the per-profile `.env`, NOT from main `~/.hermes/.env`.

This is a separate dim of multi-location rot from the symlink-based
"per-service env" pattern documented in Step 1 of the parent SKILL.

## Diagnostic Recipe (single command)

```bash
# Count actual active locations of a provider's API key
# (filters out backups, sessions, curator_backups, and skills.backup)
KEY=MiniMax
grep -rln "${KEY}_API_KEY\|^MINIMAX_API_KEY" /root/.secrets /root/.hermes 2>/dev/null \
  | grep -v "\.curator_backups\|/backups/\|/sessions/\|skills\.backup\|env-backups\|/cache/" \
  | sort -u

# Expect 5 hits for a per-profile provider key. >5 → suspect symlinks duplicating.
# <5 → suspect a profile was never wired (also a bug).
```

## Prevention: Make these files symlinks OR generate them

Long-term fix candidates (not yet implemented):

- **Option A**: Make `/root/.hermes/.env` a symlink to KUNCI-MAS (or to a
  generated flattened view). Same for per-profile files. Eliminates the
  multi-edit rotation.
- **Option B**: A `make vault-publish-hermes` target that copies SOT keys
  matching a `HERMES_*` prefix into all 5 Hermes env paths.
- **Option C**: A pre-rotation `vault-verify-hermes` check that asserts
  `~/.hermes/.env` and per-profile `.env` files match the SOT for keys
  matching `^(MiniMax|MIMO|QWEN|MINIMAX|OPENROUTER|TOKENROUTER)_`. Fails
  CI if any diverge.

Until one of these is implemented, the multi-location sweep in Step 6b
of the parent SKILL remains the manual procedure.
