# FQ Organ Flow — The Six-Layer Wiring (2026-08-04)

> **Status:** Live doctrine. Verified against arifFlow `:7073/health` + doctrine commits b2d72ebc, caf326e0, fdae3a0.
> **Doc pointer:** `/root/AAA/docs/GEOMETRY_FQ_G_J_RASA.md`

## The Six-Layer Flow (one-way up)

| # | Layer | Component | Channel | Function |
|---|-------|-----------|---------|----------|
| ① | Source | arifFlow daemon :7073 | HTTP | Cost-window pulse. Single source of truth. |
| ② | Mirror | `arifflow-fq-mirror.timer` + `fq-probe.sh v4` | systemd + filesystem | Polls /health every 5 min (TTL 300s) → `/root/AAA/state/flow_state.json` |
| ③ | Agents | Hermes / OpenCode / OpenClaw | filesystem | Read cache before action. Each tool call = receipt → feeds back to arifFlow. |
| ④ | Governance | `forge_evaluate` (G) + `forge_apex_encode` (J) + arif_judge | MCP | G fitness scalar (`is_canonical_g: true`), J sensitivity manifold (`is_canonical_g: false`). Judge uses FQ as throttle signal. |
| ⑤ | Federation | FED (router) + arifOS organs + VAULT999 | A2A | FED reads FQ to bias routing — cascade-first under OVERHEAT. Tier 666_JUDGE & 999_SEAL keep constitutional models. Seals count toward verify ratio. |
| ⑥ | Sovereign | kabarkan | observability plane | Surfaces FQ drift alerts (cron `drift-alert`) + trends. **Outside the loop** — tells Arif what the system sees about itself. |

## The Key Insight

> **FQ doesn't control — it rhythms. arifFlow doesn't command — it mirrors. Governance doesn't override — it informs.**

The brake is the engine seeing itself burn. Cooling = own act, bukan external command. This is the constitutional floor.

## Cache File Contract

**Path:** `/root/AAA/state/flow_state.json`
**TTL:** 300s (drift > 0.3 → FQ_SIGNAL_DRIFT → use live)
**Writer:** `arifflow-fq-mirror.timer` → `/root/scripts/fq-probe.sh` v4

**Schema:**
```json
{
  "fq": 15.46,
  "verdict": "OVERHEAT",
  "execute_count": 24,
  "verify_count": 20,
  "source": "arifFlow :7073 — single source of truth",
  "timestamp": "2026-08-04T..."
}
```

## Governance Tools — G vs J Labels

| Tool | Function | Label |
|------|----------|-------|
| `forge_evaluate` | `G = (A × P × E × X)^(1/4)` — constitutional fitness scalar | `is_canonical_g: true` |
| `forge_apex_encode` | `J = ∂T/∂G` — task sensitivity manifold | `is_canonical_g: false` |

**Pitfall:** J is NOT a new F1-F13 floor. No L14 without F13 seal. J-space recompute if `|J| > 0.6` on changed field.

## FED Routing Under FQ

| Condition | FED behavior |
|-----------|-------------|
| FQ ≤ 1 (BALANCED/WATCHING) | Normal routing — best quality per task class |
| FQ 3–10 (OPTIMAL) | Forge normal |
| FQ > 10 (OVERHEAT) | **Advisory hint: cascade-first.** Expensive providers → cheaper cascades. **Tier 666_JUDGE & 999_SEAL keep constitutional models** — never compromise on judge/seal. |

## Kabarkan — The Observer Outside

Kabarkan is **outside the FQ loop**. It doesn't read FQ to make decisions — it surfaces FQ to Arif. This is the **observer-as-surface** pattern:

- Internal loop: arifFlow → cache → agents → execute/verify → arifFlow
- External surface: kabarkan reads the loop's outputs and formats for Arif

The sovereignty boundary: Arif doesn't see FQ directly — Arif sees what the loop reports about itself. Observer ≠ observed (paradox acknowledged).

## Verification Commands (live probes)

```bash
# 1. Mirror timer active
systemctl is-active arifflow-fq-mirror.timer

# 2. arifFlow live
curl -sf http://127.0.0.1:7073/health | jq .fq

# 3. Cache freshness + match
python3 -c "import json;d=json.load(open('/root/AAA/state/flow_state.json'));print(d['fq'],d['verdict'])"

# 4. Recent commits
cd /root/AAA && git log --oneline -3
cd /root/A-FORGE && git log --oneline -3
cd /root/HERMES && git log --oneline -3
```

**All four should report:**
- Timer: `active`
- FQ live + cache: same value, verdict OVERHEAT/BALANCED (whatever the window says — NOT a constant)
- Commits: `b2d72ebc`, `caf326e0`, `fdae3a0` (or successors)

## Related

- `/root/AAA/docs/GEOMETRY_FQ_G_J_RASA.md` — RASA, FQ, G, J definitions
- `/root/AAA/docs/FQ_SCALE_STANDARD.md` — canonical scale (commit 56ad6d60)
- `/root/AAA/docs/AUTONOMOUS_GOVERNANCE.md` §2A — pre-execute FQ check
- `/root/AAA/docs/TOOLS.md` — G↔J table + FED advisory hint
- `references/fq-formula-inversion-fix-2026-07-29.md` — why NEVER recompute FQ
- `references/fq-staleness-2026-07-26.md` — cache freshness pitfall

DITEMPA BUKAN DIBERI ⚒️