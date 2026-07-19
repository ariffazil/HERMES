#!/usr/bin/env python3
"""
canon_audit.py — Cross-check the arifOS Kernel public surface across all
4 sources of truth. Emits a drift report.

Usage:
    cd /root/arifOS && python3 arifosmcp/_tools/canon_audit.py

Or:
    cd /root/arifOS && python3 -m scripts.canon_audit

This is a starter template. Modify the EXPECTED_N constant at the top to
match your target canon size.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


# ── Configuration ───────────────────────────────────────────────────────────
ARIFOS_ROOT = Path("/root/arifOS")  # adjust if your checkout is elsewhere
CONSTITUTIONAL_MAP = ARIFOS_ROOT / "arifosmcp" / "constitutional_map.py"
PUBLIC_SURFACE = ARIFOS_ROOT / "arifosmcp" / "runtime" / "public_surface.py"
TOOL_REGISTRY = ARIFOS_ROOT / "arifosmcp" / "tool_registry.json"
PUBLIC_SURFACE_CANON_MD = ARIFOS_ROOT / "arifosmcp" / "PUBLIC_SURFACE_CANON.md"

# Expected canon size — change this when you change the canon
EXPECTED_N = 12


def _strip_env_overrides() -> None:
    """Reset surface-mode env vars so we test the source-of-truth."""
    for v in (
        "ARIFOS_MCP_EXPOSE_DEV_TOOLS",
        "ARIFOS_PUBLIC_SURFACE_MODE",
        "ARIFOS_PUBLIC_TOOL_PROFILE",
    ):
        os.environ.pop(v, None)


def load_canonical_n() -> tuple[str, ...]:
    """Load CANONICAL_N from runtime/public_surface.py."""
    _strip_env_overrides()
    sys.path.insert(0, str(ARIFOS_ROOT))
    try:
        from arifosmcp.runtime.public_surface import CANONICAL_12  # type: ignore
        return tuple(CANONICAL_12)  # type: ignore
    except ImportError:
        from arifosmcp.runtime.public_surface import CANONICAL_7  # type: ignore
        return tuple(CANONICAL_7)  # type: ignore


def load_constitutional_tools() -> dict:
    """Load CANONICAL_TOOLS dict (post force-reset) from constitutional_map.py."""
    sys.path.insert(0, str(ARIFOS_ROOT))
    from arifosmcp.constitutional_map import CANONICAL_TOOLS  # type: ignore
    return dict(CANONICAL_TOOLS)


def load_tool_registry_canon() -> list[str]:
    """Load canonical_order from tool_registry.json."""
    with open(TOOL_REGISTRY) as f:
        data = json.load(f)
    return list(data.get("canonical_order", []))


def load_public_surface_canon_doc() -> set[str]:
    """Best-effort: parse the doc and find tool names."""
    if not PUBLIC_SURFACE_CANON_MD.exists():
        return set()
    text = PUBLIC_SURFACE_CANON_MD.read_text()
    # Crude: find lines starting with `arif_*` in backticks (the table)
    import re
    names = set()
    for line in text.splitlines():
        m = re.search(r"`(arif_[a-z_]+)`", line)
        if m:
            names.add(m.group(1))
    return names


def main() -> int:
    print(f"═══ arifOS Kernel Canon Audit ═══")
    print(f"Expected N: {EXPECTED_N}")
    print(f"Source root: {ARIFOS_ROOT}")
    print()

    canon_n = load_canonical_n()
    print(f"1. CANONICAL_N tuple (from runtime/public_surface.py): {len(canon_n)}")
    print(f"   {canon_n}")
    print()

    canonical_tools = load_constitutional_tools()
    print(f"2. CANONICAL_TOOLS dict (from constitutional_map.py): {len(canonical_tools)}")
    public_tools = sorted(
        [n for n, s in canonical_tools.items() if s.get("expose") is True]
    )
    print(f"   Public (expose=True): {len(public_tools)}")
    print(f"   {public_tools}")
    print()

    registry_canon = load_tool_registry_canon()
    print(f"3. canonical_order (from tool_registry.json): {len(registry_canon)}")
    print(f"   {registry_canon}")
    print()

    doc_canon = load_public_surface_canon_doc()
    print(f"4. PUBLIC_SURFACE_CANON.md (best-effort parse): {len(doc_canon)}")
    print(f"   {sorted(doc_canon)}")
    print()

    # ── Drift detection ─────────────────────────────────────────────────
    print("═══ Drift Report ═══")
    drift_count = 0

    # 1 vs 3
    s1, s3 = set(canon_n), set(registry_canon)
    if s1 != s3:
        drift_count += 1
        print(f"❌ DRIFT: CANONICAL_N vs tool_registry.json")
        print(f"   Only in CANONICAL_N: {s1 - s3}")
        print(f"   Only in manifest: {s3 - s1}")
    else:
        print(f"✅ CANONICAL_N == tool_registry.json canonical_order")

    # 1 vs 2 (public_tools from CANONICAL_TOOLS expose flag)
    s2 = set(public_tools)
    # Note: arif_canary lives in DIAGNOSTIC_TOOLS, so it won't appear here
    s1_in_2 = s1 & s2
    s1_not_in_2 = s1 - s2
    if s1_not_in_2:
        # Could be just arif_canary — filter
        arif_canary_only = s1_not_in_2 == {"arif_canary"}
        if not arif_canary_only:
            drift_count += 1
            print(f"❌ DRIFT: CANONICAL_N tools not marked expose=True in CANONICAL_TOOLS:")
            print(f"   {s1_not_in_2}")
        else:
            print(f"⚠️  arif_canary not in CANONICAL_TOOLS (lives in DIAGNOSTIC_TOOLS — by design)")
    else:
        print(f"✅ All CANONICAL_N tools have expose=True (modulo arif_canary)")

    # Length vs EXPECTED_N
    if len(canon_n) != EXPECTED_N:
        drift_count += 1
        print(f"❌ CANONICAL_N has {len(canon_n)} tools; expected {EXPECTED_N}")
    else:
        print(f"✅ CANONICAL_N has {len(canon_n)} tools (matches EXPECTED_N={EXPECTED_N})")

    # Doc vs 1
    if doc_canon:
        missing_in_doc = s1 - doc_canon
        if missing_in_doc:
            drift_count += 1
            print(f"❌ DRIFT: PUBLIC_SURFACE_CANON.md missing:")
            print(f"   {missing_in_doc}")
        else:
            print(f"✅ PUBLIC_SURFACE_CANON.md mentions all CANONICAL_N tools")

    print()
    if drift_count == 0:
        print(f"═══ NO DRIFT ═══")
        return 0
    else:
        print(f"═══ {drift_count} DRIFT(S) DETECTED ═══")
        return 1


if __name__ == "__main__":
    sys.exit(main())