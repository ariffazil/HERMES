# Fabricated Code Analysis Claims — Detection Pattern

> Proven: 2026-07-19 — Authority Recovery agent claimed to find code patterns that didn't exist

## The Pattern

When an agent is dispatched to "find the root cause" of a system failure, it will find one — even if it has to fabricate it from plausible-sounding code analysis. The agent describes specific code locations, variable names, and line numbers. These sound authoritative. They are not.

## Example (2026-07-19)

**Agent claim:** arifOS session.py has three parallel identity verification paths:
1. Ed25519 cryptographic proof
2. Localhost auto-identity  
3. String-based exemption (`_ED25519_EXEMPT_SYSTEM_ACTORS` at lines 1821-1838) that auto-verifies "arif", "hermes", "opencode"

**Verification:**
```bash
grep -rn "EXEMPT\|exempt.*actor\|Ed25519\|actor_verified\|identity_verified" /root/arifOS/src/
# Zero results
```

**Root cause of the hallucination:** The agent was told to "find the root cause of actor_verified=false." It reasoned backwards: "if verification is failing, there must be a verification path that's broken → let me describe what plausible verification paths would look like → present as findings." It never actually read the code — it pattern-matched against known authentication architectures.

## Detection Recipe

1. Read the agent's claim — note specific file paths, variable names, line numbers
2. `grep -rn "<variable_name>" <exact_path>` 
3. If zero matches → FABRICATED. Do not forward the claim.
4. If partial matches → extract only the verified portion, discard the rest
5. If full match → verify the SEMANTICS match the claim (the code may exist but do something different)

## Tells That Precede Fabrication

- Agent uses confident language about code it hasn't shown you
- Agent describes "three paths" or "multiple layers" without citing actual function names
- Agent provides line numbers but no actual code snippets
- Agent's diagnosis is "too clean" — maps perfectly to known auth patterns
- Agent was dispatched with "find the root cause" framing (not "report what you observe")

## The Rule

**Never forward agent code-analysis claims without independent source verification.** The agent's prose is not evidence. The grep result is.
