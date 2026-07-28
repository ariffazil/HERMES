# MOTD as Federation Health Surface — Golden-Hash RSI

> **What:** A self-auditing MOTD (Message of the Day) that renders live State-of-Truth on every SSH login, then checks its own freshness against a golden hash.

## Architecture

The MOTD (`/etc/update-motd.d/05-arifos`) is a **self-contained bash script** that:

1. **Renders live probes** — no cached data, no stale state files
2. **Displays all 6 organ health states** — from the real `/health` endpoints
3. **Shows kernel constitutional state** — SEALED/UNSEALED from `curl :8088/health | jq .state_axes.receipt_state`
4. **Reports git SHAs for all 6 governing repos** — from `.git/refs/heads/main`
5. **Shows phone node count** — from `authorized_keys` grepping
6. **Displays a context-aware init prompt** — `arif_think` if UNSEALED, `arif_init` if SEALED
7. **Self-audits** via the RSI golden-hash loop

### Golden-Hash RSI Loop

The MOTD checks its own `md5sum` against a `GOLDEN_HASH:` annotation in the companion reference document (`/root/AAA/governance/001_MOTD_RSI.md`):

```
File: /etc/update-motd.d/05-arifos       (live MOTD)
      /root/AAA/governance/001_MOTD_RSI.md  (RSI reference)

MOTD computes: md5sum /etc/update-motd.d/05-arifos
RSI doc contains: GOLDEN_HASH: f5d4d8381dde8cfb88bbeb1ad63f59f8

If mismatch → footer warns and suggests update
If match    → footer reports "MOTD fresh"
```

**Protocol:**
1. Every SSH login: MOTD renders → checks own hash against golden → reports match/mismatch
2. If mismatch: human or agent must verify the MOTD output against intent, then update `GOLDEN_HASH:` in the RSI doc
3. The golden hash is the **intent anchor** — it represents "the version that matched the spec"

### Organ Probe Pattern

```bash
check_organ() {
  local name="$1" port="$2" path="$3"
  local result
  result=$(curl -sf --max-time 2 "http://127.0.0.1:${port}${path}" 2>/dev/null)
  if [ -n "$result" ]; then
    local st=$(printf '%s' "$result" | jq -r '.status // "healthy"' 2>/dev/null)
    # s/healthy → green ●, /degraded → yellow ●
    printf "${G}●${X} %s  (%s)\n" "$name" "$st"
  else
    printf "${R}●${X} %s  (unreachable)\n" "$name"
  fi
}

check_organ "arifOS"  8088  "/health"
check_organ "A-FORGE" 7071  "/health"
check_organ "AAA"     3001  "/health"
check_organ "GEOX"    8081  "/health"
check_organ "WEALTH"  18082 "/health"
check_organ "WELL"    18083 "/health"
```

### Kernel State Extraction

```bash
KSTATE=$(curl -sf --max-time 3 http://127.0.0.1:8088/health 2>/dev/null)
STATE=$(printf '%s' "$KSTATE" | jq -r '.state_axes.receipt_state // "UNKNOWN"')
VERDICT=$(printf '%s' "$KSTATE" | jq -r '.thermodynamic.verdict // "?"')
VITALITY=$(printf '%s' "$KSTATE" | jq -r '.thermodynamic.vitality_index // "?"')
EXEC=$(printf '%s' "$KSTATE" | jq -r '.execution_readiness // "?"')
FLOORS=$(printf '%s' "$KSTATE" | jq -r '.floors_active // "?"')
```

### Context-Aware Init Prompt

```bash
if [ "$STATE" = "SEALED" ]; then
  printf "🔒 SEALED — forge actions require arif_init\n"
  printf "arif_init --actor Arif --mode init --authority OBSERVE_ONLY\n"
else
  printf "🔓 UNSEALED — session authority: OBSERVE_ONLY\n"
  printf "arif_think --mode reason --query '<your intent>'\n"
  printf "Or for a full init: arif_init --actor Arif --mode light\n"
fi
```

### Git SHA Extraction

```bash
git_sha() {
  local dir="$1" label="$2"
  if [ -d "/root/${dir}/.git" ]; then
    sha=$(cat "/root/${dir}/.git/refs/heads/main" 2>/dev/null | cut -c1-7)
    printf "⌘ ${label}  %s\n" "${sha:-???}"
  fi
}

git_sha "arifOS"  "arifOS"
git_sha "A-FORGE" "A-FORGE"
git_sha "AAA"     "AAA"
git_sha "GEOX"    "GEOX"
git_sha "WEALTH"  "WEALTH"
git_sha "WELL"    "WELL"
```

## Timing & Safety

- **Timeout killer:** `trap cleanup EXIT` with `kill $BACKGROUND_PID` — total cap 8s
- **All failures silent:** Every external command suffixed with `2>/dev/null`
- **ANSI only:** No `tput`, no `ncurses`, no external dependencies beyond `bash`, `curl`, `jq`, `coreutils`

## RSI Contract with Sessions

The companion document (`001_MOTD_RSI.md`) defines the recursive improvement cycle:

```
SSH Login → MOTD renders
    ↓
MOTD footer checks own freshness:
  • hash vs GOLDEN_HASH in RSI doc
  • age since last modification
  • render performance (from /var/run/motd_perf.log)
    ↓
If stale/drifted → SUGGEST improvement
    ↓
Session (arif_init → arif_think) reads RSI doc → proposes patch
    ↓
Patch applied → MOTD updated → golden hash updated
    ↓
Next SSH login shows fresh MOTD
```

## Pitfalls

- **`%` in bash printf:** `df /` output includes `%` in the usage column (e.g., `44%`). When passed to `printf`, `%` is interpreted as a format specifier. Fix: strip the `%` with `gsub(/%/,"")` in awk, then add `%%` in the printf format string.
- **kernel response can be large (~15KB):** Capture once with `curl -sf --max-time 3` and reuse via variable. Don't call curl multiple times for different jq extracts.
- **SSH banner vs MOTD:** SSH has two layers — the server banner (static text in sshd_config) and PAM MOTD (run-parts scripts). If `PrintMotd no` in sshd_config, the compiled `pam_motd.so` still runs `run-parts /etc/update-motd.d/`. Verify both.
- **Newline at end:** MOTD must end with `exit 0` and a final newline. Some `run-parts` implementations are strict.
