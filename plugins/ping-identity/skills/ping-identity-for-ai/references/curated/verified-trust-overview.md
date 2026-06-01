---
title: "Verified Trust Overview — Ping Identity"
product_family: cross-platform
products: ["pingone-davinci", "pingone-aic"]
capabilities: ["identity-for-ai", "universal-services"]
services: ["credentials"]
audience: ["developer", "architect"]
use_cases: ["ai-identity"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-01"
slug: "https://docs.pingidentity.com/davinci/verified-trust"
---

# Verified Trust Overview — Ping Identity

Reference for Ping Identity's Verified Trust capabilities: digitally signed trust assertions and verifiable credentials that allow AI agents and applications to carry cryptographically verifiable claims about identity, device posture, and organizational membership.

## Scope

Covers: what Verified Trust is, the trust model (issuer → holder → verifier), trust signal types and carrier formats, Ping product integration points, configuration constraints, and licensing requirements.
Does NOT cover: the general OAuth 2.0 / OIDC agent security pattern (see `references/curated/agent-security-patterns.md`), standard DaVinci flow authoring (see `ping-orchestration`), or end-user identity proofing without a credential output (see `ping-universal-services`).

---

## What Verified Trust is

Verified Trust is a framework for embedding cryptographically verifiable claims into the interactions between AI agents, applications, and protected resources. A trust signal is a signed assertion that a verifier can check without calling back to the issuer — enabling offline or low-latency trust decisions at the edge or inside an AI agent runtime.

Verified Trust addresses a specific gap in standard OAuth 2.0: an access token confirms that an authorization server issued it, but does not carry rich claims about the presenting entity's device health, organizational role, or identity-proofing outcome in a way that is portable and independently verifiable by third parties.

---

## Trust model

```
Issuer (Ping DaVinci / Credentials)
  │
  │  issues signed credential / trust signal
  ▼
Holder (AI agent, user wallet, application)
  │
  │  presents credential / trust signal
  ▼
Verifier (API gateway, resource server, another AI agent)
```

| Actor | Role | Ping surface |
|---|---|---|
| **Issuer** | Creates and signs the credential or trust signal | PingOne Credentials issuer, DaVinci Verified Trust connector |
| **Holder** | Stores and presents the credential | PingOne Credentials wallet, agent runtime, app SDK |
| **Verifier** | Checks the signature and claims | DaVinci Verified Trust verifier connector, API gateway policy, custom middleware |

---

## Trust signal types and carrier formats

| Trust signal type | What it carries | Carrier format | Ping product | Typical use case |
|---|---|---|---|---|
| Identity proofing outcome | Result of document or biometric verification (pass/fail, assurance level) | W3C Verifiable Credential (JWT-VC) | PingOne Verify → PingOne Credentials | AI agent confirms user passed identity proofing before performing privileged action |
| Device posture | Device health score, MDM enrollment status, OS patch level | Signed JSON assertion (DaVinci) | PingOne Protect → DaVinci | Deny agent API request if device posture drops below threshold |
| Organizational claim | Membership in an org, department, or role — externally verifiable | W3C Verifiable Credential (JSON-LD or JWT-VC) | PingOne Credentials | Federated agent-to-agent trust across organizational boundaries |
| Session context | Risk score, MFA completeness, session assurance level at time of issuance | Signed JWT (DPoP-bound or plain) | PingOne DaVinci | Carry session quality into downstream API calls without re-authenticating |
| Custom attribute | Arbitrary business claim (clearance level, regulatory jurisdiction) | W3C Verifiable Credential (JWT-VC) | PingOne Credentials | Regulatory compliance assertions carried by an AI agent into a regulated API |

---

## Integration points in the Ping platform

### DaVinci Verified Trust connector

The DaVinci Verified Trust connector provides both issuance and verification within an orchestration flow.

| Connector mode | What it does | Required configuration |
|---|---|---|
| Issuer | Creates and signs a trust signal for an authenticated subject | Signing key reference, claim mapping, expiry window |
| Verifier | Validates an inbound trust signal and extracts claims | Issuer DID or public key, accepted claim types, revocation check flag |

**Constraint:** The Verified Trust connector requires the DaVinci Advanced license tier. It is not available on the DaVinci Base license.

### Journey node (PingOne AIC)

PingOne AIC provides a Journey node for credential issuance and verification as part of an authentication tree.

| Node type | Purpose |
|---|---|
| Credential Issuer node | Issues a W3C Verifiable Credential after successful Journey completion |
| Credential Verifier node | Validates a presented credential before granting a Journey outcome |

**Constraint:** Journey credential nodes require PingOne Credentials to be configured and linked to the AIC tenant.

### PingOne Credentials

PingOne Credentials manages the full verifiable credential lifecycle:

| Lifecycle stage | API surface | Key constraint |
|---|---|---|
| Credential type definition | Credentials admin API — define schema, claim types, expiry rules | Schema must be defined before issuance; changes require a new credential type version |
| Issuance | Credentials issuance API — issue a credential to a wallet address or QR-code delivery | Wallet must be activated by the holder before credential can be delivered |
| Presentation | Holder presents via OpenID4VP or DIDComm | Verifier must support the same transport |
| Revocation | Credentials revocation API | Revocation check adds ~50–100 ms latency; cache TTL controls revocation freshness |

---

## Configuration field reference

### Verified Trust connector — issuer mode

| Field | Type | Constraint |
|---|---|---|
| Signing key | Key reference | Must reference a key in the DaVinci key store; RS256 or ES256 supported |
| Subject claim mapping | Claim map | Maps DaVinci flow variables to VC subject claims |
| Expiry (seconds) | Integer | Maximum 86 400 (24 hours); shorter is recommended for agent tokens |
| Credential type | String | Must match a registered credential type in PingOne Credentials if VC format is used |
| Revocation | Boolean | Enables revocation list entry on issuance; requires PingOne Credentials |

### Verified Trust connector — verifier mode

| Field | Type | Constraint |
|---|---|---|
| Trusted issuers | List of DID / JWKS URIs | At least one issuer required; wildcard not supported |
| Accepted credential types | String list | Must match the `type` array in the presented credential |
| Revocation check | Boolean | Adds external call to revocation registry; disable only for low-assurance use cases |
| Clock skew tolerance (seconds) | Integer | Default 60; increase for cross-region deployments |

---

## Licensing and availability constraints

| Capability | License requirement |
|---|---|
| DaVinci Verified Trust connector (issuer or verifier) | DaVinci Advanced |
| PingOne Credentials (wallet, issuance, revocation) | PingOne Credentials add-on |
| AIC Journey credential nodes | PingOne AIC + PingOne Credentials add-on |
| PingOne Verify (identity proofing outcome as input) | PingOne Verify add-on |

---

## Prerequisites

- DaVinci environment with the Advanced license activated.
- At least one signing key configured in the DaVinci key store.
- If issuing W3C Verifiable Credentials: PingOne Credentials tenant provisioned and linked.
- If using identity proofing outcomes as trust signal inputs: PingOne Verify configured and a verification policy defined.
- Verifier must have network access to the issuer's JWKS URI or the DID resolver if using DID-based key resolution.

---

## Common variants

| Variant | Notes |
|---|---|
| Agent-to-API (signed assertion) | Agent carries a DaVinci-issued signed JWT; API gateway verifies signature and claims inline — no credential wallet required |
| User-held VC (wallet delivery) | User identity proofing outcome issued as a W3C VC to a PingOne Credentials wallet; AI agent requests presentation before performing privileged action |
| Cross-org trust | Two organizations agree on a shared credential schema; each issues credentials under their own DID; verifiers trust both DIDs |
| Offline / edge verification | Trust signal is verified at the edge without calling back to the issuer; requires short expiry and local key cache |

---

## Related references

- `references/curated/identity-for-ai-overview.md`
- `references/curated/agent-security-patterns.md`
- `references/curated/workforce-helpdesk-ai.md`

## Source

[PingOne DaVinci Verified Trust connector](https://docs.pingidentity.com/davinci/verified-trust)
[PingOne Credentials documentation](https://docs.pingidentity.com/pingone/credentials)
[W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
