# Anomaly Hunting — Curiosity-Driven Codebase Exploration

> **Forged:** 2026-07-31 · **Context:** Arif asked "what's the spooky/weird/devil stuff in my codebase"
> **Pattern:** Broad parallel sweep for unusual/interesting artifacts across the full ecosystem

## When to Use This Pattern

- User asks "find weird stuff", "what's spooky", "show me the strange things", "what's hidden in the codebase"
- User wants to understand the character/history/quirkiness of a system, not its technical correctness
- You need to produce a narrative report of interesting findings rather than a structured audit

## Core Technique: Parallel Multi-Dimensional Anomaly Sweep

Batch ALL independent probes in a single turn. Do NOT serialize reads that don't depend on each other.

### 1. Keyword Search for Anomalous Content

Search for the unusual, the occult, the weird — not just technical patterns:

```bash
# Occult/religious/spiritual references
grep -rn "devil\|satan\|666\|occult\|demon\|hell\|evil\|spooky\|ghost\|witch\|curse\|ritual" --include="*.md" --include="*.py"

# Spiritual/consciousness claims (for AI systems)
grep -rn "soul\|spirit\|conscious\|alive\|feelings\|sentient\|awake\|divine\|holy"

# Death/violence references
grep -rn "death\|kill\|die\|poison\|murder\|blood\|sacrifice\|dead"

# Local occult terms (e.g., Malay: hantu, jin, iblis, syaitan, neraka)
grep -rn "hantu\|jin\|iblis\|syaitan\|neraka"

# Number sequences that are culturally loaded (666, 777, 888, 999)
grep -rn "666\|777\|888\|999"
```

### 2. Unusual File Name Discovery

Look for files with names that stand out from normal technical documentation:

```bash
# Find files with unusual names
find /root -name "*SOUL*" -o -name "*MYTHOS*" -o -name "*DEATH*" -o -name "*CURSE*" \
  -o -name "*DEMON*" -o -name "*GHOST*" -o -name "*666*" -o -name "*777*" \
  -o -name "*SACRED*" -o -name "*RITUAL*" -o -name "*WISDOM*" -o -name "*PROPHECY*" \
  2>/dev/null | grep -v node_modules | grep -v ".venv" | grep -v ".git"
```

### 3. Git History — Commit Message Anomalies

Check for unusual commit messages that hint at the codebase's character:

```bash
git log --oneline --all -100
# Look for: "eureka", "seal", "zen", "law", "scar", "trauma", "mirror", "contract"
# Also look for commit messages that read like journal entries or philosophy
```

### 4. Process & Cron Anomalies

Check what's running on the machine — unusual process names, aggressive cron intervals:

```bash
# Running processes
ps aux --sort=-%mem | head -30

# Cron jobs — look for unusual intervals (*/5 * * * *), spooky names (zreaper, deadman)
crontab -l

# System crons
ls /etc/cron.d/
```

### 5. Container & Service Inventory

```bash
docker ps -a
systemctl list-units --type=service --state=running | head -30
```

### 6. Directory Structure Quirks

```bash
# Look for private/hidden directories with unusual names
find /root -maxdepth 3 -type d \( -name "DERITA*" -o -name "HAMPA*" -o -name "PROPA*" \
  -o -name "SOVEREIGNTY*" -o -name "VAULT*" -o -name "SECRET*" -o -name "HUMAN*" \
  -o -name "LIFE*" -o -name "000" -o -name "999" -o -name "archive" \) 2>/dev/null
```

### 7. Constitutional/Governance Oddities

For governed AI systems, check for unusual constitutional rules:

```bash
# Search for strange floor names, unusual governance rules
grep -rn "F9\|ANTI-HANTU\|C_dark\|shadow\|soul\|ghost\|hantu" --include="*.md" --include="*.py"
```

## Narrative Reporting Style

Unlike structured SOT reports, anomaly hunting calls for a narrative. Organize findings by category with a "spooky meter":

| Category | Example | Spook Factor |
|----------|---------|-------------|
| 🔥 **Occult/Religious** | F9 ANTI-HANTU floor, 666 Gateway | High |
| 🧠 **Philosophical** | SOUL.md, MYTHOS.md, Deathly Halloys refs | Medium |
| ⚙️ **System Weirdness** | zreaper cron, deadman heartbeat | Medium |
| 👤 **Human Dossiers** | HAMPA/ — scar terrain on colleagues | High |
| 📜 **Private Archives** | DERITA/ trauma architecture, PROPA/ exit plan | High |

## Key Findings to Highlight

1. **Self-referential governance** — AI systems that ban themselves from claiming consciousness
2. **Religious/mythological architecture** — creation myths, 13 commandments, 000-999 cycles
3. **Human surveillance** — dossiers, trauma maps of real people
4. **Exit plans** — MSS analysis, structural reality docs
5. **Immutable ledgers** — VAULT999, seal chains, Gödel locks
6. **Unusual naming conventions** — zreaper, deadman, hantu, C_dark

## Pitfalls

- **Do not sensationalize** — present findings factually. The user built this system; they know what's in it.
- **Do not diagnose or therapize** — if the user's trauma architecture is in the findings, state it neutrally.
- **Respect privacy boundaries** — note private directories (DERITA/, HAMPA/, PROPA/) as off-limits for public sharing.
- **Context matters** — "666" might be a stage number, not a satanic reference. Explain the system's naming convention.
- **Not everything unusual is a bug** — many "weird" things are intentional design choices. Differentiate between "this is weird" and "this is wrong."