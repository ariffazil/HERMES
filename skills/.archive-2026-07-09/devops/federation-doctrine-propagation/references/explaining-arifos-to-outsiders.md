# Explaining arifOS Internals to Outsiders

When Arif (or another sovereign) asks for a briefing that a third party — collaborator, auditor, family member — needs to read. Pattern observed: ship a sourced, citation-rich briefing first; offer visuals second; both modes are valid outputs.

## When to Use

- Arif says: "tell X everything about Y", "explain [arifOS concept] to [person]", "X needs to understand [kernel/floor/doctrine]"
- A doctrine or floor needs to be exposed externally — for onboarding, audit, or teaching
- The recipient does **not** have federation context (read: treat them as a curious outsider, not a fellow agent)

## The Pattern

### 1. Read the canon BEFORE writing
- Open the canonical file with `read_file` (paths must be real, not memory-recalled)
- Cross-check with `search_files` if scope is wide
- Identify the load-bearing skill (e.g., S03 for ACL) and primary schema/contract
- **Pitfall:** never synthesize from memory alone. The user will read your sources and notice fabrication.

### 2. Structure: 8 numbered sections, max ~700 lines
1. One-line definition (no jargon)
2. The two/three key shapes (request vs response, etc.) as a table
3. Required fields as a code block
4. What the contract enforces (Fiqh Agentik table: WAJIB/HARAM/MAKRUH/SUNAT)
5. Lifecycle — when it fires in the loop (with stage names like 000–999)
6. A literal worked example (copied from the schema, not invented)
7. **Why it exists** — three philosophical reasons (F-floor, MCP≠authority, separation)
8. Sources — real paths under `/root/...` so the recipient can verify

### 3. Tone calibration
- Recipient is a real human, possibly non-technical
- BM/English mix only if Arif specified; otherwise plain English with citations
- Each section ends with a receipt/checkpoint, not a question

### 4. Visual mode (when asked: "lukis", "draw", "diagram")
- **Always produce BOTH:** ASCII (in-chat, monospace, immediate) AND SVG (saved file, MEDIA: attached)
- ASCII pattern: `╔═══╗` top frames + `══════►` arrows + phase-pill chips + legend at bottom
- SVG pattern: dark theme (`#0a0e1a` bg), gradient strokes (blue=request, purple=response, gold=judge), `<marker>` for arrowheads, `<filter>` glow on the central load-bearing node (e.g., 666 judge gate)
- Save SVG to `/root/.hermes/cache/<recipient>_<topic>/`, send via `MEDIA:/root/.hermes/cache/<...>/<file>.svg`

### 5. Sources block — non-negotiable
End every briefing with:
```
Sources (real paths, not memory):
- /root/arifOS/skills/<SKILL>.md
- /root/arifOS/<repo>/<file>:<line>
```
Recipient must be able to verify each claim with one command.

## Pitfalls

- **Don't auto-repair envelopes.** S03 explicitly forbids it. If asked to fix a malformed envelope, refuse with reason.
- **Don't conflate ACL (the wrapper) with ACL (the network term).** In arifOS context, "ACL" almost always means the request/response envelope skill (S03). Clarify if ambiguous.
- **Don't dump Fiqh tables when not asked.** Use F-floor references inline; only expand the WAJIB/HARAM table when the recipient is implementing a client.
- **Don't produce only ASCII when SVG was asked.** Both modes is the default unless recipient specifies one.
- **Don't cite by memory.** Read the file. The 5-second cost of read_file beats the asymmetric cost of a hallucinated path.
- **Tag visuals with both formats cleanly:** ASCII in the chat body, SVG attached as `MEDIA:` path. Avoid base64-encoding SVG into the chat.

## Filesystem Layout

```
/root/.hermes/cache/<recipient>_<topic>/
├── <diagram>.svg       # canonical visual artifact
└── notes.md            # optional: scratch state during the briefing
```

`cache` is appropriate here — these are ephemeral visuals meant for one recipient.
For permanent doctrine artifacts, use `/root/AAA/docs/ZEN-<TOPIC>.md` (the umbrella skill's main pattern).

## Related

- Umbrella: this skill (`federation-doctrine-propagation`)
- Sibling: `geological-artifact-publication` — shares the citation-rich, provenance-attached publication pattern but for geoscience domains specifically
