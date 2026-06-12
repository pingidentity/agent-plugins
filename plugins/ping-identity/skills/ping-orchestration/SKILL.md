---
name: ping-orchestration
description: "Use this skill whenever the task involves designing, building, or advising on authentication flows, journeys, or orchestration logic in Ping Identity. Triggers: DaVinci flows, PingOne Advanced Identity Cloud (AIC) journeys, PingAM authentication trees, scripted decision nodes; login, registration, recovery, MFA, or step-up journey design; passwordless authentication (passkeys, FIDO2, magic links, biometric); authenticator app enrollment, TOTP, push MFA flows; transaction approvals via email or push notification (CIBA, out-of-band step-up); progressive profiling, social login, consent; flow troubleshooting; 'what nodes do I need', 'design a flow for', 'build a journey that'. When the user asks 'journey vs DaVinci flow?', 'AIC or DaVinci?', 'which orchestration platform should we use?', or 'where do I configure MFA in Ping?' without stating both a use case (workforce / CIAM / B2B) AND a platform — you MUST ask one clarifying question before recommending. Do not guess. Also invoke with /ping-orchestration."
compatibility: Designed for Ping Identity orchestration tasks. MCP tools for PingOne Advanced Identity Cloud (AIC) are used when available to create and update journeys directly.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-orchestration

Design and build authentication flows, orchestration logic, and journey-based experiences across Ping Identity platforms. MCP tools handle execution; this skill supplies design patterns, node sequencing, branching logic, and platform-specific constraints.

## Invocation

Invoke this skill explicitly with `/ping-orchestration` or by saying "use ping-orchestration to...".

## When to use this skill

Trigger on ANY question — including advisory, planning, and "what nodes do I need" requests, not just implementation — when the task involves:
- Building or designing a login, registration, recovery, MFA, or step-up journey in PingOne Advanced Identity Cloud (AIC) / PingAM
- Passwordless authentication flows (passkeys, FIDO2, magic links, biometric)
- Authenticator app login, push MFA, or TOTP enrollment flows
- Transaction approvals via email or push (CIBA / out-of-band step-up)
- Creating or designing a DaVinci flow for authentication, MFA, or orchestration
- Configuring a PingAM authentication tree or scripted decision node
- Planning or reviewing journey structure before implementation
- Deciding between inner journeys, scripted nodes, or DaVinci connectors
- Any question about designing, planning, or advising on authentication flows, journeys, or orchestration logic in PingOne Advanced Identity Cloud (AIC), PingOne / DaVinci, or PingAM

## When NOT to use this skill

- If the platform is not yet set up (no tenant, no realm, no app registered): use `ping-foundation` first
- If the task is **configuring the platform layer** (apps, directories, policies, branding): use `ping-foundation`
- If the task is **invoking a Universal Service** (Protect, Verify, IGA, Credentials) without needing flow design: use `ping-universal-services`
- If the task is **integrating the flow into an app or SDK**: use `ping-app-integration`
- If unsure which platform: use `ping-quickstart` first

## Multi-skill use cases

| Sequence | Skill |
|---|---|
| Before: tenant, realm, identity store, app configured | `ping-foundation` |
| After: risk scoring, MFA step-up, identity verification | `ping-universal-services` |
| After: wire flow into web, mobile, or SDK app | `ping-app-integration` |

---

## MCP execution

Scan available tools for MCP tools that can perform the required operation. If matching tools are available, run the MCP config preflight first, then use them. Otherwise, proceed with curated references. See `references/runtime/mcp-preflight.md` for MCP config and Cursor preflight steps.

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne Advanced Identity Cloud (AIC), PingAM, identity cloud, ForgeRock lineage | [PingOne Advanced Identity Cloud](#pingone-advanced-identity-cloud) |
| PingOne + DaVinci | [PingOne / DaVinci](#pingone--davinci) |

---

## PingOne Advanced Identity Cloud

Sub-routing by task and journey use case: see `references/curated/pingone-st/routing-index.md`.

### Mandatory post-journey step: produce the Journey Node Manifest

After **every** `createJourney` or `updateJourneyNode` call, produce a Journey Node Manifest before handing off to any SDK skill — otherwise downstream skills generate the wrong callback views (e.g. `ValidatedUsernameCallback` instead of `NameCallback` for a login tree). Read `references/curated/pingone-st/journey-node-manifest.md` for the schema. Populate `emitsCallbacks` via Tier 1 live probe (preferred) or Tier 2 reference map (fallback). Write to `.ping/journey-manifest.<journeyName>.json`, echo a node→callbacks table, and state: *"Manifest written — pass it to the SDK skill."*

**Quick reference — node families:**

| Task | Reference |
|---|---|
| Journey Node Manifest (produced after every createJourney; consumed by all SDK skills) | `references/curated/pingone-st/journey-node-manifest.md` |
| Journey design principles, patterns, resilience, security | `references/curated/pingone-st/journey-design-patterns.md` |
| Node composition rules, PageNode usage, child node gotchas | `references/curated/pingone-st/nodes/node-fundamentals.md` |
| Username/password, passthrough auth, session entry, lifecycle outcomes | `references/curated/pingone-st/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/curated/pingone-st/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, PingOne Authorize | `references/curated/pingone-st/nodes/risk-management-nodes.md` |
| Registration, attributes, consent, KBA, T&C, social login, SelectIdP | `references/curated/pingone-st/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount | `references/curated/pingone-st/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/curated/pingone-st/nodes/federation-contextual-nodes.md` |

---

## PingOne / DaVinci

**Sub-routing by task:**

| Task | Reference |
|---|---|
| DaVinci flow concepts, connectors, variables, versioning | `references/curated/pingone-mt/davinci-overview.md` |
| DaVinci flow design patterns (login, registration, step-up, error) | `references/curated/pingone-mt/davinci-flow-patterns.md` |
| DaVinci registration + email verification + MFA enrollment/step-up | `references/curated/pingone-mt/davinci-registration-and-mfa.md` |

---

## Cross-platform orchestration patterns

| Task | Reference |
|---|---|
| Passkeys / passwordless / FIDO2 design across PingOne, PingOne Advanced Identity Cloud (AIC), Ping Software | `references/curated/cross-platform/passkeys-and-passwordless.md` |

---

## Retrieval escalation

Load 1–3 curated anchors for the detected platform/task; stop if sufficient.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| Platform setup not yet complete | `ping-foundation` |
| Shared services (Protect, Verify, IGA, Credentials) within the flow | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
| Platform selection or orientation | `ping-quickstart` |
