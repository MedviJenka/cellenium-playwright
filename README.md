# Cellenium Playwright

Cellenium Playwright is an experimental Python browser-automation toolkit built on [Playwright](https://playwright.dev/python/). It provides browser lifecycle management, a Google-Sheets-backed Page Object Model (POM), screenshot capture, and components for structured visual analysis with CrewAI.

The repository also contains **TestFlow**, a set of Claude Code skills that turns product requirements and technical specifications into traceable pytest tests, validated UI locators, execution evidence, and a test-quality verdict.

> **Status:** active development. The browser and locator layers are usable, but the checked-in vision test is still a scaffold and does not currently pass. Install it from PyPI with `pip install cellenium` (or `uv add cellenium`), then run `playwright install chromium`. Configuration (`.env`, `credentials.json`) is read from your project's working directory.

## Features

- Synchronous Chromium, Firefox, or WebKit sessions through Playwright.
- Reusable `PageEngine` helpers for navigation, locators, screenshots, scrolling, dropdowns, and tabs.
- Page Object Model data read directly from Google Sheets at runtime.
- Locator strategies for name, XPath, ID, CSS, class name, link text, and tag name.
- Structured image-analysis components built with CrewAI and Pydantic.
- Parallel pytest execution in CI on Python 3.13 and 3.14.
- Optional TestFlow skills for end-to-end pytest test generation and evaluation.

## Requirements

- Python 3.13 or 3.14
- [`uv`](https://docs.astral.sh/uv/)
- A Playwright-supported browser
- A Google service account for resolving locators
- An OpenAI-compatible model and API key when using the vision components

## Quick start

Clone the repository and install the locked dependencies:

```sh
git clone https://github.com/MedviJenka/cellenium-playwright.git
cd cellenium-playwright
uv sync --frozen
```

Install Chromium:

```sh
uv run playwright install chromium
```

On Ubuntu or another Debian-based CI runner, install Chromium and its system dependencies together:

```sh
uv run playwright install --with-deps chromium
```

## Configuration

In the project where you use cellenium, run:

```sh
cellenium init     # writes a .env template, adds .env and credentials.json to .gitignore, installs Chromium
cellenium doctor   # checks settings, credentials.json, Google Sheet access, and that Chromium launches
```

`cellenium init --with-deps` also installs Chromium's system libraries (Linux/CI). `cellenium doctor --offline` skips opening the sheet; it exits non-zero when a check fails, so it can gate CI.

Settings are read from `.env` in the working directory or from environment variables:

```dotenv
GOOGLE_SHEETS=<spreadsheet-edit-url>
CREDENTIALS_JSON=credentials.json
OPENAI_MODEL=<model-name>
OPENAI_API_KEY=<optional-api-key>
LOGFIRE_TOKEN=<optional-logfire-token>
TEST_HEADLESS=true
```

`GOOGLE_SHEETS` selects the locator spreadsheet. When `LOGFIRE_TOKEN` is omitted, logging remains local and no data is sent to Logfire.

Save the Google service-account key as `credentials.json` and share the locator spreadsheet with its `client_email` as a viewer (`cellenium doctor` prints the address). Never commit `.env` or `credentials.json`.

## Google Sheets Page Object Model

Each worksheet tab represents one screen. The first row must contain these columns:

| Column | Purpose |
|---|---|
| `name` | Logical element name used by tests |
| `locator` | Locator strategy such as `NAME`, `XPATH`, `ID`, or `CSS` |
| `type` | Locator value; this name is retained for compatibility with the source sheet |
| `actions` | Optional metadata |
| `comments` | Optional notes |

Example worksheet:

| name | locator | type | actions | comments |
|---|---|---|---|---|
| search | NAME | q | fill | Google search field |
| button | NAME | btnK | click | Search button |

`PageEngine(screen="Google")` reads locator rows directly from the worksheet tab
named `Google`. No generated JSON mapping or synchronization step is required.

## Browser automation

```python
from src.core.engine.page_engine import PageEngine

engine = PageEngine(screen="Google", headless=True)

try:
    engine.get_web("https://www.google.com")
    engine.get_element("search").fill("cats")
    engine.get_element("button").click()
    screenshot = engine.get_screenshot("google-results")
    print(screenshot)
finally:
    engine.teardown()
```

`screen="Google"` selects the worksheet tab named `Google`. With multiple tabs, pass the page's tab name when constructing `PageEngine` (for example, `Google`, `Heroku`, or `ST`). Missing worksheets, missing element names, and unsupported locator strategies raise explicit exceptions.

## Tests and linting

Run the test suite:

```sh
uv run --frozen pytest src/tests tests -v -n auto --dist loadscope
```

`src/tests/test_google_search.py` exercises the live browser flow. The unit regressions in `tests/` cover screenshot persistence and direct worksheet selection without contacting external services.

Run the blocking CI lint checks:

```sh
uvx --from flake8==7.4.1 flake8 main.py settings.py src \
  --count --select=E9,F63,F7,F82 --show-source --statistics
```

The GitHub Actions workflow in `.github/workflows/python-package.yml` performs locked dependency installation, installs Chromium, runs lint checks, and executes the tests under Xvfb for Python 3.13 and 3.14.

## TestFlow Claude Code skills

TestFlow separates pytest creation into focused stages:

```text
PRD → test specification → UI locators → pytest writer → executor → evaluator
```

| Order | Skill | Purpose |
|---:|---|---|
| Optional | `web` | Explore a live application in a real browser and produce reproducible bug evidence |
| 1 | `prd-reader` | Extract explicit, derived, and unknown test requirements from the PRD |
| 2 | `test-spec` | Design traceable pytest cases, boundaries, fixtures, and execution prerequisites |
| 3 | `locator-writer` | For UI cases, validate stable Playwright selectors and upsert elements into Google Sheets |
| 4 | `writer` | Implement deterministic, behavior-focused pytest tests |
| 5 | `executor` | Run collection, targeted tests, related tests, and classify failures |
| 6 | `evaluator` | Evaluate traceability, regression sensitivity, coverage quality, and execution evidence |

`artifact` orchestrates the complete pipeline and repeats only the affected downstream stages when evaluation finds a defect.

`web` is a report-only exploratory entry point. Verified findings become regression candidates for `test-spec`; it does not modify application code.

Validate the Claude Code plugin metadata:

```sh
claude plugin validate .
```

Run Claude Code from the repository and invoke either the complete pipeline or an individual stage:

```text
/testflow:web
/testflow:artifact
/testflow:prd-reader
/testflow:test-spec
/testflow:locator-writer
/testflow:writer
/testflow:executor
/testflow:evaluator
```

The skills are manual-only. The locator writer previews changes before replacing existing Google Sheet selectors and verifies selectors against the live UI.

The separate checklist skills live under `.claude/skills/checklist/`: `before-startup` (system ready to build tests), `cruising` (everything in place, critical errors and potential bugs), `landing` (final production readiness), and the standalone `fordec` emergency decision skill.

## Project layout

```text
.github/workflows/               GitHub Actions CI
.claude/skills/testflow/         Pytest TestFlow skill definitions
.claude/skills/checklist/        Checklist skills (before-startup, cruising, landing, fordec)
.claude/commands/testflow/       TestFlow slash-command entries
.claude-plugin/plugin.json       Claude Code plugin metadata
src/core/engine/                 Playwright browser and page engines
src/core/functions/              Locator resolution and direct Google Sheets access
src/core/ai/                     CrewAI configuration and vision components
src/tests/                       Browser test scenarios
settings.py                      Environment-backed runtime configuration
pyproject.toml                   Python requirements and dependencies
uv.lock                          Reproducible dependency lockfile
```

## Known limitations

- The checked-in vision test uses a placeholder `VisionAssertion` without a `run()` implementation.
- The sample end-to-end test depends on Google and is not hermetic.
- Configuration currently requires fields that are reserved but not consumed by every component.
- The project does not yet define a wheel/sdist build or publishing workflow.

## License

Licensed under the [ISC License](LICENSE). Copyright © 2026 Jenia Petrusenko.
