---
title: "Mobile Integration Basics — Android and iOS SDK"
product_family: cross-platform
products: ["pingone", "pingone-aic"]
capabilities: ["app-integration"]
services: []
audience: ["developer"]
use_cases: ["customer", "workforce", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/native-sdks/p1_native_sdks_landing.html"
---

# Mobile Integration Basics — Android and iOS SDK

Orientation for integrating Ping Identity authentication into Android (Kotlin) and iOS (Swift) apps using the PingOne Native SDKs — covers both PingOne (multi-tenant cloud) and PingOne Advanced Identity Cloud (AIC) targets.

## Scope

**Covers:**
- Android SDK import, initialization, OIDC flow, token storage, deep link handling, MFA push
- iOS SDK import, initialization, OIDC flow, token storage, universal links, Keychain
- Feature comparison table: Android vs. iOS
- Common failure modes for each platform
- Migration path from ForgeRock SDK to Ping Native SDK (naming and API changes)

**Does NOT cover:**
- Flow or journey design (Journey nodes, DaVinci collectors) — use `ping-orchestration`
- Platform-side application registration or redirect URI setup — use `ping-foundation`
- Web/React SDK integration — see `references/curated/web-integration-basics.md`
- Troubleshooting diagnosis beyond what is listed here — see `references/curated/integration-troubleshooting-basics.md`

## Android SDK integration

### SDK import

Gradle (Kotlin DSL):

```kotlin
dependencies {
    // Core OIDC + Journey
    implementation("com.pingidentity.sdks:oidc:<version>")
    implementation("com.pingidentity.sdks:journey:<version>")

    // DaVinci (if targeting PingOne / DaVinci flows)
    implementation("com.pingidentity.sdks:davinci:<version>")

    // Optional modules
    implementation("com.pingidentity.sdks:fido:<version>")       // FIDO2 / passkeys
    implementation("com.pingidentity.sdks:protect:<version>")    // Protect signals
    implementation("com.pingidentity.sdks:push:<version>")       // Push MFA (FCM)
    implementation("com.pingidentity.sdks:externalidp:<version>") // Social login
}
```

The SDK is hosted on Maven Central and on the Ping Identity Maven repository (`maven.pingidentity.com`). Add both repositories to `settings.gradle.kts` if Maven Central is not resolving the artifact.

### Initialization

Initialize once per process lifetime, typically in `Application.onCreate()`:

```kotlin
PingOne.init(context) {
    // Required: OIDC client configuration
    oidcConfig {
        clientId = "<client-id>"
        discoveryEndpoint = "https://<tenant>/.well-known/openid-configuration"
        // or explicit endpoints:
        // authorizationEndpoint = "..."
        // tokenEndpoint = "..."
        redirectUri = "myapp://callback"
        scopes = listOf("openid", "profile", "offline_access")
    }
    // Optional: custom logger
    logger {
        level = LogLevel.DEBUG
    }
}
```

Constraint: `PingOne.init()` must complete before any auth call. Calling `startAuthentication()` before init completes throws `PingOneNotInitializedException`.

### OIDC authorization code + PKCE flow

```kotlin
// Trigger login from an Activity or Fragment
val result = PingOne.startAuthentication(activity)

when (result) {
    is AuthResult.Success -> {
        val tokens = result.tokens
        // tokens.accessToken, tokens.idToken, tokens.refreshToken
    }
    is AuthResult.Failure -> {
        // result.error: PingOneError
    }
}
```

PKCE is enabled by default in the SDK — no additional configuration required. The SDK generates the `code_verifier` and `code_challenge` internally.

### Token storage — Android Keystore

The SDK stores tokens in `EncryptedSharedPreferences` backed by Android Keystore. No plaintext token storage occurs by default.

Key constraint: the encryption key is tied to the device. Tokens are not portable across devices or backups. Developers must not add `android:allowBackup="true"` for credential data; use `android:fullBackupContent` exclude rules if general backup is needed.

### Handling redirect URIs (deep links)

Register the redirect URI as an intent filter in `AndroidManifest.xml`:

```xml
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="myapp" android:host="callback" />
</intent-filter>
```

The scheme and host must exactly match the `redirectUri` passed to `oidcConfig` and the value registered in the Ping admin console. A mismatch causes `redirect_uri_mismatch` from the authorization server.

### Push MFA (FCM)

Requirements:
- FCM project configured in Firebase Console; `google-services.json` present in the app module
- PingOne Push policy enabled on the tenant
- Device registration completed: `PingOne.registerDevice(fcmToken)` called after obtaining an FCM registration token from `FirebaseMessaging.getInstance().token`

Incoming push messages arrive as FCM data messages. Pass the payload to `PingOne.handleRemoteMessage(remoteMessage)` in `FirebaseMessagingService.onMessageReceived()`.

Common failure: push not delivered because device registration was skipped. Device registration verification: admin surface — Users → [user] → Devices; a registered device appears with status "registered".

## iOS SDK integration

### SDK import (Swift Package Manager)

In `Package.swift` or the Xcode package dependency dialog:

```
https://github.com/ForgeRock/ping-ios-sdk
```

Select the modules needed:

| Module | When to include |
|---|---|
| `PingOidc` | All apps — OIDC token management |
| `PingJourney` | AIC / PingAM Journey-based flows |
| `PingDavinci` | PingOne DaVinci-based flows |
| `PingStorage` | Keychain-backed token storage (included by default) |
| `PingExternalIdP` | Social login (Google, Apple, Facebook) |
| `PingProtect` | PingOne Protect risk signals |
| `PingOath` | TOTP / HOTP soft tokens |
| `PingLogger` | Debug and error logging |
| `PingFido` | FIDO2 / passkey registration and assertion (iOS 16+) |

CocoaPods alternative: `pod 'PingOidc'`, `pod 'PingJourney'`, etc.

### Initialization

Initialize in `@main App.init()` or `AppDelegate.application(_:didFinishLaunchingWithOptions:)`:

```swift
import PingOidc

let config = OidcClientConfig(
    clientId: "<client-id>",
    discoveryEndpoint: "https://<tenant>/.well-known/openid-configuration",
    redirectUri: "myapp://callback",
    scopes: ["openid", "profile", "offline_access"]
)
let oidcClient = OidcClient(config: config)
```

### OIDC authorization code + PKCE on iOS

```swift
import PingOidc

let result = await oidcClient.authorize()

switch result {
case .success(let tokens):
    // tokens.accessToken, tokens.idToken, tokens.refreshToken
case .failure(let error):
    // PingOidcError
}
```

PKCE is generated by the SDK. The authorization flow launches `ASWebAuthenticationSession` internally when using the redirect-based flow.

### Token storage — Keychain

`PingStorage` persists tokens in the iOS Keychain with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`. This attribute ties the token to the device and excludes it from iCloud Keychain sync.

Key constraint: tokens are unavailable while the device is locked (screen off). Apps that require background token refresh must use `kSecAttrAccessibleAfterFirstUnlock`; this requires a custom `StorageConfiguration` passed to `OidcClientConfig`.

### Universal links for redirect URI

For a redirect URI of the form `https://app.example.com/callback`:
- An Apple App Site Association (AASA) file must be hosted at `https://app.example.com/.well-known/apple-app-site-association`
- The app must have the Associated Domains entitlement: `applinks:app.example.com`
- `onOpenURL` (SwiftUI) or `application(_:continue:restorationHandler:)` (UIKit) must forward the URL to `oidcClient.handleRedirect(url:)`

For custom-scheme URIs (`myapp://callback`): no AASA file required; register the scheme in `Info.plist` under `CFBundleURLTypes`.

### Biometric authentication

PingOne push approval and FIDO2 assertions may require biometric prompts. The app needs `NSFaceIDUsageDescription` in `Info.plist` for Face ID. Absence of this key causes a crash at runtime on Face ID–capable devices — it does not degrade gracefully.

### Swift 6 concurrency notes

The Ping iOS SDK is compatible with Swift 6's strict concurrency model. Key constraints:

- All SDK callbacks and `async` methods must be called from the `@MainActor` context or a structured concurrency task. Calling from a background thread without proper actor isolation produces Swift 6 compiler errors.
- `OidcClient` and journey/DaVinci client methods are `async` — use `await` inside `Task { }` blocks when calling from SwiftUI `.onAppear` or button actions.
- The SDK's `@MainActor`-annotated types must not be used from non-isolated closures. If integrating with Combine or legacy UIKit callbacks, use `Task { @MainActor in ... }` to hop to the main actor.

---

## Feature comparison table

| Feature | Android | iOS |
|---|---|---|
| SDK distribution | Maven Central / Ping Maven repo | Swift Package Manager / CocoaPods |
| Auth flow | `PingOne.startAuthentication(activity)` | `oidcClient.authorize()` async |
| PKCE | Auto-generated by SDK | Auto-generated by SDK |
| Token storage | `EncryptedSharedPreferences` (Keystore) | Keychain (`kSecAttrAccessibleWhenUnlockedThisDeviceOnly`) |
| Redirect URI type | Custom scheme (intent filter) | Custom scheme or universal link |
| Push MFA | FCM (`FirebaseMessagingService`) | APNs (`UNUserNotificationCenter`) |
| Social login | `externalidp` module | `PingExternalIdP` module |
| Biometric | Android Biometric API (via `binding` module) | Face ID / Touch ID (via `NSFaceIDUsageDescription`) |
| FIDO2 / passkeys | `fido` module, Android 9+ | `PingFido` module (iOS 16+, passkey API) |
| DaVinci collectors | `davinci` module, Jetpack Compose | `PingDavinci` module, SwiftUI |
| Journey callbacks | `journey` module | `PingJourney` module |

## DaVinci collector types (Android and iOS)

When driving a DaVinci flow with the `davinci` / `PingDavinci` module, the SDK delivers **collectors** per step. Render by type:

| Collector type | Interaction | Notes |
|---|---|---|
| `TextCollector` | Text input | Username, email, any free-text |
| `PasswordCollector` | Masked password input | |
| `SubmitCollector` | Submit / Continue button | Advances the flow |
| `FlowCollector` | Secondary action button | "Forgot password", "Register" — triggers a sub-flow |
| `SelectCollector` | Dropdown or radio group | |
| `MultiSelectCollector` | Multi-select list | |
| `LabelCollector` | Display-only text | No user input |
| `QrCodeCollector` | QR code display | Flow waits for external device scan |
| `SsoCollector` / `IdpCollector` | Social / external IdP button | Google, Apple, Facebook; triggers IdP redirect |
| `PhoneCollector` | Phone input with country picker | |

Auto-advancing (no user action): `DeviceAuthenticatorCollector` (biometric/passkey challenge), `ProtectCollector` (Protect signals — silent).

**Pattern:** iterate `node.collectors`, render by type, collect input, call `node.next()`.

---

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `redirect_uri_mismatch` at login | URI sent by app does not match registered URI exactly | Verify scheme, host, and path match precisely — no trailing slash differences |
| Token refresh fails after app background | `offline_access` scope not included; token storage accessibility too strict | Add `offline_access` to scopes; on iOS check `kSecAttrAccessible` setting |
| Biometric auth crash on iOS | `NSFaceIDUsageDescription` missing from `Info.plist` | Add the usage description key |
| Push notifications not received | FCM/APNs not configured; device registration skipped | Complete `PingOne.registerDevice()` / APNs flow; verify FCM project setup |
| Android Keystore error after OS upgrade | Keystore key invalidated post-biometric change | Handle `KeyPermanentlyInvalidatedException`; prompt user to re-authenticate |
| SDK not resolving in Gradle | Ping Maven repo not declared | Add `maven { url = uri("https://maven.pingidentity.com/repository/releases/") }` |

## PingOne MFA SDK — push MFA and custom AMR

For apps using the PingOne MFA SDK (distinct from the orchestration SDK), the key integration point for push MFA is the `approve()` method on Android.

**Custom AMR strings** can be passed to `approve()` to convey the authentication method used for the biometric-gated approval:

| Custom AMR | Meaning |
|---|---|
| `face` | Face biometric used to approve the push |
| `pin` | Device PIN used to approve |
| `ftp` | Fingerprint used to approve |

These strings appear in the `amr` claim of the resulting token, allowing the relying party to enforce assurance requirements (e.g., reject `pin` for high-value transactions and require `face`).

**Pairing key prerequisite:** The device must be bound to the PingOne user via a pairing key before push MFA can be initiated. Generate the pairing key server-side via the PingOne MFA API and deliver it to the app for the initial device registration step. See `ping-universal-services/references/curated/mfa-configuration.md`.

## Migration path: ForgeRock SDK → Ping SDK

For full Android, iOS, and JavaScript breaking-change tables and migration strategy, see `references/curated/integration-troubleshooting-basics.md` — Failure mode 6.

## Prerequisites

- Application record created in PingOne, AIC, or PingAM with the correct redirect URI registered (use `ping-foundation` to complete this step)
- Journey or DaVinci flow designed and tested end-to-end (use `ping-orchestration`)
- Android: API level 23+, Kotlin 1.8+, Gradle 8+
- iOS: iOS 14+, Swift 5.7+, Xcode 14+
- For push MFA: FCM project (Android) or APNs certificate/key (iOS) configured in the Ping admin console

## Common variants

| Variant | Note |
|---|---|
| PingOne target | Use `davinci` / `PingDavinci` modules; flows are DaVinci-based; discovery endpoint is `https://auth.pingone.com/<envId>/as/.well-known/openid-configuration` |
| AIC target | Use `journey` / `PingJourney` modules; flows are Journey-based; discovery endpoint is `https://<tenant>.forgeblocks.com/am/oauth2/realms/<realm>/.well-known/openid-configuration` |
| PingFederate on-prem | OIDC only (no Journey/DaVinci modules); use `oidc` / `PingOidc` module; discovery endpoint is `https://<pf-host>:<port>/.well-known/openid-configuration` |
| Embedded webview | Not recommended — hosted login in a system browser (Chrome Custom Tab / ASWebAuthenticationSession) is required for security; custom scheme redirect URI must be registered |

## Related references

- `references/curated/app-integration-overview.md` — SDK landscape and integration lifecycle
- `references/curated/web-integration-basics.md` — JavaScript and browser-based auth flows
- `references/curated/integration-troubleshooting-basics.md` — Failure mode diagnosis and migration guide

## Source

[PingOne Native SDK Documentation](https://docs.pingidentity.com/pingone/native-sdks/p1_native_sdks_landing.html)
