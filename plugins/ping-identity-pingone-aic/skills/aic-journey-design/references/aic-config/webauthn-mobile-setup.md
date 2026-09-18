# AIC — WebAuthn / Passkeys Mobile Prerequisites (Android & iOS)

AIC server-side setup required before `WebAuthnRegistrationNode` and `WebAuthnAuthenticationNode` will work in native Android and iOS apps.

## Scope

**Covers:** Android Digital Asset Links, Apple App Site Association, and CORS policy — all via AIC REST APIs.
**Does NOT cover:** SDK-side callback wiring (client-side app integration), web WebAuthn, or journey design patterns (`passkeys-and-passwordless.md`).

---

## Required steps

All three must be in place before the journey will work. Do not skip CORS — it is always required for native apps.

| Step | What to configure | REST endpoint |
|---|---|---|
| 1 | Android Digital Asset Links (`assetlinks.json`) | `PUT /openidm/config/fidc/assetlinks.<domain>` |
| 2 | Apple App Site Association | `PUT /openidm/config/fidc/apple-app-site-association.<domain>` |
| 3 | CORS — allow the app's origin in `CorsService` | GET current config → merge origin → `PUT /openidm/config/services/globalAmService` |

---

## Step 1 — Android Asset Links

**Do:** PUT the full `assetlinks.json` content — each PUT replaces the existing file.
**Do:** Include one object per app. For debug builds, add a second object with the debug certificate fingerprint.
**Don't:** Omit `delegate_permission/common.handle_all_urls` — without it the OS will not honour the link.
**Get the fingerprint:** `keytool -list -v -keystore release.jks -alias <alias> | grep SHA256`

```json
{
  "data": [
    {
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.example.myapp",
        "sha256_cert_fingerprints": ["AA:BB:CC:..."]
      }
    }
  ]
}
```

**Verify:** `GET https://<domain>/.well-known/assetlinks.json` must return content unauthenticated.

---

## Step 2 — Apple App Site Association

**Do:** Include both `applinks` and `webcredentials` — `webcredentials` is required for passkeys, `applinks` for Universal Links.
**Do:** Use `<TeamID>.<BundleID>` format for `appIDs` (visible in Xcode → Signing & Capabilities).
**Don't:** Upload to only the primary domain if a custom domain is configured — upload to every domain used as `rpId`.

```json
{
  "data": {
    "applinks": {
      "details": [{ "appIDs": ["ABCDE12345.com.example.myapp"], "components": [{ "/": "/myapp/*" }] }]
    },
    "webcredentials": {
      "apps": ["ABCDE12345.com.example.myapp"]
    }
  }
}
```

**Verify:** `GET https://<domain>/.well-known/apple-app-site-association` must return content unauthenticated.

---

## Step 3 — CORS

**Do:** GET the current `CorsService` config first, merge the new origin into `acceptedOrigins`, then PUT the full updated config back — do not overwrite the entire service config blindly.
**Don't:** Assume any origin is allowed by default — native apps always require an explicit entry.

```json
{ "CorsService": { "acceptedOrigins": ["https://app.example.com"] } }
```

---

## Journey node settings

**Do:** Set `rpId` to the exact AIC tenant hostname (or custom domain) used in Steps 1–2 — on both registration and authentication nodes.
**Don't:** Mismatch `rpId` between registration and authentication — it causes `NotAllowedError` on assertion.

| Node | Key settings |
|---|---|
| `WebAuthnRegistrationNode` | `rpId` = domain from Steps 1–2; `attachmentType` = `platform`; `residentKey` = `required` or `preferred` |
| `WebAuthnAuthenticationNode` | `rpId` = same as registration; `userVerification` = same as registration |

---

## Related references

- `references/passkey-journeys.md` — passkey journey design patterns
- `references/nodes/mfa-nodes.md` — WebAuthn node config and error handling
- `references/journey-use-cases/passwordless-mfa-registration.md` — MFA device registration journey structure

## Source

- [AIC — Upload Android assetlinks.json](https://docs.pingidentity.com/pingoneaic/end-user/upload-android-assetlinks.html)
- [AIC — Upload iOS Apple App Site Association](https://docs.pingidentity.com/pingoneaic/end-user/upload-ios-apple-app-site-association.html)
