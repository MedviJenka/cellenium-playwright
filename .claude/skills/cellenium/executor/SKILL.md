---
name: executor
description: Discover and execute pytest tests with repository-native commands, classify failures, and report exact evidence. Use after tests are written or whenever a pytest selection, suite, marker, or environment must be run reliably.
disable-model-invocation: true
---

# Pytest Executor

Execute tests and preserve trustworthy evidence. This is the fourth TestFlow stage. It runs tests; it does not rewrite expectations to obtain a green result.

## Inputs

Accept test paths, node IDs, markers, `TST-*` case mappings, or a changed-file set from `writer`. If no selection is provided, derive the narrowest relevant selection from the repository and explain it.

## Process

1. **Discover the runner contract**
   - Read `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg`, lockfiles, and relevant `conftest.py` files.
   - Determine the repository's environment runner: `uv run`, Poetry, Hatch, tox, nox, or direct Python.
   - Identify registered markers, pytest plugins, async mode, test paths, parallelism settings, and required environment.
   - Use the locked dependency path. Do not install ad hoc packages unless the repository contract requires it.

2. **Check prerequisites without exposing secrets**
   - Verify required variables by name and presence only.
   - Verify files, browsers, local services, databases, and credentials required by the selected layer.
   - Distinguish a missing prerequisite from a product failure.
   - For headed Playwright tests on Linux CI, use the repository's Xvfb convention when present.

3. **Execute from narrow to broad**
   - Collection: run `pytest --collect-only` for new or structurally changed tests.
   - Targeted: run exact node IDs or changed test files.
   - Related suite: run the owning package/module tests.
   - Full suite: run only after targeted tests produce valid evidence, unless the user asks for a narrow run.
   - Preserve repository flags such as strict markers, verbosity, coverage, parallelism, and distribution strategy.

4. **Capture evidence**
   - Record the exact command, working directory, interpreter version, pytest version, exit code, duration, and test counts.
   - Keep the first actionable traceback and concise summaries of repeated failures.
   - Never report GREEN from collection-only output.

5. **Classify every non-zero result**
   - `TEST`: assertion proves the implementation violates the specified behavior.
   - `TEST-DEFECT`: incorrect expectation, brittle setup, leaking fixture, order dependency, or test bug.
   - `COLLECTION`: import, syntax, discovery, marker, or parameterization failure.
   - `ENVIRONMENT`: missing dependency, secret, browser, service, permissions, or incompatible runtime.
   - `PRODUCT-ERROR`: unhandled application exception encountered before the intended assertion.
   - `FLAKY`: result changes under identical controlled reruns; include evidence, not suspicion.
   - `UNRELATED`: outside the changed test/behavior scope and independently attributable.

6. **Rerun only for a reason**
   - Rerun a failure to test a concrete flake hypothesis, order dependency, or isolation issue.
   - Do not repeatedly rerun until green.
   - Do not add retries, skips, xfails, or relaxed assertions.

## Result format

### Environment

State runner, Python, pytest, relevant plugins, and prerequisite status.

### Execution table

| Scope | Command | Collected | Passed | Failed | Skipped | Exit | Duration |
|---|---|---:|---:|---:|---:|---:|---:|

### Failure analysis

For each failure, provide:

- classification;
- test node ID;
- related `TST-*` and `PRD-*` IDs when available;
- first actionable traceback location;
- expected versus observed behavior;
- whether the next action belongs to `writer`, production implementation, or environment setup.

### Verdict

Use exactly one:

- `GREEN`: selected tests passed and prove the requested scope.
- `EXPECTED RED`: a new test fails on the intended missing behavior.
- `INVALID RUN`: collection or environment prevented behavioral evidence.
- `REGRESSION`: existing required behavior failed.
- `MIXED`: multiple classifications require separate actions.

## Quality gate

Execution is complete only when:

- commands are repository-native and reproducible;
- collection and execution are not conflated;
- every failure has a classification;
- exact counts and exit codes are reported;
- secrets are not printed;
- no result is hidden, weakened, or retried into a misleading verdict;
- `evaluator` receives the tests, specification, and execution evidence.
