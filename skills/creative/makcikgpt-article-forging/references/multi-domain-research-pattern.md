# Multi-Domain Research Pattern for MakcikGPT

> Used for articles that span multiple knowledge domains (economy + politics + social + technology).

## Pattern: Parallel Search, Sequential Synthesize

When the topic spans multiple domains, run parallel searches (3-4 at a time) to gather breadth, then synthesize into one hidden thread.

### Search Template

```
Domain 1 (Economy):   "Malaysia economy 2026 outlook risks challenges"
Domain 2 (Politics):  "Malaysia politics Anwar Ibrahim 2026 election"
Domain 3 (Social):    "Malaysia social issues 2026 cost of living rakyat"
Domain 4 (Technology): "Malaysia AI artificial intelligence 2026 jobs"
```

Each domain gets 2-3 searches (surface + structural + shadow). Total: 8-12 searches.

### Synthesis Rule

After all searches, ask ONE question: "Apa benang yang sama?"

All domains must connect to ONE hidden thread. If they don't connect, the article is too broad — narrow the scope.

### Example Threads (proven)

| Domains | Hidden Thread |
|---------|--------------|
| Economy + Politics + Social + AI | "Malaysia sedang makan generasi sendiri" |
| PETRONAS + Rightsizing + Farm-out | "Sistem buat orang baik rationalize evil kecil" |
| Iran + Hormuz + Subsidy + Election | "Semua orang dalam survival mode" |

### Evidence Tagging

Every data point from search results gets tagged:
- **OBS** — directly from source (ministerial statement, report, data)
- **INT** — interpretation of multiple OBS points
- **SPEC** — projection, prediction, "what if"
- **SHADOW** — human motivation inference (can't seal 100%, but pattern is strong)

### Tool Sequence

```
1. forge_search × 4 (parallel, different domains)
2. forge_search × 4 (parallel, deeper on each domain)
3. Read results, identify thread
4. Write article (sequential, one sitting)
5. Build + Deploy
```

Don't use web_extract for breadth — forge_search is faster for discovering what's out there. Use web_extract only for depth on specific articles that need quoting.

### Proven Sources for Malaysia Topics

| Source | Strength |
|--------|----------|
| Reuters | Fiscal data, PETRONAS, policy |
| ISEAS/FULCRUM | Southeast Asia analysis |
| CNA | Malaysian politics detail |
| World Bank | Structural economic data |
| UNICEF | Social impact data |
| BERNAMA | Official government statements |
| The Edge Malaysia | Business/fiscal analysis |
| East Asia Forum | Political analysis |
| BTI 2026 | Country governance assessment |
| SUHAKAM | Human rights statements |
