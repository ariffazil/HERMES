# Bulk Description Zen Workflow

Proven on 430 SKILL.md files across `/root/AAA/skills/` and `~/.hermes/skills/` on 2026-07-24.

## Principle

**Say it once, positively, no examples.** The smarter the model, the fewer instructions it needs.

## Zen Heuristic Rules (Python implementation)

These rules were derived from the principle above and proved against 430 real-world files:

```python
def zen_description(desc):
    """Shorten a description to ONE high-signal line (10–20 words, ideally ~15)."""
    if not desc:
        return desc

    # 1. Strip "Use when:" / "Use this when:" prefixes
    desc = re.sub(r'^Use this when:\s*', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'^Use when:\s*', '', desc, flags=re.IGNORECASE)

    # 2. Strip trailing "Use when…" clauses (with or without preceding period)
    desc = re.sub(r'\s*\.\s*Use when\b.*', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\s*Use this when\b.*', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\s*Use when\b.*', '', desc, flags=re.IGNORECASE)

    # 3. Remove parenthetical explanations (e.g., i.e., including, such as, like)
    desc = re.sub(r'\s*\([^)]*e\.g\.[^)]*\)', '', desc)
    desc = re.sub(r'\s*\(including\s[^)]*\)', '', desc, flags=re.IGNORECASE)

    # 4. Remove trailing example lists (em/en dash + e.g.)
    desc = re.sub(r'\s*[—–]\s*e\.g\..*', '', desc)

    # 5. Remove "Modes:" / "Modes include:" trailing clauses
    desc = re.sub(r'\s*Modes?[:\s].*', '', desc, flags=re.IGNORECASE)

    # 6. Remove mid-sentence "Use when" after comma
    desc = re.sub(r',\s*use when\b.*', '', desc, flags=re.IGNORECASE)

    # 7. Clean whitespace and trailing period
    desc = re.sub(r'\s{2,}', ' ', desc)
    desc = desc.strip().rstrip('.')

    # 8. If still >25 words, take first sentence
    if len(desc.split()) > 25:
        sentences = re.split(r'(?<=[.!?])\s+', desc)
        if len(sentences) > 1:
            desc = sentences[0].strip().rstrip('.')

    # 9. If still >22 words, hard-trim to 20
    if len(desc.split()) > 22:
        desc = ' '.join(desc.split()[:20]).rstrip('.')

    desc = desc.strip().rstrip('.')
    return desc
```

## YAML Quoting Edge Cases

Four patterns found during the 430-file run:

### Pattern A: Double-Double-Quoted `""text""`

```yaml
description: ""Audit repositories with parallel-forge history""
```

Fix: `re.sub(r'^description:\s*""(.+?)"', r'description: "\1"', content, flags=re.MULTILINE)`

### Pattern B: Single-Single-Quoted `''text''`

```yaml
description: ''Produces a seven-repository federation release manifest''
```

Fix: `re.sub(r"^description:\s*''(.+?)'", r"description: '\1'", content, flags=re.MULTILINE)`

### Pattern C: Trailing Double-Quote `"text""`

```yaml
description: "Build thin translation proxies between incompatible LLM API formats""
```

Fix: `re.sub(r'""$', '"', line)` on the description line.

### Pattern D: Strike-three trail quote `'''text'`

```yaml
description: '''SOLE controller skill for repository intelligence''
```

Fix: `re.sub(r"^description:\s*'''(.+?)'", r"description: '\1'", content, flags=re.MULTILINE)`

### Detection

```bash
grep -r '^description: ""' /path/to/skills/ --include='SKILL.md'
grep -r '^description: $' /path/to/skills/ --include='SKILL.md'
```

Full YAML validation:

```python
import yaml, re
for root, dirs, files in os.walk('/path/to/skills/'):
    if 'SKILL.md' not in files:
        continue
    fp = os.path.join(root, 'SKILL.md')
    with open(fp) as f:
        content = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        try:
            yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            print(f"YAML ERROR: {fp}: {e}")
```

## Full Workflow

```
Step 1: COLLECT → find all SKILL.md files
Step 2: EXTRACT → read YAML frontmatter, extract description, strip outer quotes
Step 3: ZEN → apply heuristic rules
Step 4: RE-QUOTE → wrap in original quote style if original had quotes
Step 5: REPLACE → find-and-replace the description line in frontmatter
Step 6: FIX QUOTES → run Patterns A-D fixes (re-poll until no more matches)
Step 7: VALIDATE → YAML parse all frontmatter blocks + grep for empty/broken
Step 8: SPOT-CHECK → manually verify ~5 random files
```

## Per-run Stats (2026-07-24)

| Metric | Value |
|--------|-------|
| Files scanned | 430 |
| Modified (first pass) | 215 |
| Double-quote fixes | 105 |
| Already concise | 208 |
| No frontmatter (skipped) | 6 |
| No description (skipped) | 1 |
| YAML errors after fix | 0 |
