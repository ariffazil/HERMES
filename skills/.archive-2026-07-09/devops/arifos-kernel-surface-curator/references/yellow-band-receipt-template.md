# YELLOW-Band Kernel Trim Receipt Template

When the live daemon probe fails (502, timeout, no MCP handshake) AND you have a trim task, the band is **YELLOW** by definition. Your work is design judgment, not a live SEAL. Use this template for `/root/arifOS/forge_work/YELLOW-KERNEL-TRIM-<N>.md`.

## Template

```markdown
# YELLOW-BAND KERNEL TRIM — <N> tools

**Date:** YYYY-MM-DD
**Band:** YELLOW (live probe failed — see T₁ evidence below)
**Verdict path:** design judgment, F13 ratification pending daemon restart
**Author:** <agent identity, e.g. Hermes/ASI-Δ>

## TL;DR

Trimmed the arifOS Kernel public surface from <OLD_N> → <NEW_N> canonical verbs.
Removed: <list of removed tools grouped by delete-law category>.
Promoted: <list of promoted tools from internal to public>.
Composes: VAULT999 owns receipt-seal; ARIF F13 owns final human veto.

## Live T₁ Probe

```
$ curl -sf http://localhost:8088/health
HTTP 502 / timeout / no handshake
```

**Band determination:** YELLOW. Patch is committed against source-of-truth;
daemon has NOT been restarted. Restart requires F13 SOVEREIGN ratification.

## Sources of Truth Patched

| File | What changed | Lines |
|---|---|---|
| `arifosmcp/constitutional_map.py` | `CORE_<OLD>` → `CORE_<NEW>`; 6 promote/demote; `_PUBLIC_<OLD>` → `_PUBLIC_<NEW>`; module docstring | <N> |
| `arifosmcp/runtime/public_surface.py` | `CANONICAL_<OLD>` → `CANONICAL_<NEW>`; deprecated aliases; mode profile_map | <N> |
| `arifosmcp/tool_registry.json` | `canonical_order` rewrite; `internal_canonical_order` | <N> |
| `arifosmcp/PUBLIC_SURFACE_CANON.md` | Full rewrite — N-tool table + remove list | <N> |
| `tests/test_public_surface_invariants.py` | All literal-7 → literal-N; new assertions | <N> |
| `tests/test_public_tool_registry.py` | Renamed + assertion swap | <N> |

## The New Canon

| Verb | Stage | Role |
|---|---|---|
| `arif_init` | 000 | Session anchor |
| `arif_canary` | 000c | Transport probe (6 modes) |
| ... | ... | ... |
| `arif_compose` | 444r | Response composer |

(Continue for all N.)

## The Remove List (grouped by delete-law category)

### Aliases → in adapter shim, not Kernel
- `arif_session_init` → `arif_init`
- `arif_gateway_connect` → `arif_route`
- ... etc.

### Fake-seal verbs → VAULT999 owns
- `arif_seal` → `arif_judge` returns `SEAL_CANDIDATE`; VAULT999 owns the receipt
- `arif_vault_seal` → VAULT999 owns

### Memory → archive/receipts
- `arif_memory` → VAULT999 / A_ARCHIVE
- `arif_memory_recall` → deprecated alias

### Duplicate conformance
- `arif_conformance_report` → `arif_canary(mode="conformance_report")`

### Domain-specific → organ
- GEOX-specific compute → GEOX
- WEALTH-specific compute → WEALTH
- WELL-specific assessment → WELL
- A-FORGE build steps → A-FORGE
- AAA display → AAA

## Test Result

```
$ python3 -B -m pytest tests/test_public_surface_invariants.py tests/test_public_tool_registry.py -v
```

<Y>/<X> PASSED.

(Failed tests are listed inline. Most common failure: `test_expanded45_includes_diagnostics` — env var `ARIFOS_MCP_EXPOSE_DEV_TOOLS` not set. Fix in `conftest.py` or relax assertion.)

## Live Surface Check (against source, not daemon)

```python
from arifosmcp.runtime.public_surface import public_tool_names_for_mode, CANONICAL_N
print(public_tool_names_for_mode())
# Expected: 12-tuple matching CANONICAL_<NEW>
```

## Daemon Restart Status

- [ ] **NOT restarted.** YELLOW band — F13 SOVEREIGN ratification required before `systemctl restart arifosmcp`.
- [ ] **Restarted** (GREEN band only).

## What the Sibling Skill Says

`geox-federation-mcp-driver` is the *consumer* of this canon. If you trim the surface, the GEOX driver's "arifOS Canonical Tool Catalog" table (in its SKILL.md) is now stale — flag for next patch cycle.

## Receipts

- This file: `/root/arifOS/forge_work/YELLOW-KERNEL-TRIM-<N>.md`
- Patch diff: `git diff arifOS/arifosmcp/constitutional_map.py arifOS/arifosmcp/runtime/public_surface.py arifOS/arifosmcp/tool_registry.json arifOS/arifosmcp/PUBLIC_SURFACE_CANON.md arifOS/tests/test_public_surface_invariants.py arifOS/tests/test_public_tool_registry.py`

## Bottom Line

The Kernel becomes powerful when it stops being impressive. <NEW_N> tools, one name per function, alias purges staged at the adapter (not the kernel). F13 SOVEREIGN ratification pending daemon restart.

DITEMPA BUKAN DIBERI.
```

## How to use this template

1. Replace all `<...>` placeholders.
2. Live T₁ Probe section is **non-optional**. If you didn't probe, you didn't do YELLOW-band correctly. Probe, paste the result, even if it's a fail.
3. Sources-of-truth table should list ALL files patched with line-count deltas (use `git diff --stat`).
4. Test result must be a literal copy-paste of `pytest -v` output. Don't summarize.
5. Daemon restart status must be explicit. YELLOW = NOT restarted.
6. Receipts section is the audit trail. Future agent reads THIS file to understand what changed and why.

## Worked Example

`/root/arifOS/forge_work/YELLOW-KERNEL-TRIM-12.md` — 2026-07-04 (7 → 12 trim). Test result: 17/17 PASSED on first cycle, 28/28 PASSED after RSI bus added (sweep includes `tests/test_rsi_event_bus.py`). Live daemon NOT restarted — F13 ratification pending.

## Anti-pattern: Don't SEAL YELLOW as GREEN

The YELLOW band is a deliberate signal that design judgment ≠ live verification. Do NOT write `BAND: GREEN` because the tests pass against source. Tests pass against source because the source was patched correctly — that's the *minimum*, not the *seal*. The seal is when the live daemon actually serves the new surface and a real MCP client gets the new canon.

If you write GREEN when the daemon is offline, you commit the cardinal sin of confusing source truth with transport truth. The Kernel's whole point is the wire surface — if no wire is talking, the kernel hasn't spoken.