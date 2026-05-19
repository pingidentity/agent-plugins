---
title: "PingOne ST — Federation and Contextual Nodes"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-05-21"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Federation and Contextual Nodes

Nodes for federated identity (social login, SAML, OIDC), external OTP delivery (Twilio), device context, cookies, certificates, and behavioral signals.

## Scope

**Covers:** Social Provider Handler V2, SAML2, OIDC validator, Twilio Verify nodes, device profiling/geofencing, cookie decisions, certificate auth, and login count behavioral nodes.
**Does NOT cover:** App registration or IdP configuration — see `ping-foundation` → `app-setup.md`.

---

## Social / Federation Nodes

### Social Provider Handler node (V2)
Initiates authentication via a configured social identity provider or any OIDC-compliant external IdP.

**Configuration:**
- Select from IdPs registered in the realm's Social Identity Provider service
- `transformScript`: optional script to map incoming claims to managed object attributes

- Outcomes: **ACCOUNT_EXISTS** / **NO_ACCOUNT** / **SOCIAL_AUTH_INTERRUPTED**
- `ACCOUNT_EXISTS` → continue to authentication or profiling flow
- `NO_ACCOUNT` → profile collection PageNode → `CreateObjectNode` for social registration
- `SOCIAL_AUTH_INTERRUPTED` → FailureNode

**Entry pattern (social + local choice):**
```
PageNode (outcomes: localAuthentication / socialAuthentication)
  → localAuthentication: Platform Username → Platform Password → DataStoreDecisionNode
  → socialAuthentication: SocialProviderHandlerNodeV2
```

See `journey-use-cases/social-and-local-registration-authentication.md` for full pattern.

### OIDC ID Token Validator node
Validates a JWT ID token from an external OpenID Connect provider. Extracts claims into shared state.

- Outcomes: **Valid** / **Invalid**
- Use when the client presents a pre-obtained ID token (e.g., native app silent authentication)

### SAML2 Authentication node
Initiates or processes a SAML 2.0 authentication exchange with an external IdP.

- Outcomes: **Success** / **Failure** / **Account not found**

### Write Federation Information node
Persists federation-related data (e.g., external IdP subject, linked account) to the user's managed object.

- Outcomes: single
- Place after Social Provider Handler or SAML2 node on the account-linking path

### Select Identity Provider node
Presents the user with a list of identity providers to choose from (for multi-IdP login pages).

- Outcomes: one per configured IdP

---

## Twilio Verify Nodes

Used for SMS and voice OTP delivery in MFA registration and authentication flows.

### Twilio Verify Identifier node (`VerifyAuthIdentifierNode`)
Validates that a phone number attribute is available before sending via Twilio.

**Configuration:**

| Field | Observed values | Notes |
|---|---|---|
| `identifierAttribute` | `telephonenumber` / `telephoneNumber` | Case varies — check your schema attribute name |
| `identifierSharedState` | `userIdentifier` | Shared state key for the resolved phone number |

- Outcomes: **True** / **False** / **Error**
- `False`: phone number missing — route to FailureNode or prompt user to add a phone number
- Place before `VerifyAuthSenderNode` — do not attempt to send if identifier lookup fails

### Twilio Verify Sender node (`VerifyAuthSenderNode`)
Sends an OTP to the user's phone via SMS or voice call.

**Configuration:**

| Field | Observed values |
|---|---|
| `channel` | `SMS` or `CALL` |
| `accountSID` | Twilio account SID |
| `authToken` | Twilio auth token |
| `serviceSID` | Twilio Verify service SID |
| `requestIdentifier` | `false` |

- Outcomes: **true** / **error**

### Twilio Verify Lookup node (`VerifyAuthLookupNode`)
Validates the phone number format and carrier information before MFA device registration.

- Outcomes: **True** / **False** / **Error**
- Use before `VerifyAuthSenderNode` in device registration flows (CIAM Passwordless MFA Device Registration)

### Twilio Verify Collector Decision node (`VerifyAuthCollectorDecisionNode`)
Collects and verifies the OTP code the user received via Twilio.

**Configuration:**

| Field | Observed value |
|---|---|
| `hideCode` | `true` |
| `showResendButton` | `false` |
| `showCancelButton` | `false` |
| `identifierSharedState` | `userIdentifier` |

- Outcomes: **true** / **false** / **error**

**Full Twilio SMS/VOICE path:**
```
VerifyAuthIdentifierNode(True)
  → VerifyAuthSenderNode(true)
  → PageNode(VerifyAuthCollectorDecisionNode)
    → true → proceed
    → false → RetryLimitDecisionNode → retry loop / Failure
    → error → FailureNode
```

---

## Contextual Nodes

### Device Profile Collector node
Collects device characteristics (browser, OS, IP, screen dimensions, fonts) silently from the client.

- Outcomes: single — no visible UI interaction

### Device Match node
Compares the current device profile against previously stored profiles for this user.

- Outcomes: **True** (known device) / **False** (unknown device)

### Device Geofencing node
Evaluates whether the user's device is within configured geographic boundaries.

- Outcomes: **True** (inside fence) / **False** (outside fence)

### Device Location Match node
Checks whether the current device location matches the user's last known location within a configured radius.

- Outcomes: **True** / **False**

### Device Tampering Verification node
Checks Ping SDK signals for device compromise (rooted/jailbroken).

- Outcomes: **True** (device appears legitimate) / **False** (tampering detected)

### Device Profile Save node
Saves the current device profile to the user's stored device list after successful authentication.

- Outcomes: single

---

## Cookie Nodes

### Cookie Presence Decision node
Checks whether a specific cookie is present in the incoming request.

- Outcomes: **True** (cookie present) / **False** (cookie absent)

### Persistent Cookie Decision node
Validates a Ping Identity persistent authentication cookie.

- Outcomes: **True** (valid cookie — user can skip re-authentication) / **False** (no valid cookie)

### Set Persistent Cookie node
Issues a persistent authentication cookie to the client after successful authentication.

- Outcomes: single

### Set Custom Cookie node
Sets an arbitrary cookie on the client response.

- Outcomes: single

---

## Certificate Nodes

### Certificate Collector node
Prompts the client to present a TLS client certificate. Stores it in transient state.

- Outcomes: single

### Certificate Validation node
Validates the collected certificate against configured trust anchors and CRL/OCSP.

- Outcomes: **True** (certificate valid) / **False** (certificate invalid or untrusted)

### Certificate User Extractor node
Extracts a username from the client certificate's Subject or SAN field and writes to shared state.

- Outcomes: single

---

## Behavioral Nodes

### Login Count Decision node
Routes based on cumulative login count stored in the user's profile.

- `interval: AT` (exactly N) or `AFTER` (N or more); `amount: N`
- Outcomes: **True** / **False**
- Primary use: trigger one-time progressive profiling or onboarding at a specific login number

### Increment Login Count node
Increments the user's stored login count by 1. Single `outcome`.

- Place post-registration and post-authentication to keep the count accurate
- Required at registration (`CreateObjectNode(CREATED)` → `IncrementLoginCountNode`) to initialize the count so `LoginCountDecisionNode` triggers on the correct subsequent login

---

## Common patterns

| Pattern | Nodes |
|---|---|
| Social login with registration fallback | Social Provider Handler V2(NO_ACCOUNT) → Attribute Collector → Create Object |
| Social + local choice at journey entry | PageNode(localAuthentication/socialAuthentication) → respective paths |
| Twilio SMS MFA | VerifyAuthIdentifier → VerifyAuthSender → PageNode(VerifyAuthCollector) → retry loop |
| Device trust check | Device Profile Collector → Device Match(False) → MFA step-up |
| Persistent cookie SSO | Persistent Cookie Decision(True) → Success / (False) → login journey |
| First-login onboarding | Login Count Decision(AT=1, True) → onboarding inner journey → Increment Login Count |
| Certificate-based auth | Certificate Collector → Certificate Validation → Certificate User Extractor → Success |

## Related references

- `nodes/basic-auth-nodes.md`
- `nodes/identity-management-nodes.md`
- `nodes/mfa-nodes.md`
- `journey-use-cases/social-and-local-registration-authentication.md`
- `journey-use-cases/mfa-authentication-multi-method.md`

## Source

[Federation nodes](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[Social Provider Handler node](https://docs.pingidentity.com/auth-node-ref/latest/social-provider-handler.html)
[Device Profile Collector node](https://docs.pingidentity.com/auth-node-ref/latest/device-profile-collector.html)
