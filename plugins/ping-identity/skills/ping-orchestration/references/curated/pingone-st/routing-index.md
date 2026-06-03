---
title: "PingOne ST — Orchestration Routing Index"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html"
---

# PingOne ST — Orchestration Routing Index

Sub-routing table for the `ping-orchestration` skill. Use this file to select the correct curated anchor when the task falls under the PingOne ST / AIC / PingAM platform branch.

## Scope

**Covers:** Node-family routing, journey use case routing, and fallback order for PingOne ST orchestration tasks.
**Does NOT cover:** DaVinci flow routing — see `../pingone-mt/davinci-overview.md`. Platform setup — see `ping-foundation`.

---

## Node-family routing

| Task | Reference |
|---|---|
| Journey design principles, patterns, resilience, security | `references/curated/pingone-st/journey-design-patterns.md` |
| Node composition rules, PageNode usage, child node gotchas | `references/curated/pingone-st/nodes/node-fundamentals.md` |
| Username/password collection, ValidatedUsernameNodeV2, passthrough auth, session entry, lifecycle outcomes | `references/curated/pingone-st/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/curated/pingone-st/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, PingOne Authorize | `references/curated/pingone-st/nodes/risk-management-nodes.md` |
| User registration, attributes (PRESENT/EQUALS), consent, KBA, T&C, social login, SelectIdP, TimeSince | `references/curated/pingone-st/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount (AT/EVERY), EmailSuspend/EmailTemplate config | `references/curated/pingone-st/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/curated/pingone-st/nodes/federation-contextual-nodes.md` |

---

## Journey use case routing

Load the matching use-case anchor when the task maps to a named scenario:

| Use case | Reference |
|---|---|
| Account recovery, username reminder, anti-enumeration | `references/curated/pingone-st/journey-use-cases/account-recovery-and-username-reminder.md` |
| Password reset (unauthenticated) or password update (authenticated) | `references/curated/pingone-st/journey-use-cases/password-reset-and-update.md` |
| MFA device registration (WebAuthn, OATH, Push, SMS, VOICE) | `references/curated/pingone-st/journey-use-cases/passwordless-mfa-registration.md` |
| Multi-method MFA authentication with retry loops and recovery codes | `references/curated/pingone-st/journey-use-cases/mfa-authentication-multi-method.md` |
| PingOne Protect risk integration (init/eval pattern, step-up chain) | `references/curated/pingone-st/journey-use-cases/pingone-protect-risk-integration.md` |
| Financial services step-up, transaction authorization, PingOne Authorize | `references/curated/pingone-st/journey-use-cases/financial-services-step-up.md` |
| Progressive profiling (login-count trigger, attribute gate) | `references/curated/pingone-st/journey-use-cases/progressive-profiling.md` |
| Social + local registration and authentication, email verification gate | `references/curated/pingone-st/journey-use-cases/social-and-local-registration-authentication.md` |

---

## Retrieval order

1. Match the task to a use case row first — use-case anchors are self-contained and include node guidance.
2. If no use case matches, select 1–2 node-family anchors from the node-family table.
3. If neither is sufficient, fall back to `references/generated/pingone-st/top-25.json`.

## Prerequisites

- PingOne AIC or PingAM tenant with at least one realm and journey capability enabled.

## Common variants

- AIC (PingOne Advanced Identity Cloud) and PingAM share the same node model; AIC adds ESVs, hosted pages, and tenant-security constraints.

## Related references

- `references/curated/pingone-st/journey-design-patterns.md`
- `references/curated/pingone-mt/davinci-overview.md`

## Source

[Authentication nodes — PingOne AIC](https://docs.pingidentity.com/pingoneaic/journeys/auth-nodes.html)
