# Three Sources of Truth — Why Triple Coverage is Load-Bearing

The arifOS MCP public wire surface has **three declared sources** where its canon is set, plus a **fourth that is always-live and overrides the three**: the running daemon's `tools/list` response.

When sources conflict, the precedence is:
1. **Live wire** — `POST :8088/mcp tools/list` response (always-live, from the running daemon)
2. **VAULT999 sealed records**
3. **Code in main branch** — the three declared sources below
4. **README / docs** — lowest. Docs describe; they do not define.

(Added 2026-07-08 federation sweep: doc/code/live drift is a routine class of bug; the live wire is the only authority that matters for "what is actually exposed right now.")

## The Triple (declared sources)

| Source | Type | Owns |
|---|---|---|
| `constitutional_map.CANONICAL_TOOLS` + `_PUBLIC_N` | Per-tool registry + force-reset set | What is *registered* and what is *forced public* |
| `runtime/public_surface.CANONICAL_N` | Ordered tuple | What `tools/list` *returns* |
| `tool_registry.json` `canonical_order` | JSON manifest | What the *machine-readable manifest* declares |

Plus a fourth: `runtime/public_surface.public_tool_names_for_mode()` is the function that **filters** the wire surface, and it reads `CANONICAL_N` plus checks `CANONICAL_TOOLS[name]["access"] != "internal_only"`.

## The Force-Reset Mechanism (why 3 places matter)

```python
# constitutional_map.py — runs at module import:
for _name, _spec in CANONICAL_TOOLS.items():
    if _name not in _PUBLIC_N:
        _spec["access"] = "internal_only"
        _spec["expose"] = False
```

**Effect:** If a tool name is NOT in `_PUBLIC_N`, its `expose` and `access` flags are forced to `False` / `"internal_only"` *regardless of what was written inside the dict block*. This means:

- Editing `CANONICAL_TOOLS["arif_canary"]["expose"] = True` while NOT adding `"arif_canary"` to `_PUBLIC_N` → silently reverts at import.
- Removing `"arif_seal"` from `_PUBLIC_N` → kernel auto-hides `arif_seal`, even if the dict block still says `"expose": True`.

**The patch rule:** Every tool on the public surface must be in BOTH:
1. `_PUBLIC_N` (the membership check), AND
2. `CANONICAL_N` (the wire list), AND
3. `tool_registry.json` `canonical_order` (the manifest)

## The `arif_canary` exception

`arif_canary` and its 6 deprecated children live in `DIAGNOSTIC_TOOLS`, not `CANONICAL_TOOLS`. The wire-surface filter:

```python
def public_tool_names_for_mode(mode: str | None = None) -> tuple[str, ...]:
    resolved = normalize_public_surface_mode(mode)
    if resolved == "expanded45":
        ...
        candidates = EXPANDED_45 if expose_dev_tools else CANONICAL_N
    else:
        candidates = CANONICAL_N
    return tuple(
        name
        for name in candidates
        if CANONICAL_TOOLS.get(name, {}).get("access") != "internal_only"
    )
```

For `arif_canary` (not in `CANONICAL_TOOLS`), `CANONICAL_TOOLS.get("arif_canary", {})` returns `{}`, so `.get("access")` returns `None`, which is `!= "internal_only"`. **Vacuously passes the filter.**

If `arif_canary` were listed in `CANONICAL_N` AND in `_PUBLIC_N`, it would be on the public surface despite never appearing in `CANONICAL_TOOLS`. This is by design — multimode dispatcher pattern.

## Why the legacy aliases work

`CANONICAL_7` and `CANONICAL_13` are kept as Python-level aliases of `CANONICAL_12`:

```python
CANONICAL_12: tuple[str, ...] = (...)  # the new 12
CANONICAL_7: tuple[str, ...] = CANONICAL_12  # DEPRECATED alias
CANONICAL_13: tuple[str, ...] = CANONICAL_12  # DEPRECATED alias
```

When an old test imports `CANONICAL_7`, Python resolves it to `CANONICAL_12` (same tuple object). The test passes its `len() == 7` assertion only if you also patch the test's literal `7` to `12` — but if you forget, you get a `7 != 12` failure that names the right place to patch.

**The alias preserves backward compatibility for any external code that imports the old name.** New code should import `CANONICAL_12` directly. Tests should pin `EXPECTED_CANONICAL_12`.

## The 6 deprecated canary children

These names exist in `DIAGNOSTIC_TOOLS` with `_deprecated: True` and `_canonical_name: "arif_canary"`:

| Name | Replacement |
|---|---|
| `arif_ping` | `arif_canary(mode="ping")` |
| `arif_schema_echo` | `arif_canary(mode="schema_echo")` |
| `arif_version_echo` | `arif_canary(mode="version_echo")` |
| `arif_transport_echo` | `arif_canary(mode="transport_echo")` |
| `arif_initialize_probe` | `arif_canary(mode="initialize_probe")` |
| `arif_conformance_report` | `arif_canary(mode="conformance_report")` |

These exist as **handler aliases** for backward compatibility. They should NOT appear on the public wire. The `FORBIDDEN_PUBLIC` test set locks them out.

## The `_LEGACY_ALIASES` table

If `arif_session_init`, `arif_gateway_connect`, etc. need to still *work* (resolve to handlers) while NOT being on the public wire, they belong in `_LEGACY_ALIASES` (in the FastMCP handlers module, not the constitutional map). This is the right pattern for SDK-long-name aliases:

- Public wire: `arif_init` (canonical)
- Internal handler table: `arif_session_init` → handler resolution → `arif_init` logic
- `FORBIDDEN_PUBLIC` test: ensures `arif_session_init` not in `tools/list`

Compatibility lives outside the Kernel. The Kernel is canonical.

## How to detect drift (the cross-check)

```python
import json
from arifosmcp.constitutional_map import CANONICAL_TOOLS, _PUBLIC_N
from arifosmcp.runtime.public_surface import CANONICAL_N

with open('arifosmcp/tool_registry.json') as f:
    reg = json.load(f)
manifest_canon = set(reg['canonical_order'])

# 1. CANONICAL_N vs manifest
drift_1 = set(CANONICAL_N) ^ manifest_canon
if drift_1:
    print(f"DRIFT: CANONICAL_N vs manifest: {drift_1}")

# 2. _PUBLIC_N vs CANONICAL_N
drift_2 = _PUBLIC_N ^ set(CANONICAL_N)
if drift_2:
    print(f"DRIFT: _PUBLIC_N vs CANONICAL_N: {drift_2}")

# 3. CANONICAL_TOOLS expose flags vs _PUBLIC_N
for name, spec in CANONICAL_TOOLS.items():
    in_public = name in _PUBLIC_N
    expose = spec.get('expose') is True
    if in_public != expose:
        print(f"DRIFT: {name}: in_public={in_public} expose={expose}")
```

If any of these fires, your trim is incomplete. Run this script after every patch as a sanity check before running `pytest`.

## How to detect doc-vs-wire drift (added 2026-07-08)

The cross-check above compares declared sources. To add the live wire as a 4th source:

```python
import json, urllib.request

def live_wire_tools(port=8088):
    body = {"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
    req = urllib.request.Request(f"http://localhost:{port}/mcp",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json",
                 "Accept":"application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
    return sorted([t["name"] for t in d["result"]["tools"]])

# 1. Probe live
live = live_wire_tools(8088)

# 2. Import declared
from arifosmcp.runtime.public_surface import CANONICAL_N
declared = sorted(CANONICAL_N)

# 3. Diff
if live != declared:
    print(f"DRIFT: live={len(live)} vs declared={len(declared)}")
    print(f"  in live but not declared: {set(live) - set(declared)}")
    print(f"  in declared but not live: {set(declared) - set(live)}")
    # If you trust live (after recent restart), patch code to match.
    # If you trust code (live is stale), restart daemon then re-probe.
```

**Decision tree when live ≠ declared:**
- Live has extra tools → daemon loaded a different snapshot; investigate
- Code has extra tools → recent code change not yet deployed; or daemon restarted to old version
- Both agree but README disagrees → doc drift; patch README
- Kernel self-reports `runtime_drift: true` in `/health` → build≠live commit; rebuild image

## Why the 3-place redundancy is constitutional, not bug

The Kernel's public surface is **the contract between the federation and every agent that calls it**. If that contract is ambiguous (3 different lists, 3 different truths), agents will route to the wrong tool. Triple coverage is intentional:

1. `constitutional_map.CANONICAL_TOOLS` = the **registry** (rich metadata per tool)
2. `_PUBLIC_N` = the **membership test** (force-reset)
3. `CANONICAL_N` = the **wire list** (ordered, what `tools/list` returns)
4. `tool_registry.json` = the **manifest** (machine-readable, for external consumers)

They serve different consumers. Patching one and forgetting the others breaks the consumer. Always patch all 3 (or 4 with the JSON).