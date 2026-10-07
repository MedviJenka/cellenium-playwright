---
name: fordec
description: "Software incident and emergency decision cycle using the aviation-derived FORDEC model: Facts, Options, Risks & Benefits, Decision, Execution, Check. Use when a production outage, failed deploy, broken main branch, data corruption, security incident, or other consequential engineering problem needs a clear, time-aware choice, assigned actions, and active reassessment."
disable-model-invocation: true
---

# FORDEC — Software Incident Decision Cycle

Use FORDEC to turn an uncertain, consequential engineering situation into an explicit, reviewable decision:

1. **Facts**
2. **Options**
3. **Risks & Benefits**
4. **Decision**
5. **Execution**
6. **Check & Monitor**

FORDEC is a decision aid, not a substitute for the team's incident-response process, runbooks, on-call escalation policy, security or legal obligations, or the judgment of the incident commander. The responsible human remains the decision owner.

## Workflow position

**Off-sequence — run on demand.** `before-startup`, `cruising`, and `landing` cover planned work. Use `fordec` whenever something goes wrong at any point: a production incident, a failed or partial deploy, a red main branch blocking the team, a suspected data loss, a leaked secret, or a regression discovered after merge. Return to the planned checklist only after this cycle reaches a stable state.

## Severity and containment gate

Before beginning the full cycle:

1. Classify impact: users affected, revenue or SLA exposure, data integrity or loss, security or privacy exposure, and whether the problem is spreading.
2. If damage is ongoing, contain first using the established, reversible lever: roll back the deploy, disable the feature flag, stop the job or queue consumer, shift or drain traffic, revoke and rotate an exposed credential, put the system in maintenance or read-only mode, or follow the runbook step.
3. Do not delay a required containment action to complete FORDEC. Stabilize first, then use the shortest useful cycle.
4. Declare the incident through the team's channel if it meets the threshold. State the incident commander (decision owner), the available decision time, and any limits on access or authority.
5. Preserve evidence before it disappears: logs, metrics snapshots, failing request IDs, the deployed revision, and the state of affected data.

Never invent runbook steps, system limits, root causes, or compliance requirements. Use observed evidence and the team's documented procedures. When an unknown could change the safe course, mark it clearly and pull in the owning team or a specialist.

## Operating rules

- Run **F → O → R → D → E → C** in order. Do not choose a fix before comparing its risks and benefits.
- Separate observations (what the logs, metrics, and tests show) from hypotheses about the cause.
- Mitigation comes before root cause. Restore service first; investigate afterward.
- Prefer the safest reversible action when evidence or time is limited: rollback beats hotfix, flag-off beats code change, pause beats delete.
- Include rollback, hold, freeze deploys, and escalate as options whenever they are viable.
- Use all available resources: dashboards, logs, traces, alerts, error trackers, git history, CI results, runbooks, owning teams, and vendors' status pages.
- Invite an independent challenge before the Decision when time permits. The person who wrote or deployed the change should not be the only one testing the diagnosis.
- Use closed-loop communication: assign a named owner, require acknowledgment, and confirm completion in the incident channel.
- A material new fact, failed assumption, or breached threshold invalidates the current decision. Stop and restart at **Facts**.
- Never treat a green deploy, a passing CI run, or a quiet alert channel as proof that the system is healthy.

## Time-pressure modes

Choose the shortest mode that preserves safety:

- **Full FORDEC** — the system is stable or degraded but contained. Gather evidence, compare realistic fixes, coordinate owners, and define monitoring.
- **Rapid FORDEC** — users are impacted now. State only the decisive facts, two or three feasible options, the dominant risk and benefit of each, the decision, immediate assignments, and the next check.
- **Immediate action** — delay is actively increasing damage (data being corrupted, secret being exploited, outage spreading). Execute the established containment lever first, announce it in the incident channel, then perform Rapid FORDEC once the bleeding stops.

Time pressure permits compression, not omission of ownership, rollback readiness, or reassessment.

## F — FACTS

Establish what is true now:

1. **Symptom** — what is failing, since when, error rates and latency vs. baseline, affected endpoints, services, jobs, regions, tenants, or user segments, and the alert or report that triggered the response.
2. **Change correlation** — recent deploys, merges, config or flag changes, migrations, infrastructure or dependency updates, and third-party incidents in the window before onset. Identify the exact running revision.
3. **Evidence quality** — label each material statement as **OBSERVED**, **REPORTED**, **INFERRED**, or **UNKNOWN**, with its source (dashboard, log query, trace, test, user report). Resolve conflicts where possible.
4. **Blast radius and trend** — what still works, what is degraded or down, whether data is being written incorrectly, and whether the situation is stable, improving, or worsening.
5. **Time** — SLA or SLO burn rate, queue backlogs, disk or quota exhaustion, certificate or token expiry, retry storms, and any point after which data becomes unrecoverable or rollback is no longer clean.
6. **Constraints** — change freezes, access or permission limits, migrations that cannot be reversed, compliance or disclosure obligations, and unavailable tooling.
7. **People and resources** — incident commander, on-call engineers, code owners of the affected area, communications owner, and vendor or platform support.
8. **Objective** — the safety outcome to protect first (data integrity, security, user trust), then the service outcome to restore.

Do not hide a missing fact inside an assumption. If it cannot be resolved in time, carry it into Risks & Benefits as uncertainty.

## O — OPTIONS

List only feasible courses:

1. Generate distinct actions, not variations in wording. Typical candidates: roll back to the last known-good revision, disable a feature flag or config, revert the offending commit and redeploy, forward-fix with a hotfix, scale or reroute traffic, pause jobs or consumers, restore or repair data, fail over, hold and gather more evidence, or escalate.
2. State what each option requires (access, build and deploy time, approvals, data steps), how quickly it can take effect, and any condition that makes it unavailable — for example, a migration that makes rollback unsafe.
3. Eliminate an option if it violates a hard constraint, depends on unavailable access, or risks making data loss or exposure worse.
4. Keep the list short enough to compare under incident workload. Do not manufacture alternatives to reach a count.
5. Identify a fallback for any option whose failure would leave no safe course, such as a hotfix that fails CI or a rollback that fails on schema mismatch.

## R — RISKS & BENEFITS

Compare every remaining option against the same criteria:

- user and business impact reduced, and how quickly;
- credible failure modes and worst credible consequence (extended outage, data loss, duplicated side effects, security exposure);
- likelihood, severity, blast radius, and uncertainty;
- time to deploy and time until the effect is visible in metrics;
- reversibility and point of no return (schema changes, emitted events, sent emails, external API calls, deleted data);
- untested code paths: a hotfix that skipped review or tests carries risk the rollback does not;
- compatibility with live data, in-flight requests, caches, queued messages, and older clients;
- workload and coordination demand on the people involved;
- mitigations, warning signs, and remaining risk after mitigation.

Use qualitative ratings only when their meaning is explicit. Never collapse an uncertain high-consequence risk into an unsupported "low risk" label. Name the assumption most likely to invalidate each option.

## D — DECISION

Make the choice explicit before acting:

1. Name the selected option and why its benefits outweigh its risks under the current facts.
2. Name the decision owner and any approval required (code owner, security, data owner, release manager).
3. Record rejected options and the decisive reason for rejecting each.
4. State accepted residual risks, their owners, and the fallback course.
5. Define success criteria in measurable terms (error rate, latency, queue depth, failing test now passing), abort thresholds, escalation triggers, and the next decision point.
6. Record meaningful dissent. Resolve safety-critical disagreement through the incident commander or escalation path; do not manufacture consensus.

If no option is acceptably safe, decide to **HOLD**, **ROLL BACK**, or **ESCALATE** rather than disguising uncertainty as permission to ship a fix.

## E — EXECUTION

Translate the Decision into coordinated action:

1. Sequence actions so that containment, data integrity, and security come before full recovery, cleanup, or root-cause work.
2. Assign each action to a named owner with a deadline or trigger, and post it in the incident channel.
3. Specify communications: status page, affected customers or internal teams, stakeholders to update, and the handover if the incident outlives the shift.
4. Confirm critical commands by readback. Double-check the target environment, revision, and scope before any destructive or irreversible command (database writes, deletes, force pushes, credential revocation).
5. Prepare the rollback or fallback before crossing a point of no return. Take a backup or snapshot before data repair.
6. Execute only the selected course and only within granted authority. Require explicit user approval for destructive or production-affecting actions unless an established runbook already authorizes them.
7. Keep a timestamped log of actions taken for the postmortem.
8. If execution exposes a material new fact or cannot proceed as planned, stop improvising and reopen FORDEC.

## C — CHECK

Verify outcomes and keep monitoring:

1. Compare observed results with the Decision's success criteria. Report actual values from metrics, logs, and tests, not "looks fixed" or "deployed successfully."
2. Confirm that assigned actions completed, communications were sent, and no affected service, job, tenant, or data set was missed.
3. For each important risk, define the signal, expected state, threshold, observation window, owner, and response.
4. Watch for secondary effects: retry backlogs draining, cache stampedes, delayed jobs catching up, and data written during the incident window.
5. At the next decision point, explicitly choose one: continue monitoring, modify, roll back, hand over, escalate, close the incident, or restart FORDEC.
6. Once stable, capture follow-ups: root-cause investigation, regression test for the failure, data repair verification, and a postmortem owner and date.

The Check phase is continuous. A changed context starts a new cycle with new Facts; it does not merely append a note to the old decision.

## Team challenge

When another competent engineer is available and time permits:

1. Give them the raw signals (graphs, logs, error samples, the diff) before sharing your preferred diagnosis.
2. Ask for an independent diagnosis, an overlooked option, and the strongest reason the preferred fix could fail.
3. Reconcile the two mental models and record unresolved disagreement.
4. Let any participant call **STOP** when an assumption fails or execution diverges from the Decision.

For a solo decision, perform the same challenge explicitly: "What evidence would prove my diagnosis wrong?" and "What safer, more reversible option have I not considered?"

## Response format

Lead with any immediate containment action. Then output:

1. `Mode: FULL FORDEC | RAPID FORDEC | IMMEDIATE ACTION` and `Severity: <level and impact summary>`
2. `Incident commander: <person or role> | Decision time: <deadline or window> | Running revision: <sha/version>`
3. a **Facts** table: `fact | status (OBSERVED/REPORTED/INFERRED/UNKNOWN) | source | relevance`;
4. an **Options** table: `option | requirements | benefits | risks | reversibility`;
5. a **Decision** line: selected option, rationale, residual risk, and required approval;
6. an **Execution** table: `priority | action | owner | trigger/deadline | confirmation`;
7. a **Check** table: `signal | expected state | threshold | window | owner | response`;
8. a **Follow-ups** list: root cause, regression test, data verification, postmortem owner;
9. a verdict: **EXECUTE**, **HOLD**, **ROLL BACK**, or **ESCALATE**, followed by the next decision point.

In Rapid mode, compress each section to the decisive content. Never omit the Decision, owner, immediate assignments, rollback path, or next Check.
