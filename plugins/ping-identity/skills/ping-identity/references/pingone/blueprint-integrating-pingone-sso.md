# Researching a PingOne SSO integration

## Scope

Use this compact brief for **PingOne SSO** integrations. PingOne SSO is attached to a PingOne environment; the application uses it through an application sign-on policy or a PingOne DaVinci flow.

### Covers

- The target PingOne organization and environment, application, population, and sign-on policy or DaVinci flow.
- The selected SAML, OAuth, or OIDC application integration and its authentication handoff.
- The application-owned handling of the returned assertion or tokens and the operational checks around promotion.

### Does NOT cover

- Tenant mutations, application fields, protocol payloads, secrets, executable flows, or configuration commands.
- A generic federation design that does not identify the PingOne environment and owning application sign-on policy or DaVinci flow.

Treat this as orientation, not configuration authority. Use the current PingOne application, sign-on policy, DaVinci, protocol, and developer documentation for implementation details.

## Research brief

Establish the PingOne environment and application first. Confirm whether the application is bound to an application sign-on policy or launched through a PingOne DaVinci flow, then identify the selected SAML, OAuth, or OIDC integration and the application’s handling of the resulting assertion or tokens. These are distinct execution paths even when they provide centralized sign-on.

A common documented lifecycle is: configure the application and its sign-on policy or DaVinci flow; launch the application through that binding; authenticate in the PingOne environment; return the protocol response; and have the application validate and process the response. Verify protocol-specific schemas, redirect or assertion settings, signing keys, claims, scopes, and lifecycle behavior in current documentation rather than inferring them here.

## Resource index

- [PingOne SSO reference](./README.md)
- [PingOne platform reference](../pingone/README.md)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [PingOne platform documentation](https://docs.pingidentity.com/pingone/p1_cloud__platform_main_landing_page.md)
- [PingOne getting started documentation](https://docs.pingidentity.com/pingone/getting_started_with_pingone/p1_p1sso_start.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Environment and ownership | Which PingOne environment owns the application, and which application sign-on policy or DaVinci flow launches it? | Do not treat SSO as detached from the PingOne environment or as an ad-hoc flow test. |
| Protocol | Is the integration SAML, OAuth, or OIDC? | Verify current protocol-specific application and response requirements. |
| Runtime | How does the application launch sign-on, validate the response, and handle errors or session state? | Confirm current claims, scopes, redirect or assertion settings, keys, and token/response validation. |
| Promotion and operations | What environment-specific application, policy, flow, key, and endpoint values must be recreated or checked? | Verify bindings, signing keys, redirect values, audit visibility, and drift. |

## Guardrails and report

Keep the PingOne environment, application, sign-on policy or DaVinci flow, protocol, and application response handling visible in the report. Do not present PingOne SSO as a standalone generic token service, and do not turn this brief into a protocol configuration runbook.

Report: (1) the PingOne environment and application boundary; (2) the owning application sign-on policy or DaVinci flow; (3) the verified protocol path; (4) application response handling; (5) promotion and unresolved checks; and (6) the appropriate handoff to the [PingOne SSO reference](./README.md), [PingOne platform reference](../pingone/README.md), [PingOne DaVinci reference](../pingone-davinci/README.md), or current official documentation.
