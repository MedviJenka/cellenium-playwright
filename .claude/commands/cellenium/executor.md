---
name: executor
description: Run repository-native pytest commands, preserve exact evidence, and classify collection, environment, test, and product failures.
argument-hint: <test paths, node IDs, or markers>
command: /cellenium:executor
---

Before doing anything else, read `.claude/skills/cellenium/executor/SKILL.md` (or `~/.claude/skills/cellenium/executor/SKILL.md` if it is not in the project) and follow it as your instructions. 
Pass `$ARGUMENTS` as the requested test selection and report exact commands, 
results, failure classifications, and verdict.
