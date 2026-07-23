# AGENTS.md — HERMES | arifOS Federation

> **DITEMPA BUKAN DIBERI** — Forged, not given.
> **Organ:** HERMES (7 of 7) | **Role:** Multi-Modal Bridge | **Layer:** L3 DOMAIN

## What This Repo Is

HERMES is the multi-modal bridge organ. It routes signals between Telegram ↔ arifOS ↔ agents and manages the federation's skill catalog. It bridges, never adjudicates.

- **Telegram edge:** Operator interface via port 8644
- **Skill catalog:** 31+ arif-specific skills under `skills/`
- **Authority:** OBSERVE_ONLY

## Build & Test

```bash
cd /root/HERMES
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"  # validate config
bash scripts/governance-gate.sh                                  # governance check
```

## Key Files

| File | Purpose |
|------|---------|
| `config.yaml` | Runtime configuration |
| `HERMES-COMMAND-MANIFEST.md` | Operator commands |
| `SOUL.md` | Hermes persona + voice |
| `skills/` | Federation skill catalog |
| `docs/SOUL.md` | Deep persona doc |
| `channel_directory.json` | Telegram channel registry |

## Conventions

- REPO= commit trailer required: `REPO=HERMES`
- Tags: `vYYYY.MM.DD` only
- Bridge organs NEVER adjudicate — route to arifOS
