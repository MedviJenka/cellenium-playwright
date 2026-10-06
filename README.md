# Testflow

Four independent Claude Code skills that each apply the aviation-derived **FORDEC** decision model to a different situation. `before-startup`, `cruising`, and `landing` form an ordered software-delivery pipeline from branch creation through production monitoring. `fordec` is a separate, general-purpose emergency/incident decision skill — it does not sit above or chain the other three; it is simply one more skill in the set that happens to use the same FORDEC structure.

## The model

FORDEC is a decision cycle, not a linear task checklist:

| Stage | Question | Required output |
|---|---|---|
| **F — Facts** | What is true now? | Fresh command output, repository rules, observed behavior, and known unknowns |
| **O — Options** | What can we do? | Viable courses, including holding position or going around |
| **R — Risks & Benefits** | What does each option gain and expose? | Concrete tradeoffs, reversibility, blast radius, and cost of delay |
| **D — Decision** | Which option are we choosing? | Explicit course, rationale, owner, accepted risks, and success criteria |
| **E — Execution** | How do we carry it out? | Ordered actions within the approved scope |
| **C — Check** | Did it work, and how will we know if conditions change? | Observed results, monitoring signals, thresholds, owners, and reconsideration triggers |

The order is mandatory:

```text
FACTS → OPTIONS → RISKS & BENEFITS → DECISION → EXECUTION → CHECK
   ↑                                                        │
   └──────────── new facts, failed check, or monitor alert ─┘
```

**Decision comes before Execution.** If Execution or Check reveals a material new fact, stop and restart the cycle instead of defending the old decision.

## Skill workflow

`before-startup` → `cruising` → `landing` is the ordered software-delivery pipeline:

| Order | Skill | FORDEC role | When to use | Success verdict |
|---:|---|---|---|---|
| 1 | [`before-startup`](.claude/skills/testflow/before-startup/SKILL.md) | Departure cycle | Once, before implementation begins | `CLEAR TO DEPART` |
| 2 | [`cruising`](.claude/skills/testflow/cruising/SKILL.md) | Repeating control cycle | At LAUNCH, COMMIT, and PR boundaries | `CLEAR TO PROCEED` |
| 3 | [`landing`](.claude/skills/testflow/landing/SKILL.md) | Final production cycle | Before final approval, merge, release, or deployment | `CLEAR TO LAND` |

```text
before-startup: FORDEC departure
        ↓
cruising: FORDEC at LAUNCH → COMMIT → repeat → PR
        ↓
landing: final FORDEC → LAND / STAGED LANDING / GO-AROUND
        ↓
production CHECK → monitor → reopen FORDEC when thresholds are crossed
```

A failed gate is a hard stop. Fix the evidence gap, choose another option, or explicitly escalate the risk; never silently continue.

[`fordec`](.claude/skills/testflow/emergency/fordec/SKILL.md) is **not part of this pipeline**. It is an independent, standalone skill for any consequential situation that needs a time-aware decision — use it on its own, whenever it's needed, regardless of where you are in before-startup/cruising/landing.

## Skill responsibilities

### 1. Before Startup

Runs the departure decision before implementation:

- establishes the real branch, remote, working-tree, baseline, dependency, environment, traffic, and blocker state;
- compares safe departure options, including holding position;
- evaluates lost-work, history, conflict, dependency, and irreversibility risks;
- chooses the branch and synchronization plan before changing state;
- executes only the selected plan;
- checks that the task branch, base, baseline, environment, and prerequisites are safe.

### 2. Cruising

Runs a complete FORDEC cycle at each implementation boundary:

- **LAUNCH:** decides whether and how to start or resume an agent or phase;
- **COMMIT:** decides whether the phase is coherent, tested, in scope, and ready to close;
- **PR:** decides whether the change and its operational plan are ready for review.

It preserves TDD evidence, architecture and contract compliance, scope control, operational detail, rollback planning, and monitoring triggers. `Cruising` repeats as conditions change.

### 3. Landing

Runs the final production decision:

- treats green checks as facts rather than automatic approval;
- compares landing, staged landing, remediation, scope reduction, deferment, and go-around;
- audits hidden bugs, avoided tests, complexity, blast radius, compatibility, deploy order, and rollback;
- separates a readiness decision from authorization to merge or deploy;
- executes only the authorized course;
- checks production behavior against explicit signals, windows, thresholds, owners, and rollback triggers.

### 4. Fordec

Independent of the other three. Runs a standalone FORDEC cycle for emergencies and incidents:

- gates on urgency first — immediate safety action before any analysis;
- labels every fact as OBSERVED, REPORTED, INFERRED, or UNKNOWN;
- compares feasible options, including hold, withdraw, or escalate;
- supports Full, Rapid, or Immediate-action modes depending on available time;
- assigns owners and deadlines to execution steps;
- defines monitoring signals and the next decision point.

## Decision discipline

- Facts must be evidence, not assumptions.
- Options come before preference; include a safe hold or go-around.
- Risks and Benefits are paired for every viable option.
- One-way-door decisions and destructive actions require explicit user approval.
- Execution must match the recorded Decision.
- Check means active monitoring, not merely confirming that a command exited successfully.
- A material new fact reopens FORDEC at **F**, even if work is already underway.

## Installation

Install the commands into the current project's `.claude/skills/testflow/` directory:

```sh
npx @medvijenia/checklist
```

Install them for the current user instead:

```sh
npx @medvijenia/checklist --global
```

The installer preserves modified skills. Pass `--force` only when you intend to replace local customizations.

The npm package is also a valid Claude Code plugin. To load its namespaced commands without copying files:

```sh
npm install --save-dev @medvijenia/checklist
claude --plugin-dir ./node_modules/@medvijenia/checklist
```

Plugin mode exposes `/testflow:before-startup`, `/testflow:cruising`, `/testflow:landing`, and `/testflow:fordec`.

## Invocation

The installer exposes the commands without a namespace:

```text
/before-startup
/cruising
/landing
/fordec
```

They are manual-only by design because their workflows can change branches, create commits, open pull requests, or deploy. Preserve the pipeline order for the first three — `before-startup` → `cruising` → `landing` — and F → O → R → D → E → C inside every skill. `fordec` is independent of that order and can be invoked on its own whenever a situation calls for it.

## Agents

No custom agent definitions are required. None of the skills names or forks to a custom subagent; `cruising` audits launches performed through Claude Code's built-in agent runtime. Shipping unused agent files would add context cost without changing behavior.
