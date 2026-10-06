---
name: cruising
description: Repeating FORDEC control cycle for implementation work. Use before launching or resuming an agent, committing a phase, or opening or updating a PR to establish Facts, compare Options, assess Risks and Benefits, make a Decision, Execute it with TDD and operational discipline, and Check results, drift, and monitoring.
disable-model-invocation: true
---

# Cruising — Repeating FORDEC Control Cycle

Purpose: prevent implementation momentum from turning assumptions into facts. Run the aviation-derived **FORDEC** sequence at every meaningful boundary:

1. **Facts**
2. **Options**
3. **Risks & Benefits**
4. **Decision**
5. **Execution**
6. **Check**

## Workflow position

**2 of 3 — repeat during implementation.** Use after `before-startup` has cleared the initial departure. Run a complete cycle at each **LAUNCH**, **COMMIT**, and **PR** boundary. Hand off to `landing` only after the PR cycle is checked and the completed change is ready for its final production decision.

## How to run

First name the boundary:

- **LAUNCH** — starting or resuming an agent or implementation phase;
- **COMMIT** — closing a phase or preparing a commit;
- **PR** — opening or updating a pull request.

Then run F → O → R → D → E → C in order for that boundary. Use command output, file paths, quoted contracts, and observed behavior. Do not choose an option before comparing risks and benefits. New material facts during Execution invalidate the decision and restart the cycle at Facts.

## F — FACTS

1. **Boundary and working tree** — identify LAUNCH, COMMIT, or PR; run `git status`; account for every uncommitted file and any partial output from a previous or killed agent. Never treat ambient changes as belonging to the current task.
2. **Architecture and contracts** — state the layer, module boundary, dependency direction, established pattern, documented invariants, and one-way-door contracts affected by the work. Cite their sources.
3. **Scope and delta** — compare the actual diff and commits with the ticket, plan, and current phase exit criteria. Name adjacent or deferred work that has entered the diff.
4. **Agent and environment state** — for LAUNCH, verify the delegation contains the goal, exact paths, binding plan substance, constraints, and session decisions; verify agent identity directly when resuming; confirm the machine, connection, services, and quota can survive the run.
5. **Quality evidence** — for COMMIT or PR, show RED evidence for each new behavior, current build/typecheck/lint/test output, end-to-end observations, failed attempts, and unresolved risks. Green tests alone do not prove the RED phase occurred.
6. **Operational state** — for PR, identify production surfaces, live-data and client compatibility, indexes, TTLs, rules, variables, secrets, scheduled work, migrations, manual steps, and repository deployment constraints.

## O — OPTIONS

7. **Viable courses** — list the realistic choices for this boundary:
    - LAUNCH: proceed with the planned approach, choose an established alternative, reduce or split scope, obtain a missing decision, or hold;
    - COMMIT: commit as one unit, split the change, remove drift, add missing evidence, revise the design, or hold;
    - PR: open or update now, reduce scope, stage behind a control, complete operational prerequisites, or hold.
8. **Fallback course** — include the safest recovery or no-go option. Do not present a destructive action, silent scope increase, or unapproved one-way-door decision as routine execution.

## R — RISKS & BENEFITS

9. **Engineering tradeoffs** — for every option, compare correctness, architectural fit, simplicity, reviewability, delivery speed, reversibility, dependency cost, and maintenance burden. Name the concrete present-day benefit; speculative flexibility does not count.
10. **Failure interrogation** — evaluate failure, retry, duplicate delivery, concurrency, partial execution, empty or hostile input, cancellation, 10× scale, and the single assumption that would invalidate the option.
11. **Production exposure** — for PR, compare blast radius, degradation mode, rollback safety, live-data compatibility, infrastructure-before-code hazards, notification needs, and the observability available if the option fails.

## D — DECISION

12. **Explicit course** — select one option before acting. State the rationale, in-scope result, deferred work, exit criteria, accepted risks and owners, rollback or recovery course, and evidence that will prove success.
13. **Approval gate** — obtain explicit user approval for schema shapes, public APIs, event formats, irreversible data writes, new production dependencies, destructive actions, or any option with no safe rollback. Without approval, the decision is **HOLD**.

## E — EXECUTION

14. **LAUNCH execution** — send a self-contained delegation, preserve existing user work, ensure the environment will remain available, and implement through RED → GREEN → REFACTOR using the selected architecture.
15. **COMMIT execution** — remove out-of-scope work, satisfy the phase exit criteria, run the repository's targeted validation, encode lessons from failed attempts, and prepare the smallest coherent commit. Do not commit unless the user requested it.
16. **PR execution** — prepare the exact deployment sequence and complete operational notes with explicit yes/no entries for indexes, TTLs, variables/secrets, scheduled functions, migrations, notifications, and manual commands. Do not open or update a PR unless the user requested it.

## C — CHECK

17. **Decision conformance** — compare the result with the selected option, architecture, scope, contracts, and exit criteria. Name every deviation; revert it or reopen FORDEC rather than accepting silent drift.
18. **Observed verification** — report the actual build, typecheck, lint, test, and end-to-end outputs applicable to the boundary. Confirm every new behavior and every reachable failure path has evidence.
19. **Risk and lesson closure** — restate each open risk with its current status and owner. Record the root cause of failed attempts in the repository's durable learning mechanism where one exists.
20. **Monitoring trigger** — define the signal, observation window, threshold, and owner that will reveal failure after this boundary. State the condition that reopens the cycle or causes a rollback, pause, or go-around.

## Report format

Output:

1. `Boundary: LAUNCH | COMMIT | PR`;
2. a `Stage | # | item | PASS/FAIL/N-A | evidence` table;
3. an **Options** list with one-line Risks and Benefits for each;
4. a **Decision** line with rationale, owner, exit criteria, and accepted risks;
5. an **Execution** line with actions actually completed;
6. a **Check** line with observed results and the monitoring trigger;
7. the verdict **CLEAR TO PROCEED** or **HOLD: <failing items or reopen conditions>**.

A FAIL is a hard stop. Fix it, select another option, or escalate it; never proceed silently.
