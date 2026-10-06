---
name: test-spec
description: Convert requirements and technical specifications into a complete, traceable pytest test specification.
argument-hint: <requirements/spec path and target>
command: /testflow:test-spec
---

Invoke the Skill tool with `skill: "testflow:test-spec"` before doing anything else. Pass `$ARGUMENTS` as specification context and return the test strategy, cases, file plan, environment contract, and traceability map.
