#!/usr/bin/env python3
"""Template: Governed Memory Store with Gödel Lock.
Copy and modify for your use case. Stdlib-only (Python 3.12+).

Usage:
  python governed_memory.py add --content "..." --truth-class OBS --authority advisory --source "session:abc"
  python governed_memory.py list [--truth-class OBS]
  python governed_memory.py render
  python governed_memory.py validate
  python governed_memory.py decay
  python governed_memory.py promote <id> --reason "..."
  python governed_memory.py forget <id> --reason "..."
"""

import argparse
import json
import os
import sys
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

# ── Paths (customize) ────────────────────────────────────────────────
STORE_DIR = Path.home() / ".hermes" / "memories"
STORE_PATH = STORE_DIR / "governed.json"
RENDERED_PATH = STORE_DIR / "RENDERED.md"

# ── Truth Classes ────────────────────────────────────────────────────
TRUTH_CLASSES = {
    "OBS": {"label": "Observed", "max_confidence": 0.90},
    "DER": {"label": "Derived", "max_confidence": 0.85},
    "INT": {"label": "Interpreted", "max_confidence": 0.75},
    "SPEC": {"label": "Speculated", "max_confidence": 0.50},
}

AUTHORITY_LEVELS = {
    "constitutional": 1.0,
    "verified": 0.8,
    "advisory": 0.5,
    "provisional": 0.3,
    "blocked": 0.0,
}

# ── Gödel Lock ───────────────────────────────────────────────────────
def godel_check(entry: dict) -> tuple[bool, list[str]]:
    violations = []
    prov = entry.get("provenance", {})
    truth = entry.get("truth", {})
    auth = entry.get("authority", {})
    tc = truth.get("class")

    if not prov.get("source"):
        violations.append("GÖDEL-1: No provenance source")
    if not tc or tc not in TRUTH_CLASSES:
        violations.append("GÖDEL-2: No valid truth class (OBS/DER/INT/SPEC)")
    if tc == "OBS" and not prov.get("evidence") and not prov.get("source_receipts"):
        violations.append("GÖDEL-3: OBS requires evidence or source_receipts")
    if auth.get("level") == "constitutional" and not auth.get("ratified_by"):
        violations.append("GÖDEL-4: Constitutional requires ratification reference")
    if tc and tc in TRUTH_CLASSES:
        max_conf = TRUTH_CLASSES[tc]["max_confidence"]
        if truth.get("confidence", 0) > max_conf:
            violations.append(f"GÖDEL-5: Confidence exceeds ceiling {max_conf} for {tc}")
    if auth.get("self_authorized") is True:
        violations.append("GÖDEL-6: Cannot self-authorize authority expansion")
    return (len(violations) == 0, violations)

# ── Entry Factory ────────────────────────────────────────────────────
def create_entry(
    content: str,
    truth_class: str = "INT",
    confidence: float = 0.5,
    authority_level: str = "advisory",
    provenance_source: str = "",
    provenance_evidence: str = "",
    category: str = "memory",
    expires_days: int | None = None,
) -> dict:
    tc = truth_class.upper()
    if tc in TRUTH_CLASSES:
        confidence = min(confidence, TRUTH_CLASSES[tc]["max_confidence"])
    now = datetime.now(UTC)
    return {
        "id": f"mem-{uuid.uuid4().hex[:12]}",
        "content": content,
        "truth": {"class": tc, "confidence": round(confidence, 2)},
        "authority": {
            "level": authority_level,
            "may_inform_reasoning": authority_level != "blocked",
            "may_change_routing": authority_level in ("constitutional", "verified"),
            "may_restrict_tools": authority_level == "constitutional",
            "may_expand_tools": False,
            "self_authorized": False,
        },
        "provenance": {
            "source": provenance_source or f"hermes-session:{now.strftime('%Y%m%d')}",
            "evidence": provenance_evidence,
            "source_receipts": [],
        },
        "lifecycle": {
            "state": "active",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "decay": {
                "confidence_per_month": 0.05,
                "review_after": (now + timedelta(days=30)).isoformat(),
            },
        },
        "category": category,
    }

# ── Store CRUD ───────────────────────────────────────────────────────
def load_store() -> list[dict]:
    if not STORE_PATH.exists():
        return []
    return json.loads(STORE_PATH.read_text())

def save_store(entries: list[dict]) -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))

def add_entry(entry: dict) -> tuple[bool, str]:
    ok, violations = godel_check(entry)
    if not ok:
        return False, "GÖDEL LOCK REJECTED:\n" + "\n".join(f"  • {v}" for v in violations)
    entries = load_store()
    entries.append(entry)
    save_store(entries)
    return True, f"Stored {entry['id']}"

# ── CLI ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p = sub.add_parser("add")
    p.add_argument("--content", required=True)
    p.add_argument("--truth-class", default="INT", choices=TRUTH_CLASSES)
    p.add_argument("--confidence", type=float, default=0.5)
    p.add_argument("--authority", default="advisory", choices=AUTHORITY_LEVELS)
    p.add_argument("--source", default="")
    p.add_argument("--evidence", default="")
    p.add_argument("--category", default="memory")
    sub.add_parser("list")
    sub.add_parser("render")
    sub.add_parser("validate")
    args = parser.parse_args()

    if args.cmd == "add":
        e = create_entry(args.content, args.truth_class, args.confidence,
                        args.authority, args.source, args.evidence, args.category)
        ok, msg = add_entry(e)
        print(msg)
        sys.exit(0 if ok else 1)
    elif args.cmd == "list":
        for e in load_store():
            print(f"  [{e['id']}] [{e['truth']['class']} {e['truth']['confidence']:.0%}] {e['content'][:80]}")
    elif args.cmd == "render":
        entries = load_store()
        lines = ["# Governed Memory\n"]
        cats: dict[str, list] = {}
        for e in entries:
            if e.get("lifecycle", {}).get("state") == "tombstoned":
                continue
            cats.setdefault(e.get("category", "other"), []).append(e)
        for cat, items in sorted(cats.items()):
            lines.append(f"## {cat.replace('_', ' ').title()}\n")
            for item in items:
                tc = item["truth"]["class"]
                conf = item["truth"]["confidence"]
                level = item["authority"]["level"]
                lines.append(f"- [{tc} {conf:.0%} | {level}] {item['content']}")
            lines.append("")
        md = "\n".join(lines)
        print(md)
        RENDERED_PATH.write_text(md)
    elif args.cmd == "validate":
        for e in load_store():
            ok, v = godel_check(e)
            print(f"  {'✅' if ok else '❌'} {e['id']}: {e['content'][:60]}")
            if v:
                for x in v: print(f"      {x}")

if __name__ == "__main__":
    main()
