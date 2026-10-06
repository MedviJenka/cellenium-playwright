---
name: cruising
description: In-flight check while tests are being built. Use after any TestFlow stage, after writing or changing tests, or before a commit or PR to verify that everything is in place and to hunt for critical errors and potential bugs in the tests, locators, fixtures, and observed product behavior.
disable-model-invocation: true
---

# Cruising — Everything in Place, No Hidden Bugs

Purpose: while tests are being built, confirm that every piece is in place and catch critical errors and potential bugs before they harden into the suite.

## Workflow position

**2 of 3 — repeat while building tests.** Use after `before-startup` returns **READY TO BUILD TESTS**. Run it after each TestFlow stage (`prd-reader`, `test-spec`, `locator-writer`, `writer`, `executor`), after any manual test change, and before every commit or PR. Hand off to `landing` only when cruising returns **ON COURSE** with no open CRITICAL findings.

## How to run

First name the checkpoint: the TestFlow stage just finished, `TEST CHANGE`, `COMMIT`, or `PR`. Then run all four sections. Use command output, file paths with line numbers, and observed behavior. Green tests alone are not evidence that nothing is wrong.

Report findings; do not silently rewrite code. When the user asks for fixes, route each finding to the stage that owns it (`prd-reader`, `test-spec`, `locator-writer`, `writer`, `executor`) and run cruising again afterward.

## 1. Everything in place

1. **Working tree:** run `git status` and account for every changed or untracked file, including partial output from earlier or interrupted runs. Nothing unexplained may remain.
2. **Stage outputs:** every completed stage has its output. That means `PRD-*` requirements, `TST-*` cases with file plan, verified locators, and test files at the planned paths. Stable IDs are preserved across handoffs.
3. **Traceability:** every `PRD-*` requirement maps to at least one `TST-*` case, every `TST-*` case maps to a test function, and no test exists without a requirement.
4. **Locators:** every logical element the tests use exists in the correct Google Sheet worksheet/screen and resolves on the live page.
5. **Fixtures and data:** every fixture, test-data file, account, and environment variable the new tests need exists and is wired in.
6. **System still healthy:** recheck the `before-startup` critical items: dependencies, browser launch, settings import, and target reachability. An environment that has since degraded is a FAIL.

## 2. Collection and execution

7. **Collection:** `pytest --collect-only` is clean, and each new test is collected exactly once.
8. **Targeted run:** run the new and changed tests and report the exact command, exit code, and pass/fail/skip counts.
9. **Failure classification:** classify every failure as **product bug**, **test bug**, or **environment**. Use evidence: traceback, screenshot, and log. An environment failure is an invalid run, not a verdict.
10. **Flakiness:** rerun each failing or newly passing test at least once, and also under the CI parallel mode (for example `-n auto --dist loadscope`). Any result that differs between runs is a finding.
11. **Baseline drift:** compare the full-suite result with the `before-startup` baseline. Any new failure outside the changed tests is a finding.

## 3. Critical errors (hard stop)

Any item here is **CRITICAL**:

12. **Broken suite:** syntax, import, collection, or fixture-setup errors, plus blocking CI lint errors.
13. **Tests that cannot fail:** missing assertions, `assert True`, assertions on the wrong object, broad `except` that swallows failures, and `skip`/`xfail` without a stated reason and ticket.
14. **Leaks and cleanup:** browser sessions or processes not torn down (no `finally`/fixture teardown), and temp data or files left behind.
15. **Secrets and safety:** credentials, tokens, or `.env` values in code, logs, screenshots, or reports, and tests that write to production data or modify the shared Google Sheet unintentionally.
16. **Wrong target:** tests pointed at the wrong environment, URL, or account.

## 4. Potential bugs

Scan the new and changed tests, fixtures, and helpers, and report each finding with `file:line`:

17. **Fragile selectors:** index-based XPath, auto-generated classes, text that changes, and selectors matching more than one element.
18. **Timing:** `sleep` instead of explicit waits, missing waits after navigation or actions, and race-prone assertions.
19. **Isolation:** shared mutable state, order dependence, and fixtures with the wrong scope for parallel execution.
20. **Hardcoding:** URLs, credentials, dates, locale, or time-zone assumptions inside tests instead of config or fixtures.
21. **Coverage gaps:** boundaries, negative paths, empty or invalid input, and error states from `test-spec` that are missing or only partially asserted.
22. **Correctness slips:** copy-paste errors in IDs, parameters, or expected values, wrong exception types, unhandled `None`, and tests whose name does not match what they assert.
23. **Product bugs observed:** any application defect seen during runs, with reproduction steps and evidence, marked as a regression-test candidate.

## Report format

Output:

1. `Checkpoint: <stage | TEST CHANGE | COMMIT | PR>`;
2. an **In place** table: `# | item | PASS/FAIL/N-A | evidence`;
3. a **Run** line: commands, exit codes, counts, and flaky tests;
4. a **Findings** table: `severity (CRITICAL/MAJOR/MINOR) | file:line | issue | evidence | owning stage / fix`;
5. the verdict **ON COURSE** or **HOLD: <CRITICAL findings and failing items>**.

Any CRITICAL finding or FAIL is a hard stop. Fix it or escalate it; never continue building past one silently.
