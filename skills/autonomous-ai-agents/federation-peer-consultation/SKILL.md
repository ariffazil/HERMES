---
name: federation-peer-consultation
description: 'Consult peer agents in the arifOS federation (OpenClaw @AGI_ASI_bot, OpenCode, Codex, Kimi) headlessly via the OpenClaw gateway CLI, and independently verify any agent self-report (POV, audit, analysis) against canonical docs + live health before relaying. Triggers: "ask OpenClaw what it thinks about X", "what is <agent> POV on Y", or Arif pastes another agent report expecting independent verification.'
---

# Federation Peer Consultation

Asking another agent in the arifOS federation for its POV/status, and verifying what it says. Two halves: (1) getting the answer, (2) not relaying it at face value.

## 1. Headless Q&A via the OpenClaw gateway (no Telegram channel needed)

```bash
# Gateway must be up first (T1-class restart; clean-shutdown units restart fine):
systemctl start openclaw-gateway
# wait until: curl -s http://127.0.0.1:18789/health → {"ok":true,"status":"live"}

# List agents if unsure of the id:
openclaw agents list

# Ask the question — runs a full agent turn via the gateway, prints the reply to stdout:
openclaw agent --agent main --message "<soalan>" --timeout 240
```

- **Pitfall:** `openclaw agent --message "..."` WITHOUT `--agent <id>` / `--session-key` / `--session-id` / `--to` fails with `Error: No target session selected.` Always pass an explicit target.
- **Agent ids observed:** `main` (default, the OpenClaw "GUTS" persona), `opencode`, `codex`, `kimi` — all model `fed/opencode`, workspaces under `~/.openclaw/workspace*`.
- **Output noise:** the reply is preceded by a big box of missing-plugin config warnings. Filter with:
  `grep -v -E "plugin not installed|Config warnings|│|◇|├|╯|╮|╭"`
- Message the agent in Malay for Arif-facing answers (matches federation language) unless the question is technical/English-native.
- After one-off Q&A, confirm the desired end state for `openclaw-gateway` (it is `disabled`, so it won't auto-start on reboot) — leave running vs stop to restore found state. Report the state change honestly.

## 2. Verify every peer self-report before relaying

Arif pastes other agents' reports (audits, analyses, POVs) expecting independent verification — treat them as SELF-REPORTS:

- **The conflation pattern:** a federation agent describes what IT sees — its own gateway/route surface — and maps that onto the authority map. Observed: OpenClaw claimed AAA "adjudicates and issues verdicts" because AAA is the A2A face it routes through; actually AAA is `DISPLAY_ONLY` ("routes and displays, never judges") and verdicts come from 888_JUDGE in the arifOS kernel (:8088). Peer agents routinely blur "the door I use" with "the authority that decides".
- **Verify against:** `AAA/docs/ORGAN.md` (canonical human map), `AAA/federation/organs.yaml` (machine twin), and live `:port/health` probes. Authority ceilings (e.g. `DISPLAY_ONLY`, `JUDGE_ONLY`, `COMPUTE_ONLY`) are the ground truth.
- **Present the result as:** the agent's POV (verbatim or quoted) + a verification table (claim → ✅/⚠️/❌ → correction). Correct the architecture-layer claims, keep the experience-layer ones.

## Support files

- `references/peer-agent-consultation-2026-08-05.md` — observed session: exact command sequence, the OpenClaw-vs-AAA divergence caught, gateway state notes.
