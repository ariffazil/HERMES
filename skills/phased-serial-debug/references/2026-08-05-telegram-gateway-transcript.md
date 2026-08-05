# phased-serial-debug — Live Transcript References

Session-specific transcripts and reproduction recipes for the phased-serial-debug pattern.

## 2026-08-05 — Telegram gateway IPv6 hang (canonical example)

**Symptom:** `@ASI_arifos_bot` not replying in Telegram. Service crash-looping every 22s-3min.

**Phases applied:**

1. **Phase 1 — stop bleeding:** Changed `RestartSec=5` → `30` in `/etc/systemd/system/hermes-asi-gateway.service`. Log spam reduced.

2. **Phase 2 — isolate layer:** Ran 4 layer tests sequentially:
   - `curl https://api.telegram.org/bot<TOKEN>/getMe` → HTTP 200 in 0.5s ✅
   - Python `httpx.Client().get(...)` → 0.52s ✅
   - Python `telegram.Bot(token=...).get_me()` → 0.51s ✅
   - `socket.getaddrinfo('api.telegram.org', 443)` → returned BOTH IPv4 and IPv6

   Conclusion: network+Python OK, but IPv6 attempts present. Suspect Layer 1.

3. **Phase 3 — propose + review (×2):**

   First patch proposed: `HERMES_TELEGRAM_DISABLE_FALLBACK_IPS=1` env var.
   User approved, applied, restarted. **Patch had NO EFFECT** — env check at line 3133, but DoH discovery runs at line 3124 BEFORE the check. Dead code.

   Second patch proposed: `/etc/gai.conf` IPv4 precedence (`precedence ::ffff:0:0/96 100`).
   User approved, applied via `sudo tee -a`. Verified with `socket.getaddrinfo` → IPv4 only.

4. **Phase 4 — apply + verify:** After gai.conf patch, initial memory dropped 285M → 113M. Restart cycle slowed 22s → 1-2min. **Connection still stuck at "Connecting (1/8)" — partial fix.**

5. **Phase 5 — revert dead code:** Reverted DoH env var patch + adapter.py patch (created `.bak-20260805-DoH-fix`). Kept gai.conf + force_ipv4 config.

6. **Phase 6 — honest report:** Reported residual state — gateway still cycles, Layer 3 (fd leak / async) suspected, needs upstream fix.

**Lessons captured:**

- **Layer 1 IPv6 force was partial, not complete.** Earlier skill wrongly claimed it as the complete fix.
- **Env var check ordering bug** in adapter.py is a recurring pattern (env checked AFTER action).
- **Systemd's `RestartSec` is a tool, not a fix.** Stop bleeding ≠ fix root cause.
- **Strace on wrong PID** — re-fetch `MainPID` immediately before attach.
- **Memory peak 285M ≠ OOM.** Check cgroup `oom_kill` counter for real OOM.

**Time spent:** ~50 minutes across 6 phases. Without phased-serial, would have batched all patches and never known which mattered.

## Reusable Probes (for future sessions)

```bash
# Layer-by-layer network probe (paste into a function)
probe_layers() {
  local TOKEN="$1"
  echo "=== L1: direct curl ==="
  time curl -sf "https://api.telegram.org/bot${TOKEN}/getMe" --max-time 10 -o /dev/null
  
  echo "=== L2: Python httpx ==="
  python3 -c "
import httpx, time
s = time.time()
r = httpx.Client(timeout=10).get('https://api.telegram.org/bot/${TOKEN}/getMe')
print(f'  {time.time()-s:.2f}s')
" 2>&1
  
  echo "=== L3: getaddrinfo family ==="
  python3 -c "
import socket
for a in socket.getaddrinfo('api.telegram.org', 443, type=socket.SOCK_STREAM):
    print('  ', a[4][0])
" 2>&1
  
  echo "=== L4: systemd service state ==="
  systemctl status hermes-asi-gateway.service --no-pager 2>&1 | grep -E "Active|Main PID|Memory"
  
  echo "=== L5: cgroup OOM events ==="
  cat /sys/fs/cgroup/system.slice/hermes-asi-gateway.service/memory.events 2>&1 | grep oom_kill
}

probe_layers "${ASI_BOT_TOKEN}"
```

## Pattern: when to stop and ask

If after Phase 2 you have 3+ candidate root causes, don't immediately patch all of them. Instead:
- Rank by probability
- Patch #1 (most likely) — verify
- If no effect, REVERT and patch #2 — verify
- If no effect, REVERT and ESCALATE ("I have evidence X but patches Y/Z didn't work; either root cause is deeper or my hypothesis is wrong")

This is the difference between efficient debugging and thrashing. The 2026-08-05 session ended with 2 working fixes (gai.conf + force_ipv4) and 1 dead-code revert (env var), not 3 mystery patches that didn't help.