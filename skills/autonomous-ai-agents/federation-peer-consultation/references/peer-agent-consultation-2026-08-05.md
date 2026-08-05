# Peer-agent consultation — headless OpenClaw Q&A (observed 2026-08-05)

## Trigger
Arif pasted OpenCode's (333-AGI) POV on AAA and asked: "Can u ask Openclaw what is it's pov on AAA."

## Sequence that worked
1. Probe: `curl -sf 127.0.0.1:18789/health` → DOWN; `systemctl status openclaw-gateway` → `disabled`, clean shutdown (exit 0) at 10:27 UTC that day.
2. `systemctl start openclaw-gateway`; ~10s later `curl :18789/health` → `{"ok":true,"status":"live"}`; webhook re-advertised on https://openclaw.arif-fazil.com/telegram-webhook.
3. `openclaw agents list` (filter the box-of-warnings noise) → agents: `main` (default, 5 routing rules), `opencode`, `codex`, `kimi` — all model `fed/opencode`, workspaces under `~/.openclaw/workspace*`.
4. `openclaw agent --agent main --message "<soalan>" --timeout 240` → full Malay answer printed to stdout (~40s). First attempt WITHOUT `--agent` failed: `Error: No target session selected.`

## Divergence caught (the verification lesson)
OpenClaw's POV claimed AAA "adjudicates"/"issues verdicts" (SEAL/HOLD/SABAR/VOID) and "AAA menghukum" — but per ORGAN.md + AAA README, AAA is DISPLAY_ONLY ("routes and displays, never judges"); verdicts come from 888_JUDGE in the arifOS kernel (:8088). OpenClaw conflated the A2A gateway surface (what it sees) with kernel authority (where judging lives).

Handling that worked: present peer POV as experience-layer truth, correct architecture-layer claims against canonical docs + live health. Response shape: POV quoted → verification table (✅/⚠️/❌ per claim) → conclusion. Never relay a peer self-report at face value (Arif expects independent verification of other agents' reports).

## State note
`openclaw-gateway` unit is `disabled` (won't auto-start on reboot) — manual `systemctl start` brings it back. After one-off Q&A uses, confirm desired end state with Arif (leave running vs stop to restore found state).
