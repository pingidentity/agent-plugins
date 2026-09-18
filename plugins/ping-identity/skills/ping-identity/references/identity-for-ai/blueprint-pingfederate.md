# Identity for AI - PingFederate variant: Access Token Manager and Token Exchange Processor Policy

## Composition

The documented PingFederate composition uses:

- OAuth 2.0 Token Exchange (RFC 8693), with the agent submitting a `subject_token` (the human's identity JWT) and an `actor_token` (the agent's own identity JWT) to PingFederate's token endpoint.
- A dedicated JWT **Access Token Manager** that defines the delegated-token contract (`sub`, `act`, `scope`, short lifetime, `at+jwt` type).
- Separate subject-token and actor-token **JWT Token Processors**, each trusting its own issuer and JWKS, so the human's identity JWT and the agent's identity JWT are validated independently.
- A **Token Exchange Processor Policy** that binds those processors and produces `subject`/`actor_sub` policy attributes, and an **Access Token Mapping** that turns those attributes into the issued token's `sub` and nested `act.sub` claims.
- An **OAuth client** registered for the agent, authenticated with private-key JWT (or client secret/TLS), enabled for the `TOKEN_EXCHANGE` grant and, optionally, `CIBA` for step-up approval of elevated scopes.
- Optional workload-identity actor tokens issued by a SPIFFE/SPIRE identity provider instead of a conventional service JWT.

Downstream enforcement (PingGateway, PingAccess, or PingAuthorize) validates the issued delegation token's signature, issuer, audience, expiration, and scope, and treats `act.sub` as the acting agent's identity for audit.

## Critical configuration concepts

| Concern | Required concept |
|---|---|
| Access Token Manager | A JWT Access Token Manager defines the issued delegation token's shape: short lifetime, centralized signing, `at+jwt` type, and an extended attribute contract carrying `sub`, `act`, and `scope`. |
| Scope design | Baseline agent scopes are distinguished from elevated or sensitive scopes; elevated scopes are excluded from the agent's default grant and require the step-up path before being issued. |
| Subject and actor token processors | Two separate JWT Token Processors validate the human's identity JWT and the agent's identity JWT respectively, each against its own trusted issuer, JWKS endpoint, required audience, and required expiration. |
| Token Exchange Processor Policy | The policy requires an actor token, accepts JWT subject and actor token types, and extracts the human's subject and the agent's subject into distinct policy attributes for downstream mapping. |
| Access Token Mapping | The mapping supplies the issued token's `sub` from the human's policy attribute and constructs a nested `act.sub` from the agent's policy attribute; scope is populated from the granted scopes, not mapped directly. |
| OAuth client registration | The agent is registered as its own OAuth client, authenticated independently of any human (private-key JWT is the documented preference), enabled for the `TOKEN_EXCHANGE` grant and bound to the delegation Access Token Manager. |
| Step-up approval | An operation outside the agent's baseline granted scope triggers a CIBA (or equivalent) approval flow to the human before PingFederate issues a token containing the elevated scope. |
| Workload-identity actor tokens | Where the agent's identity is a workload rather than a conventional service, a SPIFFE/SPIRE-issued JWT-SVID can serve as the actor token; the actor token processor must trust the SPIRE OIDC discovery provider's issuer and keys, and the resulting `act.sub` becomes the full SPIFFE ID. |
| Downstream role separation | PingAccess protects the browser-facing human session, PingFederate performs the token exchange and issuance, PingGateway or PingAuthorize validate the issued token and enforce policy at the resource edge — these are complementary roles, not alternatives to each other. |

## Optional PingFederate variants

- Client authentication for the agent can use a client secret or client TLS certificate instead of private-key JWT, but private-key JWT is the documented preference for a non-human, credential-bearing agent identity.
- Elevated-scope step-up is optional; omit CIBA (or an equivalent explicit-approval mechanism) only when every scope the agent can request is already appropriate for unattended, baseline delegation.

Do not generalize this composition to Advanced Identity Cloud or PingAM without separate supporting documentation.
