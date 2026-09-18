---
name: davinci-flow-design
description: "Use when designing or building a PingOne DaVinci flow — registration with email verification, login, MFA enrollment and step-up, passwordless and passkey flows, progressive profiling, social login, subflow composition, error-path design, and preparing flows and connector credentials for promotion between environments. Produces flow designs and connector wiring as artifacts."
compatibility: "Design-time skill for PingOne DaVinci. Produces flow designs and connector wiring as artifacts; deploying, testing, and inspecting live executions requires DaVinci console access, PingOne MCP tools, or Ping CLI 1.4.0 or later."
metadata:
  publisher: Ping Identity
  version: "1.0.0"
  product_family: pingone-mt
---

# DaVinci Flow Design

Design and build PingOne DaVinci flows: connector selection and sequencing, logical-operator branching, variables, subflow composition, and error paths. Produces flow designs and connector wiring as artifacts; live execution work belongs to the DaVinci console.

## When to use

- Build or review a DaVinci flow: login, registration with email verification, MFA enrollment, risk-driven step-up, progressive profiling, social login.
- Choose connector capabilities, wire branching, declare variables, and compose subflows.
- Design error paths: user error, system error, and security-block categories.
- Prepare flows, flow policies, and connector credentials for promotion between environments.

## When NOT to use

- Diagnosing what happened in a flow execution that already ran — use the DaVinci console's execution history and debug logging ([DaVinci flows documentation](https://docs.pingidentity.com/davinci/flows/davinci_flows.html)).
- Setting up a PingOne environment, organization, or application — use PingOne documentation.
- Embedding a flow in an app via SDK — use the client-platform integration documentation for your application stack.

## Routing

| Request signal | Start with |
|---|---|
| Flow model, logical operators, connectors, variables, versioning, invocation methods | `references/flow-model.md` |
| Login, registration, step-up, progressive-profiling, error-handling patterns | `references/flow-patterns.md` |
| Registration + email verification, MFA enrollment, Protect-driven step-up | `references/registration-and-mfa.md` |
| Passkey / passwordless flows and recovery paths | `references/passkey-flows.md` |
| Promoting flows, flow policies, and connector credentials | `references/flow-promotion.md` |
