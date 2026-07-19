# Dream Engine Activation — Full Session Trace

> Activated: 2026-07-12 by Hermes under SOVEREIGN session SEAL-3f6a404296b74a9e
> Substrate: OpenClaw Dream Engine v0.1 (Jun 7) + Federation Dream Engine skill (Jun 16)

## Initial State

- **DREAMS.md**: 4 orphan copies across sister workspaces (opencode, codex, kimi, openclaw). All contained 240 lines of "A memory trace surfaced, but details were unavailable in this run." — dead artifact from a broken introspection subsystem. Cleaned.
- **Dream Engine v0.1**: 9 files, 100KB at `/root/.openclaw/workspace/dream_engine/`. DESIGN.md, consolidate.py (302 lines), golden tests. Timer NEVER enabled — systemd units existed in prototype/ but never deployed. Pending Arif's go since Jun 7.
- **Federation skill**: 321-line SKILL.md at `/root/AAA/skills/AGI-dream-engine/` with Phase 0-3 roadmap. prototype/systemd/ dir with .service + .timer files.
- **Cron-receipts**: 22 stale receipts (pre-Jul 07) mixed with 21 active ones. Consolidated to `.archive/`.

## Env var path resolution

consolidate.py checks `SUPABASE_SERVICE_KEY` but vault.flat.env exports `SUPABASE_SERVICE_ROLE_KEY`. Fixed by adding fallback:
```python
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
```

## Known drift (documented, not fixed)

Supabase table `arifosmcp_memory_records` has no column `id`. Query returns 42703. Phase 0 bug from implementation plan. L4 audit currently skips on this error. Per architect's ruling: do not fix until 3-7 nightly cycles establish baseline.

## Timer deployment

| Item | Value |
|------|-------|
| Timer file | `/etc/systemd/system/arif-dream.timer` |
| Service file | `/etc/systemd/system/arif-dream.service` |
| WorkingDirectory | `/root/.openclaw/workspace/dream_engine` |
| ExecStart | `/opt/arifos/venv/bin/python3 dreams/consolidate.py --execute` |
| EnvironmentFile | `/root/.secrets/vault.flat.env` |
| Schedule | 04:01 MYT daily (20:01 UTC) |
| Self-heal | Restart=on-failure, RestartSec=300 |
| First dry-run | 2.450s CPU, 119.2MB memory peak, clean exit |
| Current mode | --execute (shadow namespace writes, L1-L3 only) |

## APEX Governance

After activation, applied APEX evaluation:

- A=0.85, P=0.50, E=0.90, X=0.65, Φ=0.35
- G = 0.087 (SESAT — trajectory up 19x from 0.0046)
- C_dark = 0.149 (LURUS — below 0.30 threshold, no longer BANGANG)

Entropy measurement added to every receipt: per-layer normalization (0-1), total_h, dS label (ENTROPY_UP/ENTROPY_DOWN/STEADY).

## Dual-Loop Lifecycle Diagram

Architecture diagram showing Waking Loop + Dreaming Loop as two sides of the same substrate:
`/root/A-FORGE/forge_work/2026-07-12/DUAL-LOOP-LIFECYCLE.html`

Dream Engine is now canonical in the architecture — not a side organ.

## Governing Doctrine

- Dream Engine runs in execute mode but L4 is skipped (schema drift).
- Self-heal retries on failure after 5 min.
- Dry-run was the correct first phase. Execute mode only after APEX evaluation showed C_dark < 0.30.
- L4 audit readiness checklist at `references/l4-audit-readiness-checklist.md`.

## Key lesson

The Dream Engine was not broken. It was complete, tested, and never activated. The only missing step was someone running cp, systemctl daemon-reload, and systemctl enable --now. The env vars needed one fallback line. The column drift was known and documented — not a blocker for activation, only for L4 audit.
