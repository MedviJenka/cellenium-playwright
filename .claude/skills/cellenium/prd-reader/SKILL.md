---
name: prd-reader
description: Read a product requirements document and convert it into an evidence-backed, testable requirement matrix for pytest. Use when a PRD, feature brief, ticket, or acceptance-criteria document must be understood before test design.
disable-model-invocation: true
---

# PRD Reader

Turn product intent into testable behavior without inventing requirements. This is the first TestFlow stage.

## Input

Accept a PRD path, issue, pasted requirements, or feature brief. Read the complete source and any repository files it explicitly references. If several documents conflict, identify the conflict instead of selecting a convenient interpretation.

## Process

1. **Establish scope**
   - Identify the user, problem, intended outcome, in-scope behavior, and explicit exclusions.
   - Separate product behavior from implementation suggestions.
   - Record every named platform, role, state, permission, dependency, and integration boundary.

2. **Extract requirements**
   - Give each requirement a stable ID: `PRD-001`, `PRD-002`, and so on.
   - Preserve normative terms such as must, must not, should, default, and only.
   - Capture inputs, preconditions, observable outputs, side effects, errors, and postconditions.
   - Extract non-functional constraints only when they are measurable: latency, limits, security, compatibility, accessibility, reliability, or data retention.

3. **Classify evidence**
   - `EXPLICIT`: directly stated in the PRD.
   - `DERIVED`: logically required by an explicit behavior or invariant.
   - `UNKNOWN`: materially affects the expected result but is not specified.
   - Cite the source heading, paragraph, acceptance criterion, or issue comment for every explicit requirement.

4. **Find ambiguity and contradictions**
   - Identify undefined terms, conflicting rules, missing precedence, unclear error behavior, and unowned external dependencies.
   - Do not turn an unknown into an assertion.
   - Ask for clarification only when different answers would produce materially different tests. Otherwise choose the repository's established convention and label the choice `DERIVED`.

5. **Make behavior testable**
   - Rewrite each requirement as a black-box contract: given state and input, when an action occurs, then an observable result follows.
   - Add boundary partitions implied by the requirement: empty, minimum, maximum, just below, just above, malformed, duplicate, unauthorized, unavailable dependency, and retry only when relevant.
   - Do not prescribe mocks, fixtures, private methods, or implementation details.

## Output contract

Return these sections:

### Product intent

A concise statement of the user, problem, outcome, and scope.

### Requirement matrix

| ID | Evidence | Source | Preconditions | Action/input | Observable result | Priority |
|---|---|---|---|---|---|---|

Priority is `MUST`, `SHOULD`, or `MAY`, based on the source language.

### Business rules and invariants

List rules that must remain true across scenarios.

### Test-relevant boundaries

List equivalence partitions, boundary values, error states, permissions, and external-system conditions that follow from the requirements.

### Open questions

List only unknowns that could change test expectations. State the competing interpretations and affected requirement IDs.

### Out of scope

List explicit exclusions and tempting adjacent behaviors that tests must not encode.

## Quality gate

The PRD analysis is complete only when:

- every acceptance criterion maps to at least one requirement ID;
- each requirement describes an observable outcome;
- explicit, derived, and unknown claims are distinguishable;
- contradictions and test-blocking unknowns are visible;
- no implementation detail has been promoted into product behavior;
- downstream `test-spec` can design cases without rereading the PRD.

Do not write pytest code in this stage. Hand the requirement matrix to `test-spec`.
