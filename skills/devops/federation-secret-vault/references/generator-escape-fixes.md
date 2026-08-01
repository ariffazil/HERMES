# Generator Escape Fixes — 2026-08-01 rewrite of generate-flat.sh

Session: Hermes config chaos ("fix and zen with qwen token plan") surfaced
three PRE-EXISTING generator bugs (latent since Jul 29) plus one CLI trap.
All fixed in one pass; this file is the reproduction + fix recipe.

## Bug 1 — bash-escape double-escape (`\$` → `\\$`)

SOT (correct, bash-sourced truth):
```
export ARIFOS_SOVEREIGN_BASIC="arif:\$apr1\$cF7b4sJb\$KwnUfERyprT5xi706tQ5W."
```
Bash `source` runtime value: `arif:$apr1$cF7b4sJb$KwnUfERyprT5xi706tQ5W.` (no backslashes)

Every flat generation since Jul 29 (BOTH .py and .sh):
```
ARIFOS_SOVEREIGN_BASIC="arif:\\$apr1\\$cF7b4sJb\\$KwnUfERyprT5xi706tQ5W."
```
systemd unescapes one layer → runtime `arif:\$apr1\$...` — backslashes
injected into a sovereign credential. Latent: no code consumed the var
yet, but any future consumer breaks silently.

Why .py failed too: `raw_val.encode().decode("unicode_escape")` does NOT
decode `\$` (not a valid escape in that codec — backslash survives), then
its `val.replace("\\", "\\\\")` quoting doubled the surviving backslash.

## Bug 2 — inline-comment swallowing

SOT:
```
export EMBEDDING_BACKEND="dashscope"        # dashscope | ollama | hash | auto
```
Greedy `(.*)` in .sh AND non-greedy `(.*?)` in .py both captured up to
line end → flat value `dashscope"  # dashscope | ollama | hash | auto`.
The .py's `["\']?\s*$` suffix didn't anchor because the comment follows
the closing quote.

## Bug 3 — write-before-verify corruption

.sh wrote `$FLAT` THEN ran the drift check → on failure the corrupt flat
was already on disk; a gateway restart between write and failure loads
corrupt values. Proven in-session: failed .sh run wrote the corrupt flat
at 11:25, gateway restarted 11:25:48 with it.

## Fix — rewritten generate-flat.sh

Key elements (full file at /root/.secrets/generate-flat.sh):

1. `decode_val()` applied in generation AND drift-check:
```bash
decode_val() {
    printf '%s' "$1" | sed -e 's/\\\$/\$/g' -e 's/\\\\/\\/g' -e 's/\\"/"/g'
}
```
2. Single-pass parse into `declare -A KV`:
   - double-quoted: `val="${rest#\"}" ; val="${val%%\"*}"` (stops at CLOSING quote, drops comment)
   - single-quoted: same with `'`
   - unquoted: `val="${rest%%[[:space:]]#*}"` then trim trailing spaces
3. Atomic write: generate to `$FLAT.tmp-$$`, run ALL checks on the tmp,
   `mv -f` on success, `rm -f` on failure.
4. Drift check compares `${KV[$key]:-}` (empty-safe) vs decoded flat
   value — NOT `${KV[$key]:-__MISSING__}` (empty values false-drift).
5. Key-count check on the tmp before move.

## verify-vault.py alignment

The CI verifier's `parse_sot` had the same greedy-regex + no-decode bug;
it compared SOT raw-escaped vs FLAT decoded → 4 false drifts AFTER the
generator was fixed. parse_sot must mirror generator semantics:
- `rest = m.group(2).lstrip()`
- quoted → `rest[1:].split('"',1)[0]` / `split("'",1)[0]`
- unquoted → `rest.split(" #",1)[0].rstrip()`
- decode: `val.replace("\\$","$").replace('\\"','"').replace("\\\\","\\")`

## Hex verification method (sed/grep ambiguous with backslashes)

```bash
grep '^ARIFOS_SOVEREIGN_BASIC' kunci-mas.flat.env | xxd | head -3
grep '^export ARIFOS_SOVEREIGN_BASIC' kunci-mas.env | xxd | head -3
bash -c 'source /root/.secrets/kunci-mas.env && printf "%s\n" "$ARIFOS_SOVEREIGN_BASIC"' | xxd | head -3
```
The bash-sourced value IS the runtime truth the flat must reproduce.
Expected hex: SOT `5c 24` (\$), FLAT `24` ($), bash truth `24` ($).

## CLI trap — `hermes config set` and list values

`hermes config set fallback_providers '[{...json...}]'` stores the JSON as
a quoted string (CLI only coerces scalars; `_set_nested` won't grow
lists). Fix by direct python YAML edit + validate:
```python
import yaml
c = yaml.safe_load(open('/root/.hermes/config.yaml'))
c['fallback_providers'] = [...]  # proper list
# atomic write, chmod 600
```
Note the `patch` tool refuses Hermes config.yaml (security guard) — the
guard message itself points to "edit directly or use hermes config".

## Related (same session)

- Seat placeholders: grep `PASTE_` in SOT; seats.yaml = seat→env_var map.
- Seat quota-dead (`insufficient_quota`) ≠ key invalid — test live
  completions per seat; rewire key_env to a live seat; rotation is F11/Arif.
- Makefile must point at the ONE live generator (`@bash .../generate-flat.sh`).
