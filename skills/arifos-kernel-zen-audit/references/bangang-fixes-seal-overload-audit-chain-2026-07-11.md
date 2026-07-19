# Bangang Fixes — 4 Kernel Issues (2026-07-11)

External audit found 4 issues in `runtime/tools.py` envelope builder. All fixes applied.

## BANGANG #1 — SEAL Overload (HIGH)

**Symptom:** sesat_event drift detector fires YELLOW on every correct OBSERVE_ONLY response.
- `failed_claim: "OBSERVE_ONLY — tool returned a non-SEAL status"`
- `observed_reality: "verdict=OBSERVE_ONLY, status=SEAL"`

**Root cause:** Transport `status="SEAL"` (MCP call succeeded) collides with constitutional `verdict="SEAL"` (approved/sealed). The sesat classifier was keying off status instead of verdict.

**Fix locations:**
1. `runtime/tools.py` line ~3458: Normalize `status="SEAL"` → `"OK"` immediately after reading transport status. Insert after `status = str(out.get("status") or "OK")`.
2. `runtime/tools.py` line ~3592: Sesat event now exempts `OBSERVE_ONLY` — it's a valid operational mode, not a failure.
3. `transport/conformance_spine.py`: Accepts "SEAL" for backward compat but canonical transport status is "OK".

**Pattern:** When a field name is overloaded for two meanings (transport success vs constitutional verdict), normalize at the ingestion point. Don't try to fix downstream classifiers.

```python
# At the ingestion point, right after reading status:
if status in ("SEAL", "seal"):
    status = "OK"
```

## BANGANG #2 — Audit Chain Holes (MEDIUM)

**Symptom:** `arif_init` returns populated `call_hash`, `invocation_count`, `called_from_kernel`. `arif_think` and other verbs return null for these fields.

**Root cause:** Audit spine fields were only computed in `session.py _project_light()` (arif_init path). The envelope wrapper in `tools.py` had fallback logic to extract from `out` or `out["result"]`, but if neither had them, they stayed None.

**Fix locations:**
- `runtime/tools.py` lines ~3667-3714: Three-stage fallback chain:
  1. Try `out.get(field)` or `out["result"].get(field)`
  2. If still None, compute: `_compute_call_hash(tool, payload, timestamp, session_id, salt)` for call_hash, `f"trc-{uuid.uuid4().hex[:12]}"` for trace_id
  3. Final fallback: `called_from_kernel=True`, `invocation_count=0`

**Pattern:** When a field is mandatory for F11 audit spine, the envelope wrapper must generate it if the tool didn't. Don't rely on each tool independently implementing audit fields.

## BANGANG #3 — Confidence Theater (MEDIUM)

**Symptom:** `arif_think/reason` emits `confidence_trajectory=[0.5, 0.72, 0.85]` with named axioms (L02_TRUTH, L08_GENIUS) even when "P1 degraded mode — LLM synthesis bypassed" is active.

**Root cause:** Hardcoded ReasoningStep template runs regardless of whether LLM synthesis actually occurred. The numbers look real when the reasoning behind them didn't run.

**Fix locations:**
- `runtime/tools.py` lines ~10984-10995: Detect degraded mode, then:
  1. Flatten trajectory to single point `[llm_confidence]` — no fake progression
  2. Override coherence to 0.35, depth to "shallow"
  3. Mark all steps with `axiom_used="P1_TEMPLATE_DEGRADED"`
  4. Add `confidence_provenance: "COMPUTED_NOT_OBSERVED"` to result dict

**Pattern:** When a code path bypasses LLM reasoning (template/degraded mode), ALL derived metrics must be downgraded. Confidence trajectory should be flat (single point), not ascending. Add a provenance field so downstream consumers know the numbers are synthetic.

```python
_confidence_provenance = "OBSERVED"
if _is_degraded:
    trace.confidence_trajectory = [llm_confidence]  # flat, not [0.5, 0.72, 0.85]
    trace.coherence_score = 0.35
    _confidence_provenance = "COMPUTED_NOT_OBSERVED"
# Add to result dict:
"confidence_provenance": _confidence_provenance,
```

## BANGANG #4 — Actor Identity Disagreement (LOW)

**Symptom:** `arif_think` meta says `actor_id: "ARIF"`, top-level `actor: null`, banner says `IDENTITY_NOT_VERIFIED`. Three fields, three different answers.

**Root cause:** Envelope `actor` field reads from `out.get("actor")` which is None when the tool doesn't return an actor dict. Meanwhile `actor_id` is correctly resolved from session store.

**Fix location:**
- `runtime/tools.py` line ~3807: If tool didn't return actor dict, synthesize from `resolved_actor_id`:
```python
"actor": (
    out.get("actor")
    if isinstance(out.get("actor"), dict)
    else {"actor_id": resolved_actor_id, "source": "envelope_derived"}
    if resolved_actor_id
    else None
),
```

**Pattern:** When a tool doesn't return a structured field that the envelope requires, the envelope wrapper must derive it from the single source of truth (session store / resolved_actor_id). Never leave the field null when the information is available elsewhere in the envelope.

## Files Modified
- `arifosmcp/runtime/tools.py` — all 4 fixes
- `arifosmcp/transport/conformance_spine.py` — backward-compat note for #1

## Forbidden Files (not touched)
- `runtime/sovereign_verify.py`
- `runtime/governance_identity.py`
