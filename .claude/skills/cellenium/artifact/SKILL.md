---
name: artifact
description: Run the complete TestFlow pipeline to turn a PRD or specification into traceable pytest tests, execute them, and evaluate their quality. Use when the user wants an end-to-end pytest test artifact rather than one individual TestFlow stage.
disable-model-invocation: true
---

# TestFlow Artifact

Create a complete, executable pytest test artifact from product intent. Coordinate the five TestFlow stages without skipping evidence or stopping at an intermediate handoff.

## Inputs

Accept one or more of:

- PRD, ticket, feature brief, or acceptance-criteria path;
- technical specification, API/schema contract, or behavior description;
- target package, module, endpoint, command, or user flow;
- existing pytest tests to extend or repair.

Resolve repository-provided information before asking the user. Ask only when an unresolved product choice would produce materially different assertions.

## Pipeline

Run each stage in order and preserve stable IDs across handoffs.

### 1. PRD Reader

Apply `prd-reader` to produce `PRD-*` requirements, business invariants, boundaries, exclusions, and blocking unknowns.

If there is no formal PRD, treat the highest-authority supplied acceptance criteria as the product source. Do not infer a new product contract from implementation alone.

### 2. Test Specification

Apply `test-spec` to produce `TST-*` cases, test layers, exact file plan, deterministic environment contract, and complete `PRD-*` traceability.

Do not proceed with a case whose expected result is unresolved.

### 3. Locator and Element Writer

For UI cases, apply `locator-writer` to inspect the live page, validate stable Playwright selectors, and upsert the required element rows into the configured Google Sheet.

Skip this stage for non-UI tests or when every required logical element already has a verified locator. Never guess a selector when the page cannot be inspected.

### 4. Pytest Writer

Apply `writer` to create or update the pytest files. Only test code and test-owned fixtures are in scope unless the user explicitly requests production implementation.

Require successful collection. For missing behavior, preserve valid RED evidence; for existing behavior, require targeted GREEN evidence.

### 5. Pytest Executor

Apply `executor` to run collection, targeted tests, related tests, and the full suite when appropriate. Capture exact commands, exit codes, counts, and classified failures.

A missing dependency, secret, browser, service, or fixture is an invalid run, not a product verdict.

### 6. Test Evaluator

Apply `evaluator` to assess traceability, regression sensitivity, assertions, boundaries, determinism, maintainability, and execution evidence.

Route findings back to the owning stage:

- product ambiguity → `prd-reader`;
- missing or incorrect case → `test-spec`;
- missing, stale, or ambiguous UI element → `locator-writer`;
- test implementation defect → `writer`;
- invalid or incomplete run → `executor`.

Repeat only the affected downstream stages after a correction. Finish when the evaluator returns `APPROVED`, `EXPECTED RED ACCEPTED`, or a genuine external `BLOCKED` verdict.

## Non-negotiable rules

- Tests validate observable behavior, not private implementation.
- Every MUST requirement maps to an implemented pytest node.
- Tests must collect before their behavior can be evaluated.
- A passing test must fail under at least one plausible regression of the behavior it claims to protect.
- Do not modify production code unless the user explicitly adds implementation to the request.
- Do not create empty tests, placeholders, unconditional passes, fake fixtures, hidden skips, xfails, retries, or relaxed assertions.
- Do not hit real external services in unit tests. Use real integrations only when the specification requires that layer and the environment is available.
- Never print secrets or copy credential values into tests.
- Reuse repository commands and conventions; do not introduce another test framework.

## Final deliverable

Return:

### Requirements

The final `PRD-*` matrix and unresolved non-blocking assumptions.

### Test specification

The implemented `TST-*` cases and layer rationale.

### UI locators

For UI cases, list Google Sheet rows added or updated, direct worksheet lookup results, and live selector validation results.


### Files

Exact test files created or modified, plus fixtures reused or added.

### Traceability

| Requirement | Test case | Pytest node | Result |
|---|---|---|---|

### Execution

Exact commands, interpreter and pytest versions, counts, durations, exit codes, and failure classifications.

### Evaluation

Evaluator verdict, fixed findings, remaining residual risks, and any externally blocked evidence.

## Completion criteria

The artifact is complete only when:

- all reachable test files are fully implemented;
- every MUST requirement is covered or explicitly blocked by unavailable product information;
- collection succeeds;
- targeted execution produces valid GREEN or intended RED evidence;
- related/full-suite effects are reported when runnable;
- evaluator findings are resolved or recorded as external blockers;
- no actionable work remains in a downstream stage.
