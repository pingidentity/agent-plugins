---
title: "Workforce Helpdesk AI — Identity Pattern for AI Assistants Acting on Behalf of Employees"
product_family: cross-platform
products: ["pingone", "pingone-aic"]
capabilities: ["identity-for-ai", "orchestration"]
services: []
audience: ["architect", "developer"]
use_cases: ["workforce"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/pingone/token-exchange"
---

# Workforce Helpdesk AI — Identity Pattern for AI Assistants Acting on Behalf of Employees

Identity pattern for workforce helpdesk AI: an AI assistant that handles employee requests (password reset, access provisioning, policy questions) on behalf of an authenticated user, using a delegated token rather than the user's direct credential.

## Scope

Covers: the delegation model, the verification pattern before high-risk actions, the audit trail requirement, and a sequence table mapping each step to the responsible actor and Ping product.
Does NOT cover: machine-to-machine auth without a human user (see `references/curated/agent-security-patterns.md`), Verified Trust signal issuance (see `references/curated/verified-trust-overview.md`), or standard workforce SSO setup (see `ping-foundation`).

---

## Core principle: the agent must never hold the user's credential

The AI helpdesk agent does not know the user's password, PIN, or session cookie. It receives a delegated access token — issued by Ping after the user authenticates — that carries the user's identity claims and the specific scopes the agent is authorized to exercise on the user's behalf.

This separation enforces:
- **Non-repudiation**: all actions are attributable to the user (who authorized the delegation) and the agent (which performed the action).
- **Revocability**: revoking the delegated token immediately stops the agent; the user's underlying session is unaffected.
- **Minimal privilege**: the delegated token carries only the scopes the agent needs — the user's full access rights are not transferred.

---

## The delegation model

### Step-by-step flow

```
1. User authenticates to Ping (PingOne / AIC Journey)
          │
          ▼
2. Ping issues a user access token (short-lived, user scopes)
          │
          ▼
3. AI helpdesk app requests a delegated token via OAuth 2.0
   Token Exchange (RFC 8693):
   subject_token = user access token
   requested_token_type = access_token
   scope = helpdesk:read helpdesk:provision
          │
          ▼
4. Ping AS issues a delegated token:
   sub = user identity
   act.sub = agent client_id (RFC 8693 actor claim)
   scope = helpdesk:read helpdesk:provision
   exp = short TTL (15–30 minutes recommended)
          │
          ▼
5. Agent calls directory / provisioning APIs with delegated token
          │
          ▼
6. Resource server validates token, extracts user + agent claims,
   logs action with both identities
```

### Delegation token claims

| Claim | Value | Purpose |
|---|---|---|
| `sub` | User's unique identifier (PingOne user ID or employee ID) | Identifies who the action is being performed for |
| `act.sub` | Agent's `client_id` | Identifies which agent performed the action (RFC 8693) |
| `scope` | Exactly the scopes needed by the agent | Enforces minimal privilege |
| `exp` | UTC epoch; short TTL | Limits the window of a compromised token |
| `jti` | UUID | Correlation ID for audit; unique per token issuance |
| `iss` | Ping AS URL | Allows resource server to verify token origin |

---

## Verification pattern before high-risk actions

Not all helpdesk actions carry the same risk. A tiered verification model reduces friction for low-risk requests while enforcing strong assurance before destructive operations.

### Risk tier classification

| Action | Risk tier | Verification required |
|---|---|---|
| Answer a policy question | Low | Delegated token (user already authenticated) |
| View own profile or group membership | Low | Delegated token |
| Reset own non-privileged app password | Medium | MFA step-up (DaVinci or Journey step-up flow) |
| Provision access to a new application | Medium–High | MFA step-up + manager approval (if policy requires) |
| Reset account password (Ping-managed) | High | MFA step-up + re-verification of email or phone |
| Grant privileged / admin access | High | Step-up with FIDO2 / hardware key + additional approval |
| Disable another user's account (admin scenario) | High | Admin re-authentication, not delegation |

**Constraint:** MFA step-up must be triggered by the AI application, not decided by the AI model. The decision tree above must be encoded in application logic or a DaVinci flow, not left to the LLM's judgment.

### Step-up verification using DaVinci or Journey

The AI application redirects (or presents an embedded widget for) the user to a Ping step-up endpoint:
- **DaVinci:** Use a DaVinci flow with the appropriate MFA connector; on success, DaVinci issues a step-up assertion or a new elevated token.
- **AIC Journey:** Use an auth level upgrade Journey (ACR value `urn:pingidentity:assurance:2FA`).

After step-up is confirmed, the AI application requests a new delegated token with the elevated scope. The original delegated token without elevated scope must not be used for high-risk actions.

---

## Sequence summary table

| Step | Actor | Ping product | Output |
|---|---|---|---|
| 1. User authentication | End user (employee) | PingOne MT / PingOne AIC | User session; user access token |
| 2. Helpdesk app token request | AI helpdesk application (front-end) | PingOne AS / AIC OAuth AS | Delegated access token (RFC 8693 token exchange) |
| 3. Low-risk request execution | AI agent (back-end) | Directory API / provisioning API | Action result; audit log entry |
| 4. Risk-tier evaluation | AI application logic | (No Ping product — in-app decision) | Tier classification; step-up decision |
| 5. Step-up MFA (medium/high actions) | End user | PingOne DaVinci / AIC Journey | Step-up confirmation; elevated token |
| 6. High-risk action execution | AI agent (back-end) | Directory API / provisioning API | Action result; audit log entry with step-up evidence |
| 7. Token expiry / session end | Ping AS | PingOne AS / AIC OAuth AS | Token revocation at TTL or explicit logout |

---

## Audit trail requirements

Every action taken by the AI agent on behalf of a user must produce an audit record with the following fields.

| Audit field | Source | Constraint |
|---|---|---|
| `user_id` | `sub` claim in delegated token | Must be the user's stable identifier, not a session ID |
| `agent_id` | `act.sub` claim (RFC 8693) or `client_id` | Must uniquely identify the agent component that performed the action |
| `action` | API endpoint + HTTP method + resource identifier | Resource server logs this at the time of the call |
| `authorization_evidence` | Token `jti` + step-up assertion `jti` (if applicable) | Enables reconstruction of the full authorization chain in audit |
| `timestamp` | UTC ISO 8601 from resource server clock | Must not use the token `iat`; use the time of the API call |
| `outcome` | Success / failure / partial | Required for incident investigation |
| `request_id` | `X-Request-ID` header sent by agent | Correlates multi-step operations (e.g., provision + notify) |

**Key constraint:** The AI agent must not strip or modify authorization headers before forwarding calls to downstream APIs. The delegated token must reach the resource server intact so that the resource server can log both user and agent identities.

---

## Constraints and guardrails

| Constraint | Rationale |
|---|---|
| Agent must never store user credentials (password, PIN, session token) | Prevents credential theft via agent compromise |
| Delegated token TTL must be ≤ the user session TTL | Token must not outlive the session that authorized it |
| Delegated token scope must be a strict subset of the user's scopes | Agent cannot be granted more than the user has |
| Step-up decision must be in application code, not the LLM | LLMs may be manipulated via prompt injection; security decisions must be deterministic |
| Delegated token must not be passed to sub-agents without explicit re-authorization | Lateral movement risk; each agent component must have its own token |
| Audit records must be immutable and stored outside the AI system | Prevents tampering by a compromised agent |

---

## Prerequisites

- PingOne environment or AIC tenant with OAuth 2.0 token exchange (RFC 8693) enabled on the Authorization Server.
- AI helpdesk application registered as a confidential client with `urn:ietf:params:oauth:grant-type:token-exchange` grant type.
- User-facing authentication configured (Journey or PingOne sign-on policy) with the required MFA methods for step-up.
- Directory and provisioning APIs configured to accept and validate delegated tokens.
- Audit log sink configured to receive structured log events from resource servers.

---

## Common variants

| Variant | Notes |
|---|---|
| Password reset only | Simplest variant; agent only calls the directory reset API; medium-risk tier requires MFA step-up |
| Full access provisioning | Adds approval workflow; token exchange includes `policy:provisioning` scope; approval step may require a DaVinci connector to an ITSM system |
| Multi-LLM pipeline (orchestrator + sub-agents) | Each sub-agent receives its own narrowly scoped delegated token; orchestrator must not forward its token to sub-agents |
| External identity provider (federated workforce) | User authenticates via enterprise IdP (SAML/OIDC federation to PingOne); PingOne issues a local token after federation; token exchange proceeds as normal |
| AIC-native deployment | Token exchange uses AIC's built-in OAuth AS; step-up uses AIC Journey with ACR-based auth level upgrade |

---

## Related references

- `references/curated/identity-for-ai-overview.md`
- `references/curated/agent-security-patterns.md`
- `references/curated/verified-trust-overview.md`

## Source

[RFC 8693 — OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
[PingOne Token Exchange documentation](https://docs.pingidentity.com/pingone/token-exchange)
[PingOne AIC OAuth 2.0 guide](https://docs.pingidentity.com/aic/oauth2)
[PingOne DaVinci step-up MFA](https://docs.pingidentity.com/davinci/step-up-mfa)
