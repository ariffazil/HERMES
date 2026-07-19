# Canonical Trim Checklist (Kernel Surface Curator)

Use this checklist when the target canon size changes (e.g. 7 → 12, 12 → 8, etc.). Every row is a place the change MUST propagate, or the wire surface will lie.

## The Four Load-Bearing Files

| # | File | What to patch | Failure mode if missed |
|---|---|---|---|
| 1 | `arifOS/arifosmcp/constitutional_map.py` | `CANONICAL_TOOLS[name]["expose"]` per tool; `_PUBLIC_N` frozenset; `CORE_N` ordered list; module docstring | Wire returns stale set; tests pass against wrong truth |
| 2 | `arifOS/arifosmcp/runtime/public_surface.py` | `CANONICAL_N` tuple; `normalize_public_surface_mode()` profile map; `VALID_PUBLIC_SURFACE_MODES` | `tools/list` call returns wrong set |
| 3 | `arifOS/arifosmcp/tool_registry.json` | `canonical_order` array; `internal_canonical_order` array | Machine manifest drift; downstream auto-gen (e.g. `arifOS/AGENTS.md`) reads stale |
| 4 | `arifOS/arifosmcp/PUBLIC_SURFACE_CANON.md` | Rewrite: tool table + rule-by-rule removal list | Humans reason from stale doc |

## The Two Test Files (must always be patched together)

| File | What to patch |
|---|---|
| `arifOS/tests/test_public_surface_invariants.py` | `EXPECTED_CANONICAL_N` set; `test_canonical_N_exact_count`; `test_canonical_N_contents`; `test_default_public_tools_exactly_N`; `test_canonical_N_ordered`; the `expected_order` literal list. Add new assertions for trim invariants (e.g. `arif_seal` not on surface). |
| `arifOS/tests/test_public_tool_registry.py` | Rename test; swap `arif_act`/`arif_forge` assertions if those flipped; assert all N canonical verbs are subset of `names`; assert the new removed tools (e.g. `arif_seal`, `arif_memory`) are absent. |

## The Derived Files (read but rarely edited directly)

| File | Reason |
|---|---|
| `arifOS/AGENTS.md` | Mentions 7-tool canon — update or leave (auto-generated `agents_md.py` re-derives). |
| `arifOS/arifosmcp/AGENTS.md` | Generated doc — update the generator's expected count, or hand-patch if the generator hasn't run. |
| `arifOS/forge_work/<BAND>-KERNEL-TRIM-N.md` | The trim receipt — write at end. |

## Per-Tool Patch Pattern (the meaty part)

For each tool in the **target canon**:
1. Confirm `_PUBLIC_N` membership (the force-reset set).
2. Confirm `CANONICAL_TOOLS[name]["expose"] is True`.
3. Confirm `runtime/public_surface.CANONICAL_N` includes it (in the right position).
4. Confirm `tool_registry.json` `canonical_order` includes it.
5. If `description` or `eureka_insight` are stale (e.g. tool flipped public↔internal), update both.

For each tool being **removed from public**:
- **Kept as internal handler?** Set `access: "internal_only"`, `expose: False`, update description/eureka_insight to reflect new role.
- **Deprecated alias?** Route through `_LEGACY_ALIASES`. Do NOT delete the handler.
- **Domain-specific move?** Code/compute goes to the organ. The Kernel just stops listing it.
- **Pure delete (e.g. `arif_explore` which never existed in CANONICAL_TOOLS)?** No kernel patch needed; just confirm it's not in `FORBIDDEN_PUBLIC` test set.

## The `_PUBLIC_N` Force-Reset Trap

This is the #1 cause of "I edited expose=True but it's still False on import":

```python
# At the bottom of constitutional_map.py, after CANONICAL_TOOLS block closes:
for _name, _spec in CANONICAL_TOOLS.items():
    if _name not in _PUBLIC_N:
        _spec["access"] = "internal_only"
        _spec["expose"] = False
```

**Always patch `_PUBLIC_N` when you patch per-tool `"expose"`.** Use the same name in both — they don't auto-sync.

## Verification Pattern

```python
import os
for v in ('ARIFOS_MCP_EXPOSE_DEV_TOOLS','ARIFOS_PUBLIC_SURFACE_MODE','ARIFOS_PUBLIC_TOOL_PROFILE'):
    os.environ.pop(v, None)
from arifosmcp.constitutional_map import CANONICAL_TOOLS, CORE_N
from arifosmcp.runtime.public_surface import public_tool_names_for_mode, CANONICAL_N

# 1. The per-tool flags
for name in sorted(['arif_triage','arif_bridge_connect','arif_compose','arif_critique','arif_fetch','arif_forge','arif_seal','arif_memory']):
    spec = CANONICAL_TOOLS.get(name, {})
    print(f'{name}: access={spec.get("access")!r} expose={spec.get("expose")!r}')

# 2. The wire surface
print('CANONICAL_N:', CANONICAL_N)
print('Default surface:', public_tool_names_for_mode())
assert len(public_tool_names_for_mode()) == N  # your target N
```

## Test Command

```bash
cd /root/arifOS && python3 -B -m pytest tests/test_public_surface_invariants.py tests/test_public_tool_registry.py -v
```

Expected: N+N tests PASSED. If any FAIL, the most common cause is the `expanded45` gate (env var not set) — see pitfall 5 in SKILL.md.

## Receipt Template Location

`/root/arifOS/forge_work/<BAND>-KERNEL-TRIM-<N>.md`

Replace `<BAND>` with `GREEN`, `YELLOW`, or `RED`. Replace `<N>` with the new canon size.

## 2026-07-04 Worked Example (7 → 12 trim)

Total files touched: **6**

| File | Edits |
|---|---|
| `arifosmcp/constitutional_map.py` | 1. Module docstring header (mentions 7 → 12). 2. `CORE_SEVEN` → `CORE_TWELVE` ordered list + 3 mirror dicts. 3. 6 per-tool `expose` flips (False → True: fetch, critique, triage, bridge_connect, compose; True → False: seal). 4. `arif_act`/`arif_forge` description swap + flip. 5. `_PUBLIC_7` → `_PUBLIC_12`. 6. Module MACHINERY docstring. |
| `arifosmcp/runtime/public_surface.py` | 1. `CANONICAL_7` → `CANONICAL_12` (with `CANONICAL_7`/`CANONICAL_13` as deprecated aliases). 2. `VALID_PUBLIC_SURFACE_MODES` adds `"canonical12"`. 3. `DEPRECATED_CANARY_CHILDREN` tuple added. 4. `normalize_public_surface_mode()` profile_map. 5. `public_surface_state()` mode_aliases dict + len() calls. |
| `arifosmcp/tool_registry.json` | 1. `canonical_order` rewritten (12). 2. `internal_canonical_order` rewritten (6). |
| `arifosmcp/PUBLIC_SURFACE_CANON.md` | Full rewrite (12-tool table + rule-by-rule removal list). |
| `tests/test_public_surface_invariants.py` | 1. `EXPECTED_CANONICAL_12` set + `EXPECTED_CANONICAL_7` deprecated alias. 2. `FORBIDDEN_PUBLIC` rewritten with 18 entries grouped by delete-law category. 3. 14 tests renamed/updated, 4 new tests added (legacy aliases, seal-off, memory-off, forge-on, act-off). |
| `tests/test_public_tool_registry.py` | Renamed `test_public_registry_exposes_only_canonical_12`. Asserts all 12 canonical verbs in `names`, plus absence of seal/memory/act. |

**Time to verify:** 1 round-trip via `pytest` (failed once on `expanded45` env-var gate — fixed in v2).