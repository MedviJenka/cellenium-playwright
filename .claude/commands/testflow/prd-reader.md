---
name: prd-reader
description: Extract testable, traceable pytest requirements from a PRD, feature brief, ticket, or acceptance criteria.
argument-hint: <PRD path, issue, or requirements>
command: /testflow:prd-reader
---

Invoke the Skill tool with `skill: "testflow:prd-reader"` 
before doing anything else. Pass `$ARGUMENTS` as the product 
source and return the requirement matrix without running downstream stages.
