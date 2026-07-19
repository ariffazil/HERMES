# Boot-Wiring Pattern: Knowledge Module → System Prompt

> Pattern for making a knowledge module available at every agent session start.

## Problem

A knowledge module (like ATLAS333) exists as MCP resources but agents don't consume it because:
1. Skills are loaded on-demand, not at boot
2. MCP resources require active querying
3. No auto-injection into the system prompt

## Solution: Governed Memory Boot Context

Add a compact reference to the governed memory store (`~/.hermes/memories/governed.json`) with category `boot_context`. The governed memory render (`governed_memory.py render`) includes it in `RENDERED.md`, which is injected into every Hermes system prompt.

## Steps

### 1. Create the boot entry in governed.json

```python
import json

path = "/root/.hermes/memories/governed.json"
d = json.load(open(path))

d.append({
    "id": "module-name-boot-context",
    "content": "Compact reference: key facts, access URIs, activation rules, thresholds. Keep under 500 chars for system prompt efficiency.",
    "truth": {"class": "INT", "confidence": 0.85},
    "authority": {"level": "verified", "weight": 0.8},
    "category": "boot_context",
    "provenance": {"source": "arifos://module/index", "timestamp": "ISO-8601"}
})

with open(path, 'w') as f:
    json.dump(d, f, indent=2)
```

### 2. Regenerate RENDERED.md

```bash
python3 ~/.hermes/scripts/governed_memory.py render
```

### 3. Verify

```bash
grep -c "module-name" ~/.hermes/memories/RENDERED.md
# Should return 1
```

### 4. Also create a consumer skill

The boot context gives the agent awareness. The skill gives it action:
- How to access the module's MCP resources
- When to use it (triggers)
- What the data means (reference)

## Authority Format

The `authority` field MUST be a dict with `level` key, not a bare string:
```json
{"level": "verified", "weight": 0.8}  // ✅ correct
"verified"                              // ❌ causes render crash
```

## Proven 2026-07-16

ATLAS333 boot context added to governed.json (24 entries total). RENDERED.md now includes paradox reference at top of "Boot Context" section. Every Hermes session starts with 33 paradoxes, activation rules, demand tensor, and TEARFRAME thresholds loaded.

## Pitfalls

- **Don't bloat the boot context.** The full ATLAS333 has 33 paradoxes, 7 zones, 3 organs, thresholds, activation rules. The boot context should be a COMPACT reference (under 500 chars), not the full dump. Agents can query MCP resources for detail.
- **Category must be `boot_context`.** The governed memory render groups by category. Using a different category puts it in a different section (not at the top).
- **Render crashes on wrong authority format.** If `authority` is a string instead of a dict, `auth.get("level")` fails with AttributeError. Always use `{"level": "...", "weight": 0.N}`.
