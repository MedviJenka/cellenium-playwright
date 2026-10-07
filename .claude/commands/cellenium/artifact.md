---
name: artifact
description: Turn a PRD or specification into traceable pytest tests, execute them, and evaluate their quality through the complete TestFlow pipeline.
argument-hint: <PRD/spec path and test target>
command: /cellenium:artifact
---

Before doing anything else, read `.claude/skills/cellenium/artifact/SKILL.md` (or `~/.claude/skills/cellenium/artifact/SKILL.md` if it is not in the project) and follow it as your instructions. Each stage it names lives in a sibling folder, e.g. `prd-reader` is `.claude/skills/cellenium/prd-reader/SKILL.md`; read a stage's SKILL.md before applying it. 
Pass `$ARGUMENTS` as the pipeline input and complete every reachable TestFlow stage.
