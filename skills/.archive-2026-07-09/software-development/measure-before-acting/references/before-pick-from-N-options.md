# Before "Pick from N Options" — Diagnostic Recipe

**Why this exists:** Captured 2026-07-11 after I almost drafted a duplicate 749-line APA-Telegram spec because the user sent a "pick from 5 surfaces" menu — and the spec already existed with Phase-1 surface already locked.

**Core insight:** When Arif (or anyone) sends a structured "pick from these N options" decision on a topic that could plausibly have sealed doctrine, the decision is *already made* in the docs 70%+ of the time. Probe for the doc BEFORE composing.

## The Three Probes (5-10 seconds total)

```bash
# Probe 1: Does a spec or decision doc exist on this topic?
TOPIC="telegram"  # your topic
find /root -maxdepth 6 -type f -name "*.md" -mtime -14d 2>/dev/null \
  | xargs grep -l -i "$TOPIC" 2>/dev/null \
  | xargs grep -l -iE "(spec|design|surface|phase|locked)" 2>/dev/null \
  | head -10

# Probe 2: Is there a SEAL/scan/cap pattern that already named an answer?
find /root -type f -name "*.md" 2>/dev/null \
  | xargs grep -l -E "(Phase[- ]?[0-9].*(locked|surface)|Mandatory|no[- ]?menu)" 2>/dev/null \
  | head -5

# Probe 3: Did a recent audit or plan already pick?
ls -la /root/A-FORGE/forge_work/ 2>/dev/null | tail -10
ls -la /root/.arifos/forge_work/ 2>/dev/null | tail -10
```

## Verdict rules

| Probe result | Action |
|---|---|
| Recent spec/decision doc on topic found, Phase-N locked | Confirm the existing answer; offer to deep-dive or expand, not reforge |
| Recent spec/decision doc on topic found, no lock yet | Read for context, treat user's menu as fresh design input |
| No recent doc found | Take the menu seriously; design from scratch using the user's options |
| Doc found but contradicts itself / no clear lock | Surface the contradiction; ask which to honor |

## Three "Symptom Patterns" — Same Root Failure

(All three captured 2026-07-11 in one session, see SKILL.md §Failure 23)

1. **"I have enough" without listing probes run** — closed evidence-gathering before physical probe. Probe the named state on disk before declaring done.

2. **Accepting a "first time" / "novel" claim uncritically** — when Arif or anyone claims something is first, run `grep -ril <term> /root` and `git log --since=<date>` to find prior implementations. "First in arifOS post-rename" is not the same as "first ever."

3. **Treating a "pick from N options" menu as fresh design** — sealed doctrine likely exists. Run probe first; either confirm existing answer or escalate as a real design gap.

## Cross-references

- SKILL.md §Failure 17 — negative-existence claim without grepping
- SKILL.md §Failure 18 — stale audit cited as live state
- SKILL.md §Failure 21 — duplicate-spec drafting
- SKILL.md §Failure 23 — umbrella: closed evidence-gathering before physical probe
- `references/audit-doc-staleness-probe.md` — five-second doc-vs-disk recipe

*DITEMPA BUKAN DIBERI — the next decision is forged on disk, not in the user's text.*
