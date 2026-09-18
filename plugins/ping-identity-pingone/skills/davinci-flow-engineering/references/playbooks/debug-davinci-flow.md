# Debug a DaVinci flow

Use this playbook to locate an execution, reconstruct its full flow and subflow chain, determine the terminal outcome, and recommend remediation. Map these conceptual operations to available capabilities: call connected PingOne MCP tools directly by inspecting their schemas, or use `../cli.md` for Ping CLI mode, which combines native commands with authenticated custom API requests.

## Inputs and scope

Resolve the PingOne environment before reading execution data. Use the strongest supplied locator:

1. transaction ID
2. interaction or execution ID
3. username or email
4. flow plus time window
5. time window and reported symptom

A flow ID, flow name, timestamp, client, or reported error narrows the search but is not always required. If neither the environment nor a usable locator can be inferred from context, request only the missing value. For unattended execution, use explicit task inputs and available context; do not pause for optional details.

Treat a value containing `@` as a possible username first. If no execution matches and identity lookup is available, resolve the email to its username and user ID, then retry.

## 1. Verify capabilities

Before retrieval, confirm that the selected execution mode can:

- Resolve an environment and list flows.
- Search executions by the available locator and time range.
- Retrieve complete execution events.
- Retrieve the flow definition active at execution time.
- Search audit events when execution discovery is incomplete.

Use only capabilities needed by the selected route. If a required capability is unavailable, state which evidence cannot be obtained and continue only when a defensible partial result is possible.

## 2. Discover executions

### Direct identifiers

- For a transaction ID, search all relevant flows for executions sharing it.
- For an interaction ID with a known flow, retrieve it directly.
- For an interaction ID without a flow, search flow execution summaries until its owning flow is identified.

### Actor and flow

If actor and flow are known, search the requested time range. Without an explicit range, try bounded windows in increasing order: 24 hours, 3 days, then 30 days. Stop widening after sufficient matching evidence is found.

If a flow name is supplied, resolve it exactly. If multiple flows match, use other context to disambiguate; otherwise return the candidates rather than guessing.

### Actor without flow

Search executions across flows within the requested window. Do not stop merely because the first enumerated flow has a match: collect candidates, sort them by timestamp, and select the requested or most recent execution. For an unbounded request, start with 3 days and widen only when necessary.

### Flow or time window without actor

Resolve the flow and search the explicit window. For an approximate timestamp, use a narrow surrounding window and disclose the expansion. If many executions match, filter by reported symptom or return a concise candidate list instead of selecting arbitrarily.

Honor requests for multiple executions. Use the requested count; otherwise cap detailed comparison at ten and report that additional matches exist.

## 3. Recover missing correlation data

Extract the transaction ID from the selected execution. If it is absent or discovery found no execution, search PingOne audit events in the same environment and time window using the actor or other available locator.

Inspect relevant event details when summary records omit correlation fields. If an audit event yields a transaction ID, retry execution discovery with it. Record whether audit fallback was used and what evidence it supplied.

If neither execution nor audit evidence is found, return `not_found` with the searched environment, locators, and windows. Do not infer a failure.

## 4. Analyze the complete chain

Retrieve every event for the main execution and the flow definition active at execution time. Identify all invoked subflows from the definition and execution evidence.

For each referenced subflow:

1. Search for an execution with the same transaction ID.
2. Retrieve all of its events.
3. Inspect its execution-time definition for nested subflows.
4. Repeat recursively while tracking visited execution and flow IDs.

Exhaust pagination before concluding that events or subflows are absent. A missing referenced subflow is a data-completeness warning, not proof of success or failure. See `./subflow-correlation.md` for invariants.

## 5. Classify signals

Scan every execution for candidate signals, but defer the verdict until the full chain is assembled:

- Error-response events and their code, message, node, flow, and timestamp.
- Repeated node visits: count occurrences of each node ID; 3 or more is a loop candidate that may indicate retry or a loop.
- Timeout, abort, cancellation, or an event stream that ends without completion.
- Explicit success or completion events.

Merge all events by timestamp across the main flow and subflows. Use flow-local ordering to break timestamp ties.

Determine the result from the complete chain:

- **Success:** a clear terminal success follows any earlier recoverable errors.
- **Failure:** the terminal outcome is an unresolved error, abnormal termination, or unresolved loop.
- **Partial:** logs or subflow data end before a defensible outcome can be established.

Never classify an intermediate `Send Error Response` as terminal when later retry, branch, subflow, or success evidence exists. Use `../catalogs/failure-signals.md` for classification guidance.

### Comparing multiple executions

When the request compares executions (e.g. "compare the last N failures", "most common failure node"), classify each collected execution independently through its full chain first. Then aggregate across them: identify the failure node that recurs most often and report how many of the compared executions it appears in. If executions fail at different nodes, report the spread rather than forcing a single pattern, and note any shared timing, connector, or configuration across them.

## 6. Determine root cause

Tie the root cause to observed execution evidence and the execution-time node configuration. Distinguish:

- What happened: directly observed events and status.
- Why it happened: configuration or input supported by evidence.
- What remains uncertain: missing logs, definitions, or external policy outcomes.

When the flow completes successfully but the user reports failure, check later PingOne audit events and consider application response handling or policy decisions outside DaVinci.

## 7. Recommend remediation

Recommend the smallest concrete change that addresses the observed cause. Name the affected flow and node, explain the expected effect, and include a validation step. Do not weaken a security control without explicitly marking the recommendation as advisory and requiring production review.

If evidence is insufficient, recommend the next evidence-producing action, such as increasing flow execution logging and reproducing the issue. Do not fabricate a configuration fix.

## 8. Present results

Use `../../assets/templates/EXECUTION_ANALYSIS_REPORT.md`. Always include summary, chronological timeline, subflows, diagnostics, and evidence limitations. Include a failure section only when failure is established.

Confidence:

- **High:** complete chain and unambiguous terminal outcome, with root cause supported by node configuration.
- **Medium:** abnormal terminal outcome, unresolved loop, missing subflow, or incomplete definition.
- **Low:** minimal logs, incomplete chain, or audit-only inference.

Execution data can contain PII. Include only identifiers needed to distinguish evidence and do not write execution logs to files unless explicitly requested.
