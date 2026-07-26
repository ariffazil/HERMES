# Kernel Permission Fixes (2026-07-12)

## .env Permission Denied

**Symptom:** Kernel crashes on startup:
```
PermissionError: [Errno 13] Permission denied: '.env'
```

**Root cause:** The service runs as `arifos` user, but `.env` was owned by `ariffazil` (mode 600).

**Check:**
```bash
ls -la /opt/arifos/app/.env
```

**Fix:**
```bash
chown arifos:arifos /opt/arifos/app/.env
chmod 640 /opt/arifos/app/.env
systemctl restart arifos
```

**Verify:**
```bash
journalctl -u arifos --no-pager -n 10 --since "2 minutes ago" | tail -5
curl -sf http://127.0.0.1:8088/health | python3 -c "import sys,json;r=json.loads(sys.stdin);print(f'OK: {r[\"version\"]}')"
```

**If other files also have the same problem (recursive fix):**
```bash
chown -R arifos:arifos /opt/arifos/app/
```

## vault_registry.py Permission Denied

**Symptom:** After fixing `.env`, the next crash is:
```
PermissionError: [Errno 13] Permission denied: 'vault_registry.py'
```

**Root cause:** Same issue — all files in `/opt/arifos/app/` are owned by `ariffazil` but the service runs as `arifos`.

**Fix:** Same recursive chown as above, then restart:
```bash
chown -R arifos:arifos /opt/arifos/app/
systemctl restart arifos
```

## Service User Check

```bash
grep "^User=" /etc/systemd/system/arifos.service
# Returns: User=arifos
```
