# Researching a PingOne Advanced Identity Cloud applications integration

## Scope

Use this compact brief for **application integration** with PingOne Advanced Identity Cloud (AIC). An application authenticates its users through AIC as an OIDC, SAML, or WS-Federation application (agent), with authentication itself delivered by a journey in the application's realm.

### Covers

- The target AIC tenant and realm (Alpha for consumer/CIAM, Bravo for workforce), the application agent, and the journey the application hands off to.
- Realm-scoped OAuth 2.0 and OIDC endpoints, client registration, and the token and session handling the application owns.
- Tenant-level CORS configuration and the AM services prerequisite for journey features the application depends on.

### Does NOT cover

- Tenant mutations, application fields, protocol payloads, secrets, executable journeys, or configuration commands.
- Journey or tree authoring; this brief assumes the required journey exists and runs end-to-end.
- Detailed SDK implementation steps; those live in current product documentation and product-specific skills.

Treat this as orientation, not configuration authority. Use the current AIC applications, journeys, OAuth 2.0, and tenant documentation for implementation details.

## Research brief

Establish the tenant, realm, and application agent first. Applications connect to AIC as OIDC, SAML, or WS-Federation agents; their authentication is delegated to a journey in the agent's realm, so the realm choice (Alpha or Bravo) scopes the endpoints, the journey, and the user population together. A common documented lifecycle is: register the application agent with its redirect URIs and scopes; attach or rely on the realm's default authentication journey; configure tenant CORS for the application's origin so browser-based flows work; authenticate through the journey; and have the application validate and process the returned tokens or assertions.

Journey-dependent application features presuppose the corresponding AM services in the tenant (push, OATH, WebAuthn, social identity providers, device profiles) — these fail at runtime, not design time, when the service is not configured. CORS in AIC is a tenant-level global setting rather than per-application; verify current accepted-origin, method, and header semantics in tenant documentation.

## Resource index

- [PingOne Advanced Identity Cloud reference](./README.md)
- [Authentication Orchestration reference](../orchestration/README.md)
- [App integration concepts reference](../app-integration/README.md)
- [PingOne Advanced Identity Cloud documentation](https://docs.pingidentity.com/pingoneaic/home.md)
- [AIC developer documentation](https://developer.pingidentity.com/)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Tenant, realm, and agent | Which tenant and realm own the application agent, and which journey handles its authentication? | Do not treat the agent as detached from its realm or from the journey that backs it. |
| Protocol surface | Is the application an OIDC, SAML, or WS-Federation agent? | Verify current agent-type and redirect-URI constraints in documentation. |
| CORS | Is tenant CORS configured for the origins that perform in-browser flows? | Confirm tenant-global CORS semantics and defaults in current documentation. |
| AM services | Do the journey features the application depends on have their AM services configured in the tenant? | Verify service prerequisites (push, OATH, WebAuthn, social, device profiles) per journey. |
| Runtime | How does the application launch sign-on, exchange tokens, and handle refresh and logout? | Confirm endpoints, claims, and token lifetimes in current documentation. |
| Promotion and operations | What tenant-specific agent, journey, service, and endpoint values must be recreated or checked? | Verify realm bindings, keys, redirect values, and drift. |

## Guardrails and report

Keep the tenant, realm, application agent, backing journey, protocol surface, and application token handling visible in the report. Do not present the application agent as a standalone generic token service, and do not turn this brief into an SDK implementation runbook.

Report: (1) the tenant, realm, and application agent boundary; (2) the journey that handles authentication; (3) the verified protocol path; (4) tenant CORS and AM-services prerequisites; (5) application token handling; and (6) the appropriate handoff to the [PingOne Advanced Identity Cloud reference](./README.md), [Authentication Orchestration reference](../orchestration/README.md), or current official documentation.
