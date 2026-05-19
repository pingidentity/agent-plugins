---
title: "PingOne ST — Authentication Fundamentals"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["foundation"]
services: []
audience: ["admin", "developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-19"
slug: "https://docs.pingidentity.com/pingoneaic/latest/am-journey-guide/journey-overview.html"
---

# PingOne ST — Authentication Fundamentals

Understand and configure authentication in PingOne ST: the journey model, realm authentication settings, and key design rules before building any login flow.

## Scope

**Covers:** Journey/tree concepts, realm authentication settings, node basics, journey design rules.
**Does NOT cover:** Specific node-by-node flow design — that belongs in `ping-orchestration`. Application-to-journey assignment — see `references/curated/pingone-st/app-setup.md`.

## Key steps / content

### The journey model

Authentication in PingOne ST is driven by **journeys** (also called authentication trees in PingAM). A journey is a configurable directed graph of **nodes** connected by outcome branches.

- Journeys replace static login pages with flexible, branching flows
- Nodes perform a single function: collect a credential, evaluate a condition, invoke a service, set a session variable
- Branches connect nodes to the next step based on the outcome (e.g., `True` / `False`, `Match` / `No Match`, `Success` / `Failure`)
- Journeys can be nested: an inner journey node invokes another journey and passes its result upstream

**End states:** Every journey must reach one of two terminal nodes:
- `Success` — authentication approved, session created
- `Failure` — authentication denied

### Realm authentication settings

**Admin surface:** AIC admin console → Authentication → Journeys (or AM admin console → Realm → Authentication → Settings)

| Setting | Purpose |
|---|---|
| Default authentication journey | Used when no specific journey is requested (e.g., `/login` with no `authIndexType` parameter) |
| Default failure URL | Where users land after a `Failure` outcome when the client does not specify |
| Default success URL | Where users land after a `Success` outcome when the client does not specify |
| Session settings | Idle timeout, max session time, session quota (max concurrent sessions per user) |

**Per-application override:** A specific journey can be assigned to an individual application. Set at Application settings → Authentication → Journey. Different apps can present different login flows without modifying the realm default.

### Node categories and common nodes

| Category | Examples |
|---|---|
| **Input / collection** | Username Collector, Password Collector, Choice Collector, Attribute Collector |
| **Credential validation** | Data Store Decision (validates username + password against identity store) |
| **MFA / step-up** | WebAuthn Registration/Authentication, OTP Email/SMS, Push Authentication |
| **Conditional logic** | Scripted Decision, Attribute Present Decision, Session Data Decision |
| **Session / profile** | Set Session Properties, Set Persistent Cookie, Profile Completeness Decision |
| **External integrations** | Social Provider Handler, LDAP Decision, HTTP Client, Platform Password |

**Scripted Decision node:** Executes a custom JavaScript or Groovy script to implement logic not covered by built-in nodes. The script returns a named outcome that maps to a branch. Requires a Decision Node script defined in Scripts.

**Transient state:** Nodes can store intermediate values in transient state (in-memory, session-duration) or shared state (survives across inner journeys). Use transient state to pass the username collected in one node to a validation node further down the journey.

### Key design rules

These are constraints that prevent broken or unexpected behavior:

| Rule | Why it matters |
|---|---|
| Do not set a journey as both **default** AND **always run** | "Always run" forces re-execution of the journey on every request, including mid-session. Combined with "default," this can create redirect loops. |
| Do not map a journey to the default ACR value if it is set to "always run" | Same loop risk via ACR-based routing. |
| If a user re-authenticates with the same journey during an active session, journey processing is skipped by default | This is intentional session-level caching. Override with `ForceAuth=true` if re-authentication is required. |
| Duplicate journeys via the editor (More → Duplicate) before modifying production journeys | Preserves a working copy. Journeys cannot be version-controlled natively in the console. |

### Journey activation

Journeys must be **activated** to be available for authentication. A deactivated journey still exists in the editor but returns an error if invoked.

**Admin surface:** Journey editor → More (⋮) → Activate / Deactivate

### How clients invoke a journey

| Method | When to use |
|---|---|
| Application override | Preferred; set once in app config, no per-request parameters needed |
| OIDC `acr_values` | Append `&acr_values=<journey-name>` to the authorization request |
| Direct AM endpoint | `/login?authIndexType=service&authIndexValue=<journey-name>` — use for testing or legacy integrations |

## Prerequisites

- PingOne ST tenant with at least one realm configured
- Identity store connected to the realm (see `references/curated/pingone-st/directory-setup.md`)
- Admin access to Authentication → Journeys

## Common variants

| Variant | Note |
|---|---|
| Inner journeys | Nest frequently-reused logic (e.g., MFA step) into a reusable inner journey invoked by a Journey node |
| Workforce vs. CIAM | Workforce flows are often simpler (username + password + MFA). CIAM flows add registration, progressive profiling, and verification steps — typically built in `ping-orchestration`. |
| ForgeRock AM auth trees | Same underlying model as PingAM trees. Existing ForgeRock trees can be migrated to PingOne ST journeys with node mapping. |

## Related references

- `references/curated/pingone-st/app-setup.md`
- `references/curated/pingone-st/foundation-overview.md`
- `references/curated/pingone-st/directory-setup.md`

## Source

[Journey overview — PingOne ST](https://docs.pingidentity.com/pingoneaic/latest/am-journey-guide/journey-overview.html)
[Authentication nodes reference](https://docs.pingidentity.com/pingoneaic/latest/am-authentication/authentication-node-reference.html)
[Getting started: authentication journey](https://docs.pingidentity.com/pingoneaic/latest/getting_started/getting_started-authentication_journey.html)
