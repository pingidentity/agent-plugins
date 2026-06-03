# Platform Families

Canonical product-family definitions used by all skills for routing decisions.
Every skill routes to one of these families before selecting a reference tier.

## PingOne MT Platform

Cloud-hosted administration surface: environment setup, tenant management, apps, directories, and policies.

**Products:** PingOne, PingOne MFA, PingOne Risk, PingOne Notifications, PingOne Credentials, PingOne Verify, PingOne Protect, PingOne SSO, PingOne IGA, PingOne Neo, PingOne Authorize

**Routing tag:** `pingone-mt`

## PingOne ST

Fully managed identity platform built on PingAM/ForgeRock lineage. Distinct control plane, object model, and administration UI from PingOne MT.

**Products:** PingOne ST, PingAM (within PingOne ST), PingIDM (within PingOne ST), PingDS (within PingOne ST)

**Routing tag:** `pingone-st`

## Ping Software Suite (On-Premises)

On-premises and self-managed deployments. Different deployment model, topology, and operational patterns from cloud families.

**Products:** PingFederate, PingAccess, PingDirectory, PingDataSync, PingID (on-prem), PingAM (standalone), PingIDM (standalone), PingDS (standalone), PingAuthorize

**Routing tag:** `ping-software`

## Shared / Cross-Platform

Universal Services and patterns that span multiple platform families. Used when capability is invoked from both PingOne MT and PingOne ST contexts.

**Services:** PingOne Protect, PingOne Verify, PingOne Credentials, PingOne SSO, PingOne IGA, PingOne Neo, PingOne Authorize

**Routing tag:** `cross-platform`

---

## Decision Rule

Apply platform family routing before any capability or product routing:

1. Is the user working in PingOne admin console or PingOne APIs? → `pingone-mt`
2. Is the user working in PingOne ST tenant admin, identity cloud, or AM/IDM/DS? → `pingone-st`
3. Is the user deploying, configuring, or operating on-prem software? → `ping-software`
4. Is the service invoked across both PingOne MT and PingOne ST? → `cross-platform`
