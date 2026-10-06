---
name: writer
description: Implement approved test cases as deterministic, behavior-focused pytest tests that follow repository conventions.
argument-hint: <test specification and target>
command: /testflow:writer
---

Invoke the Skill tool with `skill: "testflow:writer"` 
before doing anything else. Pass `$ARGUMENTS` as the 
approved test specification, write the pytest tests, and return collection plus targeted execution evidence.
