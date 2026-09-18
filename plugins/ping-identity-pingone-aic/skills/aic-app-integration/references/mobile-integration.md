# AIC — Mobile Integration (Android and iOS Journey Modules)

Integration guide for Android (Kotlin) and iOS (Swift) apps authenticating through PingOne Advanced Identity Cloud (AIC) journeys using the PingOne Native SDK Journey modules.

## Scope

**Covers:** Android and iOS SDK import, initialization, OIDC flow, token storage, redirect handling, push MFA, and Journey callback rendering.
**Does NOT cover:** Journey or tree authoring or node sequencing — journey-design documentation. Platform-side application-agent registration — tenant administration. PingOne DaVinci collector rendering — PingOne tooling and documentation. Web/React integration — `references/web-integration.md`. Failure diagnosis — `references/troubleshooting.md`.

---

## Android SDK integration

### SDK import

Gradle (Kotlin DSL):

```kotlin
dependencies {
    implementation("com.pingidentity.sdks:oidc:<version>")
    implementation("com.pingidentity.sdks:journey:<version>")   // Journey callbacks
    implementation("com.pingidentity.sdks:fido:<version>")      // FIDO2 / passkeys
    implementation("com.pingidentity.sdks:protect:<version>")   // Risk signals
    implementation("com.pingidentity.sdks:push:<version>")      // Push MFA
    implementation("com.pingidentity.sdks:externalidp:<version>") // Social login
}
```

The SDK is hosted on Maven Central and on the Ping Identity Maven repository (`maven.pingidentity.com`). Add both repositories to `settings.gradle.kts` if Maven Central is not resolving the artifact.

### Initialization

Initialize once per process lifetime, typically in `Application.onCreate()`:

```kotlin
PingOne.init(context) {
    oidcConfig {
        clientId = "<client-id>"
        discoveryEndpoint = "https://<tenant-host>/am/oauth2/realms/<realm>/.well-known/openid-configuration"
        redirectUri = "myapp://callback"
        scopes = listOf("openid", "profile", "offline_access")
    }
    logger {
        level = LogLevel.DEBUG
    }
}
```

Constraint: `PingOne.init()` must complete before any auth call. Calling journey entry points before init completes throws `PingOneNotInitializedException`.

### Journey callbacks (Android)

The `journey` module advances AIC journeys and delivers typed callbacks per node. Render by type, collect input, and submit to advance:

**Pattern:** iterate the node's callbacks, render each by type, collect user input, then call the node's next() to advance the journey.

### Token storage — Android Keystore

The SDK stores tokens in `EncryptedSharedPreferences` backed by Android Keystore. No plaintext token storage occurs by default.

Key constraint: the encryption key is tied to the device. Tokens are not portable across devices or backups. Do not add `android:allowBackup="true"` for credential data; use `android:fullBackupContent` exclude rules if general backup is needed.

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

The scheme and host must exactly match the `redirectUri` passed to `oidcConfig` and the value registered on the AIC application agent. A mismatch causes `redirect_uri_mismatch` from the authorization server.

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
| `PingJourney` | AIC Journey-based flows |
| `PingStorage` | Keychain-backed token storage (included by default) |
| `PingExternalIdP` | Social login (Google, Apple, Facebook) |
| `PingProtect` | Risk signals |
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
    discoveryEndpoint: "https://<tenant-host>/am/oauth2/realms/<realm>/.well-known/openid-configuration",
    redirectUri: "myapp://callback",
    scopes: ["openid", "profile", "offline_access"]
)
let oidcClient = OidcClient(config: config)
```

### Journey callbacks (iOS)

The `PingJourney` module advances AIC journeys and delivers typed callbacks per node in SwiftUI or UIKit. The journey client methods are `async` — use `await` inside `Task { }` blocks when calling from SwiftUI `.onAppear` or button actions.

### Token storage — Keychain

`PingStorage` persists tokens in the iOS Keychain with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`. This attribute ties the token to the device and excludes it from iCloud Keychain sync.

Key constraint: tokens are unavailable while the device is locked (screen off). Apps that require background token refresh must use `kSecAttrAccessibleAfterFirstUnlock`; this requires a custom `StorageConfiguration` passed to `OidcClientConfig`.

### Universal links for redirect URI

For a redirect URI of the form `https://app.example.com/callback`:
- An Apple App Site Association (AASA) file must be hosted at `https://app.example.com/.well-known/apple-app-site-association`
- The app must have the Associated Domains entitlement: `applinks:app.example.com`
- `onOpenURL` (SwiftUI) or `application(_:continue:restorationHandler:)` (UIKit) must forward the URL to the OIDC client's redirect handler

For custom-scheme URIs (`myapp://callback`): no AASA file required; register the scheme in `Info.plist` under `CFBundleURLTypes`.

### Biometric authentication

Push approval and FIDO2 assertions may require biometric prompts. The app needs `NSFaceIDUsageDescription` in `Info.plist` for Face ID. Absence of this key causes a runtime crash on Face ID–capable devices — it does not degrade gracefully.

### Swift 6 concurrency notes

The Ping iOS SDK is compatible with Swift 6's strict concurrency model. Key constraints:

- All SDK callbacks and `async` methods must be called from the `@MainActor` context or a structured concurrency task. Calling from a background thread without proper actor isolation produces Swift 6 compiler errors.
- Journey and OIDC client methods are `async` — use `await` inside `Task { }` blocks.
- The SDK's `@MainActor`-annotated types must not be used from non-isolated closures. If integrating with Combine or legacy UIKit callbacks, use `Task { @MainActor in ... }` to hop to the main actor.

---

## Feature comparison table

| Feature | Android | iOS |
|---|---|---|
| SDK distribution | Maven Central / Ping Maven repo | Swift Package Manager / CocoaPods |
| Auth flow | Journey node iteration | Journey client async calls |
| PKCE | Auto-generated by SDK | Auto-generated by SDK |
| Token storage | `EncryptedSharedPreferences` (Keystore) | Keychain (`kSecAttrAccessibleWhenUnlockedThisDeviceOnly`) |
| Redirect URI type | Custom scheme (intent filter) | Custom scheme or universal link |
| Push MFA | FCM (`FirebaseMessagingService`) | APNs (`UNUserNotificationCenter`) |
| Social login | `externalidp` module | `PingExternalIdP` module |
| Biometric | Android Biometric API (via `binding` module) | Face ID / Touch ID (via `NSFaceIDUsageDescription`) |
| FIDO2 / passkeys | `fido` module, Android 9+ | `PingFido` module (iOS 16+, passkey API) |
| Journey callbacks | `journey` module | `PingJourney` module |

## Prerequisites

- Application agent created in the tenant realm with the correct redirect URI registered (tenant prerequisite)
- Journey designed and tested end-to-end in the realm (journey prerequisite)
- AM services configured for the journey's dependent features (push, OATH, WebAuthn, social, device profiles)
- Android: API level 23+, Kotlin 1.8+, Gradle 8+
- iOS: iOS 14+, Swift 5.7+, Xcode 14+

## Common variants

| Variant | Note |
|---|---|
| AIC realm discovery | `https://<tenant-host>/am/oauth2/realms/<realm>/.well-known/openid-configuration` — verify the tenant FQDN and realm path against the target tenant |
| Self-managed PingAM | Same Journey modules; point discovery at the PingAM deployment; validate node availability against PingAM documentation |
| Embedded webview | Not recommended — hosted login in a system browser (Chrome Custom Tab / ASWebAuthenticationSession) is required for security; custom scheme redirect URI must be registered |

## Source

- [Ping SDKs](https://developer.pingidentity.com/orchsdks/index.md)
- [PingOne Advanced Identity Cloud documentation](https://docs.pingidentity.com/pingoneaic/home.md)
