---
name: landing
description: Pre-production landing checklist. Use before merging to the integration branch, cutting a release, or deploying to production — asks the honest questions that are easy to skip at the end: is this actually ready for production, where would a latent bug hide (never-executed paths, swallowed errors, races, the test we avoided writing), and did we keep it simple rather than over-engineered (speculative abstractions, one-caller indirection, unjustified new dependencies, residue).
---

# Landing — Production Readiness Checklist

Purpose: the last honest look before the work touches production. By this point everything is green and the temptation is to declare victory — this checklist exists to force the three questions that green checks do not answer: **are we actually ready** (not "do the tests pass" but "do we know what breaks, how we'd find out, and how we'd back out"), **where would a bug hide** (the code paths nothing has ever executed, the errors that vanish silently, the test that was avoided), and **did we ship the simplest thing that works** (or did we build abstractions, options, and layers for a future that may never come).

## Workflow position

**3 of 3 — run last.** Use after `before-startup` and the applicable `cruising` gates have passed, when the completed change is awaiting final approval, merge, release, or production deployment. This is the terminal production-readiness gate, not an implementation-phase checklist.

## How to run

Run this before: final PR approval / merge into the integration branch, cutting a release, or any production deploy. Evaluate every item against real evidence — command output, the actual final diff, quoted docs, observed behavior — never from memory or optimism. Honesty is the point: an evasive answer ("should be fine", "low risk", "probably covered") is a FAIL for that item. Then produce the report in the format below.

## READINESS — are we actually ready for production?

1. **The uncomfortable truth** — state plainly: which part of this change are you least confident about, and what are you hoping nobody asks? Every change has a weakest point; "nothing" is itself a FAIL. Name it, then show the evidence that it holds — or record it as an accepted risk with an owner.
2. **Validation on the final state** — build, typecheck, lint, and the full test suite ran against the branch tip as it will merge — not an earlier commit before the last "small fix". Report the real numbers.
3. **Ran for real** — the change was exercised end-to-end in a production-like environment (staging smoke, emulator flow, the real app), not only in unit tests. Name what was actually invoked and what was observed. A feature nobody has watched work has not been verified.
4. **Failure visibility** — if this misbehaves in production, how do we find out and how fast? Name the concrete signal: a log phrase, a metric row, an error surface, an alert. "Users will report it" is a FAIL — that is the absence of a signal.
5. **Blast radius and rollback** — state what breaks if this change is wrong: which user-facing surfaces, scheduled jobs, and data. Is a plain revert safe, or does the change write data or emit events old code cannot read? Name the rollback mechanism and any point of no return.
6. **Deploy order honored** — every infra-before-code dependency (indexes, TTL policies, rules, env vars, secrets, migrations) named with the exact deploy sequence per repo rules, and what degrades if a step ships out of order.

## BUGS — where would a bug hide?

7. **Never-executed paths** — list every branch this change added that no test and no manual run has ever executed: error handlers, fallbacks, retries, rare-condition guards. Each one is a prime bug candidate — execute it now, or justify why it is provably correct by inspection.
8. **Hostile diff read** — re-read the complete final diff top to bottom as an adversarial reviewer looking for the bug, not as the author confirming the plan. Report anything that made you pause, even briefly — a pause is a signal.
9. **Edge inputs** — for the new code: empty, null/absent, zero, duplicate, oversized, concurrent, retried/redelivered, clock-skewed, timezone/DST-crossing, boundary-of-page inputs. Which of these can actually reach it, and what happens for each?
10. **Swallowed errors** — audit every catch/ignore/fallback in the diff: what disappears silently, and would anyone ever know it happened? A silent catch with no log and no counter is a future debugging session with no evidence.
11. **Idempotency and races** — can this code run twice (retry, at-least-once delivery, double-click, two instances, overlapping schedule)? What duplicates, corrupts, or double-charges when it does?
12. **The avoided test** — which test did we not write because it would be hard to set up or might fail? That instinct is information. Write it now, or record it as an explicit accepted risk with an owner — never let it stay unspoken.
13. **Contract re-check on the final diff** — the documented invariants for every touched area (project CLAUDE.md, feature KNOWLEDGE.md, decisions/pitfalls ledger) verified against the diff as it stands now — not against the plan from before implementation drifted.

## SIMPLICITY — did we build the simplest thing that works?

14. **Half-the-code test** — could this change be half the size and still work? For each new abstraction (class, layer, wrapper, indirection, config surface): name the second caller or concrete case that justifies it today. One caller means inline it.
15. **Speculative generality** — list every flag, option, parameter, mode, and extension point built for an imagined future rather than a present requirement. Delete them — the future can add them back with better information than we have now.
16. **New dependency and pattern audit** — every new package, pattern, or utility justified against the existing alternative already in the codebase. Consistency beats cleverness; a second way to do the same thing is a cost, not a feature.
17. **Five-minute explanation** — can each touched module be explained to a teammate in five minutes? If explaining it requires walking through the history of how it got this way, it is too complex — simplify before landing, not after.
18. **Residue swept** — dead code, commented-out blocks, tombstone comments, `*_old`/`v2` names, debug logging, leftover scaffolding, TODOs without tickets: all gone. Land the end-state, not the transition — git holds the history.

## Report format

Output a table: `# | item | PASS/FAIL/N-A | one-line evidence`. Follow with a verdict line: **CLEAR TO LAND** or **GO-AROUND: <failing items>**. A FAIL is a hard stop — never land past one silently; fix it or escalate to the user. An honest GO-AROUND is cheaper than an incident.
