# `grep -c` + `set -euo pipefail` — Double-value Reproduction Recipe

Reproduced and fixed on af-forge VPS, 2026-07-27, during the SOT-banner refactor.

## Conditions

- bash with `set -euo pipefail`
- `grep -c PATTERN` where PATTERN has ZERO matches in the input
- Command substitution: `VAR=$(... || echo 0)`

## Reproduction

```bash
set -euo pipefail

output="line1
line2
line3"

# Simulating: no ❌ emoji in output, so grep -c returns 0 matches (exit code 1)
# BROKEN:
result=$(echo "$output" | grep -c '❌' || echo 0)
echo "$result" | cat -A
# Prints: 0^J0$
# Two "0"s separated by newline — because grep -c already printed "0" to stdout,
# and the || echo 0 fallback printed another "0"

# FIXED:
result=$(echo "$output" | grep -c '❌' || true)
echo "$result" | cat -A
# Prints: 0$
# Single "0" — || true suppresses exit code without adding extra value
```

## Root cause

1. `grep -c` always prints the count to stdout (including "0")
2. `grep -c` exits with code 1 when count is 0 (no matches)
3. With `set -o pipefail`, the pipeline exits with code 1
4. Inside `$()`, the `||` catches exit code 1, but stdout already captured "0"
5. `echo 0` appends another "0\n", captured by `$()`
6. Result: `"0\n0"` — silently broken in JSON, arithmetic, and string comparisons

## Why `|| true` works

`grep -c` already emitted "0" to stdout before exiting. `true` exits 0 without writing anything. So `$()` captures only what `grep -c` actually printed: a single "0".

## Affected commands

Any command that:
- Prints a result to stdout on success
- Exits non-zero on "zero-results" or "empty" conditions

Common examples: `grep` (with `-c`, `-l`, or bare), `wc -l` on empty, `find` with no matches, `awk` BEGIN patterns that exit early.

## Prevention

Always use `|| true` (not `|| echo <default>`) when the command already prints its result to stdout. For commands that DON'T print on zero-results, use a pattern that separates fallback from stdout capture:

```bash
# Command prints nothing on zero-results
result=$(some_command || true)
result="${result:-0}"
```
