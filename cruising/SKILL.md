---
name: cruising
description: Pre-flight error-prevention checklist. Use before launching or resuming an implementation agent, committing a phase of work, or opening a PR — verifies working-tree state, delegation prompt completeness, environment survival, architecture fit, hard-question interrogation, TDD evidence, documented contracts, production blast radius, deploy-order hazards, exit gates, and operational notes.
---

# Cruising — Pre-Flight Checklist

Purpose: catch the errors that historically cost retries — stale uncommitted agent output, non-self-contained delegations, host sleep killing long runs, missing RED-phase tests, violated documented invariants, infra-before-code deploy hazards, and incomplete PR operational notes — and force the questions that are easy to skip: does this fit the architecture, what breaks in production if it's wrong, and which uncomfortable assumption invalidates the design.

## Workflow position

**2 of 3 — run during implementation.** Use after `before-startup` has cleared the initial branch and baseline. Re-run the applicable LAUNCH, COMMIT, or PR sections at each phase boundary. Hand off to `landing` only when the final PR is ready to merge, release, or deploy.

## How to run

Determine which stage(s) apply right now: **LAUNCH** (starting or resuming an agent or phase), **COMMIT** (closing a phase), **PR** (opening or updating a PR). Evaluate every item in the applicable sections against real evidence (command output, file paths, quoted docs) — never from memory. Then produce the report in the format below.

## LAUNCH — before starting or resuming any agent or phase

1. **Working-tree audit** — run `git status`; identify every uncommitted file. Is any of it partial output from a previous or killed agent run? The launch plan must explicitly reuse it or discard it — never leave it ambient for the next agent to trip over.
2. **Self-contained delegation** — the agent prompt must carry the goal, exact file paths, the binding plan/design-doc substance (not just a pointer), constraints, and relevant session decisions. Subagents see none of the conversation.
3. **Environment survival** — will the machine stay awake and connected for the run's duration? Lid-close/clamshell sleep kills long runs, and `caffeinate` does NOT prevent lid-close sleep. Also check spend-cap/quota headroom for long runs.
4. **Identity over liveness** — when resuming or coordinating with another session/agent, verify identity directly (direct ping, file mtimes). "A process exists and is busy" is not proof it is the one you think it is.
5. **Architecture fit** — state where the change sits in the existing architecture (layer, module boundary, dependency direction) and confirm it follows established patterns, citing the pattern it follows. Any new pattern, dependency, or boundary crossing must be named and justified against the existing alternative. One-way-door decisions (schema shapes, public API contracts, event/message formats, data written in a new form) require explicit user sign-off before implementation starts.
6. **Hard questions surfaced** — enumerate the uncomfortable questions the plan glosses over: what happens under failure, retry, concurrency, partial deploy, empty or hostile input, and 10x scale; which single assumption, if wrong, invalidates the design. Answer each with evidence or record it as an explicit open risk with an owner. "No hard questions found" is itself a FAIL.

## COMMIT — before committing a phase

7. **RED evidence** — for each new behavior, show the failing test that existed before the implementation (test-run log or commit history). "Tests are green now" is not evidence.
8. **Contract check** — list the documented invariants covering the touched areas (project CLAUDE.md, feature KNOWLEDGE.md files, decisions/pitfalls ledger) and confirm each is honored, citing the source.
9. **Scope guard** — the diff stays inside the ticket boundary. Name anything that belongs to a deferred or adjacent ticket, and remove it.
10. **Validation with output** — build, typecheck, lint, and tests actually ran; report real results, not assumptions. Delegate to a Validate agent where available.
11. **Exit gates** — enumerate the plan's exit criteria for this phase and confirm each against the diff.
12. **Architecture drift check** — compare what was actually built against the architecture stated at LAUNCH (item 5). Name any deviation — a new dependency, a boundary crossed, a pattern bypassed "temporarily" — and either revert it or get it re-approved; silent drift is a FAIL.
13. **Lesson encoded** — if this phase had failed attempts, the root cause is recorded somewhere durable (pitfall entry, prompt template, working memory), not merely fixed.

## PR — before opening or updating a PR

14. **Production blast radius** — state concretely what breaks in production if this change misbehaves: which user-facing surfaces, scheduled jobs, and data are affected; whether the change is backward compatible with live data and in-flight clients; whether it degrades or hard-fails. "Low risk" without a stated mechanism is not evidence.
15. **Rollback path** — is a plain revert safe, or does the change write data / emit events in a format old code can't read? Name the rollback mechanism (revert, feature flag, config toggle) and any point of no return. If there is no rollback path, that must be stated in the PR and acknowledged by the user.
16. **Infra-before-code ordering** — does the change add or rely on a database index, TTL policy, env var, secret, or migration? State what happens if the code ships before the infra is ready, and the graceful-degradation path.
17. **Operational notes complete** — explicit yes/no for each category (indexes, TTLs, env vars/secrets, scheduled functions, migrations, manual post-deploy steps with exact commands) — even when the answer is "none".
18. **Deploy sequence stated** — the exact deploy order and modes, honoring repo deploy rules (e.g. never `auto` after a single-surface run; index → poll Enabled → hosting).
19. **Notifications** — if anything qualifies as a migration or ops action, the required people are notified per project policy, with exact commands drafted in the PR's Operational notes.
20. **Open risks restated** — any hard question left as an open risk at LAUNCH (item 6) appears in the PR description with its current status: resolved with evidence, mitigated, or still open and accepted by whom.

## Report format

Output a table: `# | item | PASS/FAIL/N-A | one-line evidence`. Follow with a verdict line: **CLEAR TO PROCEED** or **BLOCKED: <failing items>**. A FAIL is a hard stop — never proceed past one silently; fix it or escalate to the user.
