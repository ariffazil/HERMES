# Delegate Agent Audit — Verifying Subagent Claims

> Scar 2026-07-19 — Four OpenCode delegate_task agents produced conflicting claims about GEOX and arifOS state. One agent fabricated detailed code findings that did not exist in any source file.

## The Pattern

When you dispatch a `delegate_task` subagent and it returns with confident claims about code structure, tool counts, version numbers, or identity paths, **verify independently before forwarding**. Subagents have isolated contexts, no memory of your live probes, and can hallucinate detailed findings.

## Verification Recipe

For each subagent claim:

```bash
# 1. Tool count claims → health endpoint (OBS, not agent prose)
curl -s :8081/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['owner_summary']['reasons'])"

# 2. Version claims → health endpoint + git log
curl -s :8081/health | python3 -c "import json,sys; print(json.load(sys.stdin)['version'])"
git log --oneline -5

# 3. "Found code at X" claims → grep the actual source
grep -rn "claimed_pattern" /path/to/repo/src/

# 4. "Commit exists on branch" claims → git log
git log --all --oneline | grep claimed_sha

# 5. "Branch pushed to remote" claims → git ls-remote
git ls-remote --heads origin branch-name

# 6. "Service is running" claims → systemctl
systemctl is-active service-name
```

## Hallucination Red Flags

Subagent claims that warrant immediate verification:
- "Found X in file Y" → grep the file. Often the pattern doesn't exist.
- "Three parallel paths" / "Multiple implementations" → subagents invent architecture when they can't find what they're looking for.
- Specific line numbers or function names → verify they actually exist.
- "Identity verified"/"identity binding works/fails" → probe arif_init directly.
- Tool count numbers that don't match health endpoint → health wins.

## The Critical Case (2026-07-19)

An Authority Recovery agent claimed:

> "Found three parallel identity verification paths in arifosmcp/tools/session.py: Ed25519 cryptographic proof, localhost auto-identity, and string-based EXEMPT_SYSTEM_ACTORS that grants actor_verified=true for 'arif', 'hermes', 'opencode' based on string match alone."

**Verification:**
```bash
grep -rn "EXEMPT\|exempt.*actor\|auto.*verif\|Ed25519\|actor_verified\|identity_verified" /root/arifOS/src/
# → ZERO results
```

The entire claim was fabricated. The agent couldn't find what it expected, so it invented a detailed explanation. The actual arifOS identity binding works correctly — arif_init returns proper session_id and authority_scope.

**Lesson:** Never forward a subagent's code analysis to the user without verifying at least one claimed pattern exists in the actual source. A confident, well-structured claim about code is still a hallucination if grep returns nothing.
