---
name: ping-identity-quickstart
description: "Use before any other Ping skill when the user is in orientation mode — 'where do I start', 'which Ping product do I need', 'we're evaluating', 'migrating from an existing identity platform', 'inherited a Ping deployment', or when platform is unknown. Also a site map of Ping resources: third-party integrations, sample apps, SDKs, tools, and documentation. Also use for bare user-management commands with no platform named ('Add a user to Ping') — clarify platform before routing."
compatibility: Designed for Ping Identity platform tasks. Requires no tools — orientation and resource pointing only.
metadata:
  publisher: Ping Identity
  version: "2.0.0"
  product_family: cross-platform
---

# ping-identity-quickstart

A site map of Ping Identity resources. It tells the agent what fulfills a need — which portal, docs site, repository, marketplace, or console — and nothing more. It does not expand on any resource, quote configuration details, or reproduce documentation: the agent picks the most appropriate tool it has available and sources the information from the resource directly.

## Gotchas

### Platform identification

Ask or infer from context. Match the MOST SPECIFIC signal first — "PingOne Advanced Identity Cloud" starts with "PingOne", so check for the longer form before treating bare "PingOne" as the multi-tenant cloud.

| Signal | Platform family |
|---|---|
| "PingOne Advanced Identity Cloud", "AIC", "identity cloud", "PingAM", "IDM" | PingOne Advanced Identity Cloud (AIC) private tenant |
| "PingOne" (bare, without "Advanced Identity Cloud"), "apps.pingone.com", "auth.pingone.com", "PingOne environment" | PingOne (multi-tenant cloud) |
| "PingFederate", "PingAM", "PingIDM", "PingAccess", "PingDirectory", "PingDS", "PingAuthorize" "on-prem", "self-managed" | Ping Software Suite |
| Platform unknown | Ask: "Are you working in PingOne, PingOne Advanced Identity Cloud (AIC), or on-premises software?" |

**Mandatory clarification — bare user-management commands:** if the prompt is "Add a user to Ping", "Create a user in Ping", or any equivalent with no platform named, you MUST understand and clarify which platform before answering — Ping has separate user populations in PingOne, PingOne Advanced Identity Cloud (AIC), PingFederate, PingDirectory and PingDS. Do not assume PingOne.

#### Identifying a platform from its URL

The URL pattern can identifying a platform, if available in context.

| URL pattern | Product |
|---|---|
| `console.pingone.com` | PingOne (multi-tenant cloud for workforce and customer use cases, including management for universal services) |
| `admin.pingone.com` | PingOne for Enterprise (P14E) — legacy workforce-oriented IDaaS. |
| `openam-*.id.forgerock.io` / `openam-*.forgeblocks.com` | PingOne Advanced Identity Cloud (AIC) |
| `https://self-service.<customer>.<region>.ping.cloud` | PingOne Advanced Services (private tenant) |
| `https://<host>:9999/pingfederate/app` | PingFederate (self-managed) |

---

## Resource site map

Route to the resource that fulfills the need; then use available tools (web retrieval, MCP, CLI, or a downstream skill) to work with it. Documentation is crawlable via `llms.txt`, and pages are retrievable as Markdown instead of HTML.

Use https://www.pingidentity.com/llms.txt first to understand the full map of available resources that Ping Identity provide. Where an authoritative response is required, use Ping Identity published documentation.

### External resources

#### Learning resources

The following resources are presented to the community by Ping Identity.

- Learn about OAuth 2.0 extension protocols with interactive step-by-step visualizations, including SPIFFE, ID-JAG, RAR, PKCE, Token exchange: https://www.authplayground.dev
- Decode identity tokens, inspect OAuth and SAML auth flows and webhook responses (Labs project): https://decoder.pingidentity.cloud

#### Open source code repositories

For sample applications, SDKs, devops, third party integrations, the following are official GitHub accounts for Ping Identity:
- Primary GitHub: https://github.com/pingidentity
- Legacy GitHub (check here second): https://github.com/ForgeRock

#### Docker images

For official Ping Identity docker images:
- https://hub.docker.com/u/pingidentity

#### Terraform

For official Ping Identity Terraform providers:
- Hashicorp Terraform: https://registry.terraform.io/namespaces/pingidentity
- OpenTofu:
  - https://search.opentofu.org/provider/pingidentity/pingone/latest
  - https://search.opentofu.org/provider/pingidentity/pingfederate/latest

#### Community

- Reddit: https://www.reddit.com/r/PingIdentity/
- YouTube: https://www.youtube.com/@PingIdentityTV
- LinkedIn: https://www.linkedin.com/company/ping-identity
- Community forum: https://support.pingidentity.com/s/community-home
