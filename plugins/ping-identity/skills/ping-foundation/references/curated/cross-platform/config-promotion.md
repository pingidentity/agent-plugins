---
title: "Configuration Promotion Across Environments"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate", "pingaccess", "pingdirectory"]
capabilities: ["foundation"]
services: []
audience: ["admin", "architect", "operator"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-22"
slug: "https://developer.pingidentity.com/config-automation-promotion/configuration_promotion_landing_page.html"
---

# Configuration Promotion Across Environments

How to move Ping Identity configuration between development, staging, and production environments across PingOne, AIC, and Ping Software.

## Scope

**Covers:** Choosing a promotion model; environment topology rules; what promotes vs what does not; promotion variables and ESV placeholders; hard limits and constraints; rollback; GitOps with Ping CLI + Terraform; model selection.

**Does NOT cover:** Journey- and flow-specific promotion concerns — scripted decision node ESV gotchas, DaVinci flow versioning, environment lock impact on running journeys — see `ping-orchestration` → `references/curated/cross-platform/journey-and-flow-promotion.md`. Secret rotation — see `references/curated/cross-platform/core-admin-patterns.md`. Bulk user import and data migration (users, sessions, audit logs are never promoted — only static config moves). Ping CLI install and CRUD — see `references/curated/cross-platform/ping-cli-basics.md`.

---

## Three promotion models

| Model | Applies to | What moves | What does not move | Sequential constraint |
|---|---|---|---|---|
| **PingOne native promotion** | PingOne (multi-tenant cloud) | Applications, DaVinci flows and policies, sign-on policies, and most PingOne resources | Authorize, Credentials, Privilege, runtime user data, sessions, audit logs | Source/target same org; check live docs for current resource scope |
| **AIC self-service promotions** | PingOne Advanced Identity Cloud | Journeys, scripts, themes, AM/IDM static config, ESV references | Live users, sessions, user-created applications, runtime data | Sequential pairs only: dev→staging, staging→production. Non-sequential promotion not supported. |
| **Ping CLI + Terraform (config-as-code)** | PingOne, PingFederate, DaVinci, and supported universal services | Terraform-managed config via Ping Identity Terraform providers | Per-resource, determined by provider support | None — Terraform manages state independently per target environment |

---

## Environment topology

### PingOne

- Source and target must be in the **same PingOne organization**.
- The **Promotion Admin** role (or equivalent) is required in **both** the source and target environment.
- Both environments should expose the **same connected services** — promoting an application that references a service not enabled in the target will fail.
- Check the linked Ping documentation for resource types currently supported by the promotion API.

### AIC

- Promotion chain: **dev → staging → production**. Non-sequential (dev → production) is not supported.
- **Sandbox environments are excluded** from all promotion chains. Sandbox is a separate, isolated tier.
- If **UAT environments** are present, they are inserted into the chain: dev → UAT → staging → production.
- Rollback is available via API; it is not exposed in the admin console.

### Ping Software (PingFederate, PingAccess, PingDirectory)

- Configuration is managed via **server profiles** (Git-backed config-as-code). Promotion = merging and applying a server-profile branch.
- The Ping Identity Terraform providers cover PingFederate, PingAccess, and PingDirectory for state-managed config-as-code.

---

## What promotes vs what does not

| Category | PingOne native | AIC self-service | Terraform/Ping CLI |
|---|---|---|---|
| Applications and OAuth clients | ✓ | ✓ (static; user-created apps excluded) | ✓ |
| Authentication flows / journeys / trees | ✓ (DaVinci flows) | ✓ (AIC journeys and AM config) | ✓ |
| Policies (sign-on, flow) | ✓ | ✓ | ✓ |
| Themes and branding | ✓ | ✓ | ✓ |
| Scripts | n/a | ✓ | ✓ |
| ESV / environment variables | Promotion variables only | ESV references move; secrets must be pre-configured in target | Via Terraform provider variables |
| Users, sessions, audit logs | ✗ never | ✗ never | ✗ never |
| Runtime user data (devices, MFA enrollments) | ✗ never | ✗ never | ✗ never |
| PingOne Authorize, Credentials, Privilege | ✗ excluded | n/a | ✓ (where provider support exists) |

---

## Promotion variables, ESVs, and placeholders

Environment-specific values (connection endpoints, client IDs, URIs) must be externalised before promotion so the config is portable.

| Platform | Mechanism | Key constraint |
|---|---|---|
| PingOne native | **Promotion variables** — named substitution tokens in the exported config | Defined in the source; must be assigned values in the target before applying |
| AIC | **Environment secrets and variables (ESVs)** | ESVs referenced in static config must exist in the upper environment. AIC's integrity check blocks promotion if any ESV is missing or if an encrypted secret is embedded directly in config rather than referenced via an ESV. |
| Terraform | **Terraform input variables / `.tfvars` files per environment** | Standard Terraform pattern; per-environment variable files hold the target-specific values |

---

## Hard limits and constraints

| Platform | Constraint | Details |
|---|---|---|
| PingOne native | 100 resources per promotion (auto-included dependencies excluded from count) | Larger environments require multiple staged promotions |
| PingOne native | Environment lock not required | Source environment remains writable during promotion |
| PingOne native | Rollback restores the most recent promotion's state in the target | Available via admin console and API |
| AIC | **Environment lock required** on source and target during promotion | Blocks ESV API and most admin APIs in the development environment; **authentication flows for end users are unaffected** |
| AIC | Promotions take 10–45 minutes | Service restart in the upper environment is part of the process |
| AIC | Rollback available via API only | Admin console does not expose rollback |
| Ping CLI export | Terraform HCL export scope varies by service | Not all services produce HCL; check the [product compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html) |

For current availability of specific resource types in native PingOne promotion, check the linked Ping documentation — this list changes as the feature evolves.

---

## Rollback

| Platform | Rollback model | How to trigger |
|---|---|---|
| PingOne native | Restores the target environment to its state before the most recent promotion | Admin console → Promote, or Configuration Management API |
| AIC | Restores the upper environment's prior static config set | API only (`POST /promotions/{id}/rollback`) |
| Terraform | `terraform destroy` + revert to prior state file or prior `apply` | Standard Terraform rollback — revert the commit and re-apply |

---

## Choosing a promotion model

For Ping's own guidance on model selection see the [configuration promotion overview](https://developer.pingidentity.com/config-automation-promotion/configuration_promotion_landing_page.html).

| Scenario | Typical fit | Why |
|---|---|---|
| Config lives entirely within one PingOne org; team prefers admin-console workflow | PingOne native promotion | Designed for same-org, in-console use; automatic dependency management; no toolchain required |
| AIC tenant with dev/staging/prod environments | AIC self-service promotions | The platform-provided self-service promotion path for AIC; sequential pairs enforced by the platform (dev→staging→production only) |
| Cross-product (PingOne + PingFederate/PingAccess), cross-org, or Git-backed audit trail needed | Ping CLI + Terraform | Terraform providers cover PingFederate, PingAccess, and PingDirectory; Ping CLI CRUD for PingFederate is still rolling out — check the [compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html); state tracking and drift detection via Terraform |
| Mix of PingOne and AIC in the same pipeline | Can combine both | Native/AIC handles per-platform config; Terraform handles cross-product baseline and long-term state |
| PingFederate configuration between servers | Server profiles (Git) + Terraform provider | PingFederate's native config-as-code model; no equivalent in-console promotion UI |

---

## Prerequisites

- **PingOne native:** Promotion Admin role in both source and target environments; both in the same org.
- **AIC:** AIC tenant admin access in both environments; ESVs pre-configured in the upper environment.
- **Ping CLI / Terraform:** PingOne Worker app with admin roles; PingFederate admin API OAuth client; Terraform CLI; Ping Identity Terraform providers installed.

---

## Common variants

| Variant | Notes |
|---|---|
| Single-org PingOne, console workflow | Use native promotion for quick dev→test iteration; graduate to Terraform for long-term state management |
| AIC standard chain (dev/staging/prod) | Self-service promotions; ESVs must exist in target before promoting |
| AIC with UAT | dev → UAT → staging → production; non-sequential skips not supported |
| Cross-org or multi-tenant | Only Terraform covers this; native promotion is same-org only |
| Community tooling (fr-config-manager, frodo) | Widely used by AIC customers for bespoke config management; not an official Ping product — see their respective GitHub repositories |

---

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| AIC promotion blocked by integrity check | Missing ESV or encrypted secret embedded in config | Create the missing ESV in the upper environment; replace inline secrets with ESV references |
| PingOne promotion fails on service dependency | Target env missing a service the source config references | Enable the service in the target environment before promoting |
| AIC promotion locks admin APIs longer than expected | Large config sets take 10–45 minutes; lock is held throughout | Schedule promotions during low-traffic windows; monitor the promotion status API |
| Rollback restores unexpected state | Multiple promotions in quick succession | Wait for each promotion to complete before running the next; check the promotion history before rollback |
| Terraform provider missing a resource type | Resource not yet in provider support | Check the Ping Terraform provider changelog; use `pingcli pingone api` for a raw read in the interim |

---

## Related references

- `references/curated/cross-platform/ping-cli-basics.md` — Ping CLI install, profiles, and CRUD commands
- `references/curated/cross-platform/core-admin-patterns.md` — secret rotation, API patterns
- `references/curated/pingone-mt/tenant-and-environment-setup.md` — environment setup prerequisites
- `ping-orchestration` → `references/curated/cross-platform/journey-and-flow-promotion.md` — journey, script, and DaVinci flow promotion specifics

---

## Source

- [Configuration promotion overview](https://developer.pingidentity.com/config-automation-promotion/configuration_promotion_landing_page.html)
- [PingOne configuration management](https://docs.pingidentity.com/pingone/early-access-features/ea-p1_promote.html)
- [AIC self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)
- [AIC promotion FAQ](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions-faqs.html)
- [AIC configuration placeholders (ESVs)](https://docs.pingidentity.com/pingoneaic/tenants/configuration-placeholders.html)
- [Ping Terraform provider](https://terraform.pingidentity.com)
