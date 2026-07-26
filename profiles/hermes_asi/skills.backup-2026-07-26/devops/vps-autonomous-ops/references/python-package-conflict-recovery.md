# Python Package Conflict Recovery

> **Pattern:** Two pip packages share the same `site-packages/` namespace directory, causing import corruption.
> **Proven:** 2026-07-19 — `fastmcp` (2.14.7) + `fastmcp-slim` (3.4.2) both install to `site-packages/fastmcp/`.

## Recognition

Symptom: `from fastmcp import FastMCP` succeeds in one environment but fails in another (systemd vs shell). Error changes between `ModuleNotFoundError`, `ImportError: cannot import name 'PrivateKeyJWTC...'`, and `TypeError: unexpected keyword argument 'client_log_level'` — even though `inspect.signature()` shows the kwarg is valid.

Root cause: Two packages (`fastmcp` and `fastmcp-slim`) share the same namespace directory. `uv pip list` shows both. Uninstalling one removes the shared directory entirely. Reinstalling the other requires `--reinstall` to repopulate it.

## Fix Recipe

```bash
cd /root/<project>

# 1. Identify the conflicting pair
uv pip list | grep <package_prefix>

# 2. Remove the unwanted one (the slim/light variant)
uv pip uninstall <package>-slim -y

# 3. Reinstall the wanted one with --reinstall to repopulate namespace
uv pip install --reinstall "<package><3.0"

# 4. Verify import works
.venv/bin/python3 -c "import <package>; print(<package>.__version__)"

# 5. Restart service (systemd auto-retry will pick up fixed venv)
systemctl restart <service>
```

## Specific Case: FastMCP

| Package | Version | Action |
|---------|---------|--------|
| `fastmcp` | 2.14.7 | Keep (pinned `<3.0`) |
| `fastmcp-slim` | 3.4.2 | Remove — shares `site-packages/fastmcp/` namespace |

```bash
uv pip uninstall fastmcp-slim -y
uv pip install --reinstall "fastmcp<3.0"
```

## Why `uv pip install "fastmcp<3.0"` Alone Doesn't Fix It

`uv pip install "fastmcp<3.0"` with `fastmcp-slim==3.4.2` already installed reports "Checked 1 package in 10ms" — it considers the constraint satisfied because `fastmcp-slim` provides the `fastmcp` namespace even though it's the wrong major version. The slim package is NOT auto-removed by the version constraint because `uv` doesn't treat them as conflicting (different package names, same namespace directory).

## Prevention

When upgrading a package that has a `-slim`, `-lite`, or `-core` variant: always `uv pip list | grep <name>` first. If both variants are installed, remove the unwanted one before pinning the wanted one.
