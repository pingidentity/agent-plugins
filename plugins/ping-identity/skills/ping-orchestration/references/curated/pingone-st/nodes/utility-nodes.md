---
title: "PingOne ST — Utility Nodes"
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

# PingOne ST — Utility Nodes

Flow control, session management, state manipulation, scripting, UI composition, and async coordination nodes.

## Scope

**Covers:** Scripted Decision, Inner Tree Evaluator, Page node, session/state nodes, messaging, timers, polling, request inspection, email suspend, and production-observed wiring patterns.
**Does NOT cover:** Authentication logic — see `basic-auth-nodes.md`. MFA — see `mfa-nodes.md`.

---

## Scripting

### Scripted Decision node
Executes a server-side JavaScript or Groovy script to implement custom logic not covered by built-in nodes. The script sets an `outcome` variable that maps to a named branch.

**Configuration:**

| Field | Purpose |
|---|---|
| Script | Select a Decision Node script defined in Scripts |
| Outcomes | List all possible outcome strings the script may return |
| Script Inputs | Restrict which shared state properties the script can read (default: `*`) |
| Script Outputs | Specify expected output properties (default: `*`) |

- Outcomes: whatever strings are listed in the Outcomes configuration
- **Critical:** if the script returns an outcome not listed in configuration, the node logs a warning and the journey stalls

**State access pattern (next-gen script syntax):**
```javascript
var username = nodeState.get("username").asString();
nodeState.putShared("myKey", "myValue");
outcome = "myOutcome";
```

**ScriptedDecisionNode as PageNode child (UI validator pattern):**
In production journeys, a `ScriptedDecisionNode` is embedded as a PageNode child alongside input-collecting nodes (e.g., `OathTokenVerifierNode`, `RecoveryCodeCollectorDecisionNode`). The script uses `callbacksBuilder.scriptTextOutputCallback()` to inject client-side JavaScript that enforces input constraints (maxlength, numeric-only, submit button state). It reads `invalidCodeErrorMessage` from shared state on re-entry and displays errors inline.

Standard naming conventions observed: "Validate Verification Code Input Script", "Validate Recovery Code Input Script", "Set Invalid Code Error Message Script".

Shared state keys set by these scripts: `invalidCodeErrorMessage`, `errorMessage`, `errorDetails`

---

## Flow Control

### Inner Tree Evaluator node
Invokes another journey (inner journey / sub-tree) from within the current journey. Enables reusable, composable flow components.

**Configuration:**

| Field | Purpose |
|---|---|
| Tree Name | Name of the journey to invoke |
| Error Outcome | Enables an `Error` outcome branch that captures exception details |

- Outcomes: **True** (inner journey reached Success) / **False** (any other completion) / **Error** (if enabled)
- Parent journey data (username, auth level) flows into the inner journey automatically
- Transient/secure state does NOT persist between parent and inner journey
- Unlimited nesting depth

**Production pattern — MFA inner journey chain:**
```
Main journey
  → InnerTreeEvaluatorNode (Threat Detection) → true/false
  → InnerTreeEvaluatorNode (MFA Device Registration) → true/false
  → InnerTreeEvaluatorNode (MFA Authentication) → true/false
  → SuccessNode
```
Each inner journey handles one concern. The main journey sequences them. Inner journey `false` outcomes route to FailureNode at the main level.

### Choice Collector node
Presents the user with a list of choices to select from.

- Outcomes: one branch per configured choice option

### Flow Control node
Provides conditional branching based on a script-evaluated condition without requiring a full Scripted Decision node.

### Retry Limit Decision node
Tracks the number of times a journey loop has executed and routes once a limit is reached.

- `retryLimit: 3`, `incrementUserAttributeOnFailure: true`
- Outcomes: **True** (within limit) / **False** (limit exceeded)
- Used in MFA retry loops: `False` routes to FailureNode; `True` loops back through error message script to input PageNode

### Login Count Decision node
Routes the journey based on how many times the user has logged in.

**Configuration:**

| Field | Notes |
|---|---|
| `interval` | `AT` — trigger at exactly count N; `EVERY` — trigger at count N and every login after |
| `amount` | The login count threshold |
| `identityAttribute` | The IDM attribute used to retrieve the user object |

- Outcomes: **True** (count matches condition) / **False** (count does not match)
- `AT` is preferred for one-time prompts — prevents repeated triggering on every subsequent login
- Use as first gate in a progressive profiling inner journey (see `journey-use-cases/progressive-profiling.md`)

### Increment Login Count node
Increments the user's stored login count. Single `outcome`.

- Place post-registration (`CreateObjectNode(CREATED)`) to initialize the count at 1 — enables `LoginCountDecisionNode` to fire correctly on the next login

---

## UI / Page Composition

### Page node
Combines multiple input-collecting nodes onto a single user-facing screen. Reduces round-trips for multi-field forms.

**Configuration fields:**
- Page Header, Description, Submit Button Text (all localizable)
- Theme: override the journey theme for this specific page
- Stage: hint for client-side rendering

**Rules:**
- Page nodes cannot be nested inside other Page nodes
- Only the last child node may have multiple outcomes
- Non-interactive nodes (e.g., Scripted Decision without callbacks) should be placed outside Page nodes unless they are acting as UI validators

#### Rule 1 — Child nodes are REQUIRED

`config.nodes` must declare at least one child node. An empty array produces a visually empty page ("Drag nodes here") — no inputs render and the user cannot proceed.

```json
"config": {
  "nodes": [
    {"nodeType": "ValidatedUsernameNode",  "displayName": "Platform Username"},
    {"nodeType": "ValidatedPasswordNode",   "displayName": "Platform Password"}
  ],
  "pageHeader": {"en": "Sign In"},
  "pageDescription": {}
}
```

The PageNode's outcomes come from the child decision node embedded in it — not from the PageNode itself.

#### Rule 2 — Username + password share one PageNode

Never split username and password across two PageNodes unless the user explicitly requests a multi-step login:

```
Single PageNode
  ├── ValidatedUsernameNode  (child)
  └── ValidatedPasswordNode  (child)
      → outcome → DataStoreDecisionNode
```

#### Rule 3 — OTP collector pages must embed the collector node

A PageNode for OTP collection without `OneTimePasswordCollectorDecisionNode` as a child renders no input and provides no outcomes:

```json
"config": {
  "nodes": [
    {
      "nodeType": "OneTimePasswordCollectorDecisionNode",
      "displayName": "OTP Collector Decision"
    }
  ],
  "pageHeader": {"en": "One Time Passcode Required"},
  "pageDescription": {"en": "Please check your email and enter your passcode"}
}
```

#### Rule 4 — MFA code entry pages embed both a validator script and the verifier node

Production MFA code entry PageNodes always contain two child nodes:
1. `ScriptedDecisionNode` (UI validator — client-side input enforcement)
2. The MFA verifier node (`OathTokenVerifierNode`, `RecoveryCodeCollectorDecisionNode`, etc.)

The ScriptedDecisionNode drives outcomes; the verifier node validates server-side.

### Message node
Displays a localized message to the user with a configurable button to proceed.

- Outcomes: single

### Email Suspend node
Suspends the journey and emails the user a magic link to resume at a specific point.

**Configuration:**

| Field | Notes |
|---|---|
| `emailTemplateName` | IDM email template name to send |
| `emailAttribute` | The IDM email field to send to (e.g., `mail`) |
| `objectLookup` | `true` — queries the existing object for the template; `false` uses the object in shared state |
| `emailSuspendMessage` | Localized browser message while the user waits (default: "An email has been sent to your inbox.") |
| `suspendDuration` | Optional duration in minutes the journey stays suspended |
| `identityAttribute` | The IDM attribute used to identify the object |

- Outcomes: single (journey suspends; resumes when user clicks the link)
- The email template must contain `{{object.resumeURI}}` as the resume link
- `objectLookup: true` required for templates that embed user attributes (e.g., `{{object.userName}}`)
- Contrast with `EmailTemplateNode`: EmailSuspend suspends and gates continuation on user action; EmailTemplate sends a non-blocking notification and the journey continues immediately

---

## Session Management

### Get Session Data node (`SessionDataNode`)
Retrieves a value from the current active session and writes it to shared state.

**Configuration:**

| Field | Notes |
|---|---|
| `sessionDataKey` | The session property key to read (production value: `UserToken`) |
| `sharedStateKey` | The shared state key to write the value to (production value: `userName`) |

**Production pattern — authenticated journey entry:**
```
SessionDataNode (sessionDataKey: UserToken, sharedStateKey: userName)
  → AttributePresentDecisionNode
```

Used as the **first node in authenticated journeys** (e.g., password update) to identify the current user without presenting a login form. The extracted `userName` is then available for `DataStoreDecisionNode`, `IdentifyExistingUserNode`, and `PatchObjectNode` downstream.

- Outcomes: single

### Set Session Properties node
Sets custom key-value properties on the authenticated session and optionally overrides session timeout values.

**Configuration:**
- Properties: key-value pairs added to the session
- Maximum Session Time: overrides realm-level max session duration (minutes)
- Maximum Idle Time: overrides realm-level idle timeout (minutes)

- Outcomes: single
- Ignored when the journey runs with `noSession=true`
- Last processed node wins if multiple Set Session Properties nodes run

### Remove Session Properties node
Removes specified properties from the current session. Single `outcome`.

---

## State Management

### Set State node
Writes arbitrary key-value data to shared state. Outcomes: single.

### Config Provider node
Reads configuration values from a named secret or ESV and injects them into shared state.

- Outcomes: **outcome** (success) / **CONFIGURATION_FAILED**
- Used in Financial Services Make Payment to externalize success/failure message text from ESVs rather than hardcoding in scripts

### Query Parameter node
Extracts a query parameter from the incoming request and writes it to shared state. Outcomes: single.

### Request Header node
Extracts a specific HTTP request header value and writes it to shared state. Outcomes: single.

---

## Async / Polling

### Polling Wait node
Pauses journey execution and polls at a configured interval for an external event.

- `secondsToWait: 5`
- Outcomes: **DONE** (event received) / **EXITED** (user dismissed the wait screen)
- Observed at end of complex registration flows (CIAM Passwordless, Financial Services, Money Transfer) — polls for IDM provisioning completion
- Also used in push authentication loop: `PushSender → PushWaitNode(DONE) → PushResultVerifier`

### Email Template node (`EmailTemplateNode`)
Sends a non-blocking email notification without suspending the journey.

**Configuration:**

| Field | Notes |
|---|---|
| `emailTemplateName` | IDM email template name to send |
| `emailAttribute` | The IDM email field to send to (e.g., `mail`) |
| `identityAttribute` | The IDM attribute used to identify the object |

- Outcomes: **emailSent** / **emailNotSent**
- Templates observed: `disabledAccountRecovery`, `magicLinkTemplate`
- Contrast with `EmailSuspendNode`: EmailTemplate is fire-and-forget; the journey continues regardless of whether the email was sent
- `emailNotSent` should still proceed — notification failure should not block the journey

---

## URL / Redirect

### Success URL node
Sets a custom redirect URL for successful journey completion.

- Used in Financial Services and Money Transfer main journeys to redirect the user to an application page after session establishment

### Failure URL node
Sets a custom redirect URL for journey failure.

---

## Outcome Customization

### Set Success Details node
Customizes the response returned to the client on successful journey completion.

### Set Error Details node
Sets a custom error response when routing to Failure.

---

## Common patterns

| Pattern | Nodes |
|---|---|
| Authenticated journey entry | SessionDataNode → AttributePresentDecisionNode |
| Multi-field registration form | Page(AttributeCollector + ValidatedUsername + ValidatedPassword + AcceptT&C) → CreateObjectNode |
| MFA code entry with UI validation | Page(ScriptedDecisionNode + OathTokenVerifierNode) → successOutcome / failureOutcome → retry loop |
| Recovery code entry | Page(ScriptedDecisionNode + RecoveryCodeCollectorDecisionNode) → True / False → retry loop |
| Progressive profiling gate | LoginCountDecisionNode → QueryFilterDecisionNode → Page(AttributeCollector) → PatchObjectNode |
| Email verification | OTP Email Sender → EmailSuspendNode → OTP Collector Decision |
| Push wait loop | PushSender(SENT) → PushWaitNode(DONE) → PushResultVerifier(WAITING) → loop back to PushWaitNode |
| Async provisioning poll | CreateObjectNode(CREATED) → PollingWaitNode(DONE) → SuccessNode |
| Inner journey chain (MFA) | ITE(ThreatDetection) → ITE(MFADeviceRegistration) → ITE(MFAAuthentication) → SuccessNode |
| Session enrichment | SetState → SetSessionProperties |

## Related references

- `nodes/basic-auth-nodes.md`
- `nodes/mfa-nodes.md`
- `nodes/identity-management-nodes.md`
- `../scripted-decision-nodes.md`
- `../inner-journeys.md`

## Source

[Utility nodes](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
[Scripted Decision node](https://docs.pingidentity.com/auth-node-ref/latest/scripted-decision.html)
[Inner Tree Evaluator node](https://docs.pingidentity.com/auth-node-ref/latest/inner-tree-evaluator.html)
[Page node](https://docs.pingidentity.com/auth-node-ref/latest/page.html)
[Set Session Properties node](https://docs.pingidentity.com/auth-node-ref/latest/set-session-properties.html)
