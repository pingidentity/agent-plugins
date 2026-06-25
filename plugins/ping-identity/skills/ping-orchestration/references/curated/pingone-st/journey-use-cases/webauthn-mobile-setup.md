---
title: "AIC — WebAuthn / Passkeys Mobile Prerequisites (Android & iOS)"
product_family: pingone-st
products: ["pingone-aic", "pingam"]
capabilities: ["orchestration", "mfa", "passwordless"]
services: ["mfa"]
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-24"
slug: "https://docs.pingidentity.com/pingoneaic/end-user/upload-android-assetlinks.html"
---

# AIC — WebAuthn / Passkeys Mobile Prerequisites (Android & iOS)

AIC server-side setup required before `WebAuthnRegistrationNode` and `WebAuthnAuthenticationNode` will work in native Android and iOS apps using the Ping Orchestration SDKs.

## Scope

**Covers:** The three AIC-side steps that must be in place before mobile WebAuthn works — Android Digital Asset Links file, Apple App Site Association file, and CORS policy. Includes MCP tool invocations and journey node settings.

**Does NOT cover:**
- SDK-side callback wiring — see `ping-app-integration` → FIDO/passkey guides
- Web (browser) WebAuthn — no asset link files are needed for web; CORS setup is the same
- WebAuthn journey design patterns — see `references/curated/cross-platform/passkeys-and-passwordless.md`

---

## Overview

For native Android and iOS apps, the OS must verify that the app is authorized to use the AIC domain as a WebAuthn relying party. AIC hosts these verification files itself via its IDM config API.

Three steps are required:

| Step | File / config | MCP tool |
|---|---|---|
| 1 | Android Digital Asset Links — `/.well-known/assetlinks.json` | `applyAndroidAssetLinks` |
| 2 | Apple App Site Association — `/.well-known/apple-app-site-association` | `applyAppleAppAssociation` |
| 3 | CORS policy allowing the app's origin | `applyEnvironmentConfiguration` (`globalAmService` target) or `createCorsPolicyTool` |

Both files can also be applied via the `androidAssetLinks` and `appleAppAssociation` targets of `applyEnvironmentConfiguration` in a single call.

---

## Step 1 — Upload Android Digital Asset Links

AIC hosts the `assetlinks.json` file at `PUT /openidm/config/fidc/assetlinks.<domain>` with body `{ "data": <assetLinks array> }`. Each PUT replaces the full file.

**MCP tool:** `applyAndroidAssetLinks`

```json
{
  "domain": "openam-example.forgeblocks.com",
  "assetLinks": [
    {
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.example.myapp",
        "sha256_cert_fingerprints": [
          "AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99"
        ]
      }
    }
  ]
}
```

**Notes:**
- `domain` must be the exact AIC tenant hostname or configured custom domain that the app uses as its WebAuthn `rpId`
- `sha256_cert_fingerprints` — get from your signing keystore: `keytool -list -v -keystore release.jks -alias <alias> | grep SHA256`
- For debug builds, include a second object in the array with the debug certificate fingerprint
- Multiple apps — include one object per app in the array

**Verification:** After upload, `GET https://<domain>/.well-known/assetlinks.json` should return the content without authentication.

---

## Step 2 — Upload Apple App Site Association

AIC hosts the `apple-app-site-association` file at `PUT /openidm/config/fidc/apple-app-site-association.<domain>` with body `{ "data": { "applinks": ..., "webcredentials": ... } }`.

**MCP tool:** `applyAppleAppAssociation`

```json
{
  "domain": "openam-example.forgeblocks.com",
  "applinks": {
    "details": [
      {
        "appIDs": ["ABCDE12345.com.example.myapp"],
        "components": [{ "/": "/myapp/*" }]
      }
    ]
  },
  "webcredentials": {
    "apps": ["ABCDE12345.com.example.myapp"]
  }
}
```

**Notes:**
- `appIDs` format: `<TeamID>.<BundleID>` — both are visible in Xcode → Signing & Capabilities
- `webcredentials` is required for WebAuthn / passkeys (not just Universal Links)
- `applinks` enables Universal Links; include it so the OS will also handle in-app deep links
- If using a custom domain, upload the file to every domain in the WebAuthn `rpId`

**Verification:** After upload, `GET https://<domain>/.well-known/apple-app-site-association` should return the content without authentication.

---

## Step 3 — CORS policy

The AIC CorsService must allow requests from the app's origin. For native apps using a custom scheme or loopback, ensure the `acceptedOrigins` list covers that origin.

**Via `applyEnvironmentConfiguration` (`globalAmService` target):**

```json
{
  "globalAmService": {
    "serviceName": "CorsService",
    "serviceConfig": {
      "acceptedOrigins": ["https://app.example.com"]
    }
  }
}
```

This performs a GET-merge-PUT so existing origins are preserved.

**Or use the standalone CORS policy tools** (`createCorsPolicyTool`, `updateCorsPolicyTool`) if you need fine-grained control per policy entry.

---

## Journey node configuration

Once the three prerequisites above are in place, configure the journey nodes:

### WebAuthnRegistrationNode

| Setting | Value | Notes |
|---|---|---|
| `relyingPartyName` | Display name (e.g., "Example Corp") | Shown in the OS passkey prompt |
| `rpId` | `openam-example.forgeblocks.com` | Must exactly match `domain` used in Steps 1–2 |
| `userVerification` | `required` for higher assurance; `preferred` for balanced | Sets the OS biometric/PIN prompt requirement |
| `attachmentType` | `platform` | Restricts to the device's built-in authenticator (Face ID, fingerprint) |
| `residentKey` | `required` or `preferred` | Required for discoverable credentials (passkey auto-fill) |

### WebAuthnAuthenticationNode

| Setting | Value | Notes |
|---|---|---|
| `rpId` | Same as registration | Must match exactly |
| `userVerification` | Same as registration | Mismatch causes assertion failure |
| `attachmentType` | `platform` | Match registration |

**Critical:** `rpId` at authentication must equal `rpId` at registration. A mismatch causes a `NotAllowedError` on the assertion.

---

## Applying all targets in a single call

Use `applyEnvironmentConfiguration` to set all three in one tool call:

```json
{
  "androidAssetLinks": {
    "domain": "openam-example.forgeblocks.com",
    "assetLinks": [{ ... }]
  },
  "appleAppAssociation": {
    "domain": "openam-example.forgeblocks.com",
    "applinks": { ... },
    "webcredentials": { ... }
  },
  "globalAmService": {
    "serviceName": "CorsService",
    "serviceConfig": {
      "acceptedOrigins": ["https://app.example.com"]
    }
  }
}
```

Returns a `results` map — partial success is allowed; check each key's `success` flag.

---

## Routing back

| If the task is also... | Reference |
|---|---|
| SDK-side FIDO2 callback wiring for Android | `ping-app-integration` → Android FIDO2 / passkeys guide |
| SDK-side FIDO2 callback wiring for iOS | `ping-app-integration` → iOS FIDO2 / passkeys guide |
| WebAuthn journey design and registration patterns | `references/curated/cross-platform/passkeys-and-passwordless.md` |
| MFA device registration journey structure | `references/curated/pingone-st/journey-use-cases/passwordless-mfa-registration.md` |
| WebAuthn node config reference | `references/curated/pingone-st/nodes/mfa-nodes.md` |

## Source

- [AIC — Upload Android assetlinks.json](https://docs.pingidentity.com/pingoneaic/end-user/upload-android-assetlinks.html)
- [AIC — Upload iOS Apple App Site Association](https://docs.pingidentity.com/pingoneaic/end-user/upload-ios-apple-app-site-association.html)
- [Ping Orchestration SDK — Android FIDO2 before you begin](https://developer.pingidentity.com/orchsdks/journey/use-cases/fido/android/before-you-begin.html)
- [Ping Orchestration SDK — iOS FIDO2 before you begin](https://developer.pingidentity.com/orchsdks/journey/use-cases/fido/ios/before-you-begin.html)
