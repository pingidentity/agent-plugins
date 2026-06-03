---
title: "PingFederate — Administration Basics"
product_family: ping-software
products: ["pingfederate"]
capabilities: ["foundation"]
audience: ["admin", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf-admin-guide.html"
---

# PingFederate — Administration Basics

Core configuration concepts for PingFederate: server architecture, SP/IdP connections, adapter chains, and initial setup.

## Scope

**Covers:** PingFederate deployment architecture, SP connections, IdP connections, authentication adapter chains, OAuth/OIDC client setup, initial admin setup.
**Does NOT cover:** PingAccess (resource gateway), PingDirectory (directory services), or PingID MFA configuration — each has its own generated reference under `references/generated/ping-software/`.

---

## Server architecture

PingFederate is a standalone federation server deployed as a Java application.

| Component | Role |
|---|---|
| Engine node | Handles runtime federation traffic (SSO, token, OAuth) |
| Console node | Hosts the admin UI and API |
| Cluster | Multiple engine nodes behind a load balancer for HA |

**Admin API base URL:** `https://<host>:9999/pf-admin-api/v1/`
**Admin console URL:** `https://<host>:9999/pingfederate/app`

---

## SP connection (PingFederate as IdP)

An SP connection defines a SAML 2.0 or WS-Federation trust between PingFederate (acting as IdP) and a service provider (e.g., Salesforce, Workday).

**Required fields:**

| Field | Notes |
|---|---|
| Partner entity ID | Unique identifier for the SP; from SP metadata XML |
| ACS URL | Assertion Consumer Service — where PingFederate POSTs the SAML response |
| Name ID format | `email`, `persistent`, or `transient`; dictated by SP requirements |
| Attribute contract | User attributes to include in the SAML assertion (e.g., `mail`, `givenName`) |
| Authentication source | Which adapter or IdP adapter chain handles authentication for this SP |
| Signing | Sign assertions, responses, or both; export signing cert to SP admin |

**Fastest path:** Import SP metadata XML to auto-populate entity ID, ACS URL, and certificates.

---

## IdP connection (PingFederate as SP)

An IdP connection defines a SAML 2.0 trust with an upstream identity provider (e.g., Azure AD, Okta, another PingFederate).

**Required fields:**

| Field | Notes |
|---|---|
| Partner entity ID | Unique identifier for the upstream IdP |
| SSO service URL | IdP's SAML SSO endpoint |
| Signature verification cert | IdP's signing certificate; import from IdP metadata |
| Attribute mapping | Map incoming SAML attributes to PingFederate's attribute contract |

---

## Authentication adapter chain

PingFederate uses adapters to collect and validate credentials. Adapters chain together to implement multi-factor and step-up flows.

**Common adapters:**

| Adapter | Purpose |
|---|---|
| HTML Form Adapter | Username/password collection and validation against a data store |
| Kerberos Adapter | Transparent Windows SSO via Kerberos/SPNEGO |
| RADIUS Adapter | Integration with RADIUS-based MFA (RSA, Cisco ISE) |
| Composite Adapter | Chain multiple adapters; first-factor + second-factor composition |
| PingOne MFA Adapter | Step-up MFA via PingOne MFA service |

**Authentication policy:** Authentication policies (PingFederate 10+) replace adapter-per-SP configuration with a centralized policy graph. Define the policy once; reference it from multiple SP connections.

---

## OAuth 2.0 / OIDC client setup

**Admin surface:** Applications → OAuth → Clients → + Add Client

**Required fields:**

| Field | Notes |
|---|---|
| Client ID | Unique identifier; auto-generated or custom |
| Client Secret | Required for confidential clients; omit for public clients |
| Redirect URIs | Exact match required |
| Grant types | Authorization Code, Client Credentials, Refresh Token |
| Scopes | Define allowed scopes; map to attribute contracts for claims |

**OIDC discovery:** `https://<host>:9031/.well-known/openid-configuration`

---

## PingDirectory integration

PingFederate typically uses PingDirectory (or Active Directory) as the identity store.

**Data store configuration:** System → Data Stores → + Add Data Store → LDAP

Required fields: LDAP URL (`ldaps://`), Bind DN, Bind password, Base DN, Username attribute.

---

## Prerequisites

- PingFederate license file installed
- Java 11 or 17 JRE (version requirements vary by PingFederate release)
- Server profile (Git-backed) recommended for config-as-code deployments
- Network access to identity stores (LDAP/AD) and any integrated MFA services

## Common variants

| Variant | Note |
|---|---|
| Clustered deployment | Engine nodes behind a load balancer; console node separate; requires shared operational data store (PostgreSQL or Oracle) |
| PingFederate + PingDirectory | Most common workforce SSO pattern; PingDirectory serves as the identity store with LDAP |
| Server profile (config-as-code) | Recommended for production; all config stored in Git and applied at container startup |
| PingFederate as OAuth AS | Used when PingFederate issues tokens to downstream APIs; requires Access Token Manager configuration |

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| SP connection using wrong ACS URL | SAML response POSTed to wrong endpoint; SP returns error | Import SP metadata to auto-populate ACS URL; verify against SP documentation |
| Admin console port exposed | PF admin API accessible from internet | Restrict port 9999 to management CIDR; use HTTPS only |
| LDAP pool exhaustion | Authentication latency spikes under load | Increase LDAP data store connection pool size in System → Data Stores |
| Clock skew exceeds SAML tolerance | SAML assertion rejected as expired or not yet valid | Verify NTP sync on PingFederate server and all SP/IdP hosts; default tolerance is 5 minutes |

## Related references

- `references/curated/cross-platform/foundation-overview.md`
- `references/curated/cross-platform/core-admin-patterns.md`

## Source

[PingFederate Administration Guide](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf-admin-guide.html)
[PingFederate Admin API reference](https://docs.pingidentity.com/pingfederate/latest/admin-api-reference/pf-admin-api-reference.html)
[SP connection configuration](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf-creating-sp-connection.html)
[Authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf-authn-policies.html)
