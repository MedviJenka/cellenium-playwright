---
name: evaluator
description: Evaluate pytest tests against requirements, specifications, implementation contracts, and execution evidence.
argument-hint: <requirements, tests, and execution results>
command: /cellenium:evaluator
---

Before doing anything else, read `.claude/skills/cellenium/evaluator/SKILL.md` (or `~/.claude/skills/cellenium/evaluator/SKILL.md` if it is not in the project) and follow it as your instructions. Pass `$ARGUMENTS` as the evaluation 
scope and return the coverage matrix, evidence-backed findings, residual risks, and verdict.
