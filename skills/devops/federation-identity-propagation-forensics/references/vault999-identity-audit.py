#!/usr/bin/env python3
"""VAULT999 Identity Audit — quantify anonymous/openclaw-anon/self_report rates.

Run: python3 vault999-identity-audit.py [--date YYYY-MM-DD]

Outputs actor/session distribution for all three VAULT999 ledger files.
Use --date to filter to entries on or after a specific date.
"""

import json
import sys
from collections import Counter
from pathlib import Path

VAULT_DIR = Path("/root/.local/share/arifos/vault999")
LEDGERS = ["receipts_v2.jsonl", "outcomes.jsonl", "seal_chain.jsonl"]

PLACEHOLDERS = {"anonymous", "openclaw-anon", "unknown", "MISSING", "null", "", "None"}


def audit_ledger(path: Path, since_date: str | None = None):
    actors = Counter()
    sessions = Counter()
    actor_sources = Counter()
    kernel_verdicts = Counter()
    total = 0

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Date filter
            ts = d.get("timestamp") or d.get("ts") or d.get("epoch", "")
            if since_date and ts[:10] < since_date:
                continue

            total += 1
            actor = str(d.get("actor_id") or d.get("actor") or "MISSING")
            session = str(d.get("session_id") or d.get("session") or "MISSING")
            actors[actor] += 1
            sessions[session] += 1

            # seal_chain specific fields
            if "actor_source" in d:
                actor_sources[d["actor_source"]] += 1
            if "kernel_verdict" in d:
                kernel_verdicts[d["kernel_verdict"]] += 1

    return total, actors, sessions, actor_sources, kernel_verdicts


def main():
    since_date = None
    if "--date" in sys.argv:
        idx = sys.argv.index("--date")
        if idx + 1 < len(sys.argv):
            since_date = sys.argv[idx + 1]

    total_placeholders = 0
    total_entries = 0

    for fname in LEDGERS:
        path = VAULT_DIR / fname
        if not path.exists():
            print(f"\n=== {fname}: NOT FOUND ===")
            continue

        total, actors, sessions, actor_sources, kernel_verdicts = audit_ledger(path, since_date)
        total_entries += total

        anon_count = sum(v for k, v in actors.items() if k in PLACEHOLDERS)
        total_placeholders += anon_count

        print(f"\n{'='*60}")
        print(f"=== {fname} ({total} entries) ===")
        if since_date:
            print(f"=== Filtered: >= {since_date} ===")
        print(f"=== Anonymous rate: {anon_count}/{total} ({100*anon_count/max(total,1):.1f}%) ===")

        print(f"\n  Top actors:")
        for k, v in actors.most_common(10):
            flag = " ⚠ PLACEHOLDER" if k in PLACEHOLDERS else ""
            print(f"    {k:35s} {v:6d}{flag}")

        print(f"\n  Top sessions:")
        for k, v in sessions.most_common(5):
            flag = " ⚠" if k in PLACEHOLDERS else ""
            print(f"    {k:35s} {v:6d}{flag}")

        if actor_sources:
            print(f"\n  actor_source distribution:")
            for k, v in actor_sources.most_common():
                flag = " ⚠" if k == "self_report" else ""
                print(f"    {k:35s} {v:6d}{flag}")

        if kernel_verdicts:
            print(f"\n  kernel_verdict distribution:")
            for k, v in kernel_verdicts.most_common():
                flag = " ⚠" if k in ("UNKNOWN", "FAIL") else ""
                print(f"    {k:35s} {v:6d}{flag}")

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_entries} entries, {total_placeholders} anonymous ({100*total_placeholders/max(total_entries,1):.1f}%)")


if __name__ == "__main__":
    main()
