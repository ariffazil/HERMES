# Hermes Config Unblock — Full Diff (2026-08-05)

## Config file: /root/HERMES/config.yaml

### What was removed

```diff
-  disabled_toolsets:
-    - serena-mcp
-  stdio_mcp_quarantine:
-    enabled: true
-    list:
-      - serena-mcp
-    migration_target: streamable-http on localhost (per-organ)
-    opt_in_via: add to active toolset at call time
-    reason: Structural memory leak — opt-in per call, not spawn-at-load
-    restore_via: hermes tools enable <name>
+  # UNBLOCKED by F13 SOVEREIGN directive 2026-08-05 — no tool restrictions
```

```diff
-  max_bytes: 50000
-  max_lines: 2000
-  max_line_length: 2000
+  max_bytes: 200000
+  max_lines: 10000
+  max_line_length: 5000
```

```diff
-  max_concurrent_children: 3
+  max_concurrent_children: 6
```

```diff
-command_allowlist:
-  - script execution via heredoc
-  - script execution via -e/-c flag
+# UNBLOCKED by F13 SOVEREIGN directive 2026-08-05 — full terminal access
```

```diff
# browser section
-  allow_private_urls: false
+  allow_private_urls: true

# security section
-  allow_private_urls: false
+  allow_private_urls: true
```

### What was enabled via CLI

```bash
hermes tools enable video video_gen x_search context_engine homeassistant spotify yuanbao
```

All 22 toolsets now show ✓ enabled.

### Verification

```bash
hermes tools list  # all ✓
grep 'UNBLOCKED' /root/HERMES/config.yaml  # 2 comments
grep 'allow_private_urls: true' /root/HERMES/config.yaml  # 2 matches
```
