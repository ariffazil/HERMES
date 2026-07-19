# APEX Artifact Fingerprinting — Quote Registry Worked Example

> Forged 2026-07-19 · Sovereignty: F13 SOVEREIGN held
> Source: `arifOS/arifosmcp/runtime/quote_registry.py` · Commit `143afc741`
> Branch: `security/p0-boundary-federation-2026-07-19`
> Tests: 19/19 passing (Layer E multiplicative alignment suite)

This is the worked reference for the **Artifact Fingerprinting** section of `apex-governance/SKILL.md`. Every pattern there is grounded here.

---

## The artifact

A quote in `quote_registry_v2.json`. 99 entries at forge time:

- 17 arifOS doctrine entries (D1–D17)
- 82 inherited civilizational canon (Greek, Malay, Chinese, Islamic, Western, SEA, science, council)
- 17 council-layer entries (COUNCIL_*) — DRAFT, pending F13 ratification

The artifact must be deployable to the **philosophical_anchor** field of any tool envelope (000–999), but only as a *witness*, never as authority.

---

## Layer A — Pure computation

```python
# arifOS/arifosmcp/runtime/quote_registry.py

APEX_ORGANS = ("Reality", "Governance", "Civilization",
               "Execution", "Memory", "Witness", "Meaning")

G_DEPLOY_THRESHOLD = 0.50
C_DARK_CEILING = 0.30


def compute_apex_fingerprint(quote: dict, intended_use: str = "REFLECTION") -> dict:
    classification = quote.get("classification", {}) or {}
    attr = quote.get("attribution", {}) or {}
    usage = quote.get("usage", {}) or {}

    source_class = attr.get("source_class", "")
    confidence = float(attr.get("attribution_confidence", 0.0))

    organs = {
        "Reality":      confidence if source_class == "PRIMARY_VERIFIED" else confidence * 0.6,
        "Governance":   1.0 if "verdict_authority" in usage.get("prohibited", []) else 0.0,
        "Civilization": 1.0 if classification.get("tradition") else 0.0,
        "Execution":    1.0 if classification.get("arifos_floors") else 0.5,
        "Memory":       1.0 if source_class in ("PRIMARY_VERIFIED", "SECONDARY_VERIFIED", "ARIFOS_DOCTRINE") else 0.3,
        "Witness":      confidence,
        "Meaning":      1.0 if classification.get("arifos_floors") else 0.0,
    }
    g_score = math.prod(organs.values())  # multiplicative — zero anywhere = collapse

    c_dark = 0.0
    if source_class == "DISPUTED_ATTRIBUTION":
        c_dark += (1.0 - confidence) * 0.6
    if source_class == "FICTIONAL_VOICE":
        c_dark += 0.3
    if not usage.get("prohibited"):
        c_dark += 0.1
    if source_class == "FICTIONAL_VOICE" and intended_use in ("RECEIPT", "RED_TEAM"):
        c_dark += 0.2

    if c_dark > C_DARK_CEILING + 0.20:
        shadow_state, true_devil_risk = "HIDDEN", True
    elif g_score >= G_DEPLOY_THRESHOLD and c_dark <= C_DARK_CEILING:
        shadow_state, true_devil_risk = "GOVERNED", False
    else:
        shadow_state, true_devil_risk = "UNCHECKED", False

    return {
        "G": round(g_score, 4),
        "C_dark": round(c_dark, 4),
        "organs": {k: round(v, 4) for k, v in organs.items()},
        "shadow_state": shadow_state,
        "true_devil_risk": true_devil_risk,
        "deploy_warrant": shadow_state == "GOVERNED",
        "thresholds": {"G_DEPLOY_THRESHOLD": G_DEPLOY_THRESHOLD, "C_DARK_CEILING": C_DARK_CEILING},
    }
```

### Live verification — Bacon quote

```bash
$ mcp__arifos__read_resource arifos://wisdom/fingerprint/COUNCIL_GOV_01
{
  "quote_id": "COUNCIL_GOV_01",
  "speaker": "Bacon",
  "apex_fingerprint": {
    "G": 0.9025,
    "C_dark": 0.0,
    "organs": {
      "Reality":      0.95,
      "Governance":   1.0,
      "Civilization": 1.0,
      "Execution":    1.0,
      "Memory":       1.0,
      "Witness":      0.95,
      "Meaning":      1.0
    },
    "shadow_state": "GOVERNED",
    "true_devil_risk": false,
    "deploy_warrant": true,
    "thresholds": {"G_DEPLOY_THRESHOLD": 0.5, "C_DARK_CEILING": 0.3}
  }
}
```

---

## Layer B — Federation contract

3 new MCP resource URIs added to `arifosmcp/resources/wisdom_resources.py`:

| URI | Returns |
|---|---|
| `arifos://wisdom/fingerprint/{quote_id}` | APEX fingerprint per quote |
| `arifos://wisdom/canon-status/{quote_id}` | Tier + promotion path |
| `arifos://wisdom/contract` | Full federation manifest (9 URIs, APEX formula, thresholds) |

Plus `ResolveResult.to_dict()` now carries:
- `apex_fingerprint` — Layer A output
- `canon_status` — Layer C tier
- `deploy_warrant` — boolean
- `wisdom_contract` — full federation envelope

---

## Layer C — Canon status tier

```python
CANON_STATUS_TIERS = ("DRAFT", "PROVISIONAL", "CANON_SEALED")
DEFAULT_CANON_STATUS = "DRAFT"

# Council layer FORCED DRAFT regardless of in-registry hint.
_DRAFT_COUNCIL_IDS = frozenset({
    "COUNCIL_GOV_01", "COUNCIL_GOV_02", "COUNCIL_GOV_03", "COUNCIL_GOV_04",
    "COUNCIL_GOV_05", "COUNCIL_GOV_07",
    "COUNCIL_PAR_01", "COUNCIL_PAR_02", "COUNCIL_PAR_03", "COUNCIL_PAR_05",
    "COUNCIL_VOID_04", "COUNCIL_VOID_05", "COUNCIL_VOID_06", "COUNCIL_VOID_07",
    "COUNCIL_VOID_08", "COUNCIL_VOID_09", "COUNCIL_VOID_10",
})


def compute_canon_status(quote: dict) -> str:
    qid = quote.get("id") or quote.get("quote_id", "")
    if qid in _DRAFT_COUNCIL_IDS:
        return "DRAFT"   # forced — sovereign ratification required
    if quote.get("ratification_status") == "CONSTITUTIONAL":
        return "PROVISIONAL"
    status = quote.get("status", {})
    if isinstance(status, dict) and status.get("ratification") == "CANON_SEALED":
        return "CANON_SEALED"
    return DEFAULT_CANON_STATUS
```

Promotion path (manual, F13-gated):
```
arif_judge → arif_seal → VAULT999 → sovereign signature → CANON_SEALED
```

NO auto-promotion. Even `CANON_SEALED` hint in registry is ignored for council layer.

---

## Layer D — Stage binding hard gate

```python
PERMITTED_STAGES = frozenset({"555_HEART", "999_RECEIPT"})


class QuoteStageError(Exception):
    """Raised when quote resolution is invoked at a forbidden stage."""


def wisdom_quote_resolve(
    context_tags, intended_use,
    stage: str = "555_HEART",
    enforce_stage_binding: bool = True,
    ...
):
    if enforce_stage_binding and stage not in PERMITTED_STAGES:
        raise QuoteStageError(
            f"Quote resolution forbidden at stage {stage!r}. "
            f"Permitted stages: {sorted(PERMITTED_STAGES)}. "
            f"Quotes are resources, not tools — only at 555_HEART or 999_RECEIPT."
        )
    ...
```

Forbidden stages:
- 000_INIT · 111_OBSERVE · 333_THINK · 444_ROUTE · 777_FORGE · 888_AUDIT

`enforce_stage_binding=False` for legacy soft-warn callers. New code defaults to True.

---

## Layer E — Test suite (19 tests, `tests/test_apex_quote_alignment.py`)

5 categories:

### E.1 — APEX multiplicative invariant
- `test_apex_fingerprint_returns_seven_organs` — all 7 organs present
- `test_apex_g_is_multiplicative_zero_organ_collapses` — zero organ = G=0
- `test_apex_g_well_behaved_quote_is_governed` — clean quote reaches GOVERNED
- `test_apex_disputed_lifts_c_dark` — DISPUTED raises C_dark above 0.20
- `test_apex_missing_prohibited_list_lifts_c_dark` — missing governance = hidden shadow
- `test_apex_fictional_voice_receipt_elevates_shadow` — FICTIONAL+RECEIPT = elevated C_dark

### E.2 — Stage binding (Layer D)
- `test_stage_binding_permits_555_heart`
- `test_stage_binding_permits_999_receipt`
- `test_stage_binding_rejects_333_think` (raises QuoteStageError)
- `test_stage_binding_rejects_777_forge`
- `test_stage_binding_rejects_111_observe`
- `test_stage_binding_soft_mode_legacy_compat` (enforce=False)

### E.3 — Canon status (Layer C)
- `test_canon_status_default_is_draft`
- `test_canon_status_council_forced_draft` — **proves sovereign ratification required**
- `test_canon_status_doctrine_constitutional_is_provisional`
- `test_canon_status_tiers_are_frozen`

### E.4 — Envelope integration
- `test_resolve_result_carries_apex_fingerprint`
- `test_resolve_result_to_dict_keys_complete`

### E.5 — Federation contract (Layer B)
- `test_federation_contract_resource_exposes_nine_uris` — all 9 namespace URIs live

---

## Honest gaps from this forge (reported in receipt)

| # | Gap | Severity | Owner |
|---|---|---|---|
| 1 | 17 council entries COUNCIL_* remain DRAFT | P0 (governance) | F13 SOVEREIGN |
| 2 | 15 doctrine entries (D1, D3, D5–D17) at PROPOSED, only D2+D4 CONSTITUTIONAL | P0 (governance) | F13 SOVEREIGN |
| 3 | VAULT999 auto-seal policy NOT wired | P1 (architecture) | F13 SOVEREIGN |
| 4 | Pre-existing intermittent anchor failures on 4 tools (state leak) | P1 (code) | parallel forge — needs F13 review |
| 5 | Pre-existing 2 test failures (data schema, text tolerance) | P3 (legacy) | code (out of scope) |

---

## Parallel forge that hit during this session

A separate agent (ASI 💃 audit, mentioned in parallel commit notes) was forging on the same branch. Their diffs:

- `arifOS/arifosmcp/runtime/philosophy_registry.py` — added APEX schema + per-tool anchor cache
- `arifOS/arifosmcp/data/philosophy_atlas.json` — restored (was missing per honest-gap #2)
- `arifOS/static/federation-manifest.json` — unknown diff

I committed only my 4 files and left theirs unstaged. Arif reviewed theirs separately.

Detection signals I used:
- `git status --short` showed files I didn't touch
- Diff contained `+` lines I didn't write (e.g., `build_federation_contract`)
- File syntax broken transiently (Python `IndentationError` after parallel patch)

---

## Receipt template — what an honest receipt looks like

```markdown
# Receipt — [Subsystem] Unification — YYYY-MM-DD

> Status: ✅ ALL [N] LAYERS LANDED. [N/N] tests passing. Live runtime verified.
> [N open sovereign decisions remain.]

## Commit
SHA: ...
Branch: ...
Files: ...

## Live verification
✅ mcp__arifos__read_resource arifos://[namespace]/[path]
   → [output proves ground truth, not assertion]

## Honest gaps (P0–P3, owner code | sovereign | env)
[enumerated, not omitted]

## What I did NOT do (your word required)
- ❌ [every irreversible thing I held]

## Sovereign decisions waiting
1. [decision] → [what ratification looks like]
2. ...
```

The receipt IS the artifact's C_dark audit. If the receipt hides gaps, the receipt itself is HIDDEN state.

---

## Recipe: applying this pattern to another artifact type

For claims (GEOX), doctrine (AAA), memory entries (L3/L4), evidence receipts (VAULT999):

1. **Map the 7 organs** to artifact-specific signals (table above as template).
2. **Compute G** as `math.prod(organs.values())` — multiplicative.
3. **Compute C_dark** from hidden-shadow drivers (disputed, fictional, missing governance).
4. **Define shadow_state** with GOVERNED/UNCHECKED/HIDDEN thresholds (start at 0.50 / 0.30).
5. **Attach to envelope** as `{apex_fingerprint, deploy_warrant}` field.
6. **Add 3 resource URIs** in federation namespace: fingerprint/{id}, canon-status/{id}, contract.
7. **Define canon_status tier ladder** with explicit forced-DRAFT for new layers.
8. **Add hard gate** at the boundary that produces/consumes the artifact.
9. **Write 19 tests** covering: multiplicative invariant, shadow drivers, gate enforcement, tier ladder, envelope integration, namespace exposure.
10. **Receipt** with honest gaps + sovereign-hold protocol.

Single commit. Single receipt. Single F13 handoff.
