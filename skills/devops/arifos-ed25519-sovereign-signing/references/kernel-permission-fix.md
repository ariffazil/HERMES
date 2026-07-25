# Kernel Permission Fixes (2026-07-12, updated 2026-07-25)

## .env Permission Denied (2026-07-12)

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

## DID Registry Permission Denied (2026-07-25 — CRITICAL)

**Symptom:** `arif_judge` returns `ESCALATE` with F13 even when a valid Ed25519 signature is provided. The journal shows:
```
F13_ED25519: challenge exception=[Errno 13] Permission denied: '/root/secrets/did/registry.json'
F13_ED25519: free_nonce_exception=[Errno 13] Permission denied: '/root/secrets/did/registry.json'
```

**Root cause:** `resolve_actor_public_key()` in `crypto_auth.py` tries to read `/root/secrets/did/registry.json`. The arifOS service runs as user `ariffazil` (or `arifos`) who cannot traverse `/root/` (mode 700). The PermissionError propagates as an unhandled exception, making `_verify_sovereign_token()` always fail.

**Diagnostic:**
```bash
sudo -u ariffazil cat /root/secrets/did/registry.json > /dev/null 2>&1 && echo "✅ readable" || echo "❌ NOT readable"
```

**Fix options:**

**Option A — File permissions (quick):**
```bash
chmod o+x /root /root/secrets
chmod o+r /root/secrets/did/registry.json
```

**Option B — Code resilience (applied 2026-07-25, crypto_auth.py line 162):**
```python
try:
    text = reg_path.read_text(encoding="utf-8")
except (PermissionError, OSError) as exc:
    logger.debug("DID registry path inaccessible: %s — %s", reg_path, exc)
    continue
```

**Option C — Both (recommended):** Apply both fix A and B. The code fix prevents future regressions; the permission fix ensures the key resolution works even from the DID path.

**Verify fix:**
```bash
systemctl restart arifos
journalctl -u arifos --since "30 sec ago" --no-pager | grep -i 'F13_ED25519'
# Should show: challenge_verify=True or pubkey_found=True
```

## vault_registry.py Permission Denied (2026-07-12)

**Symptom:** Same issue — all files in `/opt/arifos/app/` are owned by `ariffazil` but the service runs as `arifos`.

**Fix:**
```bash
chown -R arifos:arifos /opt/arifos/app/
systemctl restart arifos
```

## Service User Check

```bash
grep "^User=" /etc/systemd/system/arifos.service
# Returns: User=arifos
```