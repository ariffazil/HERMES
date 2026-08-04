# LiteLLM FED FLAME FRAME v2 — 2026-08-04 Reactivation

> **Status:** SUPERSEDES `litellm-federation-gateway-2026-08-02.md` and the REMOVE
> proposal in `unified-routing-audit-2026-08-03.md`. That audit proposed dissolving
> LiteLLM into FED Router. The 2026-08-04 review came to the opposite conclusion:
> LiteLLM is the runtime proxy; FED Router is the intelligence plane. **Keep both.**

## What actually happened (2026-08-04)

The 2026-08-03 audit (3-layer accretion) was right about FLAME being dead and
right that there were 3 redundant config layers. But it was wrong about REMOVING
LiteLLM. The 2026-08-04 wiring event established:

- **Flat sibling layout** — `opencode | openclaw | agi-333 | hermes-asi | asi-555 | apex-888 | dispatch | asi-555-vision` all registered as LiteLLM `model_name` aliases. Agents pick alias names, never provider details.
- **Multi-provider failover per alias** — each alias has 2-3 backend entries sharing the same `model_name` (DeepSeek → MiMo → MiniMax for opencode; MiMo → MiniMax for hermes-asi). LiteLLM load-balances / fails-over across them.
- **Real upstream auth** — `MAST_KEY` in env (or `LITELLM_MASTER_KEY` on no-DB mode) is the Bearer token. Auth is real, not localhost-bypass.
- **Provider count** — 4 live providers wired into LiteLLM: DeepSeek, MiMo, MiniMax, Qwen Token Plan. MuleRouter, OpenRouter, TokenRouter are dead/orphaned.

## First-use verification protocol (use this BEFORE claiming auth/network state)

**The trap:** I declared "Drop OpenRouter", "401 auth-gated", "no master key" in
the same breath without once running curl. All three were wrong. Lesson: never
summarize ablation claims without runtime verification.

```bash
# 1. Config exists + readable
cat /root/A-FORGE/litellm-config.yaml | head -20

# 2. Process alive
ps aux | grep litellm | grep -v grep

# 3. Master key in env (NOT null, NOT 13-char placeholder)
echo "LITELLM_MASTER_KEY length: ${#LITELLM_MASTER_KEY}"

# 4. Models endpoint (proves auth + model_name registration)
curl -s http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" | python3 -m json.tool | head -30

# 5. Real completion (proves upstream provider chains actually work)
# USE max_tokens >= 20. With max_tokens=10, reasoning models return empty
# content (output goes to reasoning_content, not content).
curl -s -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"say pong"}],"max_tokens":50}'
# Check: model echoed == requested alias, content non-empty
```

**Each step proves a different layer.** Skipping any one means you're guessing.

| Step | What it proves |
|---|---|
| 1 | Config file exists, parseable, current shape |
| 2 | Process running, not zombie |
| 3 | Key is present in live env (not just config) |
| 4 | Auth works, model_name aliases registered |
| 5 | Upstream provider chain actually completes (not just registered) |

## Dead-provider hygiene (token_bank.db)

After FED activation, the old MuleRouter-era providers are orphaned in `token_bank.db`
but still have spend history. **Never `DELETE` them — audit evidence.** Mark them:

```sql
UPDATE providers
SET notes = 'ARCHIVED 2026-08-04: not in litellm-config.yaml, orphaned from old MuleRouter routing. ' || COALESCE(notes,'')
WHERE provider_name IN ('openrouter', 'mulerouter', 'tokenrouter')
  AND notes NOT LIKE 'ARCHIVED%';
```

Keep `token_bank_spend` rows intact — they're the audit trail. Mark inactive in
notes only. Filter UI (if any) can `WHERE notes NOT LIKE 'ARCHIVED%'`.

**DB path:** `/root/.local/share/arifos/token_bank.db` (NOT `/root/A-FORGE/fed/`).

## Systemd service name gotcha

When debugging gateways, the systemd unit name is usually NOT the binary name:
- `openclaw-gateway` not `openclaw` (the binary is `openclaw-gateway`)
- `litellm-proxy` not `litellm`
- `flame-api` not `flame`

Before declaring "no systemd unit found", check both `systemctl cat <binary>` AND
`systemctl cat <concise-name>`. Then `ls /etc/systemd/system/multi-user.target.wants/`
to see which are enabled.

A process alive in `ps` but `systemctl is-active` says `inactive` may mean:
- Started by an old `nohup` or supervisor, not systemd (orphan)
- Started by a different systemd unit with a related name
- Unit lost its `WantedBy=multi-user.target.wants/` symlink

Verify with `cat /proc/<PID>/cgroup` — if it shows `/system.slice/<unit>.service/`,
it IS managed by systemd, just with a different unit name than you guessed.

## Wawabot (or any new external client) wiring pattern

New client → LiteLLM is trivial. They just need:

```bash
LITELLM_BASE_URL=http://<server-ip>:4000/v1   # or 127.0.0.1 for local
LITELLM_API_KEY=$LITELLM_MASTER_KEY          # same env var, same secret
# OpenAI-compatible: model field = "hermes-asi" / "opencode" / etc.
```

No LiteLLM config edits needed. No new agent registration. Just point the client
at the proxy and use the alias names. This is the whole point of the
abstraction layer.

## What the 2026-08-03 audit got wrong

- Predicted "remove LiteLLM entirely" — WRONG. LiteLLM was reactivated within 24h
  as the actual runtime proxy. FED Router is advisory/intelligence, not the
  runtime plane.
- Overstated FLAME's death — engine stayed running but API was dead. Different
  units, different systemd files.
- Misread "key_env in 8 places" — those weren't duplicates, they were routes
  to different providers needing different keys.

**Lesson:** Consolidation audit conclusions should be phrased as proposals
("remove X if Y stays alive") not mandates ("remove X"). When the underlying
service is reactivated within a day, the conclusion inverses.
