# Cron & Memory Hygiene — Entropy Reduction Patterns

## Cron Job Redundancy Audit

When a Hermes instance has 10+ cron jobs, duplicates and overlaps accumulate. Run this audit:

### Step 1: List all jobs with schedules and delivery targets
```bash
hermes cron list 2>/dev/null
```

### Step 2: Find schedule overlaps
Look for:
- **Same time, same topic**: e.g., two gold signal jobs at 8am and 9am
- **Same topic, different audiences**: verify both audiences are intentional (e.g., DM vs group)
- **Watchdog + reminder**: if a watchdog runs 8am/8pm AND a separate reminder runs 9am, the reminder is redundant
- **Never-ran jobs**: `last_run_at: null` with `enabled: true` — verify the script exists and works

### Step 3: Check for error-state jobs
Jobs with `last_status: error` — run the script manually to diagnose:
```bash
bash ~/.hermes/scripts/<script>.sh 2>&1 | tail -10
python3 ~/.hermes/scripts/<script>.py 2>&1
```

Common causes:
- **Unbound variable** in bash scripts with `set -euo pipefail` — a variable referenced but never initialized
- **Timeout** — script takes longer than the cron runner allows (default ~30s for script-only jobs)
- **Missing dependency** — script references a file/binary that doesn't exist

### Step 4: Remove or consolidate
```bash
hermes cron remove <job_id>  # Remove redundant job
```

**Rule:** Keep the job with the BROADER scope (watchdog > reminder, combined > separate).

## Governed Memory Hygiene

The Hermes governed memory system has this architecture:
```
governed.json  →  RENDERED.md  →  system prompt injection
     ↑
MEMORY.md (legacy)  +  USER.md (legacy)
```

### Deduplication check
Entries in `governed.json` can overlap across categories (`operational_notes` vs `user_profile`). Check:
```python
import json
d = json.load(open("/root/.hermes/memories/governed.json"))
for cat in set(e.get("category") for e in d):
    entries = [e for e in d if e.get("category") == cat]
    print(f"{cat}: {len(entries)} entries")
```

Cross-category keyword overlap:
```python
# Find entries that share 4+ opening words across categories
for o in op_notes:
    o_words = set(o["content"].lower().split()[:15])
    for u in user_prof:
        u_words = set(u["content"].lower().split()[:15])
        common = o_words.intersection(u_words)
        if len(common) >= 4:
            print(f"OVERLAP: {o['content'][:60]} / {u['content'][:60]}")
```

### Legacy file cleanup
If `governed.json` contains all data from `MEMORY.md` and `USER.md`, archive the legacy files:
```bash
mkdir -p ~/.hermes/memories/.legacy
mv ~/.hermes/memories/MEMORY.md ~/.hermes/memories/.legacy/MEMORY.md.archived
mv ~/.hermes/memories/USER.md ~/.hermes/memories/.legacy/USER.md.archived
# Clean empty lock files
rm -f ~/.hermes/memories/MEMORY.md.lock ~/.hermes/memories/USER.md.lock
# Regenerate RENDERED.md
python3 ~/.hermes/scripts/governed_memory.py render
```

### Impact
- Legacy files: ~5.3KB of duplicated system prompt injection per turn eliminated
- RENDERED.md regenerated from governed.json: single source of truth
- Dr. Azli dedup: removed duplicate entry that appeared in both categories

### Rule
Never delete legacy files — archive them. The governed store may reference them for migration provenance.
