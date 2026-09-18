---
name: aic-journey-design
description: "Use when designing or building PingOne Advanced Identity Cloud (AIC) journeys or PingAM authentication trees — login, registration, account recovery, MFA enrollment and authentication, passwordless and passkeys, social login, progressive profiling, risk-based step-up with PingOne Protect, scripted decision nodes, and inner journeys. Creates and updates journeys through AIC MCP tools when connected; otherwise produces journey design artifacts."
compatibility: "Journey creation and updates use the PingOne Advanced Identity Cloud MCP tools when connected (createJourney, updateJourneyNode). Without MCP tools, produce node sequences, wiring, and configuration tables as design artifacts. PingAM trees are covered as design guidance validated against PingAM documentation for the target release."
metadata:
  publisher: Ping Identity
  version: "0.1.0"
  product_family: aic
---

# AIC Journey Design

Design and build authentication journeys for PingOne Advanced Identity Cloud (AIC) and PingAM authentication trees. MCP tools handle journey creation and updates where available; this skill supplies node selection, sequencing, wiring, and platform constraints as design artifacts otherwise.

## Scope

- Login, registration, recovery, MFA, step-up, passwordless, social login, and transaction-approval journeys.
- AIC journeys and PingAM authentication trees (shared node model).
- Scripted decision nodes, inner journeys, page composition, callback/collector sequencing, risk branches, session state, and assurance changes.
- Journey design, review, implementation, resilience, and promotion between environments.

## MCP execution

Use available MCP execution tools for AIC journey operations (createJourney, updateJourneyNode) when present. Otherwise, produce the journey design, node sequencing, branching logic, and platform constraints as implementation artifacts without setup or tool-installation instructions.

When creating journeys with the `createJourney` MCP tool, read `references/mcp-journey-authoring.md` first — the PageNode child-node pattern has a known failure mode.

## PingAM note

AIC and PingAM share the same node-and-tree model. Node guidance here is written against AIC; validate node availability and behavior against the PingAM documentation for the target release, and account for differences (realms, redirect validation, session settings).

## Routing

**Quick reference — node families:**

| Task | Reference |
|---|---|
| Node composition rules, PageNode usage, child node gotchas | `references/nodes/node-fundamentals.md` |
| Username/password, passthrough auth, session entry, lifecycle outcomes | `references/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, authorization signals | `references/nodes/risk-management-nodes.md` |
| Registration, attributes, consent, KBA, terms, social login, SelectIdP | `references/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount | `references/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/nodes/federation-contextual-nodes.md` |

**Named journey scenarios:** see `references/routing-index.md` — match the task to a use case first; use-case anchors are self-contained and include node guidance. If no use case matches, select 1–2 node-family anchors above.

**Design and cross-cutting references:**

| Task | Reference |
|---|---|
| Design checklist, AIC security lens, wiring invariants | `references/design-notes.md` |
| Passkey and passwordless journeys (registration, authentication, recovery) | `references/passkey-journeys.md` |
| Promoting journeys, scripts, themes between environments (ESVs, locks, rollback) | `references/journey-promotion.md` |
| MCP journey creation gotchas (PageNode two-step pattern) | `references/mcp-journey-authoring.md` |
| WebAuthn/passkeys on native mobile — AIC-side prerequisites | `references/aic-config/webauthn-mobile-setup.md` |
