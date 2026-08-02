# Phantom Writer — Code Corruption in server.py (2026-08-02)

The recurring phantom that rewrites `state.json` with TEST/mock data can ALSO
corrupt the WELL **code** — not just state. This reference documents the exact
failure signature, the /proc watcher used to catch it, and the git-restore
recovery that brought the organ back.

## Incident Summary

- **Time:** 2026-08-02, ~10:13–10:24 UTC
- **Effect:** `well.service` crash loop (restart counter 18), port 18083 gave
  `connection refused (000)`, AAA dependency showed `UNREACHABLE` 503 loop.
- **Journalctl root cause:**
  ```
  File "/root/WELL/server.py", line 12578
      @mcp.tool()
      ^
  SyntaxError: expected 'except' or 'finally' block
  ```
- **Underlying cause:** A new `well_system_pulse` `@mcp.tool()` function had
  been appended whose tail was an **orphaned, dedented block**:
  ```python
  return pulse
          except Exception:
              pass
          return envelope
  ```
  Those three extra lines (`except Exception: pass return envelope`) were a
  leftover from the preceding wrapper function (`_well_wrap_envelope`). They
  broke the enclosing `try:` block and produced the SyntaxError at the
  decorator.

## Diagnostic Signature

- `python3 -m py_compile server.py` (or `ast.parse`) errors **at the line of a
  `@mcp.tool()` decorator** with `expected 'except' or 'finally' block`.
- This means an enclosing `try:` had its body mangled by a **trailing orphaned
  `except`/`finally`** — distinct from a merge-conflict SyntaxError (which
  leaves `<<<<<<<` markers; this one leaves a "clean" tree with a broken
  function).
- `git diff server.py` shows the injected block as `+@mcp.tool()` +
  `+def well_system_pulse(...)` ending in the orphaned tail
  (`+ return pulse`, `+ except Exception:`, `+ pass`, `+ return envelope`).

## Why It Is Hard to Grep

- `grep` for writers of `environment = "TEST"` in `server.py` finds only the
  enum / purity-checkers — NOT the writer. The injected function does not
  touch state.json; it is a health-probe tool. The code corruption is
  orthogonal to the state corruption.
- The `/proc` watcher that catches the state.json writer may also catch the
  same process opening/holding open files — but the broader takeaway is: **do
  not assume the phantom only touches state; re-verify server.py still parses
  whenever state corruption recurs.**

## Recovery (serial: one change -> one verify -> next)

```bash
# 1. Backup the corrupt file for forensics
cp server.py /tmp/server.py.broken-phantom

# 2. Restore the committed (known-good) version. The phantom touched BOTH
#    server.py and src/server.py — restore both.
git checkout -- server.py src/server.py

# 3. Verify it parses BEFORE restarting
python3 -c "import ast; ast.parse(open('server.py').read()); print('PARSES OK')"
# (Also confirmed the committed HEAD version parses; the working tree was the
#  only broken copy.)

# 4. Restart and confirm health + AAA re-registration
systemctl restart well.service
curl -s -o /dev/null -w 'WELL -> HTTP %{http_code}\n' http://127.0.0.1:18083/health
journalctl -u well.service --no-pager -n 20 | grep -i registered
# Expected: status=active, HTTP 200, "[register] well: REGISTERED with AAA"
```

`git checkout --` is safe here because a committed good revision exists and
the broken code was UNCOMMITTED working-tree pollution. If the injection were
committed, prefer `git revert`/`git restore` the specific commit instead.

## Race Condition With Sibling/Agent Writes

While diagnosing, watch the file for active modification:
```bash
ls -la server.py            # size/mtime chang‌ing under you = active writer
```
A `file modified by sibling subagent ... after this agent's last read` warning
plus a changing byte count means another process is writing concurrently. On a
crash-loop recovery, restore the good version and restart FIRST (get the organ
green), then hunt the writer.

## Watcher (state.json) Still Authoritative for the Writer

The `/tmp/well_state_watcher.py` pattern — poll `/proc/*/fd` every ~150ms and
log PID + cmdline of anyone holding `state.json` open — remains the definitive
way to name the phantom. Note: `hermes-gateway-secure.sh` is the QUARANTINER
(it moves TEST -> state.test.json), NOT the contaminator — do not misattribute
it.