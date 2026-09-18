# Identity for AI - PingOne variant: AI Agent registration and resource-mapped token exchange

## Composition

The documented PingOne composition uses:

- A PingOne **AI Agent** object as the agent's own registered identity, separate from any human user, with its own client credentials and enabled grant types.
- Two PingOne custom resources: one representing the agent's own token audience and scope, one representing the protected MCP server or REST API the agent ultimately calls.
- A resource attribute mapping that produces the `may_act` claim on the agent's own token and the `act` claim on the exchanged, resource-scoped token.
- A PingOne consent agreement and authentication policy assigned to the agent so the human's token carries evidence of an explicit delegation consent.
- **PingGateway** as the runtime enforcement point, introspecting the exchanged token against the protected resource's credentials before proxying to the MCP server or API.

The exchange itself is the standard OAuth 2.0 token-exchange grant: the agent submits its own actor token together with the human's subject token, naming the protected resource as the target audience and scope.

## Critical configuration concepts

| Concern | Required concept |
|---|---|
| Agent identity | The AI agent is registered as its own object with its own client ID and secret, enabled for client-credentials, refresh-token, and token-exchange grants. It is never given the human's credentials. |
| Agent's own resource and scope | A custom resource represents the agent's own audience. Its `sub` mapping resolves to the human's username only in user-authorized flows; a calculated `may_act` attribute is populated with the agent's own client ID for those flows and left empty for pure client-credentials (autonomous) tokens. |
| Protected resource and scope | A second custom resource represents the MCP server or API the agent ultimately calls, with its own audience and scope. Its `sub` mapping copies the subject from the incoming subject token; its `act` mapping copies `may_act` from the subject token only when the actor token's client ID matches `may_act.sub`. |
| Consent and authentication policy | A consent agreement (with a defined reapproval interval) and an authentication policy that requires both login and agreement acceptance are assigned to the agent, so the resulting subject token carries evidence of consented delegation. |
| Delegation exchange | The agent presents its actor token and the human's subject token to PingOne's token-exchange endpoint, requesting the protected resource's audience and scope. PingOne evaluates the resource's `sub`/`act` mappings and returns the exchanged token only when the actor-to-`may_act` relationship holds. |
| Gateway enforcement | PingGateway introspects the exchanged token using the protected resource's own client credentials, checks the required scope and expected resource audience, and only then proxies the request to the MCP server or backend API. |

## Optional PingOne variants

- Autonomous, non-delegated agent actions (pure client-credentials tokens) must not carry a `may_act` claim; the resource mapping should leave `act` unset for those tokens so they are never mistaken for delegated, human-attributed access.
- A revoked or disabled agent, or a `may_act`/client-ID mismatch, must cause the resource mapping to omit `act` — treat a token with an absent `act` claim as not delegated, not as a degraded delegation.

Do not generalize this composition to Advanced Identity Cloud or PingAM without separate supporting documentation.
