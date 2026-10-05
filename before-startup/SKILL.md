---
name: before-startup
description: FORDEC departure checklist for software work. Use before writing implementation code to establish Facts, compare Options, assess Risks and Benefits, make an explicit Decision, Execute the departure plan, and Check that the branch, baseline, dependencies, environment, and task are safe to proceed.
---

# Before Startup — FORDEC Departure Checklist

Purpose: make the first implementation move deliberately. This skill adapts the aviation **FORDEC** decision model to software delivery:

1. **Facts** — establish the current state from fresh evidence.
2. **Options** — identify viable courses of action, including holding position.
3. **Risks & Benefits** — compare each option without hiding tradeoffs.
4. **Decision** — select and state the course before acting.
5. **Execution** — carry out the selected departure plan.
6. **Check** — verify the expected state and monitor for reasons to reconsider.

## Workflow position

**1 of 3 — run first.** Use once before implementation starts. After this cycle is clear, use `cruising` for repeated FORDEC cycles at launch, commit, and PR boundaries. Use `landing` only for the final production-readiness cycle.

## How to run

Run the stages in order. Do not jump from Facts to Execution. Use fresh command output, repository rules, and observed state; memory and phrases such as "probably clean" are not evidence. A destructive action, history rewrite, protected-branch change, or one-way-door decision requires explicit user approval.

## F — FACTS

1. **Integration branch and remote state** — identify the integration branch from repository evidence, fetch the remote, and report the exact divergence between `HEAD` and `origin/<integration>`. Never assume the branch is `main`.
2. **Branch and working-tree state** — report the current branch, commits ahead of the integration branch, every modified or untracked file, and any merge, rebase, or cherry-pick in progress. Distinguish existing user work from task work.
3. **Baseline state** — run the repository's build, typecheck, lint, and test commands before implementation. Report actual results and pre-existing failures.
4. **Dependencies and environment** — verify the lockfile and installed dependencies agree, then name every required variable, secret, emulator, service account, or local service and its observed status. Never expose secret values.
5. **Traffic and blockers** — identify open PRs, active branches, upstream work, unresolved product or architecture decisions, and missing contracts that can collide with or block the task.

## O — OPTIONS

6. **Viable departures** — list the safe courses available from the facts. Typical options include creating a fresh branch from the remote tip, updating the current task branch, isolating existing work before branching, splitting the scope, coordinating an overlap, or holding position. Exclude any option that would overwrite user work.
7. **No-go option** — always include stopping to resolve a red baseline, missing prerequisite, unsafe branch state, or unresolved one-way-door decision. "Proceed anyway" is not an option when evidence is missing.

## R — RISKS & BENEFITS

8. **Compare every option** — state the concrete benefit and risk of each option: lost work, history rewrite, merge-conflict debt, ambiguous test failures, dependency drift, environment mismatch, duplicated effort, or delay.
9. **Irreversibility check** — identify protected-branch changes, force updates, destructive cleanup, public contracts, schema shapes, event formats, or data writes that cannot be safely reversed. Mark each as requiring user approval.

## D — DECISION

10. **Departure decision** — choose one option and state why its benefits outweigh its risks. Name the branch, base commit, task scope, unresolved accepted risks, owner, and the evidence that will permit execution. If the safe choice is to hold, say **NO-GO** and name the unblock condition.

## E — EXECUTION

11. **Execute the selected plan only** — fetch or synchronize as decided, create or switch to the correctly named task branch, isolate unrelated changes without discarding them, install locked dependencies, and resolve the named blockers. Do not improvise a different course mid-execution; new facts reopen the FORDEC cycle.

## C — CHECK

12. **Departure verification** — confirm all of the following from fresh evidence:
    - the current branch is task-specific and not protected;
    - its base is the intended remote integration tip;
    - every ahead commit belongs to this task;
    - the working tree contains no unexplained residue;
    - the baseline is green, or every pre-existing failure is explicitly accepted;
    - dependencies and environment are ready;
    - no unresolved collision or prerequisite blocks implementation.
13. **Monitoring trigger** — state what could invalidate the decision after departure, such as a conflicting PR merging, the integration branch moving, an environment dependency failing, or a contract changing. Name how it will be detected and when to run FORDEC again.

## Report format

Output:

1. a `Stage | # | item | PASS/FAIL/N-A | evidence` table;
2. an **Options** list with one-line Risks and Benefits for each;
3. a **Decision** line: selected option, rationale, owner, and accepted risk;
4. an **Execution** line: actions actually completed;
5. a **Check** line: observed final state and monitoring trigger;
6. the verdict **CLEAR TO DEPART** or **NO-GO: <failing items or unblock conditions>**.

A FAIL is a hard stop. Never begin implementation past one silently.
