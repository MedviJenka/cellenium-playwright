---
name: writer
description: Implement behavior-focused pytest tests from an approved test specification. Use when concrete pytest files, fixtures, parameterized cases, or regression tests must be written without changing production behavior.
disable-model-invocation: true
---

# Pytest Writer

Implement the approved test specification as maintainable pytest tests. This is the third TestFlow stage and the only stage that writes test code.

## Inputs

Require a `test-spec` case set or equivalent explicit acceptance criteria. Preserve its `PRD-*` to `TST-*` traceability. If an expected result is materially ambiguous, return it to `prd-reader` or `test-spec`; do not invent an assertion.

## Rules

1. **Follow the repository**
   - Read pytest configuration, nearby tests, `conftest.py`, fixtures, factories, and package layout before editing.
   - Match existing import style, async support, markers, naming, and test placement.
   - Reuse fixtures and helpers before adding new ones.

2. **Test behavior, not implementation**
   - Exercise public functions, classes, endpoints, commands, events, or user surfaces.
   - Assert observable return values, state, output, errors, side effects, or persisted data.
   - Never inspect private attributes, patch the function under test, or duplicate the implementation algorithm in the assertion.

3. **Keep tests deterministic**
   - Isolate filesystem work with `tmp_path`.
   - Control environment with `monkeypatch`.
   - Capture output and logs with pytest fixtures.
   - Replace clock, randomness, network, subprocess, browser, and third-party services only at their boundaries.
   - Never use real sleeps or order-dependent global state.

4. **Use pytest deliberately**
   - Parameterize genuine equivalence classes and boundary tables.
   - Give parameters readable IDs when raw values are unclear.
   - Use exact exception types and `match=` when the message is part of the contract.
   - Use markers already registered by the project.
   - Keep each test focused on one behavior; multiple assertions are acceptable when they prove one outcome.

5. **Keep setup proportionate**
   - Prefer local values over fixtures used once.
   - Put shared setup in the narrowest fixture scope.
   - Avoid autouse fixtures unless the repository already requires them for isolation.
   - If setup is larger than the behavior, simplify the boundary instead of building a mock maze.

6. **Preserve production code**
   - Do not modify application code, configuration defaults, or public contracts unless the user explicitly expands the task.
   - Do not weaken or delete existing tests to make new tests pass.
   - Do not add skips, xfails, retries, arbitrary timeouts, or exception swallowing as substitutes for a working test.

## Implementation sequence

1. Map each `TST-*` case to an exact test function or parameter row.
2. Add the smallest coherent test file change.
3. Collect the new tests to catch import, fixture, and parameterization errors.
4. Run the narrowest affected test selection.
5. Interpret the result:
   - For unimplemented requested behavior, capture the expected RED failure.
   - For regression coverage of existing behavior, require GREEN.
   - A collection, fixture, environment, or unrelated failure is not valid RED evidence; fix the test harness first.
6. Refactor test code without changing the asserted behavior.
7. Hand the exact test paths and case mapping to `executor`.

## Test naming

Use names that state the condition and observable result:

```python
def test_rejects_duplicate_email_without_creating_user():
    ...
```

Avoid names such as `test_case_1`, `test_method_called`, or `test_works`.

## Output contract

Report:

- files created or modified;
- `TST-*` cases implemented by each test;
- fixtures and mocks added or reused;
- the collection command and result;
- the targeted command and RED/GREEN result;
- any blocked case with the exact missing contract or dependency.

## Quality gate

Writing is complete only when:

- all approved cases are implemented or explicitly blocked;
- tests collect successfully;
- each assertion can fail for a plausible product regression;
- boundaries are mocked, internals are not;
- tests are isolated and deterministic;
- no placeholders, empty tests, unconditional passes, or fake fallbacks remain;
- `executor` receives runnable paths and commands.
