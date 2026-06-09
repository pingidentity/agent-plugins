# Platform Scope — Ping Identity Plugin

Defines which platforms, products, and services are in scope. Use for platform detection when `/shared/taxonomies/platform-families.md` is not available.

## Platform Families

| Tag | Platform | Description |
|---|---|---|
| `pingone-mt` | PingOne (multi-tenant cloud) | SaaS-hosted administration: environments, apps, directories, policies. Admin at apps.pingone.com. |
| `pingone-st` | PingOne Advanced Identity Cloud (AIC) | Fully managed, highly customizable. Built on PingAM/PingIDM/PingDS. Distinct control plane from PingOne. |
| `ping-software` | Ping Software Suite (on-premises) | Customer-deployed server software. Different topology, ops model, and config surface from cloud families. Includes PingAM, PingIDM, PingDS, PingGateway, PingFederate, etc. |
| `cross-platform` | Shared / Universal Services | Capabilities consumed across multiple platform families (Protect, Verify, IGA, etc.). |

## Platform Detection Signals

**`pingone-mt`**
- "Multi-Tenant"
- "PingOne", "apps.pingone.com", "PingOne environment", "PingOne admin console"
- PingOne MFA, PingOne Risk, PingOne DaVinci, PingOne Verify, PingOne Protect, PingOne IGA, PingOne Credentials, PingOne Neo, PingOne Authorize, PingOne SSO

**`pingone-st`**
- "Single-Tenant"
- "AIC", "identity cloud tenant", "PingAM", "PingIDM", "PingDS"
- "ForgeRock", "AM", "IDM", "DS" (in an AIC Cloud context), AIC tenant URL
- Journeys, auth trees, realms

**`ping-software`**
- "On-prem", "Software", "Download", "Binary", ".jar", "PingFederate", "PingAccess", "PingDirectory", "PingDataSync", "PingID on-prem", "PingAM standalone", "on-prem", "self-managed", "server profile"

**`cross-platform`**
- Service invoked from both PingOne (multi-tenant cloud) and AIC contexts
- Universal Services layer questions (not product-specific setup)

## Products in Scope

### PingOne (multi-tenant)
PingOne, PingOne MFA, PingOne Risk, PingOne DaVinci, PingOne Verify, PingOne Protect, PingOne IGA, PingOne Credentials, PingOne Neo, PingOne Authorize, PingOne SSO, PingOne Notifications

### AIC
AIC, PingAM (within AIC), PingIDM (within AIC), PingDS (within AIC)

### Ping Software Suite
PingFederate, PingAccess, PingDirectory, PingDataSync, PingID (on-prem), PingAM (standalone), PingIDM (standalone), PingDS (standalone), PingAuthoriz, PingGateway

## Services Out of Scope for This Plugin

- Non-Ping identity providers
- Generic OIDC/SAML implementations not using a Ping product
- Cloud infrastructure (AWS, GCP, Azure) beyond what Ping software runs on
