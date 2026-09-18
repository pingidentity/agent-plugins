# Ping Identity PingOne Plugin

Agent-focused guidance for PingOne — connecting applications to a PingOne environment, designing and building DaVinci flows, troubleshooting live flow executions using MCP evidence, and investigating PingOne audit and platform operations.

## What this plugin is for

- Implementing app-side integration against a PingOne environment — SDK wiring, OIDC/PKCE, CORS, Worker applications, troubleshooting
- Designing and building DaVinci flows — registration, login, MFA, step-up, passkeys, promotion
- Tracing executions by actor, interaction ID, transaction ID, flow, or time window
- Correlating subflows and reconstructing chronological event chains
- Detecting unresolved errors, silent failures, loops, and recovered conditions
- Investigating audit events, failed logins, admin actions, compliance history, and resource activity
- Handling typed filters, explicit time windows, pagination, and full event details
- Producing evidence-based root cause, confidence, and remediation

## Requirements

Operational investigation requires authorized access through the remote PingOne MCP server or Ping CLI. The skills do not install tools or modify the agent harness.

## Skills

| Skill | Path | Use when |
|---|---|---|
| `pingone-app-integration` | `skills/pingone-app-integration/` | Integrating an Android, iOS, JavaScript/React, or backend app with a PingOne environment |
| `davinci-flow-design` | `skills/davinci-flow-design/` | Designing or building a DaVinci flow |
| `davinci-flow-engineering` | `skills/davinci-flow-engineering/` | Tracing or debugging DaVinci flow executions |
| `pingone-platform-ops` | `skills/pingone-platform-ops/` | Investigating PingOne audit and operational events |
