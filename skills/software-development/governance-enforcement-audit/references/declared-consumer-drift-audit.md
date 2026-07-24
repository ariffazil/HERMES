# Declared-Consumer Drift Audit

**Sub-pattern of Governance Enforcement Audit.** When a governance table (JSON, YAML, or markdown) declares consumers with specific contractual mandates, write a targeted audit script that checks each consumer independently for drift against the canonical source of truth.

## When to Use

- A governance table (e.g., `FLOOR_TABLE.json`, constitution, agent card registry) lists downstream consumers with specific contractual obligations
- You need to verify that each consumer actually honors its declared mandate
- You want a repeatable, exit-code-gated audit that can run in CI or as a pre-commit hook

## Core Pattern

### 1. Identify the Consumer List

The governance table declares a `consumers` array:

```json
"consumers": [
  {"name": "AAA AGENTS.md", "path": "/root/AAA/AGENTS.md", "must": "render F1–F13 names ..."},
  {"name": "Wealth.tsx",    "path": ".../Wealth.tsx",          "must": "F7 = HUMILITY ..."}
]
```

Extract the consumer list with path + mandate for automated checking.

### 2. Build Per-Consumer Checks

Each consumer gets a dedicated check function. Design checks to detect known drift modes:

| Drift Mode | Example | Detection |
|---|---|---|
| **Missing content** | Consumer doesn't render F1-F13 names | Regex for floor names |
| **Wrong name/label** | F9 rendered as "ANTI-CASCADE" instead of "ANTIHANTU" | Name comparison against canonical |
| **Wrong color** | F9 color #3B82F6 vs canonical #FF003C | Color hex comparison |
| **Deprecated values** | 0.90 confidence cap instead of Ω₀ ∈ [0.03, 0.05] | Regex for old values |
| **Structural gap** | No SPEC→SEAL rejection gate in state machine | Schema/state-machine inspection |
| **Missing bridge** | F6 bridge (MARUAH ⇄ EMPATHY) not rendered | Keyword search |
| **Canonical path dead** | Consumer path in table doesn't exist on disk | `Path(path).exists()` |

### 3. Add Independent Verification Notes

Even drift-detected consumers may have sub-checks that pass:
- `evidence_chip emits correct four band names ✓`
- `Reads FLOOR_TABLE dynamically ✓`

Separate positive verification notes from actual drift findings.

### 4. Check CLAUDE.md Seal Propagation

The governance table itself may have been sealed (e.g., VAULT999 chain, EUREKA architecture seal). Check:

1. Does root `CLAUDE.md` reference the seal or architecture seal date?
2. Does the system's `CLAUDE.md` delegate floor references to `AGENTS.md`?
3. Do per-organ `CLAUDE.md` files reference the floors at all?
4. Is the seal receipt file (`forge_work/.../xyz-seal.md`) present on disk?

Seal propagation means the governance table's authority is visible to boot-time agent instructions.

### 5. Exit Code Design

| Code | Meaning | Use Case |
|---|---|---|
| **0** | All consumers in-sync | CI green, pre-commit passes |
| **1** | Drift detected in one or more consumers | Non-blocking alert, investigation needed |
| **2** | Structure error (missing table, parse failure) | Blocking — governance table itself is broken |

### 6. Output Format

Dual output:
- **Markdown** for human reading (headings, tables, emoji status icons)
- **JSON** for machine parsing (CI pipeline, dashboard ingestion, structured `consumers[]` array with per-issue arrays)

Include a JSON summary at end of markdown report wrapped in ` ```json ` block so both formats appear in a single stdout stream.

## Worked Example: FLOOR_TABLE Consumer Drift Audit

A complete, stdlib-only implementation is at:

**`/root/arifOS/scripts/audit_floor_consumers.py`**

This script audits the arifOS constitutional floor table's 4 declared consumers:

### Checks Performed

| Consumer | Mandate Check | Drift Detected (2026-07-25) |
|---|---|---|
| AAA AGENTS.md | Render F1–F13 names verbatim, cite Ω₀, F6 bridge | ❌ No floor rendering, no Ω₀, no F6 bridge |
| Wealth.tsx | F7=HUMILITY (not STEWARDSHIP), F2 band chips | ❌ F9 is "ANTI-CASCADE" (#3B82F6) not "ANTIHANTU" (#FF003C) |
| wealth-static-renderer | evidence_chip emits 4 bands, Ω cap | ❌ F9 color #3B82F6 vs canonical #FF003C (2 locations) |
| GEOX claim workflow | Reject SPEC claims as SEAL-worthy | ❌ No SPEC→SEAL gate in state machine or schema |
| **CLAUDE.md seal** | Propagation across federation | ✅ SEAL_PROPAGATED — all 3 CLAUDE.md files reference floor seal |

### Drift Summary (from 2026-07-25 run)

All 4 consumers had drift. The most common drift class was **F9 color drift** (3 of 4 consumers had wrong F9 color #3B82F6 instead of canonical #FF003C). The AAA AGENTS.md had the most severe drift — it is declared as a consumer but is in fact a 7-line pointer file that renders zero floor definitions.

The GEOX claim workflow path was also declared as `/root/arifOS/contracts/...` which does not exist — the path resolved to `/root/GEOX/contracts/`.

## Pitfalls

1. **Don't assume a consumer is "present" because its file exists.** The file may exist but be a thin pointer (7 lines) that doesn't actually render the declared content. Check content, not just existence.
2. **Don't conflate "file reachable" with "content compliant".** Track both separately. A file may be reachable but have zero compliance.
3. **Color drift is the most subtle and most common.** Three different developers can pick three different shades for the same concept. Always compare consumer colors against canonical table colors.
4. **The declared path in the governance table may be stale.** Resolve to actual locations on disk (e.g., `/root/arifOS/contracts/...` → `/root/GEOX/contracts/`). Report the resolution as a finding.
5. **A positive sub-check (e.g., "reads FLOOR_TABLE dynamically ✓") does not clear the consumer.** A consumer can have mixed results — some sub-checks pass, some fail. Report both independently.
6. **Exit code 2 (structure error) must be reserved for the governance table itself.** A missing consumer file is drift (exit 1), not structure error. Only a broken or missing FLOOR_TABLE.json is exit 2.
7. **JSON output must be valid even on error paths.** The script must never crash without producing parseable output. On structure error, emit JSON with `status: "ERROR"` and the error message before `sys.exit(2)`.
