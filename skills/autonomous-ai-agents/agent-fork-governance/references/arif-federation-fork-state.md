# Arif Federation — Fork/Divergence State (snapshot 2026-08-05)

Live numbers measured on the box; re-probe before SEAL-grade claims (F2 dynamic-state rule).

## Hermes — REAL FORK (the only code-level fork in the federation)

| Metric | Value |
|---|---|
| Live install | `/usr/local/lib/hermes-agent` (systemd: hermes-asi-gateway, + A2A listener :18087, MCP bridge) |
| Fork remote | `git@github.com:ariffazil/hermes-agent.git` |
| Installed version | v0.18.2 (2026.7.7.2) |
| Local HEAD | `14995335b` (2026-07-24) — "fix(gov): model-picker fail-closed gate + Go routing fix + Telegram location rate-limit" |
| Fork base (upstream merge-base) | `aec33189` (≈ 2026-07-07) |
| Upstream HEAD (2026-08-05) | `1be70d6` |
| Drift behind upstream | ≈ 5,353 commits |
| Carried (ahead) | 2 commits: `14995335b` (gov gate + telegram rate-limit + OCR script) and `57eabe30f` (OCR SKILL.md) |

Note: `14995335b` actually carries THREE concerns (fail-closed gate, telegram location rate-limit, OCR extraction script); `57eabe30f` is just the OCR SKILL.md. So "2 commits" ≈ 3 concerns.

### Sovereignty boundary — protected files (upstream merge touching these = automatic HOLD)
- `hermes_cli/model_switch.py` — fail-closed gate (F1/F12)
- `hermes_cli/models.py` — fail-closed gate
- `plugins/platforms/telegram/adapter.py` — Telegram location rate-limit

### Refusal log verdicts (2026-08-05)
- OCR skill → ACCEPT (generic; PR to upstream; fork shrinks by one commit)
- gov fail-closed gate → REFUSE (arifOS doctrine F1/F12; upstream would ship fail-open for UX — the first genuine divergence-by-design point)

Ledger: `/root/docs/HERMES_FORK_DIVERGENCE.md` (draft; includes sovereignty boundary + refusal log + rebase contract).

## OpenClaw — STOCK BINARY, custom deployment
- `~/.npm-global/bin/openclaw`, version 2026.7.1-2 (0790d9f). NOT forked.
- Divergence lives in deployment: gateway process, `/root/.openclaw/` workspace (1.1G), custom bots under `/root/.openclaw/workspace/bots/` (11M).
- Governance seams already present: `exec-approvals.json` (mode 600), substrate gate in `bot.py` (ARIFOS_MCP_URL → http://127.0.0.1:8088/mcp, added ~2026-06-11, backup `bot.py.pre-substrate-gate-2026-06-11` exists), `/000-/999` machine verbs with HOLD/VOID.
- Refork trigger per doctrine: only if F1 fail-closed violation or proxy-bypass is detected (none detected 2026-08-05; exec-approvals.json ≈ 171 bytes = gate nearly empty — audit pending).

## OpenCode — STOCK
- `~/.npm-global/bin/opencode`, 1.18.11. No fork, no patch. Governed via 777-FORGE bot wrapper.

## Storage doctrine (Arif, ratified 2026-08-05)
1. **Substrate (hardware/filesystem):** DO NOT FORK / DO NOT TOUCH — pure infrastructure, like the kernel.
2. **Agent boundary (OpenClaw/OpenCode access):** read free (ro) to metabolize; writes restricted to a designated scratchpad; permanent-dir writes/config changes/deletes must be proxied to kernel → explicit 888_HOLD. This is where F1 reversibility risk lives.
3. **Persistent state (ATLAS333 ledger):** permanent path, backed up, append-only from agents; DDL kernel/sovereign only.

## Related canonical docs
- ATLAS333 ledger persistence contract: `arifOS/docs/ATLAS333_INTELLIGENCE_FLOW.md` §8.1 (sealed_by: ARIF :: 2026-08-05)
- Ledger DB: `/root/.local/share/arifos/atlas333/atlas_ledger.db` (SQLite `paradox_events`, 640 root:arifos)
