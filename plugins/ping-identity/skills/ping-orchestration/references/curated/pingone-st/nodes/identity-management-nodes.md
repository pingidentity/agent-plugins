---
title: "PingOne ST — Identity Management Nodes"
product_family: pingone-st
products: ["pingone-aic", "pingam", "pingidm"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-02"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# PingOne ST — Identity Management Nodes

Nodes for reading, writing, and managing user identity data during authentication journeys — registration, profile collection, consent, KBA, object operations, and social federation.

## Scope

**Covers:** Attribute collection and validation, user object creation/update/lookup, consent, KBA, profile completeness, social login, and PingOne Verify integration.
**Does NOT cover:** Directory setup or managed object schema — see `ping-foundation` → `directory-setup.md`. Deep provisioning and reconciliation patterns — outside the scope of this reference.

---

## User Lookup

### Identify Existing User node
Looks up an existing user in the identity store by a specified attribute and writes the found user's identifier to shared state.

**Configuration:**

| Field | Purpose |
|---|---|
| `identityAttribute` | The attribute used to look up the user in the identity store (e.g., `mail`) |
| `identifier` | The shared state key populated with the found user's identifier (e.g., `userName`) |

- Outcomes: **True** (user found) / **False** (user not found)

**Anti-enumeration wiring:** In recovery and reset journeys, wire both `True` and `False` outcomes to the same successor node (typically `EmailSuspendNode`). The user sees an identical message regardless of whether an account exists. Never route `True` and `False` to different user-facing messages — that leaks account existence.

**Multiple uses per journey:** Used both as an entry lookup (recovery journeys look up by `mail`) and as an in-journey user context loader (MFA inner journeys load user context before PingOne Protect evaluation).

### Display Username node
Displays the authenticated or recovered user's username on the current page.

- Configuration: `userName: userName`, `identityAttribute: mail`
- Outcomes: single — no branching
- Used in OOTB Account Recovery to show the recovered username in the browser after email verification, before routing to the Login inner journey
- Contrast with the Forgotten Username journey, which sends the username in the email body instead of displaying it in-browser

---

## Attribute Collection

### Attribute Collector node
Prompts the user to provide values for specified identity schema attributes.

**Configuration:**

| Field | Notes |
|---|---|
| `attributesToCollect` | List of schema attribute names; must be present and viewable in identity schema |
| `required` | When `true`, all fields are mandatory (node name in config: `required`, label: "All Attributes Required") |
| `validateInputs` | When `true`, enforces IDM schema policy against submitted values |
| `identityAttribute` | Attribute used to identify the managed object (default: `userName`) |

- Outcomes: single (attribute values stored in shared state)
- Supports dot-path notation for nested attributes: `preferences/marketing`, `preferences/updates`
- Must be a PageNode child — standalone AttributeCollector renders no fields (see `nodes/utility-nodes.md` Rule 1)

### Attribute Present Decision node
Checks whether a specific attribute exists on the managed user object (regardless of whether the field is private).

**Configuration:**

| Field | Notes |
|---|---|
| `presentAttribute` | The object attribute to verify is present (e.g., `password`) |
| `identityAttribute` | The attribute to query in the IDM object (e.g., `userName`) |

- Outcomes: **True** (attribute present) / **False** (attribute absent)
- Use case: detect passwordless users — `presentAttribute: password` returns `False` for users without a password set, enabling conditional branching to email-gate verification instead of current-password challenge

### Attribute Value Decision node
Evaluates whether a specific attribute in the user's profile matches a configured comparison operation.

**Configuration:**

| Field | Notes |
|---|---|
| `comparisonOperation` | `PRESENT` — checks for attribute existence; `EQUALS` — checks if attribute value equals `comparisonValue` |
| `comparisonAttribute` | The object attribute to compare (e.g., `emailVerified`) |
| `comparisonValue` | The value to compare against when using `EQUALS` operation (e.g., `true`) |
| `identityAttribute` | The attribute used to look up the IDM object (e.g., `userName`) |

- Outcomes: **True** / **False**
- `PRESENT` is equivalent to a null-check and does not require a `comparisonValue`
- Common use: "Is Email Verified?" gate — `comparisonAttribute: emailVerified`, `comparisonOperation: EQUALS`, `comparisonValue: true`; `False` triggers email verification flow

### Required Attributes Present node
Checks whether all required attributes are present in shared state before proceeding.

- Outcomes: **True** (all present) / **False** (one or more missing)
- Use before `CreateObjectNode` in registration flows to prevent partial user creation

---

## User Object Operations

### Create Object node
Creates a new managed object (typically `managed/alpha_user`) using attributes collected in shared state.

**Configuration:**

| Field | Notes |
|---|---|
| `identityResource` | The IDM identity resource to create (e.g., `managed/alpha_user`). Must match the journey's identity resource. |

- Outcomes: **CREATED** / **FAILURE**
- On `FAILURE`: in production journeys, the failure path runs a `ScriptedDecisionNode` ("Delete User Entry") to clean up any partially created record before routing to FailureNode — prevents orphaned partial accounts
- `CREATED`: route to `IncrementLoginCountNode` to initialize the login count to 1 (enables `LoginCountDecisionNode` to trigger on the subsequent login)

### Patch Object node
Updates an existing managed object with attribute values from shared state.

**Configuration:**

| Field | Notes |
|---|---|
| `identityResource` | The IDM identity resource to patch (e.g., `managed/alpha_user`). Must match the journey's identity resource. |
| `patchAsObject` | `false` (default) — merges changes rather than replacing the whole object |
| `ignoredFields` | Fields from shared state to exclude from the patch (e.g., `[userName]` prevents username modification) |
| `identityAttribute` | Attribute used to look up the object (usually `userName` or `mail`) |

- Outcomes: **PATCHED** / **FAILURE**
- Uses: password update, email verification status flag, preferences update, MFA device metadata update

---

## Social Login

See `nodes/federation-contextual-nodes.md` → Social Provider Handler node (V2) and Select Identity Provider node for the full social login node documentation and entry patterns.

---

## Consent and Terms

### Accept Terms and Conditions node
Presents the current T&C version to the user and records acceptance with timestamp and version.

- Outcomes: single
- Common placement: embedded as a PageNode child alongside registration fields (co-located with signup form)

### Terms and Conditions Decision node
Checks whether the user has accepted the current version of terms.

- Outcomes: **True** (accepted and current) / **False** (not accepted or version outdated)
- `False` → `AcceptTermsAndConditionsNode`; used in authentication journeys to enforce T&C re-acceptance when a new version is published

### Consent Collector node
Collects user consent for data processing or specific purposes defined in the IDM consent schema.

**Configuration:**

| Field | Notes |
|---|---|
| `allRequired` | `true` — all configured mappings require consent to proceed |
| `message` | Localized privacy and consent notice displayed to the user |

- Outcomes: single

---

## Knowledge-Based Authentication (KBA)

### KBA Definition node
Prompts the user to define KBA security questions and answers during enrollment.

**Configuration:**

| Field | Notes |
|---|---|
| `message` | Localized message describing the purpose (default: "Select a security question.") |
| `allowUserDefinedQuestions` | `true` allows users to write their own custom KBA questions |

- Outcomes: single (questions stored in user profile)

### KBA Verification node
Presents the user's pre-defined KBA questions and checks answers.

**Configuration:**

| Field | Notes |
|---|---|
| `kbaInfoAttribute` | The attribute in the IDM user object where KBA questions/answers are stored |
| `identityAttribute` | The IDM attribute used to identify the object (e.g., `userName`) |

- Outcomes: **True** (answers correct) / **False** (answers incorrect)

### KBA Decision node
Evaluates whether the user has already set up KBA questions (i.e., meets the system's minimum required count).

**Configuration:**

| Field | Notes |
|---|---|
| `identityAttribute` | The IDM attribute used to retrieve the object |

- Outcomes: **True** (KBA set up and meets minimum) / **False** (not set up or insufficient)

---

## Profile Completeness

### Profile Completeness Decision node
Checks whether the user's profile meets a configured completeness threshold (% of non-null, user-viewable, user-editable fields).

**Configuration:**

| Field | Notes |
|---|---|
| `threshold` | Percentage [0–100] of required fields that must be populated |
| `identityAttribute` | The attribute to query for the IDM object |

- Outcomes: **True** (profile meets threshold) / **False** (profile incomplete)
- Use to trigger progressive profiling after login

### Query Filter Decision node
Evaluates an LDAP/SCIM-style filter against the user's profile attributes.

**Configuration:**

| Field | Notes |
|---|---|
| `queryFilter` | SCIM/LDAP-style filter string evaluated against the user object |
| `identityAttribute` | Attribute used to retrieve the user object |

- Outcomes: **True** (filter matches) / **False** (filter does not match)
- SCIM filter syntax example: `"!(/preferences pr) or /preferences/marketing eq false or /preferences/updates eq false"` — matches users who are missing the preferences attribute OR have it set to false
- Use dot-path notation for nested attributes: `/preferences/marketing`
- Use in combination with `LoginCountDecisionNode` for progressive profiling double-gate (see `journey-use-cases/progressive-profiling.md`)

---

## User Lifecycle / Provisioning

### Time Since Decision node
Evaluates whether a specified amount of time has elapsed since the user registered.

**Configuration:**

| Field | Notes |
|---|---|
| `elapsedTime` | Elapsed time in minutes to compare against |
| `identityAttribute` | The attribute to query in the IDM object |

- Outcomes: **True** (elapsed time has passed) / **False** (elapsed time has not passed)
- Use case: gate time-sensitive flows (e.g., require re-verification if account was created more than N minutes ago)

For passthrough authentication against a third-party system via ICF connector, see `nodes/basic-auth-nodes.md` → Passthrough Authentication node.

---

## PingOne Verify (Identity Proofing)

### PingOne Verify Evaluation node
Initiates a PingOne Verify identity proofing session (document capture, liveness check).

- Outcomes: **Success** / **Failure** / **Error**
- Requires PingOne Verify service configured in the environment

### PingOne Verify Completion Decision node
Checks the result of an ongoing PingOne Verify session.

- Outcomes: **Pass** / **Fail** / **Pending**

---

## PingOne User Operations

### PingOne Create User node
Creates a user in PingOne MT from within an AIC journey.

### PingOne Delete User node
Deletes a PingOne MT user from within an AIC journey.

### PingOne Identity Match node
Attempts to match an authenticating user against a PingOne identity.

- Outcomes: **Single Match** / **No Match** / **Multiple Matches**

---

## Common patterns

| Pattern | Nodes |
|---|---|
| Self-registration | AttributeCollector → RequiredAttributesPresent → CreateObject(CREATED) → IncrementLoginCount → Success |
| Create Object with cleanup | CreateObject(FAILURE) → ScriptedDecision("Delete User Entry") → FailureNode |
| Progressive profiling | ProfileCompletenessDecision(False) → AttributeCollector → PatchObject |
| T&C enforcement | TermsAndConditionsDecision(False) → AcceptTermsAndConditions → Success |
| KBA enrollment at first login | KbaDecision(False) → KbaCreate → Success |
| Anti-enumeration lookup | IdentifyExistingUser(true AND false) → EmailSuspendNode (same successor for both outcomes) |
| Passwordless branch | AttributePresentDecision(`password` = False) → EmailSuspendNode |
| Email verification gate | AttributeValueDecision(`emailVerified` EQUALS `true` = False) → email verification inner journey |
| Social + local choice | SelectIdPNode(socialAuthentication) → SocialProviderHandlerV2 / (localAuthentication) → Platform Username path |
| Passthrough auth (migration) | CredentialCollection → PassthroughAuthenticationNode(Authenticated) → Success / (Failed) → FailureNode |
| Social registration | SocialProviderHandlerV2(NO_ACCOUNT) → PageNode(AttributeCollector) → RequiredAttributesPresent → CreateObject |
| Time-gated re-verification | TimeSinceDecision(True) → verification inner journey |

## Prerequisites

- Managed object schema configured in IDM with the required attributes present and viewable.
- IDM accessible from the AIC/PingAM journey engine (standard in AIC; requires IDM connector in standalone PingAM).

## Common variants

- **B2B tenant:** use `managed/alpha_organization` alongside `managed/alpha_user` for org-scoped attribute collection.
- **Social registration:** Social Provider Handler V2 writes normalized claims to shared state; `AttributeCollectorNode` fills any missing required fields before `CreateObjectNode`.

## Related references

- `nodes/basic-auth-nodes.md`
- `nodes/federation-contextual-nodes.md`
- `nodes/utility-nodes.md`
- `journey-use-cases/account-recovery-and-username-reminder.md`
- `journey-use-cases/social-and-local-registration-authentication.md`
- `journey-use-cases/progressive-profiling.md`

## Source

[Identity management nodes](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[Attribute Collector node](https://docs.pingidentity.com/auth-node-ref/latest/attribute-collector.html)
[Create Object node](https://docs.pingidentity.com/auth-node-ref/latest/create-object.html)
