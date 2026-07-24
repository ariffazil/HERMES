# Governance Pointer Propagation — AGENTS.md Consistency

> **Pattern:** Inject a cross-cutting governance pointer/reference line into all federation organ AGENTS.md files and external agent harness AGENTS.md files.

## When to Use

- A new governance document is created (e.g., `AAA-ZEN-ALIGNMENT.md`) and every organ + agent harness needs a pointer line to it.
- A canonical path changes and needs updating across all AGENTS.md files.
- A new federation organ needs to be added to the list of files that carry a standard footer/pointer.

## Files to Update

### Federation Organ AGENTS.md (6 organs)
```
/root/arifOS/AGENTS.md
/root/A-FORGE/AGENTS.md
/root/GEOX/AGENTS.md
/root/WEALTH/AGENTS.md
/root/WELL/AGENTS.md
/root/HERMES/AGENTS.md
```

### AAA Surface
```
/root/AAA/CLAUDE.md
```

### External Agent Harness AGENTS.md (7 agents)
```
/root/.arifos/agents/claude/AGENTS.md
/root/.arifos/agents/antigravity/AGENTS.md
/root/.arifos/agents/gemini/AGENTS.md
/root/.arifos/agents/copilot/AGENTS.md
/root/.arifos/agents/kimi/AGENTS.md
/root/.arifos/agents/opencode/AGENTS.md
/root/.arifos/agents/cursor/AGENTS.md
```

## Insertion Point

All AGENTS.md files follow a consistent structure: a blockquote header block (`> ...` lines with metadata), then an empty line, then the first `##` section heading. The pointer goes as the LAST line of the header blockquote:

### Organs with 2-line blockquote (most common)

Organ files have:
```
> **Purpose line.**
> Organ role description.
```
Add after the second `>` line:
```
> **ZEN:** `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` — 18 operational rules. Load at boot.
```

### Organs that already have inline Zen reference (arifOS, HERMES)

arifOS has `**Zen:** /root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` inline — already present, skip.
HERMES has inline `**Zen:** ...` — already present, skip.

### External harness files (7 agents)

These have a 3-5 line blockquote:
```
> **Authority:** 888 (...)
> **Citizenship:** warga-aaa | **Status:** ACTIVE
> **Runtime:** <agent-name> | **Config:** <path>
```
Add after the LAST `>` line (typically the `Runtime:` or `Config:` line):
```
> **ZEN:** `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` — 18 operational rules. Load at boot.
```

### Copilot exception

Copilot's header ends with `**Forged:** ... · **DITEMPA BUKAN DIBERI**` and is followed by `---` separator, not `## INIT`. Insert after the last `>` line, before `---`.

## Procedure

### 1. Check which files already have the pointer

```bash
# In organ AGENTS.md files
grep -rn "ZEN-ALIGNMENT\|AAA-ZEN" /root/{arifOS,A-FORGE,GEOX,WEALTH,WELL,HERMES,AAA}/AGENTS.md /root/AAA/CLAUDE.md 2>/dev/null

# In external harness files
grep -rn "ZEN-ALIGNMENT\|AAA-ZEN" /root/.arifos/agents/*/AGENTS.md 2>/dev/null
```

### 2. Read each file to find the correct insertion point

```bash
head -20 /root/WEALTH/AGENTS.md
# etc. for each file
```

### 3. Patch with the pointer line

Use the `patch` tool. The old_string should include the last blockquote line + the empty line + the section heading to ensure uniqueness. Example for a file with 2-line blockquote:

```python
# old_string:
"> Organ role description.\n\n## Identity"

# new_string:
"> Organ role description.\n> **ZEN:** `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` — 18 operational rules. Load at boot.\n\n## Identity"
```

### 4. Verify

```bash
grep -rn "ZEN-ALIGNMENT\|AAA-ZEN" /root/{arifOS,A-FORGE,GEOX,WEALTH,WELL,HERMES,AAA}/AGENTS.md /root/AAA/CLAUDE.md 2>/dev/null
grep -rn "ZEN-ALIGNMENT\|AAA-ZEN" /root/.arifos/agents/*/AGENTS.md 2>/dev/null
```

Every file should now show the pointer. Expected total count: **14 files** (6 organs + CLAUDE.md + 7 agent harnesses).

## Common Pattern: Inline vs Separate Line

Two styles of ZEN reference are used across the federation:

| Style | Example Files | When to Use |
|-------|--------------|-------------|
| **Inline** (part of existing `>` line) | `arifOS/AGENTS.md`, `HERMES/AGENTS.md`, `AAA/CLAUDE.md` | When the organ has a compound header line listing multiple canonical references |
| **Separate `>` line** | WEALTH, WELL, A-FORGE, GEOX, agent harnesses | All other organs — cleaner separation, easier to grep |

For propagation tasks, use the **separate line** style unless the target already has an inline style from a previous propagation.

## Pitfalls

- **GEOX already had pointer before 2026-07-24 propagation.** Some organs may have been wired earlier. Always check (Step 1) before patching.
- **Copilot file has `---` separator instead of `## INIT`.** Don't confuse the insertion point. Read the file first.
- **arifOS and AAA/CLAUDE.md already have inline zen references.** Skip these — they were wired correctly during prior sessions. Injecting a second pointer would create duplication.
- **Don't assume all 14 files need the pointer.** Pre-existing references in arifOS, HERMES, GEOX, and AAA/CLAUDE.md mean actually only 10 files need the injection (verified 2026-07-24).
