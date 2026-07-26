# Bounded Forge Workflow

## 1. Frame

Record:

- desired observable outcome;
- invariant protected;
- current evidence;
- owner of the change;
- affected organs and interfaces;
- reversible and irreversible steps.

## 2. Inspect

Inspect code, tests, registry, deployment state, and current errors. Do not patch from a screenshot alone.

## 3. Design the minimal permanent fix

Prefer, in order:

1. one source of truth;
2. generated manifests and documentation;
3. semantic capability and modes;
4. internal adapter;
5. temporary compatibility alias with expiry.

Do not reverse this order.

## 4. Prepare change set

A complete change set includes:

- code or configuration;
- schema migration;
- compatibility impact;
- unit and property tests;
- conformance or registry snapshot test;
- documentation generated from the source of truth;
- rollback or compensation;
- post-deployment probe.

## 5. Gate

For read-only or reversible work, proceed within available authority.

For mutation, deployment, publication, deletion, promotion, or sealing:

- require the proper judge output;
- bind the actor and approved action hash;
- require human acknowledgement where irreversible;
- use A-FORGE or the authorised write connector;
- preserve idempotency and receipt references.

## 6. Verify

After change:

1. re-run tests;
2. re-run live registry/conformance;
3. compare expected and live surfaces;
4. verify rollback remains possible;
5. verify the receipt can be replayed;
6. report residual unknowns.
