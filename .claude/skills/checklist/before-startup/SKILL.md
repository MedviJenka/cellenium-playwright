---
name: before-startup
description: System readiness check before building tests. Use before starting TestFlow or writing any test to verify that the repository, toolchain, browsers, configuration, external services, test infrastructure, baseline, and inputs are healthy and ready for test creation.
disable-model-invocation: true
---

# Before Startup — Ready to Build Tests

Purpose: prove the system is healthy and ready to build tests before any test is designed or written. A test built on a broken environment produces failures that say nothing about the product.

## Workflow position

**1 of 3 — run first.** Use once before TestFlow (`prd-reader` → `test-spec` → `locator-writer` → `writer` → `executor` → `evaluator`) or any manual test work starts. When the verdict is **READY TO BUILD TESTS**, continue with `cruising` while tests are built. Use `landing` for the final check.

## How to run

Check every item from fresh command output and observed files. Memory and phrases such as "should be installed" are not evidence. Discover the real commands from the repository (`pyproject.toml`, `uv.lock`, CI workflow, README) before running them.

Do not fix anything silently. For each FAIL, give the exact fix command or action. Run only non-destructive setup (for example `uv sync --frozen` or `playwright install chromium`) when the user agrees. Never print secret values. Report only whether a secret is present and valid.

## 1. Repository

1. **Branch and working tree:** report the current branch, every modified or untracked file, and any merge, rebase, or cherry-pick in progress. Separate existing user work from work for this task.
2. **Integration state:** fetch the remote and report divergence from the integration branch. Do not assume it is `main`.

## 2. Toolchain and dependencies

3. **Python:** confirm the active interpreter matches the version `pyproject.toml` requires.
4. **Locked dependencies:** confirm the lockfile and environment agree (for example `uv sync --frozen` succeeds with no changes) and that `pytest`, its plugins (such as `pytest-xdist`), and `playwright` import.
5. **Browsers:** confirm the required Playwright browser is installed and launches. Run a headless launch smoke check, not just a file lookup.

## 3. Configuration and secrets

6. **Environment variables:** confirm `.env` exists and that every variable the settings contract requires is set and non-empty. List names only.
7. **Credentials:** confirm required credential files (such as `credentials.json`) exist, parse, and contain the expected fields. Confirm they are ignored by Git.
8. **Settings import:** import the settings module and confirm validation passes with no missing or malformed fields.

## 4. External services

9. **Application under test:** confirm the target URL or service responds with the expected page or status from this machine.
10. **Locator source:** for UI work, confirm the Google Sheet is reachable with the service account and that every worksheet/screen required by the target flow can be read directly.
11. **AI and model services:** when vision or LLM components are used, confirm the configured model and API key work with a minimal call.

## 5. Test infrastructure

12. **Collection:** `pytest --collect-only` completes with zero import, syntax, or fixture errors.
13. **Fixtures and engine:** shared fixtures and `conftest.py` import, and a browser session can be opened and torn down cleanly with no leaked processes.
14. **Output paths:** screenshot, report, and artifact directories exist and are writable.

## 6. Baseline

15. **Lint:** run the blocking CI lint command and report the result.
16. **Existing suite:** run the existing tests and record every pre-existing failure with its cause. New failures must be distinguishable from this baseline later.

## 7. Inputs for building tests

17. **Requirements:** the PRD, ticket, spec, or acceptance criteria exist and are readable.
18. **Target and data:** the flow, module, or endpoint under test is identified, and the required test accounts, data, and permissions are available.
19. **Blocking unknowns:** list any open product question that would change an expected result. An unresolved one is a FAIL for the affected scope.

## Report format

Output:

1. a `Area | # | item | PASS/FAIL/N-A | evidence` table;
2. a **Fixes** list: the exact command or action for every FAIL;
3. a **Baseline** line: pre-existing failures that are accepted;
4. the verdict **READY TO BUILD TESTS** or **NOT READY: <failing items>**.

A FAIL is a hard stop. Never start building tests past one silently.
