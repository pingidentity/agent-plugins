# Authentication Orchestration

## Overview
Authentication orchestration is the design of identity experiences — sign-in, registration, recovery, MFA, step-up, passwordless, social login, and profile management — expressed as explicit, testable flows. In this topic an **experience** means that end-to-end sequence of steps and what the user sees at each one; each Ping platform builds it with a different construct: journeys/trees of nodes in PingAM and Advanced Identity Cloud, connector-based flows in PingOne DaVinci, and authentication policies in PingFederate. This topic covers the design-level concepts that are common across those platforms: lifecycle modeling, friction and assurance, fallback behavior, and operational readiness. It is design orientation only — implementation detail lives in product documentation and product-specific skills.

## Core Concepts
- **Experiences as lifecycle models:** An experience is not a login screen; it models where the actor starts (invited, pending verification, active, suspended, locked, closed) and what state they leave in.
- **Actor and state modeling:** Define actor types (customer, employee, admin, delegated admin, machine) and the attributes that matter (email, phone, locale, MFA state, recovery identifiers, entitlements) consistently across all flows — drift between apps is a primary support burden.
- **Friction matched to risk:** Use a small set of risk outcomes — allow, light check, step-up, limited fallback, safe deny — and apply friction when the action justifies it, not uniformly to every user.
- **Explicit branching and explainability:** Every branch should answer what happened, what the user sees, and what they can do next. Hidden behavior that exists only in scripts or policy conditions erodes supportability.
- **Fallback and degraded-mode behavior:** Risk engines, notification providers, identity stores, and upstream identity providers fail. Design alternate routes and clear stopping points; avoid loops, blank screens, and silent retries.
- **Session and assurance posture:** Decide explicitly how sessions, tokens, and assurance levels change after sign-in, password change, privilege elevation, MFA reset, and device changes — and make the change visible in the experience.
- **Safe messaging and anti-enumeration:** User-facing text explains the next step without exposing policy outcomes, protocol details, or account existence.
- **Versioning and promotion as design concerns:** Experiences are products, not one-time diagrams. Release discipline, telemetry, and rollback plans are part of the design.

## When to use
- Designing or reviewing an authentication experience — sign-in, registration, recovery, or MFA — before selecting product nodes, connectors, or policy constructs.
- Comparing how a design concept (step-up, passkey enrollment, account recovery) maps across Ping platforms.
- Establishing design standards, experience review checklists, or supportability requirements for identity flows.

## When not to use
- For node, connector, or API configuration detail — use the product documentation for the target platform.
- For protocol internals (OAuth 2.0, OIDC, SAML, WebAuthn mechanics), use the protocol specifications and product protocol documentation.
- This topic is not an API, configuration, or product-limit reference.

## Design references

| Request signal | Reference |
|---|---|
| Orchestration design principles, fallback patterns, reliability patterns | `orchestration-design-principles.md` |
| Passkey and passwordless design tiers and patterns | `passkeys-and-passwordless.md` |

## Integrations
- Platform-specific experience models: [PingOne Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) and [PingAM](../pingam/README.md) share a node-and-tree journey model; [PingOne DaVinci](../pingone-davinci/README.md) uses a connector-based flow model; [PingFederate](../pingfederate/README.md) implements orchestration as authentication policies.
- Moving flow and authentication-policy configuration between environments: [Ping Configuration Promotion](../configuration-promotion/README.md).

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Advanced Identity Cloud journeys documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [PingOne DaVinci documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
- [PingFederate documentation](https://docs.pingidentity.com/pingfederate/latest/index.md)
