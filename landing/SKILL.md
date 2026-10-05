---
name: landing
description: Final FORDEC production-readiness cycle. Use before final PR approval, merge, release, or production deployment to establish Facts, compare land and go-around Options, assess Risks and Benefits, make an explicit Decision, define or perform the authorized Execution, and Check production signals with rollback triggers.
---

# Landing — Final FORDEC Production Decision

Purpose: make the last pre-production decision with the discipline of the aviation **FORDEC** model:

1. **Facts**
2. **Options**
3. **Risks & Benefits**
4. **Decision**
5. **Execution**
6. **Check**

Green checks are inputs, not the decision. The final cycle must expose the weakest evidence, compare landing with a go-around, state who accepts residual risk, and define how production will be monitored.

## Workflow position

**3 of 3 — run last.** Use after `before-startup` and the applicable `cruising` cycles have passed, when the completed change awaits final approval, merge, release, or deployment. This is the terminal production-readiness cycle.

## How to run

Run F → O → R → D → E → C in order against the final branch state. Evidence must come from the actual final diff, branch-tip validation, observed end-to-end behavior, repository rules, and deploy configuration. Do not merge, release, or deploy unless the user has authorized that action. If new facts appear during Execution or Check, stop and restart the cycle.

## F — FACTS

1. **Uncomfortable truth** — name the part of the change with the weakest evidence and the question you most hope nobody asks. "Nothing" is a FAIL. Prove it safe or record it as residual risk with an owner.
2. **Final state** — identify the exact branch tip and re-read the complete final diff adversarially. Confirm documented invariants for every touched area against what was built, not the original plan.
3. **Validation evidence** — report build, typecheck, lint, full-suite, and relevant targeted-test results from the final state. Identify every changed branch that no test or manual run executed.
4. **Operational evidence** — report the production-like end-to-end run, concrete failure signals, expected logs or metrics, affected user surfaces and jobs, data compatibility, rollback mechanism, and point of no return.
5. **Deployment readiness** — list indexes, TTL policies, rules, variables, secrets, migrations, scheduled work, notifications, manual steps, and exact ordering constraints. State what happens if code arrives before infrastructure.

## O — OPTIONS

6. **Landing choices** — list the viable courses supported by the facts: land as-is, land through a staged or controlled rollout, fix and repeat the cycle, reduce scope, defer the change, or go around. Do not manufacture equivalence: eliminate any option that violates a hard invariant.
7. **Simpler option** — explicitly test whether half the code, fewer abstractions, an existing dependency or pattern, or a narrower change satisfies the requirement with less production exposure.
8. **Recovery options** — identify plain revert, feature or configuration disablement, forward fix, data repair, traffic shift, and full go-around. Mark unavailable recovery paths clearly.

## R — RISKS & BENEFITS

9. **Option comparison** — for each option, state user benefit, delivery benefit, operational burden, reversibility, blast radius, and the cost of delay. A vague "low risk" or "faster" is not evidence.
10. **Hidden-bug audit** — assess never-executed handlers, fallbacks, retries, edge inputs, oversized and duplicate inputs, swallowed errors, idempotency, races, overlapping schedules, clock skew, time zones, and page boundaries. Name what happens for every reachable case.
11. **Avoided-test audit** — name the test omitted because setup was hard or failure was likely. Run it, select an option that removes the exposure, or record the risk with an owner.
12. **Simplicity audit** — challenge one-caller indirection, speculative flags and modes, new packages or patterns, hard-to-explain modules, dead code, debug output, scaffolding, tombstone names, and TODOs without tickets. State the present requirement that justifies anything retained.
13. **Deployment risk** — assess live-data and in-flight-client compatibility, infra-before-code hazards, rollback after writes or emitted events, observability delay, and every point after which a go-around becomes harder.

## D — DECISION

14. **Land or go around** — select one option and state why its benefits outweigh its risks. Record approver, residual risks and owners, prerequisites, success criteria, rollback threshold, and any point of no return. If a hard gate lacks evidence, the decision is **GO-AROUND**.
15. **Authorization boundary** — distinguish approval of the readiness decision from authorization to merge, release, or deploy. Never infer production authorization from a request to review.

## E — EXECUTION

16. **Execute the authorized course** — complete required fixes and validation, then follow the exact approved merge, release, infrastructure, migration, and deployment order. Use the selected rollout controls and prepare the rollback commands before crossing the point of no return. If authorization stops at review, produce the execution plan without performing the release.

## C — CHECK

17. **Immediate verification** — after every executed step, verify the expected revision, environment, service health, user-visible behavior, data state, scheduled work, and required infrastructure. Report observed values, not "deployed successfully."
18. **Monitor and decide again** — define each signal, baseline, observation window, threshold, owner, and response. A breached threshold triggers the selected rollback or go-around and starts a new FORDEC cycle with the new facts.

## Report format

Output:

1. a `Stage | # | item | PASS/FAIL/N-A | evidence` table;
2. an **Options** table: `option | benefits | risks | reversibility`;
3. a **Decision** line: **LAND**, **STAGED LANDING**, or **GO-AROUND**, with rationale, approver, and residual-risk owners;
4. an **Execution** line: authorized actions completed or the exact pending plan;
5. a **Check** table: `signal | expected | threshold | window | owner | response`;
6. the verdict **CLEAR TO LAND** or **GO-AROUND: <failing items or unblock conditions>**.

A FAIL is a hard stop. Never land past one silently. An honest go-around is cheaper than an incident.
