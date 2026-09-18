# Researching a PingOne applications integration

## Scope

Use this compact brief for **application integration** on PingOne. An application authenticates users or services against a PingOne environment through an application record, its sign-on policy or DaVinci flow policy, and the OAuth 2.0/OIDC protocol surface.

### Covers

- The target PingOne organization and environment, the application record (OIDC client, redirect URIs, grant types), and the owning population.
- The launch surface that binds authentication to the application: application sign-on policy or DaVinci flow policy.
- The application-owned handling of tokens, CORS settings on the application, and the Worker-application model for service principals.

### Does NOT cover

- Tenant mutations, application fields, protocol payloads, secrets, executable flows, or configuration commands.
- DaVinci flow authoring or collector sequencing; this brief assumes the required flow or sign-on policy exists.
- Detailed SDK implementation steps; those live in product documentation and product-specific skills.

Treat this as orientation, not configuration authority. Use the current PingOne application, sign-on policy, DaVinci, protocol, and developer documentation for implementation details.

## Research brief

Establish the PingOne environment and application first. Confirm whether the application authenticates through an application sign-on policy or launches a DaVinci flow through a flow policy — these are distinct launch surfaces even when both provide centralized sign-on. Identify the protocol surface (OIDC for most app integrations; SAML where federation is required) and confirm the environment's OAuth settings support the grants the application needs.

A common documented lifecycle is: create the application record with its redirect URIs and grant types; attach a sign-on policy or DaVinci flow policy; configure the application's CORS settings so browser-based token exchange works from the application's origin; authenticate; and have the application validate and process the returned tokens. Application CORS settings are per-application, are not derived from redirect URIs, and follow the environment's default-origin semantics — verify current behavior in the application documentation. Worker applications act as service principals for backend and M2M integrations and are a separate application type from browser or native application records.

## Resource index

- [PingOne platform reference](./README.md)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingOne MFA reference](../pingone-mfa/README.md)
- [App integration concepts reference](../app-integration/README.md)
- [PingOne applications documentation](https://docs.pingidentity.com/pingone/applications/p1_applications_landing_page.md)
- [PingOne developer documentation](https://developer.pingidentity.com/pingone-api/platform/)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Environment and ownership | Which PingOne environment owns the application, and which sign-on policy or DaVinci flow policy launches authentication? | Do not treat the application as detached from its environment or as an ad-hoc flow test. |
| Application record | What redirect URIs, grant types, and token settings does the application record carry? | Verify current application-type and grant constraints in documentation. |
| CORS | Are the application's CORS settings aligned with the origins that perform in-browser token exchange? | Confirm per-application CORS semantics and defaults in current documentation. |
| Worker applications | Does the backend use a Worker application as its service principal, with the grants and scopes it needs? | Confirm Worker vs browser/native application-type differences before wiring M2M clients. |
| Runtime | How does the application launch sign-on, exchange tokens, and handle refresh and logout? | Confirm endpoints, claims, and token lifetimes in current documentation. |
| Promotion and operations | What environment-specific application, policy, flow, and endpoint values must be recreated or checked? | Verify bindings, keys, redirect values, audit visibility, and drift. |

## Guardrails and report

Keep the PingOne environment, application record, launch surface (sign-on policy or DaVinci flow policy), protocol, and application token handling visible in the report. Do not present the application record as a standalone generic token service, and do not turn this brief into an SDK implementation runbook.

Report: (1) the PingOne environment and application boundary; (2) the owning sign-on policy or DaVinci flow policy; (3) the verified protocol path; (4) application CORS and token handling; (5) Worker-application needs for backends; and (6) the appropriate handoff to the [PingOne platform reference](./README.md), [PingOne DaVinci reference](../pingone-davinci/README.md), or current official documentation.
