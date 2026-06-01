---
title: "Common Starting Patterns"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate"]
capabilities: ["quickstart"]
audience: ["admin", "developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-05-29"
---

# Common Starting Patterns

The most frequent starting scenarios and which skills and platforms to use for each.

## Scope

Covers: the top 6 starting patterns, required configuration fields, grant type guidance, known gotchas, and routing to the next skill.
Does NOT cover: step-by-step configuration — see `ping-foundation` or the relevant capability skill.

---

## Prerequisites

Before following any of these patterns:

- Active Ping Identity subscription or trial (see `plugins/ping-identity/skills/ping-quickstart/references/curated/choose-the-right-ping-platform.md` for platform selection).
- Admin role on the target platform (Environment Admin for PingOne MT; Tenant Admin for PingOne ST; server admin for Software Suite).
- Platform decided — if not yet decided, start with the platform decision guide above.
- For SDK patterns (Pattern 4): a registered application client with appropriate grant type and redirect URI.

---

## Pattern 1: Employee SSO to cloud apps

**Platform:** PingOne MT or PingFederate
**Skill:** `ping-foundation` → `pingone-mt` or `ping-software/pingfederate`
**Grant type:** SAML 2.0 for legacy apps; OIDC Authorization Code for modern apps; WS-Fed if required by Office 365/Azure AD.

Required configuration fields:
| Field | PingOne MT | PingFederate |
|---|---|---|
| App type | SAML App or OIDC | SP Connection (SAML) or OAuth Client |
| Assertion consumer service / Redirect URI | Required; exact match | Required in SP connection |
| Subject / NameID | Employee email or UPN | Mapped from identity store |
| Attribute mapping | Email, Groups | Adapter contract attributes |
| Session policy | Sign-on policy with MFA | Authentication policy contract |

Known gotchas:
- Redirect URI must be an exact match including trailing slash; mismatches cause silent 401 errors.
- For Office 365: NameID format must be `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` or `unspecified`; persistent format will break login.
- PingFederate requires a valid PKIX certificate on SP connections; self-signed certs are rejected in production.

---

## Pattern 2: Customer registration and login (CIAM)

**Platform:** PingOne ST (journey-based) or PingOne MT + DaVinci
**Skill:** `ping-foundation` for setup; `ping-orchestration` for flow design
**Grant type:** Authorization Code + PKCE for web and mobile clients; avoid implicit grant.

Required configuration fields:
| Field | PingOne ST | PingOne MT + DaVinci |
|---|---|---|
| Realm | `alpha` (consumer) | N/A (environment-level) |
| Registration journey / flow | Create or import tree | DaVinci flow with registration form |
| Identity store | PingDirectory or built-in datastore | PingOne Directory |
| Self-service | Enable password reset node in tree | DaVinci self-service flow |
| Social login | Social auth node + provider | DaVinci social connector |

Known gotchas:
- PingOne ST: if the identity store uses PingDirectory, confirm schema extensions are deployed before enabling registration; missing attributes cause silent user creation failures.
- PingOne MT + DaVinci: token exchange from DaVinci flow to PingOne OIDC requires a DaVinci connector configured with the correct environment ID and client credentials.
- PKCE is required for public clients; omitting it results in `invalid_grant` errors from modern library versions.

---

## Pattern 3: Add MFA to an existing deployment

**Platform:** Any — PingOne MT, PingOne ST, or PingFederate + PingID
**Skill:** `ping-foundation` for MFA policy setup; `ping-universal-services` for PingOne Protect/risk-based step-up

Required configuration fields:
| Field | PingOne MT | PingOne ST | PingFederate + PingID |
|---|---|---|---|
| MFA policy | Sign-on policy MFA requirement | Authentication tree MFA node | PingID adapter config |
| MFA methods | Email OTP, TOTP, FIDO2 | TOTP, push, FIDO2 nodes | PingID mobile push, TOTP |
| Step-up trigger | Sign-on policy risk threshold | Risk evaluation node | Policy contract condition |
| Bypass / recovery | Admin override in console | Recovery codes node | PingID admin console |

Known gotchas:
- PingOne MT: MFA policy must be attached to the sign-on policy that is assigned to the app; a policy not assigned to an app has no effect.
- PingOne ST: the TOTP node requires the user to have a `totpSecretKey` attribute in the identity store; ensure the schema is extended before enabling.
- PingFederate + PingID: the PingID adapter requires outbound internet access from PingFederate to `idpxnyl3m7.execute-api.us-east-1.amazonaws.com`; block it and MFA silently fails.

---

## Pattern 4: Protect an API or web app

**Platform:** PingAccess (Software Suite) or PingOne MT + app integration
**Skill:** `ping-foundation` → `ping-software/pingaccess`; or `ping-app-integration` for SDK patterns
**Grant type:** Authorization Code for user-facing apps; Client Credentials for service-to-service; JWT Bearer for delegated access.

Required configuration fields for PingAccess:
| Field | Value guidance |
|---|---|
| Site | Backend target URL; include base path if app is not at root |
| Application | Virtual host + context root; maps to the site |
| Web session | Cookie settings, idle timeout, max session lifetime |
| Token provider | Must point to PingFederate AS or PingOne MT token endpoint |
| Resource policy | Rules to allow/deny access; apply at application or resource level |

Known gotchas:
- PingAccess requires valid token introspection or JWT validation; misconfigured token provider causes 401 on every request.
- Web session cookies are domain-scoped; wildcard domain config is needed for multi-subdomain apps.
- For PingOne MT + SDK pattern: use the Ping Android/iOS SDK or JavaScript SDK via `ping-app-integration` — do not inline token handling.

---

## Pattern 5: Migrate from ForgeRock / legacy deployment

**Platform:** PingOne ST
**Skill:** `ping-foundation` → `pingone-st`

Required configuration fields:
| Field | Value guidance |
|---|---|
| Target realm | `alpha` or `bravo` depending on use case |
| Journey import | Export tree JSON from ForgeRock AM; import via PingOne ST admin REST API |
| Identity store migration | Use PingDirectory LDIF import or SCIM bulk import |
| OAuth clients | Re-register; client IDs and secrets do not migrate automatically |
| Social providers | Re-configure; refresh tokens from old provider are invalid on new tenant |

Known gotchas:
- Custom authentication nodes (scripted or Java) must be rewritten as PingOne ST custom nodes; they do not import directly.
- LDIF imports retain password hashes only if the hash algorithm is supported by PingDirectory; bcrypt hashes from ForgeRock IDM may require re-hash on first login.
- Users will need to re-register MFA devices unless the TOTP seed is migrated manually via the `totpSecretKey` attribute.

---

## Pattern 6: Add identity verification (KYC)

**Platform:** PingOne MT + PingOne Verify
**Skill:** `ping-universal-services` → `verify` branch

Required configuration fields:
| Field | Value guidance |
|---|---|
| PingOne Verify policy | Create in PingOne console → Verify → Policies; choose document types accepted |
| Document types | Passport, driver's license, national ID; configure per country |
| Liveness check | Enable face comparison against document photo |
| Verification trigger | Invoke from DaVinci flow (Verify connector) or PingOne ST journey (Verify node) |
| Result handling | Map `APPROVED`/`DECLINED`/`REQUIRES_INSPECTION` to next step in flow |

Known gotchas:
- PingOne Verify requires the end user to have camera access; ensure the HTTPS origin is correct or camera permission is denied by the browser.
- `REQUIRES_INSPECTION` results require a human review queue if manual fallback is needed; no automatic approval.
- Verify connector in DaVinci must have the PingOne Verify worker app client ID/secret; use a dedicated worker — do not reuse the main app credential.

---

## Common variants

### Greenfield vs brownfield per pattern

- Pattern 1 (Employee SSO): Greenfield — new PingOne MT environment from scratch. Brownfield — add an SP connection to existing PingFederate; no existing apps need to change.
- Pattern 2 (CIAM): Greenfield — new PingOne ST tenant with `alpha` realm. Brownfield — import existing user accounts via SCIM; re-register OAuth clients.
- Pattern 3 (MFA): Always brownfield — MFA is added to an existing authentication policy or journey.
- Pattern 4 (API protection): Greenfield — deploy PingAccess and configure from scratch. Brownfield — insert PingAccess in front of existing APIs; configure reverse proxy routing.
- Pattern 5 (Migration): Always brownfield — existing ForgeRock or legacy deployment.
- Pattern 6 (Verify): Always additive — PingOne Verify is inserted into an existing flow.

### Single-environment vs multi-environment

- Development/QA/Production environments in PingOne MT: separate PingOne environments per stage; OAuth client IDs differ per stage — do not share.
- PingOne ST multi-stage: separate tenant instances per stage; use Config Manager or Ping DevOps tooling to promote configuration.
- Ping Software Suite multi-stage: separate PingFederate cluster per stage; connections and adapters can be exported as XML and imported.

### Trial license constraints

- PingOne MT trial: rate-limited API calls; no SLA; environments expire after 30 days unless renewed.
- PingOne ST trial: limited number of users, journeys, and API calls; social connectors may require production keys.
- Ping Software Suite evaluation: time-limited license file; full functionality but expires; obtain production license before go-live.

---

## Related references

- `plugins/ping-identity/skills/ping-quickstart/references/curated/getting-started-overview.md`
- `plugins/ping-identity/skills/ping-quickstart/references/curated/choose-the-right-ping-platform.md`

## Source

[Ping Identity Solution Guides](https://docs.pingidentity.com/solution-guides/)
