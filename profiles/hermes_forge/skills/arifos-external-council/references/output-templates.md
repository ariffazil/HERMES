# Output Templates

## Reality audit

```text
# Verdict
[Hardest verified truth]

Evidence: L1/L2/L3/L4
Confidence: low/medium/high

## Claim map
| Claim | Expected | Evidence | Gap | Status |

## Boundary findings
[Ownership or authority violations]

## Drift findings
[Surface, schema, runtime, identity, receipt, transport]

## Fix order
P0: ...
P1: ...
P2: ...

## Unknowns
[Only material unknowns]
```

## Architecture decision record

```yaml
adr:
  title: <decision>
  status: proposed|accepted|rejected|superseded
  invariant: <protected invariant>
  owner: <law-bearing owner>
  context: <verified current state>
  decision: <chosen design>
  rejected_alternatives:
    - option: <name>
      reason: <why rejected>
  capability_contract: <semantic capability>
  authority_path: <actor to judge to execute to receipt>
  portability_test: <models, hosts, transports replaced>
  consequences:
    positive: []
    negative: []
  tests: []
  rollback: <procedure>
  evidence_refs: []
```

## Forge manifest

```yaml
forge_manifest:
  objective: <observable outcome>
  owner: A-FORGE
  repositories: []
  files_expected: []
  preconditions: []
  changes: []
  tests: []
  dry_run: true
  reversible: true
  blast_radius: low
  rollback: <procedure>
  post_change_probe: <probe>
  judge_state_required: true
  human_ack_required: false
  receipt_expected: <receipt type>
```

## Future organ admission

```text
Verdict: ADMIT_TO_INCUBATION | HOLD | REJECT

Domain law:
Owned capabilities:
Explicit non-ownership:
Registry truth:
Evidence envelope:
Authority and risk model:
Conformance results:
Benchmark results:
Unresolved hazards:
Promotion conditions:
```
