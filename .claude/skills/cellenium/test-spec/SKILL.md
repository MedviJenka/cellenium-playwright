---
name: test-spec
description: Convert product requirements and technical specifications into a traceable pytest test specification. Use after PRD analysis or when API, behavior, schema, or acceptance specifications need concrete test cases before implementation.
disable-model-invocation: true
---

# Test Specification

Design the smallest complete pytest test set that proves the requested behavior. This is the second TestFlow stage.

## Inputs

Use, in priority order:

1. the `prd-reader` requirement matrix;
2. explicit acceptance criteria or technical specifications;
3. public contracts in code, schemas, API documentation, or repository conventions;
4. implementation details only to discover branches and boundaries, never as the asserted contract.

When sources disagree, preserve the higher-authority product contract and report the conflict. Do not silently encode current implementation behavior over the specification.

## Process

1. **Inspect existing test conventions**
   - Locate pytest configuration, `conftest.py`, fixtures, factories, markers, plugins, and nearby tests.
   - Reuse established file placement, naming, fixture scope, async style, and assertion patterns.
   - Do not introduce a second testing convention.

2. **Choose the correct test boundary**
   - Unit: pure behavior with dependencies injected or replaced at public boundaries.
   - Integration: collaboration between owned components or a real local persistence boundary.
   - Contract: request/response, schema, event, CLI, or adapter behavior.
   - End-to-end: critical user workflow through the real system surface.
   - Prefer the lowest layer that can prove the observable contract; add a higher-level test only when the integration itself is part of the requirement.

3. **Partition behavior**
   - Cover the primary success path.
   - Cover each observable error path and state transition.
   - Cover meaningful boundaries and equivalence classes.
   - Cover precedence where multiple rules could apply.
   - Include security and permission cases only when the contract crosses a trust boundary.
   - Exclude impossible, duplicate, and implementation-only cases.

4. **Design deterministic setup**
   - Use existing fixtures first.
   - Prefer `tmp_path`, `monkeypatch`, `capsys`, `caplog`, `freezegun`, or repository equivalents over global state and real delays.
   - Mock network, clock, randomness, process, and third-party boundaries; do not mock the unit under test or its private methods.
   - Name required environment, credentials, browser, database, or service dependencies explicitly.

5. **Define proof**
   - Every case must include an assertion that would fail if the behavior were removed or inverted.
   - Avoid assertions limited to mock call counts unless the call itself is the public contract.
   - Prefer exact domain outcomes, state changes, emitted events, error types, and user-visible results.

## Test-case format

Assign stable IDs: `TST-001`, `TST-002`, and so on.

| Test ID | Requirement IDs | Layer | Scenario | Setup | Action | Expected result | Fixtures/mocks |
|---|---|---|---|---|---|---|---|

For parameterized cases, list the complete input/output table rather than describing it as “various inputs.”

## Required output

### Test strategy

State the chosen layers, why each is necessary, and which expensive layers were intentionally avoided.

### Test cases

Provide the traceable case table.

### File plan

List the exact test files to create or modify and the existing fixtures to reuse. Name new fixtures only when reuse is impossible.

### Environment contract

List commands, markers, variables, services, browsers, and credentials needed to collect and execute the tests. Separate required dependencies from optional integration dependencies.

### Traceability

Map every `PRD-*` requirement to one or more `TST-*` cases. Mark any uncovered requirement as `BLOCKED` with the missing information.

### Exclusions

State behaviors intentionally not tested and why they are outside scope, redundant, or owned by a third party.

## Quality gate

The specification is ready for `writer` only when:

- every MUST requirement maps to a concrete test case;
- every case has one clear behavior and meaningful expected result;
- success, errors, boundaries, and precedence are covered where specified;
- tests target public behavior rather than private implementation;
- setup is deterministic and repository-native;
- file locations and execution prerequisites are explicit;
- no case depends on an unresolved expectation.

Do not write or execute tests in this stage. Hand the approved specification to `writer`.
