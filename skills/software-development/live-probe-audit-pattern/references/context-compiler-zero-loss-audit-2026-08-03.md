# Context Compiler "Zero Information Loss" Audit — 2026-08-03

Worked example for the Invariant-Preservation Audit section of the parent skill.

## The claims under audit

An agent report (Federation Context Compiler build) claimed:

| Claim | Verdict | Evidence |
|---|---|---|
| 3-pass compiler built, 921 lines | ✅ TRUE | file on disk, runs, exit 0 |
| 80.6% token reduction on kernel task | ✅ TRUE (compiled side) | live run: compiled output ~6,600 tokens |
| Boot doc 2,930 bytes vs 31,298 | ✅ TRUE | `wc -c`: 2913 vs 31298 (~90% byte reduction) |
| Build time <1ms | ✅ TRUE | 0.1 ms observed |
| Routing correct (kernel→arifos, seismic→geox…) | ✅ TRUE | live run showed arifos 100% primary |
| "zero information loss for the task at hand" | ❌ FALSE | floors table had 10 floors, not 13 |
| "214 lines" compiled variant | ❌ FALSE | disk: 84 lines |
| "43 receipts, metabolic cycle complete" | ⚠️ UNVERIFIED | no locatable receipt store found → [SPEC] |
| "FQ=1.22 OVERHEAT = sub-ms timing artifact" | ⚠️ SELF-EXPLAINED | builder's own interpretation → [INT]; also FQ ∉ [0,1] = clamp bug |

## The core finding — constitutional amnesia

`context_boot.sh` hardcoded a floors table that omitted:

- **F3 TRI-WITNESS** (DERIVED) — the very mechanism that caught this bug
- **F5 PEACE²** (SOFT)
- **F12 RESILIENCE** (HARD — injection defense!)

An agent booting with that slim doc would operate without its injection-defense floor. Slim boot ≠ floor boot: organs may be on-demand via `arif_route`, floors may not.

## The fix (applied, verified)

Patched the hardcoded table in `/root/A-FORGE/scripts/context_boot.sh` to include all 13 floors. Re-verified live later the same day:

```bash
bash /root/A-FORGE/scripts/context_boot.sh "fix arifOS kernel judge bug" 2>/dev/null \
  | grep -o "F[0-9]\+" | sort -u | tr '\n' ' '
# → F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13  (all 13 present)
wc -c   # 3142 (was 2913 — +229 bytes, still ~90% reduction)
```

Note the verification gotcha: `context_boot.sh` with a path arg still writes to stdout (usage: `--print|--write <path>|--flow`), so capture stdout to a file rather than expecting the arg to be written.

## Turn 2/3 findings — the benchmark and the mechanism

The build continued (v2: context_boot.sh + tool_surface_gen.py + arifFlow pipeline). Three more class-level findings:

### 1. Hardcoded baseline = benchmark theater
`grep -n` on context_compile.py found `FULL_LOAD_BASE_TOKENS = ***` — the "naive full-dump 34,000 tokens" every reduction % was computed against is a **constant, never measured**. The compiled token counts were real (measured per run), but "65–80% reduction" was relative to an assumption. Until the true full load (all tool schemas + skills catalog + docs) is token-counted, the headline ratio is unverifiable. The reduction % is only as honest as its baseline.

### 2. Attention reduction ≠ access reduction
The v2 narrative claimed: "tool yang tak ada = tak boleh dipanggil salah." Only half true:
- Slim AGENTS.md reduces **temptation** (attention) — the model is less lured toward irrelevant tools. ✅
- But excluded organs' MCP servers stay wired — their tool schemas are still loaded and CALLABLE. The doc says "don't use GEOX"; the model still *can* call `geox_seismic_compute`. ⚠️
- True exclusion requires **runtime schema gating** — e.g. Hermes cron `enabled_toolsets`, booting the agent with only arifos+aforge toolsets for a kernel task. Doc compile = half the mechanism; schema gate = the other half.

Also: "5× faster first-token latency" is directionally right (prefill ∝ token count) but [DER] — no benchmark was run on this stack. Don't cite multipliers without measurement.

### 3. Canary criteria for compressed-context rollout
A single-organ canary proves only the easy case. The compiler's failure mode is the **cross-organ task** ("interpret seismic, then compute EMV" — both organs need Tier 1). Binary criteria proposed:
1. **Routing hit** — agent picks the correct organ(s) without hints (pass/fail)
2. **Missed dependency** — was anything needed but excluded? If yes, did the on-demand `arif_route` rescue succeed? (this is the real Tier 3 test)
3. **Regression** — output quality ≥ full-context run on the same task

## Lessons (class-level, not session-level)

1. **Compression claims split in three:** the reduction engine, the invariant set, and the baseline. Verify each separately — a good engine can launder a broken invariant set AND a fake baseline.
2. **Generated artifacts are the audit surface.** The report's numbers describe intent; `wc`/`grep` on the output file describe reality.
3. **Hardcoded "always include" blocks are where loss hides.** In any slim-doc/context-compiler generator, diff the always-include block against the canonical source list — that diff IS the loss function.
4. **Grep for the baseline constant before citing any reduction ratio.** Assigned ≠ computed.
5. **Invariant restoration is nearly free.** +229 bytes bought back 3 constitutional floors. Never accept "compression needs the loss" framing. Floors are the compiler's own type system — a real compiler never strips those.
6. **Doc-slimming is attention control; schema gating is access control.** The "zero information loss" / "can't call wrong tool" claims conflate them. Name which half a mechanism actually delivers.
7. **Cross-witness in action:** the builder claimed losslessness; an independent probe found the loss; the builder then cited the independent probe as proof F3 works. That loop — claim → independent falsification → fix → re-verification — is F3 doing its job. Record it as such when reporting.

## Related artifacts

- Compiler: `/root/A-FORGE/scripts/context_compile.py` (921L, stdlib only)
- Boot generator: `/root/A-FORGE/scripts/context_boot.sh` (floors fixed 2026-08-03, re-verified 13/13)
- Helpers: `context_compile.sh` (bash wrapper), `tool_surface_gen.py` (organ listings)
- Receipt: `/root/forge_work/2026-08-03-context-compiler/RECEIPT_v2.md`
- Original inspiration: github.com/Emmimal/context-compiler (reachability + skeletonization; same 3-tier idea: full / skeleton / excluded). Note the federation version's Pass 1 is a keyword classifier (~150 mappings), not structural AST import resolution like the article's — a class difference worth naming when evaluating it.
