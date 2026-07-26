# Worked Example: WhatsApp Chat with Nabilah Fazil (2015-2026)

## Input
- File: WhatsApp Chat with Nabilah Fazil.txt
- Size: 38,571 lines, 2.2MB
- Parse result: 27,410 messages (Nabilah: 16,405, Arif: 11,005)
- Date range: Aug 2015 → Jul 2026 (11 years)
- Peak years: 2019 (5,072), 2020 (4,731) — COVID lockdown era

## Parse Technique That Worked
- Wrote parse script to `/tmp/nab_analysis.py` via `write_file`
- Ran via `terminal("python3 /tmp/nab_analysis.py", timeout=30)`
- Did NOT use `execute_code` batch reads — file too large for read_file pagination
- Ran 4 separate analysis passes: (1) full stats, (2) keyword frequency, (3) life-event timeline, (4) 2026 crisis section

## Keyword Categories Used
```python
{
    "husband": ["fahim"],
    "child": ["fattah"],
    "marriage": ["nikah", "kahwin", "tunang"],
    "divorce": ["cerai", "talaq", "lafaz"],
    "career": ["schlumberger", "infineon", "engineer", "lecturer", "cikgu", "PhD", "IPG"],
    "health": ["hospital", "sakit"],
    "finance": ["hutang", "loan", "CTOS", "saman"],
    "emotional": ["sorry", "takut", "sedih", "marah", "love", "rindu", "syukur"],
    "family": ["mak", "abah", "azwa", "jia"],
    "spiritual": ["doa", "solat", "islam", "quran", "allah"],
}
```

## Deliverable Shape Produced
6-tier structure delivered in BM casual + English analytical:

1. **Fakta Keras** — career timeline, marriage date, child name, father's death
2. **Yang Tersembunyi** — 5 things the chat revealed that Arif likely didn't know
3. **Pattern Recognition** — chronic sorry, pendam-explode cycle, invisible caretaker, dependency on abah
4. **Trauma Layers** — abah (deepest), mak (complicated), Arif (trust broken), Fahim (financial abuse)
5. **Kekuatan** — career pivot, spiritual grounding, political awareness, resilience
6. **Nasihat** — 7 direct points written as if speaking to Nabilah

## Key Insight: "Sorry" Frequency
The most revealing single metric was the count of "sorry" messages from Nabilah — estimated 100+ across 11 years. This single pattern (chronic guilt/apologizing for existing) was more diagnostic than any topic frequency table.

## Pitfall Encountered
- First attempt used `execute_code` with inline `terminal()` calls containing nested Python — escaped quotes broke. Fix: always `write_file` the script, then `terminal("python3 /tmp/script.py")`.
- Initial keyword extraction missed career pivot (2017: engineer → 2024: cikgu) because "kerja" is too common. Had to add specific company names (Infineon, Schlumberger) and role names (lecturer, cikgu, IPG) to catch the full arc.
