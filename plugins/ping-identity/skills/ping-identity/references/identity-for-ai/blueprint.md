# Identity for AI - Securing Digital Assistants Fulfillment Blueprint

## Overview

This blueprint describes a typical Identity for AI outcome: an AI agent or digital assistant acts on behalf of a human user, and every downstream request carries proof of both who authorized the action and which agent performed it.

Securing Digital Assistants is a cross-product composition, not a standalone product. The documented implementations combine an authorization server, an explicit agent identity, OAuth 2.0 token exchange for delegation, and PingGateway as the runtime enforcement point in front of an MCP server or REST resource server. PingOne and PingFederate expose materially different token-exchange configuration surfaces and must be designed as separate variants.

Use this page to decide **what** must be configured and **what** the human user, the agent, the authorization server, and the gateway must accomplish.
Use the owning product skill and current product documentation for **how** to create objects, register clients, configure token managers or resources, call APIs, or deploy a gateway route.

## Scope

This blueprint covers:

- Registering an AI agent or digital assistant as its own identity, distinct from any human's.
- Delegating access through OAuth 2.0 token exchange (RFC 8693) instead of user impersonation.
- The delegation-token claim contract that lets downstream services distinguish the human from the agent.
- Least-privilege issuance: short-lived, audience-restricted, scope-restricted delegation tokens.
- Runtime enforcement of that contract at PingGateway in front of an MCP server or REST API.
- Step-up approval for elevated or out-of-baseline agent actions, where documented.
- Failure, revocation, and audit boundaries for delegated agent access.

## Does not cover

This is not a product configuration runbook. It does not prescribe:

- API payloads, CLI commands, Terraform, SDK code, or exact console-mutation procedures.
- General AI model safety, content moderation, or agent-behavior controls outside identity and access management.
- Product pricing, quotas, licensing, or release-state details.
- An equivalent worked composition for PingOne Advanced Identity Cloud (AIC) or PingAM. The cited use-case pages name both as supported authorization servers but document a full delegation composition only for PingOne and PingFederate.
- Agent-to-agent (A2A) delegation chains or MCP tool-level authorization detail beyond the single-hop delegation shown in the cited pages.

If the platform is not known, ask for it before selecting an authorization-server variant. Do not infer an AIC or PingAM composition from the PingOne or PingFederate examples.

## Fulfillment contract

### Actors

| Actor | Responsibility |
|---|---|
| Human user (customer or employee) | Authenticates to the host application, consents to agent delegation, and becomes the `sub` of every delegated token issued on their behalf. |
| AI agent or digital assistant | Holds its own registered identity and credentials, separate from the human's. Obtains its own token, then exchanges the user's token together with its own credentials for a delegation token. Never receives or uses the human's credentials directly. |
| Host application | Authenticates the human, obtains the initial subject token, and hands it to the agent when the human requests an agent-performed action. |
| Authorization server (PingOne, AIC, PingFederate, or PingAM) | Authenticates the agent, validates the subject and actor tokens, applies the token-exchange policy, and issues a delegation token scoped to the target resource. |
| PingGateway | Runtime security proxy in front of the protected resource. Validates the delegation token's actor claim, audience, and scope before proxying the request. |
| Backend resource server (MCP server or REST API) | Executes the requested operation only within the granted scope and audience, and logs both the human and agent identity for audit. |
| Optional step-up authenticator (for example CIBA) | Obtains explicit human approval when the agent requests an operation outside its baseline granted scope. |

### Expected outcome

Success means a resource server can attribute every agent-performed action
to both the specific human who authorized it and the specific agent that
performed it, using a delegation token that is short-lived and restricted
to the resource and scope actually needed. An agent obtaining a token, or a
gateway merely forwarding a request, is not by itself a successful
outcome — the delegation token must carry a verifiable actor claim, and the
gateway and resource server must enforce it.

## Platform decision boundary

Select the variant before choosing product skills or execution surfaces.

| Environment signal | Variant and delegation mechanism | Enforcement |
|---|---|---|
| PingOne environment with AI Agent registration and custom resources | PingOne issues the agent's own token, then performs OAuth 2.0 token exchange against a resource-specific `may_act`/`act` claim mapping. | PingGateway introspects the exchanged token against the target resource's client credentials and required scope. |
| PingFederate environment with Token Exchange and an Access Token Manager | PingFederate validates separate subject-token and actor-token JWT Token Processors through a Token Exchange Processor Policy, then issues a delegated access token via an Access Token Mapping. | PingGateway, PingAccess, or PingAuthorize can validate the issued token at the edge, depending on which are deployed. |
| AIC tenant or PingAM instance named as the authorization server | Stop. The cited use-case pages list AIC and PingAM as supported authorization products but do not document a worked token-exchange composition for either. Route to the AIC or PingAM reference first; do not assume the PingOne or PingFederate composition applies unmodified. | Not established by the cited pages. |
| Platform not identified | Stop and request the platform. | Do not infer PingOne AI Agent objects or a PingFederate Access Token Manager. |

## Shared fulfillment lifecycle

Use this as the solution-level sequence, not as a console or API-call prescription:

1. Confirm the authorization-server platform and the resource the agent needs to reach.
2. Register the AI agent as its own identity, with its own credentials, distinct from any human's.
3. The human authenticates to the host application and consents to the agent acting on their behalf.
4. The agent obtains its own actor token from the authorization server, independent of any user session.
5. The agent obtains (or is handed) a subject token representing the authenticated human.
6. The agent submits the subject token and its own actor credentials to the authorization server's OAuth 2.0 token-exchange endpoint, naming the target resource and requested scope.
7. The authorization server validates both tokens, confirms the delegation relationship is authorized, and issues a delegation token containing the human as `sub` and the agent as `act.sub`, restricted to the requested audience and scope.
8. The agent presents the delegation token to PingGateway (or another edge enforcement point) in front of the target resource.
9. The gateway validates the token's audience, scope, and actor claim, then proxies the validated request to the resource server.
10. The resource server executes the operation and records both the human and agent identity for audit.
11. If the agent needs an operation outside its granted baseline scope, it triggers a step-up approval flow (for example CIBA) before a wider-scoped delegation token is issued.
12. Preserve enough token, transaction, and policy-version context to reconstruct which human authorized which agent action, subject to the organization's privacy and retention requirements.

The solution must define what happens when delegation is denied, expired, or scoped incorrectly. Avoid designs where an agent can act with a token that omits the actor claim, or where a gateway accepts a token whose audience does not match the resource it protects.

## Delegation token contract

| Claim | Meaning | Design constraint |
|---|---|---|
| `iss` | Authorization server that issued the delegation token. | Must match what the resource server and gateway trust. |
| `aud` | The specific resource server or MCP endpoint the token authorizes. | Restrict to one resource per exchange; re-exchange for a different resource rather than widening the audience. |
| `sub` | The human who authorized the action. | Never the agent's own identifier. |
| `act.sub` | The identifier of the acting agent. | Must be present whenever the token results from a delegation exchange; its absence means the token cannot be attributed to a specific agent. |
| `scope` | The narrow permission granted for the current action. | Keep to the minimum the current operation requires; request a new exchange for a different or elevated scope rather than granting broad scope up front. |
| `iat` / `exp` | Issuance and expiration time. | Keep the lifetime short; treat the token as non-refreshable for the delegated action. |

Do not treat a token that lacks `act.sub` as evidence of delegated,
attributable agent access, even if it otherwise authenticates successfully.

## Failure, recovery, and audit boundaries

Design these states before implementation:

| State | Required architectural handling |
|---|---|
| Delegation succeeds, `act.sub` present, scope and audience correct | Permit only the specific operation the granted scope covers. |
| Actor claim missing or `act.sub` does not match the presenting agent | Reject at the gateway or resource server; do not treat the token as valid delegated access. |
| Expired or reused delegation token | Require a fresh token-exchange call; do not accept a cached or expired token. |
| Agent requests a scope beyond its granted baseline | Route to the configured step-up approval path (for example CIBA); do not silently widen scope. |
| Human revokes consent or the agent identity is disabled | The authorization server must refuse further token exchange for that agent or that human-agent pairing. |
| Gateway or resource server cannot reach the authorization server for introspection/validation | Fail closed; do not proxy the request unvalidated. |
| Authorized delegation with no downstream action configured | Return a clear incomplete-configuration outcome; do not imply the token itself performs the action. |

Capture the identifiers and version context needed to correlate the human,
the agent, the delegation transaction, the granted scope, and the resource
accessed, subject to the organization's privacy and retention
requirements. Separate operational audit logging from any storage of the
underlying subject or actor token material.

## PingOne variant: AI Agent registration and resource-mapped token exchange

See [PingOne variant reference](blueprint-pingone.md).

## PingFederate variant: Access Token Manager and Token Exchange Processor Policy

See [PingFederate variant reference](blueprint-pingfederate.md).

## Implementation handoffs

After selecting the platform, continue with the owning references for the **how**:

- [PingOne platform](../pingone/README.md) — host environment and AI Agent object surface.
- [Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) — AIC tenant context; no worked delegation composition is established here.
- [PingFederate](../pingfederate/README.md) — token-exchange, Access Token Manager, and OAuth client surface.
- [PingAM](../pingam/README.md) — self-managed access-management context; no worked delegation composition is established here.
- [PingGateway](../pinggateway/README.md) — runtime enforcement proxy in front of the protected resource.

Select API, CLI, Terraform, MCP, or SDK execution surfaces only after the platform, resource, and delegation intent are known. This skill is an orientation and routing layer; it does not mutate a tenant.

## Verification checklist

Before calling the solution ready for a test or production handoff, confirm:

- The authorization-server platform and variant are explicit.
- The agent is registered with its own credentials, distinct from any human's.
- The human's consent to agent delegation is captured and can be revoked.
- The delegation token contains both `sub` (human) and `act.sub` (agent) whenever the action is agent-performed.
- Token audience and scope are restricted to the specific resource and operation, not granted broadly.
- PingGateway (or the deployed enforcement point) rejects tokens with a missing or mismatched actor claim.
- Step-up approval is tested for any operation outside the agent's baseline scope, where configured.
- Revocation of the agent identity or the human's consent is tested and takes effect on the next exchange.
- Audit logging correlates the human, the agent, the granted scope, and the resource accessed.
- Production rollout, policy, and rollback decisions are reviewed in the owning platform skill.

## Related references

- [Identity for AI overview](README.md)

## Source

- [Securing Digital Assistants](https://developer.pingidentity.com/identity-for-ai/use-cases/idai-securing-digital-assistants.html)
- [Securing AI agents with PingOne using delegation and least privilege](https://developer.pingidentity.com/identity-for-ai/use-cases/idai-securing-agents-pingone.html)
- [Securing AI agents with PingFederate using delegated access tokens](https://developer.pingidentity.com/identity-for-ai/use-cases/idai-securing-agents-pingfed.html)
- [Product Index](https://docs.pingidentity.com/product-index.html)
