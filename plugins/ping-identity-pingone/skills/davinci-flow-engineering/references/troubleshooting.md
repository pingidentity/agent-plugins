# Troubleshooting

Troubleshoot DaVinci flow executions using focused references.

## Scope

Use this reference to:

- Trace login, registration, MFA, or orchestration failures.
- Diagnose executions by username, email, interaction ID, transaction ID, flow, or time window.
- Correlate main-flow and nested-subflow executions.
- Detect unresolved errors, loops, silent termination, and recovered conditions.
- Compare failed executions and identify recurring failure nodes.
- Produce a chronological timeline, confidence rating, root cause, and remediation.

Do not use it to design or build flows, configure the platform, or troubleshoot non-DaVinci orchestration.

## Route by investigation need

Load the troubleshooting playbook first, then only the supporting references needed.

| Need | Reference |
|---|---|
| Locate and diagnose an execution | `playbooks/debug-davinci-flow.md` |
| Render the required result | `../assets/templates/EXECUTION_ANALYSIS_REPORT.md` |
| Interpret supplied identifiers | `catalogs/execution-identifiers.md` |
| Classify an error, loop, or silent termination | `catalogs/failure-signals.md` |
| Traverse or correlate subflows | `playbooks/subflow-correlation.md` |

## Execution

Use an authorized execution mode already available in the agent environment. When PingOne MCP tools are connected, call them directly and inspect each tool's schema for its exact parameters. For Ping CLI, load `cli.md`, which combines native commands with authenticated `pingcli pingone api` requests for execution and audit endpoints. Do not install tools, expose credentials, or modify the execution harness.

## Working principles

1. Resolve the environment and strongest available identifier before retrieval.
2. Use bounded searches and honor explicit time windows.
3. Separate observed evidence from inference; never invent executions, nodes, or configuration.
4. Inspect the complete main-flow and subflow chain before deciding success or failure.
5. Treat intermediate error responses as candidates until later events are checked.
6. Exhaust pagination and report missing evidence.
7. Treat tool-call errors (authorization, HTTP, rate limit) as evidence gaps, not flow failures — report the failed operation and continue with available evidence.
8. Keep recommendations specific, actionable, and advisory for production changes.
9. Minimize exposed PII. Execution output can contain usernames, email addresses, and flow execution IDs sourced from DaVinci logs — do not persist, log, or write it to any store beyond the current session, with no exception for a user request.

## Documentation fallback

If an MCP capability is unavailable or unconfigured, use https://developer.pingidentity.com/build-with-ai/llms.txt for available setup and documentation options.

