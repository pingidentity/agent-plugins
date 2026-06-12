---
title: "PingOne Advanced Identity Cloud (AIC) — Journey Node Manifest"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: reference
status: current
canonical: true
last_updated: "2026-06-12"
slug: "https://docs.pingidentity.com/auth-node-ref/latest/overview.html"
---

# Journey Node Manifest

A **Journey Node Manifest** is a structured JSON artifact produced by `ping-orchestration` immediately after any `createJourney` / `updateJourney` call. It records the **resolved** callbacks emitted by every node in the journey — ground truth that downstream SDK skills (`ping-app-integration`, `ping-orchestration-ios-sdk`, `ping-orchestration-android-sdk`, etc.) must read before generating any callback/collector views.

## Scope

**Covers:** Journey Node Manifest schema, Tier 1 live probe protocol, Tier 2 node→callback reference map, manifest persistence, and consumer instructions for SDK skills.
**Does NOT cover:** Individual node configuration — see `nodes/basic-auth-nodes.md`, `nodes/mfa-nodes.md`, etc. SDK code generation — see `ping-app-integration` and the companion SDK skills.

---

## Why it exists

The same node type emits **different callbacks** depending on tree purpose and configuration:

- `ValidatedUsernameNode` in an **authentication** tree → `NameCallback`
- `ValidatedUsernameNode` in a **registration** tree → `ValidatedCreateUsernameCallback` / `ValidatedUsernameCallback`

An SDK skill that infers the callback from the node type name alone will generate the wrong view in the wrong context. The manifest removes this guessing.

---

## When to produce it

After **every** `createJourney` or `updateJourneyNode` call, build and persist the manifest before handing off to any SDK or integration skill.

---

## Manifest schema

```jsonc
{
  "journeyName": "AgentsLogin",
  "realm": "alpha",
  "serverUrl": "https://openam-<tenant>.forgeblocks.com/am",
  "identityResource": "managed/alpha_user",
  "purpose": "authentication",       // authentication | registration | password-reset | mfa | progressive-profile
  "steps": [
    {
      "order": 1,
      "displayName": "Username",
      "nodeType": "PageNode",
      "children": [
        {
          "nodeType": "ValidatedUsernameNode",
          "config": { "validateInput": false },
          "emitsCallbacks": ["NameCallback"],
          "callbackSource": "probe"   // probe | reference-map | assumed
        }
      ]
    },
    {
      "order": 2,
      "displayName": "Password",
      "nodeType": "PageNode",
      "children": [
        {
          "nodeType": "ValidatedPasswordNode",
          "config": { "validateInput": false },
          "emitsCallbacks": ["PasswordCallback"],
          "callbackSource": "probe"
        }
      ]
    }
  ],
  "callbackUnion": ["NameCallback", "PasswordCallback", "TextOutputCallback"],
  "recommendedCallbackTier": "basic",  // basic | advanced
  "selfAdvancingCallbacks": [],
  "browserRequired": false,            // true if SelectIdP / social provider present
  "sessionCookieName": "iPlanetDirectoryPro",  // confirm from tenant Global Settings
  "notes": [
    "ValidatedUsernameNode / ValidatedPasswordNode emit Name/PasswordCallback in authentication trees.",
    "Cookie name not yet confirmed against tenant Global Settings — see ping-foundation am-services.md."
  ]
}
```

### Key fields

| Field | Description |
|---|---|
| `purpose` | Tree intent — drives the Tier 2 reference map lookup. Derive from journey name, description, or ask the user. |
| `emitsCallbacks` | **The resolved list of callbacks this node emits in this tree.** Set from Tier 1 probe or Tier 2 map. Never infer from the node type name alone. |
| `callbackSource` | `"probe"` — live result, authoritative. `"reference-map"` — table lookup, inferred. `"assumed"` — no source, flag for manual review. |
| `callbackUnion` | Deduplicated union of all `emitsCallbacks` across all nodes/steps. SDK skills generate handlers for exactly this set. |
| `recommendedCallbackTier` | `"basic"` — standard callbacks (Name, Password, Choice, TextOutput). `"advanced"` — includes FIDO2/WebAuthn, Push, OATH, Social. |
| `browserRequired` | `true` when `SelectIdPNode` or a social provider handler is present — signals that a WKWebView or ASWebAuthenticationSession is required. |
| `sessionCookieName` | AIC session cookie name (default `iPlanetDirectoryPro`; tenant-specific values override). Read from Global Settings. |

---

## How to populate `emitsCallbacks` — two tiers

### Tier 1: live callback probe (authoritative, use by default)

After creating the journey, start it once and record the real callbacks:

```
POST {serverUrl}/json/realms/root/realms/{realm}/authenticate
     ?authIndexType=service&authIndexValue={journeyName}
```

Walk each `callbacks[].type` in the response, submitting throwaway values (`"dummy"`, `"00000000"`) to advance, until `tokenId` / success or a terminal node. Record every `type` seen → `emitsCallbacks`, `callbackSource: "probe"`.

**Abandon the session:** do not submit the final success step; the probe session can be left to expire or explicitly invalidated.

> If an AIC MCP tool `probeJourneyCallbacks` (or equivalent) is available, use it instead of hand-rolling HTTP.

### Tier 2: context-aware reference map (fallback, offline / no credentials)

When a live probe is not possible, fall back to this table. Mark entries `callbackSource: "reference-map"`.

| Node type | Tree purpose | Emits |
|---|---|---|
| `ValidatedUsernameNode` | **authentication** | `NameCallback` |
| `ValidatedUsernameNode` | registration | `ValidatedCreateUsernameCallback`, `ValidatedUsernameCallback` |
| `ValidatedUsernameNodeV2` | **authentication** | `NameCallback` |
| `ValidatedUsernameNodeV2` | registration | `ValidatedCreateUsernameCallback`, `ValidatedUsernameCallback` |
| `ValidatedPasswordNode` | **authentication** | `PasswordCallback` |
| `ValidatedPasswordNode` | registration / password-reset | `ValidatedCreatePasswordCallback`, `ValidatedPasswordCallback` |
| `PageNode` | any | union of children's callbacks |
| `ChoiceCollectorNode` | any | `ChoiceCallback` |
| `AttributeCollectorNode` | any | `StringAttributeInputCallback` (+ `BooleanAttributeInputCallback`, `NumberAttributeInputCallback` per attribute type) |
| `KbaCreateNode` | registration | `KbaCreateCallback` |
| `OneTimePasswordCollectorDecisionNode` | mfa | `PasswordCallback` |
| `WebAuthnAuthenticationNode` | authentication / mfa | `HiddenValueCallback`, `MetadataCallback`, `WebAuthnAuthenticationCallback` |
| `WebAuthnRegistrationNode` | registration / mfa | `HiddenValueCallback`, `MetadataCallback`, `WebAuthnRegistrationCallback` |
| `SelectIdPNode` | any | `IdPCallback` (`browserRequired: true`) |
| `TextOutputNode` | any | `TextOutputCallback` |
| `HiddenValueCollector` | any | `HiddenValueCallback` |
| `PollingWaitNode` | any | `PollingWaitCallback` |
| `ConsentMappingNode` | registration | `ConsentMappingCallback` |
| `AcceptTermsAndConditionsNode` | registration | `TermsAndConditionsCallback` |

> Tier 2 is a safety net. Tier 1 probe overrides it whenever available. If neither is available, set `callbackSource: "assumed"` and flag for manual review.

---

## Persistence and session handoff

1. Write the manifest to `.ping/journey-manifest.<journeyName>.json` in the working directory.
2. Echo a compact summary table in the chat response:

   ```
   Journey: AgentsLogin | Purpose: authentication
   ─────────────────────────────────────────────────────────
   Step | Node                    | Emits                 | Source
   1    | ValidatedUsernameNode   | NameCallback          | probe
   2    | ValidatedPasswordNode   | PasswordCallback      | probe
   ─────────────────────────────────────────────────────────
   callbackUnion: [NameCallback, PasswordCallback]
   ```

3. State explicitly in the handoff: *"Manifest written to `.ping/journey-manifest.<journeyName>.json` — pass it to the SDK skill."*

---

## Consumer instructions (for SDK and integration skills)

When invoked for a Journey integration task:

1. **Look for `.ping/journey-manifest.*.json` first.** If present, use `callbackUnion` and per-node `emitsCallbacks` to decide exactly which callback/collector views to generate. Do **not** infer from node type names.
2. If no manifest exists, fall back to Journey Export Analysis or ask the user — and emit a warning: *"No manifest found — callback generation is inference-based and may be incorrect."*
3. The `create-sample` arg surface should accept `--manifest <path>` so the manifest can be passed explicitly in a fresh session.

---

## Common mistakes this prevents

| Mistake | How the manifest prevents it |
|---|---|
| `ValidatedUsernameCallback` view generated for a login tree | `emitsCallbacks: ["NameCallback"]` from probe or Tier 2 map |
| `ValidatedPasswordCallback` view generated for a login tree | `emitsCallbacks: ["PasswordCallback"]` from probe or Tier 2 map |
| Missing `ChoiceCallback` handler for `ChoiceCollectorNode` | `callbackUnion` explicitly lists it |
| Unnecessary `WebAuthnAuthenticationCallback` for a basic login | `callbackUnion` does not include it → SDK skill omits it |

---

## Related references

- `nodes/basic-auth-nodes.md` — ValidatedUsernameNode, ValidatedPasswordNode callback context
- `nodes/mfa-nodes.md` — WebAuthn, OATH, Push callback types
- `nodes/identity-management-nodes.md` — AttributeCollectorNode, KbaCreateNode
- `ping-foundation/references/curated/pingone-st/am-services.md` — session cookie name discovery (P6)
