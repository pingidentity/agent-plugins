---
title: "PingOne Advanced Identity Cloud (AIC) — MFA Method Selection at Registration"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: ["mfa"]
audience: ["developer", "architect"]
use_cases: ["customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-05"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# AIC — MFA Method Selection at Registration

User selects one MFA method during registration (TOTP, WebAuthn/passkey, or Push). The chosen method is mandatory on all subsequent logins — no skip path.

## Scope

**Covers:** Registration journey with user-choice MFA enrollment, login journey with per-method routing, shared state contract between the two journeys.
**Does NOT cover:** SMS/email OTP enrollment, multi-method concurrent enrollment, step-up flows.

---

## Overview

Two journeys share a `custom_mfaDevices` attribute on `alpha_user`:

- **Registration** — creates the user, collects method choice, enrolls the chosen factor using AM-native nodes, then records the enrolled method via an existing tenant script.
- **Login** — authenticates username/password, reads `custom_mfaDevices` to determine which verifier to invoke.

---

## Prerequisites

1. `custom_mfaDevices` attribute added to `alpha_user` managed object schema (type: `array`, items: `string`, `returnByDefault: false`). See `ping-foundation → directory-setup.md → Custom attributes must be pre-created`.
2. Tenant must be HTTPS — required for WebAuthn.
3. Push service (APNs/FCM) configured if Push enrollment is offered.

---

## Registration journey

### Node sequence

```
PageNode (ValidatedUsernameNode + ValidatedPasswordNode + AttributeCollectorNode)
  → CreateObjectNode (CREATED → Select MFA Method; FAILURE → failure)
  → ScriptedDecisionNode "Select MFA Method"
      OTP      → GetAuthenticatorAppNode → OathRegistrationNode ──────────────────┐
      WebAuthn → WebAuthnRegistrationNode ──────────────────────────────────────┤
      PUSH     → GetAuthenticatorAppNode → PushRegistrationNode ─────────────────┤
      Error    → failure                                                           │
                                                              ┌───────────────────┘
                                          ScriptedDecisionNode "Set Allowed MFA Types"
                                            → ScriptedDecisionNode "Set MFA device in profile"
                                              → RecoveryCodeDisplayNode → success
```

### Key node configurations

**`OathRegistrationNode`** — `postponeDeviceProfileStorage: false`. Device stored directly on success; no separate `OathDeviceStorageNode` needed.

**`WebAuthnRegistrationNode`** — standalone node (not inside a PageNode). `postponeDeviceProfileStorage: false`. Required fields: `relyingPartyDomain` (tenant domain), `origins` (full `https://` URL), `excludeCredentials: false` (boolean), `trustStoreAlias: "trustalias"`.

**`PushRegistrationNode`** — `postponeDeviceProfileStorage` does not apply; device stored on success automatically.

### Shared state contract

The "Select MFA Method" `ScriptedDecisionNode` must write **`mfaDeviceType` as a string** to shared state before routing:

| Selected outcome | `mfaDeviceType` value |
|---|---|
| `OTP` | `"OTP"` |
| `WebAuthn` | `"FIDO2"` |
| `PUSH` | `"PUSH"` |

Do **not** write `mfaDeviceType` as an array. The standard "Set MFA device in profile" tenant script reads it as a string.

### Post-enrollment convergence

After any enrollment branch succeeds, two scripted decision nodes run in sequence:

1. **"Set Allowed MFA Types"** — seeds `ciam_allowedMFATypes: ["OTP", "PUSH", "FIDO2"]` in shared state (required input for the next script).
2. **"Set MFA device in profile"** (tenant script `Threat Detection - Set MFA device in user's profile`) — reads `_id`, `ciam_allowedMFATypes`, and `mfaDeviceType` from shared state; patches `custom_mfaDevices` on the user profile.

`RecoveryCodeDisplayNode` follows on the `true` outcome and shows the generated codes before routing to `success`.

---

## Login journey

### Node sequence

```
PageNode (UsernameCollectorNode + PasswordCollectorNode)
  → DataStoreDecisionNode (true → Set Allowed MFA Types; false → failure)
  → ScriptedDecisionNode "Set Allowed MFA Types"
  → ScriptedDecisionNode "Get Users Registered MFA devices"
      OTP    → PageNode(OathTokenVerifierNode) → success
      PUSH   → PushAuthenticationSenderNode → PushWaitNode → PushResultVerifierNode → success
      FIDO2  → WebAuthnAuthenticationNode → success
      Error  → failure
```

The "Get Users Registered MFA devices" script reads `custom_mfaDevices`, filters by `ciam_allowedMFATypes`, and routes to the matching verifier outcome.

---

## Common failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| "Invalid node config for: WebAuthnRegistrationNode" on create | `excludeCredentials` passed as string `"DONT_CHECK"` instead of boolean | Use `false` (boolean) |
| WebAuthn registration fails silently | `relyingPartyDomain` does not match origin domain | Set both `relyingPartyDomain` and `origins` to the tenant URL |
| "Set MFA device in profile" script returns Error | `_id` is null — `CreateObjectNode` sets `_id` in shared state but some script contexts miss it | Read both `nodeState.get("_id")` and `nodeState.getObject("objectAttributes")._id` as fallback |
| Login routes to Error after registration | `custom_mfaDevices` is empty on the user | "Set MFA device in profile" script was not reached, or `mfaDeviceType` was null/array — verify the Select script writes a string |
| 500 error on PageNode creation via MCP | Human-readable IDs used in `config.nodes[].\_id` | Use two-step: create children as top-level nodes, then call `updateJourneyNode` — see `node-fundamentals.md` |

---

## Related references

- `nodes/mfa-nodes.md` — OATH, WebAuthn, Push node configurations
- `nodes/node-fundamentals.md` — PageNode two-step MCP creation pattern
- `nodes/identity-management-nodes.md` — CreateObjectNode, AttributeCollectorNode
- `ping-foundation → directory-setup.md` — custom attribute schema setup

## Source

[Authentication node reference](https://docs.pingidentity.com/auth-node-ref/latest/overview.html)
