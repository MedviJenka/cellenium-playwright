---
name: fordec
description: "Structured emergency and incident decision support using the aviation-derived FORDEC cycle: Facts, Options, Risks & Benefits, Decision, Execution, Check. Use when a consequential situation needs a clear, time-aware choice, assigned actions, and active reassessment."
disable-model-invocation: true
---

# FORDEC — Emergency Decision Cycle

Use FORDEC to turn an uncertain, consequential situation into an explicit, reviewable decision:

1. **Facts**
2. **Options**
3. **Risks & Benefits**
4. **Decision**
5. **Execution**
6. **Check & Monitor**

FORDEC is a decision aid, not a substitute for law, emergency services, trained responders, an aircraft or equipment checklist, or an organization's emergency procedures. The responsible human remains the decision owner.

## Safety and urgency gate

Before beginning the full cycle:

1. Determine whether there is an immediate threat to life, physical safety, essential system control, or containment.
2. If there is, lead with the applicable immediate action: call the local emergency number, warn or evacuate people, maintain control, isolate the hazard, or follow the established memory item, checklist, or emergency procedure.
3. Do not delay a required immediate action to complete FORDEC. Stabilize first, then use the shortest useful cycle.
4. State the available decision time, the decision owner, and any limits on authority or capability.

Never invent emergency instructions, technical limits, diagnoses, or regulatory requirements. Use authoritative procedures and observed evidence. When an unknown could change the safe course, mark it clearly and obtain qualified help.

## Operating rules

- Run **F → O → R → D → E → C** in order. Do not choose an option before comparing its risks and benefits.
- Separate observations from interpretations and unknowns.
- Prefer the safest feasible reversible action when evidence or time is limited.
- Include escalation, holding position, stopping, evacuation, or withdrawal when they are viable options.
- Use all available resources: procedures, instruments, logs, witnesses, specialists, emergency services, and other team members.
- Invite an independent challenge before the Decision when time permits. Do not let the person who framed the problem be the only person testing it.
- Use closed-loop communication: assign a named person, require acknowledgment, and confirm completion.
- A material new fact, failed assumption, or breached threshold invalidates the current decision. Stop and restart at **Facts**.
- Never treat silence, task completion, or the absence of a new alert as proof that the situation is safe.

## Time-pressure modes

Choose the shortest mode that preserves safety:

- **Full FORDEC** — enough time exists to gather evidence, compare realistic options, coordinate people, and define monitoring.
- **Rapid FORDEC** — time is constrained. State only the decisive facts, two or three feasible options, the dominant risk and benefit of each, the decision, immediate assignments, and the next check.
- **Immediate action** — delay would increase harm. Follow the applicable emergency procedure or safest established action first, announce the action and assignments, then perform Rapid FORDEC as soon as the situation is stable.

Time pressure permits compression, not omission of responsibility, execution ownership, or reassessment.

## F — FACTS

Establish what is true now:

1. **Situation** — what happened, when it began, current effects, trend, location, people or systems exposed, and the triggering observation.
2. **Evidence quality** — label each material statement as **OBSERVED**, **REPORTED**, **INFERRED**, or **UNKNOWN**. Resolve conflicts where possible.
3. **Control and stability** — what remains under control, what is degraded or unavailable, and whether the situation is stable, improving, or worsening.
4. **Time** — immediate deadlines, depletion rates, safe operating windows, points of no return, and when the next fact will become available.
5. **Constraints** — applicable procedures, legal or operational limits, dependencies, access restrictions, environmental conditions, and unavailable resources.
6. **People and resources** — decision owner, responders, affected people, specialists, equipment, communications, and credible external assistance.
7. **Objective** — the safety outcome to protect, followed by the operational outcome to preserve.

Do not hide a missing fact inside an assumption. If it cannot be resolved in time, carry it into Risks & Benefits as uncertainty.

## O — OPTIONS

List only feasible courses:

1. Generate distinct actions, not variations in wording. Include the safest hold, stop, withdraw, or escalate course when feasible.
2. State what each option requires, how quickly it can begin, and any condition that makes it unavailable.
3. Eliminate an option if it violates a hard constraint, depends on an unavailable resource, or creates an unjustified immediate danger.
4. Keep the list short enough to compare under the available workload. Do not manufacture alternatives merely to reach a target count.
5. Identify a fallback for any option whose failure would otherwise leave no safe course.

## R — RISKS & BENEFITS

Compare every remaining option against the same criteria:

- likely safety benefit and operational benefit;
- credible failure modes and worst credible consequence;
- likelihood, severity, exposure, and uncertainty;
- time to act and time to benefit;
- reversibility and point of no return;
- workload, coordination demand, and resource consumption;
- second-order effects on people, systems, environment, and later recovery;
- mitigations, warning signs, and remaining risk after mitigation.

Use qualitative ratings only when their meaning is explicit. Never collapse an uncertain high-consequence hazard into an unsupported “low risk” label. Name the assumption most likely to invalidate each option.

## D — DECISION

Make the choice explicit before acting:

1. Name the selected option and why its benefits outweigh its risks under the current facts.
2. Name the decision owner and any authority whose approval is required.
3. Record rejected options and the decisive reason for rejecting each.
4. State accepted residual risks, their owners, and the fallback or recovery course.
5. Define success criteria, abort thresholds, escalation triggers, and the next decision point.
6. Record meaningful dissent. Resolve safety-critical disagreement through the applicable command or escalation path; do not manufacture consensus.

If no option is acceptably safe, decide to **HOLD**, **WITHDRAW**, or **ESCALATE** rather than disguising uncertainty as permission to proceed.

## E — EXECUTION

Translate the Decision into coordinated action:

1. Set priorities and sequence actions so that control, life safety, and containment come before recovery or convenience.
2. Assign each action to a named owner with a deadline or trigger.
3. Specify communications: who must be warned, consulted, updated, or handed over to.
4. Confirm critical instructions by readback and verify irreversible actions before they occur.
5. Prepare the fallback before crossing a point of no return.
6. Execute only the selected course and only within the granted authority. Require explicit approval for destructive or irreversible actions unless an established emergency procedure already authorizes them.
7. If execution exposes a material new fact or cannot proceed as planned, stop improvising and reopen FORDEC.

## C — CHECK

Verify outcomes and keep monitoring:

1. Compare observed results with the Decision's success criteria; report values and behavior, not “looks good.”
2. Confirm that assigned actions completed, communications were received, and no affected person or system was omitted.
3. For each important risk, define the signal, expected state, threshold, observation window, owner, and response.
4. Reassess workload, resource depletion, secondary hazards, and the continued availability of the fallback.
5. At the next decision point, explicitly choose one: continue, modify, abort, hand over, escalate, or restart FORDEC.

The Check phase is continuous. A changed context starts a new cycle with new Facts; it does not merely append a note to the old decision.

## Team challenge

When another competent person is available and time permits:

1. Give them the raw observations before sharing the preferred explanation.
2. Ask for an independent diagnosis, overlooked option, and strongest reason the preferred option could fail.
3. Reconcile the two mental models and record unresolved disagreement.
4. Let any participant call **STOP** when a safety assumption fails or execution diverges from the Decision.

For a solo decision, perform the same challenge explicitly: “What fact would prove my diagnosis wrong?” and “What safer reversible option have I not considered?”

## Response format

Lead with any immediate safety action. Then output:

1. `Mode: FULL FORDEC | RAPID FORDEC | IMMEDIATE ACTION`
2. `Decision owner: <person or role> | Decision time: <deadline or window>`
3. a **Facts** table: `fact | status (OBSERVED/REPORTED/INFERRED/UNKNOWN) | source | relevance`;
4. an **Options** table: `option | requirements | benefits | risks | reversibility`;
5. a **Decision** line: selected option, rationale, residual risk, and required approval;
6. an **Execution** table: `priority | action | owner | trigger/deadline | confirmation`;
7. a **Check** table: `signal | expected state | threshold | window | owner | response`;
8. a verdict: **EXECUTE**, **HOLD**, **WITHDRAW**, or **ESCALATE**, followed by the next decision point.

In Rapid mode, compress each section to the decisive content. Never omit the Decision, owner, immediate assignments, fallback, or next Check.