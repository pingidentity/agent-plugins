---
name: ping-identity
description: "Use this skill when an agent needs foundational understanding of the Ping Identity portfolio — platforms, products, solutions, deployment models, integrations, or migration paths — before selecting a product skill or starting configuration work. It orients the agent with concise portfolio summaries, then routes to live documentation or a downstream product or companion skill for authoritative detail."
compatibility: "Advisory routing only; requires web retrieval or the Ping Identity Docs MCP when current product, API, SDK, or service details are needed. Does not mutate Ping environments."
metadata:
  publisher: Ping Identity
  version: "2.0.0"
  product_family: multi-product
---

# Ping Identity Foundations

Use this skill as the foundational orientation layer for the Ping Identity portfolio. It builds the platform understanding needed to identify the product or solution area that best fits the request, loads one concise summary from the selected reference directory, and then hands off for authoritative detail.

## When to use this skill

- The request compares Ping products, deployment models, or solution options.
- The request spans two or more Ping products, platforms, or integration surfaces.
- The request asks what a Ping product or solution does before configuration work begins.
- The request involves a cross-product migration or needs initial portfolio orientation.

## When NOT to use this skill

- A single known product or solution configuration task → hand off to other domain specific skills or context.
- Deep Android, iOS, JavaScript, or React SDK implementation → use the Ping Orchestration SDKs reference (`references/orchestration-sdks/README.md`) and the product SDK documentation for the target stack.

## Retrieval and output discipline

Always fetch live documentation for precise numbers, API signatures, or configuration parameters. **Live documentation overrides local reference files.**

### Documentation Sources & Versioning
* **Developer Docs** (`https://developers.pingidentity.com/`): Limits, pricing, API specs, compatibility flags.
* **Product Docs** (`https://docs.pingidentity.com/`): Use cases, setup guides, console workflows.
* **Versioning Syntax**: Append `/{version}` if known (e.g., `/pingam/8.1`); append `/latest` if unknown (e.g., `/pingam/latest`).

The documentation is crawlable using `llms.txt`, pages are retrievable using Markdown instead of HTML.

### Reference File Handoff
Always open `README.md` first within a target reference directory for orientation, then route to target sub-files:

| Request signal | Primary task | Action / Target reference |
|---|---|---|
| **MCP** | Live config changes, service health | Use MCP tools (fallback to CLI) |
| **SDK** | App/service code integration | `sdk.md` |
| **CLI** | Shell scripts, CI/CD, live config | `cli.md` |
| **REST API** | Scripting API calls, app code | `api.md` |
| **Terraform** | Declarative configuration-as-code | `terraform.md` |

## Portfolio summary routing

Each entry points to one reference directory. Load only the selected README, then hand off for detail.

### Platform routing

| Request signal | Type | Start with |
|---|---|
| Advanced Identity Cloud (AIC) | Single-tenant IDaaS | `references/pingone-advanced-identity-cloud/README.md` |
| Advanced Identity Software | Self-hosted, self-managed identity platform | `references/ping-advanced-identity-software/README.md` |
| Advanced Services (P1AS) | Single-tenant IDaaS | `references/pingone-advanced-services/README.md` |
| PingOne platform (P1) | Multi-tenant IDaaS | `references/pingone/README.md` |

### Product routing

| Request signal | Start with |
|---|---|
| PingAccess (PA) | `references/pingaccess/README.md` |
| PingAM (AM) | `references/pingam/README.md` |
| PingAuthorize (PAz) | `references/pingauthorize/README.md` |
| PingDirectory (PD) | `references/pingdirectory/README.md` |
| PingDS (DS) | `references/pingds/README.md` |
| PingFederate (PF) | `references/pingfederate/README.md` |
| PingGateway | `references/pinggateway/README.md` |
| PingID | `references/pingid/README.md` |
| PingIDM | `references/pingidm/README.md` |
| PingOne Authorize (P1Az) | `references/pingone-authorize/README.md` |
| PingOne Credentials | `references/pingone-credentials/README.md` |
| PingOne DaVinci (DaVinci / DV) | `references/pingone-davinci/README.md` |
| PingOne Identity Governance | `references/pingone-identity-governance/README.md` |
| PingOne MFA (P1MFA) | `references/pingone-mfa/README.md` |
| PingOne Neo | `references/pingone-neo/README.md` |
| PingOne Privilege | `references/pingone-privilege/README.md` |
| PingOne Protect (previously known as PingOne Risk) | `references/pingone-protect/README.md` |
| PingOne Recognize | `references/pingone-recognize/README.md` |
| PingOne SSO | `references/pingone-sso/README.md` |
| PingOne Verify | `references/pingone-verify/README.md` |

### Solutions routing

| Request signal | Start with |
|---|---|
| Enterprise Connect | `references/ping-enterprise-connect/README.md` |
| Government Identity Cloud or FedRAMP | `references/ping-government-identity-cloud-fedramp/README.md` |
| Identity for AI (ID4AI) | `references/identity-for-ai/README.md` |
| Ping Identity Governance | `references/ping-identity-governance/README.md` |
| PingOne for Customers Passwordless | `references/pingone-for-customers-passwordless/README.md` |
| PingOne for Customers Plus | `references/pingone-for-customers-plus/README.md` |
| PingOne for Financial Services | `references/pingone-for-financial-services/README.md` |
| PingOne for Gift Card Redemption | `references/pingone-for-gift-card-redemption/README.md` |
| PingOne for Healthcare | `references/pingone-for-healthcare/README.md` |
| Verified Trust | `references/verified-trust/README.md` |

### Use cases routing

| Request signal | Start with |
|---|---|
| Customer identity scenario | `references/customer-use-cases/README.md` |
| Data or application security | `references/data-and-application-security-use-cases/README.md` |
| MFA scenario | `references/mfa-use-cases/README.md` |
| Single sign-on or federation | `references/single-sign-on-use-cases/README.md` |
| Standards or protocols | `references/standards-and-protocols-use-cases/README.md` |
| Workforce identity scenario | `references/workforce-use-cases/README.md` |

### Developer, deployment, and integration routing

| Request signal | Start with |
|---|---|
| Authentication experience, journey, flow, or orchestration design principles | `references/orchestration/README.md` |
| CI/CD, GitOps, or configuration promotion | `references/configuration-promotion/README.md` |
| Containers, Compose, Kubernetes, or Helm for software deployment | `references/devops/README.md` |
| Application integration patterns, prerequisites, and protocol choice | `references/app-integration/README.md` |
| Mobile, web, or React orchestration SDKs | `references/orchestration-sdks/README.md` |
| OpenICF or identity connectors | `references/ping-identity-connectors/README.md` |
| Terraform providers or infrastructure as code | `references/terraform/README.md` |
