# HERMES Copilot Instructions

> **Organ:** HERMES (7 of 7) | **Layer:** L3 DOMAIN | **Role:** Multi-Modal Bridge

HERMES is a bridge organ — it routes signals, never adjudicates. No build/test suite, no code compilation. Key operations:

```bash
# Validate config
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Governance check
bash scripts/governance-gate.sh

# Skill catalog count
find skills/ -name 'SKILL.md' | wc -l
```

- **Authority:** OBSERVE_ONLY
- **Secrets:** `/root/.secrets/vault.env`
- **Tags:** `vYYYY.MM.DD` only
