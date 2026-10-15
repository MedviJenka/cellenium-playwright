---
name: plan
description: Write an implementation plan as one interactive HTML page instead of a plan.md file. The plan is a three-level tree of claims that the user can disagree with, each with a visual (screen mockup, code, flow, or table) and inline decisions with recommendations. The user answers in the page, clicks Respond, and pastes the generated text back. Use when the user asks for a plan, a design proposal, or wants to review an approach before implementation.
disable-model-invocation: true
---

# Interactive HTML Plan

Write the plan as one self-contained HTML page. The user reads it fast, opens only the depth they need, answers decisions in place, and sends the answers back to you with one paste.

Do not write a `plan.md` file. Do not implement anything while this skill is active.

## Workflow

1. **Research.** Read the relevant code, tests, and docs before you write a claim. Every level-3 claim must point to a real file. If a file does not exist yet, say "new file".
2. **Build the tree.** Follow [Rules](#rules).
3. **Write the page.**
   - Output path: `.plans/<kebab-slug>.html` in the project root. Create `.plans/` if it does not exist.
   - Copy `template.html` from this skill folder to the output path. Do not rewrite the template.
   - Replace the single line `__PLAN_DATA__` with the plan JSON ([Schema](#schema)). In the JSON, write every `</` as `<\/`.
   - Validate the JSON before you continue, for example: `python -c "import json,re,sys; s=open(sys.argv[1],encoding='utf-8').read(); json.loads(re.search(r'<script id=\"plan-data\"[^>]*>(.*?)</script>', s, re.S).group(1))" .plans/<slug>.html`.
4. **Open the page.** Windows: `start "" ".plans\<slug>.html"`. macOS: `open`. Linux: `xdg-open`. If you cannot open it, give the path.
5. **Stop and wait.** In chat, send only: the file path, the outcome sentence, the number of decisions, and this instruction: "Answer in the page, click **Respond**, and paste the text here." Do not repeat the plan in chat.

## Rules

### 1. The plan is a tree with three levels

| Level | Label in the page | Content |
|---|---|---|
| Root (`outcome`) | Result after this plan | One sentence: what the user has when the plan is complete. |
| 1 | Outcome | What a user or caller can do, see, or rely on. No file names. |
| 2 | How it works | The mechanism: data flow, components, rules, limits. |
| 3 | Where in code | The exact files, functions, tables, and tests that change. |

- Use 3–7 level-1 nodes. Use 1–5 children for each node.
- A reader who opens only level 1 must understand the full result.
- Do not go deeper than level 3. Put more detail in `detail` or in the visual.

### 2. Every node is a claim that the user can disagree with

A claim is one specific, testable sentence. It contains a number, a name, a boundary, or a behavior that a person can say "no" to.

| Bad (heading) | Good (claim) |
|---|---|
| Scheduling support | A user can schedule a maximum of 50 messages at the same time. |
| Error handling | If the send fails, the worker tries 3 more times, then marks the message `failed`. |
| Database changes | A new table `scheduled_messages` stores each message with its `send_at` time. |

If you cannot write a claim, you do not know the answer yet. Make it a decision (rule 4).

### 3. Every node has a visual

Select the visual from what the claim is about:

| Claim is about | `visual.kind` |
|---|---|
| What a user sees | `mockup`: an ASCII screen of the UI state. |
| Code that changes | `code`: the real file path, line range, and a short snippet. Start added lines with `+` and removed lines with `-`. |
| Order of steps or data flow | `flow`: the steps in order. |
| Values, limits, mappings, comparisons | `table`. |

Keep each visual small: a maximum of about 15 lines. A visual shows the claim; it does not repeat it. Copy code snippets from the real files when they exist. Do not invent line numbers.

### 4. Decisions sit next to the part they change

- Put each open question in the `decisions` array of the node that it affects. Do not collect questions at the end.
- Give 2–4 options. Each option has a short `label` and a `description` with the trade-off.
- Mark exactly one option `"recommended": true` when you have a recommendation. Put it first.
- Set `"multi": true` only when the options are not exclusive.
- The page adds an "Other" option automatically. Do not add one.
- Ask only what changes the plan. Do not ask what the code, the request, or a safe default already answers. Write the default as a claim.
- Number decisions `D1`, `D2`, … in the order they appear in the tree. Keep the IDs stable across revisions.

### 5. Write in Simplified Technical English (ASD-STE100)

All text in the page (claims, details, questions, options, captions) follows these rules:

- One topic in each sentence. A maximum of 20 words in an instruction and 25 words in a description.
- Use the active voice and the simple present tense. ("The worker sends the message", not "The message will be sent".)
- Use the imperative for instructions. ("Run the migration.")
- Use one word for one meaning. Do not change terms for variety. If you write "worker" once, do not write "job runner" later.
- Use simple, common words: "use" (not "utilize"), "start" (not "initiate"), "show" (not "display"), "make sure" (not "ensure").
- Do not use "-ing" words as nouns or adjectives when a simple verb or noun is clear.
- Write the articles ("a", "the") and the subjects. Do not use telegraphic style.
- Do not use filler: "basically", "simply", "robust", "seamless", "leverage".
- Technical names (files, functions, flags) stay exactly as they are in the code.

### 6. The response loop

The user's paste starts with `PLAN RESPONSE`. When you get it:

- It is **feedback on the plan, not approval**. Do not start implementation.
- Apply every answered decision and every agreed claim.
- For each disagreement or comment, change the claim. If the change is not clear, ask in chat.
- If there are unanswered decisions or new questions, ask them in chat with `AskUserQuestion` (or plain text if the tool is not available). Ask only what blocks the next revision.
- Then write a new revision to the **same file**: increase `revision` by 1 and list each change in `changes` (one short sentence for each change). Keep node IDs and decision IDs stable; give new nodes new IDs. Remove answered decisions and write their result as claims.
- Repeat until the user explicitly says to implement (for example, "approved", "go", "implement it"). A response with zero disagreements is still not approval: ask "Implement this plan?" in chat.
- When you implement, follow the tree. Report against the node IDs.

## Schema

```json
{
  "title": "Scheduled messages",
  "request": "The user's request in one sentence.",
  "file": ".plans/scheduled-messages.html",
  "revision": 1,
  "changes": [],
  "outcome": "A user can write a message now, and the app sends it at the time that the user selects.",
  "nodes": [
    {
      "id": "1",
      "claim": "A user can schedule a maximum of 50 messages at the same time.",
      "detail": "Optional. One or two sentences of context.",
      "visual": { "kind": "mockup", "caption": "Composer with the schedule menu", "text": "+-----------------+\n| Message  [Send v]|\n+-----------------+" },
      "decisions": [
        {
          "id": "D1",
          "question": "What is the maximum number of scheduled messages for each user?",
          "multi": false,
          "options": [
            { "label": "50", "description": "Low storage cost. Most users schedule fewer than 10.", "recommended": true },
            { "label": "100", "description": "Supports power users. Doubles the worst-case queue size." }
          ]
        }
      ],
      "children": [
        {
          "id": "1.1",
          "claim": "The worker sends each message within 60 seconds of its scheduled time.",
          "visual": { "kind": "flow", "caption": "Send path", "steps": ["Composer", "POST /schedule", "scheduled_messages", "Worker (every 30 s)", "Chat service"] },
          "children": [
            {
              "id": "1.1.1",
              "claim": "A new migration adds the table scheduled_messages.",
              "visual": { "kind": "code", "file": "db/migrations/0042_scheduled_messages.sql", "change": "add", "lang": "sql", "snippet": "+CREATE TABLE scheduled_messages (\n+  id BIGSERIAL PRIMARY KEY,\n+  send_at TIMESTAMPTZ NOT NULL\n+);" }
            }
          ]
        }
      ]
    }
  ]
}
```

Field notes:

- `id` is the tree position (`1`, `1.2`, `1.2.3`). The page uses it in the response text.
- `visual.kind` is one of `mockup` (`text`), `code` (`file`, optional `lines` such as `"40-58"`, `change` = `add` | `modify` | `delete`, `snippet`), `flow` (`steps`), or `table` (`columns`, `rows`). All kinds accept `caption`.
- `changes` is empty in revision 1.
- The page computes the level from the depth in the tree. Do not add a level field.

## Self-check before you open the page

- [ ] The outcome sentence and the level-1 claims alone explain the full result.
- [ ] Every node is a claim with a specific value, name, or behavior. No node is a heading.
- [ ] Every node has a visual of the correct kind.
- [ ] Every level-3 node names a real file path (or "new file").
- [ ] Every decision is on the node that it affects, has 2–4 options, and has a recommendation when you have one.
- [ ] All text follows Simplified Technical English.
- [ ] The JSON is valid, and every `</` inside it is written as `<\/`.
