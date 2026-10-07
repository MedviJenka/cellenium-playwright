---
name: locator-writer
description: Discover stable Playwright element locators, validate them against the live page, and upsert the element records into the repository's Google Sheets Page Object Model. Use when UI pytest cases need missing or corrected screen elements in the shared locator sheet.
disable-model-invocation: true
---

# Locator and Element Writer

Create reliable Page Object Model entries for UI tests and write them to the configured Google Sheet. Use this stage after `test-spec` identifies required UI interactions and before `writer` implements tests that depend on those elements.

## Inputs

Require:

- the target page or route;
- the worksheet/screen name;
- the `TST-*` cases or interaction list;
- an available browser session or reproducible navigation path;
- `.env` with `GOOGLE_SHEETS` and `credentials.json` for writes.

If the actual page cannot be inspected, do not guess selectors from prose or screenshots. Return the unresolved elements as blocked.

## Sheet contract

Each worksheet is one screen. Preserve these columns exactly:

| Column | Value |
|---|---|
| `name` | Stable logical element name used by `PageEngine.get_element()` |
| `locator` | Supported strategy: `NAME`, `XPATH`, `ID`, `CSS`, `CLASS_NAME`, `LINK_TEXT`, or `TAG_NAME` |
| `type` | Selector value consumed by the strategy |
| `actions` | Intended interactions such as `fill`, `click`, `select_option`, or `assert_visible` |
| `comments` | Purpose, state constraints, or selector rationale |

The repository parser intentionally maps sheet column `locator` to internal field `type` and sheet column `type` to internal field `value`. Do not “correct” those headers.

## Process

1. **Read before writing**
   - Load the target worksheet directly from Google Sheets.
   - Index existing rows by normalized `name`.
   - Detect duplicate names, unsupported strategies, and empty selector values.
   - Never clear or replace an entire worksheet.

2. **Inspect the real UI**
   - Navigate through the same state and permissions required by the test case.
   - Inspect each required interactive or asserted element in its relevant state.
   - Record elements only when a planned test action or assertion requires them.

3. **Choose stable locators**
   - Prefer a unique stable `ID` or `NAME` owned by the application.
   - Next prefer `CSS` using a stable `data-testid`, semantic attribute, or application-owned identifier.
   - Use exact `LINK_TEXT` only when visible link text is a stable product contract.
   - Use `CLASS_NAME` or `TAG_NAME` only when unique and semantically stable.
   - Use `XPATH` last, and keep it relative to stable attributes rather than DOM position.
   - Reject generated IDs, hashed classes, index-based selectors, deep CSS chains, and selectors tied to presentation.

4. **Validate every locator**
   - Resolve it with the same Playwright strategy used by `src/core/functions/locators.py`.
   - Require exactly one intended match in the relevant state.
   - Verify the element is attached and supports the planned action.
   - Recheck after a page reload or repeated navigation when the application is dynamic.
   - A locator that merely finds “something” is invalid.

5. **Prepare an upsert diff**
   - `ADD`: new logical name.
   - `UPDATE`: existing row whose selector, actions, or comments must change.
   - `UNCHANGED`: existing row already satisfies the test.
   - `CONFLICT`: duplicate name, changed ownership, or uncertain replacement.
   - Show old and new values for updates. Obtain user approval before overwriting an existing non-empty selector or resolving a conflict.

6. **Write safely with gspread**
   - Authenticate with `gspread.service_account(filename="credentials.json")`.
   - Open the spreadsheet ID or URL from `Config.GOOGLE_SHEETS`.
   - Create the worksheet only when the requested screen does not exist and creation is authorized.
   - Update matching rows in place; append new rows in one batch.
   - Preserve unrelated rows, columns, formatting, and worksheet order.
   - Never print credential contents or API keys.

7. **Verify direct retrieval**
   - Read the target screen with `fetch_locators(screen)` after a successful write.
   - Confirm each written row is returned with the mapped `type`, `value`, `actions`, and `comments` fields.
   - Resolve each locator once more through `PageEngine` or `get_locator`.
   - Hand the verified logical names to `writer`.

## Naming rules

Use concise snake_case names based on purpose, not markup:

- `email_input`
- `submit_button`
- `validation_error`
- `account_menu`

Avoid `div_3`, `blue_button`, `left_panel_item`, and selector text in the name.

## Output contract

### Element plan

| Test IDs | Screen | Name | Action/assertion | Strategy | Selector |
|---|---|---|---|---|---|

### Sheet diff

| Operation | Screen | Name | Previous row | New row | Validation |
|---|---|---|---|---|---|

### Verification

Report the spreadsheet/worksheet identifiers without secret data, direct lookup results, and live Playwright match results.

### Blockers

List pages that could not be reached, states that could not be reproduced, ambiguous selectors, missing write access, or conflicts requiring a product decision.

## Quality gate

The locator stage is complete only when:

- every UI interaction in the approved test specification has a logical element entry;
- each new or updated locator matches exactly the intended element;
- no selector depends on generated or positional markup when a stable attribute exists;
- sheet mutations are limited to the approved rows;
- direct worksheet retrieval returns the Google Sheet values;
- `writer` can use logical names without embedding raw selectors in tests.
