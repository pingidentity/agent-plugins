---
title: "PingOne ST — Basic Authentication Nodes"
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

# PingOne ST — Basic Authentication Nodes

Core nodes for credential collection, user lookup, and validation against identity stores.

## Scope

**Covers:** Username/password collection, credential validation, session-based user identification, attribute branching, and terminal outcomes.
**Does NOT cover:** MFA — see `nodes/mfa-nodes.md`. Flow control — see `nodes/utility-nodes.md`.

---

## Credential Collection

### Platform Username node (`ValidatedUsernameNode`)
Collects the username from the user. Writes to `username` in shared state. **Use this in AIC — do not use the deprecated Username Collector node.**

**Configuration:**

| Field | Notes |
|---|---|
| `validateInput` | `true` enforces IDM username policy (format, length) on submission |
| `usernameAttribute` | The IDM attribute storing the username (default: `userName`) |
| `autocompleteValues` | If set, provides HTML5 autocomplete suggestions for the input field |

- Outcomes: single (proceeds to next node)
- Must be a PageNode child — standalone placement renders no input field

### Platform Username node V2 (`ValidatedUsernameNodeV2`)
V2 adds prepopulation support. Use V2 when the journey may have the username already in state (e.g., re-authentication after session expiry, step-up flows).

**Additional field vs V1:**

| Field | Notes |
|---|---|
| `prepopulate` | `true` — input field is prepopulated with the `username` value from node state if present |

- All other configuration identical to V1
- Outcomes: single

### Platform Password node (`ValidatedPasswordNode`)
Collects the password from the user. Writes to `password` in transient state. **Use this in AIC — do not use the deprecated Password Collector node.**

**Configuration:**

| Field | Notes |
|---|---|
| `validateInput` | `true` enforces IDM password policy on submission; `false` skips policy check (for existing credential verification) |
| `passwordAttribute` | The IDM attribute storing the password (default: `password`) |

- Outcomes: single
- Must be a PageNode child

**Two-instance pattern (password update journeys):**
- Instance 1 — "Verify Existing Password": `validateInput: false` (existing credential, no policy enforcement)
- Instance 2 — "New Password": `validateInput: true` (new credential, policy enforced)

### Zero Page Login Collector node
Captures username and password in a single step without presenting an intermediate page. Useful when the client has already collected credentials.

- Outcomes: single

> **AIC note:** `Username Collector` and `Password Collector` nodes are not compatible with Advanced Identity Cloud. Always use `Platform Username` (`ValidatedUsernameNode`) and `Platform Password` (`ValidatedPasswordNode`) instead.

---

## Credential Validation

### Data Store Decision node
Validates username + password against the realm's configured data store.

- Outcomes: **True** (credentials match) / **False** (credentials do not match)
- No configurable properties — operates on the realm's default data store
- Pair with `RetryLimitDecisionNode` to allow multiple attempts before lockout
- Used in authenticated password-update journeys to verify the current password before allowing a change

**Contrast with IdentityStoreDecisionNode:** DataStoreDecisionNode returns only True/False. Use `IdentityStoreDecisionNode` when you need to handle LOCKED, EXPIRED, or CANCELLED states explicitly.

### Identity Store Decision node
Authenticates against the cloud identity store with granular lifecycle outcomes.

- Outcomes: **TRUE** / **FALSE** / **LOCKED** / **EXPIRED** / **CANCELLED**
- Wire each outcome explicitly:
  - `LOCKED` → account-locked message or recovery path
  - `EXPIRED` → password-change inner journey
  - `CANCELLED` → FailureNode
- Used in financial-grade and CIAM journeys where account lifecycle states must be handled distinctly

### LDAP Decision node
Authenticates against an external LDAP or Active Directory server. Supports password policy outcomes not available in Data Store Decision.

- Outcomes: **True** / **False** / password policy outcomes (e.g., `EXPIRED`, `LOCKED`)
- Use when the realm is connected to an external LDAP/AD and password-policy-aware branching is needed

### AD Decision node
Authenticates specifically against Active Directory.

- Outcomes: **True** / **False**

### Passthrough Authentication node
Authenticates a user against a third-party system via an ICF connector without requiring the user to re-enter credentials. The credentials are already in journey state.

**Configuration:**

| Field | Notes |
|---|---|
| `systemEndpoint` | Name of the ICF connector to use (configured in IDM) |
| `objectType` | ICF object type for the authenticating user |
| `identityAttribute` | The IDM attribute used as the username for authentication |
| `passwordAttribute` | The IDM attribute used as the password for authentication |

- Outcomes: **Authenticated** / **Failed** / **Missing Input**
- `Missing Input`: username or password not present in journey state — route back to credential collection
- Use during directory migration to validate credentials against a legacy system while the primary directory is being replaced

---

## Session-Based User Identification

### Get Session Data node (`SessionDataNode`)
Extracts a value from the current active session into shared state, enabling authenticated journeys to identify the user without a login form.

**Production configuration:**
- `sessionDataKey: UserToken` — the session property containing the user token
- `sharedStateKey: userName` — the shared state key to write the username to

- Outcomes: single
- **Canonical entry pattern for authenticated journeys** (password update, profile management): place as the first node; the extracted `userName` is then available for `DataStoreDecisionNode`, `PatchObjectNode`, and `IdentifyExistingUserNode` downstream

---

## Attribute-Based Branching

### Attribute Present Decision node
Checks whether a specific attribute exists in the user's profile or shared state.

- Outcomes: **True** (attribute present) / **False** (attribute absent)
- `presentAttribute: password` — detects whether a user has a password set; returns `False` for passwordless users, enabling conditional routing to email-gated verification instead of current-password challenge

### Attribute Value Decision node
Evaluates whether a specific attribute in the user's profile matches a configured comparison operation.

**Configuration:**

| Field | Notes |
|---|---|
| `comparisonOperation` | `PRESENT` — checks attribute exists; `EQUALS` — checks attribute value equals `comparisonValue` |
| `comparisonAttribute` | The object attribute to evaluate (e.g., `emailVerified`) |
| `comparisonValue` | Value to compare against when using `EQUALS` (e.g., `true`) |
| `identityAttribute` | The IDM attribute used to look up the user object |

- Outcomes: **True** / **False**
- `PRESENT` does not require `comparisonValue` — it is a null/existence check only
- Common use: "Is Email Verified?" gate — `comparisonAttribute: emailVerified`, `comparisonOperation: EQUALS`, `comparisonValue: true`; `False` triggers email verification inner journey

---

## Terminal Nodes

### Success node
Ends the journey successfully. Creates an authenticated session. Every journey must have at least one Success node.

### Failure node
Ends the journey with an authentication failure. No session created. Use at the end of any path that should deny access.

---

## Common patterns

| Pattern | Nodes |
|---|---|
| Basic login | PageNode(ValidatedUsername + ValidatedPassword) → DataStoreDecisionNode → Success / Failure |
| Login with retry | DataStoreDecisionNode(False) → RetryLimitDecisionNode → retry loop or Failure |
| Full lifecycle login | PageNode(ValidatedUsername + ValidatedPassword) → IdentityStoreDecisionNode(TRUE/LOCKED/EXPIRED/CANCELLED/FALSE) |
| Authenticated journey entry | SessionDataNode → AttributePresentDecisionNode |
| Passwordless user branch | AttributePresentDecisionNode(`password` = False) → EmailSuspendNode / (True) → DataStoreDecisionNode |
| Email verification gate | AttributeValueDecisionNode(False) → email verification inner journey → (true) proceed |

## Related references

- `nodes/mfa-nodes.md`
- `nodes/utility-nodes.md`
- `nodes/risk-management-nodes.md`
- `journey-use-cases/password-reset-and-update.md`

## Source

[Basic authentication nodes](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[Data Store Decision node](https://docs.pingidentity.com/auth-node-ref/latest/data-store-decision.html)
[Platform Username node](https://docs.pingidentity.com/auth-node-ref/latest/platform-username.html)
