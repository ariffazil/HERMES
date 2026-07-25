# OpenCode Forge Submission Pattern

> **DITEMPA BUKAN DIBERI** — Submit governed forge prompts, not vague requests.
> **Origin:** 2026-07-25 arifFlow Phase 2 session
> **Lesson learned:** Always probe for existing compiled implementations before writing specs. If a Rust binary exists with 24 tests, your prompt must say EXTEND, not REWRITE.

---

## When to Use This Pattern

You have a forge-ready spec (canonical doc, invariants, data models, state machine) that needs implementation by OpenCode — the federation's coding actuator.

**Do NOT use when:**
- The task is trivial and can be done directly (single file edit, fix, test)
- The task is a question or analysis (use delegation)
- The task needs human review first (submit to Arif via DM, not OpenCode)

## Steps

### Step 1: Prepare the Spec

Before submitting, ensure:
- Canonical document exists (e.g., `ARIFLOWKERNELCANON.md` — invariants A1-A5)
- Unified spec exists (e.g., `UNIFIED_SPEC_v1.md` — existing code + gap analysis)
- Extend-not-rewrite prompt file exists (`arifflow-extend-prompt.md`)

**Critical: probe for existing code first:**
```bash
# Check for existing binary
find /root -name "target" -type d -maxdepth 3 2>/dev/null
ls /root/arifFlow/target/release/ariflow 2>/dev/null

# Check test counts
grep -c "#\[test\]" /root/arifFlow/src/*.rs /root/arifFlow/src/**/*.rs 2>/dev/null

# Check if there's an adapter
ls /root/A-FORGE/domain/orchestration/arifFlow_adapter.py 2>/dev/null
```

If a compiled binary exists with tests passing, your prompt must say **EXTEND NOT REWRITE**. Two specs = two schedulers = governance violation.

### Step 2: Write the Extend-Only Prompt

Write a prompt file with these sections:

1. **Preface** — "Your task is NOT to rewrite. Your task is to EXTEND existing code."
2. **Existing code inventory** — List every file that exists and should NOT be changed
3. **Features to implement** — Only additive work. Each feature: file path, what to add, what NOT to change.
4. **Governance rules** — A1-A5 or other invariants. Mandatory.
5. **Tests to generate** — Per-feature
6. **Output** — What files will be produced

### Step 3: Submit via opencode_manager

```bash
cd /root/A-FORGE/forge_work && python3 opencode_manager.py spawn \
  --task "EXTEND existing X — NOT rewrite. See /path/to/prompt.md for full spec. Features: 1)..., 2)..., 3)..." \
  --actor "arif-888" \
  --authority "OPERATOR"
```

**Arguments:**
- `--task`: Concise summary (OpenCode sees this first). Reference the full prompt file.
- `--actor`: Who requested it (e.g., `arif-888`, `hermes`, `333-AGI`)
- `--authority`: `OPERATOR` (standard) or `CIVILIZATION` (requires 888_HOLD token)

### Step 4: Verify Submission

Check the spawn receipt:
```json
{
  "session_id": "forge-e992be6b",
  "pid": 701258,
  "verdict": "SPAWNED",
  "authority_class": "OPERATOR",
  "f1_f13_status": "intact"
}
```

### Step 5: Post-Submission Tests

After OpenCode completes, run the 3 production gates before 888-HOLD can be lifted:

| Gate | Test | Pass condition |
|------|------|----------------|
| FFI stability | N calls to adapter → arif_judge → verdict | 0 failures |
| Verdict timeout | Kill arifOS, run step, measure time to HOLD | < 15s |
| Crash recovery | Kill Rust mid-run, restore checkpoint, verify authority re-checked | Successful resume |

## Pitfalls

- **Do NOT write a complete replacement spec when a compiled binary exists.** The AAA G1 BSP spec proposed a TypeScript scheduler from scratch. But `/root/arifFlow/target/release/ariflow` existed with 24 tests. The correct architecture: Rust stays as substrate, Python bridges as conduit, TypeScript wraps as surface. One spec, three layers, zero confusion.
- **Do NOT submit to Telegram DM or AAA group for execution.** OpenCode is the coding actuator. Telegram is for governance humans. AAA group is for governance discussion, not execution prompts.
- **Do NOT use CIVILIZATION authority class without 888_HOLD token.** The manager will reject the spawn.
- **Verify after submission** — check `opencode_manager.py list --active-only` to confirm the session is running
