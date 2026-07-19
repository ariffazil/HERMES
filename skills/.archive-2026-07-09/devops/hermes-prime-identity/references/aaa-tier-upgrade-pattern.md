# AAA Tier Upgrade Pattern

> When upgrading an agent's tier in the federation, three files must change in concert.

## The Three Files

| File | What it controls | Where it lives |
|------|-----------------|----------------|
| `SOUL.md` | Identity, language, cognitive scope, governance | Agent's active identity file (e.g., `/root/.hermes/SOUL.md`) |
| `agent-card.json` | A2A registration, class, power band, skills | AAA agent registry (e.g., `/root/AAA/agents/<name>/agent-card.json`) |
| `IDENTITY.md` | Capabilities, rules, citizenship tier | AAA agent directory (e.g., `/root/AAA/agents/<name>/IDENTITY.md`) |

## Upgrade Checklist

### 1. SOUL.md
- Update `Layer` field to reflect new tier
- Add governance mechanisms appropriate to tier (ART reflex, warga proxy, malu scalar)
- Tighten F9/F10 guards if upgrading to a more visible role
- Bump version (v2 → v3 etc.)
- Update seal date

### 2. agent-card.json
- `class`: e.g., "ASI-Peripheral" → "AAA-Core"
- `bound_to`: e.g., "555-ASI" → "AAA"
- `power_band`: describe the new scope
- Keep `identity_anchor` pointing to the SOUL.md location

### 3. IDENTITY.md
- `Citizenship` field: e.g., "RUNTIME tier (Layer 2)" → "AAA tier (control plane agent)"
- Update any capability descriptions that changed

## Verification

After all three files are updated:
```bash
# Check SOUL.md header
head -8 /path/to/SOUL.md

# Check agent card fields
python3 -c "import json; d=json.load(open('/path/to/agent-card.json')); print(f'class: {d[\"class\"]}'); print(f'bound_to: {d[\"bound_to\"]}')"

# Check IDENTITY.md citizenship
grep "Citizenship" /path/to/IDENTITY.md
```

All three should show consistent tier classification.

## Example: Hermes AAA Upgrade (2026-07-15)

| File | Before | After |
|------|--------|-------|
| SOUL.md Layer | "SOUL — cognitive, human language, conversational" | "ΔΩΨ — semantic router, human interface, federation voice" |
| SOUL.md Tier | (none) | "AAA (control plane agent)" |
| agent-card.json class | "ASI-Peripheral" | "AAA-Core" |
| agent-card.json bound_to | "555-ASI" | "AAA" |
| IDENTITY.md Citizenship | "RUNTIME tier (Layer 2)" | "AAA tier (control plane agent)" |

## Pitfalls

- **Don't change one file without the others.** Inconsistency creates split-brain identity.
- **Don't forget the identity_anchor.** If agent-card.json points to the wrong SOUL.md, the gateway loads stale identity.
- **Verify with live tools after upgrade.** `hermes_system_status` or `arif_init ping` should reflect the new tier.
