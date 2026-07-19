# Capability ABI

Use semantic capabilities as the stable kernel contract. Tool names, providers, transports, and models are replaceable implementations.

## Required organ manifest

```yaml
organ:
  id: geox
  version: 1.0.0
  domain_law: NATURAL_LAW
  owner: GEOX
  purpose: Earth evidence and governed geoscience computation
  does_not_own:
    - constitutional_judgment
    - capital_allocation
    - human_medical_diagnosis

capabilities:
  - capability_id: earth.seismic.compute
    semantic_version: 1.0.0
    implementation:
      provider: mcp
      tool: geox_seismic_compute
    input_schema_ref: schema://earth.seismic.compute/input/1
    output_schema_ref: schema://earth.seismic.compute/output/1
    action_class: COMPUTE
    mutation: false
    irreversible: false
    authority_required: OBSERVER
    evidence_required: true
    idempotency: deterministic
    timeout_seconds: 120
    failure_mode: HOLD
    receipt_policy: result_hash
    constitutional_floors: [F2, F4, F7, F9, F11]

registry:
  source_of_truth: generated
  health_capability: system.registry.status
  profiles:
    public: []
    trusted: []
    operator: []
    executor: []

promotion:
  conformance_suite: tests/organ_conformance.json
  benchmark_ref: benchmark://organ/geox/1
  sovereign_approval_required: true
```

## Required invariants

- Capability IDs are semantic and transport neutral.
- A capability has exactly one law-bearing owner.
- Tool aliases are implementation details, not capabilities.
- Every mutating capability declares rollback or compensation.
- Every irreversible capability requires explicit human acknowledgement.
- Every output carries provenance, epistemic status, timestamp, and schema version.
- A failed authority, evidence, or schema check fails closed.
- The organ cannot promote its own membership or authority.

## Portability test

The design passes only if all of these can change without changing constitutional meaning:

- ChatGPT to another model host;
- OpenAI model to local or other provider model;
- MCP to REST or A2A adapter;
- mobile UI to CLI or cockpit;
- Python implementation to another language;
- one tool name to another implementation.
