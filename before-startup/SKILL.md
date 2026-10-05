---
name: before-startup
description: Pre-implementation branch and blocker checklist. Use before writing the first line of implementation code — verifies alignment with the integration branch, that work happens on a fresh correctly-named feature branch (never on the integration branch itself), and that no floes (blockers) sit in the water: dirty working tree, red baseline, out-of-sync dependencies, missing environment, or conflicting in-flight work.
---

# Before-Startup — Branch & Floes Checklist

Purpose: guarantee a clean departure before implementation begins — the work starts from the current tip of the integration branch, on a properly named feature branch, with no floes (blockers) that would force a restart mid-implementation: leftover local state, a baseline that was already red, missing env/secrets, stale dependencies, or a colleague's in-flight change about to collide with ours.

## Workflow position

**1 of 3 — run first.** Use once before implementation starts. After this checklist is clear, use `cruising` at each launch, commit, and PR boundary. Do not use `landing` until the PR is complete and ready for its final production-readiness decision.

## How to run

Evaluate every item against real command output — never from memory or assumption. Run the git commands fresh; a `git status` from earlier in the session is stale evidence. Then produce the report in the format below.

## ALIGNMENT — are we in sync with the integration branch?

1. **Integration branch identified** — name the repo's integration branch explicitly (from repo docs, CLAUDE.md, PR conventions, or default branch — e.g. `develop`, `main`, `integration`). Do not assume `main`; cite the source of the answer.
2. **Remote fetched** — run `git fetch` (or `git fetch origin <integration>`) now, so all subsequent comparisons are against the remote's current state, not a stale local ref.
3. **Base is current** — the commit we branch from must be the remote tip of the integration branch. Run `git rev-list --left-right --count origin/<integration>...HEAD` (or equivalent): if we are behind, rebase/reset onto the tip before starting; starting from a stale base is a guaranteed merge-conflict debt.

## BRANCH — are we on the right vessel?

4. **Not on the integration branch** — `git branch --show-current` must NOT be the integration branch (or any protected branch). Implementation never happens directly on it.
5. **Feature branch exists and is named to convention** — a dedicated branch created for this work, following the repo's convention (`feature/<ticket-or-slug>`, or `fix/`, `chore/` as appropriate). If it does not exist yet, create it now from the verified tip (item 3) and state the exact name.
6. **Branch is fresh for this task** — the branch contains no commits from unrelated or abandoned work. If reusing an existing branch, list its commits ahead of the integration branch and confirm every one belongs to this task.

## FLOES — blockers in the water

7. **Clean working tree** — run `git status`; no uncommitted changes, untracked residue, or in-progress merge/rebase/cherry-pick state (`.git/MERGE_HEAD`, `rebase-merge/`). Anything present must be explicitly stashed, committed elsewhere, or discarded — never carried silently into the new work.
8. **Baseline is green** — build, typecheck, lint, and the test suite pass on the fresh branch BEFORE any implementation code is written. A red baseline is a hard stop: fix it or escalate — otherwise every later failure is ambiguous between "we broke it" and "it was broken".
9. **Dependencies in sync** — the lockfile matches the manifest and installed modules match the lockfile (e.g. `npm ci` / install completes cleanly, no peer-dependency errors). New teammates' dependency bumps on the integration branch are a classic silent floe.
10. **Environment ready** — every env var, secret, emulator, service account, or local service the task needs is present and reachable. Name each one and its status; "probably configured" is a FAIL.
11. **No colliding in-flight work** — check open PRs and active branches touching the same files/areas (e.g. `gh pr list`, team board). Name any overlap and the coordination decision (proceed, wait, or split scope).
12. **Task is unblocked** — the ticket/plan has no unresolved dependency: no pending decision awaiting the user, no upstream ticket that must merge first, no missing design/contract this implementation consumes. List each candidate blocker with evidence it is resolved.

## Report format

Output a table: `# | item | PASS/FAIL/N-A | one-line evidence`. Follow with a verdict line: **CLEAR TO DEPART** or **BLOCKED: <failing items>**. A FAIL is a hard stop — never start implementation past one silently; fix it or escalate to the user.
