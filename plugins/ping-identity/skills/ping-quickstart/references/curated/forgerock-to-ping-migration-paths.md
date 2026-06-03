---
title: "ForgeRock to Ping Migration Paths"
product_family: cross-platform
products: ["pingone", "pingone-aic", "pingfederate"]
capabilities: ["quickstart"]
services: []
audience: ["developer", "admin", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-01"
slug: https://developer.pingidentity.com/orchsdks/journey/migration.html
---

# ForgeRock to Ping Migration Paths

Orientation guide covering the three distinct migration dimensions when moving from ForgeRock to Ping Identity, with routing rules, key constraints, and the correct skill for each track.

## Scope

Covers:
- Three migration dimensions: (A) SDK code migration, (B) self-managed ForgeRock AM/IDM → PingOne AIC, (C) PingFederate → PingOne MT via Cloud Acceleration Toolset
- Legacy P14E → PingOne MT migration status
- Routing guidance for each dimension to the right downstream skill
- Key constraints and gotchas per dimension

Does NOT cover:
- Step-by-step node-by-node Journey migration — see `ping-orchestration`
- SDK implementation details and callback/collector rendering — see `ping-app-integration`
- Okta or Auth0 migration (no public Ping migration guide or toolset exists — see routing note below)
- Per-environment Journey tree exports or import procedures

---

## The three migration dimensions

| Dimension | What moves | Who drives it | Primary skill | Docs entry point |
|---|---|---|---|---|
| A — SDK code | Mobile/web app authentication code from ForgeRock SDK to Ping Orchestration SDK | Developer | `ping-app-integration` | [SDK migration](https://developer.pingidentity.com/orchsdks/journey/migration.html) |
| B — Server/SaaS | Self-managed ForgeRock AM/IDM tenant → PingOne Advanced Identity Cloud (AIC) | Architect + PS | `ping-foundation` | [AIC planning & migration](https://docs.pingidentity.com/pingoneaic/planning/plan-identity-cloud.html) |
| C — PingFederate → PingOne MT | PingFederate apps and policies → PingOne MT via Cloud Acceleration Toolset | Admin + Architect | `ping-foundation` | [Cloud Acceleration Toolset](https://docs.pingidentity.com/pingone/migration-tools/p1_cloud_acceleration_toolset.html) |

These dimensions are independent. A single engagement may involve all three, or only one.

---

## Dimension A — SDK code migration

Applies when your mobile or web app uses `FRAuth`, `FRSession`, `@forgerock/javascript-sdk`, or any `forgerock-android-sdk` / `forgerock-ios-sdk` import.

ForgeRock SDK end-of-maintenance date: **15 April 2028**. Plan migration before that date.

### Platform migration table

| Platform | Old package | New package(s) | Key breaking changes | Minimum version |
|---|---|---|---|---|
| Android (Kotlin) | `forgerock-android-sdk` / `FRSession` | `com.pingidentity.sdks:android` (journey, davinci, oidc modules) | Kotlin Coroutines replaces callbacks; `FRSession` → `SuccessNode` + Journey API | Android API 23+ |
| iOS (Swift) | `forgerock-ios-sdk` / `FRAuth` | `Ping/ping-ios-sdk` (`PingJourney`, `PingDavinci`, `PingOidc` modules) | Typed properties replace callback model; `FRAuth` → `PingOrchestrate`/`PingJourney` | iOS 16+, Swift 6.0+ |
| JavaScript / TypeScript | `@forgerock/javascript-sdk` | `@forgerock/journey-client` + `@forgerock/oidc-client` | Async `init()` replaces synchronous config; instance-based API replaces static calls | Node 18+, modern browsers |

### AI-assisted migration guides

Each SDK repo ships a `MIGRATION.md` with AI-assisted step-by-step guidance:
- `github.com/ForgeRock/ping-android-sdk` → `MIGRATION.md`
- `github.com/ForgeRock/ping-ios-sdk` → `MIGRATION.md`
- `github.com/ForgeRock/ping-javascript-sdk` → `MIGRATION.md`

### Key API shifts to communicate to developers

- **Async init**: All three SDKs now require `await` on startup configuration — static sync patterns will break.
- **Instance-based API**: JavaScript SDK is no longer a singleton; each module must be instantiated.
- **Kotlin Coroutines**: Android callback chains (`FRCallback`) are replaced by `suspend` functions and `Flow` collectors.
- **Typed properties**: iOS callback fields (`getString()`, `setValue()`) are replaced by typed Swift properties on collector types.

Deep implementation details and code samples live in `ping-app-integration` (Orchestration SDK skill). Route there after orientation.

---

## Dimension B — Server/SaaS migration (self-managed ForgeRock AM/IDM → AIC)

Applies when a customer self-hosts ForgeRock Access Management or Identity Management and wants to move to PingOne Advanced Identity Cloud (AIC).

### Four-phase S2S model

| Phase | Name | Key activities |
|---|---|---|
| 1 | Assess & Plan | Inventory realms, journeys, scripts, connectors; map to AIC equivalents; identify blockers |
| 2 | Transform | Re-author journeys in AIC; migrate user store; test parity |
| 3 | Adopt & Refine | Parallel-run; traffic switching; performance and security validation |
| 4 | Enable | Cutover; decommission self-managed systems; post-go-live tuning |

### PingGateway key-sharing route

PingGateway provides an in-place migration option: it sits in front of the existing ForgeRock AM instance and enables gradual traffic shifting to AIC without a domain change.

**Constraints — all three must hold for PingGateway route to be viable:**
- Customer has ≤ 2 realms (AIC hard limit: Alpha + Bravo realms per tenant)
- Signing and encryption keys are exportable from the existing AM instance
- Single FQDN entry point (multi-domain configurations require additional work)

**PingGateway route enables:** session continuity, gradual cutover, rollback capability during migration.

**PingGateway route cannot:** migrate more than 2 realm configurations, merge identity stores across tenants, or resolve scripted policy logic that has no AIC equivalent.

AIC environment limits to communicate early: Sandbox (max 10k identities, no HA), Dev (max 10k, in pipeline), UAT and Staging (HA, in pipeline), Production (HA, SLA). AIC FQDN patterns: Production `openam-<base>-<region>.id.forgerock.io`; Sandbox `openam-<sandbox>-<region>.forgeblocks.com`.

---

## Dimension C — PingFederate → PingOne MT (Cloud Acceleration Toolset)

Applies when a customer runs PingFederate on-premises and wants to move federated app connections to PingOne MT.

### Prerequisites

All three must be in place before the toolset can be used:

| Requirement | Detail |
|---|---|
| PingFederate version | 10.3 or later |
| PingOne MT capabilities | SSO license + DaVinci enabled in the target environment |
| Worker App permissions | Worker App must have the Environment Admin role in the target PingOne environment |

### App category classifications

The toolset classifies each PingFederate application into one of three categories:

| Category | Meaning | Action |
|---|---|---|
| Migratable | App can be moved as-is via the toolset | Use toolset migration workflow |
| Change Required | App needs configuration adjustments before migration | Remediate, then migrate |
| Reimagine | App cannot be auto-migrated; fundamental redesign needed | Manual re-implementation in PingOne/DaVinci |

The toolset is accessible from within the PingOne admin console at `console.pingone.com` under the Migration Tools section. It does not require a separate download.

---

## P14E → PingOne MT migration (legacy)

Applies when a customer uses PingOne for Enterprise (P14E, `admin.pingone.com`) and wants to move to PingOne MT (`console.pingone.com`).

**Status:** The legacy PingOne Migration Tool was **deprecated August 2023** and is no longer available.

**Current path:** DaVinci JIT (Just-In-Time) password sync flow. On first login to PingOne MT, the DaVinci flow authenticates the user against the P14E directory and provisions the identity into PingOne MT transparently.

**Docs status:** Full documentation for this path is tracked under DOCS-11270 (in progress as of 2026-06-01). Check `docs.pingidentity.com` for updates or engage Professional Services.

P14E variant identification: check top nav — standard P14E shows Dashboard/Apps/Users/Setup/Account; MSP variant adds a Customers menu; SSO for SaaS Apps adds Customer Connections; SSO for SaaS Apps with Managed Accounts adds both Customer Connections and Managed Accounts.

---

## Routing note for Okta / Auth0 migration

No public Ping migration guide or automated toolset exists for migrating from Okta or Auth0 to Ping Identity. Do not fabricate documentation.

If a customer asks about this path:
- Direct them to their Ping Account Executive or open a support case
- Partner tooling (e.g., identity migration specialists) exists but is not part of Ping's public documentation
- Do not route to any Ping skill as if authoritative guidance exists — acknowledge the gap

---

## Decision rule — which dimension applies

| Your situation | Dimension to use |
|---|---|
| App code uses `FRAuth`, `FRSession`, `@forgerock/javascript-sdk` | A — SDK code migration |
| Running self-managed ForgeRock AM or IDM on-premises or in a private cloud | B — Server/SaaS migration (AM/IDM → AIC) |
| Running PingFederate and want to move app connections to PingOne MT SaaS | C — Cloud Acceleration Toolset (PF → PingOne MT) |
| Using PingOne for Enterprise (admin.pingone.com) and want PingOne MT | P14E → PingOne MT (legacy path, DaVinci JIT) |
| Using Okta or Auth0 and want to move to Ping | No public guide — engage AE or support |
| All of the above simultaneously | Start with B (server migration unlocks the new tenant), then A (SDK), then C (federated apps) |

---

## Prerequisites

- Identify which dimension(s) apply before engaging any migration resource
- For Dimension A: audit all SDK imports across mobile and web codebases; confirm iOS 16+ and Swift 6.0+ target minimums
- For Dimension B: inventory all realms, journeys, and scripts in the self-managed AM instance before scoping PingGateway viability
- For Dimension C: verify PingFederate version is 10.3+; confirm PingOne MT has SSO + DaVinci enabled; create the Worker App with Environment Admin role before running the toolset
- ForgeRock SDK EOL is 15 April 2028 — use this date for customer urgency conversations

## Common variants

- **Greenfield + SDK migration only**: Customer keeps their existing identity server but re-writes mobile/web apps using Ping Orchestration SDK. Only Dimension A applies.
- **Full platform consolidation**: Customer migrates server, re-writes SDKs, and moves PingFederate apps simultaneously. All three dimensions apply; recommended sequencing is B → A → C.
- **PingGateway-gated rollout**: Customer uses PingGateway to run ForgeRock AM and AIC in parallel during Dimension B, enabling zero-downtime cutover.
- **Inherited AIC tenant**: Customer already has AIC provisioned (common post-ForgeRock acquisition consolidation); only SDK migration (Dimension A) is needed.

## Related references

- `plugins/ping-identity/skills/ping-app-integration/` — SDK implementation depth for Dimension A
- `plugins/ping-identity/skills/ping-orchestration/` — Journey and DaVinci flow implementation after server migration
- `plugins/ping-identity/skills/ping-foundation/` — AIC environment setup and PingFederate configuration for Dimensions B and C
- `plugins/ping-identity/skills/ping-quickstart/references/curated/getting-started-overview.md` — platform selection before committing to a migration path

## Source

- SDK migration: https://developer.pingidentity.com/orchsdks/journey/migration.html
- AIC planning and migration: https://docs.pingidentity.com/pingoneaic/planning/plan-identity-cloud.html
- Cloud Acceleration Toolset: https://docs.pingidentity.com/pingone/migration-tools/p1_cloud_acceleration_toolset.html
- AIC environments: https://docs.pingidentity.com/pingoneaic/tenants/environments.html
- AIC realms: https://docs.pingidentity.com/pingoneaic/realms/alpha-bravo-realms.html
- Developer SDK entry: https://developer.pingidentity.com/sdks.html
