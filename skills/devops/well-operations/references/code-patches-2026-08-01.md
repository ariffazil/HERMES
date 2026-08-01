# well_machine_diagnose Code Patches — 2026-08-01

These two code bugs were discovered when AGI repeatedly called `well_machine_diagnose` and got tool errors. Both fixes are in `/root/WELL/server.py`.

## Patch 1: Missing `os` import

**Error:** `name 'os' is not defined`
**Root cause:** `well_machine_diagnose()` at L10448 imports `json` and `pathlib` but calls `os.cpu_count()` at L10502 without importing `os`.

**Fix (server.py):**
```
# BEFORE (L10460-10461):
    import json as _json_md
    from pathlib import Path as _PathMd

# AFTER:
    import json as _json_md
    import os as _os_md
    from pathlib import Path as _PathMd
```

**AND fix the call (L10502):**
```
# BEFORE:
    cpu_count = os.cpu_count() or 4

# AFTER:
    cpu_count = _os_md.cpu_count() or 4
```

## Patch 2: Missing `mode` parameter in `_omega_well_output` calls

**Error:** `_omega_well_output() missing 1 required positional argument: 'mode'`
**Root cause:** `_omega_well_output()` signature has `mode: str` as a required parameter (no default), but all three calls inside `well_machine_diagnose` omit it.

**Fix — Add `mode="M_DIAGNOSE"` after each `lane="AGI"` in all three calls:**

**Call 1 (L10469):**
```
# BEFORE:
            ok=False,
            stage="M_DIAGNOSE",
            lane="AGI",
            verdict="HOLD",
            error="machine_state.json not found ...

# AFTER:
            ok=False,
            stage="M_DIAGNOSE",
            lane="AGI",
            mode="M_DIAGNOSE",
            verdict="HOLD",
            error="machine_state.json not found ...
```

**Call 2 (L10481):**
```
# BEFORE:
            ok=False,
            stage="M_DIAGNOSE",
            lane="AGI",
            verdict="HOLD",
            error=f"machine_state.json corrupt: {exc}",

# AFTER:
            ok=False,
            stage="M_DIAGNOSE",
            lane="AGI",
            mode="M_DIAGNOSE",
            verdict="HOLD",
            error=f"machine_state.json corrupt: {exc}",
```

**Call 3 (L10681):**
```
# BEFORE:
        ok=(severity != "RED"),
        stage="M_DIAGNOSE",
        lane="AGI",
        verdict=verdict,

# AFTER:
        ok=(severity != "RED"),
        stage="M_DIAGNOSE",
        lane="AGI",
        mode="M_DIAGNOSE",
        verdict=verdict,
```

**After applying both patches:** `systemctl restart well`
