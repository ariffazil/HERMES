# Quote Registry Audit Timeline (2026-07-19)

Concrete reproduction recipe for the **mid-audit commit inversion** pattern. The audit was the second iteration of a parallel-forge sequence; the third commit landed while the audit was in flight and inverted the verdict from PARTIAL to YES.

## The three-commit sequence

| # | Time (UTC) | Commit | Author | What it did |
|---|---|---|---|---|
| 1 | 08:58Z | `143afc741` | Arif | Layer A/B/C/D APEX alignment in `quote_registry.py`: `compute_apex_fingerprint`, `compute_canon_status`, `QuoteStageError`, `ResolveResult` carries `apex_fingerprint/canon_status/deploy_warrant/wisdom_contract` |
| 2 | 09:00Z | `6b1e84b37` | ASI 💃 (parallel forge) | Wire `inject_philosophy` through Layer A+B+C+D: `APEX_ORGANS` schema in `philosophy_registry.py`, per-tool anchor cache, `philosophy_atlas.json` restored (359 lines) |
| 3 | 09:22Z | `b953eef8f` | FORGE-000Ω (mid-audit fix) | **Path Y dedup**: `quote_constants.py` (62 LOC) becomes single source of truth for `APEX_ORGANS`/`PERMITTED_STAGES`/`FORBIDDEN_STAGES`/`G_DEPLOY_THRESHOLD`/`C_DARK_CEILING`; both consumers re-import; `wisdom_quotes.py` (1285 LOC) deleted; `quote_registry.compute_apex_fingerprint` extended to accept `verdict_context` for adapter compat |

The audit started between #2 and #3. The verdict at audit start was **PARTIAL** (dual APEX_ORGANS, dual fingerprint, dead wisdom_quotes.py). The verdict at audit finalization was **YES** (single source of truth, all tests pass).

## What the receipt must look like to survive this

Header at T₁ (the moment of writing):
```
# Unified SOT Audit — 2026-07-19 (T₁: post b953eef8f, Path Y dedup)

> Status at T₁: ✅ YES — single SOT path, one canonical resolver.
> T₀ note (was PARTIAL): Commit b953eef8f landed during the audit and
> inverted the verdict. Re-probed under new HEAD; receipt rewritten.
> HEAD at T₁: b953eef8f
```

The receipt must NOT pretend the T₀ state never existed. Future agents reading the receipt want to know what changed and why the conclusion flipped. Burying the inversion makes the receipt look authoritative when it was actually a moving target.

## Live re-probe commands (T₁ re-verification)

```bash
# 1. Identity check — APEX_ORGANS is the same object across all 3 import sites
python -c "
from arifosmcp.runtime.quote_constants import APEX_ORGANS, PERMITTED_STAGES
from arifosmcp.runtime.quote_registry import APEX_ORGANS as QR, PERMITTED_STAGES as QRS
from arifosmcp.runtime.philosophy_registry import APEX_ORGANS as PR, PERMITTED_STAGES as PRS
print('APEX identity:', APEX_ORGANS is QR is PR)
print('PERMITTED identity:', PERMITTED_STAGES is QRS is PRS)
print('type tuple:', type(APEX_ORGANS).__name__)
"

# 2. Single canonical resolver probe
python -c "
from arifosmcp.runtime import quote_registry, philosophy_registry
raw = next(q for q in quote_registry.load_registry()['quotes'] if q['id']=='INIT_Q_001')
print('quote_registry', quote_registry.compute_apex_fingerprint(raw)['G'])
print('philosophy_registry', philosophy_registry.compute_apex_fingerprint(raw)['G'])
# Must produce identical G. If they diverge, the dedup is incomplete.
"

# 3. End-to-end MCP wire check
python -c "
import asyncio
from arifosmcp.runtime.tools import _CANONICAL_HANDLERS, _enforce_nine_signal
async def main():
    for tool in ['arif_init','arif_memory','arif_seal']:
        h = _CANONICAL_HANDLERS[tool]
        raw = await h(mode='light', actor_id='sot-audit', session_id=None) if hasattr(h, '__wrapped__') else None
        if raw is None:
            raw = h(mode='light', actor_id='sot-audit')  # sync path
        final = _enforce_nine_signal(tool, raw if isinstance(raw, dict) else {'status':'OK','tool':tool,'result':{}}, session_id=None, actor_id='sot-audit')
        a = final.get('philosophical_anchor')
        print(tool, 'has_anchor=', bool(a), 'quote_id=', a.get('quote_id') if a else None)
asyncio.run(main())
"

# 4. Dedup test
python -m pytest -q tests/test_quote_constants_unity.py
# Must show 15 passed. The test enforces object identity — if Path Y is
# incomplete, this fails with a clear "constants disagree" assertion.
```

## What the audit was right about (T₀) and wrong about (T₁)

### T₀ (correct at the time)
- Two `APEX_ORGANS` declarations existed (tuple in `quote_registry.py:165`, list in `philosophy_registry.py:48`).
- Two `compute_apex_fingerprint` impls with different signatures.
- `wisdom_quotes.py` (1285 LOC) still alive with `CIVILIZATIONAL_CANON` hardcoded dict.
- `quote_ledger.py` still imported by `context_safety.py`, `context_witness.py`, `quote_retriever.py`, and 3 tests.
- `philosophy_atlas.json` restored by `6b1e84b37` (359 lines, 27 zones).
- `philosophy.py:25` `ATLAS_PATH = parents[2] / "data" / "philosophy_atlas.json"` resolves to `/root/arifOS/data/philosophy_atlas.json` — **wrong directory**, file lives at `/root/arifOS/arifosmcp/data/philosophy_atlas.json`. Live warning: "Philosophy atlas not found".

### T₁ (after `b953eef8f`)
- `APEX_ORGANS` is one tuple, identity-preserved across all 3 import sites.
- `compute_apex_fingerprint` lives in `quote_registry.py:592`. `philosophy_registry.compute_apex_fingerprint` is a 12-line adapter that maps `verdict_context → intended_use` and delegates. `quote_constants.compute_apex_fingerprint` is a re-export wrapper.
- `wisdom_quotes.py` deleted (-1285 LOC).
- `quote_ledger.py` still alive and still imported (the b953eef8f commit removed `wisdom_quotes.py` but NOT `quote_ledger.py`; the ledger still has 3 importers, all frozen because `.archive-pre-zen-2026-07-12/wisdom_quotes_lite.json` was purged by `9322af4ec`).
- `philosophy.py:25` ATLAS_PATH **still broken** (commit b953eef8f did not fix this — `philosophy.py` was untouched by the dedup, only `philosophy_registry.py` and `quote_registry.py` were edited).
- `tests/test_quote_constants_unity.py` (15 tests) added by b953eef8f; passes 15/15.
- 6 tests still fail because they depend on the deleted `quote_ledger.py` archive. The commit fixed the dedup but didn't migrate the test files.

## Live dead-code backlog at T₁ (still real, did NOT get fixed by b953eef8f)

| File / symbol | LOC | Status | Why still dead |
|---|---|---|---|
| `arifosmcp/runtime/quote_ledger.py` | 292 | Imported by 3 runtime files, all fail at runtime because archive deleted | `load_quote_ledger()` raises `QuoteSchemaError("Ledger file not found: ...wisdom_quotes_lite.json")`. 6 tests fail. |
| `arifosmcp/runtime/tools.py:_WISDOM_QUOTES` (line 6359) | 165 | Unwired | `_wisdom_for_tool` (line 6527) has 0 callers in `arifosmcp/` |
| `arifosmcp/runtime/philosophy.py:ATLAS_PATH` (line 25) | 1 line | Wrong `parents[N]` | `parents[2]` → `/root/arifOS/data/`; correct is `parents[1]` → `/root/arifOS/arifosmcp/data/`. Fix is 1 line. |
| `arifosmcp/runtime/philosophy.py:PHILOSOPHY_REGISTRY` (line 329) | ~50 | Module-private | 0 external references |

b953eef8f closed the schema-dedup gap but left the runtime-bug backlog intact. The atlas path bug means `select_atlas_philosophy` (called by `enforcer.py:413`, `kernel_core.py:522`, `megaTools/tool_01_init_anchor.py:505`) returns empty zones with a "Philosophy atlas not found" warning logged every call. Live fallback quote is a hardcoded string.

## Pattern summary for future audits

When you audit a parallel-forge repo and find "duplicate" definitions:

1. **Snapshot HEAD before you start probing.** Write the hash into your notes.
2. **Read the docstrings** to detect declared legacy boundaries.
3. **Run your live probes** to confirm what the runtime actually does TODAY (against the HEAD you snapshotted).
4. **Before you finalize the receipt**: re-run `git log --oneline <snapshot>..HEAD`. If new commits touched the audited files, re-probe and rewrite the verdict.
5. **Cite the HEAD at finalization time**, not the HEAD at audit start. Receipt headers must be honest about which state they describe.

The receipt you write at T₁ is the source of truth for T₁. If the next session runs the same audit at T₂, the new receipt is the new source of truth. Don't try to make one receipt span multiple states.
