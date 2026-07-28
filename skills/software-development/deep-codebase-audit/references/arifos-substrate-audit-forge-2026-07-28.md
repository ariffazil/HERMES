# arifOS Substrate Audit Forge — 2026-07-28

Full worked example of forging 7 audit findings across the arifOS federation kernel.  
Consult this when remediating audit findings — it captures the exact commands, verification patterns, and migration strategies used.

## Findings Summary

| ID | Finding | Priority | Status | Pattern |
|---|---|---|---|---|
| F1 | Package collision (arifos_mcp/ vs arifosmcp/) | P0 | Already resolved | Git log verification, stale import check |
| F2 | Port mapping drift | P0 | Consistent + doc fix | Cross-ref systemd, Caddy, docs, live curl |
| F3 | Global `_ACTIVE_SESSION_ID` singleton | P1 | Implemented | Redis-backed SessionRegistry via session_registry.py |
| F4 | Monolithic tools.py (24,685 lines) | P2 | Partially split | Tool impls already in `tools/` modules; runtime/tools.py is a governance support file |
| F5 | Static .well-known/ in kernel repo | P2 | Removed | Per FEDERATION_CONTRACT §5.4.5, AAA owns agent cards |
| F6 | Legacy 3-term underscore names | P2 | Already aliased | interceptor.py TOOL_ALIASES covers all; server.py SDK alias registration |
| F7 | Standalone arifos_wiki_tools/ package | P3 | Consolidated | Absorbed into arifosmcp/tools/wiki.py |

## Key Commands

### Stale-Finding Detection
```bash
# Check git history for rename evidence
git log --all --oneline --diff-filter=D -- "arifos_mcp*"
# => commit 2af86baeb refactor: rename arifos_mcp → arifosmcp

# Check if finding line numbers still valid
wc -l <suspected_file>
# If cited line > actual lines, fix was already applied
```

### Port Auditing — Cross-Reference All Sources
```bash
# Systemd units
cat /etc/systemd/system/{arifos,geox-mcp,wealth-organ,well,a-forge,aaa-a2a}.service | grep -i port

# Caddyfile
cat /etc/caddy/Caddyfile.live | grep '127.0.0.1:' | sort -t: -k2 -n

# AGENTS.md documentation
grep -A1 '| \*\*' /root/arifOS/AGENTS.md | grep '| `curl'

# Live probes
for port in 8088 8081 18082 18083 7071 7072 3001; do
  echo -n ":$port => "; curl -s --connect-timeout 2 http://127.0.0.1:$port/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "FAILED"
done

# Organ-level configs (A-FORGE's runtime_metrics.py, GEOX scripts, etc.)
grep -r "808[0-9]\|1808[0-9]" /root/A-FORGE/ --include='*.py' | grep -v __pycache__
grep -r "808[0-9]\|1808[0-9]" /root/GEOX/scripts/ --include='*.py'
```

### Redis-Backed SessionRegistry Pattern
```python
# session_registry.py — module-level singleton pattern
from arifosmcp.runtime.session_registry import get_registry

# Async methods for Redis
registry = get_registry()
await registry.set_session("sid_abc", {"actor_id": "arif"})
await registry.get_session("sid_abc")
await registry.set_active_session_id("sid_abc")
await registry.get_active_session_id()
await registry.check_and_record_nonce("request-uuid")  # replay protection

# Sync bridging (for existing synchronous modules)
if _HAS_REDIS_REGISTRY:
    try:
        import asyncio
        asyncio.run(_REDIS_SESSION_REGISTRY.set_active_session_id(session_id))
    except Exception:
        pass  # fallback to in-memory global
```

Key design decisions:
- `SETNX` for per-session async mutex locks
- Lua script for lock release (CAS pattern — only delete if token matches)
- In-memory dict + thread lock fallback when Redis unavailable
- Flat Redis hash encoding for session data (string-encoded JSON for nested fields)
- Nonce cache with TTL (600s default, bounded LRU in-memory fallback)

### Package Consolidation (Wiki Tools → tools/wiki.py)
```python
# Create consolidated module
# File: arifosmcp/tools/wiki.py
# Wire into: arifosmcp/tools/__init__.py
from arifosmcp.tools.wiki import ingest_repo, search_index, map_repo, ask_repo

# Remove standalone package
mv arifos_wiki_tools /tmp/backup/
git rm -r arifos_wiki_tools/
```

The consolidated module combines: models (FileRecord/ChunkRecord), indexer (gitignore-aware chunking, symbol extraction), search (TF-IDF index + grep fallback), synthesis (repo map + evidence-first Q&A).

### Alias Verification (Dual Naming)
```bash
# Check interceptor.py alias coverage
grep -A100 "TOOL_ALIASES" /root/arifOS/arifosmcp/kernel/interceptor.py | head -80

# Check server.py SDK alias registration
grep -B2 -A10 "SDK_ALIAS_REGISTRATIONS" /root/arifOS/arifosmcp/server.py | head -40

# Find any missing 3-term names
grep -r '"arif_[a-z]\+_[a-z]\+_[a-z]\+"' /root/arifOS/arifosmcp/ --include='*.py' | grep -v __pycache__ | grep -v '".*:.*"' | head -20
```

### Surface Gate Handling
The arifOS repo has a pre-commit `SURFACE-GATE` hook that checks live tools against declared surface. When running commits:
```bash
# If surface gate blocks, check that:
git commit -m "..."  # will run surface-map drift check
# Must have arifOS service running on :8088 with 8 public tools
# Failure: "SURFACE-GATE: STRICT MODE — Live tools mismatch"
```

## Data Flows

### Session Lifecycle (After F3 Fix)
```
Client ──arif_init──→ SessionRegistry.set_session(sid, {actor, authority})
                         ├── Redis HSET arifos:session:<sid> TTL 24h
                         └── Redis SET arifos:active_session <sid> TTL 24h
                             
Client ──arif_judge──→ SessionRegistry.get_session(sid)
                         ├── Redis HGETALL arifos:session:<sid>
                         └── actor ownership check via canonical key

Client ──arif_seal───→ SessionRegistry.acquire_session_lock(sid)
                         ├── Redis SETNX arifos:session_lock:<sid> <token>
                         └── Lua CAS for release
```

## Related Reference Files

- `references/geox-sot-inventory-2026-07-13.md` — Audit methodology (pre-forge phase)
- `references/credential-redaction-verification.md` — Federation-wide credential patterns
- `references/mcp-tool-surface-drift-audit.md` — Tool surface drift detection
