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
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/davinci/davinci_introduction.html"
---

# PingOne MT — DaVinci Overview

DaVinci is the orchestration engine for PingOne MT. It lets you build no-code/low-code authentication and identity flows using a visual flow canvas, connector library, and reusable subflows. Flows guide users through IAM activities — registration, authentication, MFA, account recovery, and self-service — and are deployed to PingOne applications via a flow policy.

## Scope

**Covers:** DaVinci flow model, node types, logical operators, connector model, flow variables, versioning and deployment, subflow patterns, and flow invocation methods.
**Does NOT cover:** PingOne MT environment and app setup — see `ping-foundation`. Flow design patterns — see `references/curated/pingone-mt/davinci-flow-patterns.md`. Detailed connector configuration — see per-connector references.

---

## Flow model

A DaVinci **flow** is a directed graph of **nodes** connected by **logical operators**. Every flow has:
- A **start node** (HTTP connector or trigger) that receives the initial request
- **Nodes** — each performs exactly one task via a connector capability
- **Logical operators** — sit between nodes, route execution based on outcomes
- One or more **success paths** that redirect the user to the application
- One or more **failure paths** that return an error

**Node visual types:**
| Border | Meaning |
|---|---|
| Dotted | Involves user interaction (forms, displays) |
| Solid | Runs silently in the background |

---

## Logical operators

| Operator | Behavior |
|---|---|
| If All True | All preceding nodes succeeded |
| If Any True | At least one node succeeded |
| If All False | All preceding nodes failed |
| If Any False | At least one node failed |
| All Triggers Complete | All nodes finished (success or failure) |
| Any Trigger Completes | Any node finished (success or failure) |

Use **If All True** for sequential happy-path steps. Use **If Any True** when any one of several parallel checks is sufficient to proceed.

---

## Connector model

Connectors integrate DaVinci with Ping products or external services. Each connector exposes discrete **capabilities** (specific actions).

| Category | Examples |
|---|---|
| Core | Flow Control, Variables, Functions — no external config needed |
| Identity | PingOne (user CRUD, MFA, Verify), PingOne Notifications |
| Authentication | PingFederate, Okta, Google, Apple |
| Risk | PingOne Protect, SEON |
| Notification | Twilio, Mailchimp |
| API | HTTP, Generic Connector (arbitrary REST calls) |

**Connector instances:** The same connector can be added multiple times with different credentials — use one instance for dev, another for production. Configuration changes to an instance propagate to every flow node using that instance automatically.

**Credential storage:** Credentials are stored at the connector instance level, not per node. Enter them once; all flow nodes sharing the instance use the same credentials.

---

## Flow variables

| Scope | Lifetime | Use |
|---|---|---|
| Flow variables | Single flow execution | Carry data between nodes within one flow invocation |
| Company variables | Persistent across flows | Configuration constants, feature flags, global counters; shared across all flows in the environment |

Variable types: `string`, `number`, `boolean`, `object`, `list`, `secret`.

**Key constraint:** Variables must be declared before they can be read. Reading an undeclared variable produces a runtime error that silently skips the node in some cases — always declare explicitly.

**UI Studio:** A companion tool for customizing the HTML/CSS of DaVinci-hosted pages (hosted by DaVinci, not your application). Use it to apply branding without writing raw HTML.

---

## Versioning and deployment

| Action | Effect |
|---|---|
| **Save** | Creates a new version entry; does not affect the live (deployed) flow |
| **Deploy** | Publishes the current saved state as the live version |
| **Try Flow** | Test run using the deployed version; grayed out if flow has never been deployed |
| **Flow Versions → Revert** | Roll back to any prior version |

**Draft vs. deployed:** Changes are only visible to users after Deploy. Save frequently to preserve version history. Revert without re-deploying to roll back.

**Debug logging:** Enable via More options → Flow Settings → Logging → Debug. Required for diagnosing node-level failures and unexpected branching.

---

## Subflow patterns

A **subflow** is a DaVinci flow called from within another flow using the **Flow Connector**. Use subflows to:
- Share logic across multiple flows (e.g., MFA step-up, risk evaluation, email verification)
- Keep individual flows focused and below a manageable node count
- Version and test shared components independently

**Subflow output:** The called flow returns its output variables to the parent flow. Map output variable names explicitly in the Flow Connector node. All subflows must define both a success path and a failure path that the parent flow handles.

---

## Flow invocation methods

A DaVinci flow is exposed to users via one of three methods:

| Method | How it works | Best for |
|---|---|---|
| **Redirect** | Full-page redirect to DaVinci-hosted URL; OIDC/SAML authentication via PingOne policy | Flows with UI; fastest to deploy; no custom HTML required |
| **Widget** | Flow embedded in the application page; stays on same URL | When UX must remain on the app's own domain; requires minimal app-side code |
| **API** | Flow invoked via direct API call | Flows without direct user interaction (M2M, backend orchestration) |

**Redirect integration steps:**
1. Build the flow in DaVinci and Deploy it.
2. Create a DaVinci Application in DaVinci; assign the flow and a flow policy.
3. In PingOne, assign the DaVinci flow policy to the PingOne application's sign-on policy.
4. PingOne OIDC/SAML login now triggers the DaVinci flow.

**A/B testing:** DaVinci applications support splitting traffic across flow versions or different flows for controlled rollouts.

---

## Prerequisites

- PingOne MT environment with DaVinci service activated
- Admin access to DaVinci console (`davinci.pingidentity.com`)
- At least one PingOne connector instance configured for user operations

## Common variants

- **Workforce flows:** triggered by a PingOne SAML or OIDC application; use PingFederate or Okta connectors for upstream federation; MFA step-up on resource access
- **CIAM flows:** triggered from a web/mobile app; progressive registration via redirect; PingOne MFA + PingOne Verify for onboarding
- **Template-based:** download a pre-built flow JSON from the Ping Identity Marketplace, import it via Add Flow → Import From JSON, then customize

## Related references

- `references/curated/pingone-mt/davinci-flow-patterns.md`

## Source

[DaVinci introduction](https://docs.pingidentity.com/davinci/davinci_introduction.html)
[DaVinci flows](https://docs.pingidentity.com/davinci/flows/davinci_flows.html)
[Getting started with flows](https://docs.pingidentity.com/davinci/flows/davinci_getting_started.html)
[Connectors](https://docs.pingidentity.com/davinci/connectors/davinci_connections.html)
[Implementing a flow in an application](https://docs.pingidentity.com/davinci/integrating_flows_into_applications/davinci_how_to_implement_a_flow.html)
[Best practices](https://docs.pingidentity.com/davinci/davinci_best_practices/davinci_best_practices.html)
