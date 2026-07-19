---
name: audit-parallel-forge-history
description: Audit repositories with parallel-forge history — multiple commits touching the same files from different sessions/agents. Prevents over-engineering dedup based on "duplicate grep hits" that are actually documented legacy boundaries. Load when auditing repos where multiple agents have forged independently, especially when finding "duplicate" constants/functions across modules.
tags: [audit, refactoring, parallel-forge, dedup, legacy-boundaries, governance]
triggers:
  - "audit for duplicates"
  - "find dead code"
  - "parallel forge"
  - "lower entropy"
  - "dedup APEX"
  - "consolidate runtime paths"
---

# Audit Repositories With Parallel-Forge History

The trap: when two agents forge the same file in parallel, the resulting code has **declared boundaries** that look like bugs to a third-party auditor. Grep finds "duplicate" `APEX_ORGANS`, "duplicate" `compute_apex_fingerprint`, "duplicate" `PERMITTED_STAGES`. The naive audit verdict: "PARTIAL — single SOT but dual runtime paths." The naive recommendation: forge a merge.

**Wrong.** A `git log --oneline <file>` reveals one agent intentionally tagged its work as `legacy compat shim`. The "duplicates" are a stable API contract.

## The Iron Rule

> **Before flagging "duplicate" definitions across files, read the docstrings of all modules first.**
>
> Grep shows duplication. Docstrings declare intent. **Docstring wins.**

## Concrete pattern (from arifOS quote registry 2026-07-19)

### What I almost did (wrong)

```bash
$ grep -rn "APEX_ORGANS\s*=" arifosmcp/
arifosmcp/runtime/quote_registry.py:165  APEX_ORGANS = (...)           # tuple
arifosmcp/runtime/philosophy_registry.py:48  APEX_ORGANS = [...]      # list
```

Verdict: "PARTIAL — schema drift, two definitions." Recommendation: merge into shared module.

### What docstring check revealed (right)

```bash
$ head -370 arifosmcp/runtime/quote_registry.py
... line 365:
"For NEW code, prefer philosophy_registry.resolve_quote() — it has
the unified schema (APEX fingerprint, federation URI, stage gate, and
tool-curated mapping) and is THE canonical resolution path. This function
is retained for backward compatibility with existing 555/999 callers."
```

The "duplicate" was a **declared legacy boundary**. `quote_registry.wisdom_quote_resolve` is intentionally kept as compat shim. `philosophy_registry.resolve_quote` is canonical. Both load from `quote_registry_v2.json` (single SOT).

### Verdict corrected

| Field | Naive | Corrected |
|---|---|---|
| SOT verdict | PARTIAL — schema drift | PARTIAL but INTENTIONAL — declared legacy boundary |
| Action | Merge APEX_ORGANS into shared module | Accept architecture; only merge if user explicitly demands strict unification (Path Y) |

## Audit Procedure (6 steps)

0. **Snapshot HEAD at audit start** — record `git rev-parse HEAD` and `git status --short`. The worktree is a moving target.
1. **Grep first, but don't trust** — find the "duplicates"
2. **Read every docstring** of files containing duplicates — look for "LEGACY", "compat shim", "deprecated but kept", "prefer X over this"
3. **`git log --oneline -- <file>`** for each duplicate file — identify parallel-forge history
4. **Check test coverage** — if both definitions have tests, they're load-bearing APIs; if only one, the other may be genuinely dead
5. **Re-probe HEAD before finalizing the receipt** — if a new commit lands mid-audit, re-verify the verdict from scratch (see "Mid-audit commit inversion" below)
6. **Ask the user before forging** — present Path X (accept architecture) vs Path Y (strict merge) with risk+cost

## Mid-audit commit inversion (proven 2026-07-19)

**The trap you didn't see coming**: the audit you started on commit X can be invalidated by commit X+N landing before you finalize. In a parallel-forge environment, this is the *default*, not an edge case. The receipt you wrote at T₀ is **historical**, not live, the moment a new commit lands.

**Proven pattern (2026-07-19 quote-registry audit)**:

```
T₀  06:58Z  commit 143afc741  Layer A/B/C/D unification. Author: Arif.
T₀  09:00Z  commit 6b1e84b37  inject_philosophy wiring. Author: ASI 💃.
T₀  09:18Z  audit starts. Verdict: PARTIAL (dual APEX_ORGANS, dual
         compute_apex_fingerprint, wisdom_quotes.py still alive,
         quote_ledger.py still imported).
T₁  09:22Z  commit b953eef8f  Path Y dedup. Author: FORGE-000Ω.
         - 3 duplicate definitions → 1 source of truth
         - APEX_ORGANS container drift → single tuple
         - wisdom_quotes.py (1285 LOC) DELETED
T₁  09:35Z  receipt overwritten with YES verdict + re-probe evidence
         (APEX_CONSTANTS is QR_APEX is PR_APEX holds at runtime)
```

The original receipt at `UNIFIED-SOT-AUDIT-RECEIPT-2026-07-19.md` was written at T₀ with the PARTIAL verdict. It is **stale**, even though the file still exists on disk and no one edited it. Future readers who pull just the receipt without re-running the audit will see a verdict that disagrees with live state.

**Reflex: before writing the final receipt line, run** `git log HEAD~5..HEAD --stat -- <scope>`. If the commit graph advanced since audit start, **re-probe from step 0**. Do not patch the existing verdict — rewrite the receipt with the new ground truth. Cite the new HEAD in the receipt header.

**3-step reflex**:
1. `git rev-parse HEAD` at audit start, write it into a "snapshot" line in your notes.
2. Before finalizing: `git log --oneline <snapshot>..HEAD` — list any new commits.
3. If new commits touch the audited files, re-run the live probes (greps, runtime imports, test suites) and rewrite the verdict section with `git rev-parse HEAD` at the time of finalization.

The verdict itself may flip (PARTIAL → YES in the example above). Do not fight the new reality — the receipt's job is to describe what IS, not what you found first.

## DeepSeek/OpenCode second-opinion pattern

When the audit verdict is non-trivial, spawn a second-opinion agent:

```bash
timeout 240 opencode run --model opencode-go/deepseek-v4-flash-free \
  --title "<audit-topic>" \
  '<spec with file:line citations and the specific question>'
```

DeepSeek caught 3 things the in-line grep audit missed:
1. Signature mismatch would break runtime if merged blindly
2. Container type drift (tuple vs list) — non-obvious failure mode
3. Lazy import → top-level feasibility (no circular import risk)

**Pattern**: give OpenCode the EXACT files + EXACT commands + a tight 4-line verdict format (VERDICT_LINE_1 through _4). Don't ask for new features.

## Dead code elimination — before deletion, trace the chain

For "this file looks dead" candidates:

```bash
# 1. Find direct importers
grep -rn "from .FILENAME" arifosmcp/

# 2. Recursively check if THOSE importers are live
# Example: quote_ledger.py was imported by context_witness.py
#          which IS used by tools.py:7060 → NOT dead despite no direct
#          caller in main runtime.
grep -n "FILENAME" arifosmcp/runtime/tools.py arifosmcp/runtime/__init__.py
```

**Rule**: A file is dead only when zero transitive importers are reachable from a live tool path.

## Pitfalls

- **Mid-audit commits invalidate your verdict** — snapshot `git rev-parse HEAD` at audit start, re-verify at finalization. See "Mid-audit commit inversion" above. The most common failure: writing a PARTIAL/NO verdict based on T₀ state, then a parallel-forge agent ships the fix at T₁, and the receipt stays stale on disk.
- **Grep is necessary but not sufficient** — duplicates may be declared legacy boundaries. Always read docstrings first.
- **Naive "PARTIAL" verdicts** are harmful — they suggest dedup work that breaks stable APIs.
- **OpenCode smoke-test first** — `opencode run --model opencode-go/deepseek-v4-flash-free 'Print ONLY: SMOKE_OK'`. If smoke fails, don't spawn the long task. Note: model IDs rotate — the canonical 2026-07 ID is `mimo-platform/mimo-v2.5-pro-ultraspeed` (default for the opencode-go provider) or `tokenplan-mimo/mimo-v2.5-pro` (legacy). Verify with `opencode models <provider>` before relying on a model ID.
- **OpenCode provider billing** — `tokenplan-mimo/mimo-v2.5-pro` and `mimo-platform/mimo-v2.5-pro-ultraspeed` may return "Insufficient account balance". Fallback: `qwen-token/qwen3.6-flash` (cheaper) or `mimo-platform/mimo-v2.5-pro` (try the non-ultraspeed tier first). Always probe before the full audit task.
- **Trust the parallel forge** — if the docstring says "canonical" / "legacy shim", believe it. Don't try to "improve" what two agents already agreed on.
- **Path Y is over-engineering** — only forge the merge if the user explicitly says "yes do Path Y." Default: Path X (status quo).
- **Atlas path off-by-one** — when a module uses `Path(__file__).resolve().parents[N] / "data" / "foo.json"`, N must match the actual file location relative to data/. If a sibling module uses `parents[N-1]` and the file resolves, the misaligned one is broken even though the file exists. The fix is always `parents[N-1]`, never "let me just add a workaround."

## References

- `references/quote-registry-2026-07-19-timeline.md` — three-commit sequence (T₀ audit start → T₁ commit inversion → T₁ receipt rewrite), live re-probe commands, dead-code backlog that survived the dedup, atlas path off-by-one reproducer
- `/root/A-FORGE/forge_work/2026-07-19/UNIFIED-SOT-AUDIT-RECEIPT-2026-07-19.md` — full session example (initial audit was wrong, corrected after docstring check + OpenCode verdict; **final receipt was itself invalidated by commit b953eef8f mid-audit** — see "Mid-audit commit inversion" above)
- `/root/A-FORGE/forge_work/2026-07-19/ENTROPY-LOWERING-RECEIPT-2026-07-19.md` — Path Y execution receipt
- `/root/A-FORGE/forge_work/2026-07-19/QUOTE-REGISTRY-APEX-UNIFICATION-RECEIPT-2026-07-19.md` — Layer A/B/C/D background
- `/root/A-FORGE/forge_work/2026-07-19/QUOTE-REGISTRY-UNIFICATION-RECEIPT-2026-07-19.md` — Path Y follow-up after b953eef8f