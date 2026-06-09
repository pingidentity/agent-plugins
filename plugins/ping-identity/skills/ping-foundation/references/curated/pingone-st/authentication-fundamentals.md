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
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/pingoneaic/am-journey-guide/journey-overview.html"
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

---

## Journey troubleshooting patterns

| Symptom | Likely cause | Diagnosis step |
|---|---|---|
| Journey returns error on activation | Node configuration is incomplete or references a deleted script | Open the journey editor; look for nodes with red indicators; check Scripts for the referenced script |
| User reaches `Failure` node unexpectedly | A credential validation node rejected the input (wrong password, locked account, schema mismatch) | Enable debug logging in PingAM (`org.forgerock.openam.auth.nodes` logger) and replay the authentication |
| Journey skipped entirely for authenticated user | Session already exists; journey caching prevents re-execution | Append `ForceAuth=true` to the authorization request to bypass session-level caching |
| Inner journey not executing | Inner journey is deactivated or the Journey node references the wrong name | Verify the inner journey is activated; check the Journey node's `Journey Name` field for exact case-sensitive match |
| `Cannot find node of type X` error | A node type was removed from the product or a module was disabled | Check if the node's plugin is installed and enabled; reinstall or replace the node |
| `Scripted Decision` node always exits on `False` | Script syntax error or unhandled exception | Check the AM server log for `ScriptException` entries; validate the script independently |

---

## Session management

| Setting | Location | Notes |
|---|---|---|
| Session idle timeout | Realm → Sessions → Max Idle Time | After this period of inactivity the session expires; user must re-authenticate |
| Session max time | Realm → Sessions → Max Session Time | Absolute limit regardless of activity; prevents infinite sessions |
| Session quota | Realm → Sessions → Maximum Sessions | Limits concurrent sessions per user; older sessions destroyed when limit reached |
| Session notifications | AM admin console → Sessions → Notifications | Push session invalidation events to registered listeners (e.g., app server logout) |

Session tokens issued by PingAM are bound to the realm. A session created in the `alpha` realm is not valid in the `bravo` realm.

Cross-realm SSO requires explicit federation configuration (e.g., an OAuth2 authorization grant referencing a cross-realm token, or a SAML federation between the two realms). This is an advanced pattern — plan the realm architecture before onboarding users to avoid cross-realm session issues.

## Prerequisites

- PingOne ST tenant with at least one realm configured
- Identity store connected to the realm (see `references/curated/pingone-st/directory-setup.md`)
- Admin access to Authentication → Journeys
- Scripts environment configured if Scripted Decision nodes will be used (AIC admin console → Scripts)

## Common variants

| Variant | Note |
|---|---|
| Inner journeys | Nest frequently-reused logic (e.g., MFA step) into a reusable inner journey invoked by a Journey node |
| Workforce vs. CIAM | Workforce flows are often simpler (username + password + MFA). CIAM flows add registration, progressive profiling, and verification steps — typically built in `ping-orchestration`. |
| ForgeRock AM auth trees | Same underlying model as PingAM trees. Existing ForgeRock trees can be migrated to PingOne ST journeys with node mapping. |
| ACR-based routing | Different client apps can invoke different journeys by passing `acr_values` on the authorization request; map ACR values to journey names in OAuth 2.0 provider settings |

## Related references

- `references/curated/pingone-st/app-setup.md` — assign journeys to OIDC/SAML applications
- `references/curated/pingone-st/foundation-overview.md` — tenant and realm architecture
- `references/curated/pingone-st/am-services.md` — AM services that journey nodes depend on (Push, OATH, WebAuthn, Social, Session, Validation, etc.) — configure these before authoring the corresponding nodes
- `references/curated/pingone-st/directory-setup.md` — identity store configuration required before journey data store decisions

## Source

[Journey overview — PingOne ST](https://docs.pingidentity.com/pingoneaic/am-journey-guide/journey-overview.html)
[Authentication nodes reference](https://docs.pingidentity.com/pingoneaic/am-authentication/authentication-node-reference.html)
[Getting started: authentication journey](https://docs.pingidentity.com/pingoneaic/getting_started/getting_started-authentication_journey.html)
[Session management — PingAM](https://docs.pingidentity.com/pingoneaic/am-sessions-guide/session-management-overview.html)
[Scripted decision node — PingAM](https://docs.pingidentity.com/pingoneaic/am-authentication/auth-node-scripted-decision.html)
[Inner journeys — PingAM](https://docs.pingidentity.com/pingoneaic/am-journey-guide/journey-inner-trees.html)
[ACR values and authentication — PingAM](https://docs.pingidentity.com/pingoneaic/am-oidc-guide/oidc-acr-values.html)
