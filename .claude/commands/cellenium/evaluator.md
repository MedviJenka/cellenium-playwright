---
name: evaluator
description: Evaluate pytest tests against requirements, specifications, implementation contracts, and execution evidence.
argument-hint: <requirements, tests, and execution results>
command: /cellenium:evaluator
---

Invoke the Skill tool with `skill: "testflow:evaluator"` 
before doing anything else. Pass `$ARGUMENTS` as the evaluation 
scope and return the coverage matrix, evidence-backed findings, residual risks, and verdict.
