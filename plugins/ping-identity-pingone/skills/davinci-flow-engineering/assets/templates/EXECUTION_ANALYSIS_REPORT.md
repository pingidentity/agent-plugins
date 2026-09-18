# Execution analysis report

Use this presentation contract after applying the debug playbook. Render output only as the markdown sections below. Never emit raw YAML or JSON to the user, and never merge, summarize, or paraphrase timeline rows — every retrieved event gets its own row.

## Required sections

### Summary

Include result (`SUCCESS`, `FAILED`, `PARTIAL`, `NOT_FOUND`, or `ERROR`), confidence, environment, flow and version when known, interaction ID, transaction ID, start/end time, duration, and client when relevant.

### Timeline

Render every retrieved event from every execution in one ascending chronological table:

| Step | Time | Flow | Interaction | Node | Event | Status |
|---|---|---|---|---|---|---|

Rules:

- Number rows once across the merged chain with no gaps.
- Include flow ID, interaction ID, and node ID; use `null` when unavailable.
- Do not merge consecutive events or group by flow before sorting.
- Include system start events.
- Omit definition-only routing nodes that emit no event, and state that omission.

### Failure

Include only when failure is established. Identify failing step, node and description, owning flow, error code/message, root cause, and recommended fix. Root cause must distinguish evidence from inference. The fix must include a validation step.

Once failure is established, the failing node, owning flow, root cause, and recommended fix MUST be populated — never left null, and never written as "N/A" or "unknown." If a genuinely necessary fact is unavailable, state what is known and name the next evidence-producing step instead of leaving the field empty. If the recommended fix touches a security control, append: "This recommendation is advisory — review with your security team before applying to a production flow."

### Subflows

List every discovered subflow execution with flow, flow ID, interaction ID, transaction ID, and whether it is included in the timeline. Write `none` when no subflow exists.

### Diagnostics

Include data completeness, total events, total subflows, pagination handling, audit fallback use, searched scope, and warnings. For a multi-execution comparison, include the recurring failure node (or the spread, if none recurs) and how many of the compared executions it appears in.

### Next steps

Include when the result is partial/not found, or when DaVinci succeeded despite a reported user failure.

## Outcome rules

- Earlier error events followed by clear success are recovered conditions, not the Failure section.
- A terminal unresolved error, abnormal exit, or unresolved loop is a failure.
- Incomplete logs without a defensible terminal outcome are partial.
- No matching execution after bounded execution and audit searches is not found.

## Pre-emit checks

These are MUST-pass gates, not suggestions. If any check fails, go back and populate the missing field before emitting — do not emit a partial or incomplete result.

- Timeline contains all retrieved events and is chronologically sorted.
- Every row identifies its source execution and flow.
- A reported failure has a non-empty node or terminal event, root cause, and remediation — never null, never "N/A", never "unknown."
- Missing evidence is explicit.
- PII is minimized.
