# Audit Workflow

## Evidence hierarchy

1. Live registry, conformance, health, and callable tool result.
2. Runtime code, schemas, tests, CI, deployment manifests, and pinned artifacts.
3. Repository documentation and release notes.
4. User-provided architecture documents and screenshots.
5. Conversation memory and inference.

## Claim map

For every material claim, record:

| Field | Meaning |
|---|---|
| Claim | Precise statement being tested |
| Expected implementation | Code, route, schema, invariant, test, or runtime behavior that should exist |
| Evidence found | Direct evidence and source |
| Evidence missing | What could not be checked |
| Status | VERIFIED, PARTIAL, MISMATCH, MISSING, UNVERIFIABLE |
| Consequence | Why the gap matters |
| Fix | Smallest permanent repair |

## Drift taxonomy

- `SURFACE_DRIFT`: documentation, manifest, connector export, and tools/list disagree.
- `SCHEMA_DRIFT`: same capability has incompatible input or output contracts.
- `ALIAS_DRIFT`: deprecated names remain visible or resolve differently across hosts.
- `AUTHORITY_DRIFT`: capability can execute outside its declared authority path.
- `IDENTITY_DRIFT`: actor, session, model, or principal binding is inconsistent.
- `RECEIPT_DRIFT`: action and immutable evidence cannot be replayed end to end.
- `TRANSPORT_DRIFT`: MCP, REST, A2A, or connector metadata differs from the declared protocol.
- `DOMAIN_DRIFT`: an organ performs another organ's law-bearing function.
- `RUNTIME_DRIFT`: deployed code differs from the declared or attested build.
- `EVALUATION_DRIFT`: benchmark claims do not match pinned data, code, or current model.

## Hard tests

A public surface passes only when these derive from one source:

```text
capability registry
-> server registration
-> tools/list
-> connector/app export
-> generated manifest
-> generated documentation
-> profile snapshot tests
```

A claimed alias is safe only when:

- it is absent from normal discovery;
- it resolves to one canonical capability;
- it emits a deprecation signal;
- it cannot bypass newer authority checks;
- removal has a defined migration date.

## Audit conclusion

Do not grade maturity from tool count. Grade:

- semantic clarity;
- evidence integrity;
- authority integrity;
- end-to-end replay;
- failure-closed behavior;
- replaceability of model and transport;
- measured competence;
- post-action learning.
