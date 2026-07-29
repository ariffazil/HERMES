# Nested Quote + Inline Comment Bug — OpenCode JSONC Parse Death

## Symptom

OpenCode boots, loads config, then crashes with JSON parse error.
24/24 MCP tools show "disconnected" in the TUI.
Config file looks syntactically valid when opened on its own.

## Root Cause

A vault value like:
```
export OPENROUTER_API_KEY='"sk-or-…"  # arifOS-federation — zen org key'
```

When OpenCode (or any tool with `env:` expansion in JSONC config) expands
`${OPENROUTER_API_KEY}` into a JSONC config value, the shell expands the
variable including its outer quotes, producing:
```jsonc
{
  "apiKey": ""sk-or-…"  # comment"    // ← INVALID JSONC
}
```

The double-double-quote `""` + inline `# comment` + trailing text after
the closing quote makes this unparseable. JSONC accepts `#` as comments
only at line boundaries, not inline.

## Fix

1. Clean the vault value — remove all quoting and comments:
```bash
# BEFORE
export OPENROUTER_API_KEY='"sk-or-…"  # arifOS-federation-20260724 — zen org key'

# AFTER
export OPENROUTER_API_KEY="sk-or-…"
```

2. Regenerate flat env:
```bash
cd /root/.secrets
python3 generate-flat.py
```

3. Restart the tool (systemd service for OpenCode):
```bash
systemctl restart opencode.service
```

## Prevention

When adding any key to kunci-mas.env:
- Format: `export KEY="value"` — single pair of outer quotes
- NO inline comments in the value field (put comments ABOVE the line)
- NO nested double-quotes inside the value
- NO trailing text after the closing quote

```bash
# ✅ CORRECT
# arifOS federation OpenRouter key, rotated 2026-07-24
export OPENROUTER_API_KEY="sk-or-..."

# ❌ WRONG — nested quotes + inline comment
export OPENROUTER_API_KEY='"sk-or-..."  # comment'

# ❌ WRONG — trailing text after quote
export OPENROUTER_API_KEY="sk-or-..." some text
```

## Detection Script

```bash
# Find vault values with problematic patterns
grep -n '"[^"]*".*#' /root/.secrets/kunci-mas.env  # nested quotes + comments
grep -n '"[^"]*" .*"' /root/.secrets/kunci-mas.env  # trailing text after closing quote
```
