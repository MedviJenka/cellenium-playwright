---
name: locator-writer
description: Discover stable Playwright locators, validate the target elements, and upsert them into the configured Google Sheets Page Object Model.
argument-hint: <page, screen, and required elements>
command: /testflow:locator-writer
---

Invoke the Skill tool with `skill: "testflow:locator-writer"` 
before doing anything else. Pass `$ARGUMENTS` as the UI target and element requirements. 
Preview updates before replacing existing non-empty sheet rows.
