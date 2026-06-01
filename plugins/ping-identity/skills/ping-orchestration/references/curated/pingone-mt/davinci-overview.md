---
title: "PingOne MT — DaVinci Overview"
product_family: pingone-mt
products: ["davinci", "pingone"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/davinci/latest/davinci-overview.html"
---

# PingOne MT — DaVinci Overview

DaVinci is the orchestration engine for PingOne MT. It lets you build no-code/low-code authentication and identity flows using a visual flow canvas, connector library, and reusable subflows.

## Scope

**Covers:** DaVinci flow model, connector types, flow variables, subflow patterns, and DaVinci policy assignment in PingOne.
**Does NOT cover:** PingOne MT environment and app setup — see `ping-foundation`. Flow design patterns — see `references/curated/pingone-mt/davinci-flow-patterns.md`. Detailed connector configuration — see per-connector references.

---

## Flow model

A DaVinci **flow** is a directed graph of **nodes** (connectors) connected by **edges** (transitions). Every flow has:
- A **start node** (HTTP connector or trigger) that receives the initial request
- One or more **success paths** that redirect the user to the application
- One or more **failure paths** that return an error

Flows are versioned. A draft version can be tested without affecting the deployed version.

---

## Connector types

| Category | Description | Examples |
|---|---|---|
| **Core** | Control flow, variable management, error handling | Flow Control, Variables, Functions |
| **Identity** | PingOne user operations, MFA, Verify | PingOne, PingOne MFA, PingOne Verify |
| **Authentication** | External IdPs, social login | PingFederate, Okta, Google |
| **Risk** | PingOne Protect, external risk signals | PingOne Protect, SEON |
| **Notification** | Email, SMS | PingOne Notifications, Twilio |
| **API** | HTTP calls to external systems | HTTP, Generic Connector |

Connectors must be configured with credentials before use. Credentials are stored in DaVinci and can be shared across flows.

---

## Flow variables

DaVinci provides two variable scopes:

| Scope | Lifetime | Use |
|---|---|---|
| **Flow variables** | Single flow execution | Carry data between nodes within one flow invocation |
| **Company variables** | Persistent across flows | Store configuration constants, feature flags, global counters |

Variables are typed: `string`, `number`, `boolean`, `object`, `list`, `secret`.

**Key constraint:** Variables must be declared before they can be read. Undeclared variable reads produce a runtime error.

---

## Subflow patterns

A **subflow** (Annotation: Flow) is a DaVinci flow called from within another flow using the **Flow Connector**. Use subflows to:
- Share logic across multiple flows (e.g., MFA step-up, risk evaluation)
- Keep individual flows focused and below a manageable node count
- Version and test shared components independently

**Subflow output:** The called flow returns its output variables to the parent flow. Map output variable names explicitly in the Flow Connector node.

---

## DaVinci policy assignment in PingOne

A DaVinci flow is exposed to applications via a **DaVinci policy** in PingOne:
1. Create a DaVinci application in DaVinci and assign the flow.
2. In PingOne, create an **Identity Verification Policy** or **Authentication Policy** that references the DaVinci application.
3. Assign the policy to the PingOne application (OIDC or SAML) that initiates authentication.

Without policy assignment, the flow is not reachable from a PingOne OIDC/SAML login.

---

## Prerequisites

- PingOne MT environment with DaVinci enabled
- Admin access to DaVinci console
- At least one PingOne connector configured (for user operations)

## Common variants

- **Workforce flows:** typically triggered by a PingOne SAML or OIDC application; use PingFederate or Okta connectors for upstream federation
- **CIAM flows:** triggered from a web/mobile app; use PingOne MFA + PingOne Verify for progressive registration

## Related references

- `references/curated/pingone-mt/davinci-flow-patterns.md`

## Source

[DaVinci overview](https://docs.pingidentity.com/davinci/latest/davinci-overview.html)
[DaVinci connectors](https://docs.pingidentity.com/davinci/latest/connectors.html)
