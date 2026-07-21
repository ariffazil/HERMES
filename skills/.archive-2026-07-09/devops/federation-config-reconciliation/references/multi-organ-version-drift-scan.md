# Multi-Organ Version & Config Drift Scan

> Forged 2026-07-20 from GLM 5.2 free-tier federation audit session.

## When to Use

When a quick health check isn't enough — you need to detect version staleness, systemd path drift, and model/provider divergence across ALL organs in parallel.

## The Scan (3 parallel probes)

### Probe 1 — Version freshness across all organs

```bash
echo "=== FEDERATION VERSION SCAN ===" && \
for org in arifOS A-FORGE AAA geox WEALTH WELL hermes-agent; do
  echo "--- $org ---"
  if [ -f /root/$org/pyproject.toml ]; then
    grep -E '(version|name|requires-python)' /root/$org/pyproject.toml 2>/dev/null | head -3
  elif [ -f /root/$org/package.json ]; then
    python3 -c "import json; d=json.load(open('/root/$org/package.json')); print(f'name: {d.get(\"name\",\"?\")}'); print(f'version: {d.get(\"version\",\"?\")}')" 2>/dev/null
  fi
  echo
done
```

**What to look for:** Version strings > 30 days old indicate the tag wasn't bumped, not that code is stale. Always verify with `git log --oneline -3` before flagging staleness.

### Probe 2 — Systemd working directory audit

```bash
echo "=== SYSTEMD PATH AUDIT ===" && \
for svc in arifos a-forge a-forge-mcp aaa-a2a geox-mcp wealth-organ well; do
  echo -n "$svc: "
  systemctl cat $svc 2>/dev/null | grep -E '(WorkingDirectory|ExecStart)' | head -2 | tr '\n' ' '
  echo
done
```

**What to look for:** Paths that disagree with AGENTS.md declarations. Before flagging, check override files in `/etc/systemd/system/<service>.service.d/` for documented case-fix or workdir overrides.

### Probe 3 — TokenRouter model consensus

```bash
echo "=== MODEL CONSENSUS ===" && \
echo "--- Hermes ---" && \
grep -A2 'tokenrouter' /root/.hermes/config.yaml 2>/dev/null | head -10 && \
echo "--- arifOS LLM ---" && \
grep -E 'TOKENROUTER_MODEL|"model"' /root/arifOS/arifosmcp/runtime/llm_client.py 2>/dev/null | head -5 && \
echo "--- Env override ---" && \
grep 'TOKENROUTER_MODEL' /root/.secrets/tokenrouter.env 2>/dev/null
```

**What to look for:** The env var in `tokenrouter.env` overrides code defaults. What looks like divergence (code says `MiniMax-M3`, env says `gemini-3.5-flash`) is correct configuration, not drift.

## Verdict Classification

| Finding | Verdict | Action |
|---|---|---|
| Version > 30d but commits < 24h | Tag stale, code current | Note for housekeeping |
| Systemd path ≠ AGENTS.md, override explains it | Documented workaround | No action |
| Systemd path ≠ AGENTS.md, no override | Real drift | Investigate which is canonical |
| Model differs by component, env var explains it | By design | No action |
| Model differs, no env var, no doc | Real drift | Reconcile to single source |
