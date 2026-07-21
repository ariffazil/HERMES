# GEOX Dual-Repo Case-Collision Diagnostic

> **Pattern identified:** 2026-07-20 | **Session:** Scar Shadow / GLM 5.2
> **Root cause:** Case-sensitive path collision — `GEOX` vs `geox` with systemd running one, AGENTS.md declaring the other, and a `path-geox-casefix.conf` override bridging them.

## Detection Signature

```bash
# Two independent git trees with overlapping history
diff <(cd /root/GEOX && git log --oneline -10) <(cd /root/geox && git log --oneline -10)

# systemd runs uppercase
systemctl cat <service> | grep WorkingDirectory
# → WorkingDirectory=/root/GEOX

# But AGENTS.md declares lowercase
grep "scope:" /root/GEOX/AGENTS.md
# → scope: /root/geox

# Casefix override confirms the drift
cat /etc/systemd/system/<service>.service.d/path-geox-casefix.conf
# → "live tree is /root/GEOX (case). /root/geox path absent → restart would fail."
```

## Resolution

**Option A (recommended when systemd is live):** Declare the systemd-running path as sovereign. Delete the ghost repo. Update AGENTS.md to match reality. Remove the casefix override (no longer needed when doc matches reality).

**Option B (high W_scar):** Migrate systemd to the aspirational path. Requires systemd surgery + venv relinking + restart. Only worth it if the lowercase path has structural meaning beyond aesthetics.

## Why This Happens

Case-insensitive filesystems (macOS) vs case-sensitive (Linux). A repo cloned on macOS as `geox/` gets pushed. On Linux, a second clone creates `GEOX/`. They're different directories. systemd picks one, AGENTS.md points at the other. The casefix override is the scar of a previous failed migration attempt.

## Related Scars

- **Scar #7 (Stale-Process Port-Lock):** Same root — patch correct, old process holds port
- **Scar #10 (Agent-Summary vs Reality):** Agent claims match filesystem — probe reveals drift