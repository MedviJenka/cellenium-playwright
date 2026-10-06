---
name: executor
description: Run repository-native pytest commands, preserve exact evidence, and classify collection, environment, test, and product failures.
argument-hint: <test paths, node IDs, or markers>
command: /testflow:executor
---

Invoke the Skill tool with `skill: "testflow:executor"` before doing anything else. 
Pass `$ARGUMENTS` as the requested test selection and report exact commands, 
results, failure classifications, and verdict.
